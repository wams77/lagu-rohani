import firebase_admin
import json
import os
import requests
import sys
import re
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
        return "Penyembahan"

def is_valid_artist_name(name):
    """Memeriksa apakah string adalah nama artis yang valid (bukan media, studio, atau angka)."""
    if not name or len(name) < 3:
        return False
    
    # Daftar kata kunci yang sering menandakan itu BUKAN penyanyi/artis
    invalid_keywords = [
        'media', 'studio', 'channel', 'record', 'production', 'music', 
        'official', 'album', 'vol', 'volume', 'kumpulan', 'kompilasi', 
        'lagu', 'rohani', 'terbaik', 'terpopuler', 'audio', 'mp3', 'kbps',
        'y2mate', 'yt1s'
    ]
    
    name_lower = name.lower()
    
    # Jika hanya angka (seperti "1")
    if name.isdigit():
        return False
        
    # Jika mengandung kata kunci yang tidak valid
    if any(keyword in name_lower for keyword in invalid_keywords):
        return False
        
    # Pastikan mengandung setidaknya satu huruf alfabet
    if not re.search('[a-zA-Z]', name):
        return False
        
    return True

def bersihkan_judul_dan_artis(raw_title, raw_artist):
    """Mengekstrak artis dari judul (Artis - Judul) dan memvalidasi nama artis."""
    
    final_title = raw_title.replace(".mp3", "").replace("_", " ").strip()
    final_artist = "Worship Leader"
    
    # 1. Coba ambil artis dari metadata bawaan (jika valid)
    if is_valid_artist_name(raw_artist):
        final_artist = raw_artist.title() # Format huruf besar di awal kata
    
    # 2. Seringkali judul berisi "Nama Artis - Judul Lagu"
    if " - " in final_title:
        parts = final_title.split(" - ", 1)
        potential_artist = parts[0].strip()
        potential_title = parts[1].strip()
        
        # Jika bagian depan terlihat seperti nama artis yang valid, gunakan itu
        if is_valid_artist_name(potential_artist):
            final_artist = potential_artist.title()
            final_title = potential_title # Hapus nama artis dari judul
    
    # 3. Filter terakhir jika nama artis masih aneh
    if not is_valid_artist_name(final_artist):
        final_artist = "Worship Leader"
        
    # Bersihkan sisa-sisa angka bitrate atau domain web di judul
    final_title = re.sub(r'(?i)\b\d+kbps\b|\.com|\.net', '', final_title).strip()
    # Hapus karakter aneh di awal atau akhir
    final_title = re.sub(r'^[-_.\s]+|[-_.\s]+$', '', final_title)
        
    return final_title, final_artist

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
        metadata = data.get("metadata", {})
        files = data.get("files", [])
        songs = []
        
        for file in files:
            if file.get("name", "").lower().endswith(".mp3"):
                duration = float(file.get("length", 0))
                if 0 < duration <= 600: # Diperluas ke 10 menit maksimal
                    
                    raw_title = file.get("title") or file.get("name")
                    raw_artist = metadata.get("creator") or metadata.get("artist") or ""
                    
                    clean_title, clean_artist = bersihkan_judul_dan_artis(raw_title, raw_artist)
                    category = tentukan_kategori(clean_title)
                    
                    seo_description = f"Download lagu rohani kristen berjudul {clean_title} oleh {clean_artist} dalam kategori {category}. Dapatkan kualitas suara terbaik untuk saat teduh dan pujian."
                    
                    songs.append({
                        "title": clean_title,
                        "artist": clean_artist,
                        "url": f"https://archive.org/download/{identifier}/{file.get('name')}",
                        "duration": duration,
                        "category": category,
                        "description": seo_description,
                        "keywords": f"download lagu rohani kristen, lagu {clean_artist}, lagu pujian, lagu penyembahan"
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
        
        if len(all_new_songs) > 500: break
        
    if all_new_songs:
        update_songs_to_firebase(all_new_songs)
    else:
        print("Tidak ada lagu baru ditemukan.")
