# SkinCare DSS (Decision Support System)
Deskripsi Proyek


SkinCare DSS adalah sistem pendukung keputusan (Decision Support System) berbasis Graph yang digunakan untuk membantu pengguna memilih produk pelembab (moisturizer) yang sesuai berdasarkan jenis kulit dan masalah kulit yang dialami.


Sistem memanfaatkan struktur data Graph berbobot (Weighted Graph) dan algoritma Dijkstra untuk menentukan rekomendasi produk terbaik berdasarkan jalur dengan bobot total paling rendah.

## Tujuan Proyek

1. Menerapkan konsep Graph dalam studi kasus pemilihan skincare.
2. Mengimplementasikan Weighted Graph menggunakan Adjacency List.
3. Menggunakan algoritma Dijkstra untuk pencarian jalur terbaik.
4. Menampilkan rekomendasi produk berdasarkan hasil analisis graph.
5. Menyediakan visualisasi graph yang interaktif.
6. Menambahkan fitur AI Recommendation dan Centrality Analysis.

## Konsep Graph yang Digunakan

1. Representasi Data

Graph digunakan untuk merepresentasikan hubungan antar data:

Jenis Kulit → Masalah Kulit → Kandungan Aktif → Produk Pelembab

2. Analisis Hubungan

Graph memungkinkan sistem menganalisis hubungan antar node sehingga dapat diketahui:

Masalah kulit yang terkait dengan jenis kulit tertentu.
Kandungan aktif yang sesuai untuk suatu masalah kulit.
Produk yang mengandung kandungan aktif tersebut.

3. Optimasi Keputusan

Setiap edge memiliki bobot yang menunjukkan tingkat kecocokan.

Semakin kecil bobot total jalur:

Jenis Kulit → Masalah → Kandungan → Produk

maka semakin tinggi tingkat rekomendasinya.

## Implementasi Graph

Adjacency List

Graph disimpan menggunakan struktur dictionary Python.

Contoh:

graph = {
    "Jerawat": {
        "Salicylic Acid": 1,
        "Centella": 1
    }
}

Weighted Graph

Setiap hubungan memiliki bobot.

Contoh:

"Salicylic Acid": {
    "Azarine Oil Free Moisturizer": 1,
    "Acnes Moisturizer": 2
}

Bobot digunakan oleh algoritma Dijkstra untuk menentukan jalur terbaik.

## Algoritma Graph

Dijkstra Algorithm

Algoritma Dijkstra digunakan untuk mencari jalur dengan total bobot terkecil dari node masalah kulit menuju node produk.

Langkah kerja:

Memilih node awal (Masalah Kulit).
Menghitung jarak minimum ke seluruh node.
Menyimpan jalur terbaik.
Menghasilkan rekomendasi produk dengan skor terkecil.
