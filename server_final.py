import socket
import ssl
import threading

# Dummy database of bank accounts
accounts = {
    '1234567890': {'balance': 100000, 'pin': '1234', 'aadhar': True},
    '0987654321': {'balance': 5000, 'pin': '4321', 'aadhar': False},
    '5555555555': {'balance': 20000, 'pin': '5555', 'aadhar': True},
    '1234123412': {'balance': 100, 'pin': '1234', 'aadhar': False},
    '7890789078': {'balance': 190027, 'pin':'7890','aadhar': False}
}

def validate_account(account_number, pin):
    if account_number in accounts:
        return accounts[account_number]['pin'] == pin
    return False

def check_balance(account_number):
    return accounts[account_number]['balance']

def transfer_money(sender_account, receiver_account, amount):
    if sender_account in accounts and receiver_account in accounts:
        sender_balance = accounts[sender_account]['balance']
        if sender_balance >= amount:
            accounts[sender_account]['balance'] -= amount
            accounts[receiver_account]['balance'] += amount
            return 'SUCCESS'
        else:
            return 'INSUFFICIENT_BALANCE'
    elif sender_account not in accounts:
        return 'SENDER_NOT_FOUND'
    else:
        return 'RECEIVER_NOT_FOUND'
    
def aadhar_seeding(account_number):
    if account_number in accounts:
        return accounts[account_number]['aadhar']
    else:
        return 'ACCOUNT_NOT_FOUND'
    
def handle_client_connection(ssl_conn, addr):
    flag = False
    while True:
        data = ssl_conn.recv(1024).decode()

        if data == 'LOGIN':
            ssl_conn.send(str.encode("PROCEED"))
            data_login = ssl_conn.recv(1024).decode()
            account_number, pin = data_login.split()
            if validate_account(account_number, pin):
                ssl_conn.send(str.encode("LOGIN_SUCCESS"))
                flag = True
                continue
            else:
                ssl_conn.send(str.encode("LOGIN_FAILED"))
                continue

        elif data == 'BALANCE':
            if flag:
                ssl_conn.send(str.encode("PROCEED"))
                data_balance = ssl_conn.recv(1024).decode()
                account_number, pin = data_balance.split()
                if validate_account(account_number, pin):
                    balance = check_balance(account_number)
                    ssl_conn.send(str.encode(f"{balance}"))
                    continue
                else:
                    ssl_conn.send(str.encode("ERROR"))
                    continue
            else:
                ssl_conn.send(str.encode("NO_LOGIN"))
                continue
                
        elif data == 'TRANSFER':
            if flag:
                ssl_conn.send(str.encode("PROCEED"))
                data_transfer = ssl_conn.recv(1024).decode()
                sender_account, receiver_account, amount = data_transfer.split()
                amount = float(amount)
                result = transfer_money(sender_account, receiver_account, amount)
                ssl_conn.send(str.encode(str(result)))
                continue
            else:
                ssl_conn.send(str.encode("NO_LOGIN"))
                continue

        elif data == 'AADHAR':
            if flag:
                ssl_conn.send(str.encode("PROCEED"))
                data_aadhar = ssl_conn.recv(1024).decode()
                result = aadhar_seeding(data_aadhar)
                if result == True:
                    ssl_conn.send(str.encode("TRUE"))
                elif result == False:
                    ssl_conn.send(str.encode("FALSE"))
                    aadhar_number = ssl_conn.recv(1024).decode()
                    if(len(aadhar_number)==12):
                        accounts[account_number]['aadhar'] = True
                        ssl_conn.send(str.encode('SUCCESS'))
                    else:
                        ssl_conn.send(str.encode('INCORRECT'))
                else:
                    ssl_conn.send(str.encode("ACCOUNT_NOT_FOUND"))
            else:
                ssl_conn.send(str.encode("NO_LOGIN"))
                continue

        else:
            break
    ssl_conn.close()

def main():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="cn_pro.crt", keyfile="cn_pro.key")
    ssl_server_socket = context.wrap_socket(server_socket, server_side=True)
    print("Bank server is running...")

    while True:
        ssl_conn, addr = ssl_server_socket.accept()
        print(f"Connection established with {addr}")
        threading.Thread(target=handle_client_connection, args=(ssl_conn, addr)).start()

if __name__ == "__main__":
    main()
