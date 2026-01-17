# vigor-sms

A simple desktop GUI for interacting with **DrayTek Vigor routers** that support SMS over LTE.

The application uses **Telnet** to communicate with the router and provides a small Tkinter-based interface for sending and reading SMS messages.

---

## Features

- Send SMS via LTE (`wan lte send`)
- Read SMS inbox from the router (`wan lte read all`)
- Distinguish between **unread** and **read** SMS using router-provided tags
- Automatically detects the Telnet prompt
- Simple desktop UI built with Tkinter
- Saves connection settings locally (`settings.json`)
- Clear output window for command responses

---

## Screens / UI

The UI consists of:

- Connection fields:
  - Host Address
  - UserName
  - Password
  - Message To
  - Text
- Buttons:
  - **Send** – send an SMS
  - **Read SMS** – read inbox (unread only or all)
  - **Clear output**
  - **Quit**
- Checkbox:
  - **Show unread only**

---

## How it works

- The router is accessed via **Telnet**
- After login, the application **auto-detects the prompt** by reading the last line ending in `>` or `#`
- SMS sending is done using:
```

wan lte send <number> "<text>"

```
(text is quoted to avoid `Too many inputs` errors)
- SMS reading is done using:
```

wan lte read all

````
- Messages are parsed from the router output and classified using:
- `Tag: NoRead`
- `Tag: Read`

No local “read/unread” state is stored — the router is treated as the source of truth.

---

## Files

### `telnetConn.py`
Handles all Telnet communication:
- Login
- Prompt detection
- Command execution
- Helper functions:
- `send_sms(...)`
- `read_sms_all(...)`

### `vigor-sms.py`
The Tkinter GUI application:
- Form handling
- Settings persistence (`settings.json`)
- SMS parsing and display
- User interaction

### `settings.json`
Created automatically.
Stores the last used values for all input fields (including host and username).

---

## Requirements

- Python **3.9+**
- A DrayTek Vigor router with:
- LTE modem
- SMS functionality enabled
- Telnet access enabled

No external Python dependencies are required.

---

## Usage

```bash
python vigor-sms.py
````

1. Enter router connection details
2. Enter recipient number and message text
3. Click **Send** to send an SMS
   **or**
4. Click **Read SMS** to fetch messages from the router

---

## Notes & Limitations

* The Telnet prompt is assumed to end with `>` or `#`
* Only routers supporting `wan lte send` and `wan lte read all` are supported
* Marking messages as read explicitly or deleting messages is not implemented
* The UI is intentionally minimal and functional

---

## Possible Future Improvements

* Explicit “mark as read” or “delete SMS” actions (if supported by firmware)
* Message filtering/search
* CLI version (headless mode)
* Web-based UI
* Better validation and input hints

---

## Disclaimer

This tool is provided as-is.
Use at your own risk when interacting with network equipment.

