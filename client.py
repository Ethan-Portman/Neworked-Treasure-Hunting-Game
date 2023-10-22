#!/usr/bin/python3.11

from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
from struct import pack, unpack

# Network Variables
BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12346







def get_bytes(curr_sock: socket, num_bytes: int) -> bytes:
    buffer = b''
    while len(buffer) < num_bytes:
        data = curr_sock.recv(min(num_bytes - len(buffer), BUF_SIZE))
        if data == b'':
            return buffer
        buffer += data
    return buffer


def connect_to_server() -> socket:
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((HOST, PORT))
    return s


def enter_game(curr_sock: socket) -> int:
    initial_response = get_bytes(curr_sock, 1)
    if initial_response == b'':
        return -1
    player_id, = unpack('!B', initial_response)
    return player_id



"""
player 1: xxxx01xx
player 2: xxxx10xx

U: 0010xxxx
player1: 00100100


L: 0100xxxx
R: 0110xxxx
D: 0011xxxx
Q: 1000xxxx
G: 1111xxxx
"""

def get_bytes(curr_sock: socket, num_byes: int) -> bytes:
    buffer = b''
    while len(buffer) < num_byes:
        data = curr_sock.recv(num_byes - len(buffer))
        if data == b'':
            return buffer
        buffer += data
    return buffer


def play_game(player_id: int, curr_sock: socket) -> None:
    print(f"Welcome, your id is {player_id}")
    while True:
        command = input("Enter a command, (Q)uit, (G)ame, (U)p, (L)eft, (R)ight, (D)own: ")
        match command:
            case "U":
                curr_sock.sendall(bytes([0x24]) if player_id == 0 else bytes([0x28]))
            case "D":
                curr_sock.sendall(bytes([0x34]) if player_id == 0 else bytes([0x38]))
            case "L":
                curr_sock.sendall(bytes([0x44]) if player_id == 0 else bytes([0x48]))
            case "R":
                curr_sock.sendall(bytes([0x64]) if player_id == 0 else bytes([0x68]))
            case "Q":
                curr_sock.sendall(bytes([0x00]))
            case "G":
                curr_sock.sendall(bytes([0xF0]))

        response_size, = unpack('!B', curr_sock.recv(1))
        response = get_bytes(curr_sock, response_size)
        print(response.hex())


sock = connect_to_server()
player_id = enter_game(sock)
if player_id == -1:
    print("Error, the game is full.")
else:
    play_game(player_id, sock)






with socket(AF_INET, SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    initial_response = unpack('!B', get_bytes(sock, 1))
    if initial_response == -1:
        print("Error, the game is full.")
    player_id = initial_response
    print(f"Your player id is {player_id}")
    # Get the player ID
    while True:
        # Receive the prompt
        reply = sock.recv(BUF_SIZE)

        # Perform the Command

        # Show scores and latest board after every direction command





