import threading
import time
import toolboxTMU
import tkinter as tk

def mainloop(thread_name, interval):
    while True:
        print(3)
        time.sleep(5)

def Restart():
    print("restart")

def Start():
    print("Start")

def Stop():
    print("Stop")

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
            font = ("Helvetica",9)
            )
    trafoStatLbl = tk.Label(
            screen,
            font = ("Helvetica",9)
            )
    progStatLbl = tk.Label(
            screen,
            font = ("Helvetica",9)
            )
    firstDatLbl = tk.Label(
            screen,
            font = ("Helvetica",9)
            )
    secondDatLbl = tk.Label(
            screen,
            font = ("Helvetica",9)
            )
    thirdDatLbl = tk.Label(
            screen,
            font = ("Helvetica",9)
            )
    fourthDatLbl = tk.Label(
            screen,
            font = ("Helvetica",9)
            )
    DILbl = tk.Label(
            screen,
            font = ("Helvetica",9)
            )
    AILbl = tk.Label(
            screen,
            font = ("Helvetica",9)
            )
    debugLbl = tk.Label(
            screen,
            font = ("Helvetica",9)
            )
    
    lastTsLbl.place(x = 10, y = 50)
    trafoStatLbl.place(x = 10, y = 90)
    progStatLbl.place(x = 10, y = 130)
    firstDatLbl.place(x = 10, y = 170)
    secondDatLbl.place(x = 10, y = 210)
    thirdDatLbl.place(x = 10, y = 250)
    fourthDatLbl.place(x = 10, y = 290)
    DILbl.place(x = 10, y = 330)
    AILbl.place(x = 10, y = 370)
    debugLbl.place(x = 10, y = 410)
    restartBtn.place(x = 915, y = 625)
    startBtn.place(x = 815, y = 625)
    stopBtn.place(x = 715, y = 625)

    thread1 = threading.Thread(target=mainloop, args=('thread1', 1))
    thread1.start()
    screen.mainloop()