import socket

def run_test_client():
    server_ip = '10.5.0.2'
    server_port = 12000
    password = "HELLO"
    username = "Harkaran"

    try: 
        # Connects to the server and sends the password to automatically be authorized
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            print(f"Connecting to server at {server_ip}:{server_port}...")
            client_socket.connect((server_ip, server_port))

            client_socket.sendall(password.encode())
            response = client_socket.recv(1024).decode()
            print(f"Server response to password: {response.strip()}")

            # Establishes a username for server to use
            if "What is your name?" in response:
                client_socket.sendall(username.encode())
                welcome = client_socket.recv(1024).decode()
                print(f"Server Welcome: {welcome.strip()}")

            # Testing out changing username command
            print("\n Testing Command: HELLO| \n")
            client_socket.sendall("HELLO|Harkaran New Name".encode())
            print(f"Server response: {client_socket.recv(1024).decode().strip()}")
            client_socket.recv(1024) 

            # Testing out the test massage command
            print("\n Testing Command: MSG| \n")
            client_socket.sendall("MSG|Test message, please work".encode())
            print(f"Server response: {client_socket.recv(1024).decode().strip()}")
            client_socket.recv(1024)

            print("\n Testing Command: EXIT \n")
            client_socket.sendall("EXIT".encode())
            print("Sent EXIT command. Closing connection.")

    # Error handling if server is not reachable or anything else
    except ConnectionRefusedError:
        print("Error: Could not connect to the server")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":

    run_test_client()
