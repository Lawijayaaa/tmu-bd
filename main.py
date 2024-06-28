import threading
import time
import os, sys
from toolboxTMU import initTkinter

#init value
engineName = " Trafo X"
progStat = True

#main program
def mainloop(thread_name, interval):
    global progStat
    #main loop
    while True:
        while progStat:
            mainScreen.prog1Lbl['text'] = "Running"
            time.sleep(0.5)
        else:
            mainScreen.prog1Lbl["text"] = "Stop"
            time.sleep(0.5)

#restart program
def Restart():
    os.execv(sys.executable, [sys.executable] + ['/main.py'])

#continue program
def Start():
    global progStat
    progStat = True

#pause program
def Stop():
    global progStat
    progStat = False

if __name__ == "__main__":
    #import tkinter, connect buttons with function
    mainScreen = initTkinter()
    mainScreen.restartBtn1["command"] = Restart
    mainScreen.startBtn1["command"] = Start
    mainScreen.stopBtn1["command"] = Stop
    #threading to multi process between tkinter and main program
    thread1 = threading.Thread(target=mainloop, args=('thread1', 1))
    thread1.start()
    #start tkinter
    mainScreen.screen.mainloop()
