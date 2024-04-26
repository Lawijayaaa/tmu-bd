import threading
import os, sys
from tkInit import initTkinter
import subprocess

#init value
progStat = True

#main program
def mainloop(thread_name, interval):
    global progStat
    while True:
        while progStat:
            mainScreen.progStatLbl['text'] = "Running"
        else:
            mainScreen.progStatLbl["text"] = "Stop"

#restart program
def Restart():
    os.execv(sys.executable, [sys.executable] + ['/home/pi/tmu-bd/IoT_Trafo_Project.py'])

#continue program
def Start():
    global progStat
    progStat = True

#pause program
def Stop():
    global progStat
    progStat = False

if __name__ == "__main__":
    mainScreen = initTkinter()
    mainScreen.restartBtn["command"] = Restart
    mainScreen.startBtn["command"] = Start
    mainScreen.stopBtn["command"] = Stop
    #threading to multi process between tkinter and main program
    thread1 = threading.Thread(target=mainloop, args=('thread1', 1))
    thread1.start()
    #start tkinter
    mainScreen.screen.mainloop()