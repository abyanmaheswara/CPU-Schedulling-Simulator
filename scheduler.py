# Initial content for scheduler.py

class Process:

    def __init__(self, pid, arrival_time, burst_time, priority=0):

        self.pid = pid

        self.arrival_time = arrival_time

        self.burst_time = burst_time
        self.priority = priority # Assign priority here

        self.start_time = 0  # First time the process starts

        self.completion_time = 0

        self.turnaround_time = 0

        self.waiting_time = 0

        self.remaining_burst_time = burst_time

        self.last_execution_end_time = arrival_time 
        self.has_started = False

    def copy(self):
        return Process(self.pid, self.arrival_time, self.burst_time, self.priority)



def fcfs_scheduling(processes):

    # Sort processes by arrival time for FCFS

    processes.sort(key=lambda x: x.arrival_time)



    current_time = 0

    gantt_chart = []



    for process in processes:

        if current_time < process.arrival_time:

            current_time = process.arrival_time

        

        process.start_time = current_time

        process.completion_time = process.start_time + process.burst_time

        process.turnaround_time = process.completion_time - process.arrival_time

        process.waiting_time = process.turnaround_time - process.burst_time



        gantt_chart.append((process.pid, current_time, process.completion_time))

        current_time = process.completion_time

    

    return processes, gantt_chart



def calculate_average_waiting_time(processes):

    total_waiting_time = sum(p.waiting_time for p in processes)

    return total_waiting_time / len(processes)



def display_gantt_chart(gantt_chart):
    print("\nGantt Chart:")
    # Header
    header = "|"
    for item in gantt_chart:
        pid, start, end = item
        header += f" P{pid} |"
    print(header)

    # Times
    times = str(gantt_chart[0][1])  # Start time of the first process
    for item in gantt_chart:
        pid, start, end = item
        # Calculate spacing for time
        padding = (len(f" P{pid} ") - len(str(end)))
        times += " " * padding + str(end)
    print(times)











def sjf_scheduling(processes):

    processes.sort(key=lambda x: x.arrival_time) # Sort by arrival time initially

    

    current_time = 0

    completed_processes = []

    gantt_chart = []

    

    n = len(processes)

    is_completed = [False] * n

    

    while len(completed_processes) < n:

        available_processes = []

        for i in range(n):

            if processes[i].arrival_time <= current_time and not is_completed[i]:

                available_processes.append(processes[i])

        

        if not available_processes: # No processes available, advance time

            current_time += 1

            continue

            

        # Select process with shortest burst time among available

        available_processes.sort(key=lambda x: x.burst_time)

        shortest_job = available_processes[0]

        

        # Find index of the shortest job in the original processes list

        shortest_job_index = -1

        for i in range(n):

            if processes[i].pid == shortest_job.pid and not is_completed[i]:

                shortest_job_index = i

                break



        process = processes[shortest_job_index]

        

        process.start_time = current_time

        process.completion_time = process.start_time + process.burst_time

        process.turnaround_time = process.completion_time - process.arrival_time

        process.waiting_time = process.turnaround_time - process.burst_time



        gantt_chart.append((process.pid, current_time, process.completion_time))

        current_time = process.completion_time

        is_completed[shortest_job_index] = True

        completed_processes.append(process)



    # Sort completed processes by PID for consistent output

    completed_processes.sort(key=lambda x: x.pid)

    return completed_processes, gantt_chart



