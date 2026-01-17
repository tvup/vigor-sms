import json
import os
import tkinter as tk
from telnetConn import telnetConnection


fields = 'Host Address', 'UserName', 'Password', 'Message To', 'Text'
SETTINGS_FILE = "settings.json"

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {}
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_settings(data: dict):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def fetch(entries):
    input_list = []
    data_to_save = {}

    for field, ent in entries:
        value = ent.get()
        input_list.append(value)

        data_to_save[field] = value

    save_settings(data_to_save)
    telnetConnection(input_list[0],input_list[1],input_list[2],input_list[3],input_list[4])
    


def makeform(root, fields):
    entries = []
    settings = load_settings()
    for field in fields:
        row = tk.Frame(root)
        lab = tk.Label(row, width=15, text=field, anchor='w')
        if field == "Password":
            ent = tk.Entry(row, show="*")
        else:
            ent = tk.Entry(row)

        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)

        if field in settings:
            ent.insert(0, settings[field])

        entries.append((field, ent))
    return entries





if __name__ == '__main__':
    root = tk.Tk()
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))   

    btnSend = tk.Button(root, text='Send',
                  command=(lambda e=ents: fetch(e)))                  
    btnSend.pack(side=tk.LEFT, padx=5, pady=5)

    btnQuit = tk.Button(root, text='Quit', command=root.quit)
    btnQuit.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()