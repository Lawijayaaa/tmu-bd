import tkinter as tk
from threading import Timer, Lock
import json
import math

class parameter:
    def __init__(self, name, value, isWatched, highAlarm, lowAlarm, highTrip, lowTrip, status, trafoStat):
        self.name = name
        self.value = value
        self.isWatched = isWatched
        self.highAlarm = highAlarm
        self.lowAlarm = lowAlarm
        self.highTrip = highTrip
        self.lowTrip = lowTrip
        self.status = status
        self.trafoStat = trafoStat
        
    def toJson(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)

def initParameter(dataSet, inputData, trafoSetting, trafoData, tripSetting, dataLen):
    paramThreshold = [[None]*dataLen, [None]*dataLen, [None]*dataLen, [None]*dataLen]
    paramTrip = [None]*dataLen
    arrayString = ["Voltage UN", "Voltage VN", "Voltage WN", 
                    "Voltage UV", "Voltage VW", "Voltage UW",
                    "Current U", "Current V", "Current W", 
                    "Total Current", "Neutral Current",
                    "THDV U", "THDV V", "THDV W",
                    "THDI U", "THDI V", "THDI W",
                    "Active Power U", "Active Power V", 
                    "Active Power W", "Total Active Power",
                    "Reactive Power U", "Reactive Power V", 
                    "Reactive Power W", "Total Reactive Power",
                    "Apparent Power U", "Apparent Power V", 
                    "Apparent Power W", "Total Apparent Power",
                    "Power Factor U", "Power Factor V", "Power Factor W",
                    "Average Power Factor", "Frequency",
                    "Active Energy", "Reactive Energy",
                    "Busbar Temperature U", "Busbar Temperature V", 
                    "Busbar Temperature W", "Top Oil Temperature",
                    "Winding Temperature U", "Winding Temperature V", 
                    "Winding Temperature W", "Oil Level", "Tank Pressure",
                    "KRated U", "Derating U", 
                    "KRated V", "Derating V", 
                    "KRated W", "Derating W",
                    "H2 ppm", "Water Content ppm",
                    "Gap Voltage U-V", "Gap Voltage V-W", "Gap Voltage U-W",]
    iswatchBool = [False, False, False, True, True, True,
                    True, True, True, False, True, 
                    True, True, True, True, True, True,
                    False, False, False, False,
                    False, False, False, False,
                    False, False, False, False,
                    False, False, False, True, True, False, False,
                    True, True, True, True, True, True, True, True, True,
                    False, False, False, False, False, False, 
                    True, True, True, True, True]
        
    for i in range(0, 3):
        paramThreshold[0][i+3] = trafoSetting[2] #low trip Voltage
        paramThreshold[1][i+3] = trafoSetting[4] #low alarm Voltage
        paramThreshold[2][i+3] = trafoSetting[6] #high alarm Voltage
        paramThreshold[3][i+3] = trafoSetting[8] #high trip Voltage
        paramThreshold[2][i+53] = (trafoSetting[9] * trafoData[4])/(100 * math.sqrt(3)) #high alarm gap Voltage
        paramThreshold[3][i+53] = (trafoSetting[10] * trafoData[4])/(100 * math.sqrt(3)) #high trip gap Voltage
        paramThreshold[2][i+6] = (trafoSetting[21] * trafoData[6])/100 #high alarm Current Profile
        paramThreshold[3][i+6] = (trafoSetting[22] * trafoData[6])/100 #high trip Current Profile
        paramThreshold[2][i+40] = trafoSetting[17] #high alarm WTI Temp
        paramThreshold[3][i+40] = trafoSetting[18] #high trip WTI Temp
        paramThreshold[2][i+36] = trafoSetting[27] #high alarm Busbar Temp
        paramThreshold[3][i+36] = trafoSetting[28] #high trip Busbar Temp
        paramThreshold[2][i + 11] = trafoSetting[31] #high alarm THD Voltage Alarm
        paramThreshold[3][i + 11] = trafoSetting[32] #high trip THD Voltage Trip
        paramThreshold[2][i + 14] = trafoSetting[29] #high alarm THD Current Alarm
        paramThreshold[3][i + 14] = trafoSetting[30] #high trip THD Current Trip

        paramTrip[i+3] = tripSetting[1] #trip setting Voltage
        paramTrip[i+53] = tripSetting[2] #trip setting gap Voltage
        paramTrip[i+6] = tripSetting[7] #trip setting Current Profile
        paramTrip[i+40] = tripSetting[11] #trip setting WTI
        paramTrip[i+36] = tripSetting[5] #trip setting Busbar Temp
        paramTrip[i+11] = tripSetting[12] #trip setting THD Voltage
        paramTrip[i+14] = tripSetting[13] #trip setting THD Current

    paramThreshold[0][33] = trafoData[7] - ((trafoSetting[11] * trafoData[7])/100) #low trip Frequency
    paramThreshold[1][33] = trafoData[7] - ((trafoSetting[12] * trafoData[7])/100) #low alarm Frequency
    paramThreshold[2][33] = trafoData[7] + ((trafoSetting[14] * trafoData[7])/100) #high alarm Frequency
    paramThreshold[3][33] = trafoData[7] + ((trafoSetting[13] * trafoData[7])/100) #high trip Frequency
    paramThreshold[2][39] = trafoSetting[15] #high alarm Top Oil Temp
    paramThreshold[3][39] = trafoSetting[16] #high trip Top Oil Temp
    paramThreshold[1][32] = trafoSetting[19] #low alarm PF
    paramThreshold[0][32] = trafoSetting[20] #low trip PF
    paramThreshold[2][44] = trafoSetting[25] #high alarm Pressure Tank
    paramThreshold[3][44] = trafoSetting[26] #high trip Pressure Tank
    paramThreshold[2][10] = trafoSetting[33] #high alarm Neutral Current
    paramThreshold[3][10] = trafoSetting[34] #high trip Neutral Current
    paramThreshold[1][43] = 3 #low alarm Oil Level
    paramThreshold[0][43] = 2 #low trip Oil Level
    paramThreshold[2][51] = trafoSetting[35] #high alarm H2 ppm
    paramThreshold[3][51] = trafoSetting[36] #high trip H2 ppm
    paramThreshold[2][52] = trafoSetting[37] #high alarm Water Content ppm
    paramThreshold[3][52] = trafoSetting[38] #high trip Water Content ppm

    paramTrip[33] = tripSetting[3] #trip setting Frequency
    paramTrip[39] = tripSetting[4] #trip setting Oil Temp
    paramTrip[32] = tripSetting[6] #trip setting PF
    paramTrip[44] = tripSetting[9] #trip setting Tank Pressure
    paramTrip[10] = tripSetting[14] #trip setting Neutral Current
    paramTrip[43] = tripSetting[10] #trip setting Oil Level
    paramTrip[51] = tripSetting[15] #trip setting H2 ppm
    paramTrip[52] = tripSetting[16] #trip setting Water Content ppm

    for i in range(0, dataLen):            
        dataSet[i].name = arrayString[i]
        dataSet[i].value = inputData[i]
        dataSet[i].isWatched = iswatchBool[i]
        if dataSet[i].isWatched:
            dataSet[i].highAlarm = paramThreshold[2][i]
            dataSet[i].lowAlarm = paramThreshold[1][i]
            dataSet[i].highTrip = paramThreshold[3][i]
            dataSet[i].lowTrip = paramThreshold[0][i]
            if dataSet[i].highAlarm and dataSet[i].lowAlarm:
                if dataSet[i].value <= dataSet[i].lowTrip:
                    dataSet[i].status = 1
                    if paramTrip[i] == 0:
                        dataSet[i].trafoStat = 1
                    elif paramTrip[i] == 1:
                        dataSet[i].trafoStat = 2
                    elif paramTrip[i] == 2:
                        dataSet[i].trafoStat = 3
                elif dataSet[i].value > dataSet[i].lowTrip and dataSet[i].value <= dataSet[i].lowAlarm:
                    dataSet[i].status = 2
                    dataSet[i].trafoStat = 1
                elif dataSet[i].value > dataSet[i].lowAlarm and dataSet[i].value < dataSet[i].highAlarm:
                    dataSet[i].status = 3
                    dataSet[i].trafoStat = 0
                elif dataSet[i].value >= dataSet[i].highAlarm and dataSet[i].value < dataSet[i].highTrip:
                    dataSet[i].status = 4
                    dataSet[i].trafoStat = 1
                elif dataSet[i].value >= dataSet[i].highTrip:
                    dataSet[i].status = 5
                    if paramTrip[i] == 0:
                        dataSet[i].trafoStat = 1
                    elif paramTrip[i] == 1:
                        dataSet[i].trafoStat = 2
                    elif paramTrip[i] == 2:
                        dataSet[i].trafoStat = 3
            elif dataSet[i].highAlarm:
                if dataSet[i].value < dataSet[i].highAlarm:
                    dataSet[i].status = 3
                    dataSet[i].trafoStat = 0
                elif dataSet[i].value >= dataSet[i].highAlarm and dataSet[i].value < dataSet[i].highTrip:
                    dataSet[i].status = 4
                    dataSet[i].trafoStat = 1
                elif dataSet[i].value >= dataSet[i].highTrip:
                    dataSet[i].status = 5
                    if paramTrip[i] == 0:
                        dataSet[i].trafoStat = 1
                    elif paramTrip[i] == 1:
                        dataSet[i].trafoStat = 2
                    elif paramTrip[i] == 2:
                        dataSet[i].trafoStat = 3
            elif dataSet[i].lowAlarm:
                if dataSet[i].value <= dataSet[i].lowTrip:
                    dataSet[i].status = 1
                    if paramTrip[i] == 0:
                        dataSet[i].trafoStat = 1
                    elif paramTrip[i] == 1:
                        dataSet[i].trafoStat = 2
                    elif paramTrip[i] == 2:
                        dataSet[i].trafoStat = 3
                elif dataSet[i].value > dataSet[i].lowTrip and dataSet[i].value <= dataSet[i].lowAlarm:
                    dataSet[i].status = 2
                    dataSet[i].trafoStat = 1
                elif dataSet[i].value > dataSet[i].lowAlarm:
                    dataSet[i].status = 3
                    dataSet[i].trafoStat = 0
    return(dataSet)

