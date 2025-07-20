# cpu_scheduling-# cpu_scheduling-# CPU Scheduling Simulator

This is a Streamlit-based web application that demonstrates various CPU scheduling algorithms by simulating process execution and visualizing the timeline with a Gantt chart.

---

## Supported Algorithms

- First-Come-First-Serve (FCFS)
- Shortest Job First (SJF)
- Round Robin (RR)
- Priority Scheduling (non-preemptive)
- Shortest Remaining Time First (SRTF)
- Priority Preemptive Scheduling

---

## Features

- Input process details: arrival time, burst time, and priority (when applicable).
- Specify quantum time for Round Robin scheduling.
- Calculates completion time, turnaround time (TAT), and waiting time (WT) for each process.
- Displays average turnaround and waiting times.
- Visualizes process execution with a Gantt chart.

---

## How to Run

1. Install dependencies using:

pip install streamlit pandas matplotlib

2. Launch the app with:
streamlit run main.py


3. Follow on-screen instructions to select algorithm, enter process data, and run the scheduler.

---

## Usage Notes

- Arrival time must be zero or positive.
- Burst time must be at least 1.
- Lower priority numbers indicate higher priority.
- Quantum time for Round Robin should be at least 1.

---

## License

This project is free for personal and educational use.

---

