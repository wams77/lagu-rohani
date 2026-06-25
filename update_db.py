import firebase_admin
import json
import os
from firebase_admin import credentials, db

# Inisialisasi Firebase
service_account_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
if not service_account_json:
    print("ERROR: FIREBASE_SERVICE_ACCOUNT tidak ditemukan.")
    exit(1)

cred = credentials.Certificate(json.loads(service_account_json))
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://lagu-rohani-b507a-default-rtdb.asia-southeast1.firebasedatabase.app'
    })

def bersihkan_judul_dan_artis(title, artist):
    # Logika sederhana pembersihan nama artis
    clean_artist = artist.replace("Worship Leader", "").replace("Penyembahan", "").strip()
    return title.strip(), clean_artist.strip()

def filter_content(title, artist):
    # FILTER UTAMA: Menolak Bigman Sirait
    blacklist = ["bigman sirait"]
    if any(term in artist.lower() for term in blacklist) or any(term in title.lower() for term in blacklist):
        return False
    return True

def run_update():
    # ... logic scraping Anda di sini ...
    # Pastikan setiap lagu yang akan di-push ke database melewati:
    # if filter_content(raw_title, raw_artist):
    #     push_to_firebase()
    print("Sistem filter Bigman Sirait aktif.")

if __name__ == "__main__":
    run_update()
