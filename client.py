import socket, sys, threading, tkinter
from tkinter import font
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.connect((sys.argv[1], int(sys.argv[2]))) # IP, PORT
except:
    server.connect((input("Enter IP: "), int(input("Enter Port: "))))
players = []
display_players = [["bob", 1]]
try:
    with open("leaderboard.txt", "r") as f:
        players = f.readline().strip()
except FileNotFoundError:
    pass

def handle():
    global server, players, players_var
    while True:
        try:
            name, score = server.recv(1024).decode("ascii").split("|")
            players.append([name, score])
            update_display()
            server.send("Added player".encode("ascii"))
        except Exception as e:
            server.send(str(e).encode("ascii"))

def update_display():
    global display_players, players, players_var
    with open("leaderboard.txt", "w") as f:
        f.write(str(players))
    display_players.clear()
    temp = sorted(players,key=lambda x: (x[1]))
    temp.reverse()
    print("temp:", temp)
    for ind, player in enumerate(temp):
        print(100-len(player[0]))
        temp_str = str(ind+1) + "." + " "*(8-len(str(ind+1))) + player[0] + " "*(50-(len(player[0])*1)) + player[1]
        display_players.append(temp_str)
    players_var.set(display_players)
    print(display_players)

handle_thread = threading.Thread(target=handle)
handle_thread.daemon = True
handle_thread.start()

root = tkinter.Tk()
root.title("Robotics Challenge Leaderboard")
root.attributes('-fullscreen', True)
root.config(bg="#ffffff")

fnt = font.Font(family="Courier", size=30)

players_var = tkinter.StringVar(value=display_players)
tkinter.Label(root, text="Robotics Challenge Leaderboard", font=("Courier", 30), bg="#ffffff").pack(pady=15)
board = tkinter.Listbox(root, listvariable=players_var, borderwidth=0, highlightthickness=0, font=("Courier", 22), width=root.winfo_screenwidth()-30, height=100)
board.pack(padx=15, pady=15)
root.mainloop()