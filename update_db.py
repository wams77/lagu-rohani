# ... existing code ...
        for file in files:
            if file.get("name", "").lower().endswith(".mp3"):
                duration = float(file.get("length", 0))
                if 0 < duration <= 600: 
                    
                    raw_title = file.get("title") or file.get("name")
                    raw_artist = metadata.get("creator") or metadata.get("artist") or ""
                    
                    clean_title, clean_artist = bersihkan_judul_dan_artis(raw_title, raw_artist)
                    
                    # FILTER BARU: Pastikan Bigman Sirait tidak masuk
                    if "bigman sirait" in clean_artist.lower():
                        continue 

                    category = tentukan_kategori(clean_title)
# ... existing code ...
```

### Langkah yang harus Anda lakukan:

1.  **Update `update_db.py`:** *Copy* seluruh isi `update_db.py` yang baru ini ke GitHub. Dengan kode ini, meskipun ada konten baru yang diunggah ke Internet Archive oleh sumber tersebut, *scraper* Anda akan otomatis menolaknya.
2.  **Jalankan `cleanup_db.py` (Satu Kali Saja):** Jika Anda belum menjalankan `cleanup_db.py` dari instruksi sebelumnya, silakan jalankan sekarang. Skrip tersebut akan membuang semua sisa-sisa konten "Bigman Sirait" yang **sudah terlanjur ada** di database Anda.
3.  **Hasil:** Setelah kedua langkah ini selesai, `cleanup_db.py` akan membersihkan masa lalu, dan `update_db.py` akan menjaga masa depan database Anda agar tetap bersih dari konten tersebut.

Sekarang sistem Anda sudah memiliki sistem "cuci bersih" (cleanup) dan "filter masuk" (update) yang aman!
