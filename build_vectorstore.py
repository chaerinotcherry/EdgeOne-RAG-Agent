import requests
from bs4 import BeautifulSoup
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://www.tencentcloud.com"
ROOT_URL = f"{BASE_URL}/document/product/1145"

def get_all_links_recursive(root_url, max_depth=2):
    visited = set()
    to_visit = [(root_url, 0)]
    all_links = set()
    
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    
    while to_visit:
        url, depth = to_visit.pop(0)
        if url in visited or depth > max_depth:
            continue
        visited.add(url)
        
        try:
            res = requests.get(url, headers=headers, timeout=30)
            soup = BeautifulSoup(res.text, "html.parser")
            
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "/document/product/1145/" in href:
                    full_url = BASE_URL + href if href.startswith("/") else href
                    # 쿼리스트링 제거
                    full_url = full_url.split("?")[0]
                    if full_url not in visited:
                        all_links.add(full_url)
                        to_visit.append((full_url, depth + 1))
        except Exception as e:
            print(f"❌ {url} — {e}")
    
    print(f"✅ Found {len(all_links)} pages")
    return all_links

def scrape_page(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        res = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(res.text, "html.parser")
        
        content = soup.find("div", class_="catalogue-detail-innerHtml")
        if not content:
            return None
            
        text = content.get_text(separator="\n", strip=True)
        if len(text) < 100:
            return None
            
        return text
    except Exception as e:
        print(f"❌ Failed: {url} — {e}")
        return None

def build_doc_vectorstore():
    links = get_all_links_recursive(ROOT_URL, max_depth=2)
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = []
    
    for i, url in enumerate(links):
        print(f"[{i+1}/{len(links)}] Scraping: {url}")
        text = scrape_page(url)
        if text:
            chunks = splitter.create_documents([text], metadatas=[{"source": url}])
            docs.extend(chunks)
    
    print(f"\n📦 Total chunks: {len(docs)}")
    
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        docs, embeddings,
        persist_directory="vectorstore/"
    )
    print(f"✅ {len(docs)} chunks saved to vectorstore!")

if __name__ == "__main__":
    build_doc_vectorstore()