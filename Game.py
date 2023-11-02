#!/usr/bin/python3

from asyncio import run, start_server, StreamReader, StreamWriter
from struct import pack
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Semaphore, Thread
from Board import Board
import view
import constants

# Game Variables
PLAYER_ONE_NAME = "1"
PLAYER_TWO_NAME = "2"
BOARD_LENGTH = 10
NUM_TREASURES = 10
MIN_TREASURE = 1
MAX_TREASURE = 5
MAX_PLAYERS = 2

# To prevent race conditions during gameplay.
COMMAND_LOCK = Semaphore()


class Game:
    """
    The Game class manages a treasure-hunting game server.
        - Creates a Board of Tiles populated with Treasure.
        - Sets up a TCP socket to accept connections represented as players.
        - Handles the player commands from the connections maintaining the flow of the game.
    """
    def __init__(self):
        """
        Initializes the Game instance by creating the game board, adding players to the board, and setting up
        the server socket.
        """
        self.game_board = Board(BOARD_LENGTH, NUM_TREASURES, MIN_TREASURE, MAX_TREASURE)
        self.game_board.add_player_to_game_board(PLAYER_ONE_NAME)
        self.game_board.add_player_to_game_board(PLAYER_TWO_NAME)

        self.num_connections = 0

    """------------------- RECEIVING DATA FROM CLIENT -------------------"""

    @staticmethod
    def get_player_from_byte(byte: bytes) -> str:
        """
        Byte from Server ----> Player Name
        :param byte: Byte from Server
        :return: Player Name
        """
        player_map = {                  # byte:        0110 10 00 -> Extract the 5th & 6th least significant bits
            0b01: PLAYER_ONE_NAME,      # & 0xC:       0000 10 00
            0b10: PLAYER_TWO_NAME       # >> 2:        __00 00 10
        }                               # player_bits: 10

        player_bits = (int.from_bytes(byte, byteorder='big') & 0xC) >> 2
        return player_map.get(player_bits, "ERROR")

    @staticmethod
    def get_command_from_byte(byte: bytes) -> str:
        """
        Byte from Server ----> Command Name
        :param byte: Byte from Server
        :return: Command Name
        """
        command_map = {         # byte:          0010 1000  -> Extract the 4 most significant bits
            0b0010: 'U',        # >> 4:          ____ 0010
            0b0100: 'L',        # command_bits:  0010
            0b0110: 'R',
            0b0011: 'D',
            0b0000: 'Q',
            0b1111: 'G'
        }
        command_bits = (int.from_bytes(byte, byteorder='big')) >> 4
        return command_map.get(command_bits, "ERROR")

    def parse_command_byte(self, byte: bytes) -> tuple[str, str]:
        """
        Byte from Server ----> [Player Name, Command Name]
        :param byte: Byte from Server
        :return: [Player Name, Command Name]
        """
        player = self.get_player_from_byte(byte)        # Byte Format: CCCC PP **
        command = self.get_command_from_byte(byte)          # C = Command Bit
        return player, command                              # P =  Player Bit

    async def send_board_to_client(self, writer: StreamWriter) -> None:
        board = view.display(self.game_board)
        player_1_score = self.game_board.find_player_by_name(PLAYER_ONE_NAME).get_score()
        player_2_score = self.game_board.find_player_by_name(PLAYER_TWO_NAME).get_score()

        packet = pack('!HH', player_1_score, player_2_score) + board.encode()
        packet_header = pack('!H', len(packet))
        writer.write(packet_header + packet)
        await writer.drain()

    async def send_results_to_client(self, writer: StreamWriter) -> None:
        results = self.game_board.get_results()

        packet = results.encode()
        packet_header = pack('!H', len(packet))
        writer.write(packet_header + packet)
        await writer.drain()

    async def execute_client_command(self, reader: StreamReader, writer: StreamWriter, player: str, command: str) -> None:
        if command in ['U', 'L', 'D', 'R']:
            self.game_board.move_player_on_board(player, command)
            await self.send_board_to_client(writer)
        elif command == 'G':
            await self.send_board_to_client(writer)
        elif command == 'ERROR':
            writer.write(b"Error in Command. Terminating Connection.")
            await writer.drain()
            writer.close()
            await writer.wait_closed()

    async def handle_client_coroutine(self, reader: StreamReader, writer: StreamWriter):
        print("Start")
        self.num_connections += 1
        client_id = self.num_connections
        writer.write(pack('!HB', 1, client_id))
        await writer.drain()

        while True:
            client_byte = await reader.readexactly(1)
            player, command = self.parse_command_byte(client_byte)
            if command != 'Q':
                await self.execute_client_command(reader, writer, player, command)  # Execute the byte from the client
            else:
                await self.send_results_to_client(writer)
                self.num_connections -= 1
                break

    """-------------------------- GAME DRIVER ---------------------------"""

    async def start(self) -> None:
        """
        Starts the game server by accepting client connections and creating threads for each player
        connection. Game server accepts two concurrent connection and will send a packet containing 0
        if the game server is full.
        """
        server = await start_server(self.handle_client_coroutine, constants.HOST, constants.PORT)
        await server.serve_forever()



