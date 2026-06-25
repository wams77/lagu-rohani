import firebase_admin
import json
import os
import requests
from firebase_admin import credentials, db

# Membaca config dari GitHub Secrets
service_account_info = json.loads(os.getenv('FIREBASE_SERVICE_ACCOUNT'))

cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://lagu-rohani-b507a-default-rtdb.asia-southeast1.firebasedatabase.app'
})

def update_songs_to_firebase(list_lagu):
    ref = db.reference('songs')
    ref.set(list_lagu)
    print(f"Berhasil memperbarui {len(list_lagu)} lagu ke Firebase!")

def search_archive_for_identifiers(query, max_results=3):
    print(f"Mencari koleksi baru di Archive.org dengan kata kunci: '{query}'...")
    search_url = "https://archive.org/advancedsearch.php"
    params = {
        "q": f"({query}) AND mediatype:audio",
        "fl[]": "identifier",
        "sort[]": "-addeddate", # Sortir berdasarkan yang paling baru diupload
        "output": "json",
        "rows": max_results # Batasi jumlah pencarian agar tidak membebani memori
    }
    
    try:
        response = requests.get(search_url, params=params)
        if response.status_code == 200:
            data = response.json()
            docs = data.get("response", {}).get("docs", [])
            identifiers = [doc["identifier"] for doc in docs]
            print(f"Ditemukan {len(identifiers)} koleksi baru: {identifiers}")
            return identifiers
        else:
            print("Gagal terhubung ke pencarian Archive.org.")
            return []
    except Exception as e:
        print(f"Error saat mencari: {e}")
        return []

def fetch_songs_from_archive(identifier):
    print(f"Mencari lagu dari sumber Archive.org: {identifier}...")
    url = f"https://archive.org/metadata/{identifier}"
    
    # Mengambil data mentah (JSON) dari Archive.org
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Gagal mengambil data dari {identifier}")
        return []

    data = response.json()
    files = data.get("files", [])
    
    colors = ["1e40af", "9d174d", "065f46", "b45309", "3f3f46", "4c1d95", "b91c1c", "0f766e"]
    categories = ["Worship", "Penyembahan", "Saat Teduh", "Praise"]
    
    formatted_songs = []
    song_id = 1

    for file in files:
        # Kita hanya mengambil file audio berekstensi .mp3
        if file.get("name", "").endswith(".mp3"):
            
            # Ambil judul asli dari metadata, jika kosong gunakan nama file
            raw_title = file.get("title", file.get("name").replace(".mp3", ""))

            # Pisahkan artis jika ada tanda strip (-)
            artist = "Worship Leader"
            title = raw_title
            if " - " in raw_title:
                parts = raw_title.split(" - ", 1)
                title = parts[0].strip()
                artist = parts[1].strip()

            # Hitung otomatis ukuran file ke format MB
            size_bytes = int(file.get("size", 0))
            size_mb = f"{round(size_bytes / (1024 * 1024), 1)} MB"

            # Ambil 2 huruf awal untuk cover gambar
            cover_text = title[:2].upper() if len(title) >= 2 else "SG"

            # Distribusikan kategori secara merata
            category = categories[song_id % len(categories)]

            formatted_songs.append({
                "id": song_id,
                "title": title,
                "artist": artist,
                "duration": "04:30", # Archive.org tidak selalu memberikan durasi, ini nilai default
                "size": size_mb,
                "category": category,
                "coverColor": colors[song_id % len(colors)],
                "coverText": cover_text,
                "url": f"https://archive.org/download/{identifier}/{file.get('name')}"
            })
            song_id += 1

    return formatted_songs

if __name__ == "__main__":
    # 1. Koleksi andalan yang sudah kita tahu bagus
    sumber_archive = ["c-84_20250706"]
    
    # 2. Kata kunci pencarian untuk ditarik otomatis
    query_pencarian = 'title:"lagu rohani" OR title:"praise worship indonesia" OR subject:"lagu rohani kristen"'
    
    # 3. Lakukan pencarian otomatis dan ambil 3 koleksi/album terbaru
    sumber_tambahan = search_archive_for_identifiers(query_pencarian, max_results=3)
    
    # Gabungkan koleksi andalan dengan hasil pencarian baru
    for sumber in sumber_tambahan:
        if sumber not in sumber_archive:
            sumber_archive.append(sumber)

    semua_lagu = []
    # Loop ke semua sumber untuk mengambil file MP3-nya
    for sumber in sumber_archive:
        lagu_dari_sumber = fetch_songs_from_archive(sumber)
        semua_lagu.extend(lagu_dari_sumber)

    # Susun ulang ID agar berurutan untuk UI
    for i, lagu in enumerate(semua_lagu):
        lagu["id"] = i + 1

    # Mengunggah seluruh data yang otomatis terkumpul ke Firebase
    if semua_lagu:
        update_songs_to_firebase(semua_lagu)
    else:
        print("Tidak ada lagu yang ditemukan untuk diperbarui.")
