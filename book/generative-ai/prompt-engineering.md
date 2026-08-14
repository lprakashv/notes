# ChatGPT Prompt Engineering

## A useful prompt contract

!!! info "AI-generated"

A strong prompt usually states:

1. outcome and audience;
2. necessary context;
3. constraints and approval boundaries;
4. required evidence and output format.

State each instruction once. Keep examples when they encode a real product rule
or repair a measured failure; remove decorative prose and repeated reminders.

```text
Summarize the incident for an engineering manager.

Use only the attached timeline. Lead with impact and current status, then list
the three most important contributing factors and the next owner/action/date.
If a fact is missing, say "unknown". Use at most 180 words.
```

## Grounding and uncertainty

!!! info "AI-generated"

- Separate instructions from untrusted documents or user-supplied content.
- Require evidence and define what to do when sources disagree or are incomplete.
- Keep authorization, secrets, calculations, and strict validation in code.

## Improve with evaluations

!!! info "AI-generated"

Keep reviewed examples, change one prompt element at a time, and rerun the same
evaluation. Version production prompts; validate machine-readable output against
a schema.

Further reading: [OpenAI prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)
and [evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices).
