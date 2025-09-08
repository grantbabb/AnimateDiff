# AWS Bedrock Agent Examples

Two approaches are included:

- Converse API lightweight agent with tool use: `bedrock_converse_agent.py`
- Managed Agents for Bedrock scripts: `bedrock_managed_agents.py`

## Setup

1) Python deps

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2) AWS credentials

- Configure credentials with permissions for `bedrock` and `bedrock-runtime`.
- Set `AWS_REGION` or `AWS_DEFAULT_REGION`.
- Optionally set `BEDROCK_MODEL_ID` to override the default model.

## Converse API agent

Run a prompt through a small agent loop with a demo tool `get_weather`.

```bash
python bedrock_converse_agent.py --prompt "What's the weather in London in F?"
```

Options:

- `--model-id`: override model (default: `anthropic.claude-3-5-sonnet-20240620-v1:0`)
- `--region`: AWS region override

## Managed Agents for Bedrock

Create, prepare, and invoke a managed Agent.

```bash
# Create agent
python bedrock_managed_agents.py create-agent \
  --name demo-agent \
  --foundation-model anthropic.claude-3-5-sonnet-20240620-v1:0 \
  --instruction "You are a helpful assistant."

# Prepare (deploy) agent
python bedrock_managed_agents.py prepare-agent --agent-id <AGENT_ID>

# Invoke agent
python bedrock_managed_agents.py invoke-agent --agent-id <AGENT_ID> --input-text "Hello"
```

Notes:

- Ensure your account has access to the chosen foundation model.
- For production, add tools/knowledge bases/guardrails to the managed agent as needed.