import subprocess
import time

def startProc():
    return subprocess.Popen(["python3", "data_handler.py"],
                            stdout = subprocess.PIPE)

proc = startProc()
with proc.stdout:
    for line in iter(proc.stdout.readline, b''):
        print(line)

"""
while True:
    print("begin")
    print(proc.poll())
    print("program running")
    with proc.stdout:
        for line in iter(proc.stdout.readline, b''):
            print(line)
    print(proc.poll())
    print("Start over")
    proc = startProc()
    """