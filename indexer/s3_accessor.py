import boto3

class S3Accessor:
    """Zugriff auf S3-Dateien (Lesen von Rohdaten)."""

    def __init__(self, bucket: str):
        self.bucket = bucket
        self.s3 = boto3.client("s3")

    def list_objects(self, prefix: str = "") -> list[str]:
        """Liste aller Objekt-Keys im angegebenen Prefix."""
        resp = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
        return [obj["Key"] for obj in resp.get("Contents", [])]

    def get_object_text(self, key: str) -> str:
        """Liest den Textinhalt eines Objekts."""
        obj = self.s3.get_object(Bucket=self.bucket, Key=key)
        return obj["Body"].read().decode("utf-8")