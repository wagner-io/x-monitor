import json
from datetime import datetime, timezone
from typing import Any


def build_metadata(items: list[dict[str, Any]]) -> tuple[list[str], list[dict[str, Any]]]:
    """Convert monitoring records to searchable text and metadata."""
    docs: list[str] = []
    metadata: list[dict[str, Any]] = []

    for item in items:
        doc_type = item.get("type", "generic")
        if doc_type == "cost":
            text = f"{item.get('date', '')} {item.get('service', '')} {item.get('region', '')}: {item.get('cost', '')} USD"
        elif doc_type == "log":
            text = f"[{item.get('timestamp', '')}] {item.get('source', '')}: {item.get('message', '')}"
        elif doc_type == "event":
            text = f"[{item.get('timestamp', '')}] {item.get('service', '')} {item.get('detail', '')}"
        else:
            text = json.dumps(item, ensure_ascii=False, sort_keys=True)

        metadata.append({
            "id": item.get("id", str(len(metadata) + 1)),
            "type": doc_type,
            "s3_key": item.get("s3_key"),
            "timestamp": item.get("timestamp"),
            "service": item.get("service"),
            "region": item.get("region"),
            "text": text,
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
        docs.append(text)

    return docs, metadata
