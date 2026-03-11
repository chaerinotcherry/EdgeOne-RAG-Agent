from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

def build_vectorstore():
    # 1. 문서 로딩
    loader = TextLoader("data/tencent_docs.txt")
    documents = loader.load()

    # 2. 문서 쪼개기
    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    chunks = splitter.split_documents(documents)

    # 3. 벡터 DB에 저장
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        chunks, embeddings,
        persist_directory="vectorstore/"
    )
    print(f"✅ Vectorstore built! {len(chunks)} chunks saved.")

if __name__ == "__main__":
    build_vectorstore(). ㄹㄹ