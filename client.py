#!/usr/bin/python3.11
from asyncio import open_connection, run
from struct import unpack
import constants
"""
This Python script establishes a network connection to the game server (Game.py) and interacts 
with it using TCP sockets. 
It is split up into three parts.
    1. Network Functions
    2. General Gameplay
    3. Main Function
"""


async def get_bytes_from_server(reader, num_bytes: int) -> bytes:
    """
    Gets a specified number of bytes from the server.
    :param client: The socket for communication with the game server.
    :param num_bytes: The number of bytes to receive.
    :return: Bytes from server.
    """
    buffer = b''
    while len(buffer) < num_bytes:
        data = await reader.readexactly(num_bytes - len(buffer))
        if data == b'':
            return buffer
        buffer += data
    return buffer


async def get_payload_from_server(reader) -> bytes:
    """
    Gets a payload of data from the server.
     - Packet = [header][payload]
     - header = Length of payload as an Unsigned Short
    :param client: The socket for communication with the server.
    :return: The received packet as bytes.
    """
    header = await get_bytes_from_server(reader, constants.HEADER_LENGTH)
    payload_length = unpack('!H', header)[0]
    payload = await get_bytes_from_server(reader, payload_length)
    return payload


async def receive_board_from_server(reader) -> None:
    """
    Receives both scores and the game board sent by the server and displays result.
    :param client: The socket for communication with the server.
    """
    board_payload = await get_payload_from_server(reader)
    score_1, score_2 = unpack('!HH', board_payload[:4])
    board = board_payload[4:].decode()
    print(f'Player 1: {score_1}, Player 2: {score_2}')
    print(board)


async def receive_results_from_server(reader) -> None:
    """
    Receives and displays game results sent by the server.
    :param reader: The socket for communication with the server.
    """
    results_payload = await get_payload_from_server(reader)
    results = results_payload.decode()
    print(results)


async def play_game(player_id: int, reader, writer) -> None:
    """
    Manages the gameplay for a player, allowing them to send commands to the server
    and receive game updates.
    :param player_id: The unique id of the player.
    :param curr_sock: The socket for communication with the server.
    """
    print(f"Welcome, your id is {player_id}")

    available_commands = {
        "U": 0x24 if player_id == 1 else 0x28,
        "D": 0x34 if player_id == 1 else 0x38,
        "L": 0x44 if player_id == 1 else 0x48,
        "R": 0x64 if player_id == 1 else 0x68,
        "Q": 0x04 if player_id == 1 else 0x08,
        "G": 0xF4 if player_id == 1 else 0xF8
    }

    while True:
        command = input("Enter a command, (Q)uit, (G)ame, (U)p, (L)eft, (R)ight, (D)own: ").upper()
        if command in available_commands:
            writer.write(bytes([available_commands[command]]))
            if command == "Q":
                await receive_results_from_server(reader)
                break
            else:
                await receive_board_from_server(reader)


async def main():
    reader, writer = await open_connection(constants.HOST, constants.PORT)
    initial_response_bytes = await reader.readexactly(constants.HEADER_LENGTH)
    initial_response = unpack('!H', initial_response_bytes)[0]

    if initial_response == 0:
        print("Error, the game is full")
    else:
        player_id_bytes = await reader.readexactly(initial_response)
        player_id = unpack('!B', player_id_bytes)[0]
        await play_game(player_id, reader, writer)

run(main())
