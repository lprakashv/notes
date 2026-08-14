# Amazon Bedrock

## What it provides

!!! info "AI-generated"

Amazon Bedrock is a managed AWS service for invoking foundation models with AWS
controls such as IAM, encryption, and logging.

The managed building blocks include:

- model inference and evaluation;
- Knowledge Bases for retrieval-augmented generation (RAG);
- Guardrails for input and output controls;
- Agents for coordinating models, knowledge bases, and action APIs.

Model availability, features, quotas, and pricing vary by AWS Region, so verify
them before choosing an architecture.

## Request path

!!! info "AI-generated"

1. Authenticate with an IAM role and call a selected model.
2. Optionally apply Guardrails and retrieve context from a Knowledge Base.
3. Generate a response.
4. Validate it before display or action.

Keep model calls behind an application boundary. That is the right place for
timeouts, retries, cost limits, input validation, authorization, and audit logs.

## Security checklist

!!! info "AI-generated"

- Grant only the model and API actions the workload needs.
- Treat prompts, retrieved documents, and tool output as sensitive or untrusted.
- Enforce authorization in application code, not only in prompts.
- Test guardrails and audit decisions without logging secrets.

Further reading: [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html),
[Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html), and
[Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html).
