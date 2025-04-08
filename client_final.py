import socket
import ssl

def main():
    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Create SSL context
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations('cn_pro.crt')
    # Wrap the socket with SSL
    ssl_client_socket = context.wrap_socket(client_socket, server_hostname='Jananii')

    ssl_client_socket.connect((host, port))

    print("Connected to bank server.")

    account_number = 'temp'

    while True:
        print("1. Login")
        print("2. Check Balance")
        print("3. Transfer Money")
        print("4. Aadhar Seeding")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            ssl_client_socket.sendall(str.encode("LOGIN"))
            confirmation = ssl_client_socket.recv(1024).decode()
            if confirmation == "PROCEED":
                account_number = input("Enter your account number: ")
                pin = input("Enter your PIN: ")
                #ssl_client_socket.sendall(str.encode(f"LOGIN {account_number} {pin}"))
                ssl_client_socket.sendall(str.encode(f"{account_number} {pin}"))
                response = ssl_client_socket.recv(1024).decode()
                print(response)
                continue
            else:
                print("An error occured. Please try again!")
                continue


        elif choice == '2':
            #account_number = input("Enter your account number: ")
            #ssl_client_socket.sendall(str.encode(f"BALANCE {account_number}"))
            ssl_client_socket.sendall(str.encode("BALANCE"))
            confirmation = ssl_client_socket.recv(1024).decode()
            #print("works till here")
            if confirmation == "PROCEED":
                # account_number = input("Enter your account number: ")
                # pin = input("Enter your pin: ")
                ssl_client_socket.sendall(str.encode(f"{account_number} {pin}"))
                balance = ssl_client_socket.recv(1024).decode('utf-8')
                if balance == "ERROR":
                    print("Incorrect pin!")
                    continue
                elif balance == "NO_LOGIN":
                    print("Please Login to proceed")
                    continue
                else:
                    print(f"Balance: {balance}")
                    continue
            else:
                print("Please login to continue")
            # balance = ssl_client_socket.recv(1024).decode()
            # if balance == "NO_LOGIN":
            #     print("please login first")
            # else:
            #     print(f"Balance: {balance}")
            #     #print(balance)

        elif choice == '3':
            ssl_client_socket.sendall(str.encode("TRANSFER"))
            confirmation = ssl_client_socket.recv(1024).decode()
            if confirmation == "PROCEED":   
                # sender_account = input("Enter sender's account number: ")
                receiver_account = input("Enter receiver's account number: ")
                amount = input("Enter amount to transfer: ")
                ssl_client_socket.sendall(str.encode(f"{account_number} {receiver_account} {amount}"))
                response = ssl_client_socket.recv(1024).decode()
                if response == "INSUFFICIENT_BALANCE":
                    print("Insufficient balance")
                    continue
                elif response == "SENDER_NOT_FOUND":
                    print("Sender account number is invalid! Please retry")
                    continue
                elif response == "RECIEVER_NOT_FOUND":
                    print("Reciever account number is invalid! Please try again")
                    continue
                elif response == 'NO_LOGIN':
                    print("Please login to continue")
                else:
                    print("Transfer successful")
                    continue

        elif choice == '4':
            ssl_client_socket.sendall(str.encode("AADHAR"))
            confirmation = ssl_client_socket.recv(1024).decode()
            if confirmation == "PROCEED":
                # account_number = input("Enter your account number: ")
                ssl_client_socket.sendall(str.encode(f"{account_number}"))
                response = ssl_client_socket.recv(1024).decode()
                if response == 'TRUE':
                    print("Aadhar seeded to account")
                elif response == 'FALSE':
                    print("Aadhar not seeded to account")
                    aadhar_number = input('please enter your aadhar number: ')
                    ssl_client_socket.sendall(str.encode(f"{aadhar_number}"))
                    status = ssl_client_socket.recv(1024).decode()
                    if status == 'SUCCESS':
                        print('Aadhar successfully added')
                    else:
                        print('Invalid Aadhar')
                elif response == 'NO_LOGIN':
                    print("Please login to continue")
                else:
                    print("Account not found")

        elif choice == '5':
            break

        else:
            print("Invalid choice")

    ssl_client_socket.close()

if __name__ == "__main__":
    main()
