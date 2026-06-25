import firebase_admin
import json
import os
import requests
from firebase_admin import credentials, db

service_account_info = json.loads(os.getenv('FIREBASE_SERVICE_ACCOUNT'))
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://lagu-rohani-b507a-default-rtdb.asia-southeast1.firebasedatabase.app'
})

def update_songs_to_firebase(list_lagu):
    ref = db.reference('songs')
    ref.set(list_lagu)
    print(f"Berhasil memperbarui {len(list_lagu)} lagu ke Firebase!")

def get_identifiers_from_search(query, max_items=5):
    url = "https://archive.org/advancedsearch.php"
    params = {
        "q": query,
        "fl[]": "identifier",
        "rows": max_items,
        "page": 1,
        "output": "json"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        docs = response.json().get("response", {}).get("docs", [])
        return [doc["identifier"] for doc in docs]
    return []

def fetch_files_from_identifier(identifier):
    url = f"https://archive.org/metadata/{identifier}"
    response = requests.get(url)
    if response.status_code != 200: return []
    
    data = response.json()
    files = data.get("files", [])
    songs = []
    
    for file in files:
        if file.get("name", "").lower().endswith(".mp3"):
            # Membersihkan nama file menjadi judul
            title = file.get("title", file.get("name").replace(".mp3", "").replace("_", " "))
            songs.append({
                "title": title,
                "url": f"https://archive.org/download/{identifier}/{file.get('name')}",
                "size": file.get("size", "0")
            })
    return songs

if __name__ == "__main__":
    # Mencari item dengan kata kunci "lagu rohani"
    search_query = 'title:"lagu rohani" OR subject:"lagu rohani"'
    album_ids = get_identifiers_from_search(search_query, max_items=5)
    
    all_songs = []
    for album_id in album_ids:
        songs = fetch_files_from_identifier(album_id)
        all_songs.extend(songs)
    
    # Memberi ID unik berurutan
    for idx, song in enumerate(all_songs):
        song["id"] = idx + 1
        song["category"] = "Worship" # Default category
        
    if all_songs:
        update_songs_to_firebase(all_songs)
```

### Langkah yang perlu Anda lakukan sekarang:

1. **Update `update_db.py`**: Gunakan kode di atas untuk menimpa file `update_db.py` yang ada di repository GitHub Anda.
2. **Update `update-songs.yml`**: Pastikan library `requests` sudah terpasang. Ubah bagian `run: pip install firebase-admin` menjadi:
   `run: pip install firebase-admin requests`
3. **Commit & Run**: Lakukan *commit* pada perubahan tersebut dan jalankan ulang Workflow di tab **Actions** GitHub Anda.

**Apa yang terjadi?**
Script ini sekarang tidak lagi bersifat "statis". Ia akan mencari 5 hasil teratas dari Archive.org (berdasarkan kata kunci "lagu rohani"), mengambil daftar lagu dari masing-masing hasil tersebut, dan mengunggahnya ke Firebase Anda secara otomatis. 

Jika nanti Anda ingin mengambil lebih banyak lagu (misal 10 atau 20 koleksi), cukup ubah angka `max_items=5` pada script di atas! Apakah Anda ingin mencoba menjalankannya sekarang?
