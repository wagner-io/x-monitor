# metadata_builder.py
import json
from datetime import datetime, timezone
from typing import List, Dict, Tuple


class MetadataBuilder:

    def build_metadata(items: List[dict]) -> Tuple[List[str], List[dict]]:
        """Erzeugt Texte und zugehörige Metadaten für jedes DynamoDB-Item."""

        docs = []
        metadata = []

        for item in items:
            doc_type = item.get("type", "generic")

        # Text erzeugen
        if doc_type == "cost":
            text = f"{item.get('date','')} {item.get('service','')} {item.get('region','')}: {item.get('cost','')} USD"
        elif doc_type == "log":
            text = f"[{item.get('timestamp','')}] {item.get('source','')}: {item.get('message','')}"
        elif doc_type == "event":
            text = f"[{item.get('timestamp','')}] {item.get('service','')} {item.get('detail','')}"
        else:
            text = json.dumps(item, ensure_ascii=False)

        # Metadaten definieren
        meta = {
            "id": item.get("id", str(len(metadata) + 1)),
            "type": doc_type,
            "s3_key": item.get("s3_key", None),
            "timestamp": item.get("timestamp", None),
            "service": item.get("service", None),
            "region": item.get("region", None),
            "text": text,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        docs.append(text)
        metadata.append(meta)

        return docs, metadata
