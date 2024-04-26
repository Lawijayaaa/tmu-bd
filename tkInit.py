import tkinter as tk

def initTkinter():
    class MyScreen:
        screen = tk.Tk()
        screen.title("TMU Gateway")
        width= screen.winfo_screenwidth() 
        height= screen.winfo_screenheight()
        screen.geometry("%dx%d" % (width, height))
        screen.attributes('-topmost', True)
        screen.configure(background='#17C0EB')

        restartBtn = tk.Button(
            screen,
            text = "Restart")
        startBtn = tk.Button(
            screen,
            text = "Start")
        stopBtn = tk.Button(
            screen,
            text = "Stop")
        
        progStatTxt = tk.Label(
                screen,
                font = ("Helvetica",12),
                text = "Program Status"
                )
        progStatLbl = tk.Label(
                screen,
                font = ("Helvetica",12)
                )
        lastTsTxt = tk.Label(
                screen,
                font = ("Helvetica",12),
                text = "Last Timestamp"
                )
        lastTsLbl = tk.Label(
                screen,
                font = ("Helvetica",12)
                )
        trafoStatTxt = tk.Label(
                screen,
                font = ("Helvetica",12),
                text = "Trafo Status"
                )
        trafoStatLbl = tk.Label(
                screen,
                font = ("Helvetica",12)
                )        
        firstDatTxt = tk.Label(
                screen,
                font = ("Helvetica",12),
                text = "First Data Sequence"
                )
        firstDatLbl = tk.Label(
                screen,
                font = ("Helvetica",12)
                )        
        secondDatTxt = tk.Label(
                screen,
                font = ("Helvetica",12),
                text = "Second Data Sequence"
                )
        secondDatLbl = tk.Label(
                screen,
                font = ("Helvetica",12)
                )
        thirdDatTxt = tk.Label(
                screen,
                font = ("Helvetica",12),
                text = "Third Data Sequence"
                )
        thirdDatLbl = tk.Label(
                screen,
                font = ("Helvetica",12)
                )
        fourthDatTxt = tk.Label(
                screen,
                font = ("Helvetica",12),
                text = "Fourth Data Sequence"
                )
        fourthDatLbl = tk.Label(
                screen,
                font = ("Helvetica",12)
                )
        DITxt = tk.Label(
                screen,
                font = ("Helvetica",12),
                text = "DI status"
                )
        DILbl = tk.Label(
                screen,
                font = ("Helvetica",12)
                )
        AITxt = tk.Label(
                screen,
                font = ("Helvetica",12),
                text = "AI status"
                )
        AILbl = tk.Label(
                screen,
                font = ("Helvetica",12)
                )
        debug1Txt = tk.Label(
                screen,
                font = ("Helvetica",12),
                text = "Debug message 1"
                )
        debug1Lbl = tk.Label(
                screen,
                font = ("Helvetica",12)
                )
        debug2Txt = tk.Label(
                screen,
                font = ("Helvetica",12),
                text = "Debug message 2"
                )
        debug2Lbl = tk.Label(
                screen,
                font = ("Helvetica",12)
                )
    mainScreen = MyScreen()
    mainScreen.progStatTxt.place(x = 10, y = 50)
    mainScreen.lastTsTxt.place(x = 10, y = 100)
    mainScreen.trafoStatTxt.place(x = 10, y = 150)
    mainScreen.firstDatTxt.place(x = 10, y = 200)
    mainScreen.secondDatTxt.place(x = 10, y = 250)
    mainScreen.thirdDatTxt.place(x = 10, y = 300)
    mainScreen.fourthDatTxt.place(x = 10, y = 350)
    mainScreen.DITxt.place(x = 10, y = 400)
    mainScreen.AITxt.place(x = 10, y = 450)
    mainScreen.debug1Txt.place(x = 10, y = 500)
    mainScreen.debug2Txt.place(x = 10, y = 550)

    mainScreen.progStatLbl.place(x = 225, y = 50)
    mainScreen.lastTsLbl.place(x = 225, y = 100)
    mainScreen.trafoStatLbl.place(x = 225, y = 150)
    mainScreen.firstDatLbl.place(x = 225, y = 200)
    mainScreen.secondDatLbl.place(x = 225, y = 250)
    mainScreen.thirdDatLbl.place(x = 225, y = 300)
    mainScreen.fourthDatLbl.place(x = 225, y = 350)
    mainScreen.DILbl.place(x = 225, y = 400)
    mainScreen.AILbl.place(x = 225, y = 450)
    mainScreen.debug1Lbl.place(x = 225, y = 500)
    mainScreen.debug2Lbl.place(x = 225, y = 550)

    mainScreen.restartBtn.place(x = 915, y = 630)
    mainScreen.startBtn.place(x = 815, y = 630)
    mainScreen.stopBtn.place(x = 715, y = 630)
    return mainScreen