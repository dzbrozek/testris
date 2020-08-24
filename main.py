import copy
import random
from typing import List

BOARD_WIDTH = 20
BOARD_HEIGHT = 20

blocks = [
    [
        [1, 1, 1, 1]
    ],
    [
        [1, 0],
        [1, 0],
        [1, 1]
    ],
    [
        [0, 1],
        [0, 1],
        [1, 1]
    ],
    [
        [0, 1],
        [1, 1],
        [1, 0]
    ],
    [
        [1, 1],
        [1, 1]
    ]
]


def display_board(game_board: 'GameBoard', block_board: 'BlockBoard') -> None:
    for row_index, row in enumerate(game_board):
        print('*', end='')
        for cell_index, cell in enumerate(game_board[row_index]):
            if block_board[row_index][cell_index]:
                print('x', end='')
            elif game_board[row_index][cell_index]:
                print('#', end='')
            else:
                print(' ', end='')
        print('*')
    print(''.join(['*'] * (len(game_board[0]) + 2)))


def make_move(available_moves: List[str]) -> str:
    messages = {
        'a': '• a (return): move piece left',
        'd': '• d (return): move piece right',
        'w': '• w (return): rotate piece counter clockwise',
        's': '• s (return) rotate piece clockwise'
    }
    while True:
        print('Make a move:')
        for move in available_moves:
            print(messages[move])
        move = input()
        if move not in available_moves:
            print('Invalid move')
            continue

        return move


def has_collision(game_board: 'GameBoard', block_board: 'BlockBoard') -> bool:
    for row_index in range(game_board.height):
        for cell_index in range(game_board.width):
            if game_board[row_index][cell_index] and block_board[row_index][cell_index]:
                return True
    return False


def get_available_moves(game_board: 'GameBoard', block_board: 'BlockBoard') -> List[str]:
    all_moves = ['a', 'd', 'w', 's']
    available_moves = []

    for move in all_moves:
        test_block_board = block_board.clone()
        try:
            test_block_board.move_block(move)
            if not has_collision(game_board, test_block_board):
                available_moves.append(move)
        except ValueError:
            pass

    return available_moves


class Block:

    def __init__(self, data: List[List[int]]):
        self.data = data

    @property
    def width(self) -> int:
        return len(self.data[0])

    @property
    def height(self) -> int:
        return len(self.data)

    def rotate(self, clockwise: bool = True) -> None:
        rotated = [[0] * len(self.data) for _ in range(len(self.data[0]))]
        for row_index, row in enumerate(self.data):
            for cell_index, cell in enumerate(self.data[row_index]):
                if clockwise:
                    rotated[cell_index][len(rotated[cell_index]) - (row_index + 1)] = self.data[row_index][cell_index]
                else:
                    rotated[len(rotated) - (cell_index + 1)][row_index] = self.data[row_index][cell_index]
        self.data = rotated

    def __getitem__(self, item: int) -> List[int]:
        return self.data[item]


class Board:

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.data = []

        self.clear_board()

    def __getitem__(self, item: int) -> List[int]:
        return self.data[item]

    def clear_board(self) -> None:
        self.data = [[False] * self.width for _ in range(self.height)]


class GameBoard(Board):

    def is_last_move(self, board: 'BlockBoard') -> bool:
        for row_index in range(self.height):
            for cell_index in range(self.width):
                if board[row_index][cell_index]:
                    if row_index == self.height - 1:
                        # end of the board reached
                        return True
                    if self.data[row_index + 1][cell_index]:
                        # block is adjacent to the block below
                        return True
        # this is last move if no other moves available
        return not len(get_available_moves(self, board))

    def merge_block(self, board: 'BlockBoard') -> None:
        for row_index in range(self.height):
            for cell_index in range(self.width):
                if board[row_index][cell_index]:
                    self[row_index][cell_index] = board[row_index][cell_index]


class BlockBoard(Board):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.block = None
        self.row_position = None
        self.cell_position = None

    def add_new_block(self) -> None:
        self.block = Block(random.choice(blocks))
        self.row_position = 0
        self.cell_position = random.randint(0, self.width - self.block.width)
        self.update_board()

    def update_board(self) -> None:
        self.clear_board()

        for row_index in range(self.block.height):
            for cell_index in range(self.block.width):
                if self.block[row_index][cell_index]:
                    data_row_index = self.row_position + row_index
                    data_cell_index = self.cell_position + cell_index
                    if not 0 <= data_row_index < self.height:
                        # block outside of board
                        raise ValueError('invalid move')
                    if not 0 <= data_cell_index < self.width:
                        # block outside of board
                        raise ValueError('invalid move')

                    self.data[data_row_index][data_cell_index] = \
                        self.block[row_index][cell_index]

    def move_block(self, move: str) -> None:
        if move == 'a':
            # move left
            self.cell_position -= 1
        elif move == 'd':
            # move right
            self.cell_position += 1
        elif move == 'w':
            # rotate piece counter clockwise
            self.block.rotate(clockwise=False)
        elif move == 's':
            # rotate piece clockwise
            self.block.rotate(clockwise=True)
        else:
            raise ValueError('Invalid move')

        self.row_position += 1

        self.update_board()

    def clone(self) -> 'BlockBoard':
        board = BlockBoard(width=self.width, height=self.height)
        board.block = Block(copy.deepcopy(self.block.data))
        board.row_position = self.row_position
        board.cell_position = self.cell_position
        board.data = copy.deepcopy(board.data)

        return board


def play() -> None:
    game_board = GameBoard(BOARD_WIDTH, BOARD_HEIGHT)
    block_board = BlockBoard(BOARD_WIDTH, BOARD_HEIGHT)
    block_board.add_new_block()

    while True:
        display_board(game_board, block_board)
        available_moves = get_available_moves(game_board, block_board)
        if not len(available_moves):
            print('No move available. Game is over')
            return

        move = make_move(available_moves)
        block_board.move_block(move)

        if game_board.is_last_move(block_board):
            game_board.merge_block(block_board)
            block_board.add_new_block()


if __name__ == '__main__':
    play()
