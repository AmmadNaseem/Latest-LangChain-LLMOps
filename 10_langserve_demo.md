# Groq translation API: concepts and usage

A **REST API** lets another application call your code over HTTP. **FastAPI** validates requests and documents endpoints. **Uvicorn** is the server process. **LangServe** exposes LangChain Runnables as HTTP endpoints. It is an archived project; this lesson preserves the requested integration, while new deployments should assess maintenance needs before adopting it.

The LCEL pipeline is `ChatPromptTemplate | ChatGroq | StrOutputParser`: format instructions, call Groq, then extract a string. Use this predictable chain for translation. An agent with tools is useful when execution must depend on model decisions.

## Setup (PowerShell)

Run from the project root:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe 10_langserve_demo.py
```

Copy settings from `groq_demos.env.example` into your existing `.env`; preserve other settings and replace the key placeholder. Notebook 11 also needs Tavily for search. Choose the project virtual environment as the notebook kernel and run cells in order.

Open http://127.0.0.1:8000/docs to inspect the API. In another terminal:

```powershell
$payload = @{input = @{language = "Urdu"; text = "I am learning LangChain."}} | ConvertTo-Json -Depth 3
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/chain/invoke" -ContentType "application/json" -Body $payload
```

LangServe wraps your validated input inside `input`; its response contains `output`. The Pydantic schema rejects empty or oversized fields. **Timeouts** bound provider waiting; **retries** recover from transient failures. Neither fixes invalid credentials or exhausted quota. The application factory separates construction from server startup and allows offline tests to inject a fake model.

## Deployment considerations

This is a learning API with production-oriented boundaries, not a fully deployed enterprise service. Before public exposure, add authentication, per-client rate limits, TLS at a reverse proxy, request-size limits, sanitized error handling, and monitoring. Keep keys in a secret manager and avoid logging request content. The default localhost binding serves only this computer. `/chain/stream` supports streamed output; streaming improves perceived latency but does not guarantee a faster model.

Sources: [LangServe repository and maintenance status](https://github.com/langchain-ai/langserve), [ChatGroq integration](https://docs.langchain.com/oss/python/integrations/chat/groq).
