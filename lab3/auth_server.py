import socket
import hashlib
import pyotp #type: ignore
import time

serverPort = 12000
username = "harkaran"
h = hashlib.sha256()

  # Example base32 secret

shared_secret = pyotp.random_base32()
hotp = pyotp.HOTP(shared_secret)


# Password is no longer stored on server
# It's stored in a password.txt, that is read and hashed on the server
# filename = "password.txt"
n = 0

# try:
#     with open(filename, 'rb') as f:
#         passw = f.read()
#         h.update(passw)
#         hashpass = h.hexdigest()

# except FileNotFoundError:
#     print("File not found")

# password is stored as a hash
# User input for password will be hashed and directly compared to see if hashes are the same
hashpass = "0be64ae89ddd24e225434de95d501711339baeee18f009ba9b4369af27d30d60"



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', serverPort))
    s.listen()
    print("Server is now running")

    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        conn.send("You have connected to the server\nWhat's your username?\n".encode())

        authorized = False
        username_accepted = False
        password_accepted = False
        cred_fails = 0


        while not username_accepted:
            data = conn.recv(1024)
            if not data:
                break


            client_input = data.decode().strip().lower()
            print(f"Client sent username attempt: {client_input}")

            if client_input == username:
                conn.send("Username accepted, please enter your password\n".encode())
                print("Username correct. Moving to password stage.")
                username_accepted = True

            else:
                cred_fails += 1
                if cred_fails >= 3:
                    conn.send("Too many incorrect username attempts, disconnecting\n".encode())
                    print(f"Disconnecting {addr} after 3 failed usernames.")
                    conn.close()

                    
                else:
                    conn.send(f"Incorrect username, please try again (Attempt {cred_fails}/3)\n".encode())

        # Reset failure counter for the password stage
        cred_fails = 0

        while username_accepted and not password_accepted:
                    data = conn.recv(1024)
                    if not data:
                        break
                    
                    password_input = data.decode().strip()
                    
                    # Hash the received password
                    client_hash = hashlib.sha256(password_input.encode()).hexdigest()

                    if client_hash == hashpass:
                        print("Password correct. Moving to OTP stage.")
                        conn.send("The username password combination is correct\n".encode())
                        
                        # Send secret and prompt as one message
                        auth_payload = f"{shared_secret}\nPlease enter your one time password\n"
                        conn.send(auth_payload.encode())
                        print(f"Debugging secret sent: {shared_secret}")
                        
                        password_accepted = True # Password stage complete
                    else:
                        cred_fails += 1
                        if cred_fails >= 3:
                            conn.send("Too many incorrect password attempts, disconnecting\n".encode())
                            print(f"Disconnecting {addr} after 3 failed passwords.")
                            conn.close()
                            

                        else:
                            conn.send(f"Incorrect password, please try again (Attempt {cred_fails}/3)\n".encode())

        while password_accepted and not authorized:
            # Everytime user gets OTP wrong, a new one is generated
            
            current_otp = hotp.at(n)

            if data := conn.recv(1024):
                data = data.decode().strip()

                if data == current_otp:
                    conn.send("You have been authorized\n".encode())
                    authorized = True
                    print("Client is now authorized")
                    errcount = 0
                elif n >= 5:
                    conn.send("Too many incorrect OTP attempts, disconnecting\n".encode())
                    conn.close()
                    break
                else:
                    conn.send("Incorrect OTP, please try again\n".encode())
                    n += 1
                    print("Client entered incorrect OTP, attempt number:", n)
                            

                while authorized:
                    welcome_message = (
                    f"\nWelcome to the stateful server {username}, "
                    "you have 2 options of what you can input (Character limit of 128)\n"
                    "1. 'MSG|' you can enter the prefix followed by any text\n"
                    "2. EXIT\n\n"
                    "Error count: " + str(errcount) + "\n"
                    "Exceeding 5 errors will disconnect you\n\n"
                )

                    conn.sendall(welcome_message.encode())

                    data = conn.recv(1024)
                    if not data:
                        break

                    data = data.decode().strip()
                    data = data.upper()

                    print("\nClient said: " + data + "\n") 

                    if len(data) > 128:
                        conn.sendall("\nYou sent above the character limit, try not to do that\n".encode())



                    elif data[0:4] == "MSG|":
                        data = data[4:]
                        response = (("\nOk " + data + "\n").encode())
                        print("Client said: " + data)
                        conn.sendall(f"Ok {data}\n".encode())

                    elif data == "EXIT":
                        print("Client has exited")
                        authorized = False
                        conn.close()
                        break

                    else:
                        conn.send("Error, that isn't a valid input\n".encode())
                        errcount += 1
                        if errcount >= 5:
                            conn.send("Too many invalid inputs, disconnecting\n".encode())
                            conn.close()

                            break
