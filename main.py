import threading
import time
import os, sys
from toolboxTMU import initTkinter

#init value
engineName = " Trafo X"
progStat = [True, True, True]

#main program
def mainloop(thread_name, interval):
    global progStat
    #main loop
    while True:
        for i in range(0, 3):
            if progStat[i] == True and i == 0:
                mainScreen.prog1Lbl['text'] = "Running"
                time.sleep(0.5)
            elif progStat[i] == False and i == 0:
                mainScreen.prog1Lbl["text"] = "Stop"
                time.sleep(0.5)
            elif progStat[i] == True and i == 1:
                mainScreen.prog2Lbl['text'] = "Running"
                time.sleep(0.5)
            elif progStat[i] == False and i == 1:
                mainScreen.prog2Lbl["text"] = "Stop"
                time.sleep(0.5)
            elif progStat[i] == True and i == 2:
                mainScreen.prog3Lbl['text'] = "Running"
                time.sleep(0.5)
            elif progStat[i] == False and i == 2:
                mainScreen.prog3Lbl["text"] = "Stop"
                time.sleep(0.5)

#restart program
def Restart(progSelect):
    os.execv(sys.executable, [sys.executable] + ['/main.py'])

#continue program
def Start(progSelect):
    global progStat
    progStat[progSelect - 1] = True

#pause program
def Stop(progSelect):
    global progStat
    progStat[progSelect - 1] = False

if __name__ == "__main__":
    #import tkinter, connect buttons with function
    mainScreen = initTkinter()
    mainScreen.restartBtn1["command"] = Restart(1)
    mainScreen.startBtn1["command"] = Start(1)
    mainScreen.stopBtn1["command"] = Stop(1)
    mainScreen.restartBtn2["command"] = Restart(2)
    mainScreen.startBtn2["command"] = Start(2)
    mainScreen.stopBtn2["command"] = Stop(2)
    mainScreen.restartBtn3["command"] = Restart(3)
    mainScreen.startBtn3["command"] = Start(3)
    mainScreen.stopBtn3["command"] = Stop(3)
    #threading to multi process between tkinter and main program
    thread1 = threading.Thread(target=mainloop, args=('thread1', 1))
    thread1.start()
    #start tkinter
    mainScreen.screen.mainloop()
