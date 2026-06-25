import firebase_admin
import json
import os
import re
from firebase_admin import credentials, db

# Inisialisasi Firebase
# Anda bisa menggunakan environment variable seperti sebelumnya, 
# atau langsung arahkan ke file JSON credential lokal Anda jika dijalankan di komputer.
service_account_json = os.getenv('FIREBASE_SERVICE_ACCOUNT')

if service_account_json:
    service_account_info = json.loads(service_account_json)
    cred = credentials.Certificate(service_account_info)
else:
    # Jika dijalankan lokal di PC, pastikan file JSON ada di folder yang sama
    # Ganti 'firebase-key.json' dengan nama file kunci asli Anda jika ada.
    try:
        cred = credentials.Certificate('firebase-key.json')
    except:
        print("Error: Tidak menemukan FIREBASE_SERVICE_ACCOUNT atau file firebase-key.json")
        exit(1)

try:
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://lagu-rohani-b507a-default-rtdb.asia-southeast1.firebasedatabase.app'
        })
except Exception as e:
    print(f"Error inisialisasi Firebase: {e}")
    exit(1)

def is_valid_artist_name(name):
    """Memeriksa apakah string adalah nama artis yang valid."""
    if not name or len(name) < 2:
        return False
    
    # Daftar kata kunci yang menandakan itu BUKAN penyanyi
    invalid_keywords = [
        'media', 'studio', 'channel', 'record', 'production', 'music', 
        'official', 'album', 'vol', 'volume', 'kumpulan', 'kompilasi', 
        'lagu', 'rohani', 'terbaik', 'terpopuler', 'audio', 'mp3', 'kbps',
        'y2mate', 'yt1s', 'cover', 'akustik', 'instrumental'
    ]
    
    name_lower = name.lower()
    
    # Filter jika hanya angka
    if name.strip().isdigit():
        return False
        
    # Filter jika mengandung kata kunci tidak valid
    if any(keyword in name_lower for keyword in invalid_keywords):
        return False
        
    # Filter jika tidak ada huruf alfabet sama sekali
    if not re.search('[a-zA-Z]', name):
        return False
        
    return True

def bersihkan_judul_dan_artis(raw_title, raw_artist):
    """Mengekstrak dan merapikan artis dari judul yang kotor."""
    final_title = raw_title.replace(".mp3", "").replace("_", " ").strip()
    final_artist = raw_artist.strip() if raw_artist else ""
    
    # 1. Cek apakah artis bawaan valid
    if not is_valid_artist_name(final_artist):
        final_artist = "Worship Leader"
    else:
        final_artist = final_artist.title()
    
    # 2. Ekstrak nama artis dari judul jika ada " - " (Contoh: "Alfonso Sahetapy - Judul Lagu")
    if " - " in final_title:
        parts = final_title.split(" - ", 1)
        potential_artist = parts[0].strip()
        potential_title = parts[1].strip()
        
        # Jika bagian kiri adalah nama artis yang valid, gunakan itu
        if is_valid_artist_name(potential_artist):
            final_artist = potential_artist.title()
            final_title = potential_title
    
    # 3. Bersihkan sisa-sisa teks sampah di judul
    # Menghapus [128kbps], (y2mate.com), angka di depan, dll
    final_title = re.sub(r'(?i)\b\d+kbps\b|\.com|\.net|y2mate|yt1s', '', final_title)
    final_title = re.sub(r'[\[\(\{].*?[\]\)\}]', '', final_title) # Hapus teks dalam kurung
    final_title = re.sub(r'^[-_.\s\d]+|[-_.\s]+$', '', final_title) # Hapus karakter aneh di ujung
    
    # Jika setelah dibersihkan judul jadi kosong, kembalikan ke aslinya
    if not final_title:
        final_title = raw_title
        
    return final_title.strip(), final_artist

def clean_database():
    """Fungsi utama untuk menarik data, membersihkan, dan mengunggah kembali."""
    print("Mengambil data lagu dari Firebase...")
    ref = db.reference('songs')
    songs = ref.get()
    
    if not songs:
        print("Database kosong.")
        return

    updated_count = 0
    cleaned_songs = []
    
    for song in songs:
        if not song: continue # Lewati entri kosong (null)
        
        original_title = song.get('title', '')
        original_artist = song.get('artist', '')
        
        new_title, new_artist = bersihkan_judul_dan_artis(original_title, original_artist)
        
        # Jika ada perubahan, update dan catat
        if new_title != original_title or new_artist != original_artist:
            song['title'] = new_title
            song['artist'] = new_artist
            updated_count += 1
            print(f"Update: '{original_artist}' -> '{new_artist}' | '{original_title}' -> '{new_title}'")
            
        cleaned_songs.append(song)
        
    if updated_count > 0:
        print(f"\nMenyimpan {updated_count} perubahan ke database...")
        ref.set(cleaned_songs)
        print("Selesai! Database Anda sekarang sudah bersih.")
    else:
        print("\nTidak ada lagu yang perlu diperbarui. Data sudah bersih.")

if __name__ == "__main__":
    print("Memulai Skrip Pembersih Database...")
    clean_database()
