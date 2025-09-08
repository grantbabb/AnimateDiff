import json
import os
from typing import Any, Dict, List, Callable, Optional, Tuple

import boto3
from botocore.config import Config
import click
from rich.console import Console
from rich.panel import Panel


console = Console()


def get_bedrock_runtime_client(region_name: Optional[str] = None):
	region = region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
	if not region:
		raise RuntimeError("AWS region not set. Provide --region or set AWS_REGION/AWS_DEFAULT_REGION.")
	return boto3.client("bedrock-runtime", region_name=region, config=Config(retries={"max_attempts": 10}))


def get_default_model_id() -> str:
	# Popular high-quality model on Bedrock; change if your account lacks access
	return os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")


class Tool:
	def __init__(self, name: str, description: str, json_schema: Dict[str, Any], impl: Callable[[Dict[str, Any]], Dict[str, Any]]):
		self.name = name
		self.description = description
		self.json_schema = json_schema
		self.impl = impl

	def to_tool_spec(self) -> Dict[str, Any]:
		return {
			"toolSpec": {
				"name": self.name,
				"description": self.description,
				"inputSchema": {"json": self.json_schema},
			}
		}


def get_weather_impl(args: Dict[str, Any]) -> Dict[str, Any]:
	city = str(args.get("city", ""))
	unit = str(args.get("unit", "c")).lower()
	if unit not in {"c", "f"}:
		unit = "c"
	# Dummy data; in real use, call a weather API here
	base_temp_c = 22.3
	if unit == "f":
		temp = base_temp_c * 9 / 5 + 32
	else:
		temp = base_temp_c
	return {"city": city, "unit": unit, "temperature": round(temp, 1), "conditions": "Sunny"}


def build_tool_registry() -> Dict[str, Tool]:
	return {
		"get_weather": Tool(
			name="get_weather",
			description="Get current weather for a city.",
			json_schema={
				"type": "object",
				"properties": {
					"city": {"type": "string", "description": "City name, e.g., London"},
					"unit": {"type": "string", "enum": ["c", "f"], "default": "c"},
				},
				"required": ["city"],
			},
			impl=get_weather_impl,
		),
	}


def extract_tool_uses_from_content(content: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
	tool_uses: List[Dict[str, Any]] = []
	for block in content:
		if "toolUse" in block:
			tool_uses.append(block["toolUse"])
	return tool_uses


def build_tool_results(tool_uses: List[Dict[str, Any]], registry: Dict[str, Tool]) -> List[Dict[str, Any]]:
	results: List[Dict[str, Any]] = []
	for tu in tool_uses:
		name = tu.get("name")
		tool_use_id = tu.get("toolUseId")
		inputs = tu.get("input") or {}
		impl = registry.get(name)
		if not impl:
			results.append({
				"toolResult": {
					"toolUseId": tool_use_id,
					"content": [{"text": f"Tool '{name}' not implemented."}],
					"status": "error",
				}
			})
			continue
		try:
			output_json = impl.impl(inputs)
			results.append({
				"toolResult": {
					"toolUseId": tool_use_id,
					"content": [{"json": output_json}],
					"status": "success",
				}
			})
		except Exception as exc:  # pragma: no cover (defensive)
			results.append({
				"toolResult": {
					"toolUseId": tool_use_id,
					"content": [{"text": f"Tool '{name}' failed: {exc}"}],
					"status": "error",
				}
			})
	return results


def run_converse_agent(prompt: str, model_id: Optional[str] = None, region: Optional[str] = None, system_prompt: Optional[str] = None) -> Tuple[str, List[Dict[str, Any]]]:
	client = get_bedrock_runtime_client(region)
	model = model_id or get_default_model_id()
	tools = build_tool_registry()
	tool_config = {"tools": [t.to_tool_spec() for t in tools.values()]}
	system_blocks = [{"text": system_prompt or "You are a concise, helpful agent. Use tools when beneficial."}]
	messages: List[Dict[str, Any]] = [{"role": "user", "content": [{"text": prompt}]}]

	final_text: str = ""
	for _ in range(5):
		resp = client.converse(modelId=model, system=system_blocks, toolConfig=tool_config, messages=messages)
		assistant_msg = resp.get("output", {}).get("message", {})
		stop_reason = resp.get("stopReason")
		content = assistant_msg.get("content", [])

		# Gather any assistant text so far
		for block in content:
			if "text" in block:
				final_text += block["text"]

		tool_uses = extract_tool_uses_from_content(content)
		if tool_uses:
			results = build_tool_results(tool_uses, tools)
			messages.append(assistant_msg)
			messages.append({"role": "user", "content": results})
			continue

		# If no tool use requested, or completed after tool results
		if stop_reason in {"end_turn", "max_tokens"} or not tool_uses:
			break

	return final_text.strip(), messages


@click.command()
@click.option("--prompt", required=True, help="User prompt to send to the agent")
@click.option("--model-id", default=lambda: get_default_model_id(), show_default=True, help="Bedrock model ID")
@click.option("--region", default=lambda: os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "", help="AWS region")
def main(prompt: str, model_id: str, region: str):
	"""Run a lightweight agent loop on Bedrock using the Converse API."""
	final_text, _ = run_converse_agent(prompt=prompt, model_id=model_id or None, region=region or None)
	console.print(Panel.fit(final_text or "(no content)", title="Assistant", subtitle=model_id))


if __name__ == "__main__":
	main()

