import pandas as pd
from ingest import fetch_logs

def query_agent(question: str, days_back: int = 0) -> str:
    df = fetch_logs(days_back=days_back)

    if df.empty:
        return "No logs found for the specified period."

    # 기본 통계
    total = len(df)
    status_counts = df["status"].value_counts().to_dict() if "status" in df.columns else {}
    error_4xx = sum(v for k, v in status_counts.items() if str(k).startswith("4"))
    error_5xx = sum(v for k, v in status_counts.items() if str(k).startswith("5"))

    summary = f"""
Total requests: {total}
4xx errors: {error_4xx}
5xx errors: {error_5xx}
Status breakdown: {status_counts}
"""
    return summary