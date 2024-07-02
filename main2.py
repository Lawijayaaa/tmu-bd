import threading, subprocess, time
import os, sys, datetime
from toolboxTMU import initTkinter

#init value
engineName = " Trafo X"
progStat = [True, True, False]
startFlag = [False, False, False]
stopFlag = [False, False, False]
stream1 = "init"
stream2 = "init"
stream3 = "init"

def startProc1():
    return subprocess.Popen(["python3", "data_handler.py"],
                            stdout = subprocess.PIPE)

def startProc2():
    return subprocess.Popen(["python3", "module_IO.py"],
                            stdout = subprocess.PIPE)

def streamProc(proc, interval):
    global stream1, stream2
    with proc.stdout:
        for line in iter(proc.stdout.readline, b''):
            code = line[0:1]
            heartbeat = line[2:].decode("utf-8")
            if code == b'2' :
                stream2 = heartbeat
            elif code == b'1':
                stream1 = heartbeat
            else :
                print("error")
                
#main program
def updateTk(proc1, proc2, interval):
    global progStat, stopFlag
    #main loop
    while True:
        if stopFlag[0]:
            proc1.terminate()
            stopFlag[0] = False
        if stopFlag[1]:
            proc2.terminate()
            stopFlag[1] = False
        
        mainScreen.lastHB1Lbl['text'] = stream1
        mainScreen.lastHB2Lbl['text'] = stream2
        mainScreen.lastHB3Lbl['text'] = stream3
        if progStat[0]:
            mainScreen.prog1Lbl['text'] = "Running"
            mainScreen.stopBtn1['state'] = 'normal'
        else:
            mainScreen.prog1Lbl["text"] = "Stop"
            mainScreen.stopBtn1['state'] = 'disabled'
            
        if progStat[1]:
            mainScreen.prog2Lbl['text'] = "Running"
            mainScreen.stopBtn2['state'] = 'normal'
        else:
            mainScreen.prog2Lbl["text"] = "Stop"
            mainScreen.stopBtn2['state'] = 'disabled'
            
        if progStat[2]:
            mainScreen.prog3Lbl['text'] = "Running"
            mainScreen.stopBtn3['state'] = 'normal'
        else:
            mainScreen.prog3Lbl["text"] = "Stop"
            # mainScreen.startBtn3['state'] = 'normal'
            # mainScreen.stopBtn3['state'] = 'disabled'
        time.sleep(0.5)
    
def Restart():
    proc1.terminate()
    proc2.terminate()
    time.sleep(1)
    os.execv(sys.executable, [sys.executable] + ['/home/pi/tmu-bd/main2.py'])

def Stop1():
    global progStat, stopFlag
    proc1.terminate()
    stopFlag[0] = True
    progStat[0] = False

def Stop2():
    global progStat, stopFlag
    stopFlag[1] = True
    progStat[1] = False
    
def Stop3():
    global progStat, stopFlag
    stopFlag[2] = True
    progStat[2] = False

if __name__ == "__main__":
    #import tkinter, connect buttons with function
    mainScreen = initTkinter()
    mainScreen.restartBtn["command"] = Restart
    mainScreen.stopBtn1["command"] = Stop1
    mainScreen.stopBtn2["command"] = Stop2
    mainScreen.stopBtn3["command"] = Stop3
    mainScreen.stopBtn3["state"] = 'disabled'
    #threading to multi process between tkinter and main program
    proc1 = startProc1()
    #proc2 = startProc2()
    #thread1 = threading.Thread(target = streamProc, args=(proc1, 1))
    #thread1.start()
    #thread2 = threading.Thread(target = streamProc, args=(proc2, 1))
    #thread2.start()
    #thread3 = threading.Thread(target = updateTk, args=(proc1, proc2, 1))
    #thread3.start()
    #start tkinter
    #mainScreen.screen.mainloop()
