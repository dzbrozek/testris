import unittest

from main import Block, GameBoard, BlockBoard, has_collision


class BlockTest(unittest.TestCase):

    def test_rotate_clockwise(self):
        block = Block([
            [1, 0],
            [1, 0],
            [1, 1]
        ])

        block.rotate()
        assert block.data == [
            [1, 1, 1],
            [1, 0, 0]
        ]

        block.rotate()
        assert block.data == [
            [1, 1],
            [0, 1],
            [0, 1]
        ]

        block.rotate()
        assert block.data == [
            [0, 0, 1],
            [1, 1, 1]
        ]

        block.rotate()
        assert block.data == [
            [1, 0],
            [1, 0],
            [1, 1]
        ]

    def test_rotate_anticlockwise(self):
        block = Block([
            [0, 1],
            [0, 1],
            [1, 1]
        ])

        block.rotate(False)
        assert block.data == [
            [1, 1, 1],
            [0, 0, 1]
        ]

        block.rotate(False)
        assert block.data == [
            [1, 1],
            [1, 0],
            [1, 0]
        ]

        block.rotate(False)
        assert block.data == [
            [1, 0, 0],
            [1, 1, 1]
        ]

        block.rotate(False)
        assert block.data == [
            [0, 1],
            [0, 1],
            [1, 1]
        ]


class CommonTest(unittest.TestCase):

    def test_has_collision(self):
        game_board = GameBoard(width=4, height=4)
        game_board.data = [
            [0, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 1, 0, 0]
        ]
        block_board = BlockBoard(width=4, height=4)
        block_cases = [
            [
                [1, 1, 0, 0],
                [1, 1, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ], [
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0]
            ], [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 1],
                [0, 1, 1, 1]
            ]
        ]
        for case_index, case_data in enumerate(block_cases):
            with self.subTest(f'Case {case_index + 1}'):
                block_board.data = case_data
            self.assertTrue(has_collision(game_board, block_board))

    def test_has_no_collision(self):
        game_board = GameBoard(width=4, height=4)
        game_board.data = [
            [0, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 1, 0, 0]
        ]
        block_board = BlockBoard(width=4, height=4)
        block_cases = [
            [
                [0, 0, 1, 1],
                [0, 0, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ], [
                [1, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 0, 0]
            ], [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 1, 1, 1],
                [0, 0, 0, 1]
            ]
        ]
        for case_index, case_data in enumerate(block_cases):
            with self.subTest(f'Case {case_index + 1}'):
                block_board.data = case_data
            self.assertFalse(has_collision(game_board, block_board))

    def test_valid_block_move(self):
        moves = ['a', 'd', 'w', 's']
        for move in moves:
            with self.subTest(f'Move: {move}'):
                block = BlockBoard(width=5, height=5)
                block.cell_position = 1
                block.row_position = 0
                block.block = Block([
                    [1, 0],
                    [1, 0],
                    [1, 1]
                ])

                self.assertIsNone(block.move_block(move))

    def test_can_not_move_to_left(self):
        block = BlockBoard(width=5, height=5)
        block.cell_position = 0
        block.row_position = 0
        block.block = Block([
            [1, 1],
            [1, 1],
        ])

        with self.assertRaises(ValueError):
            block.move_block('a')

    def test_can_not_move_to_right(self):
        block = BlockBoard(width=5, height=5)
        block.cell_position = 0
        block.row_position = 4
        block.block = Block([
            [1, 1],
            [1, 1],
        ])

        with self.assertRaises(ValueError):
            block.move_block('a')

    def test_can_not_move_outside_of_board(self):
        block = BlockBoard(width=5, height=5)
        block.cell_position = 1
        block.row_position = 4
        block.block = Block([
            [1, 1],
            [1, 1],
        ])

        with self.assertRaises(ValueError):
            block.move_block('a')

    def test_can_not_rotate(self):
        block = BlockBoard(width=5, height=5)
        block.cell_position = 3
        block.row_position = 0
        block.block = Block([
            [0, 1],
            [0, 1],
            [1, 1]
        ])

        with self.assertRaises(ValueError):
            block.move_block('s')


if __name__ == "__main__":
    unittest.main()
