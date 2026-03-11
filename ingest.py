import gzip
import json
import io
import pandas as pd
from datetime import datetime, timedelta
from qcloud_cos import CosConfig, CosS3Client
from dotenv import load_dotenv
import os

load_dotenv()

config = CosConfig(
    Region=os.getenv("COS_REGION"),
    SecretId=os.getenv("TENCENT_SECRET_ID"),
    SecretKey=os.getenv("TENCENT_SECRET_KEY")
)
client = CosS3Client(config)

def fetch_logs(days_back=0):
    date = datetime.now() - timedelta(days=days_back)
    prefix = f"{os.getenv('COS_LOG_PREFIX')}/{date.strftime('%Y%m%d')}/"

    response = client.list_objects(
        Bucket=os.getenv("COS_BUCKET"),
        Prefix=prefix
    )

    logs = []
    for obj in response.get("Contents", []):
        key = obj["Key"]
        if not key.endswith(".gz"):
            continue

        res = client.get_object(Bucket=os.getenv("COS_BUCKET"), Key=key)
        compressed = res["Body"].get_raw_stream().read()

        with gzip.open(io.BytesIO(compressed)) as f:
            for line in f:
                try:
                    logs.append(json.loads(line))
                except:
                    pass

    return pd.DataFrame(logs)

if __name__ == "__main__":
    df = fetch_logs()
    print(df.head())
    print(f"\n총 {len(df)} 개 로그 로드됨")