import firebase_admin
import json
import os
import re
from firebase_admin import credentials, db

# Inisialisasi Firebase
service_account_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT')

if service_account_json:
    try:
        service_account_info = json.loads(service_account_json)
        cred = credentials.Certificate(service_account_info)
    except Exception as e:
        print(f"ERROR: {e}")
        exit(1)
else:
    try:
        cred = credentials.Certificate('firebase-key.json')
    except:
        print("ERROR: Kredensial tidak ditemukan.")
        exit(1)

try:
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://lagu-rohani-b507a-default-rtdb.asia-southeast1.firebasedatabase.app'
        })
except Exception as e:
    print(f"Error inisialisasi Firebase: {e}")
    exit(1)

def clean_database():
    """Fungsi utama untuk menarik data, membersihkan (menghapus Bigman Sirait), dan mengunggah kembali."""
    print("Mengambil data lagu dari Firebase...")
    ref = db.reference('songs')
    songs = ref.get()
    
    if not songs:
        print("Database kosong.")
        return

    updated_songs = []
    deleted_count = 0
    
    for song in songs:
        if not song: continue
        
        artist = song.get('artist', '') or ""
        title = song.get('title', '') or ""
        
        # LOGIKA PENGHAPUSAN: Hapus jika artis adalah Bigman Sirait
        if "bigman sirait" in artist.lower():
            print(f"Menghapus lagu (Kategori tidak sesuai): {title} oleh {artist}")
            deleted_count += 1
            continue # Lewati/Hapus
        
        updated_songs.append(song)
        
    if deleted_count > 0:
        print(f"\nMenghapus {deleted_count} lagu. Menyimpan perubahan ke database...")
        ref.set(updated_songs)
        print("Selesai! Database Anda sekarang sudah bersih.")
    else:
        print("\nTidak ada lagu Bigman Sirait ditemukan. Data aman.")

if __name__ == "__main__":
    print("Memulai Skrip Pembersih Database...")
    clean_database()
```

### Langkah Selanjutnya:
1. **Update File:** Buka repositori GitHub Anda, buka file `cleanup_db.py`, klik ikon pensil (Edit), hapus kode lama, dan paste kode di atas. Klik **Commit changes**.
2. **Jalankan Workflow:**
   * Pergi ke tab **Actions**.
   * Klik **"Pembersihan Database Manual"**.
   * Klik **"Run workflow"**.
3. **Hasil:** Setelah *workflow* selesai dengan tanda centang hijau, semua lagu "Bigman Sirait" akan hilang dari database Firebase Anda dan tidak akan muncul lagi di website.
