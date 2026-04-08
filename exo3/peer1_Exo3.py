import sys
import select
import random
import time

from udp_network_Exo3 import create_udp_socket, send_message, receive_message

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = create_udp_socket()

SN = random.randint(0, 100)

TIMEOUT = 5
waiting_ack = False
last_packet = None
last_send_time = None

print("Peer1 UDP chat started")
print("You: ", end="", flush=True)

while True:

    if waiting_ack and (time.time() - last_send_time > TIMEOUT):
        print("[TIMEOUT] Retransmission...")
        send_message(sock, last_packet, UDP_IP, UDP_PORT)
        last_send_time = time.time()

    readable, _, _ = select.select([sys.stdin, sock], [], [], 1)

    for r in readable:

        if r == sys.stdin:

            if waiting_ack:
                print("[WAIT] En attente de ACK...")
                print("You: ", end="", flush=True)
                continue

            message = sys.stdin.readline().strip()
            length = len(message)

            packet = f"DATA|{SN}|{length}|{message}"
            send_message(sock, packet, UDP_IP, UDP_PORT)

            last_packet = packet
            last_send_time = time.time()
            waiting_ack = True

            print(f"[SEND] DATA='{message}' | SN={SN} | LEN={length}")

        elif r == sock:
            msg, addr = receive_message(sock)

            if msg:
                parts = msg.split("|")

                if parts[0] == "DATA":
                    recv_SN = int(parts[1])
                    recv_len = int(parts[2])
                    data = parts[3]

                    print(f"Peer2: {data}")
                    print(f"[RECV] SN={recv_SN} | LEN={recv_len}")

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