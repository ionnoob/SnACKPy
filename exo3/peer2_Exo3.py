import sys
import select
import random
import time

from udp_network_Exo3 import create_udp_socket, bind_socket, send_message, receive_message

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = create_udp_socket()
bind_socket(sock, UDP_IP, UDP_PORT)

peer_addr = None

SN = random.randint(0, 100)

TIMEOUT = 5
waiting_ack = False
last_packet = None
last_send_time = None

print("Peer2 UDP chat started. Waiting for messages from Peer1")

while True:

    if waiting_ack and (time.time() - last_send_time > TIMEOUT):
        print("[TIMEOUT] Retransmission...")
        send_message(sock, last_packet, peer_addr[0], peer_addr[1])
        last_send_time = time.time()

    readable, _, _ = select.select([sys.stdin, sock], [], [], 1)

    for r in readable:

        if r == sock:
            msg, addr = receive_message(sock)

            peer_addr = addr

            if msg:
                parts = msg.split("|")

                if parts[0] == "DATA":
                    recv_SN = int(parts[1])
                    recv_len = int(parts[2])
                    data = parts[3]

                    print(f"Peer1: {data}")
                    print(f"[RECV] SN={recv_SN} | LEN={recv_len}")

                    if random.random() < 0.2:
                        print("[LOSS SIMULATED] ACK perdu")
                    else:
                        ack = f"ACK|{recv_SN}"
                        send_message(sock, ack, addr[0], addr[1])
                        print(f"[SEND] ACK={recv_SN}")

                elif parts[0] == "ACK":
                    ack_SN = int(parts[1])

                    print(f"[RECV] ACK={ack_SN}")

                    if ack_SN == SN:
                        print("[CHECK] ACK correct")
                        SN += 1
                        waiting_ack = False
                    else:
                        print("[CHECK] ACK incorrect")

                print("\nYou: ", end="", flush=True)

        elif r == sys.stdin:

            if peer_addr:

                if waiting_ack:
                    print("[WAIT] En attente de ACK...")
                    print("You: ", end="", flush=True)
                    continue

                message = sys.stdin.readline().strip()
                length = len(message)

                packet = f"DATA|{SN}|{length}|{message}"
                send_message(sock, packet, peer_addr[0], peer_addr[1])

                last_packet = packet
                last_send_time = time.time()
                waiting_ack = True

                print(f"[SEND] DATA='{message}' | SN={SN} | LEN={length}")