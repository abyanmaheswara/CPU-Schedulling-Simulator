# Aplikasi web Flask untuk simulasi penjadwalan CPU
# File: app.py
# Tujuan: Menghubungkan logika scheduling (dari scheduler.py) ke antarmuka web
# Menggunakan Flask untuk membuat antarmuka web yang memungkinkan pengguna memasukkan data proses
# dan melihat hasil simulasi berbagai algoritma penjadwalan

from flask import Flask, render_template, request
# Mengimpor modul inti dari file logika kita (scheduler.py)
from scheduler import Process, run_all_schedulers, get_default_processes

# Membuat instance aplikasi Flask
app = Flask(__name__)

def parse_form_data(form):
    """
    Fungsi parse_form_data:
    Tujuan: Mengambil data string dari form HTML, memvalidasinya, dan mengonversinya
            menjadi list objek Process yang siap diolah oleh algoritma.
    Ini adalah JEMBATAN antara user input (frontend) dan logika perhitungan (backend).
    """
    processes = []
    # Mengambil list nilai dari form untuk setiap atribut proses
    pids = form.getlist('pid')
    arrivals = form.getlist('arrival_time')
    bursts = form.getlist('burst_time')
    priorities = form.getlist('priority')

    for i in range(len(pids)):
        try:
            # 1. Konversi ke Integer: Wajib dilakukan karena input form selalu berupa string
            pid = int(pids[i])
            arrival = int(arrivals[i])
            burst = int(bursts[i])
            priority = int(priorities[i])
            
            # 2. Validasi Dasar: Memastikan data input valid (misal, Burst Time harus positif)
            if burst > 0:
                processes.append(Process(pid, arrival, burst, priority))
        except (ValueError, IndexError):
            # Penanganan Error: Jika input non-angka atau tidak lengkap, entry tersebut dilewati
            # Ini mencegah aplikasi crash karena input user yang salah.
            continue
    return processes

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Rute Utama ('/'): Menangani tampilan halaman beranda dan logika simulasi.
    Ini adalah FUNGSI KONTROLER yang menentukan alur data.
    """
    if request.method == 'POST':
        # 1. POST Request (Ketika user SUBMIT data):
        # Ambil dan validasi data dari form
        processes = parse_form_data(request.form)
        
        # Penanganan data kosong/invalid: Jika tidak ada proses valid, gunakan data default
        if not processes: 
            processes = get_default_processes()
    else:
        # 2. GET Request (Akses halaman PERTAMA KALI):
        # Tampilkan data proses default sebagai contoh awal di form
        processes = get_default_processes()
    
    # 3. Eksekusi Simulasi: Panggil fungsi dari scheduler.py
    # 'results' akan berisi data terstruktur dari FCFS, SJF, RR, dan Priority
    results = run_all_schedulers(processes)
    
    # 4. Render ke Frontend: Kirim hasil perhitungan dan data proses yang digunakan
    # ke template HTML (index.html) untuk visualisasi.
    return render_template('index.html', results=results, processes=processes)

if __name__ == '__main__':
    # Jalankan aplikasi Flask:
    # `debug=True` sangat berguna selama development karena akan me-restart server secara otomatis
    # saat ada perubahan kode dan menampilkan pesan error di browser.
    app.run(debug=True)