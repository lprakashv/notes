# LangSmith

## Purpose

!!! info "AI-generated"

LangSmith traces, evaluates, and monitors model applications, with or without
LangChain. A useful trace captures prompts, models, tools, latency, and errors—
but not secrets or unnecessary personal data.

## Evaluation workflow

!!! info "AI-generated"

1. Build a reviewed dataset of representative inputs.
2. Run a fixed application version against it.
3. Score with deterministic checks, humans, or calibrated model evaluators.
4. Compare task success, critical slices, latency, errors, and cost.

Model-based evaluators are useful for fuzzy criteria, but they are measurements,
not ground truth. Calibrate them against human labels and inspect disagreements.

## Operational use

!!! info "AI-generated"

- Tag traces with application version, prompt version, model, and environment.
- Sample high-volume traffic while retaining failures and unusual paths.
- Turn repeated production failures into regression examples.
- Define retention and redaction policies before sending trace payloads.

Further reading: [LangSmith evaluation concepts](https://docs.langchain.com/langsmith/evaluation-concepts)
and [observability concepts](https://docs.langchain.com/langsmith/observability-concepts).
