FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY indexer ./indexer
COPY api ./api
COPY scripts ./scripts
COPY README.md .
RUN python scripts/create_demo_index.py
ENV INDEX_DIR=/app/data/index EMBEDDING_BACKEND=hash
EXPOSE 8000
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
