import sys
sys.path.insert(0, "libs")

import serial
import serial.tools.list_ports
import threading
import tkinter as tk
from tkinter import ttk
import time
import math

def find_esp32_port():
    ports = serial.tools.list_ports.comports()
    print("🔍 Dostępne porty:")
    for port in ports:
        print(f"  {port.device} -> {port.description} [{port.hwid}]")

    for port in ports:
        if "USB" in port.device or "CP210" in port.description or "CH340" in port.description or "FTDI" in port.description:
            print(f"✅ Wybrano port: {port.device}")
            return port.device

    return None

PORT = find_esp32_port()
if PORT is None:
    print("❌ Nie znaleziono ESP32. Podłącz płytkę i spróbuj ponownie.")
    sys.exit(1)

BAUDRATE = 115200
SCAN_INTERVAL = 3

ser = serial.Serial(PORT, BAUDRATE, timeout=1)
time.sleep(2)

networks = {}

def estimate_distance(rssi, tx_power=-40, n=2.0):
    try:
        rssi = int(rssi)
        distance = 10 ** ((tx_power - rssi) / (10 * n))
        return f"{distance:.1f} m"
    except:
        return "?"

def signal_icon(rssi):
    try:
        rssi = int(rssi)
        if rssi >= -50:
            return "▂▄▆█"
        elif rssi >= -60:
            return "▂▄▆"
        elif rssi >= -70:
            return "▂▄"
        elif rssi >= -80:
            return "▂"
        else:
            return "."
    except:
        return "?"

def read_serial():
    global networks
    while True:
        try:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8', errors='ignore').rstrip()
                if line and " : " in line and "No networks" not in line:
                    parts = line.split(" : ")
                    if len(parts) == 4:
                        ssid, rssi, channel, enc = parts
                        dist = estimate_distance(rssi)
                        icon = signal_icon(rssi)
                        networks[ssid] = {
                            "values": (ssid, rssi, channel, enc, dist, icon),
                            "ttl": 4
                        }
        except Exception as e:
            print("Błąd serial:", e)
        time.sleep(0.1)

def refresh_table():
    global networks
    for ssid in list(networks.keys()):
        networks[ssid]["ttl"] -= 1
        if networks[ssid]["ttl"] <= 0:
            for child in tree.get_children():
                if tree.item(child, 'values')[0] == ssid:
                    tree.delete(child)
            del networks[ssid]
        else:
            values = networks[ssid]["values"]
            found = False
            for child in tree.get_children():
                if tree.item(child, 'values')[0] == ssid:
                    tree.item(child, values=values)
                    found = True
            if not found:
                tree.insert('', 'end', values=values)

    root.after(SCAN_INTERVAL * 1000, refresh_table)

def treeview_sort_column(tv, col, reverse):
    data_list = [(tv.set(k, col), k) for k in tv.get_children('')]
    try:
        data_list.sort(key=lambda t: float(t[0].split()[0]), reverse=reverse)
    except:
        data_list.sort(reverse=reverse)
    for index, (val, k) in enumerate(data_list):
        tv.move(k, '', index)
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

root = tk.Tk()
root.title("ESP32 WiFi Scanner")

columns = ('SSID', 'RSSI', 'Channel', 'Encryption', 'Distance', 'Signal')
tree = ttk.Treeview(root, columns=columns, show='headings', height=20)

for col in columns:
    tree.heading(col, text=col, command=lambda c=col: treeview_sort_column(tree, c, False))
    tree.column(col, width=120 if col not in ('SSID', 'Signal') else 200)

tree.pack(padx=10, pady=10, fill="both", expand=True)

thread = threading.Thread(target=read_serial, daemon=True)
thread.start()

refresh_table()

root.mainloop()
