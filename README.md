# X-Monitor

Semantische Suche für Monitoring-Daten mit Python, Sentence Transformers und FAISS.

## Funktionsweise

```text
S3 (Logs/Events/Kosten) -> Indexer -> Embeddings -> FAISS -> FastAPI-Suche
                                      \-> Metadaten
```

Der Indexer liest Textdateien aus S3, erzeugt 384-dimensionale Embeddings mit
`all-MiniLM-L6-v2` und speichert einen normalisierten FAISS-Index inklusive
Metadaten. Die API lädt diesen Index und liefert die ähnlichsten Dokumente.

## Lokale Demo

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/create_demo_index.py
uvicorn api.app:app --reload
curl 'http://localhost:8000/health'
curl 'http://localhost:8000/search?q=database%20timeout&top_k=3'
```

Zum lokalen Testen wird standardmäßig ein kleines Hash-Embedding verwendet;
dadurch funktioniert die Demo ohne Modelldownload. Für echte Daten:

```bash
EMBEDDING_BACKEND=sentence-transformers MODEL_DIR=/path/to/model \
  uvicorn api.app:app --reload
```

## Tests und Qualität

```bash
pip install -r requirements-dev.txt
pytest -q
python -m compileall indexer api scripts
```

## Konfiguration

| Variable | Default | Zweck |
|---|---|---|
| `INDEX_DIR` | `./data/index` | FAISS-Index und Metadaten |
| `EMBEDDING_BACKEND` | `hash` | `hash` für Demo, `sentence-transformers` für Produktion |
| `MODEL_DIR` | `./data/model` | lokales Sentence-Transformer-Modell |
| `TOP_K_MAX` | `20` | maximale Trefferzahl |
| `DATA_BUCKET` | `x-monitor-data` | S3-Quelle des Indexers |
| `S3_PREFIX` | `logs/` | S3-Prefix |
| `OUTPUT_DIR` | `./data/index` | Ausgabe des Indexers |

## AWS-Betrieb

Terraform liegt unter `infra/`. Die ECS/Fargate-Task wird per EventBridge
alle 15 Minuten gestartet. Vor `terraform apply` Bucket-Namen, Region und
IAM-Berechtigungen prüfen. Keine echten Zugangsdaten ins Repository committen.

## Architekturentscheidungen

- FAISS `IndexFlatIP` plus L2-Normalisierung: schneller, deterministischer
  Baseline-Vektorindex und Cosine-Ähnlichkeit.
- Adapter für Embeddings: lokale Demo bleibt reproduzierbar und testbar.
- JSON-Metadaten neben dem Index: einfache Portabilität und Inspektion.
- FastAPI: typisierte, automatisch dokumentierte Suchschnittstelle.

## Portfolio-Fokus

Das Projekt zeigt Python-Backend-Entwicklung, REST-API-Design, AWS/S3,
Containerisierung, Embeddings, Vektorsuche, Tests, Konfiguration und IaC.

## Lizenz

Für Bewerbungszwecke. Lizenz bei Veröffentlichung ergänzen.
