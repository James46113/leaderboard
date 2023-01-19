import socket, sys

port = int(sys.argv[1])
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", port))
print(f"IP: {server.getsockname()[0]}\nPORT: {server.getsockname()[1]}")
server.listen()
client, _ = server.accept()
while (name := input("Enter player name: ")) != "exit":
    if len(name) == 0:
        print("Please enter a name")
        continue
    try:
        while (score := int(input("Enter player score: "))) >= 100:
            print("Score must be under 100")
    except ValueError:
        print("Please enter a valid score")
        continue
    client.send((name + "|" + str(score)).encode("ascii"))
    if (e := client.recv(1024).decode("ascii")) != "Added player":
        print("An error occured on the server side:", e)
        break