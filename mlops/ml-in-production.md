# ML in Production

## The production loop

!!! info "AI-generated"

A model is only one part of a production ML system. The surrounding loop is:

1. define the decision and success metric;
2. validate representative data and train reproducibly;
3. evaluate against a baseline and important slices;
4. deploy with a rollback path;
5. monitor outcomes and retrain only when evidence supports it.

## Offline and online evaluation

!!! info "AI-generated"

Offline metrics are fast and repeatable, but they are proxies. A higher accuracy,
F1 score, or ranking metric does not automatically improve the product outcome.
Before launch, compare with a simple baseline and inspect slices where mistakes
have unequal cost. After launch, use a controlled experiment or shadow traffic
when practical.

Keep three kinds of checks separate:

- **model quality:** prediction performance and calibration;
- **data quality:** schema, ranges, missing values, and drift;
- **service quality:** latency, throughput, availability, and cost.

## Safe deployment

!!! info "AI-generated"

- Version the model, preprocessing, and feature definitions together.
- Check training-serving parity.
- Start with shadow or canary traffic and keep a rollback ready.
- Record model/feature versions; watch for feedback-loop data.

## Monitoring drift

!!! info "AI-generated"

Input drift means the feature distribution changed. Concept drift means the
relationship between inputs and the desired outcome changed. Neither proves that
the model is worse. Use drift as a signal to investigate, then confirm with
ground-truth outcomes when they arrive.

Further reading: [Google's Rules of ML](https://developers.google.com/machine-learning/guides/rules-of-ml).
