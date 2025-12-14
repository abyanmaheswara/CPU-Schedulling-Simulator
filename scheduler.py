# File scheduler.py: Berisi implementasi algoritma penjadwalan CPU
# Class Process dan fungsi-fungsi untuk FCFS, SJF, Round Robin, Priority Scheduling

class Process:

    def __init__(self, pid, arrival_time, burst_time, priority=0):
        """
        Inisialisasi objek Process dengan atribut-atribut dasar.
        pid: ID unik proses
        arrival_time: Waktu kedatangan proses
        burst_time: Waktu eksekusi yang dibutuhkan
        priority: Prioritas proses (lebih rendah lebih tinggi prioritas)
        """
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority 

        # Atribut untuk hasil perhitungan
        self.start_time = 0  # Waktu pertama proses mulai dieksekusi (penting untuk Turnaround Time)
        self.completion_time = 0  # Waktu penyelesaian proses
        self.turnaround_time = 0  # Waktu turnaround (completion - arrival)
        self.waiting_time = 0  # Waktu menunggu dalam antrian

        # Atribut tambahan KHUSUS untuk Round Robin dan Preemptive (non-preemptive tidak pakai)
        self.remaining_burst_time = burst_time  # Waktu burst yang tersisa (digunakan RR/Preemptive)
        self.last_execution_end_time = arrival_time  # Waktu akhir eksekusi terakhir (penting untuk hitung Waiting Time RR)
        self.has_started = False  # Flag apakah proses sudah mulai dieksekusi (penting untuk Start Time RR)

    def copy(self):
        """ Membuat salinan objek proses agar algoritma lain bisa berjalan dari data awal yang sama. """
        return Process(self.pid, self.arrival_time, self.burst_time, self.priority)


# --- FCFS Scheduling (Non-Preemptive) ---
def fcfs_scheduling(processes):
    """
    Fungsi FCFS Scheduling: Implementasi First-Come, First-Served.
    Prinsip: Proses dieksekusi berdasarkan urutan kedatangan - yang datang duluan, jalan duluan.
    """
    # 1. Kunci Utama FCFS: Sort processes berdasarkan arrival time.
    processes.sort(key=lambda x: x.arrival_time)

    current_time = 0  # Waktu simulasi saat ini
    gantt_chart = []  # List untuk simpan data Gantt chart

    for process in processes:
        # 2. Tangani CPU Idle: Jika CPU selesai, tapi proses berikutnya belum tiba.
        if current_time < process.arrival_time:
            current_time = process.arrival_time  # Majukan waktu simulasi ke waktu kedatangan proses

        # 3. Eksekusi Proses: Non-preemptive, proses berjalan sampai selesai.
        process.start_time = current_time
        process.completion_time = process.start_time + process.burst_time
        
        # 4. Hitung Metrik: Rumus dasar CPU Scheduling
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time

        gantt_chart.append((process.pid, current_time, process.completion_time))
        current_time = process.completion_time  # Update current time

    return processes, gantt_chart


# --- Fungsi Bantuan ---
def calculate_average_waiting_time(processes):
    """ Menghitung Rata-rata Waktu Tunggu dari seluruh proses. """
    total_waiting_time = sum(p.waiting_time for p in processes)
    return total_waiting_time / len(processes)

def display_gantt_chart(gantt_chart):
    """
    Menampilkan Gantt chart dalam format teks sederhana (CLI).
    Ini menunjukkan urutan dan durasi eksekusi proses.
    """
    print("\nGantt Chart:")
    header = "|"
    for item in gantt_chart:
        pid, start, end = item
        header += f" P{pid} |"
    print(header)

    times = str(gantt_chart[0][1])
    for item in gantt_chart:
        pid, start, end = item
        # Menghitung padding agar angka waktu sejajar di bawah bar proses
        padding = (len(f" P{pid} ") - len(str(end)))
        times += " " * padding + str(end)
    print(times)


