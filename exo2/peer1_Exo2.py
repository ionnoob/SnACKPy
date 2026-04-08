import sys
import select
import random

# Import helper functions for UDP communication
from udp_network_Exo2 import create_udp_socket, send_message, receive_message

# IP address and port where the peer will send messages
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# Create socket
sock = create_udp_socket()

# Initialize sequence number
SN = random.randint(0, 100)

print("Peer1 UDP chat started")
print("You: ", end="", flush=True)

while True:

    readable, _, _ = select.select([sys.stdin, sock], [], [])

    for r in readable:

        # Keyboard input
        if r == sys.stdin:
            message = sys.stdin.readline().strip()
            length = len(message)

            packet = f"DATA|{SN}|{length}|{message}"
            send_message(sock, packet, UDP_IP, UDP_PORT)

            print(f"[SEND] DATA='{message}' | SN={SN} | LEN={length}")

        # Socket input
        elif r == sock:
            msg, addr = receive_message(sock)

            if msg:
                parts = msg.split("|")

                # DATA reçu
                if parts[0] == "DATA":
                    recv_SN = int(parts[1])
                    recv_len = int(parts[2])
                    data = parts[3]

                    print(f"Peer2: {data}")
                    print(f"[RECV] SN={recv_SN} | LEN={recv_len}")

                    # envoyer ACK
                    ack = f"ACK|{recv_SN}"
                    send_message(sock, ack, addr[0], addr[1])

                    print(f"[SEND] ACK={recv_SN}")

                # ACK reçu
                elif parts[0] == "ACK":
                    ack_SN = int(parts[1])

                    print(f"[RECV] ACK={ack_SN}")

                    if ack_SN == SN:
                        print("[CHECK] ACK correct")
                        SN += 1
                    else:
                        print("[CHECK] ACK incorrect")

                print("\nYou: ", end="", flush=True)