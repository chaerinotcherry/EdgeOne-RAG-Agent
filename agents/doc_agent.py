from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_cohere import CohereRerank
from langchain.retrievers import ContextualCompressionRetriever
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings()
vectorstore = Chroma(
    persist_directory="vectorstore/",
    embedding_function=embeddings
)
llm = ChatOpenAI(model="gpt-4o-mini")

# Reranker 추가
reranker = CohereRerank(model="rerank-v3.5", top_n=3)
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})  # 많이 뽑고
retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=base_retriever
)  # reranker가 진짜 관련있는 3개 골라냄

prompt = ChatPromptTemplate.from_messages([
    ("system", """
For general greetings or small talk, respond naturally and friendly.
For technical questions, answer questions based on the provided documentation context.
If the answer is not found, say "I could not find this in the EdgeOne documentation".
Keep answers specific and actionable.
Context: {context}"""),
    ("human", "{input}"),
])

def doc_agent(question: str) -> str:
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(
        retriever,
        combine_docs_chain
    )
    result = retrieval_chain.invoke({"input": question})
    print("CONTEXT:", result["context"])
    return result["answer"]