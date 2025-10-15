import boto3
import json
from typing import Any


class DynamoAccessor:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(table_name)

    def fetch_docs(self) -> list[str]:
        """Scannt die Tabelle und erzeugt lesbare Textdarstellungen."""
        print(f"📦 Lese Items aus DynamoDB ({self.table_name}) ...", flush=True)
        items, last_key = [], None

        while True:
            if last_key:
                resp = self.table.scan(ExclusiveStartKey=last_key)
            else:
                resp = self.table.scan()
            items.extend(resp.get("Items", []))
            last_key = resp.get("LastEvaluatedKey")
            if not last_key:
                break

        print(f"✅ {len(items)} Items geladen.", flush=True)

        docs = []
        for it in items:
            t = it.get("type", "unknown")
            if t == "cost":
                txt = f"{it.get('date','')} - {it.get('service','')} in {it.get('region','')} cost {it.get('cost','')} USD"
            elif t == "log":
                txt = f"[{it.get('timestamp','')}] {it.get('source','')}: {it.get('message','')}"
            elif t == "event":
                txt = f"[{it.get('timestamp','')}] {it.get('service','')} - {it.get('detail','')}"
            else:
                txt = json.dumps(it, ensure_ascii=False)
            docs.append(txt)
        return docs