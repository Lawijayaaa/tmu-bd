import asyncio
import signal
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.server import StartAsyncTcpServer
from pymodbus.device import ModbusDeviceIdentification
import logging
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "client",
    passwd = "raspi",
    database= "iot_trafo_client")

def unsigned32bit(value):
    high_register = (value >> 16) & 0xFFFF
    low_register = value & 0xFFFF
    return high_register, low_register

def signed32bit(value):
    if value < 0:
        value = (1 << 32) + value
    high_register = (value >> 16) & 0xFFFF
    low_register = value & 0xFFFF
    return high_register, low_register

def dataStore(data):
    storage = [0]*99
    for i in range(0, 17):
        data[i] = round(data[i]*1000)
        storage[i*2 + 1], storage[i*2] = unsigned32bit(data[i])
    for i in range(17, 25):
        data[i] = round(data[i])
        storage[i*2 + 1], storage[i*2] = signed32bit(data[i])
    for i in range(25, 29):
        data[i] = round(data[i])
        storage[i*2 + 1], storage[i*2] = unsigned32bit(data[i])
    for i in range(29, 33):
        data[i] = round(data[i]*1000)
        storage[i*2 + 1], storage[i*2] = signed32bit(data[i])
    for i in range(33, 46):
        data[i] = round(data[i]*1000)
        storage[i*2 + 1], storage[i*2] = unsigned32bit(data[i])
    for i in range(46, len(data)):
        storage[i+46] = round(data[i]*100)
    return storage

def gatherValues():
    cursor = db.cursor()
    sql = "SELECT * FROM reading_data ORDER BY data_id DESC LIMIT 1"
    cursor.execute(sql)
    result = cursor.fetchall()
    listResult = list(result[0])
    listResult.pop(0)
    listResult.pop(0)
    db.commit()
    return dataStore(listResult)

# Handler untuk menampilkan log di tkinter
class LogDisplayHandler(logging.Handler):
    def __init__(self, text_widget, max_lines=10):
        super().__init__()
        self.text_widget = text_widget
        self.max_lines = max_lines

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.see(tk.END)  # Scroll otomatis ke baris terakhir

        # Batasi jumlah baris log agar tidak membebani memori
        num_lines = int(self.text_widget.index('end-1c').split('.')[0])
        if num_lines > self.max_lines:
            self.text_widget.delete('1.0', f'{num_lines - self.max_lines}.0')

# Fungsi untuk memulai tkinter dalam thread terpisah
def start_tkinter_loop():
    root = tk.Tk()
    root.title("Modbus Server Log")
    text_area = ScrolledText(root, wrap=tk.WORD, state='disabled', height=20, width=80)
    text_area.pack(padx=10, pady=10)
    text_area.configure(state='normal')

    log_handler = LogDisplayHandler(text_area)
    log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    log.addHandler(log_handler)
    log.setLevel(logging.DEBUG)

    root.mainloop()

# Jalankan tkinter di thread terpisah
threading.Thread(target=start_tkinter_loop, daemon=True).start()

# Konfigurasi logging
logging.basicConfig()
log = logging.getLogger()

# Membuat blok data dengan 20 parameter acak
values = [0 for _ in range(99)]
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, values),
    co=ModbusSequentialDataBlock(0, values),
    hr=ModbusSequentialDataBlock(0, values),
    ir=ModbusSequentialDataBlock(0, values)
)
context = ModbusServerContext(slaves=store, single=True)

# Fungsi untuk memperbarui nilai register setiap 2 detik
async def update_register_values():
    while True:
        new_values = gatherValues()
        store.setValues(3, 0, new_values)  # 3 = Holding Register
        #log.debug(f"register values updated: {new_values}")
        log.debug(f"register values updated")
        await asyncio.sleep(2)

# Identifikasi perangkat
identity = ModbusDeviceIdentification()
identity.VendorName = 'CustomModbusServer'
identity.ProductCode = 'PYSERVER'
identity.ModelName = 'Modbus TCP Server'
identity.MajorMinorRevision = '1.0'

# Fungsi untuk menangani sinyal sistem dan menutup server dengan benar
def handle_exit(*args):
    log.info("Shutting down server...")
    exit(0)

# Tangkap sinyal sistem
signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

# Fungsi untuk menjalankan server
async def run_server():
    # Jalankan fungsi pembaruan data dan server secara bersamaan
    await asyncio.gather(
        update_register_values(),
        StartAsyncTcpServer(context, identity=identity, address=("0.0.0.0", 1502), allow_reuse_address=True)
    )

# Menjalankan server
asyncio.run(run_server())