def round_robin_scheduling(processes, time_quantum):



    n = len(processes)



    # Create a deep copy of processes to avoid modifying original objects



    processes_copy = [p.copy() for p in processes]



    for p in processes_copy:



        p.remaining_burst_time = p.burst_time



        # last_execution_end_time tracks when a process last finished an execution burst



        # This helps in calculating waiting time correctly when it is picked up again.



        p.last_execution_end_time = p.arrival_time 



        p.has_started = False # Flag to track if the process has started its first execution







    # Sort by arrival time initially



    processes_copy.sort(key=lambda x: x.arrival_time)







    current_time = 0



    completed_processes = []



    gantt_chart = []



    ready_queue = []  # Stores process objects



    



    # To track processes that haven't arrived yet for initial addition to ready_queue



    process_arrival_index = 0 







    while len(completed_processes) < n:



        # Add newly arrived processes to the ready queue



        while process_arrival_index < n and processes_copy[process_arrival_index].arrival_time <= current_time:



            p = processes_copy[process_arrival_index]



            if p.remaining_burst_time > 0 and p not in ready_queue:



                ready_queue.append(p)



            process_arrival_index += 1



        



        if not ready_queue: # CPU is idle



            current_time += 1



            continue







        current_process = ready_queue.pop(0)



        



        # Set start_time only if it's the first time this process runs



        if not current_process.has_started:



            current_process.start_time = current_time



            current_process.has_started = True







        # Calculate actual time slice for this execution



        execute_time = min(time_quantum, current_process.remaining_burst_time)







        # Calculate waiting time for this segment



        # Waiting time is accumulated only when the process is in the ready queue



        # and current_time is greater than its last_execution_end_time (when it last finished execution or arrived).



        if current_process.last_execution_end_time != -1:



            current_process.waiting_time += (current_time - current_process.last_execution_end_time)







        # Record this segment in Gantt chart



        # Check if the last entry in gantt_chart is a continuation of the same process



        if gantt_chart and gantt_chart[-1][0] == current_process.pid and gantt_chart[-1][2] == current_time:



            # Extend the previous segment if it's a continuous execution



            gantt_chart[-1] = (current_process.pid, gantt_chart[-1][1], current_time + execute_time)



        else:



            gantt_chart.append((current_process.pid, current_time, current_time + execute_time))







        current_process.remaining_burst_time -= execute_time



        current_time += execute_time



        current_process.last_execution_end_time = current_time # Update when this burst finishes







        # Add newly arrived processes that arrived *during* the execution of current_process



        while process_arrival_index < n and processes_copy[process_arrival_index].arrival_time <= current_time:



            p = processes_copy[process_arrival_index]



            if p.remaining_burst_time > 0 and p not in ready_queue:



                ready_queue.append(p)



            process_arrival_index += 1







        if current_process.remaining_burst_time > 0: # Process not finished, add back to end of queue



            ready_queue.append(current_process)



        else: # Process finished



            current_process.completion_time = current_time



            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time



            completed_processes.append(current_process)



            



    # Sort completed processes by PID for consistent output



    completed_processes.sort(key=lambda x: x.pid)



    return completed_processes, gantt_chart



def priority_scheduling(processes):
    # Sort processes by arrival time initially
    processes.sort(key=lambda x: x.arrival_time)

    current_time = 0
    completed_processes = []
    gantt_chart = []

    n = len(processes)
    is_completed = [False] * n

    while len(completed_processes) < n:
        available_processes = []
        for i in range(n):
            if processes[i].arrival_time <= current_time and not is_completed[i]:
                available_processes.append(processes[i])
        
        if not available_processes: # No processes available, advance time
            current_time += 1
            continue
            
        # Select process with highest priority (lowest priority number) among available
        available_processes.sort(key=lambda x: x.priority)
        highest_priority_job = available_processes[0]
        
        # Find index of the highest priority job in the original processes list
        highest_priority_job_index = -1
        for i in range(n):
            if processes[i].pid == highest_priority_job.pid and not is_completed[i]:
                highest_priority_job_index = i
                break

        process = processes[highest_priority_job_index]
        
        process.start_time = current_time
        process.completion_time = process.start_time + process.burst_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time

        gantt_chart.append((process.pid, current_time, process.completion_time))
        current_time = process.completion_time
        is_completed[highest_priority_job_index] = True
        completed_processes.append(process)

    # Sort completed processes by PID for consistent output
    completed_processes.sort(key=lambda x: x.pid)
    return completed_processes, gantt_chart

def get_default_processes():
    process_data = [
        (1, 0, 5, 2),
        (2, 1, 3, 1),
        (3, 2, 8, 3),
        (4, 3, 6, 4)
    ]
    return [Process(p[0], p[1], p[2], p[3]) for p in process_data]

def run_all_schedulers(processes):
    results = {}

    # FCFS
    processes_fcfs = [p.copy() for p in processes]
    scheduled_fcfs, gantt_fcfs = fcfs_scheduling(processes_fcfs)
    avg_waiting_fcfs = calculate_average_waiting_time(scheduled_fcfs)
    results['FCFS'] = {
        'processes': scheduled_fcfs,
        'gantt_chart': gantt_fcfs,
        'avg_waiting_time': avg_waiting_fcfs
    }

    # SJF
    processes_sjf = [p.copy() for p in processes]
    scheduled_sjf, gantt_sjf = sjf_scheduling(processes_sjf)
    avg_waiting_sjf = calculate_average_waiting_time(scheduled_sjf)
    results['SJF'] = {
        'processes': scheduled_sjf,
        'gantt_chart': gantt_sjf,
        'avg_waiting_time': avg_waiting_sjf
    }

    # Round Robin
    time_quantum = 2
    processes_rr = [p.copy() for p in processes]
    scheduled_rr, gantt_rr = round_robin_scheduling(processes_rr, time_quantum)
    avg_waiting_rr = calculate_average_waiting_time(scheduled_rr)
    results['Round Robin'] = {
        'processes': scheduled_rr,
        'gantt_chart': gantt_rr,
        'avg_waiting_time': avg_waiting_rr,
        'time_quantum': time_quantum
    }

    # Priority
    processes_priority = [p.copy() for p in processes]
    scheduled_priority, gantt_priority = priority_scheduling(processes_priority)
    avg_waiting_priority = calculate_average_waiting_time(scheduled_priority)
    results['Priority Scheduling'] = {
        'processes': scheduled_priority,
        'gantt_chart': gantt_priority,
        'avg_waiting_time': avg_waiting_priority
    }
    
    return results

