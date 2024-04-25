import threading
import time
import os
import toolboxTMU
import tkinter as tk

progStat = True

def mainloop(thread_name, interval):
    global progStat
    while True:
        while progStat:
            progStatLbl['text'] = "Running"
        else:
            progStatLbl["text"] = "Stop"

def Restart():
    os.execv(sys.executable, [sys.executable] + ['/tmu-bd/IoT_Trafo_Project.py'])

def Start():
    global progStat
    progStat = True

def Stop():
    global progStat
    progStat = False

if __name__ == "__main__":
    screen = tk.Tk()
    screen.title("TMU Gateway")
    width= screen.winfo_screenwidth() 
    height= screen.winfo_screenheight()
    screen.geometry("%dx%d" % (width, height))
    screen.attributes('-topmost', True)
    screen.configure(background='#17C0EB')

    restartBtn = tk.Button(
        screen,
        text = "Restart",
        command = Restart)
    startBtn = tk.Button(
        screen,
        text = "Start",
        command = Start)
    stopBtn = tk.Button(
        screen,
        text = "Stop",
        command = Stop)
    lastTsLbl = tk.Label(
            screen,
            font = ("Helvetica",12)
            )
    trafoStatLbl = tk.Label(
            screen,
            font = ("Helvetica",12)
            )
    progStatLbl = tk.Label(
            screen,
            font = ("Helvetica",12)
            )
    firstDatLbl = tk.Label(
            screen,
            font = ("Helvetica",12)
            )
    secondDatLbl = tk.Label(
            screen,
            font = ("Helvetica",12)
            )
    thirdDatLbl = tk.Label(
            screen,
            font = ("Helvetica",12)
            )
    fourthDatLbl = tk.Label(
            screen,
            font = ("Helvetica",12)
            )
    DILbl = tk.Label(
            screen,
            font = ("Helvetica",12)
            )
    AILbl = tk.Label(
            screen,
            font = ("Helvetica",12)
            )
    debugLbl = tk.Label(
            screen,
            font = ("Helvetica",12)
            )
    
    lastTsLbl.place(x = 10, y = 50)
    trafoStatLbl.place(x = 10, y = 100)
    progStatLbl.place(x = 10, y = 150)
    firstDatLbl.place(x = 10, y = 200)
    secondDatLbl.place(x = 10, y = 250)
    thirdDatLbl.place(x = 10, y = 300)
    fourthDatLbl.place(x = 10, y = 350)
    DILbl.place(x = 10, y = 400)
    AILbl.place(x = 10, y = 450)
    debugLbl.place(x = 10, y = 500)
    restartBtn.place(x = 915, y = 630)
    startBtn.place(x = 815, y = 630)
    stopBtn.place(x = 715, y = 630)

    thread1 = threading.Thread(target=mainloop, args=('thread1', 1))
    thread1.start()
    screen.mainloop()