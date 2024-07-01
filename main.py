import threading
import time
import os, sys
from toolboxTMU import initTkinter

#init value
engineName = " Trafo X"
progStat = [True, True, False]

#main program
def mainloop(thread_name, interval):
    global progStat
    #main loop
    while True:
        if progStat[0]:
            mainScreen.prog1Lbl['text'] = "Running"
        else:
            mainScreen.prog1Lbl["text"] = "Stop"
        if progStat[1]:
            mainScreen.prog2Lbl['text'] = "Running"
        else:
            mainScreen.prog2Lbl["text"] = "Stop"
        if progStat[2]:
            mainScreen.prog3Lbl['text'] = "Running"
        else:
            mainScreen.prog3Lbl["text"] = "Stop"
        time.sleep(0.5)

def Restart1():
    os.execv(sys.executable, [sys.executable] + ['/home/pi/tmu-bd/main.py'])

def Restart2():
    os.execv(sys.executable, [sys.executable] + ['/home/pi/tmu-bd/main.py'])

def Restart3():
    os.execv(sys.executable, [sys.executable] + ['/home/pi/tmu-bd/main.py'])

def Start1():
    global progStat
    progStat[0] = True

def Start2():
    global progStat
    progStat[1] = True
    
def Start3():
    global progStat
    progStat[2] = True
    progStat[2] = False

def Stop1():
    global progStat
    progStat[0] = False

def Stop2():
    global progStat
    progStat[1] = False
    
def Stop3():
    global progStat
    progStat[2] = False

if __name__ == "__main__":
    #import tkinter, connect buttons with function
    mainScreen = initTkinter()
    mainScreen.restartBtn1["command"] = Restart1
    mainScreen.startBtn1["command"] = Start1
    mainScreen.stopBtn1["command"] = Stop1
    
    mainScreen.restartBtn2["command"] = Restart2
    mainScreen.startBtn2["command"] = Start2
    mainScreen.stopBtn2["command"] = Stop2
    
    mainScreen.restartBtn3["command"] = Restart3
    mainScreen.startBtn3["command"] = Start3
    mainScreen.stopBtn3["command"] = Stop3
    #threading to multi process between tkinter and main program
    thread1 = threading.Thread(target=mainloop, args=('thread1', 1))
    thread1.start()
    #start tkinter
    mainScreen.screen.mainloop()
