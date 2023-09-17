import socket
# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to a port
server_socket.bind(("localhost", 8080))