import firebase_admin
import json
import os
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

if __name__ == "__main__":
    # Ini data contoh. Nantinya, bagian ini diisi dengan script otomatis
    # untuk mengambil link dari Archive.org
    data_lagu_baru = [
        {"id": 1, "title": "Lagu Rohani Test GitHub", "artist": "SolaGratia", "category": "Worship", "url": "https://archive.org/download/c-84_20250706/C1.mp3"}
    ]
    update_songs_to_firebase(data_lagu_baru)
