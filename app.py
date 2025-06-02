import streamlit as st
from pymongo import MongoClient
from collections import Counter, defaultdict
import datetime
import matplotlib.pyplot as plt

# Koneksi MongoDB
client = MongoClient(st.secrets["mongo_uri"])
db = client.scrapping
data = db.artikel_patah_tulang.find()

def extract_frequent_words(data):
    all_text = ' '.join([item.get('paragraf', '') for item in data])
    words = all_text.lower().split()
    stopwords = set(["dan", "yang", "untuk", "dengan", "dari", "pada", "ini", "atau", "oleh", "karena", "jika", "akan", "adalah", "dapat", "saat", "juga", "lebih", "tidak", "dalam"])
    filtered = [w.strip(".,!?") for w in words if w not in stopwords and len(w) > 2]
    return Counter(filtered).most_common(10)

def plot_bar_chart(labels, values, title, color):
    fig, ax = plt.subplots()
    ax.bar(labels, values, color=color, alpha=0.7)
    ax.set_title(title)
    ax.set_ylabel('Jumlah')
    ax.set_xticklabels(labels, rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

def main():
    st.title("Visualisasi Artikel Patah Tulang")

    try:
        # Data artikel per sumber
        pipeline = [
            {"$group": {"_id": "$sumber", "jumlah": {"$sum": 1}}}
        ]
        artikel_per_sumber = list(db.artikel_patah_tulang.aggregate(pipeline))

        st.header("Diagram Jumlah Artikel per Sumber")
        labels = [doc['_id'] for doc in artikel_per_sumber]
        values = [doc['jumlah'] for doc in artikel_per_sumber]
        plot_bar_chart(labels, values, "Jumlah Artikel per Sumber", color='orange')

        # Data kata paling sering
        wiki_data = list(db.artikel_patah_tulang.find({"sumber": "Wikipedia"}))
        hello_data = list(db.artikel_patah_tulang.find({"sumber": "HelloSehat"}))
        alodokter_data = list(db.artikel_patah_tulang.find({"sumber": "Alodokter"}))

        st.header("Diagram Kata Paling Sering Muncul")

        st.subheader("Wikipedia")
        wiki_word_freq = extract_frequent_words(wiki_data)
        if wiki_word_freq:
            labels, values = zip(*wiki_word_freq)
            plot_bar_chart(labels, values, "Kata Paling Sering - Wikipedia", color='blue')
        else:
            st.write("Tidak ada data kata.")

        st.subheader("HelloSehat")
        hello_word_freq = extract_frequent_words(hello_data)
        if hello_word_freq:
            labels, values = zip(*hello_word_freq)
            plot_bar_chart(labels, values, "Kata Paling Sering - HelloSehat", color='green')
        else:
            st.write("Tidak ada data kata.")

        st.subheader("Alodokter")
        alodokter_word_freq = extract_frequent_words(alodokter_data)
        if alodokter_word_freq:
            labels, values = zip(*alodokter_word_freq)
            plot_bar_chart(labels, values, "Kata Paling Sering - Alodokter", color='red')
        else:
            st.write("Tidak ada data kata.")

        # Jadwal artikel per bulan
        semua_artikel = list(db.artikel_patah_tulang.find({}))
        bulan_sumber = defaultdict(lambda: defaultdict(int))
        for art in semua_artikel:
            try:
                bulan = datetime.datetime.strptime(art['tanggal'], "%Y-%m-%d").strftime("%B %Y")
                bulan_sumber[bulan][art['sumber']] += 1
            except:
                continue

        st.header("Jadwal Artikel per Bulan")
        if bulan_sumber:
            for bulan, sumber_info in sorted(bulan_sumber.items()):
                st.markdown(f"### Artikel Bulan {bulan}")
                for sumber, jumlah in sumber_info.items():
                    st.write(f"- **{sumber}**: {jumlah} artikel")
        else:
            st.write("Belum ada data jadwal artikel.")

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    main()
