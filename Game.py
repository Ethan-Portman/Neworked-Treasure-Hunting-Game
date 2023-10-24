#!/usr/bin/python3
from struct import pack, unpack
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Semaphore, Thread
from Board import Board
import View
import constants

# Game Variables
PLAYER_ONE_NAME = "1"
PLAYER_TWO_NAME = "2"
BOARD_LENGTH = 10
NUM_TREASURES = 10
MIN_TREASURE = 1
MAX_TREASURE = 5
MAX_PLAYERS = 2
COMMAND_LOCK = Semaphore()

class Game:
    """
    The Game class manages a multi-threaded treasure-hunting game server. It orchestrates the game's core functionality,
    including setting up the game board, handling player connections, processing player commands, and maintaining
    the game's progression.
    """
    def __init__(self):
        """
        Initializes the Game instance by creating the game board, adding players to the board, setting up the server
        socket, and keeping track of the number of connected players.
        """
        self.game_board = Board(BOARD_LENGTH, NUM_TREASURES, MIN_TREASURE, MAX_TREASURE)
        self.game_board.add_player_to_game_board(PLAYER_ONE_NAME)
        self.game_board.add_player_to_game_board(PLAYER_TWO_NAME)
        self.server = self.get_server_socket()
        self.num_connections = 0

    @staticmethod
    def get_server_socket() -> socket:
        """
        Creates and configures a TCP Socket to be used as the game server.
        :return: The created and configured TCP socket ready to accept connections.
        """
        s = socket(AF_INET, SOCK_STREAM)
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind((constants.HOST, constants.PORT))
        s.listen(MAX_PLAYERS)
        return s

    @staticmethod
    def get_player_from_byte(byte: bytes) -> str:
        """
        Extracts the player name from a byte received from the client.
        :param byte: The byte with the player name encoded.
        :return: The player name.
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
        Extracts the command name from a byte received by the client.
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

    def parse_command_byte(self, byte: bytes) -> tuple[str, str]:
        """
        Parses a command byte received from the client and extracts the  player and command names.
        :param byte: The byte containing player and command information.
        :return: A tuple containing player name and command name.
        """
        player = self.get_player_from_byte(byte)
        command = self.get_command_from_byte(byte)
        return player, command

    def send_scores_to_client(self, client: socket) -> None:
        """
        Sends the scores of both players to the client. It first sends the length of the packet
        followed by the packet containing the scores.
        :param client: The client socket connected to the game server.
        """
        player_1_score = self.game_board.find_player_by_name(PLAYER_ONE_NAME).get_score()
        player_2_score = self.game_board.find_player_by_name(PLAYER_TWO_NAME).get_score()

        packet = pack('!HH', player_1_score, player_2_score)
        client.sendall(pack('!H', len(packet)))
        client.sendall(packet)

    def send_board_to_client(self, client: socket) -> None:
        """
        Sends both the scores and the board to the client. It first sends the length of the
        packet followed by the packet containing the scores and board.
        :param client: The client socket connected to the game server.
        """
        board = View.display(self.game_board)
        player_1_score = self.game_board.find_player_by_name(PLAYER_ONE_NAME).get_score()
        player_2_score = self.game_board.find_player_by_name(PLAYER_TWO_NAME).get_score()

        packet = pack('!HH', player_1_score, player_2_score) + board.encode()
        client.sendall(pack('!H', len(packet)))
        client.sendall(packet)

    def send_results_to_client(self, client: socket) -> None:
        """
        Sends the game results to the client. It first sends the length of the packet followed
        by the packet containing the results.
        :param client: The client socket connected to the game server.
        """
        results = self.game_board.get_results()

        packet = results.encode()
        client.sendall(pack('!H', len(packet)))
        client.sendall(packet)

    def execute_client_command(self, client: socket, player: str, command: str) -> None:
        """
        Executes a client command, updates the game state, and communicates with
        the client.
        :param player: The player associated with the command.
        :param command: The command to be executed.
        :param sock: The client socket for communication.
        """
        global COMMAND_LOCK
        if command in ['U', 'L', 'D', 'R']:
            with COMMAND_LOCK:
                self.game_board.move_player_on_board(player, command)
            self.send_board_to_client(client)
        elif command == 'G':
            self.send_board_to_client(client)
        elif command == 'ERROR':
            client.sendall(b"Error in command. Terminating Connection.")
            client.close()

    def handle_player_thread(self, client: socket, client_id: int):
        """
        Handles communication and gameplay for a connected player.
        :param client: The client socket connected to the game server.
        :param client_id: The unique identifier for the player.
        """
        with client:
            client.sendall(pack('!H', 1))
            client.sendall(pack('!B', client_id))
            while True:
                player, command = self.parse_command_byte(client.recv(1))
                print(f'Player: {player}, Command: {command}')
                if command == 'Q':
                    self.send_results_to_client(client)
                    break
                else:
                    self.execute_client_command(client, player, command)

    def start(self) -> None:
        """
        Starts the game server by accepting client connections and creating threads for player interaction.
        """
        player_threads = []
        player_count = 0

        while player_count < 2:
            client, client_address = self.server.accept()
            player_count += 1
            print(f'Connected to client {client_address[0]}:{client_address[1]}')

            player_thread = Thread(target=self.handle_player_thread, args=(client, player_count))
            player_threads.append(player_thread)
            player_thread.start()

        # If there are more than two players, reject additional connections
        while True:
            client, _ = self.server.accept()
            client.sendall(pack('!H', 0))
            client.close()







