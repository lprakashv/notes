# Enhancing RAG with RAPTOR

## Core idea

!!! info "AI-generated"

RAPTOR—Recursive Abstractive Processing for Tree-Organized Retrieval—builds a
hierarchy over document chunks. Nearby chunks are clustered, summarized, and
then clustered again. Retrieval can search both detailed leaves and higher-level
summaries, helping with questions that span several passages.

## Indexing flow

!!! info "AI-generated"

1. Split documents into leaf chunks with source metadata.
2. Embed and cluster related chunks.
3. Summarize each cluster into a parent node; repeat as needed.
4. Store the tree with source lineage.

~{RAPTOR indexing and retrieval tree}(<raptor-index-and-retrieve.json> "Chunks are recursively clustered and summarized; retrieval searches leaves and summaries while retaining source lineage.")

At query time, either search all levels together or traverse from broad nodes to
their most relevant children. The second approach can reduce search space but is
more sensitive to an early routing mistake.

## Trade-offs and evaluation

!!! info "AI-generated"

- Summaries cost more to build and may omit details.
- Updates may require regenerating ancestor nodes.
- Keep citations to original chunks and compare with a flat or hybrid baseline.

Evaluate retrieval recall separately from answer quality. Compare against a flat
chunk baseline using the same corpus, questions, model, and token budget.

Source: [RAPTOR paper](https://arxiv.org/abs/2401.18059).
