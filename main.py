import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque

st.set_page_config(page_title="CPU Scheduling Simulator", layout="centered")
st.title("CPU Scheduling Simulator")
algo = st.selectbox("Select Algorithm", ["FCFS", "SJF", "Round Robin", "Priority", "SRTF", "Priority Preemptive"])
n = st.number_input("Number of Processes", 1, 10, 4)

arrival, burst, priority = [], [], []

if algo == "Round Robin":
    quantum = st.number_input("Quantum Time", min_value=1, step=1)
else:
    quantum = None

st.subheader("Enter Process Details")

for i in range(n):
    cols = st.columns(3)
    arrival.append(cols[0].number_input(f"Arrival P{i}", key=f"a{i}", min_value=0))
    burst.append(cols[1].number_input(f"Burst P{i}", key=f"b{i}", min_value=1))
    if "Priority" in algo:
        priority.append(cols[2].number_input(f"Priority P{i}", key=f"p{i}", min_value=0))
    else:
        priority.append(0)

def run_scheduler():
    time, complete = 0, 0
    rem_bt = burst[:]
    done = [False] * n
    ct, tat, wt = [0]*n, [0]*n, [0]*n
    gantt = []
    queue = deque()
    visited = [False]*n
    prev = -1

    if algo == "FCFS":
        idx_order = sorted(range(n), key=lambda i: arrival[i])
        for i in idx_order:
            start = max(time, arrival[i])
            time = start + burst[i]
            ct[i] = time
            tat[i] = ct[i] - arrival[i]
            wt[i] = tat[i] - burst[i]
            gantt.append((i, start, time))

    elif algo == "SJF":
        while complete < n:
            idx = -1
            min_b = float('inf')
            for i in range(n):
                if not done[i] and arrival[i] <= time and burst[i] < min_b:
                    min_b = burst[i]
                    idx = i
            if idx != -1:
                start = time
                time += burst[idx]
                ct[idx] = time
                tat[idx] = ct[idx] - arrival[idx]
                wt[idx] = tat[idx] - burst[idx]
                gantt.append((idx, start, time))
                done[idx] = True
                complete += 1
            else:
                time += 1

    elif algo == "Round Robin":
        while complete < n:
            for i in range(n):
                if arrival[i] <= time and not visited[i]:
                    queue.append(i)
                    visited[i] = True
            if not queue:
                time += 1
                continue
            idx = queue.popleft()
            exec_time = min(quantum, rem_bt[idx])
            start = time
            time += exec_time
            rem_bt[idx] -= exec_time
            for i in range(n):
                if arrival[i] <= time and not visited[i]:
                    queue.append(i)
                    visited[i] = True
            if rem_bt[idx] == 0:
                ct[idx] = time
                tat[idx] = ct[idx] - arrival[idx]
                wt[idx] = tat[idx] - burst[idx]
                complete += 1
            else:
                queue.append(idx)
            gantt.append((idx, start, time))

    elif algo == "Priority":
        while complete < n:
            idx = -1
            high = float('inf')
            for i in range(n):
                if not done[i] and arrival[i] <= time and priority[i] < high:
                    high = priority[i]
                    idx = i
            if idx != -1:
                start = time
                time += burst[idx]
                ct[idx] = time
                tat[idx] = ct[idx] - arrival[idx]
                wt[idx] = tat[idx] - burst[idx]
                done[idx] = True
                complete += 1
                gantt.append((idx, start, time))
            else:
                time += 1

    elif algo == "SRTF":
        while complete < n:
            idx = -1
            min_rem = float('inf')
            for i in range(n):
                if arrival[i] <= time and rem_bt[i] > 0 and rem_bt[i] < min_rem:
                    min_rem = rem_bt[i]
                    idx = i
            if idx != -1:
                if prev != idx:
                    gantt.append((idx, time, time+1))
                else:
                    gantt[-1] = (idx, gantt[-1][1], time+1)
                rem_bt[idx] -= 1
                if rem_bt[idx] == 0:
                    ct[idx] = time + 1
                    tat[idx] = ct[idx] - arrival[idx]
                    wt[idx] = tat[idx] - burst[idx]
                    complete += 1
                prev = idx
                time += 1
            else:
                time += 1

    elif algo == "Priority Preemptive":
        while complete < n:
            idx = -1
            high = float('inf')
            for i in range(n):
                if arrival[i] <= time and rem_bt[i] > 0 and priority[i] < high:
                    high = priority[i]
                    idx = i
            if idx != -1:
                if prev != idx:
                    gantt.append((idx, time, time+1))
                else:
                    gantt[-1] = (idx, gantt[-1][1], time+1)
                rem_bt[idx] -= 1
                if rem_bt[idx] == 0:
                    ct[idx] = time + 1
                    tat[idx] = ct[idx] - arrival[idx]
                    wt[idx] = tat[idx] - burst[idx]
                    complete += 1
                prev = idx
                time += 1
            else:
                time += 1

    return ct, tat, wt, gantt

if st.button("Run Scheduler"):
    ct, tat, wt, gantt = run_scheduler()
    df = pd.DataFrame({
        "Process": [f"P{i}" for i in range(n)],
        "Arrival": arrival,
        "Burst": burst,
        "Priority": priority if "Priority" in algo else ["-"]*n,
        "Completion": ct,
        "TAT": tat,
        "WT": wt
    })
    st.subheader("Result Table")
    st.dataframe(df)

    st.success(f"Average TAT: {sum(tat)/n:.2f}")
    st.success(f"Average WT: {sum(wt)/n:.2f}")

    st.subheader("Gantt Chart")
    fig, ax = plt.subplots(figsize=(10, 2))
    for pid, start, end in gantt:
        ax.broken_barh([(start, end-start)], (10, 9), facecolors='tab:blue')
        ax.text((start+end)/2, 14, f"P{pid}", ha='center', va='center', color='white')
    ax.set_ylim(5, 25)
    ax.set_xlim(0, gantt[-1][2])
    ax.axis('off')
    st.pyplot(fig)
