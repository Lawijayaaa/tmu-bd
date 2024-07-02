import subprocess
import time
import threading

def startProc1():
    return subprocess.Popen(["python3", "data_handler.py"],
                            stdout = subprocess.PIPE)
def startProc2():
    return subprocess.Popen(["python3", "module_IO.py"],
                            stdout = subprocess.PIPE)

def streamProc(proc, interval):
    with proc.stdout:
        for line in iter(proc.stdout.readline, b''):
            code = line[0:1]
            heartbeat = line[2:].decode("utf-8")
            if code == b'2' :
                print("moduleIO")
                print(heartbeat)
            elif code == b'1':
                print("dataHandler")
                print(heartbeat)
            else :
                print("error")
                print(code)
        
def main():
    proc1 = startProc1()
    proc2 = startProc2()
    
    thread1 = threading.Thread(target = streamProc, args=(proc1, 1))
    thread1.start()
    thread2 = threading.Thread(target = streamProc, args=(proc2, 1))
    thread2.start()
    
main()