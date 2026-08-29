import psutil
import os
import time


def clear_screen():
    os.system("clear")


def show_processes():
    clear_screen()

    print("=" * 70)
    print("              GRAND LINE GUARDIAN")
    print("=" * 70)

    print(f"{'PID':<10} {'PROCESS NAME':<30} {'CPU %':<10} {'MEMORY %'}")
    print("-" * 70)

    processes = []

    for process in psutil.process_iter(
        ['pid', 'name', 'cpu_percent', 'memory_percent']
    ):
        try:
            info = process.info
            processes.append(info)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    for process in processes[:20]:
        pid = process['pid']
        name = process['name']
        cpu = process['cpu_percent']
        memory = process['memory_percent']

        print(f"{pid:<10} {name[:28]:<30} {cpu:<10.1f} {memory:.2f}")

    print("-" * 70)
    print(f"Total Active Processes: {len(processes)}")
    print("Press Ctrl+C to exit.")


while True:
    show_processes()
    time.sleep(1)
