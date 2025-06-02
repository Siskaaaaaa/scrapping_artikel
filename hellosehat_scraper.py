import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_data():
    url = "https://hellosehat.com/muskuloskeletal/tulang/patah-tulang-fraktur/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    category = "Patah Tulang"
    date_scraped = datetime.now().strftime("%Y-%m-%d")

    # Perhatikan selector ini, tergantung struktur HTML
    paragraphs = soup.select("article p")

    data = []
    for p in paragraphs:
        text = p.get_text(strip=True)
        if len(text) > 50:
            data.append({
                "sumber": "HelloSehat",
                "paragraf": text,
                "tanggal": date_scraped,
                "kategori": category
            })

    print(f"[HelloSehat] Total data: {len(data)}")
    return data
