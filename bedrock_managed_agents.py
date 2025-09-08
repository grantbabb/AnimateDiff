import json
import os
from typing import Any, Dict, Optional

import boto3
from botocore.config import Config
import click
from rich.console import Console
from rich.panel import Panel


console = Console()


def get_bedrock_clients(region_name: Optional[str] = None):
	region = region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
	if not region:
		raise RuntimeError("AWS region not set. Provide --region or set AWS_REGION/AWS_DEFAULT_REGION.")
	return (
		boto3.client("bedrock", region_name=region, config=Config(retries={"max_attempts": 10})),
		boto3.client("bedrock-runtime", region_name=region, config=Config(retries={"max_attempts": 10})),
	)


@click.group()
def cli():
	"""Scripts to create and invoke an Agent for Amazon Bedrock."""
	pass


@cli.command("create-agent")
@click.option("--name", required=True, help="Agent name")
@click.option("--foundation-model", required=True, help="Model ID, e.g., anthropic.claude-3-5-sonnet-20240620-v1:0")
@click.option("--instruction", required=True, help="System prompt / instruction for the agent")
@click.option("--region", default=lambda: os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "", help="AWS region")
def create_agent(name: str, foundation_model: str, instruction: str, region: str):
	bedrock, _ = get_bedrock_clients(region)
	resp = bedrock.create_agent(
		agentName=name,
		foundationModel=foundation_model,
		instruction=instruction,
		offGuardrail=False,
	)
	agent_id = resp["agent"].get("agentId")
	console.print(Panel.fit(f"Created agent: {agent_id}", title="Create Agent"))
	console.print(json.dumps(resp, indent=2))


@cli.command("prepare-agent")
@click.option("--agent-id", required=True, help="Agent ID from create-agent")
@click.option("--region", default=lambda: os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "", help="AWS region")
def prepare_agent(agent_id: str, region: str):
	bedrock, _ = get_bedrock_clients(region)
	resp = bedrock.prepare_agent(agentId=agent_id)
	console.print(Panel.fit(f"Preparing agent: {agent_id}", title="Prepare Agent"))
	console.print(json.dumps(resp, indent=2))


@cli.command("invoke-agent")
@click.option("--agent-id", required=True, help="Agent ID")
@click.option("--input-text", required=True, help="User input")
@click.option("--session-id", default=None, help="Optional session ID for continuity")
@click.option("--region", default=lambda: os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "", help="AWS region")
def invoke_agent(agent_id: str, input_text: str, session_id: Optional[str], region: str):
	bedrock, bedrock_runtime = get_bedrock_clients(region)
	resp = bedrock_runtime.invoke_agent(agentId=agent_id, sessionId=session_id or "session-1", inputText=input_text)
	completion = resp.get("completion")
	console.print(Panel.fit(completion or "(no content)", title="Agent Response"))


if __name__ == "__main__":
	cli()

