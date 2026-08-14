# Building Systems with ChatGPT AI

## Start with a small contract

!!! info "AI-generated"

Define the task before tuning the prompt:

- input, context, and expected output schema;
- actions and tools the model may use;
- hard safety, privacy, cost, and latency limits;
- examples of success and important failure cases.

Treat model output as untrusted: validate it, authorize side effects in code, and
require human approval for consequential actions.

## A practical request pipeline

!!! info "AI-generated"

1. Validate input and retrieve only relevant context.
2. State one objective, its constraints, and the output contract.
3. Run allowed tools with timeouts and least privilege.
4. Validate the result and record a privacy-safe trace.

Keep calculations, permissions, and state transitions in deterministic code.

## Evaluation before optimization

!!! info "AI-generated"

Use a small, reviewed evaluation set covering normal requests, ambiguity, missing
context, prompt injection, tool failures, and abstention. Compare task success
before latency, token use, and cost.

Further reading: [OpenAI prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)
and [evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices).
