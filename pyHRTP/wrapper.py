import socket
from threading import Thread

def echo(name:str, client_id:int, data:str)->list:
    """ Basic callback function that echos everything """
    return data

class HRTPServer(object):
    """ Server object """
    
    def __init__(self, ip="0.0.0.0", port=8088, callback=None):
        self.ip = ip
        self.port = port
        self.callback = callback
        self.running = True
        
        # start socket server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(1)
    
    def listen(self, conn, addr):
        message = []
        name = "Unknown"
        client_id = 0
        message_count = 0
        
        while True:
            data = conn.recv(1024)
            #skip on no data
            if not data: break
            
            # check if hello sent
            if data.decode().strip() != "Hello" and message_count == 0:
                conn.send(b"?\n")
                conn.close()
                break
            if data.decode().strip() == "End":
                conn.send(b"Goodbye\n")
                conn.close()
                break
            
            # If Over sent, parse message
            if data.decode().strip() == "Over":
                # Do handshake
                if name == "Unknown":
                    for line in message:
                        line = line.decode()
                        if line.split(" ")[0] == "Name:":
                            name = line.split(" ")[1]
                            conn.send(("Id: "+ str(client_id) + "\n").encode())
                            conn.send(b"Ready\nOver\n")
                            break
                    if name == "Unknown":
                        conn.send(b"Who?\n")
                        conn.send(b"Over\n")
                else:
                    # Send data to callback function
                    response = self.callback(name, client_id, message[:-1])
                    for line in response:
                        conn.send((line + "\n").encode())
                    conn.send(b"Over\n")
                    message = []
            message.append(data.strip())
            message_count += 1
        conn.close()
    
    def start(self, v=False):
        while self.running:
            conn, addr = self.socket.accept()
            if v:
                print(f"{addr[0]} connected")
            
            thread = Thread(target=self.listen, args=(conn, addr ))
            thread.start()
            