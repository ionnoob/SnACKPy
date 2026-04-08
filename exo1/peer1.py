import sys
import select

# Import helper functions for UDP communication
from udp_network import create_udp_socket, send_message, receive_message

# IP address and port where the peer will send messages
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# Create and configure the UDP socket using the helper function
sock = create_udp_socket()

# Display startup message for the chat
print("Peer1 UDP chat started")

# Show the prompt for the user to type a message
print("You: ", end="", flush=True)

# Infinite loop to keep the chat running
while True:

    # Wait until either:
    # - the user types something (sys.stdin)
    # - a message arrives on the socket (sock)
    readable, _, _ = select.select([sys.stdin, sock], [], [])

    # Iterate over the sources that are ready to read
    for r in readable:

        # If the input comes from the keyboard
        if r == sys.stdin:
            # Read the user's message from the terminal
            message = sys.stdin.readline().strip()

            # Send the message via UDP to the specified IP and port
            send_message(sock, message, UDP_IP, UDP_PORT)

        # If the input comes from the network socket
        elif r == sock:
            # Receive a message from the UDP socket
            msg, _ = receive_message(sock)

            # If a valid message was received
            if msg:
                # Print the message from the other peer
                print(f"Peer2: {msg}")

                # Re-display the prompt for the user
                print("\nYou: ", end="", flush=True)