# --- SJF Scheduling (Non-Preemptive) ---
def sjf_scheduling(processes):
    """
    Implementasi algoritma Shortest Job First (SJF) Non-Preemptive.
    Prinsip: Di antara proses yang sudah tiba (available), pilih yang waktu burst-nya terpendek.
    """
    processes.sort(key=lambda x: x.arrival_time)  # Urutkan berdasarkan waktu kedatangan
    current_time = 0
    completed_processes = []
    gantt_chart = []
    n = len(processes)
    is_completed = [False] * n

    while len(completed_processes) < n:
        # 1. Identifikasi Proses yang Sudah Tersedia (Available Processes)
        available_processes = []
        for i in range(n):
            if processes[i].arrival_time <= current_time and not is_completed[i]:
                available_processes.append(processes[i])

        if not available_processes:
            # 2. CPU Idle: Tidak ada proses tersedia, majukan waktu
            current_time += 1
            continue

        # 3. Kunci Utama SJF: Pilih proses dengan waktu burst terpendek
        available_processes.sort(key=lambda x: x.burst_time)
        shortest_job = available_processes[0]

        # Temukan indeks proses yang dipilih di daftar proses asli
        shortest_job_index = -1
        for i in range(n):
            if processes[i].pid == shortest_job.pid and not is_completed[i]:
                shortest_job_index = i
                break

        process = processes[shortest_job_index]

        # 4. Eksekusi Proses: Non-preemptive, berjalan sampai selesai
        process.start_time = current_time
        process.completion_time = process.start_time + process.burst_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time

        gantt_chart.append((process.pid, current_time, process.completion_time))
        current_time = process.completion_time
        is_completed[shortest_job_index] = True
        completed_processes.append(process)

    completed_processes.sort(key=lambda x: x.pid) # Pastikan urutan output konsisten
    return completed_processes, gantt_chart


# --- Round Robin Scheduling (Preemptive) ---
def round_robin_scheduling(processes, time_quantum):
    """
    Fungsi Round Robin Scheduling: Implementasi dengan time quantum (Preemptive).
    Prinsip: Setiap proses mendapat jatah eksekusi (time_quantum) secara bergantian.
    """

    n = len(processes)
    # Gunakan copy() karena ini algoritma preemptive, butuh modifikasi remaining time
    processes_copy = [p.copy() for p in processes]

    # Inisialisasi awal untuk RR
    for p in processes_copy:
        p.remaining_burst_time = p.burst_time
        p.last_execution_end_time = p.arrival_time # Kapan terakhir kali keluar dari CPU/tiba
        p.has_started = False

    processes_copy.sort(key=lambda x: x.arrival_time) # Urutkan berdasarkan waktu kedatangan
    current_time = 0
    completed_processes = []
    gantt_chart = []
    ready_queue = []  # Antrian siap
    process_arrival_index = 0 # Indeks untuk melacak proses yang belum tiba

    

    while len(completed_processes) < n:
        # 1. Tambahkan Proses Tiba: Masukkan proses baru yang sudah tiba ke ready queue
        while process_arrival_index < n and processes_copy[process_arrival_index].arrival_time <= current_time:
            p = processes_copy[process_arrival_index]
            if p.remaining_burst_time > 0 and p not in ready_queue:
                ready_queue.append(p)
            process_arrival_index += 1

        if not ready_queue:  # CPU idle
            current_time += 1
            continue

        current_process = ready_queue.pop(0) # 2. Ambil Proses Pertama dari Queue (FIFO)

        # Set start_time hanya pada eksekusi pertama
        if not current_process.has_started:
            current_process.start_time = current_time
            current_process.has_started = True

        # 3. Hitung Waktu Eksekusi: Maksimal time_quantum atau sisa burst time
        execute_time = min(time_quantum, current_process.remaining_burst_time)

        # 4. Hitung Waktu Tunggu: Waktu tunggu = Waktu saat ini - Waktu terakhir selesai eksekusi/tiba
        if current_process.last_execution_end_time != -1:
            current_process.waiting_time += (current_time - current_process.last_execution_end_time)

        # Rekam segmen ini di Gantt chart
        gantt_chart.append((current_process.pid, current_time, current_time + execute_time))

        # 5. Update Waktu dan Sisa Burst
        current_process.remaining_burst_time -= execute_time
        current_time += execute_time
        current_process.last_execution_end_time = current_time # Update waktu akhir eksekusi

        # 6. Tambahkan Proses Baru yang Tiba Saat Eksekusi Berlangsung
        while process_arrival_index < n and processes_copy[process_arrival_index].arrival_time <= current_time:
            p = processes_copy[process_arrival_index]
            if p.remaining_burst_time > 0 and p not in ready_queue:
                ready_queue.append(p)
            process_arrival_index += 1

        if current_process.remaining_burst_time > 0: 
            # 7. Belum Selesai: Masukkan kembali ke ANTRIAN BELAKANG
            ready_queue.append(current_process)
        else: 
            # 8. Selesai: Hitung metrik akhir dan pindahkan ke completed
            current_process.completion_time = current_time
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
            completed_processes.append(current_process)

    completed_processes.sort(key=lambda x: x.pid)
    return completed_processes, gantt_chart


