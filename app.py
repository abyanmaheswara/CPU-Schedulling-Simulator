from flask import Flask, render_template, request
from scheduler import Process, run_all_schedulers, get_default_processes

app = Flask(__name__)

def parse_form_data(form):
    processes = []
    pids = form.getlist('pid')
    arrivals = form.getlist('arrival_time')
    bursts = form.getlist('burst_time')
    priorities = form.getlist('priority')

    for i in range(len(pids)):
        try:
            pid = int(pids[i])
            arrival = int(arrivals[i])
            burst = int(bursts[i])
            priority = int(priorities[i])
            if burst > 0: # Ensure burst time is positive
                processes.append(Process(pid, arrival, burst, priority))
        except (ValueError, IndexError):
            # Skip invalid or incomplete entries
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
    app.run(debug=True)
