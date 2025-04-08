# Secure Banking System using SSL in Python

This project is a secure banking system simulation implemented in Python using socket programming and SSL/TLS encryption. It consists of a client-server architecture where the client can perform basic banking operations securely over an encrypted channel.

## Features

- Secure communication using SSL
- User authentication (Login)
- Balance inquiry
- Money transfer between accounts
- Aadhar seeding (for KYC compliance)

## Project Structure

.
├── client_final.py           # Client-side application for user interaction
├── server_final.py           # Server-side application handling banking logic
├── cn_pro.crt          # SSL Certificate (for secure communication)
├── cn_pro.key          # SSL Private Key (for the server)
└── README.md           # Project documentation

## Requirements

- Python 3.x
- OpenSSL (for generating certificates)
- No external Python libraries required (uses standard `socket` and `ssl` modules)

## Setting Up

### 1. Generate SSL Certificate and Key (if not already provided)

openssl req -x509 -newkey rsa:4096 -keyout cn_pro.key -out cn_pro.crt -days 365 -nodes

> Ensure that the Common Name (CN) matches the server name ("Jananii").

### 2. Start the Server

python server.py

You should see:
"Bank server is running..."

### 3. Run the Client

Open a new terminal window and run:

python client.py

## Client Options

1. Login – Enter account number and PIN to authenticate.
2. Check Balance – View current balance (requires login).
3. Transfer Money – Transfer funds to another account (requires login).
4. Aadhar Seeding – Link your Aadhar number to your account if not already linked.
5. Exit – Close the client application.

## Sample Accounts (For Testing)

| Account Number | PIN   | Balance  | Aadhar Linked |
|----------------|-------|----------|----------------|
| 1234567890     | 1234  | 100000   | Yes            |
| 0987654321     | 4321  | 5000     | No             |
| 5555555555     | 5555  | 20000    | Yes            |
| 1234123412     | 1234  | 100      | No             |
| 7890789078     | 7890  | 190027   | No             |

## Notes

- All communications are SSL-encrypted, ensuring data confidentiality.
- Server handles multiple clients using threads.
- Only valid account numbers and correct PINs are accepted.
- The login session is retained for each client connection.

## License

This project is for educational purposes only. Not intended for production use.

## Author

Jananii
