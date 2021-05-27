import socket
import pickle

#Class network is responsible for connecting to the server.
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Local ip of computer running the server
        self.server = "192.168.0.42"
        self.port = 5556
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            #Returns player number of the client
            #see line 31 in server.py
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            #Send string data - Receive object data
            # use pickle.loads to unpickle object
            return pickle.loads(self.client.recv(4096))
        except socket.error as e:
            print(e)
