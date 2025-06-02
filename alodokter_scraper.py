import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_data():
    url = "https://www.alodokter.com/fraktur"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    category = "Patah Tulang"
    date_scraped = datetime.now().strftime("%Y-%m-%d")

    # Gunakan selector yang benar-benar muncul di HTML
    paragraphs = soup.select("article p")

    data = []
    for p in paragraphs:
        text = p.get_text(strip=True)
        if len(text) > 50:
            data.append({
                "sumber": "Alodokter",
                "paragraf": text,
                "tanggal": date_scraped,
                "kategori": category
            })
        if len(data) >= 30:
            break

    print(f"[Alodokter] Total data: {len(data)}")
    return data
