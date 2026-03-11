from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from agents.doc_agent import doc_agent
from agents.query_agent import query_agent
from agents.summary_agent import summary_agent
from agents.alert_agent import alert_agent
# from langchain_core.tools import Tool
# from dotenv import load_dotenv
# from agents.doc_agent import doc_agent
# from agents.query_agent import query_agent
# from agents.summary_agent import summary_agent


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def orchestrator(question: str) -> str:
    # 1. Quick Route (Takes < 1 second)
    router_prompt = f"""
    Route the user's request to the correct agent. Reply with ONLY the name.
    - DocAgent: For documentation, how-to, or best practices.
    - QueryAgent: For logs, error counts, or traffic stats.
    - SummaryAgent: For high-level reports.
    - AlertAgent: To send notifications or emails.
    
    Question: {question}
    Agent:"""
    
    target_agent = llm.invoke([HumanMessage(content=router_prompt)]).content.strip()

    # 2. Direct Execution (No planning overhead)
    if "DocAgent" in target_agent:
        return doc_agent(question)
    elif "QueryAgent" in target_agent:
        return query_agent(question)
    elif "SummaryAgent" in target_agent:
        return summary_agent()
    elif "AlertAgent" in target_agent:
        return alert_agent(question)
    else:
        # Fallback to a general doc search
        return doc_agent(question)
    
# from langchain_openai import ChatOpenAI
# from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
# from langchain_core.tools import Tool
# from dotenv import load_dotenv
# from agents.doc_agent import doc_agent
# from agents.query_agent import query_agent
# from agents.summary_agent import summary_agent
# from agents.alert_agent import alert_agent

# load_dotenv()
# llm = ChatOpenAI(model="gpt-4o-mini")

# tools = [
#     Tool(
#         name="DocAgent",
#         func=lambda x: doc_agent(x if isinstance(x, str) else x.get("query", str(x))),
#         description="Search EdgeOne official documentation to answer questions about configuration, troubleshooting, and best practices."
#     ),
#     Tool(
#         name="QueryAgent",
#         func=query_agent,
#         description="Use for specific log questions: error counts, request counts, status codes, DDoS attempts."
#     ),
#     Tool(
#         name="SummaryAgent",
#         func=lambda _: summary_agent(),
#         description="Use to generate a summary report of CDN traffic."
#     ),
#     Tool(
#         name="AlertAgent",
#         func=alert_agent,
#         description="Use to send an email alert when an anomaly or critical issue is detected."
#     ),
# ]

# # Planner + Executor
# planner = load_chat_planner(llm)
# executor = load_agent_executor(llm, tools, verbose=True)
# executor.chain.handle_parsing_errors = True
# agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)

# def orchestrator(question: str) -> str:
#     return agent.invoke({"input": question})["output"]