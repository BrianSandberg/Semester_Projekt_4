import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.42"
        self.port = 5556
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            #Send object data - use pickle.loads
            return pickle.loads(self.client.recv(4096))
        #Should handle a socket.error, but need to handle this for now
        except socket.error as e:
            print(e)
        else:
            self.client.send(int.encode(data))
            return pickle.loads(self.client.recv(4096))

