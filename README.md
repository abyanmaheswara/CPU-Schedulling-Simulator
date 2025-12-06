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

## Penjelasan Algoritma

Berikut adalah penjelasan singkat mengenai setiap algoritma yang disimulasikan dalam proyek ini.

### 1. First-Come, First-Served (FCFS)
- **Konsep:** Algoritma yang paling sederhana. Proses yang datang pertama akan dilayani hingga selesai, mirip seperti antrian di kasir.
- **Karakteristik:** Non-preemptive (tidak bisa diinterupsi). Begitu proses mulai dieksekusi, ia akan berjalan sampai selesai.
- **Kelebihan:** Sangat mudah dipahami dan diimplementasikan.
- **Kekurangan:** Dapat menyebabkan **convoy effect**, di mana proses-proses singkat harus menunggu selesainya proses yang sangat panjang di depannya. Hal ini menyebabkan waktu tunggu rata-rata yang tinggi dan utilisasi CPU yang tidak efisien.

### 2. Shortest Job First (SJF)
- **Konsep:** Algoritma ini akan menjalankan proses dengan **burst time** (waktu eksekusi) terpendek dari semua proses yang sudah siap di antrian.
- **Karakteristik:** Versi yang diimplementasikan di sini adalah **non-preemptive**.
- **Kelebihan:** Terbukti optimal dalam menghasilkan **average waiting time** (waktu tunggu rata-rata) yang paling minimal.
- **Kekurangan:** Kesulitan terbesarnya adalah memprediksi **burst time** sebuah proses secara akurat di lingkungan nyata. Prediksi yang salah dapat mengurangi keoptimalannya.

### 3. Round Robin (RR)
- **Konsep:** Setiap proses mendapatkan jatah waktu CPU yang sama, yang disebut **time quantum**. Jika proses belum selesai dalam jatah waktu tersebut, ia akan dihentikan sementara (preempted) dan dipindahkan ke belakang antrian siap untuk menunggu giliran berikutnya.
- **Karakteristik:** Preemptive (bisa diinterupsi), dirancang khusus untuk sistem *time-sharing*.
- **Kelebihan:** Sangat adil dan responsif. Tidak ada proses yang mengalami **starvation** (menunggu selamanya). Sangat baik untuk lingkungan interaktif di mana respons cepat lebih penting.
- **Kekurangan:** Kinerja sangat bergantung pada ukuran **time quantum**. Jika *quantum* terlalu kecil, akan terlalu banyak terjadi *context switch* yang memakan overhead CPU. Jika terlalu besar, perilakunya akan mendekati FCFS.

### 4. Priority Scheduling
- **Konsep:** Setiap proses diberi sebuah nilai prioritas. Proses dengan prioritas tertinggi (dalam simulasi ini, nilai numerik yang lebih kecil) akan dijalankan terlebih dahulu.
- **Karakteristik:** Versi yang diimplementasikan di sini adalah **non-preemptive**.
- **Kelebihan:** Memungkinkan eksekusi tugas-tugas penting atau mendesak untuk didahulukan, memberikan fleksibilitas dalam manajemen proses.
- **Kekurangan:** Dapat menyebabkan **starvation**, di mana proses dengan prioritas rendah mungkin tidak akan pernah mendapatkan giliran dieksekusi jika selalu ada proses berprioritas tinggi yang datang.

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
