import threading
import subprocess
import time
import os
import sys
from toolboxTMU import initTkinter

class App:
    def __init__(self):
        self.progStat = [True, True, False]
        self.stopFlag = [False, False, False]
        self.streams = ["init", "init", "init"]
        
        self.proc1 = self.start_proc("/home/pi/tmu-bd/data_handler.py")
        self.proc2 = self.start_proc("/home/pi/tmu-bd/module_IO.py")
        
        self.main_screen = initTkinter()
        self.main_screen.restartBtn["command"] = self.restart
        self.main_screen.stopBtn1["command"] = self.stop_proc1
        self.main_screen.stopBtn2["command"] = self.stop_proc2
        self.main_screen.stopBtn3["command"] = self.stop_proc3
        self.main_screen.stopBtn3["state"] = 'disabled'

        self.thread1 = threading.Thread(target=self.stream_proc, args=(self.proc1, 1))
        self.thread2 = threading.Thread(target=self.stream_proc, args=(self.proc2, 1))
        self.thread3 = threading.Thread(target=self.update_tk, args=(1,))
        
        self.thread1.start()
        self.thread2.start()
        self.thread3.start()
        
        self.main_screen.screen.mainloop()

    def start_proc(self, script):
        return subprocess.Popen(["python3", script], stdout=subprocess.PIPE)

    def stream_proc(self, proc, index):
        with proc.stdout:
            for line in iter(proc.stdout.readline, b''):
                code = line[0:1]
                heartbeat = line[2:].decode("utf-8").strip()
                if code == b'1':
                    self.streams[0] = heartbeat
                elif code == b'2':
                    self.streams[1] = heartbeat
                else:
                    print("error: unexpected code", code)

    def update_tk(self, interval):
        while True:
            self.main_screen.lastHB1Lbl['text'] = self.streams[0]
            self.main_screen.lastHB2Lbl['text'] = self.streams[1]
            self.main_screen.lastHB3Lbl['text'] = self.streams[2]

            self.update_buttons()
            
            time.sleep(interval)

    def update_buttons(self):
        self.main_screen.prog1Lbl['text'] = "Running" if self.progStat[0] else "Stop"
        self.main_screen.stopBtn1['state'] = 'normal' if self.progStat[0] else 'disabled'

        self.main_screen.prog2Lbl['text'] = "Running" if self.progStat[1] else "Stop"
        self.main_screen.stopBtn2['state'] = 'normal' if self.progStat[1] else 'disabled'

        self.main_screen.prog3Lbl['text'] = "Running" if self.progStat[2] else "Stop"
        self.main_screen.stopBtn3['state'] = 'normal' if self.progStat[2] else 'disabled'

    def restart(self):
        if self.proc1:
            self.proc1.terminate()
        if self.proc2:
            self.proc2.terminate()
        time.sleep(1)
        os.execv(sys.executable, [sys.executable] + ['/home/pi/tmu-bd/main.py'])

    def stop_proc1(self):
        self.proc1.terminate()
        self.progStat[0] = False

    def stop_proc2(self):
        self.proc2.terminate()
        self.progStat[1] = False
    
    def stop_proc3(self):
        self.progStat[2] = False

if __name__ == "__main__":
    app = App()

