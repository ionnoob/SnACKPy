import socket

BUFFER_SIZE = 1024  # Maximum message size

def create_udp_socket():
    """Create a UDP socket."""
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_message(sock, message, ip, port):
    """Send a message to the specified IP and port."""
    sock.sendto(message.encode(), (ip, port))

def receive_message(sock):
    """Receive a message from any sender."""
    data, addr = sock.recvfrom(BUFFER_SIZE)
    return data.decode(), addr

def bind_socket(sock, ip, port):
    """Bind the socket to an IP and port."""
    sock.bind((ip, port))