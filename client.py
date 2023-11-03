#!/usr/bin/python3.11
from asyncio import open_connection, run
from struct import unpack
import constants

"""
This script is an asynchronous client program that interacts with a game server (Game.py) over a network connection. 
It allows players to participate in a multiplayer game by sending commands to the server and receiving game updates. 
The script establishes a connection to the game server, obtains a unique player ID, and then enters a loop where 
players can input commands (e.g., move in different directions, get game results, or quit). The server responds with 
game updates, including scores and the current game board, and the player's interactions are managed asynchronously.
"""


async def get_bytes_from_server(reader, num_bytes: int) -> bytes:
    """
    Asynchronously receives and accumulates a specified number of bytes from the server. If the connection is closed
    and data received is b'' the buffer is returned without getting the full amount of bytes requested.

    :param reader: A StreamReader for reading data from the server.
    :param num_bytes: The number of bytes to receive and accumulate.
    :return: A bytes object containing the accumulated bytes received from the server.
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
    Asynchronously retrieves a payload of data from the server, following a defined packet structure. The packet
    structure from the server consists of two parts:
     - Header: A packed unsigned short representing the length of the payload.
     - Payload: The actual data content of the packet.

    :param reader: A StreamReader for reading data from the server.
    :return: A bytes object containing the received packet's payload.
    """
    header = await get_bytes_from_server(reader, constants.HEADER_LENGTH)
    payload_length = unpack('!H', header)[0]
    payload = await get_bytes_from_server(reader, payload_length)
    return payload


async def receive_board_from_server(reader) -> None:
    """
    Asynchronously receives, processes, and displays a game board/ scores update from the server. The function
    first gets the payload and then extracts the scores and board from the payload. Finally, the function prints out
    the scores and board to the console. This function is called after everytime the player moves or enters the Game
    command.
    The format of the payload is the first two unsigned shorts are the scores and the rest is the binary string
    representing the board.
    :param reader: A StreamReader for reading data from the server.
    """
    board_payload = await get_payload_from_server(reader)
    score_1, score_2 = unpack('!HH', board_payload[:4])
    board = board_payload[4:].decode()
    print(f'Player 1: {score_1}, Player 2: {score_2}')
    print(board)


async def receive_results_from_server(reader) -> None:
    """
    Asynchronously receives, processes, and displays game results sent by the server. The function first gets the
    payload and then extracts the binary string of the results and prints them to the console. This function is called
    when the client quits.
    :param reader: A StreamReader for reading data from the server.
    """
    results_payload = await get_payload_from_server(reader)
    results = results_payload.decode()
    print(results)


async def play_game(player_id: int, reader, writer) -> None:
    """
    Manages the gameplay experience for a player, allowing them to interact with the game server, send commands,
    and receive real-time game updates. The function first welcomes the client to the game and then continually
    prompts the client for commands. It then executes those commands until the client quits ths game.
    :param player_id: The unique identifier for the player.
    :param reader: A StreamReader for reading data from the server.
    :param writer: A StreamWriter for sending data to the server.
    """
    print(f"Welcome, your id is {player_id}")
    available_commands = {
        constants.UP: 0x24 if player_id == 1 else 0x28,
        constants.DOWN: 0x34 if player_id == 1 else 0x38,
        constants.LEFT: 0x44 if player_id == 1 else 0x48,
        constants.RIGHT: 0x64 if player_id == 1 else 0x68,
        constants.QUIT: 0x04 if player_id == 1 else 0x08,
        constants.GAME: 0xF4 if player_id == 1 else 0xF8
    }

    while True:
        command = input("Enter a command, (Q)uit, (G)ame, (U)p, (L)eft, (R)ight, (D)own: ").upper()
        if command in available_commands:
            writer.write(bytes([available_commands[command]]))
            if command == constants.QUIT:
                await receive_results_from_server(reader)
                break
            else:
                await receive_board_from_server(reader)


async def main():
    """
    The entry point of the game client program, responsible for  establishing a connection to the game server. The
    function first attempts to connect to the game server by receiving a client id. If the client received a valid
    client id it joins the game by entering the play_game function. All errors are caught and displayed.
    """
    try:
        reader, writer = await open_connection('127.0.0.1', constants.PORT)
        initial_response_bytes = await reader.readexactly(constants.HEADER_LENGTH)
        initial_response = unpack('!H', initial_response_bytes)[0]

        if initial_response == 0:
            print("Error, the game is full")
        else:
            player_id_bytes = await reader.readexactly(initial_response)
            player_id = unpack('!B', player_id_bytes)[0]
            await play_game(player_id, reader, writer)
    except Exception as e:
        print("An Unexpected Error Occurred")


run(main())
