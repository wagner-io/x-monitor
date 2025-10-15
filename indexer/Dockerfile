FROM python:3.10-slim

# System-Dependencies für faiss / numpy
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential wget git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python-Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 🔽 Modell beim Build einbetten (kein Runtime-Download)
#  - all-MiniLM-L6-v2 → 384-Dim, klein & robust
RUN python - <<'PY'
from sentence_transformers import SentenceTransformer
SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2").save("/app/model")
print("✅ Modell gespeichert in /app/model")
PY

# App-Code
COPY indexer.py /app/indexer.py

# Default-Umgebungsvariablen (können über ECS überschrieben werden)
ENV MODEL_DIR=/app/model \
    INDEX_S3_BUCKET=x-monitor-indexes \
    INDEX_S3_PREFIX=faiss \
    INDEX_DIM=384 \
    DDB_TABLE=x-monitor-mock-data

# Entrypoint
CMD ["python", "/app/indexer.py"]