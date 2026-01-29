
---

## End-to-end flow (how a request moves through your app)

### 0) App startup

1. `uvicorn app.main:app --reload`
2. `app/main.py` boots FastAPI and mounts routers from `app/api/*`
3. `core/config.py` loads env vars (Qdrant URL, collection, model names, etc.)
4. `core/logging.py` configures structured logs

---

## 1) Runtime flow: Ask a question (RAG)

### Client → `POST /ask`

**Flow:**

1. `api/ask.py`

   * validates request body (question, top_k, filters optional)
   * calls the RAG service layer
2. `services/rag_chain.py`

   * orchestrates the RAG pipeline:

     * embeds query (via `services/embeddings.py`)
     * retrieves chunks (via `services/qdrant_store.py`)
     * builds prompt + calls LLM (via `services/llm.py`)
     * returns final answer + citations
3. Response goes back through `api/ask.py` to client (often: answer, sources, timings)

✅ This is your “production path”.

---

## 2) Offline/ops flow: Ingest documents (build knowledge base)

### Client → `POST /ingest` (or CLI calling ingest service)

**Flow:**

1. `api/ingest.py`

   * receives ingestion job request (files/folder/url options)
   * calls ingestion service
2. `services/ingestion.py`

   * loads docs, cleans text, chunks them
   * generates embeddings for chunks (`services/embeddings.py`)
   * upserts to Qdrant (`services/qdrant_store.py`)
3. returns counts: docs_loaded, chunks_created, vectors_upserted

✅ This is your “data plane”.

---

## 3) LLMOps flow: Evaluate quality (RAGAS + golden set)

### Client → `POST /eval` (or run eval route)

**Flow:**

1. `api/eval.py`

   * takes dataset reference (golden set), config knobs (top_k, model, etc.)
   * calls evaluation service
2. `services/eval_ragas.py`

   * runs RAGAS metrics:

     * context precision/recall
     * faithfulness
     * answer relevance
   * uses:

     * your RAG pipeline (`services/rag_chain.py`) to generate answers
     * your LLM (`services/llm.py`) as judge (if configured)
3. returns a report: scores + per-question breakdown

✅ This is your “quality & reliability loop”.

---

## 4) Utility flows

### Health check

* `GET /health` → `api/health.py`
* returns `{ ok: true, version, qdrant_status? }`

---

# What each file does (exactly)

## `app/main.py`

**Role:** Application entrypoint
**Responsibilities:**

* create FastAPI instance
* register routers:

  * `health.py`, `ask.py`, `ingest.py`, `eval.py`
* possibly add middleware (CORS, request-id, timing)
* initializes logging config

---

## `app/api/health.py`

**Role:** Readiness/liveness endpoint
**Responsibilities:**

* `GET /health`
* optionally checks:

  * Qdrant connectivity
  * env configuration sanity

---

## `app/api/ask.py`

**Role:** Public RAG endpoint
**Responsibilities:**

* request validation schema (question, top_k, filters)
* calls `services/rag_chain.py`
* formats response (answer + sources + metadata)

---

## `app/api/ingest.py`

**Role:** Public ingestion endpoint
**Responsibilities:**

* takes ingestion source config (folder, file list, url list)
* calls `services/ingestion.py`
* returns ingestion summary

---

## `app/api/eval.py`

**Role:** Public evaluation endpoint
**Responsibilities:**

* takes dataset + run config
* triggers `services/eval_ragas.py`
* returns evaluation report

---

## `app/core/config.py`

**Role:** All settings in one place
**Responsibilities:**

* reads `.env` / environment variables
* defines:

  * Qdrant URL + collection
  * embedding provider/model
  * LLM provider/model
  * chunk size/overlap
  * top_k defaults
  * eval toggles

---

## `app/core/logging.py`

**Role:** Logging standardization
**Responsibilities:**

* sets log format (json/pretty)
* sets levels
* configures uvicorn + app logger consistency
* optionally adds request-id or correlation-id formatting

---

## `app/services/embeddings.py`

**Role:** Embedding client wrapper
**Responsibilities:**

* “single function” like `embed_texts(texts)` / `embed_query(q)`
* supports whatever backend you use:

  * OpenAI embeddings
  * HF Inference endpoints
  * local embeddings (Ollama/Instructor/etc.)
* ensures consistent output shape + retries

---

## `app/services/llm.py`

**Role:** LLM client wrapper
**Responsibilities:**

* `generate(prompt)` / `chat(messages)`
* supports:

  * OpenAI / HF endpoints / local
* handles:

  * timeouts, retries
  * temperature, max_tokens
  * system prompts

---

## `app/services/qdrant_store.py`

**Role:** Vector DB access layer
**Responsibilities:**

* create/get collection
* upsert vectors + payload metadata
* search vectors (top_k + filters)
* optionally hybrid search / scoring normalization

---

## `app/services/ingestion.py`

**Role:** Ingestion orchestrator
**Responsibilities:**

* load documents (file/pdf/web)
* clean & chunk
* embed chunks
* upsert to Qdrant
* returns ingestion stats

*(This file is usually where chunking strategy lives or calls a chunking util.)*

---

## `app/services/rag_chain.py`

**Role:** The RAG pipeline brain
**Responsibilities:**

* `answer(question)`:

  1. embed query
  2. retrieve top chunks
  3. construct prompt with citations
  4. call LLM
  5. return answer + sources
* may include:

  * reranking step
  * context trimming
  * prompt templates
  * guardrails (“if no relevant context, say I don’t know”)

---

## `app/services/eval_ragas.py`

**Role:** Evaluation engine (RAGAS)
**Responsibilities:**

* loads eval dataset (golden set)
* runs:

  * your pipeline to produce answers + contexts
  * ragas metrics computation
* outputs:

  * global scores
  * per-sample breakdown
  * optional failure buckets (hallucination / low recall / etc.)

---


* a **Mermaid flow diagram** (request paths + dependencies)
* a **README.md “how to run”** section (commands + env vars)
* recommended endpoints + response contracts (JSON schemas)

Just say “make me the README + mermaid diagram”.
