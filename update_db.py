import firebase_admin
import json
import os
import requests
import sys
from firebase_admin import credentials, db

# Memastikan environment variable tersedia
service_account_json = os.getenv('FIREBASE_SERVICE_ACCOUNT')
if not service_account_json:
    print("Error: Variabel FIREBASE_SERVICE_ACCOUNT tidak ditemukan di GitHub Secrets!")
    sys.exit(1)

try:
    service_account_info = json.loads(service_account_json)
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://lagu-rohani-b507a-default-rtdb.asia-southeast1.firebasedatabase.app'
    })
except Exception as e:
    print(f"Error saat inisialisasi Firebase: {e}")
    sys.exit(1)

def update_songs_to_firebase(new_songs):
    try:
        ref = db.reference('songs')
        # Mengambil data lama terlebih dahulu agar tidak terhapus
        existing_songs = ref.get() or []
        
        # Membuat set URL untuk menghindari duplikasi lagu
        existing_urls = {song.get('url') for song in existing_songs if isinstance(song, dict)}
        
        updated_list = list(existing_songs)
        added_count = 0
        
        for song in new_songs:
            if song.get('url') not in existing_urls:
                # Memberikan ID baru berdasarkan panjang list
                song["id"] = len(updated_list) + 1
                updated_list.append(song)
                existing_urls.add(song.get('url'))
                added_count += 1
        
        ref.set(updated_list)
        print(f"Selesai! Menambahkan {added_count} lagu baru. Total lagu saat ini: {len(updated_list)}")
    except Exception as e:
        print(f"Gagal mengunggah ke Firebase: {e}")
        sys.exit(1)

def get_identifiers_from_search(query, max_items=20):
    url = "https://archive.org/advancedsearch.php"
    params = {
        "q": query,
        "fl[]": "identifier",
        "rows": max_items,
        "page": 1,
        "output": "json"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            docs = response.json().get("response", {}).get("docs", [])
            return [doc["identifier"] for doc in docs]
    except Exception as e:
        print(f"Gagal mengambil data dari Archive.org: {e}")
    return []

def fetch_files_from_identifier(identifier):
    url = f"https://archive.org/metadata/{identifier}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200: return []
        
        data = response.json()
        files = data.get("files", [])
        songs = []
        
        for file in files:
            # Memastikan file adalah mp3
            if file.get("name", "").lower().endswith(".mp3"):
                duration = float(file.get("length", 0))
                
                # Aturan: Ambil lagu dengan durasi maksimal 300 detik (5 menit)
                # Durasi 0 dianggap tidak valid atau data durasi tidak terbaca
                if 0 < duration <= 300:
                    title = file.get("title", file.get("name").replace(".mp3", "").replace("_", " "))
                    songs.append({
                        "title": title,
                        "url": f"https://archive.org/download/{identifier}/{file.get('name')}",
                        "size": file.get("size", "0"),
                        "duration": duration,
                        "category": "Worship"
                    })
        return songs
    except Exception as e:
        print(f"Gagal mengambil file dari {identifier}: {e}")
        return []

if __name__ == "__main__":
    print("Memulai proses pencarian...")
    # Menggunakan query yang luas
    search_query = 'title:"lagu rohani" OR subject:"lagu rohani"'
    # max_items tetap 20 untuk membatasi jumlah album yang dibuka agar tidak timeout
    album_ids = get_identifiers_from_search(search_query, max_items=20)
    
    if not album_ids:
        print("Tidak ada album ditemukan.")
        sys.exit(0)
    
    all_new_songs = []
    for album_id in album_ids:
        print(f"Memproses album: {album_id}")
        songs = fetch_files_from_identifier(album_id)
        all_new_songs.extend(songs)
        
    if all_new_songs:
        update_songs_to_firebase(all_new_songs)
    else:
        print("Tidak ada lagu baru yang memenuhi kriteria ditemukan.")
