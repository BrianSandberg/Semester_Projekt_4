import socket
from _thread import *
import pickle
from game import Game

# Every game is stored in the server, and not as individual clients

# LocalIP of the computer running the server
server = "192.168.0.42"
port = 5556

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# For safety and errorhandling, we try if the port is unused and can bind to the socket, together with the server
try:
    s.bind(("192.168.0.42", 5556))
except socket.error as e:
    print(str(e))

# sock.listen() "opens" up the port so that we can start connecting to it. The argument is the max number of connections
s.listen()
print("Waiting for a connection, Server Started")

connected = set() # Stores IP of clients in sets
games = {} # Dictionary that stores the games, ID is key and game object is value
idCount = 0 # Tracks current ID, so 2 games cant have same ID

def threaded_client(conn, p, gameId):
    #Global variable can be used inside and outside of function
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()
            ##Checks if the game still exists
            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    #reset the game, both players played - Is sent from client side
                    if data == "reset":
                        game.resetWent()
                    # If its not "get" its "move" -  The client sends the move to the server, which updates the game and sends it to client
                    elif data != "get":
                        game.play(p, data)
                    #Last move is "get" - sends the game to the client - Is sent every frame

                    reply = game
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2 # Creates a new game if there is an uneven number of players
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    # Start a new thread for each connection
    start_new_thread(threaded_client, (conn, p, gameId))