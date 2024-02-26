import psutil
import subprocess
import time
import sys

def monitor_memory(pid):
    process = psutil.Process(pid)
    max_memory_used = 0
    while process.is_running() and process.status() != psutil.STATUS_ZOMBIE:
        memory_info = process.memory_info()
        max_memory_used = max(max_memory_used, memory_info.rss)
        time.sleep(0.01)
        process = psutil.Process(pid)
    byte = max_memory_used % 1000
    kb = max_memory_used // 1000 % 1000
    mb = max_memory_used // 1000000 % 1000
    gb = max_memory_used // 1000000000 % 1000
    print(f"Memory peak was {gb} GB {mb} MB {kb} KB {byte} bytes.")


def run_program(program_args):
    process = subprocess.Popen(program_args, start_new_session=True)
    monitor_memory(process.pid)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python memory_monitor.py <program> [args...]")
        sys.exit(1)

    program_args = sys.argv[1:]
    run_program(program_args)