#!/usr/bin/python3
from struct import pack, unpack
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Semaphore, Thread
from Board import Board
import View

# Game Variables
PLAYER_ONE_NAME = "1"
PLAYER_TWO_NAME = "2"
BOARD_LENGTH = 10
NUM_TREASURES = 10
MIN_TREASURE = 1
MAX_TREASURE = 5

# Network Variables
HOST = '127.0.0.1'
PORT = 12346
LOCKS = [Semaphore(), Semaphore()]
LOCKS[1].acquire()


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
        self.num_players = 0

    @staticmethod
    def create_tcp_socket() -> socket:
        """
        Create a TCP server socket to be used as the game server.
        :return: The created TCP server socket.
        """
        s = socket(AF_INET, SOCK_STREAM)
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(2)  # Allow for two players
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

        player_from_bits = (int.from_bytes(byte, byteorder='big') >> 2) & 0b00000011
        return player_map.get(player_from_bits, "ERROR")

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
        command_from_bits = (int.from_bytes(byte, byteorder='big') & 0xF0) >> 4
        return command_map.get(command_from_bits, "ERROR")

    def establish_client_connection(self) -> socket:
        """
        Establishes a network connection with the client for receiving bytes.
        :return: The Client Socket used for accepting command bytes.
        """
        client, client_address = self.sock.accept()
        print(f'Client {client_address[0]}: {client_address[1]}')
        return client

    def client_entry_point(self, client_id: int):
        client = self.establish_client_connection()
        with client:
            client.sendall(pack('!B', client_id))  # Send Client their Client ID
            while True:
                player, command = self.parse_command_byte(client.recv(1))
                print(f'Player: {player}, Command: {command}')
                self.execute_command(player, command, client)


    def start(self) -> None:
        """
        Initiates and manages a game loop, continually accepting player commands over a network,
        executing these commands, and progressing the game until all treasures are collected.
        """
        num_connections = 0
        thread_list = []
        while True:
            for i in range(2):
                thread_list.append(Thread(target=self.client_entry_point, args=(num_connections,)))
                thread_list[-1].start()
                num_connections += 1


    def parse_command_byte(self, byte: bytes) -> tuple[str, str]:
        """
        Parses a command byte and extracts player and command names.
        :param byte: The byte containing player and command information.
        :return: A tuple with player name and command name.
        """
        print(byte)
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
            self.send_encoded_scores(sock)
            self.send_encoded_board(sock)
        elif command == 'Q':
            self.send_encoded_game_results(sock)
            self.end_game()
        elif command == 'ERROR':
            sock.sendall(b"Error in command. Terminating Connection.")
            sock.close()

    def send_encoded_scores(self, sock: socket) -> None:
        score_size = pack('!B', 4)
        sock.sendall(score_size)
        sock.sendall(pack('!H', self.game_board.find_player_by_name(PLAYER_ONE_NAME).get_score()))
        sock.sendall(pack('!H', self.game_board.find_player_by_name(PLAYER_TWO_NAME).get_score()))

    def send_encoded_board(self, sock: socket) -> None:
        sock.sendall(View.display(self.game_board).encode())

    def send_encoded_game_results(self, sock: socket) -> None:
        sock.sendall(self.game_board.get_results().encode())

    def end_game(self) -> None:
        self.game_board.quit_application()


