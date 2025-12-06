# CPU Scheduling Simulator

Sebuah aplikasi berbasis web yang mensimulasikan berbagai algoritma penjadwalan CPU dan memvisualisasikan hasilnya dengan Gantt Chart, serta menghitung waktu tunggu rata-rata.

## Fitur

*   **Simulasi Algoritma Penjadwalan CPU:**
    *   First-Come, First-Served (FCFS)
    *   Shortest Job First (SJF)
    *   Round Robin (RR)
    *   Priority Scheduling
*   **Antarmuka Pengguna Berbasis Web (GUI):** Menggunakan Flask untuk visualisasi yang interaktif.
*   **Gantt Chart:** Menampilkan urutan eksekusi proses secara grafis.
*   **Metrik Kinerja:** Menghitung waktu tunggu dan waktu perputaran untuk setiap proses, serta waktu tunggu rata-rata.
*   **Input Proses Dinamis:** Memungkinkan pengguna untuk menambah, mengedit, dan menghapus proses langsung dari antarmuka web.

## Teknologi yang Digunakan

*   **Backend:** Python 3
*   **Web Framework:** Flask
*   **Frontend:** HTML, CSS (dengan Bootstrap untuk styling), JavaScript

## Cara Setup dan Menjalankan Proyek

Ikuti langkah-langkah di bawah ini untuk mengatur dan menjalankan simulator di mesin lokal Anda.

### 1. Clone Repositori (Jika belum)

Jika Anda belum meng-clone repositori ini, gunakan perintah berikut:

```bash
git clone https://github.com/abyanmaheswara/CPU-Schedulling-Simulator.git
cd CPU-Schedulling-Simulator
```

### 2. Buat Virtual Environment (Disarankan)

Membuat virtual environment akan membantu mengelola dependensi proyek tanpa mengganggu instalasi Python global Anda.

```bash
python -m venv venv
```

### 3. Aktifkan Virtual Environment

*   **Windows:**
    ```bash
    .\venv\Scripts\activate
    ```
*   **macOS/Linux:**
    ```bash
    source venv/bin/activate
    ```

### 4. Install Dependensi

Instal semua library Python yang dibutuhkan menggunakan pip:

```bash
pip install Flask
```

### 5. Jalankan Aplikasi Web

Setelah dependensi terinstal, Anda dapat menjalankan aplikasi Flask:

```bash
python app.py
```

Anda akan melihat output di terminal yang menunjukkan bahwa server Flask telah dimulai, biasanya di `http://127.0.0.1:5000/`.

### 6. Akses Aplikasi

Buka browser web Anda dan navigasikan ke alamat:

```
http://127.0.0.1:5000/
```

## Penggunaan Aplikasi

Pada antarmuka web, Anda akan melihat tabel proses yang dapat Anda konfigurasi:

*   **Edit Data Proses:** Ubah nilai PID, Arrival Time, Burst Time, atau Priority di kolom input.
*   **Tambah Proses:** Klik tombol "Add Process" untuk menambahkan baris baru ke tabel.
*   **Hapus Proses:** Klik tombol "Remove" di samping baris proses untuk menghapusnya.
*   **Simulasikan Ulang:** Setelah Anda melakukan perubahan pada data proses, klik tombol "Recalculate & Simulate" untuk menjalankan kembali semua algoritma penjadwalan dengan data baru Anda. Hasil Gantt Chart dan metrik kinerja akan diperbarui secara otomatis di halaman.

Selamat mencoba simulasi!
