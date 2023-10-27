#!/usr/bin/python3
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
        self.server = self.create_server_socket()
        self.num_connections = 0

    @staticmethod
    def create_server_socket() -> socket:
        """
        Creates and configures a TCP Socket to be used as the game server.
        :return: The Server Socket
        """
        s = socket(AF_INET, SOCK_STREAM)
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind((constants.HOST, constants.PORT))
        s.listen(MAX_PLAYERS)
        return s

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

    """--------------------- SENDING DATA TO CLIENT ---------------------"""

    def send_scores_to_client(self, client: socket) -> None:
        """
        Server ----> packet([length][score1 score2]) ----> Client
        :param client: The client connected to the game server.
        """
        player_1_score = self.game_board.find_player_by_name(PLAYER_ONE_NAME).get_score()
        player_2_score = self.game_board.find_player_by_name(PLAYER_TWO_NAME).get_score()

        packet = pack('!HH', player_1_score, player_2_score)
        packet_header = pack('!H', len(packet))
        client.sendall(packet_header + packet)

    def send_board_to_client(self, client: socket) -> None:
        """
        Server ----> packet([length][score1 score2 board]) ----> Client
        :param client: The client connected to the game server.
        """
        board = view.display(self.game_board)
        player_1_score = self.game_board.find_player_by_name(PLAYER_ONE_NAME).get_score()
        player_2_score = self.game_board.find_player_by_name(PLAYER_TWO_NAME).get_score()

        packet = pack('!HH', player_1_score, player_2_score) + board.encode()
        packet_header = pack('!H', len(packet))
        client.sendall(packet_header + packet)

    def send_results_to_client(self, client: socket) -> None:
        """
        Server ----> packet([length][results]) ----> Client
        :param client: The client socket connected to the game server.
        """
        results = self.game_board.get_results()

        packet = results.encode()
        packet_header = pack('!H', len(packet))
        client.sendall(packet_header + packet)

    """------------------------ HANDLING THREADS ------------------------"""

    def execute_client_command(self, client: socket, player: str, command: str) -> None:
        """
        Executes a clients command, updates the game state, and sends the results to the client.
        :param client: The client socket for communication.
        :param player: The player associated with the command.
        :param command: The command to be executed.
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

    def handle_client_thread(self, client: socket, client_id: int):
        """
        Handles communication and gameplay for a connected player.
        :param client: The client socket connected to the game server.
        :param client_id: The unique identifier for the player.
        """
        with client:
            client.sendall(pack('!HB', 1, client_id))  # Send Client their ID

            while True:
                player, command = self.parse_command_byte(client.recv(1))  # Get a byte from the client
                print(f'Player: {player}, Command: {command}')
                if command != 'Q':
                    self.execute_client_command(client, player, command)  # Execute the byte from the client
                else:
                    self.send_results_to_client(client)
                    self.num_connections -= 1
                    break

    """-------------------------- GAME DRIVER ---------------------------"""

    def start(self) -> None:
        """
        Starts the game server by accepting client connections and creating threads for each player
        connection. Game server accepts two concurrent connection and will send a packet containing 0
        if the game server is full.
        """
        while self.num_connections < MAX_PLAYERS:
            try:
                client, client_address = self.server.accept()
                print(f'Connected to client {client_address[0]}:{client_address[1]}')
                self.num_connections += 1
                Thread(target=self.handle_client_thread, args=(client, self.num_connections)).start()

            except ConnectionError:
                print("Error: Could not Establish a connection to the client.")
            except TimeoutError:
                print("Error: Connection to the client timed out.")
            except Exception as details:
                print("Error: An unexpected error occurred.")
                print(details)

        while True:  # If server is full, reject additional connections.
            try:
                client, client_address = self.server.accept()
                client.sendall(pack('!H', 0))
                client.close()
                print(f"{client_address[0]}:{client_address[1]} attempted to connect but was denied entry.")
            except Exception:
                continue
