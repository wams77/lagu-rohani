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

def tentukan_kategori(title):
    """Logika sederhana untuk menentukan kategori berdasarkan judul lagu."""
    title_lower = title.lower()
    if any(word in title_lower for word in ['teduh', 'tenang', 'doa', 'renungan', 'instrumen']):
        return "Saat Teduh"
    elif any(word in title_lower for word in ['praise', 'semangat', 'ceria', 'agung', 'sorak']):
        return "Praise"
    elif any(word in title_lower for word in ['worship', 'faith', 'yesus', 'tuhan']):
        return "Worship"
    else:
        return "Penyembahan" # Kategori default

def update_songs_to_firebase(new_songs):
    try:
        ref = db.reference('songs')
        existing_songs = ref.get() or []
        existing_urls = {song.get('url') for song in existing_songs if isinstance(song, dict)}
        
        updated_list = list(existing_songs)
        added_count = 0
        
        for song in new_songs:
            if song.get('url') not in existing_urls:
                song["id"] = len(updated_list) + 1
                updated_list.append(song)
                existing_urls.add(song.get('url'))
                added_count += 1
        
        ref.set(updated_list)
        print(f"Selesai! Menambahkan {added_count} lagu baru. Total lagu: {len(updated_list)}")
    except Exception as e:
        print(f"Gagal mengunggah ke Firebase: {e}")
        sys.exit(1)

def search_archive_org(query, rows=100):
    url = "https://archive.org/advancedsearch.php"
    params = {
        "q": query,
        "fl[]": "identifier",
        "rows": rows,
        "page": 1,
        "output": "json"
    }
    try:
        response = requests.get(url, params=params, timeout=20)
        if response.status_code == 200:
            docs = response.json().get("response", {}).get("docs", [])
            return [doc["identifier"] for doc in docs]
    except Exception as e:
        print(f"Error saat mencari di Archive.org: {e}")
    return []

def fetch_files_from_identifier(identifier):
    url = f"https://archive.org/metadata/{identifier}"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200: return []
        
        data = response.json()
        files = data.get("files", [])
        songs = []
        
        for file in files:
            if file.get("name", "").lower().endswith(".mp3"):
                duration = float(file.get("length", 0))
                if 0 < duration <= 300:
                    title = file.get("title", file.get("name").replace(".mp3", "").replace("_", " "))
                    # Menggunakan fungsi kategori baru
                    category = tentukan_kategori(title)
                    
                    songs.append({
                        "title": title,
                        "url": f"https://archive.org/download/{identifier}/{file.get('name')}",
                        "duration": duration,
                        "category": category
                    })
        return songs
    except Exception as e:
        return []

if __name__ == "__main__":
    print("Memulai pencarian lagu rohani secara dinamis...")
    
    queries = [
        'title:("lagu rohani" OR "lagu rohani kristen") AND mediatype:audio',
        'subject:("lagu rohani" OR "kristen" OR "pujian") AND mediatype:audio'
    ]
    
    all_new_songs = []
    processed_ids = set()
    
    for q in queries:
        ids = search_archive_org(q, rows=50)
        for album_id in ids:
            if album_id not in processed_ids:
                print(f"Mengambil lagu dari koleksi: {album_id}")
                songs = fetch_files_from_identifier(album_id)
                all_new_songs.extend(songs)
                processed_ids.add(album_id)
        
    if all_new_songs:
        update_songs_to_firebase(all_new_songs)
    else:
        print("Tidak ada lagu baru ditemukan.")