def dataParser(getTemp, getElect1, getElect2, getElect3, getH2, getMoist, dataLen, CTratio, PTratio):
    outputData = [0]*dataLen
    #parse getTemp
    try:
        outputData[38:41] = [(0 if member > 2400 else member/10) for member in getTemp.registers] #Busbar Temp
    except:
        pass
    #parse getElect1
    try:
        for i in range(0, 3):
            outputData[i] = (PTratio * getElect1.registers[i])/100 #Voltage Phase Neutral
            outputData[i + 3] = (PTratio * getElect1.registers[i+3])/100 #Voltage Phase Phase
            outputData[i + 6] = (CTratio * getElect1.registers[i+6])/1000 #Current
            outputData[i + 29] = (signedInt16Handler(getElect1.registers[i+21]))/1000 #PF
            outputData[i + 17] = (CTratio * PTratio * signedInt16Handler(getElect1.registers[i+15]))/10 #P
            outputData[i + 21] = (CTratio * PTratio * signedInt16Handler(getElect1.registers[i+18]))/10 #Q
        outputData[10] = (CTratio * getElect1.registers[9])/1000 #Neutral Current
        outputData[20] = ((CTratio * PTratio * signedInt32Handler(getElect1.registers[10:12]))[0])/10 #Psig
        outputData[24] = ((CTratio * PTratio * signedInt32Handler(getElect1.registers[12:14]))[0])/10 #Qsig
        outputData[33] = (getElect1.registers[24])/1000 #Frequency 
        outputData[34] = (unsignedInt32Handler(getElect1.registers[25:27]))/10 #kWh
        outputData[35] = (unsignedInt32Handler(getElect1.registers[27:]))/10 #kVARh
        outputData[32] = (outputData[29] + outputData[30] + outputData[31])/3 #Average PF
        outputData[9] = outputData[6] + outputData[7] + outputData[8] #Total Current
        outputData[53] = abs(outputData[0] - outputData[1]) #Gap Voltage Un-Vn
        outputData[54] = abs(outputData[1] - outputData[2]) #Gap Voltage Vn-Wn
        outputData[55] = abs(outputData[0] - outputData[2]) #Gap Voltage Un-Wn
    except:
        pass
    #parse getElect2
    try:
        for i in range(25, 28):
            outputData[i] = CTratio * PTratio * ((getElect2.registers[i])/10) #S
        outputData[28] = CTratio * PTratio * ((unsignedInt32Handler(getElect2.registers[3:]))/10) #Ssig
    except:
        pass
    #parse getElect3
    try:
        for i in range(11, 14):
            outputData[i] = (getElect3.registers[i])/10 #THD Voltage
            outputData[i + 3] = (getElect3.registers[i+3])/10 #THD Current
    except:
        pass
    #parse getH2 and getMoist
    try:
        outputData[51] = getH2.registers #H2 ppm
        outputData[52] = getMoist.registers #Water Content ppm
    except:
        pass

