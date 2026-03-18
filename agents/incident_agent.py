from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings()
vectorstore = Chroma(
    persist_directory="vectorstore/",
    embedding_function=embeddings
)
llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_messages([
    ("system", "Use the given context to answer the question about past incidents. Context: {context}"),
    ("human", "{input}"),
])

def incident_agent(question: str) -> str:
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(
        vectorstore.as_retriever(search_kwargs={"k": 3}),
        combine_docs_chain
    )
    return retrieval_chain.invoke({"input": question})["answer"]