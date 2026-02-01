import socket
import pyotp #type: ignore

def run_test_client():
    server_ip = '10.5.0.2'
    server_port = 12000
    empty_user_count = 0
    empty_pass_count = 0


    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            print(f"Connecting to server at {server_ip}:{server_port}...")
            client_socket.connect((server_ip, server_port))

            # Username input and sending
            response = client_socket.recv(1024).decode()
            print(response.strip())

            # Username loop 
            while True:
                username = ""
                # username = input()

                while not username:
                    username = input("Username: ").strip()
                    if not username:
                        empty_user_count += 1
                        print("Input cannot be empty. Please enter a username.")
                        print((f"Empty input attempts: {empty_user_count}/5\n"))

                        if empty_user_count >= 5:
                            print("Too many empty inputs, disconnecting.")
                            client_socket.close()
                            return
                        
                client_socket.send(username.encode())
                response = client_socket.recv(1024).decode()
                print(response.strip())
                if "Username accepted" in response:
                    break
                if "disconnecting" in response:
                    return
                
            # Password loop
            while True:
                # password = input("Password: ")
                password = ""

                while not password:
                    password = input("Password: ").strip()
                    if not password:
                        empty_pass_count += 1
                        print("Input cannot be empty. Please enter a password.")
                        print((f"Empty input attempts: {empty_pass_count}/5\n"))

                        if empty_pass_count >= 5:
                            print("Too many empty inputs, disconnecting.")
                            client_socket.close()
                            return

                client_socket.send(password.encode())
                combined_data = client_socket.recv(4096).decode()

                if "Incorrect password" in combined_data:
                    print(combined_data.strip())
                elif "Disconnecting" in combined_data:
                    print(combined_data.strip())
                    return
                else:
                    print("\n--- Auth Data Recevied ---")
                    print(combined_data.strip())
                    print("--------------------------\n")
                    break

            # Secret

            raw_data = client_socket.recv(1024).decode()
            secret = raw_data.split()[0].strip()
            
            print(f"Extracted Secret: {secret}")
            hotp = pyotp.HOTP(secret)
            
            auth = False
            otp_counter = 0


            # OTP loop
            while not auth:

                otp_code = hotp.at(otp_counter)
                print(f"Sending OTP (Counter {otp_counter}): {otp_code}")
                client_socket.send(otp_code.encode())

                response = client_socket.recv(1024).decode()
                print(f"Server: {response.strip()}")

                if "authorized" in response.lower():
                    auth = True
                elif "incorrect" in response.lower():
                    otp_counter += 1
                    return
            
            while auth:
                welcome = client_socket.recv(1024).decode()
                print(welcome.strip())
                
                user_input = ""
                empty_count = 0

                while not user_input:
                    user_input = input("Enter command: ").strip()

                    if not user_input:
                            empty_count += 1
                            print("Input cannot be empty. Please enter a command.")
                            print((f"Empty input attempts: {empty_count}/5\n"))

                            if empty_count >= 5:
                                print("Too many empty inputs, disconnecting.\n")
                                client_socket.close()
                                return

                client_socket.send(user_input.encode())
                
                if user_input.upper() == "EXIT":
                    print("Exiting...")
                    break

                response = client_socket.recv(1024).decode()
                print(f"\nResponse: {response.strip()}\n")








            # response = client_socket.recv(1024).decode()
            # if response.strip() == "Incorrect username, please try again\n":
            #     while response.strip() == "Incorrect username, please try again\n":
            #         print(response.strip())
            #         username = input()
            #         client_socket.send(username.encode())
            #         response = client_socket.recv(1024).decode()
            # else:

            # # Password input and sending
            #     response = client_socket.recv(1024).decode()
            #     print(response.strip())
            # password = input()
            # client_socket.send(password.encode())

            # # Takes the combination correct, secret, and OTP prompt block
            # # Using 4096 to receive all at once other wise it breaks on me
            # combined_data = client_socket.recv(4096).decode()
            # print("\n--- Received from Server ---")
            # print(combined_data.strip())
            # print("----------------------------\n")

            # Extract the secret from the combined data
            # lines = [line.strip() for line in combined_data.split('\n') if line.strip()]

            # secret = ""
            # for line in lines:
                
            #     if line.isupper() and len(line) >= 16:
            #         secret = line
            #         break

            # if not secret:
            #     print("Shared secret not found in server response.")
            #     return
            
            # print(f"Extracted Secret: {secret}")
            # response = client_socket.recv(1024).decode()

            # raw_data = client_socket.recv(1024).decode()
            # secret = raw_data.split()[0].strip()

            # # secret = client_socket.recv(1024).decode()
            # print(f"Received secret: {secret}")
            # # print(response.strip())

            # hotp = pyotp.HOTP(secret)
            # print("Test for secret\n")
            # print(hotp.at(0)) 
            # print("\nTest for secret\n")
            # client_socket.send(hotp.at(0).encode())
            
            # auth = False
            # while not auth:
            #     n = 0


            #     print(response.strip())
            #     otp_count = hotp.at(n)
            # # print(f"Generated OTP (Counter 0): {otp_0}")
            #     client_socket.send(otp_count.encode())

            #     response = client_socket.recv(1024).decode()
            #     print(response.strip())

            #     if response.strip() == "You have been authorized":
            #         # print("Client successfully authorized with OTP.")
            #         auth = True
            
            # while auth:
            #     welcome = client_socket.recv(1024).decode()
            #     print(welcome.strip())

            #     userinpt = input("Enter your choice: ")
            #     if userinpt == "":
            #         empt = 0

            #         while userinpt == "":

            #             empt += 1
            #             print("Input cannot be empty. Please try again.")
            #             userinpt = input("Enter your choice: ")

            #             if empt >= 5:
            #                 print("Too many empty inputs, disconnecting.")
            #                 client_socket.close()
            #                 return
            #         continue

            #     client_socket.send(userinpt.encode())
            #     response = client_socket.recv(1024).decode()
            #     print(response.strip())

            #     # break


                



            # response = client_socket.recv(1024).decode()
            # print(response.strip())
            # secret = client_socket.recv(1024).decode()
            # print("\nTest test test\n")
            # print(secret)
            # print("\n")
            # response = client_socket.recv(1024).decode()
            # print(response.strip())

            # hotp = pyotp.HOTP(secret)
            # print("Test for secret\n")
            # print(hotp.at(0))  # OTP for counter 0
            # print("\ndone\n")
            # client_socket.send(hotp.at(0).encode())

            # response = client_socket.recv(1024).decode()
            # print(response.strip())




            # if "What is your name?" in response:
            #     client_socket.sendall(username.encode())
            #     welcome = client_socket.recv(1024).decode()
            #     # print(f"Server Welcome: {welcome.strip()}")

            # print("\n Testing Command: HELLO| \n")
            # client_socket.sendall("HELLO|Harkaran New Name".encode())
            # print(f"Server response: {client_socket.recv(1024).decode().strip()}")
            # client_socket.recv(1024) 

            # # print("\n Testing Command: MSG| \n")
            # client_socket.sendall("MSG|Test message, please work".encode())
            # # print(f"Server response: {client_socket.recv(1024).decode().strip()}")
            # client_socket.recv(1024)

            # # print("\n Testing Command: EXIT \n")
            # client_socket.sendall("EXIT".encode())
            # print("Sent EXIT command. Closing connection.")

    except ConnectionRefusedError:
        print("Error: Could not connect to the server")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_test_client()