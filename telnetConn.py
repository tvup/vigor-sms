import os
import sys
import telnetlib
import time
import getpass
import ctypes
import socket

def notify(title, msg):
    # Windows popup
    if os.name == "nt":
        ctypes.windll.user32.MessageBoxW(0, msg, title, 1)
    else:
        # Linux/macOS: just print
        print(f"{title}: {msg}")

def shut_down_sockets(tn):
    tn.get_socket().shutdown(socket.SHUT_WR)
    data = tn.read_all().decode('ascii')
    tn.close()

def telnetConnection(host, username, password, number, inputText):


    print('Connection started... \nHost: %s\nUsername: %s\nPassword: %s\nMessage: %s\nText %s'%(host, username, password, number, inputText))
    HOST = host
    user = username
    password = password
    tn = telnetlib.Telnet(HOST)
    try:
        

        print("Connection Established...")

        tn.read_until(b"login: ", timeout = 5)
        tn.write(user.encode('ascii') + b"\n")
        if password:
            tn.read_until(b"Password: ", timeout = 5)
            tn.write(password.encode('ascii') + b"\n")

        notify("Aawwwyyyy yeah", "Login Successful.")
        #print("Login Successful.")
    except Exception as e:
        shut_down_sockets(tn)
        notify("Error", "Oh snap! %s happened"%(e.__class__,))
    try:
        send_msg = "wan lte send"
        notify("BBBAAAZZZINNNGGAAAA", "Sending Message....")
        #print("Sending Message...\n")
        command = f"{send_msg} {number} {inputText}"
        response = f"Send {inputText} to {number}"
        time.sleep(1) 
        #tn.write(command.encode('ascii')+b"\n")
        #tn.read_until(response.encode('ascii'), timeout = 5)
        notify("oooohhhh booooyyyy", "Message to %s sent.\n"%(number))
        tn.write(b"ls\n")
        tn.write(b"exit\n")
        notify("NANANANANA BATMAN", "Telnet connection closed")
        #print("Telnet connection closed\n")
    except Exception as e:
        shut_down_sockets(tn)
        notify("Error", "Oh snap! %s happened"%(e.__class__,));
    
    # tn.write(b"ls\n")
    # tn.write(b"exit\n")

    # print(tn.read_all().decode('ascii'))

