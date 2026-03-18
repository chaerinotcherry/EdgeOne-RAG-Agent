import requests
from bs4 import BeautifulSoup
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

BASE_TENCENT = "https://www.tencentcloud.com"
BASE_EDGEONE = "https://edgeone.ai"

ROOT_URLS = [
    f"{BASE_TENCENT}/document/product/1145",
    f"{BASE_EDGEONE}/document",
]

def get_all_links_recursive(root_url, max_depth=2):
    visited = set()
    pending = set()
    to_visit = [(root_url, 0)]
    pending.add(root_url)
    all_links = set()
    
    root_domain = urlparse(root_url).netloc
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
                
                if href.startswith("http"):
                    full_url = href
                elif href.startswith("/"):
                    full_url = f"https://{root_domain}{href}"
                else:
                    continue
                
                if urlparse(full_url).netloc != root_domain:
                    continue
                
                full_url = full_url.split("?")[0].split("#")[0]
                
                if full_url not in visited and full_url not in pending:
                    all_links.add(full_url)
                    to_visit.append((full_url, depth + 1))
                    pending.add(full_url)
                    
        except Exception as e:
            print(f"❌ {url} — {e}")
    
    print(f"✅ Found {len(all_links)} pages from {root_url}")
    return all_links

def scrape_page(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        res = requests.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(res.text, "html.parser")
        
        if "tencentcloud.com" in url:
            content = soup.find("div", class_="catalogue-detail-innerHtml")
        elif "edgeone.ai" in url:
            for tag in soup.find_all(["header", "footer", "nav"]):
                tag.decompose()
            content = soup.find("main") or soup.find("body")
        else:
            content = soup.find("main") or soup.find("body")
            
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
    all_links = set()
    for root_url in ROOT_URLS:
        links = get_all_links_recursive(root_url, max_depth=2)
        all_links.update(links)
    
    print(f"\n🔗 Total unique pages: {len(all_links)}")
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = []
    failed = []
    
    for i, url in enumerate(all_links):
        print(f"[{i+1}/{len(all_links)}] Scraping: {url}")
        text = scrape_page(url)
        if text:
            chunks = splitter.create_documents([text], metadatas=[{"source": url}])
            docs.extend(chunks)
        else:
            failed.append(url)
    
    print(f"\n📦 Total chunks: {len(docs)}")
    print(f"❌ Failed: {len(failed)} pages")
    if failed:
        print("\n실패한 URL들:")
        for url in failed:
            print(f"  - {url}")
    
    if not docs:
        print("❌ No docs found! 크롤링 실패")
        return
        
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        docs, embeddings,
        persist_directory="vectorstore/"
    )
    print(f"✅ {len(docs)} chunks saved to vectorstore!")

if __name__ == "__main__":
    build_doc_vectorstore()