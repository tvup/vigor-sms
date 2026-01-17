import re
import tkinter as tk
from tkinter import messagebox

from telnetConn import send_sms, read_sms_all

fields = 'Host Address', 'UserName', 'Password', 'Message To', 'Text'

def makeform(root, fields):
    entries = []
    for field in fields:
        row = tk.Frame(root)
        lab = tk.Label(row, width=15, text=field, anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))
    return entries

def get_inputs(entries):
    return {field: ent.get() for field, ent in entries}


def append_output(output_box: tk.Text, text: str):
    output_box.insert(tk.END, text)
    output_box.see(tk.END)


def clear_output(output_box: tk.Text):
    output_box.delete("1.0", tk.END)
def parse_sms_read_all(raw: str):
    """
    Parses output from 'wan lte read all' as shown by DrayTek:
      Index: 3. Tag: NoRead. ...
      Sender: ...
      Content: ...

    Returns: list[dict] with index/id, tag, sender, received_time, content, and raw_block
    """

    raw = raw.strip()

    pattern = re.compile(
        r"(Index:\s*(\d+)\..*?)(?=(?:\nIndex:\s*\d+\.|\Z))",
        re.DOTALL,
    )

    messages = []
    for block, idx in pattern.findall(raw):
        tag_m = re.search(r"Tag:\s*(\w+)", block)
        sender_m = re.search(r"Sender:\s*(.*?),\s*received time:(.*)", block)
        content_m = re.search(r"Content:\s*(.*)", block)

        tag = tag_m.group(1) if tag_m else ""
        sender = sender_m.group(1).strip() if sender_m else ""
        rtime = sender_m.group(2).strip() if sender_m else ""
        content = content_m.group(1).strip() if content_m else ""

        messages.append(
            {
                "index": idx,
                "tag": tag,
                "sender": sender,
                "received_time": rtime,
                "content": content,
                "raw": block.strip(),
            }
        )

    return messages


def on_send(entries, output_box: tk.Text):
    vals = get_inputs(entries)
    host = vals["Host Address"]
    user = vals["UserName"]
    pwd = vals["Password"]
    to = vals["Message To"]
    text = vals["Text"]

    if not host or not user or not to or not text:
        messagebox.showerror("Missing fields", "Host, UserName, Message To and Text cannot be empty.")
        return

    clear_output(output_box)
    append_output(output_box, "Sending SMS...\n")
    try:
        raw = send_sms(host, user, pwd, to, text)
        append_output(output_box, "\n--- Router output ---\n")
        append_output(output_box, raw + "\n")
        messagebox.showinfo("Sent", f"SMS sent to {to}")
    except Exception as e:
        append_output(output_box, f"\nERROR: {e}\n")
        messagebox.showerror("Error", str(e))


def on_read_sms(entries, output_box: tk.Text, unread_only_var: tk.IntVar):
    vals = get_inputs(entries)
    host = vals["Host Address"].strip()
    user = vals["UserName"].strip()
    pwd = vals["Password"]

    if not host or not user:
        messagebox.showerror("Missing fields", "Host and UserName cannot be empty.")
        return

    clear_output(output_box)
    append_output(output_box, "Reading SMS (wan lte read all)...\n")

    try:
        raw = read_sms_all(host, user, pwd)
        msgs = parse_sms_read_all(raw)

        unread = [m for m in msgs if m["tag"].lower() == "noread"]
        read = [m for m in msgs if m["tag"].lower() != "noread"]

        unread_only = bool(unread_only_var.get())

        def render_list(title, items):
            append_output(output_box, f"\n--- {title} ({len(items)}) ---\n")
            if not items:
                append_output(output_box, "None.\n")
                return
            for m in items:
                append_output(output_box, "-" * 60 + "\n")
                append_output(output_box, f'Index: {m["index"]} | Tag: {m["tag"]}\n')
                append_output(output_box, f'From: {m["sender"]}\n')
                append_output(output_box, f'Time: {m["received_time"]}\n')
                append_output(output_box, f'{m["content"]}\n')

        if unread_only:
            render_list("Unread SMS", unread)
        else:
            render_list("Unread SMS", unread)
            render_list("Read SMS", read)

    except Exception as e:
        append_output(output_box, f"\nERROR: {e}\n")
        messagebox.showerror("Error", str(e))

def on_clear_output(output_box: tk.Text):
    clear_output(output_box)



if __name__ == '__main__':
    root = tk.Tk()
    ents = makeform(root, fields)
    controls = tk.Frame(root)
    controls.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    output = tk.Text(root, height=20, width=95)
    output.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

    btnSend = tk.Button(controls, text="Send", command=lambda: on_send(ents, output))
    btnSend.pack(side=tk.LEFT, padx=5)

    unread_only_var = tk.IntVar(value=1)
    chk = tk.Checkbutton(controls, text="Show unread only", variable=unread_only_var)
    chk.pack(side=tk.LEFT, padx=5)

    btnRead = tk.Button(
        controls,
        text="Read SMS",
        command=lambda: on_read_sms(ents, output, unread_only_var),
    )
    btnRead.pack(side=tk.LEFT, padx=5)

    btnClear = tk.Button(controls, text="Clear output", command=lambda: on_clear_output(output))
    btnClear.pack(side=tk.LEFT, padx=5)

    btnQuit = tk.Button(controls, text="Quit", command=root.quit)
    btnQuit.pack(side=tk.RIGHT, padx=5)

    root.bind("<Return>", lambda event: on_send(ents, output))

    root.mainloop()
