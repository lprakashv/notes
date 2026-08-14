# LangChain

## What it is

!!! info "AI-generated"

LangChain is an open-source framework for combining models with tools, retrieval,
structured output, and agents. Use it when those integrations remove more
complexity than they add; otherwise, prefer a direct model call.

## Core pieces

!!! info "AI-generated"

- **Models and messages** normalize generation, tool calls, and conversation turns.
- **Tools** pair a callable operation with a name, description, and input schema.
- **Retrievers** return relevant documents for a query.
- **Agents** let a model choose and call tools in a bounded loop.
- **Middleware** adds guardrails, state, retries, or observability.

Current LangChain agents use LangGraph as their underlying graph runtime. Reach
for LangGraph directly when the workflow needs explicit state, branching,
durability, or human checkpoints.

## Production habits

!!! info "AI-generated"

- Pin versions and keep tool schemas small.
- Enforce authentication and authorization inside tools.
- Bound steps, retries, time, and spend.
- Trace and evaluate complete outcomes; keep fixed steps deterministic.

Further reading: [LangChain overview](https://docs.langchain.com/oss/python/langchain/overview)
and [retrieval](https://docs.langchain.com/oss/python/langchain/retrieval).
