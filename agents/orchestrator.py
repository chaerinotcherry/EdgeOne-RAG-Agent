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
    router_prompt = f"""
    You are an AI Agent that helps the user with questions related to Tencent Cloud's CDN product--EdgeOne.
    Route the user's request to the correct agent. Reply with ONLY the name.

    - DocAgent: Questions about EdgeOne FEATURES, CAPABILITIES, HOW-TO, configuration, or best practices. 
    Examples: "What log services does EdgeOne provide?", "How do I set up DDoS protection?", "What features does EdgeOne have?"
    
    - QueryAgent: Questions that require analyzing ACTUAL REAL-TIME DATA from the user's application.
    Examples: "How many 5xx errors today?", "What is my current traffic volume?", "Show me today's request count."
    
    - SummaryAgent: High-level summary reports of actual traffic data.

    - AlertAgent: Send notifications or emails about detected issues.

    Key distinction: If the question is about what EdgeOne CAN DO → DocAgent. If it's about what IS HAPPENING in the user's data → QueryAgent.

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