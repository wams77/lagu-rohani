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

def update_songs_to_firebase(list_lagu):
    try:
        ref = db.reference('songs')
        ref.set(list_lagu)
        print(f"Berhasil memperbarui {len(list_lagu)} lagu ke Firebase!")
    except Exception as e:
        print(f"Gagal mengunggah ke Firebase: {e}")
        sys.exit(1)

def get_identifiers_from_search(query, max_items=5):
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
            if file.get("name", "").lower().endswith(".mp3"):
                title = file.get("title", file.get("name").replace(".mp3", "").replace("_", " "))
                songs.append({
                    "title": title,
                    "url": f"https://archive.org/download/{identifier}/{file.get('name')}",
                    "size": file.get("size", "0")
                })
        return songs
    except Exception as e:
        print(f"Gagal mengambil file dari {identifier}: {e}")
        return []

if __name__ == "__main__":
    print("Memulai proses pencarian...")
    search_query = 'title:"lagu rohani" OR subject:"lagu rohani"'
    album_ids = get_identifiers_from_search(search_query, max_items=5)
    
    if not album_ids:
        print("Tidak ada album ditemukan.")
        sys.exit(0)
    
    all_songs = []
    for album_id in album_ids:
        print(f"Mengambil lagu dari: {album_id}")
        songs = fetch_files_from_identifier(album_id)
        all_songs.extend(songs)
    
    for idx, song in enumerate(all_songs):
        song["id"] = idx + 1
        song["category"] = "Worship"
        
    if all_songs:
        update_songs_to_firebase(all_songs)
    else:
        print("Tidak ada lagu ditemukan untuk diunggah.")
