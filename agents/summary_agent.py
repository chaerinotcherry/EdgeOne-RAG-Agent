from langchain_openai import ChatOpenAI
from ingest import fetch_logs
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini")

def summary_agent(days_back: int = 0) -> str:
    df = fetch_logs(days_back=days_back)

    if df.empty:
        return "No logs found."

    stats = df.describe(include="all").to_string()
    sample = df.head(20).to_string()

    response = llm.invoke(f"""
You are a CDN log analyst. Summarize the following EdgeOne CDN logs in a clear, concise report.
Include: total traffic, error rates, any anomalies or patterns you notice.

Stats:
{stats}

Sample logs:
{sample}
""")
    return response.content