# --- Priority Scheduling (Non-Preemptive) ---
def priority_scheduling(processes):
    """
    Implementasi algoritma Priority Scheduling Non-Preemptive.
    Prinsip: Di antara proses yang sudah tiba, pilih yang memiliki prioritas tertinggi (angka prioritas terendah).
    """
    processes.sort(key=lambda x: x.arrival_time)
    current_time = 0
    completed_processes = []
    gantt_chart = []
    n = len(processes)
    is_completed = [False] * n

    while len(completed_processes) < n:
        # 1. Identifikasi Proses yang Sudah Tersedia
        available_processes = []
        for i in range(n):
            if processes[i].arrival_time <= current_time and not is_completed[i]:
                available_processes.append(processes[i])

        if not available_processes:
            # 2. CPU Idle
            current_time += 1
            continue

        # 3. Kunci Utama Priority: Pilih proses dengan prioritas tertinggi (angka terkecil)
        available_processes.sort(key=lambda x: x.priority)
        highest_priority_job = available_processes[0]

        # Temukan indeks proses yang dipilih di daftar proses asli
        highest_priority_job_index = -1
        for i in range(n):
            if processes[i].pid == highest_priority_job.pid and not is_completed[i]:
                highest_priority_job_index = i
                break

        process = processes[highest_priority_job_index]

        # 4. Eksekusi Proses: Non-preemptive, berjalan sampai selesai
        process.start_time = current_time
        process.completion_time = process.start_time + process.burst_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time

        gantt_chart.append((process.pid, current_time, process.completion_time))
        current_time = process.completion_time
        is_completed[highest_priority_job_index] = True
        completed_processes.append(process)

    completed_processes.sort(key=lambda x: x.pid)
    return completed_processes, gantt_chart

# --- Fungsi Utility (Setup dan Main Execution) ---

def get_default_processes():
    """ Membuat daftar proses default untuk demonstrasi. Data: (pid, arrival_time, burst_time, priority) """
    process_data = [
        (1, 0, 5, 2),
        (2, 1, 3, 1),
        (3, 2, 8, 3),
        (4, 3, 6, 4)
    ]
    return [Process(p[0], p[1], p[2], p[3]) for p in process_data]

def run_all_schedulers(processes):
    """ Menjalankan semua algoritma penjadwalan dan mengembalikan hasilnya dalam bentuk dictionary. """
    results = {}

    # FCFS: Menggunakan salinan proses
    processes_fcfs = [p.copy() for p in processes]
    scheduled_fcfs, gantt_fcfs = fcfs_scheduling(processes_fcfs)
    avg_waiting_fcfs = calculate_average_waiting_time(scheduled_fcfs)
    results['FCFS'] = {'processes': scheduled_fcfs, 'gantt_chart': gantt_fcfs, 'avg_waiting_time': avg_waiting_fcfs}

    # SJF: Menggunakan salinan proses
    processes_sjf = [p.copy() for p in processes]
    scheduled_sjf, gantt_sjf = sjf_scheduling(processes_sjf)
    avg_waiting_sjf = calculate_average_waiting_time(scheduled_sjf)
    results['SJF'] = {'processes': scheduled_sjf, 'gantt_chart': gantt_sjf, 'avg_waiting_time': avg_waiting_sjf}

    # Round Robin: Menggunakan salinan proses dan Time Quantum = 2
    time_quantum = 2
    processes_rr = [p.copy() for p in processes]
    scheduled_rr, gantt_rr = round_robin_scheduling(processes_rr, time_quantum)
    avg_waiting_rr = calculate_average_waiting_time(scheduled_rr)
    results['Round Robin'] = {'processes': scheduled_rr, 'gantt_chart': gantt_rr, 'avg_waiting_time': avg_waiting_rr, 'time_quantum': time_quantum}

    # Priority: Menggunakan salinan proses
    processes_priority = [p.copy() for p in processes]
    scheduled_priority, gantt_priority = priority_scheduling(processes_priority)
    avg_waiting_priority = calculate_average_waiting_time(scheduled_priority)
    results['Priority Scheduling'] = {'processes': scheduled_priority, 'gantt_chart': gantt_priority, 'avg_waiting_time': avg_waiting_priority}

    return results

