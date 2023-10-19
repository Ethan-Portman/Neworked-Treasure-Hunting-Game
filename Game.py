#!/usr/bin/python3
import struct
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from Board import Board
import View

# Game Variables
PLAYER_ONE_NAME = "1"
PLAYER_TWO_NAME = "2"
BOARD_LENGTH = 5
NUM_TREASURES = 10
MIN_TREASURE = 1
MAX_TREASURE = 5

# Network Variables
HOST = ''
PORT = 12345


class Game:
    """
    The Game class facilitates a networked treasure-hunting game. It sets up a game board, manages player
    connections, processes player commands, and maintains the game flow.
    """
    def __init__(self):
        self.game_board = Board(BOARD_LENGTH, NUM_TREASURES, MIN_TREASURE, MAX_TREASURE)
        self.game_board.add_player_to_game_board(PLAYER_ONE_NAME)
        self.game_board.add_player_to_game_board(PLAYER_TWO_NAME)
        self.sock = self.create_tcp_socket()

    @staticmethod
    def create_tcp_socket() -> socket:
        """
        Create a TCP server socket to be used as the game server.
        :return: The created TCP server socket.
        """
        s = socket(AF_INET, SOCK_STREAM)
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        return s

    @staticmethod
    def get_player_from_byte(byte: bytes) -> str:
        """
        Extracts the player name from a byte received by the server.
        :param byte: The byte with the player name encoded.
        :return: The player name
        """
        player_map = {
            0b01: PLAYER_ONE_NAME,
            0b10: PLAYER_TWO_NAME
        }

        player_bits = (int.from_bytes(byte, byteorder='big') >> 2) & 0b00000011
        return player_map.get(player_bits, "ERROR")

    @staticmethod
    def get_command_from_byte(byte: bytes) -> str:
        """
        Extracts the command name from a byte received by the server.
        :param byte: The byte with the command name encoded.
        :return: The command name.
        """
        command_map = {
            0b0010: 'U',
            0b0100: 'L',
            0b0110: 'R',
            0b0011: 'D',
            0b0000: 'Q',
            0b1111: 'G'
        }
        command_bits = (int.from_bytes(byte, byteorder='big') & 0xF0) >> 4
        return command_map.get(command_bits, "ERROR")

    def start(self) -> None:
        """
        Initiates and manages a game loop, continually accepting player commands over a network,
        executing these commands, and progressing the game until all treasures are collected.
        """
        while self.game_board.num_treasures > 0:
            client_socket = self.establish_client_connection()
            with client_socket:
                command_byte = client_socket.recv(1)
                player, command = self.parse_command_byte(command_byte)
                self.execute_command(player, command, client_socket)
        self.end_game()

    def establish_client_connection(self) -> socket:
        """
        Establishes a network connection with the client for receiving bytes.
        :return: The Client Socket used for accepting command bytes.
        """
        client_socket, client_address = self.sock.accept()
        print(f'Client {client_address[0]}: {client_address[1]}')
        return client_socket

    def parse_command_byte(self, byte: bytes) -> tuple[str, str]:
        """
        Parses a command byte and extracts player and command names.
        :param byte: The byte containing player and command information.
        :return: A tuple with player name and command name.
        """
        player = self.get_player_from_byte(byte)
        command = self.get_command_from_byte(byte)
        return player, command

    def execute_command(self, player, command, sock: socket) -> None:
        """
        Executes the specified command, communicates with the client socket,
        and manages the game flow.
        :param player: The player associated with the command.
        :param command: The command to be executed.
        :param sock: The client socket for communication.
        """
        if command in ['U', 'L', 'D', 'R']:
            self.game_board.move_player_on_board(player, command)
            self.send_encoded_scores(sock)
        elif command == 'G':
            self.send_encoded_board(sock)
        elif command == 'Q':
            self.send_encoded_game_results(sock)
            self.end_game()
        elif command == 'ERROR':
            sock.sendall(b"Error in command. Terminating Connection.")
            self.game_board.quit_application()

    def send_encoded_scores(self, sock: socket) -> None:
        encoded_score_1 = struct.pack('!H', self.game_board.find_player_by_name(PLAYER_ONE_NAME).get_score())
        encoded_score_2 = struct.pack('!H', self.game_board.find_player_by_name(PLAYER_TWO_NAME).get_score())
        sock.sendall(encoded_score_1)
        sock.sendall(encoded_score_2)

    def send_encoded_board(self, sock: socket) -> None:
        sock.sendall(View.display(self.game_board).encode())

    def send_encoded_game_results(self, sock: socket) -> None:
        sock.sendall(self.game_board.get_results().encode())

    def end_game(self) -> None:
        self.game_board.quit_application()


