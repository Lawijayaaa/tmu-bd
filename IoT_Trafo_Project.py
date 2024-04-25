import threading
import time
import toolboxTMU
import tkinter as tk

screen = tk.Tk()
screen.title("TMU Gateway")
width= screen.winfo_screenwidth() 
height= screen.winfo_screenheight()
screen.geometry("%dx%d" % (width, height))
screen.attributes('-topmost', True)
screen.configure(background='#17C0EB')

def mainloop():
    while True:
        print(3)
        time.sleep(5)

if __name__ == "__main__":
    thread1 = threading.Thread(target=mainloop, args=('thread1', 1))
    thread1.start()
    screen.mainloop()