## AskMyDocs v2 — Copilot / AI agent instructions

This file gives concise, repo-specific guidance so an AI coding agent can be productive immediately.

### Big picture (what this repo does)
- FastAPI-based API that exposes a single `/ask` endpoint (`api/main.py`) which delegates to `api/model_runner.py`.
- Streamlit UI (`ui/app.py`) posts questions to the API at `http://localhost:8000/ask`.
- Infrastructure includes Docker + Docker Compose (`infra/Dockerfile`, `infra/docker-compose.yml`) and monitoring via Prometheus/Grafana (`infra/prometheus.yml`).
- Model/training pieces: `trainer/fine_tune.py` is currently a placeholder; model pulling is supported via the `Makefile` target `pull-model` which uses the Hugging Face CLI.

### Key files to inspect / change (quick map)
- `api/main.py` — FastAPI routes: `/ask` (calls `run_model`) and `/metrics` (Prometheus output).
- `api/model_runner.py` — currently loads tokenizer/model inside `run_model()` on every call. Any model-change work should start here.
- `ui/app.py` — Streamlit front-end; posts form data to the API.
- `trainer/fine_tune.py` — training entrypoint (placeholder); `make train` runs this.
- `infra/docker-compose.yml` — orchestrates `api`, `mlflow`, `prometheus`, `grafana`. Note: `build: ..` and `volumes: ../:/app` use the repo root as the Docker context.
- `infra/Dockerfile` — container image; installs from `requirements.txt` (repo currently uses `environment.yml` — see quirks below).
- `Makefile` — canonical convenience targets: `setup`, `pull-model`, `up`, `ui`, `train`, `clean`.

### Developer workflows (concrete commands)
Prefer using the Makefile targets where available. Examples:

To set up the Conda environment (first time):
```
make setup
# then activate
conda activate askmydocs
```

To run the full stack with Docker Compose (builds image from repo root):
```
make up
# or
docker compose -f infra/docker-compose.yml up --build
```

To run the API locally (no container):
```
conda activate askmydocs
uvicorn api.main:app --reload
```

To run the Streamlit UI locally:
```
make ui
# or
streamlit run ui/app.py
```

To pull the LLaMA model via Hugging Face (Makefile helper uses HF CLI):
```
make pull-model
# requires `huggingface-cli login` and sufficient credentials/entitlements
```

### Integration points & external dependencies
- Hugging Face model artifacts (transformers). `model_runner.py` expects `meta-llama/Llama-3.1-8B-Instruct` to be available via HF.
- mlflow is included as a service in `infra/docker-compose.yml` and is referenced via `MLFLOW_TRACKING_URI` in the compose env.
- Prometheus scrapes the API at `/metrics` (see `infra/prometheus.yml`) — the API exposes metrics using `prometheus_client`.

### Project-specific conventions & important quirks (do not change without tests)
- Conda-first: repository includes `environment.yml` and the Makefile `setup` target. Use `environment.yml` for dev environment installs.
- Dockerfile installs from `requirements.txt` but the repo currently does not include `requirements.txt` — be careful when changing Docker-related dependency logic (fast fix: add a small `requirements.txt` or update the Dockerfile to use the conda env or `pip install -r <generated>`).
- `api/model_runner.py` loads model/tokenizer inside `run_model()` on every request. This is discoverable and affects performance and resource usage. Any change to make model loading persistent should:
  - Move tokenizer/model to module-level cached objects.
  - Ensure device_map and dtype choices stay compatible with target runtime.
  - Add a small smoke test that calls `/ask` to validate behavior.
- `trainer/fine_tune.py` is intentionally a placeholder. `make train` invokes it; expect training work to be manual and external until this file is implemented.

### Safe, concrete edits an AI agent can make automatically
- Small improvements to `api/model_runner.py` that cache tokenizer/model at module load (do not change the model architecture). Add a fallback message when the model is unavailable (current code already returns an error string).
- Add a lightweight `requirements.txt` synchronized with `environment.yml` if you need to build the Docker image reliably.
- Add unit/smoke tests that call `api.main` endpoints (FastAPI TestClient) to verify `/ask` and `/metrics` after edits.

### Things to ask the maintainer before larger changes
- Do you want the Dockerfile and CI to rely on `environment.yml` (conda) or `requirements.txt` (pip)? There's currently a mismatch.
- Is the Hugging Face model intended to be pulled during CI/automation or provisioned manually (due to licensing/entitlements)?

If anything is unclear or you want this shortened, expanded, or reorganized (e.g., add quick jump-to diffs for the `model_runner` caching change), tell me which sections to adjust and I will iterate.
