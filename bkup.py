import os
import datetime
import shutil

def createBkup(filePath):
    bkupDir = '/home/pi/tmu-bd/assets/rawdata Test/backup/'
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    bkupPath = os.path.join(bkupDir, f'datalogger-backup-{timestamp}.xlsx')
    shutil.copy2(filePath, bkupPath)
    
createBkup('/home/pi/tmu-bd/assets/rawdata Test/datalogger-20240703 Trafo X .xlsx')
#os.remove('/home/pi/tmu-bd/assets/rawdata Test/backup/datalogger-backup-20240703.xlsx')