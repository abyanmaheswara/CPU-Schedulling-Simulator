# Aplikasi web Flask untuk simulasi penjadwalan CPU
# Menggunakan Flask untuk membuat antarmuka web yang memungkinkan pengguna memasukkan data proses
# dan melihat hasil simulasi berbagai algoritma penjadwalan

from flask import Flask, render_template, request
from scheduler import Process, run_all_schedulers, get_default_processes

# Membuat instance aplikasi Flask
app = Flask(__name__)

def parse_form_data(form):
    """
    Mengurai data dari formulir web dan membuat daftar objek Process.
    Fungsi ini memvalidasi input pengguna dan membuat proses hanya jika data valid.
    """
    processes = []
    # Mengambil daftar nilai dari formulir untuk setiap atribut proses
    pids = form.getlist('pid')
    arrivals = form.getlist('arrival_time')
    bursts = form.getlist('burst_time')
    priorities = form.getlist('priority')

    for i in range(len(pids)):
        try:
            # Mengonversi string ke integer
            pid = int(pids[i])
            arrival = int(arrivals[i])
            burst = int(bursts[i])
            priority = int(priorities[i])
            if burst > 0:  # Pastikan waktu burst positif
                processes.append(Process(pid, arrival, burst, priority))
        except (ValueError, IndexError):
            # Lewati entri yang tidak valid atau tidak lengkap
            continue
    return processes

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        processes = parse_form_data(request.form)
        if not processes: # If form is empty or invalid, use default
            processes = get_default_processes()
    else:
        # Get the default process data for GET request
        processes = get_default_processes()
    
    # Run all scheduling algorithms
    results = run_all_schedulers(processes)
    
    return render_template('index.html', results=results, processes=processes)

if __name__ == '__main__':
    # Menjalankan aplikasi Flask dalam mode debug untuk pengembangan
    app.run(debug=True)