def signedInt16Handler(data):
    if data > (math.pow(2, 16))/2:
        data = data - math.pow(2, 16)
    else:
        data = data
    return data

def signedInt32Handler(dataset):
    hexData = [hex(member)[2:] for member in dataset]
    idata = [0]*int(len(dataset)/2)
    for i in range(0, len(hexData)): 
        while len(hexData[i]) < 4: hexData[i] = "0" + hexData[i]
    for i in range(0, int(len(hexData)/2)):
        tempData = int((hexData[i*2+1] + hexData[i*2]),16)
        if tempData > (math.pow(2, 32))/2:
            idata[i] = tempData - math.pow(2, 32)
        else:
            idata[i] = tempData
    return idata

def unsignedInt32Handler(dataset):
    hexData = [hex(member)[2:] for member in dataset]
    for i in range(0, len(hexData)): 
        while len(hexData[i]) < 4: hexData[i] = "0" + hexData[i]
    tempData = int((hexData[1] + hexData[0]),16)
    return tempData

class TimerEx(object):
    """
    A reusable thread safe timer implementation
    """

    def __init__(self, interval_sec, function, *args, **kwargs):
        """
        Create a timer object which can be restarted

        :param interval_sec: The timer interval in seconds
        :param function: The user function timer should call once elapsed
        :param args: The user function arguments array (optional)
        :param kwargs: The user function named arguments (optional)
        """
        self._interval_sec = interval_sec
        self._function = function
        self._args = args
        self._kwargs = kwargs
        # Locking is needed since the '_timer' object might be replaced in a different thread
        self._timer_lock = Lock()
        self._timer = None

    def start(self, restart_if_alive=True):
        """
        Starts the timer and returns this object [e.g. my_timer = TimerEx(10, my_func).start()]

        :param restart_if_alive: 'True' to start a new timer if current one is still alive
        :return: This timer object (i.e. self)
        """
        with self._timer_lock:
            # Current timer still running
            if self._timer is not None:
                if not restart_if_alive:
                    # Keep the current timer
                    return self
                # Cancel the current timer
                self._timer.cancel()
            # Create new timer
            self._timer = Timer(self._interval_sec, self.__internal_call)
            self._timer.start()
        # Return this object to allow single line timer start
        return self

    def cancel(self):
        """
        Cancels the current timer if alive
        """
        with self._timer_lock:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None

    def is_alive(self):
        """
        :return: True if current timer is alive (i.e not elapsed yet)
        """
        with self._timer_lock:
            if self._timer is not None:
                return self._timer.is_alive()
        return False

    def __internal_call(self):
        # Release timer object
        with self._timer_lock:
            self._timer = None
        # Call the user defined function
        self._function(*self._args, **self._kwargs)

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