import socket
import sys
import time
from pathlib import Path
from math import ceil


def print_bar(proc):
    toolbar_width = 20
    if proc >= 10:
        sys.stdout.write("\b" * (toolbar_width +4 + len(str(proc))))  
    sys.stdout.write(f"{proc}%[{' ' * toolbar_width}]")
    sys.stdout.write("\b" * (toolbar_width -2 + len(str(proc)))) 
    sys.stdout.write("##" * (proc // 10))
    sys.stdout.flush()

try:
    filename, ip, port = sys.argv[1], sys.argv[2], int(sys.argv[3])
except Exception as err:
    print("Usage: ./client.py filenema ip port")
    sys.exit()

try:
    file = Path(f'./{filename}')
    size = file.stat().st_size
    f = open (filename, "rb")
except Exception:
    print("No such file")
    sys.exit()

try:
    s = socket.socket()
    s.connect((ip,port))
except Exception:
    print("Can't connect")
    sys.exit()


if __name__ == '__main__':
    # send filename
    filename += '\n'
    s.send(bytes(filename, encoding='utf-8'))
    time.sleep(1)

    # send data
    data = f.read(1024)
    completness = 0
    sended_size = 0
    while (data):
        s.send(data)
        sended_size += 1024

        # update progress bar
        if size // 100 * completness <= sended_size:
            print_bar(completness)
            completness += 10
        data = f.read(1024)
        
    s.close()
    f.close()
