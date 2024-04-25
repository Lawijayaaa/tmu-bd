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
    
    lastTsLbl.place(x = 10, y = 30)
    trafoStatLbl.place(x = 10, y = 70)
    progStatLbl.place(x = 10, y = 110)
    firstDatLbl.place(x = 10, y = 150)
    secondDatLbl.place(x = 10, y = 190)
    thirdDatLbl.place(x = 10, y = 230)
    fourthDatLbl.place(x = 10, y = 270)
    DILbl.place(x = 10, y = 310)
    AILbl.place(x = 10, y = 350)
    debugLbl.place(x = 10, y = 390)
    restartBtn.place(x = 315, y = 440)
    startBtn.place(x = 215, y = 440)
    stopBtn.place(x = 115, y = 440)

    thread1 = threading.Thread(target=mainloop, args=('thread1', 1))
    thread1.start()
    screen.mainloop()