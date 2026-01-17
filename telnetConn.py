import telnetlib
import socket
from typing import List

def shut_down_sockets(tn):
    try:
        tn.get_socket().shutdown(socket.SHUT_WR)
    except Exception:
        pass
    try:
        tn.close()
    except Exception:
        pass

def _detect_prompt(tn: telnetlib.Telnet, timeout: int = 5) -> bytes:
    """
    Read until we see something that looks like a prompt on the last line.
    We assume the prompt is the last line and typically ends with '>' or '#'.
    """
    buf = tn.read_until(b"\n", timeout=timeout)
    buf += tn.read_very_eager()

    for _ in range(10):
        data = buf + tn.read_very_eager()
        lines = data.splitlines()
        if lines:
            last = lines[-1].strip()
            if last.endswith(b">") or last.endswith(b"#"):
                return last
        buf += tn.read_until(b"\n", timeout=timeout)

    return b">"

def telnetConnection(host, username, password, commands, timeout=5):
    """
    Generic telnet connection: login + run one or more commands + return output as text.
    commands: list[str] or str
    """
    if isinstance(commands, str):
        commands = [commands]

    tn = None
    try:
        tn = telnetlib.Telnet(host)

        tn.read_until(b"login: ", timeout=timeout)
        tn.write(username.encode("ascii") + b"\n")

        if password:
            tn.read_until(b"Password: ", timeout=timeout)
            tn.write(password.encode("ascii") + b"\n")

        prompt = _detect_prompt(tn, timeout=timeout)

        out_parts: List[str] = []

        for cmd in commands:
            tn.write(cmd.encode("ascii") + b"\n")
            chunk = tn.read_until(prompt, timeout=timeout)
            out_parts.append(chunk.decode("ascii", errors="ignore"))

        tn.write(b"exit\n")
        out_parts.append(tn.read_all().decode("ascii", errors="ignore"))

        return "".join(out_parts)

    except Exception:
        if tn:
            shut_down_sockets(tn)
        raise

def send_sms(host: str, username: str, password: str, number: str, text: str) -> str:
    safe = text.replace('"', '\\"')
    cmd = f'wan lte send {number} "{safe}"'
    return telnetConnection(host, username, password, cmd)


def read_sms_all(host: str, username: str, password: str) -> str:
    return telnetConnection(host, username, password, "wan lte read all")

