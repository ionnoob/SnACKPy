import sys
import select
import random

# Import helper functions used for UDP communication
from udp_network_Exo2 import create_udp_socket, bind_socket, send_message, receive_message

# IP address and port where this peer will listen
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# Create the UDP socket
sock = create_udp_socket()

# Bind the socket
bind_socket(sock, UDP_IP, UDP_PORT)

# Variable to store peer address
peer_addr = None

# Initialize sequence number
SN = random.randint(0, 100)

print("Peer2 UDP chat started. Waiting for messages from Peer1")

while True:

    readable, _, _ = select.select([sys.stdin, sock], [], [])

    for r in readable:

        # Message reçu
        if r == sock:
            msg, addr = receive_message(sock)

            peer_addr = addr

            if msg:
                parts = msg.split("|")

                # DATA reçu
                if parts[0] == "DATA":
                    recv_SN = int(parts[1])
                    recv_len = int(parts[2])
                    data = parts[3]

                    print(f"Peer1: {data}")
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

        # Envoi utilisateur
        elif r == sys.stdin:

            if peer_addr:
                message = sys.stdin.readline().strip()
                length = len(message)

                packet = f"DATA|{SN}|{length}|{message}"
                send_message(sock, packet, peer_addr[0], peer_addr[1])

                print(f"[SEND] DATA='{message}' | SN={SN} | LEN={length}")