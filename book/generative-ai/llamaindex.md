# LlamaIndex

## What it is

!!! info "AI-generated"

LlamaIndex connects model applications to private or domain data through
ingestion, indexing, retrieval, query workflows, and agents.

## Data path

!!! info "AI-generated"

- **Documents and nodes** represent source items and retrievable units.
- An **index** organizes nodes; a vector index is one option.
- A **retriever** selects nodes for a query.
- A **query engine** coordinates retrieval and response synthesis.

Keep stable document identifiers and source metadata through every stage. Without
them, citations, deletion, access control, and incremental re-indexing become
fragile.

## Retrieval checklist

!!! info "AI-generated"

1. Start with a lexical or flat-vector baseline.
2. Tune chunking to document structure.
3. Filter by tenant and permission before retrieval.
4. Evaluate retrieved evidence, not only final-answer fluency.
5. Version the index, embeddings, parser, and prompt.

Further reading: [LlamaIndex high-level concepts](https://developers.llamaindex.ai/python/framework/getting_started/concepts/).