def cli_main():
    # Example processes: (pid, arrival_time, burst_time, priority)
    process_data = [
        (1, 0, 5, 2),
        (2, 1, 3, 1),
        (3, 2, 8, 3),
        (4, 3, 6, 4)
    ]
    
    # FCFS Scheduling
    print("\n========================================")
    print("FCFS Scheduling")
    print("========================================")
    processes_fcfs = [Process(p[0], p[1], p[2], p[3]) for p in process_data]
    scheduled_processes_fcfs, gantt_chart_fcfs = fcfs_scheduling(processes_fcfs)

    print(f"{'PID':<5}{'Arrival':<10}{'Burst':<10}{'Start':<10}{'Completion':<12}{'Turnaround':<12}{'Waiting':<10}")
    for p in scheduled_processes_fcfs:
        print(f"{p.pid:<5}{p.arrival_time:<10}{p.burst_time:<10}{p.start_time:<10}{p.completion_time:<12}{p.turnaround_time:<12}{p.waiting_time:<10}")

    display_gantt_chart(gantt_chart_fcfs)
    avg_waiting_time_fcfs = calculate_average_waiting_time(scheduled_processes_fcfs)
    print(f"\nAverage Waiting Time: {avg_waiting_time_fcfs:.2f}")

    # SJF Scheduling
    print("\n========================================")
    print("SJF Scheduling")
    print("========================================")
    processes_sjf = [Process(p[0], p[1], p[2], p[3]) for p in process_data] # Re-initialize processes for SJF
    scheduled_processes_sjf, gantt_chart_sjf = sjf_scheduling(processes_sjf)

    print(f"{'PID':<5}{'Arrival':<10}{'Burst':<10}{'Start':<10}{'Completion':<12}{'Turnaround':<12}{'Waiting':<10}")
    for p in scheduled_processes_sjf:
        print(f"{p.pid:<5}{p.arrival_time:<10}{p.burst_time:<10}{p.start_time:<10}{p.completion_time:<12}{p.turnaround_time:<12}{p.waiting_time:<10}")
    
    display_gantt_chart(gantt_chart_sjf)
    avg_waiting_time_sjf = calculate_average_waiting_time(scheduled_processes_sjf)
    print(f"\nAverage Waiting Time: {avg_waiting_time_sjf:.2f}")

    # Round Robin Scheduling
    print("\n========================================")
    print("Round Robin Scheduling")
    print("========================================")
    time_quantum = 2
    processes_rr = [Process(p[0], p[1], p[2], p[3]) for p in process_data] # Re-initialize processes for RR
    scheduled_processes_rr, gantt_chart_rr = round_robin_scheduling(processes_rr, time_quantum)

    print(f"{'PID':<5}{'Arrival':<10}{'Burst':<10}{'Start':<10}{'Completion':<12}{'Turnaround':<12}{'Waiting':<10}")
    for p in scheduled_processes_rr:
        print(f"{p.pid:<5}{p.arrival_time:<10}{p.burst_time:<10}{p.start_time:<10}{p.completion_time:<12}{p.turnaround_time:<12}{p.waiting_time:<10}")
    
    display_gantt_chart(gantt_chart_rr)
    avg_waiting_time_rr = calculate_average_waiting_time(scheduled_processes_rr)
    print(f"\nAverage Waiting Time (Time Quantum = {time_quantum}): {avg_waiting_time_rr:.2f}")

    # Priority Scheduling
    print("\n========================================")
    print("Priority Scheduling")
    print("========================================")
    processes_priority = [Process(p[0], p[1], p[2], p[3]) for p in process_data] # Re-initialize processes for Priority
    scheduled_processes_priority, gantt_chart_priority = priority_scheduling(processes_priority)

    print(f"{'PID':<5}{'Arrival':<10}{'Burst':<10}{'Priority':<10}{'Start':<10}{'Completion':<12}{'Turnaround':<12}{'Waiting':<10}")
    for p in scheduled_processes_priority:
        print(f"{p.pid:<5}{p.arrival_time:<10}{p.burst_time:<10}{p.priority:<10}{p.start_time:<10}{p.completion_time:<12}{p.turnaround_time:<12}{p.waiting_time:<10}")

    display_gantt_chart(gantt_chart_priority)
    avg_waiting_time_priority = calculate_average_waiting_time(scheduled_processes_priority)
    print(f"\nAverage Waiting Time: {avg_waiting_time_priority:.2f}")

if __name__ == "__main__":
    cli_main()