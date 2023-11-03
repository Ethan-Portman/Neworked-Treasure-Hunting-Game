#!/usr/bin/python3
from asyncio import start_server, StreamReader, StreamWriter
from struct import pack
from Board import Board
import view
import constants


class Game:
    """
    The Game class manages a treasure-hunting game server.
        - Creates a Board of Tiles populated with Treasure (Board.py).
        - Sets up a TCP Asynchronous Server to accept connections represented as players.
        - Handles the player commands Asynchronously from the connections maintaining the flow of the game.
    """
    def __init__(self):
        """
        Initializes the Game instance by creating the game board by instantiating the Board object.
        Adds Two players to the board.
        Num connections is 0 to start with because no connections have been accepted yet. The game can only support two
        connections.
        """
        self.game_board = Board(constants.BOARD_LENGTH, constants.NUM_TREASURES, constants.MIN_TREASURE, constants.MAX_TREASURE)
        self.game_board.add_player_to_game_board(constants.PLAYER_ONE_NAME)
        self.game_board.add_player_to_game_board(constants.PLAYER_TWO_NAME)
        self.num_connections = 0
        self.max_connections = 2

    """------------------- RECEIVING DATA FROM CLIENT -------------------"""

    @staticmethod
    def get_player_from_byte(byte: bytes) -> str:
        """
        Byte ----> Player Name
        :param byte: A byte with the 5th and 6h bits mapping to a player: ****PP**
        :return: Player Name that matches the 5th and 6th most significant bits in byte, "ERROR" if the bits
        do not map to a valid player.
        """
        player_map = {                            # byte:        0110 10 00
            0b01: constants.PLAYER_ONE_NAME,      # & 0xC:       0000 10 00
            0b10: constants.PLAYER_TWO_NAME       # >> 2:        __00 00 10
        }                                         # player_bits: 10

        player_bits = (int.from_bytes(byte, byteorder='big') & 0xC) >> 2
        return player_map.get(player_bits, "ERROR")

    @staticmethod
    def get_command_from_byte(byte: bytes) -> str:
        """
        Byte ----> Command Name
        :param byte: A byte with the 4 most significant bits mapping to a player: CCCC****
        :return: Command Name that matches the 4 most significant bits in byte, "ERROR" if ths bits
        do not map to a valid command.
        """
        command_map = {                     # byte:          0010 1000
            0b0010: constants.UP,           # >> 4:          ____ 0010
            0b0100: constants.LEFT,         # command_bits:  0010
            0b0110: constants.RIGHT,
            0b0011: constants.DOWN,
            0b0000: constants.QUIT,
            0b1111: constants.GAME,
        }
        command_bits = (int.from_bytes(byte, byteorder='big')) >> 4
        return command_map.get(command_bits, "ERROR")

    def parse_command_byte(self, byte: bytes) -> tuple[str, str]:
        """
        Byte from Server ----> [Player Name, Command Name]
        :param byte: A byte with command and player hard-coated in: CCCC PP ** (C = Command; P = Player)
        :return: (Player Name, Command Name) extracted from the byte.
        """
        player = self.get_player_from_byte(byte)
        command = self.get_command_from_byte(byte)
        return player, command

    """------------------- SENDING DATA TO CLIENT -------------------"""

    async def send_board_to_client(self, writer: StreamWriter) -> None:
        """
        Asynchronously sends the player scores and current game board state to a client.
        Prepares a data packet containing the following information:
          - Length of Packet as an Unsigned Short
          - Scores of both players, both as Unsigned Shorts
          - Current state of the game-board as a binary string.
        :param writer: The StreamWriter used for sending data to the specific client.
        """
        board = view.display(self.game_board)
        player_1_score = self.game_board.find_player_by_name(constants.PLAYER_ONE_NAME).get_score()
        player_2_score = self.game_board.find_player_by_name(constants.PLAYER_TWO_NAME).get_score()

        packet = pack('!HH', player_1_score, player_2_score) + board.encode()
        packet_header = pack('!H', len(packet))
        writer.write(packet_header + packet)
        await writer.drain()

    async def send_results_to_client(self, writer: StreamWriter) -> None:
        """
        Asynchronously sends the player scores to a client.
        Prepares a data packet containing the following information:
          - Length of Packet as an Unsigned Short
          - Scores of both players, both as Unsigned Shorts
        :param writer: The StreamWriter used for sending data to the specific client.
        """
        results = self.game_board.get_results()

        packet = results.encode()
        packet_header = pack('!H', len(packet))
        writer.write(packet_header + packet)
        await writer.drain()

    async def execute_client_command(self, writer: StreamWriter, player: str, command: str) -> None:
        """
        Asynchronously processes and executes a client command, updating the game state and responding accordingly.
        If the Command is a valid movement, it executes the movement and sends updates scores and board to client.
        If the Command is Game, it sends scores and board to client.
        If the Command is an error, it sends an error message and terminates the connection with the client.

        :param writer: The StreamWriter used for sending data to the specific client.
        :param player: The name of the player associated with the command.
        :param command: The command issued by the client.
        """
        if command in [constants.UP, constants.LEFT, constants.DOWN, constants.RIGHT]:
            self.game_board.move_player_on_board(player, command)
            await self.send_board_to_client(writer)
        elif command == constants.GAME:
            await self.send_board_to_client(writer)
        elif command == 'ERROR':
            writer.write(b"Error in Command. Terminating Connection.")
            await writer.drain()
            writer.close()
            await writer.wait_closed()

    async def manage_game_client(self, reader: StreamReader, writer: StreamWriter):
        """
        Asynchronous coroutine to manage a single client connection and handle game interactions between the client
        and the server. If the number of connections is 2 or greater the server rejects the connection by sending a
        0 as an unsigned short and closing the connection. If the server accepts the connection it then continuously
        waits for commands from the client and returns the results until the client enters the quit command.

        :param reader: The StreamReader used for reading data from the specific client.
        :param writer: The StreamWriter used for sending data to the specific client.
        """
        if self.num_connections >= self.max_connections:
            writer.write(pack('!H', 0))  # Reject the Connection
            return

        self.num_connections += 1
        client_id = self.num_connections
        writer.write(pack('!HB', 1, client_id))  # Send the Client their ID
        await writer.drain()

        while True:
            client_byte = await reader.readexactly(1)  # Wait for a command as a byte from the client
            player, command = self.parse_command_byte(client_byte)
            if command != constants.QUIT:
                await self.execute_client_command(writer, player, command)  # Execute the byte from the client
            else:
                await self.send_results_to_client(writer)  # Quit the game
                self.num_connections -= 1
                break

    """-------------------------- GAME DRIVER ---------------------------"""

    async def start(self) -> None:
        """
        Sets up a TCP asynchronous server to listen for client connections. When a client connects, it is
        managed by the 'manage_game_client' coroutine. If the maximum allowed number of connections is reached
        (2 players), the server will reject the connection and notify the client with a 0-length packet.

        This method is the entry point for starting and running the game server using asynchronous coroutines.
        If an error occurs during server setup or while serving clients, it is caught and an error message is printed,
        but the server continues serving.
        """
        try:
            server = await start_server(self.manage_game_client, constants.HOST, constants.PORT)
            await server.serve_forever()
        except Exception as e:
            print("An unexpected error has occured occurred.")
            print(e)



