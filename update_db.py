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
    # Data 130 Lagu Mentah
    raw_data = [
        {"id": 1, "title": "Sejauh Timur Dari Barat", "size": "6.3 MB", "category": "Worship"},
        {"id": 2, "title": "Terlalu Besar - Mike Mohede", "size": "4.0 MB", "category": "Penyembahan"},
        {"id": 3, "title": "Hanya Kau Tuhan", "size": "3.0 MB", "category": "Saat Teduh"},
        {"id": 4, "title": "Tetap Kupercaya", "size": "3.4 MB", "category": "Praise"},
        {"id": 5, "title": "Tetap Setia", "size": "4.7 MB", "category": "Worship"},
        {"id": 6, "title": "Tiada Yang Sukar", "size": "3.3 MB", "category": "Penyembahan"},
        {"id": 7, "title": "Sbab Kau Besar", "size": "5.4 MB", "category": "Saat Teduh"},
        {"id": 8, "title": "Trust In You - Amanda Nitisastro", "size": "3.3 MB", "category": "Praise"},
        {"id": 9, "title": "Tuhan Dengar Doaku", "size": "4.7 MB", "category": "Worship"},
        {"id": 10, "title": "Tuhan Dipihakku", "size": "4.7 MB", "category": "Penyembahan"},
        {"id": 11, "title": "Berharga BagiMu", "size": "3.9 MB", "category": "Saat Teduh"},
        {"id": 12, "title": "Tuhan Melihat Hati", "size": "3.7 MB", "category": "Praise"},
        {"id": 13, "title": "Tuhan Pasti Sanggup - Jason Irwan", "size": "5.1 MB", "category": "Worship"},
        {"id": 14, "title": "Tuhan Punya Cara", "size": "4.5 MB", "category": "Penyembahan"},
        {"id": 15, "title": "Tuhan Selalu Punya Cara - Jason Irwan", "size": "4.1 MB", "category": "Saat Teduh"},
        {"id": 16, "title": "Tuhan Tak Pernah Salah - Jason Irwan", "size": "4.1 MB", "category": "Praise"},
        {"id": 17, "title": "Tuhan Yang Tak Terbatas", "size": "3.3 MB", "category": "Worship"},
        {"id": 18, "title": "Tuhan Yesus Baik", "size": "3.1 MB", "category": "Penyembahan"},
        {"id": 19, "title": "Waktu Tuhan", "size": "3.4 MB", "category": "Saat Teduh"},
        {"id": 20, "title": "Walau Ku Tak Dapat Melihat", "size": "4.1 MB", "category": "Praise"},
        {"id": 21, "title": "Yesus Benteng Hidupku", "size": "3.3 MB", "category": "Worship"},
        {"id": 22, "title": "Berjejakan Anugerah", "size": "4.3 MB", "category": "Penyembahan"},
        {"id": 23, "title": "Yesus Jawabanku - Maria Shandi", "size": "5.2 MB", "category": "Saat Teduh"},
        {"id": 24, "title": "Yesus Kupercaya", "size": "3.6 MB", "category": "Praise"},
        {"id": 25, "title": "Yesus Peganglah Erat Tanganku", "size": "3.9 MB", "category": "Worship"},
        {"id": 26, "title": "Yesus Segalanya", "size": "3.0 MB", "category": "Penyembahan"},
        {"id": 27, "title": "Yesus Sukacitaku", "size": "3.9 MB", "category": "Saat Teduh"},
        {"id": 28, "title": "Yesuslah Penolongku", "size": "3.8 MB", "category": "Praise"},
        {"id": 29, "title": "You Are My Father - Amanda Nitisastro", "size": "3.7 MB", "category": "Worship"},
        {"id": 30, "title": "You Have Search Me - Amanda Nitisastro", "size": "3.7 MB", "category": "Penyembahan"},
        {"id": 31, "title": "Biarkan Ku Menyembah", "size": "4.3 MB", "category": "Saat Teduh"},
        {"id": 32, "title": "Bila Kupandang", "size": "3.2 MB", "category": "Praise"},
        {"id": 33, "title": "Bunda Maria", "size": "3.7 MB", "category": "Worship"},
        {"id": 34, "title": "Campur Tangan Tuhan", "size": "4.2 MB", "category": "Penyembahan"},
        {"id": 35, "title": "Campur Tangan Tuhan - Kezia Sunarko", "size": "4.2 MB", "category": "Saat Teduh"},
        {"id": 36, "title": "Detak di Hidupku", "size": "4.0 MB", "category": "Praise"},
        {"id": 37, "title": "Dia Buka Jalan", "size": "2.6 MB", "category": "Worship"},
        {"id": 38, "title": "Masih Ada Jalan", "size": "4.4 MB", "category": "Penyembahan"},
        {"id": 39, "title": "Berharap PadaMu", "size": "4.4 MB", "category": "Saat Teduh"},
        {"id": 40, "title": "Dia Mengerti", "size": "5.8 MB", "category": "Praise"},
        {"id": 41, "title": "DihadiratMu", "size": "5.1 MB", "category": "Worship"},
        {"id": 42, "title": "Doa Bapa Kami", "size": "3.3 MB", "category": "Penyembahan"},
        {"id": 43, "title": "Doa Yabes", "size": "4.4 MB", "category": "Saat Teduh"},
        {"id": 44, "title": "Falling In Love With Jesus - Maria Shandi", "size": "3.6 MB", "category": "Praise"},
        {"id": 45, "title": "Firman Jadi Manusia", "size": "3.8 MB", "category": "Worship"},
        {"id": 46, "title": "FirmanMu Tetap Terbukti", "size": "4.4 MB", "category": "Penyembahan"},
        {"id": 47, "title": "Hanya Anugerah - Maria Shandi", "size": "3.8 MB", "category": "Saat Teduh"},
        {"id": 48, "title": "Bunda Maria (Versi 2)", "size": "3.6 MB", "category": "Praise"},
        {"id": 49, "title": "Allah Turut Bekerja", "size": "3.2 MB", "category": "Worship"},
        {"id": 50, "title": "Hatiku Bersandar - Jason Irwan", "size": "3.1 MB", "category": "Penyembahan"},
        {"id": 51, "title": "Hatiku Percaya", "size": "5.0 MB", "category": "Saat Teduh"},
        {"id": 52, "title": "Hatiku Ada Bagiku", "size": "5.0 MB", "category": "Praise"},
        {"id": 53, "title": "I am Here", "size": "4.0 MB", "category": "Worship"},
        {"id": 54, "title": "Itu Namanya Cinta", "size": "4.9 MB", "category": "Penyembahan"},
        {"id": 55, "title": "Jejak Penuh Anugerah", "size": "3.5 MB", "category": "Saat Teduh"},
        {"id": 56, "title": "Ajaib Kau dan Mulia", "size": "11.0 MB", "category": "Praise"},
        {"id": 57, "title": "Kasih Bapa", "size": "4.2 MB", "category": "Worship"},
        {"id": 58, "title": "Kasih SetiaMu", "size": "5.2 MB", "category": "Penyembahan"},
        {"id": 59, "title": "Kasih Tuhan - Jason Irwan", "size": "4.8 MB", "category": "Saat Teduh"},
        {"id": 60, "title": "Allahku Dahsyat", "size": "3.0 MB", "category": "Praise"},
        {"id": 61, "title": "Kasih Tuhan", "size": "3.5 MB", "category": "Worship"},
        {"id": 62, "title": "Kau Hapus Air Mataku", "size": "3.8 MB", "category": "Penyembahan"},
        {"id": 63, "title": "Kau Satu-satunya Harapan", "size": "3.1 MB", "category": "Saat Teduh"},
        {"id": 64, "title": "Kau Tetap Ada Saat Semua Tiada", "size": "6.0 MB", "category": "Praise"},
        {"id": 65, "title": "Kau Tuhan Adalah Bapaku - Maria Shandi", "size": "4.9 MB", "category": "Worship"},
        {"id": 66, "title": "Kekuatan Hatiku", "size": "3.7 MB", "category": "Penyembahan"},
        {"id": 67, "title": "Kekuatan Hatiku (Versi 2)", "size": "3.9 MB", "category": "Saat Teduh"},
        {"id": 68, "title": "Kekuatan Hatiku (Versi 3)", "size": "3.6 MB", "category": "Praise"},
        {"id": 69, "title": "Kekuatan Hatiku - Wawan Yap", "size": "3.6 MB", "category": "Worship"},
        {"id": 70, "title": "Kemurahan Tuhan", "size": "4.1 MB", "category": "Penyembahan"},
        {"id": 71, "title": "Anugerah Terindah", "size": "4.7 MB", "category": "Saat Teduh"},
        {"id": 72, "title": "Kesetiaan Tuhan", "size": "4.1 MB", "category": "Praise"},
        {"id": 73, "title": "Kesetiaan Tuhan (Versi 2)", "size": "4.0 MB", "category": "Worship"},
        {"id": 74, "title": "Ku Berserah", "size": "3.7 MB", "category": "Penyembahan"},
        {"id": 75, "title": "Ku Perlu Kau Tuhan", "size": "4.4 MB", "category": "Saat Teduh"},
        {"id": 76, "title": "Kuperlu Kau Tuhan (Versi 2)", "size": "4.7 MB", "category": "Praise"},
        {"id": 77, "title": "Ku Tetap Setia", "size": "3.3 MB", "category": "Worship"},
        {"id": 78, "title": "Kuberserah", "size": "3.6 MB", "category": "Penyembahan"},
        {"id": 79, "title": "Kunyanyi Haleluya", "size": "5.1 MB", "category": "Saat Teduh"},
        {"id": 80, "title": "Kurindu MengenalMu", "size": "2.4 MB", "category": "Praise"},
        {"id": 81, "title": "Kusembah Kau", "size": "3.9 MB", "category": "Worship"},
        {"id": 82, "title": "Anugerah Terindah - Veren", "size": "5.2 MB", "category": "Penyembahan"},
        {"id": 83, "title": "Lebih Dari Yang Aku Tahu", "size": "3.9 MB", "category": "Saat Teduh"},
        {"id": 84, "title": "Lebih Indah DiriMU - Amanda Nitisastro", "size": "3.4 MB", "category": "Praise"},
        {"id": 85, "title": "Lord of the Future", "size": "3.5 MB", "category": "Worship"},
        {"id": 86, "title": "Lost & Found", "size": "4.2 MB", "category": "Penyembahan"},
        {"id": 87, "title": "Masih Ada Harapan", "size": "4.4 MB", "category": "Saat Teduh"},
        {"id": 88, "title": "Masih Ada Tuhan", "size": "3.8 MB", "category": "Praise"},
        {"id": 89, "title": "Masuk HadiratMu Tuhan", "size": "3.8 MB", "category": "Worship"},
        {"id": 90, "title": "Mata Hatiku - Jason Irwan", "size": "4.5 MB", "category": "Penyembahan"},
        {"id": 91, "title": "Mataku Tertuju PadaMu", "size": "5.3 MB", "category": "Saat Teduh"},
        {"id": 92, "title": "Mataku Tertuju PadaMu (Versi 2)", "size": "4.7 MB", "category": "Praise"},
        {"id": 93, "title": "Bapa Selidiki Hatiku", "size": "4.2 MB", "category": "Worship"},
        {"id": 94, "title": "Mengenal Hatiku", "size": "5.3 MB", "category": "Penyembahan"},
        {"id": 95, "title": "Menari Buat Tuhan", "size": "2.8 MB", "category": "Saat Teduh"},
        {"id": 96, "title": "Mengampuni", "size": "4.2 MB", "category": "Praise"},
        {"id": 97, "title": "MengenalMu", "size": "3.7 MB", "category": "Worship"},
        {"id": 98, "title": "Pada Yesus", "size": "4.4 MB", "category": "Penyembahan"},
        {"id": 99, "title": "Pada Yesus (Versi 2)", "size": "3.3 MB", "category": "Saat Teduh"},
        {"id": 100, "title": "God Sees Me - El Roi", "size": "9.7 MB", "category": "Praise"},
        {"id": 101, "title": "Pemilik Hidupku", "size": "4.0 MB", "category": "Worship"},
        {"id": 102, "title": "Pemilik Hidupku (Versi 2)", "size": "4.0 MB", "category": "Penyembahan"},
        {"id": 103, "title": "Pemulihan Keluarga", "size": "3.5 MB", "category": "Saat Teduh"},
        {"id": 104, "title": "Bapaku Yang Ajaib", "size": "3.7 MB", "category": "Praise"},
        {"id": 105, "title": "PenyertaanMu", "size": "3.9 MB", "category": "Worship"},
        {"id": 106, "title": "Percaya", "size": "4.9 MB", "category": "Penyembahan"},
        {"id": 107, "title": "PertolonganMu", "size": "4.5 MB", "category": "Saat Teduh"},
        {"id": 108, "title": "PertolonganMu (Long Version)", "size": "6.8 MB", "category": "Praise"},
        {"id": 109, "title": "Piano Worship - Marthin Siahaan", "size": "13.5 MB", "category": "Worship"},
        {"id": 110, "title": "Saat Kau Berkati", "size": "4.2 MB", "category": "Penyembahan"},
        {"id": 111, "title": "Satu-Satunya Yang Kuandalkan - Angel Pieters", "size": "4.5 MB", "category": "Saat Teduh"},
        {"id": 112, "title": "Selalu Ada UntukKu", "size": "2.9 MB", "category": "Praise"},
        {"id": 113, "title": "Selalu diHatiku", "size": "4.4 MB", "category": "Worship"},
        {"id": 114, "title": "Sentuh Hatiku", "size": "4.3 MB", "category": "Penyembahan"},
        {"id": 115, "title": "Bapaku Yang Ku Cinta", "size": "3.8 MB", "category": "Saat Teduh"},
        {"id": 116, "title": "Serahkanlah Bebanmu", "size": "4.7 MB", "category": "Praise"},
        {"id": 117, "title": "S'gala Puji - Amanda Nitisastro", "size": "2.9 MB", "category": "Worship"},
        {"id": 118, "title": "Switch", "size": "5.0 MB", "category": "Penyembahan"},
        {"id": 119, "title": "Tak Pernah Sendiri", "size": "3.5 MB", "category": "Saat Teduh"},
        {"id": 120, "title": "Tak Pernah Terlambat", "size": "3.2 MB", "category": "Praise"},
        {"id": 121, "title": "Take Us Deeper - Surjadi Sunarko", "size": "6.5 MB", "category": "Worship"},
        {"id": 122, "title": "Tangan Tuhan - Jason Irwan", "size": "3.6 MB", "category": "Penyembahan"},
        {"id": 123, "title": "Tangan Yang Kuat Menopangku - Surjadi Sunarko", "size": "5.8 MB", "category": "Saat Teduh"},
        {"id": 124, "title": "Tenanglah Kini Hatiku - Maria Shandi", "size": "3.4 MB", "category": "Praise"},
        {"id": 125, "title": "Terima Kasih Tuhan", "size": "4.0 MB", "category": "Worship"},
        {"id": 126, "title": "Tetap Percaya", "size": "3.5 MB", "category": "Penyembahan"},
        {"id": 127, "title": "Tetap Percaya PadaMu", "size": "3.5 MB", "category": "Saat Teduh"},
        {"id": 128, "title": "Tidak Pernah Gagal", "size": "4.0 MB", "category": "Praise"},
        {"id": 129, "title": "Tuhan Itu Baik", "size": "3.8 MB", "category": "Worship"},
        {"id": 130, "title": "Tuhan Kau Gembala Hidupku", "size": "4.2 MB", "category": "Penyembahan"}
    ]

    colors = ["1e40af", "9d174d", "065f46", "b45309", "3f3f46", "4c1d95", "b91c1c", "0f766e"]
    
    formatted_songs = []
    
    # Looping untuk merapikan data, memisahkan artis, dan menambahkan URL
    for index, item in enumerate(raw_data):
        title = item["title"]
        artist = "Worship Leader"
        
        # Jika ada tanda strip (-), pisahkan judul dan artis
        if " - " in title:
            parts = title.split(" - ", 1)
            title = parts[0].strip()
            artist = parts[1].strip()

        # Generate dua huruf awal untuk cover
        cover_text = title[:2].upper() if len(title) >= 2 else "SG"

        formatted_songs.append({
            "id": item["id"],
            "title": title,
            "artist": artist,
            "duration": "04:30",
            "size": item["size"],
            "category": item["category"],
            "coverColor": colors[index % len(colors)],
            "coverText": cover_text,
            "url": f"https://archive.org/download/c-84_20250706/C{item['id']}.mp3"
        })

    # Mengunggah data yang sudah rapi ke Firebase
    update_songs_to_firebase(formatted_songs)
