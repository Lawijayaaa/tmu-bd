import threading
import subprocess
import time
import datetime
import os
import sys
import logging
from toolboxTMU import initTkinter

ts = time.strftime("%Y%m%d")
logName = r'/home/pi/tmu-bd/assets/sysdata Test/syslog-' + ts + '.log'
logging.basicConfig(filename=logName, format='(asctime)s | %(levelname)s: %(message)s',level=logging.DEBUG)

os.chdir('/home/pi/tmu-bd/')

class App:
    def __init__(self):
        logging.debug("Initializing App")
        self.progStat = [True, True, False]
        self.stopFlag = [False, False, False]
        self.streamsHB = ["init", "init", "init"]
        self.streamsDebug = ["", ""]
        
        self.proc2 = self.start_proc("module_IO.py")
        time.sleep(1)
        self.proc1 = self.start_proc("data_handler.py")
        
        self.main_screen = initTkinter()
        self.main_screen.restartBtn["command"] = self.restart
        self.main_screen.stopBtn1["command"] = self.stop_proc1
        self.main_screen.stopBtn2["command"] = self.stop_proc2
        self.main_screen.stopBtn3["command"] = self.stop_proc3
        self.main_screen.stopBtn3["state"] = 'disabled'

        self.thread1 = threading.Thread(target=self.stream_proc, args=(self.proc1, 0))
        self.thread2 = threading.Thread(target=self.stream_proc, args=(self.proc2, 1))
        self.thread3 = threading.Thread(target=self.update_tk, args=(1,))
        self.thread4 = threading.Thread(target=self.watchdog, args=(20,))
        
        self.thread1.start()
        self.thread2.start()
        self.thread3.start()
        self.thread4.start()
        
        self.main_screen.screen.mainloop()

    def start_proc(self, script):
        logging.debug(f"Starting process: {script}")
        try:
            return subprocess.Popen(["python3", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            logging.error(f"Failed to start process {script}: {e}")
            return None

    def stream_proc(self, proc, index):
        if not proc:
            logging.error(f"Process {index} is None, skipping stream_proc")
            return
        try:
            with proc.stdout:
                for line in iter(proc.stdout.readline, b''):
                    code = line[0:1]
                    type = line[1:2]
                    message = line[3:].decode("utf-8").strip()
                    if code == b'1':
                        if type == b'T':
                            self.streamsHB[0] = message
                        elif type == b'D':
                            self.streamsDebug[0] = message
                    elif code == b'2':
                        if type == b'T':
                            self.streamsHB[1] = message
                        elif type == b'D':
                            self.streamsDebug[1] = message
                    else:
                        logging.error(f"Unexpected code: {code}")
        except Exception as e:
            logging.error(f"Error in stream_proc {index}: {e}")

    def update_tk(self, interval):
        try:
            while True:
                self.main_screen.lastHB1Lbl['text'] = self.streamsHB[0]
                self.main_screen.lastHB2Lbl['text'] = self.streamsHB[1]
                self.main_screen.lastHB3Lbl['text'] = self.streamsHB[2]

                self.main_screen.debug1Lbl['text'] = self.streamsDebug[0]
                self.main_screen.debug2Lbl['text'] = self.streamsDebug[1]
                
                self.main_screen.prog1Lbl['text'] = "Running" if self.progStat[0] else "Stop"
                self.main_screen.stopBtn1['state'] = 'normal' if self.progStat[0] else 'disabled'

                self.main_screen.prog2Lbl['text'] = "Running" if self.progStat[1] else "Stop"
                self.main_screen.stopBtn2['state'] = 'normal' if self.progStat[1] else 'disabled'

                self.main_screen.prog3Lbl['text'] = "Running" if self.progStat[2] else "Stop"
                self.main_screen.stopBtn3['state'] = 'normal' if self.progStat[2] else 'disabled'
                
                time.sleep(interval)
        except Exception as e:
            logging.error(f"Error in update_tk: {e}")
    
    def watchdog(self, interval):
        try:
            anchorDays = datetime.datetime.now().day
            lastLabel1 = self.main_screen.lastHB1Lbl['text']
            lastLabel2 = self.main_screen.lastHB2Lbl['text']
            while True:
                nowTime = datetime.datetime.now()
                time.sleep(interval)
                currentLabel1 = self.main_screen.lastHB1Lbl['text']
                currentLabel2 = self.main_screen.lastHB2Lbl['text']
                if lastLabel1 == currentLabel1 or lastLabel2 == currentLabel2 or anchorDays != nowTime.day:
                    if self.progStat[0] and self.progStat[1]:
                        self.restart()
                        logging.info(f"Restarting machine: {nowTime}")
                    else:
                        pass
                else:
                    lastLabel1 = currentLabel1
                    lastLabel2 = currentLabel2
        except Exception as e:
            logging.error(f"Error in watchdog: {e}")

    def restart(self):
        self.terminate_procs()
        time.sleep(2)
        os.execv(sys.executable, [sys.executable] + ['/home/pi/tmu-bd/main.py'])

    def stop_proc1(self):
        self.proc1.terminate()
        self.progStat[0] = False

    def stop_proc2(self):
        self.proc2.terminate()
        self.progStat[1] = False
    
    def stop_proc3(self):
        self.progStat[2] = False

    def terminate_procs(self):
        if self.proc1:
            self.proc1.terminate()
        if self.proc2:
            self.proc2.terminate()

if __name__ == "__main__":
    logging.debug("Starting App")
    app = App()
