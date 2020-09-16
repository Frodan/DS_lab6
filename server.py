import socket
from threading import Thread
import os

clients = []


# Thread to listen one particular client
class ClientListener(Thread):
    def __init__(self, name: str, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock
        self.name = name


    def _close(self):
        clients.remove(self.sock)
        self.sock.close()
        print(self.name + ' disconnected')

    def run(self):
        data = self.sock.recv(1024)
        print(f"File: {data}")
        filename, extension = str(data, encoding='utf-8').strip().split('.')

        # Check if file with such name already exists
        if f"{filename}.{extension}" in os.listdir():
            i_copy = 1
            while f"{filename}_copy{i_copy}.{extension}" in os.listdir():
                i_copy += 1
            name = f"{filename}_copy{i_copy}.{extension}"
        else:
            name = f"{filename}.{extension}"

        # Write file
        f = open(name, 'wb')
        data = 1
        while data:
            data = self.sock.recv(1024)
            f.write(data)
        f.close()      
        self._close()
        return


def main():
    next_name = 1

    #Creating listening socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 8800))
    sock.listen()
    
    while True:

        #Waiting for clients
        con, addr = sock.accept()
        clients.append(con)

        #Log the name
        name = 'u' + str(next_name)
        next_name += 1
        print(str(addr) + ' connected as ' + name)
        # start new thread to deal with client
        ClientListener(name, con).run()


if __name__ == "__main__":
    main()
