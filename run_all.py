import pymongo
import streamlit as st
from pymongo import MongoClient
import certifi  # ✅ untuk SSL certificate

from wikipedia_scraper import get_data as get_wiki
from hellosehat_scraper import get_data as get_hello
from alodokter_scraper import get_data as get_alodokter
import re
from collections import Counter


def save_to_mongo(data):
    # ✅ Gunakan certifi untuk koneksi SSL aman
    client = MongoClient(st.secrets["mongo_uri"], tlsCAFile=certifi.where())
    db = client["scrapping"]  # nama database
    collection = db["artikel_patah_tulang"]  # nama collection
    collection.delete_many({})  # kosongkan dulu jika perlu
    collection.insert_many(data)


def extract_frequent_words(data, sumber):
    print(f"Inspecting {sumber} data: {data[0]}")

    try:
        filtered = [item['konten'] for item in data if item.get('sumber') == sumber]
    except KeyError:
        filtered = [item.get('text', '') for item in data if item.get('sumber') == sumber]

    text = ' '.join(filtered).lower()
    words = re.findall(r'\b\w{4,}\b', text)
    common = Counter(words).most_common(10)
    return [{"kata": k, "jumlah": v} for k, v in common]


if __name__ == "__main__":
    data = []

    try:
        wiki_data = get_wiki()
        print(f"[Wikipedia] {len(wiki_data)} data")
        data += wiki_data
    except Exception as e:
        print(f"Error Wikipedia: {e}")

    try:
        hello_data = get_hello()
        print(f"[HelloSehat] {len(hello_data)} data")
        data += hello_data
    except Exception as e:
        print(f"Error HelloSehat: {e}")

    try:
        alodokter_data = get_alodokter()
        print(f"[Alodokter] {len(alodokter_data)} data")
        data += alodokter_data
    except Exception as e:
        print(f"Error Alodokter: {e}")

    print(f"[TOTAL] Menyimpan {len(data)} data ke MongoDB Atlas")
    save_to_mongo(data)
    print("✅ Data berhasil disimpan ke MongoDB Atlas.")

    try:
        wiki_word_freq = extract_frequent_words(data, "Wikipedia")
        print(f"[Wikipedia] Kata terpopuler: {wiki_word_freq}")
    except Exception as e:
        print(f"Error extracting Wikipedia words: {e}")

    try:
        hello_word_freq = extract_frequent_words(data, "HelloSehat")
        print(f"[HelloSehat] Kata terpopuler: {hello_word_freq}")
    except Exception as e:
        print(f"Error extracting HelloSehat words: {e}")

    try:
        alodokter_word_freq = extract_frequent_words(data, "Alodokter")
        print(f"[Alodokter] Kata terpopuler: {alodokter_word_freq}")
    except Exception as e:
        print(f"Error extracting Alodokter words: {e}")
