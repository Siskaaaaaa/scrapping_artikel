import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_data():
    url = "https://id.wikipedia.org/wiki/Patah_tulang"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    category = "Patah Tulang"
    date_scraped = datetime.now().strftime("%Y-%m-%d")
    elements = soup.select("p, li, h2, h3")

    data = []
    for el in elements:
        text = el.get_text(strip=True)
        if len(text) > 50:
            data.append({
                "sumber": "Wikipedia", 
                "paragraf": text, 
                "tanggal": date_scraped,
                "kategori": category
            })
    return data
