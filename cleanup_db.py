import firebase_admin
import json
import os
from firebase_admin import credentials, db

# Inisialisasi Firebase
service_account_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT')

if not service_account_json:
    print("ERROR: FIREBASE_SERVICE_ACCOUNT tidak ditemukan di environment.")
    exit(1)

try:
    # Coba memuat JSON
    service_account_info = json.loads(service_account_json)
    cred = credentials.Certificate(service_account_info)
    
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://lagu-rohani-b507a-default-rtdb.asia-southeast1.firebasedatabase.app'
        })
    print("Firebase terinisialisasi dengan sukses.")
except Exception as e:
    print(f"ERROR Fatal saat inisialisasi Firebase: {e}")
    exit(1)

def clean_database():
    print("Mengambil data lagu dari Firebase...")
    ref = db.reference('songs')
    songs = ref.get()
    
    if not songs:
        print("Database kosong.")
        return

    # Jika database berupa list, kita ubah jadi list baru
    if isinstance(songs, dict):
        updated_songs = [s for s in songs.values() if s]
    else:
        updated_songs = [s for s in songs if s]

    original_count = len(updated_songs)
    
    # Filter Bigman Sirait
    cleaned_songs = []
    deleted_count = 0
    
    for song in updated_songs:
        artist = str(song.get('artist', '')).lower()
        title = str(song.get('title', '')).lower()
        
        if "bigman sirait" in artist or "bigman sirait" in title:
            print(f"Menghapus: {title} oleh {artist}")
            deleted_count += 1
            continue
        
        cleaned_songs.append(song)
        
    if deleted_count > 0:
        print(f"\nMenghapus {deleted_count} lagu. Menyimpan {len(cleaned_songs)} lagu tersisa...")
        ref.set(cleaned_songs)
        print("Selesai! Database bersih.")
    else:
        print("\nTidak ada konten Bigman Sirait ditemukan. Data aman.")

if __name__ == "__main__":
    clean_database()
