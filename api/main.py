
from fastapi import FastAPI, Form
from api.model_runner import run_model
from prometheus_client import Counter, generate_latest

app = FastAPI(title="AskMyDocs v2")
REQUEST_COUNTER = Counter("askmydocs_requests_total", "Total /ask requests")

@app.post("/ask")
async def ask(query: str = Form(...)):
    REQUEST_COUNTER.inc()
    answer = run_model(query)
    return {"answer": answer}

@app.get("/metrics")
async def metrics():
    return generate_latest()
