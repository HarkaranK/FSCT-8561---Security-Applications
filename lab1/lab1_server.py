import socket

serverPort = 12000
password = "HELLO"


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', serverPort))
    s.listen()
    print("Server is now running")

    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)

        while True:
            data = conn.recv(1024)
            if not data:
                break

            authorized = False

            while not authorized:

                print("Client said: " + data.decode())
                data = data.decode().strip()

                if data == password:
                    authorized = True
                    conn.send("Hi nice to meet you.\nWhat is your name?\n".encode())
                    data = conn.recv(1024)
                    username = data.decode().strip()

                else:
                    conn.send("Error, that isn't a valid input\n".encode())
                    break
            
            while authorized:
                welcome_message = (
                    f"\nWelcome to the stateful server {username}, "
                    "you have 3 options of what you can input (Character limit of 128)\n"
                    "1. 'HELLO|' you can enter prefix followed by anything to introduce yourself\n"
                    "2. 'MSG|' you can enter the prefix followed by any text\n"
                    "3. EXIT\n\n"
                )

                conn.sendall(welcome_message.encode())

                data = conn.recv(1024)
                data = data.decode().strip()

                if len(data) > 128:
                    conn.sendall("You sent above the character limit".encode())

                elif data[0:6] == "HELLO|":
                    data = data[6:]
                    response = (("\nHi nice to meet you " + data + "\n").encode())
                    print("Client said: " + data)
                    username = data
                    conn.sendall(response)

                elif data[0:4] == "MSG|":
                    data = data[4:]
                    response = (("\nOk " + data + "\n").encode())
                    print("Client said: " + data)
                    conn.sendall(response)

                elif data == "EXIT":
                    print("Client has exited")
                    authorized = False
                    conn.close()
                    break

                else:
                    conn.sendall("\nThat wasn't a valid input\n".encode())

            # conn.sendall("\n".encode())
