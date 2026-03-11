# 추가 테스트
import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

url = "https://www.tencentcloud.com/document/product/1145/46348"
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

# div 클래스 목록 확인
divs = soup.find_all("div", class_=True)
classes = set()
for d in divs:
    for c in d.get("class", []):
        classes.add(c)

print("div 클래스들:")
for c in sorted(classes):
    print(c)