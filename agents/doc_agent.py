from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_cohere import CohereRerank
from langchain.retrievers import ContextualCompressionRetriever, EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings()
vectorstore = Chroma(
    persist_directory="vectorstore/",
    embedding_function=embeddings
)
llm = ChatOpenAI(model="gpt-4o-mini")

def get_all_docs_batched(vectorstore, batch_size=5000):
    all_documents = []
    offset = 0
    while True:
        batch = vectorstore.get(limit=batch_size, offset=offset, include=["documents", "metadatas"])
        if not batch["documents"]:
            break
        for text, meta in zip(batch["documents"], batch["metadatas"]):
            all_documents.append(Document(page_content=text, metadata=meta))
        offset += batch_size
        print(f"📥 Loaded {len(all_documents)} docs...")
        if len(batch["documents"]) < batch_size:
            break
    return all_documents

print("📥 Loading docs for BM25...")
docs_for_bm25 = get_all_docs_batched(vectorstore)
print(f"✅ Loaded {len(docs_for_bm25)} docs for BM25")

# BM25 (키워드 검색)
bm25_retriever = BM25Retriever.from_documents(docs_for_bm25)
bm25_retriever.k = 10

# ChromaDB (시맨틱 검색)
semantic_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

# Hybrid = BM25 + Semantic (가중치 50:50)
hybrid_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, semantic_retriever],
    weights=[0.5, 0.5]
)

# Reranker
reranker = CohereRerank(model="rerank-v3.5", top_n=5)
retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=hybrid_retriever
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
Answer questions based on the provided documentation context.
If the context contains relevant information, use it to answer even if it doesn't directly address the question format (e.g. comparisons, summaries).
Only say "I could not find this in the EdgeOne documentation" if the context has absolutely no relevant information.
For general greetings or small talk, respond naturally.
Keep answers specific and actionable.
Context: {context}"""),
    ("human", "{input}"),
])

def doc_agent(question: str) -> str:
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
    result = retrieval_chain.invoke({"input": question})
    return result["answer"]