def cli_main():
    """ Fungsi utama untuk menjalankan simulasi dan menampilkan hasil di Command Line Interface (CLI). """
    
    # Data Proses Contoh: (pid, arrival_time, burst_time, priority)
    process_data = [
        (1, 0, 5, 2),
        (2, 1, 3, 1),
        (3, 2, 8, 3),
        (4, 3, 6, 4)
    ]
    
    # --- FCFS Scheduling ---
    print("\n========================================")
    print("FCFS Scheduling (First-Come, First-Served)")
    print("========================================")
    processes_fcfs = [Process(p[0], p[1], p[2], p[3]) for p in process_data]
    scheduled_processes_fcfs, gantt_chart_fcfs = fcfs_scheduling(processes_fcfs)

    print(f"{'PID':<5}{'Arrival':<10}{'Burst':<10}{'Start':<10}{'Completion':<12}{'Turnaround':<12}{'Waiting':<10}")
    for p in scheduled_processes_fcfs:
        print(f"{p.pid:<5}{p.arrival_time:<10}{p.burst_time:<10}{p.start_time:<10}{p.completion_time:<12}{p.turnaround_time:<12}{p.waiting_time:<10}")

    display_gantt_chart(gantt_chart_fcfs)
    avg_waiting_time_fcfs = calculate_average_waiting_time(scheduled_processes_fcfs)
    print(f"\nAverage Waiting Time (FCFS): {avg_waiting_time_fcfs:.2f}")

    # --- SJF Scheduling ---
    print("\n========================================")
    print("SJF Scheduling (Shortest Job First)")
    print("========================================")
    processes_sjf = [Process(p[0], p[1], p[2], p[3]) for p in process_data]
    scheduled_processes_sjf, gantt_chart_sjf = sjf_scheduling(processes_sjf)

    print(f"{'PID':<5}{'Arrival':<10}{'Burst':<10}{'Start':<10}{'Completion':<12}{'Turnaround':<12}{'Waiting':<10}")
    for p in scheduled_processes_sjf:
        print(f"{p.pid:<5}{p.arrival_time:<10}{p.burst_time:<10}{p.start_time:<10}{p.completion_time:<12}{p.turnaround_time:<12}{p.waiting_time:<10}")

    display_gantt_chart(gantt_chart_sjf)
    avg_waiting_time_sjf = calculate_average_waiting_time(scheduled_processes_sjf)
    print(f"\nAverage Waiting Time (SJF): {avg_waiting_time_sjf:.2f}")

    # --- Round Robin Scheduling ---
    print("\n========================================")
    print("Round Robin Scheduling (Time-Sliced Preemptive)")
    print("========================================")
    time_quantum = 2
    processes_rr = [Process(p[0], p[1], p[2], p[3]) for p in process_data]
    scheduled_processes_rr, gantt_chart_rr = round_robin_scheduling(processes_rr, time_quantum)

    print(f"{'PID':<5}{'Arrival':<10}{'Burst':<10}{'Start':<10}{'Completion':<12}{'Turnaround':<12}{'Waiting':<10}")
    for p in scheduled_processes_rr:
        print(f"{p.pid:<5}{p.arrival_time:<10}{p.burst_time:<10}{p.start_time:<10}{p.completion_time:<12}{p.turnaround_time:<12}{p.waiting_time:<10}")
    
    display_gantt_chart(gantt_chart_rr)
    avg_waiting_time_rr = calculate_average_waiting_time(scheduled_processes_rr)
    print(f"\nAverage Waiting Time (Round Robin | Time Quantum = {time_quantum}): {avg_waiting_time_rr:.2f}")

    # --- Priority Scheduling ---
    print("\n========================================")
    print("Priority Scheduling (Non-Preemptive)")
    print("========================================")
    processes_priority = [Process(p[0], p[1], p[2], p[3]) for p in process_data]
    scheduled_processes_priority, gantt_chart_priority = priority_scheduling(processes_priority)

    print(f"{'PID':<5}{'Arrival':<10}{'Burst':<10}{'Priority':<10}{'Start':<10}{'Completion':<12}{'Turnaround':<12}{'Waiting':<10}")
    for p in scheduled_processes_priority:
        print(f"{p.pid:<5}{p.arrival_time:<10}{p.burst_time:<10}{p.priority:<10}{p.start_time:<10}{p.completion_time:<12}{p.turnaround_time:<12}{p.waiting_time:<10}")

    display_gantt_chart(gantt_chart_priority)
    avg_waiting_time_priority = calculate_average_waiting_time(scheduled_processes_priority)
    print(f"\nAverage Waiting Time (Priority): {avg_waiting_time_priority:.2f}")

if __name__ == "__main__":
    cli_main()