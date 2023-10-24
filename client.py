#!/usr/bin/python3.11
from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
from struct import pack, unpack
import constants


def connect_to_server() -> socket:
    """
    Connects to a game server using a TCP socket.
    :return: A socket connected to the game server.
    """
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((constants.HOST, constants.PORT))
    return s


def get_bytes_from_server(client: socket, num_bytes: int) -> bytes:
    """
    Receives a specified number of bytes from the server.
    :param client: The socket for communication with the game server.
    :param num_bytes: The number of bytes to receive.
    :return: The received bytes.
    """
    buffer = b''
    while len(buffer) < num_bytes:
        data = client.recv(num_bytes - len(buffer))
        if data == b'':
            return buffer
        buffer += data
    return buffer


def get_packet_from_server(client: socket) -> bytes:
    """
    Receives a packet of data from the server.
    :param client: The socket for communication with the server.
    :return: The received packet as bytes.
    """
    header_size = 2
    packet_length, = unpack('!H', get_bytes_from_server(client, header_size))
    packet = get_bytes_from_server(client, packet_length)
    return packet


def receive_scores_from_server(client: socket) -> None:
    """
    Receives and displays player scores sent by the server.
    :param client: The socket for communication with the server.
    """
    scores_packet = get_packet_from_server(client)
    score_1, score_2 = unpack('!HH', scores_packet)
    print(f'Player 1: {score_1}, Player 2: {score_2}')


def receive_board_from_server(client: socket) -> None:
    """
    Receives and displays player scores and the game board sent by the server.
    :param client: The socket for communication with the server.
    """
    board_packet = get_packet_from_server(client)
    score_1, score_2 = unpack('!HH', board_packet[:4])
    board = board_packet[4:].decode()
    print(f'Player 1: {score_1}, Player 2: {score_2}')
    print(board)


def receive_results_from_server(client: socket) -> None:
    """
    Receives and displays game results sent by the server.
    :param client: The socket for communication with the server.
    """
    results_packet = get_packet_from_server(client)
    results = results_packet.decode()
    print(results)


def enter_game(curr_sock: socket) -> None:
    response_length, = unpack('!H', get_bytes_from_server(curr_sock, 2))
    if response_length == 0:
        print("Error, the game is full.")
    else:
        player_id, = unpack('!B', get_bytes_from_server(curr_sock, response_length))
        play_game(player_id, curr_sock)


def play_game(player_id: int, curr_sock: socket) -> None:
    print(f"Welcome, your id is {player_id}")
    command_map = {
        "U": 0x24 if player_id == 1 else 0x28,
        "D": 0x34 if player_id == 1 else 0x38,
        "L": 0x44 if player_id == 1 else 0x48,
        "R": 0x64 if player_id == 1 else 0x68,
        "Q": 0x00,
        "G": 0xF0
    }
    while True:
        command = input("Enter a command, (Q)uit, (G)ame, (U)p, (L)eft, (R)ight, (D)own: ")
        if command in command_map:
            curr_sock.sendall(bytes([command_map[command]]))
            if command == "Q":
                receive_results_from_server(curr_sock)
                break
            else:
                receive_board_from_server(curr_sock)







server_socket = connect_to_server()
enter_game(server_socket)







