from Board import Board
from Piece import Piece
from shapes import shapes
#from Next_figure import Next_figure
import random
import pygame


class Tetris(Board):
    def __init__(self, fps):
        #Next_figure(fps)
        width = 12
        height = 20
        super().__init__(width, height, left=10, top=40, cell_size=26)
        self.count = 0
        self.spic_colors_act = ['red', 'blue', 'orange', 'brown', 'purple', 'green', 'yellow']
        self.fps = fps
        self.difficulty = 30
        self.border_color = pygame.Color('white')
        self.ACTIVE_PIECE = 1
        self.BLOCK = 11
        self.stack_active_piece_color = int(random.randint(0, 3))
        self.BLOCK_COLOR = pygame.Color('white')
        self.create_active_piece()
        self.render_active_piece()

    def render_cell(self, i, j, screen):
        x, y = self.get_cell_position(i, j)
        rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        val = self.board[i][j]
        if val == self.ACTIVE_PIECE:
            pygame.draw.rect(screen, self.spic_colors_act[self.stack_active_piece_color], rect)
        elif val == self.BLOCK:
            pygame.draw.rect(screen, self.BLOCK_COLOR, rect)
        else:
            pygame.draw.rect(screen, self.border_color, rect, width=self.border_width)

    def update(self):
        self.count += 1
        if self.count % (self.fps - self.difficulty) == 0:
            self.update_world()

    def update_world(self):
        if self.can_move(pygame.K_DOWN):
            self.remove_active_piece()
            self.active_piece.down()
            self.render_active_piece()
        else:
            self.active_piece_to_block()
            self.check_complete_lines()
            self.create_active_piece()
            self.render_active_piece()

    def active_piece_to_block(self):
        self.stack_active_piece_color += 1
        self.stack_active_piece_color %= 7
        shape = self.active_piece.get_shape()
        for i in range(self.active_piece.size):
            for j in range(self.active_piece.size):
                board_row = i + self.active_piece.row
                board_column = j + self.active_piece.column
                if self.is_valid_pos(board_row, board_column):
                    shape_val = int(shape[i][j])
                    if shape_val == self.ACTIVE_PIECE:
                        self.board[board_row][board_column] = self.BLOCK

    def check_complete_lines(self):
        for row in range(self.height):
            if self.board[row].count(self.BLOCK) == self.width:
                self.delete_line(row)

    def delete_line(self, index):
        for i in range(index, 0, -1):
            self.board[i] = self.board[i - 1]
        self.board[0] = [0] * self.width

    def render_active_piece(self):
        shape = self.active_piece.get_shape()
        for i in range(self.active_piece.size):
            for j in range(self.active_piece.size):
                board_row = i + self.active_piece.row
                board_column = j + self.active_piece.column
                if self.is_valid_pos(board_row, board_column):
                    shape_val = int(shape[i][j])
                    if shape_val == self.ACTIVE_PIECE:
                        self.board[board_row][board_column] = self.ACTIVE_PIECE

    def remove_active_piece(self):
        shape = self.active_piece.get_shape()
        for i in range(self.active_piece.size):
            for j in range(self.active_piece.size):
                board_row = i + self.active_piece.row
                board_column = j + self.active_piece.column
                if self.is_valid_pos(board_row, board_column):
                    shape_val = int(shape[i][j])
                    if shape_val == self.ACTIVE_PIECE:
                        self.board[board_row][board_column] = self.default_value

    def is_valid_pos(self, row, col):
        return 0 <= row < self.height and 0 <= col < self.width

    def get_random_shape(self):
        return random.choice(list(shapes.values()))

    def create_active_piece(self):
        #Next_figure(self.fps)
        self.active_piece = Piece(self.get_random_shape(), 0, 0)

    def can_move(self, direction):
        actions = {pygame.K_DOWN: self.active_piece.down, pygame.K_LEFT: self.active_piece.left,
                   pygame.K_RIGHT: self.active_piece.right, pygame.K_UP: self.active_piece.rotate}
        reverse_actions = {pygame.K_DOWN: self.active_piece.up, pygame.K_LEFT: self.active_piece.right,
                           pygame.K_RIGHT: self.active_piece.left, pygame.K_UP: self.active_piece.rotate_prev}
        result = True
        actions[direction]()
        shape = self.active_piece.get_shape()
        for i in range(self.active_piece.size):
            for j in range(self.active_piece.size):
                board_row = i + self.active_piece.row
                board_column = j + self.active_piece.column
                shape_val = int(shape[i][j])
                if not self.is_valid_pos(board_row, board_column) and shape_val == self.ACTIVE_PIECE:
                    result = False
                    break
                if not self.is_valid_pos(board_row, board_column):
                    continue
                board_val = self.board[board_row][board_column]
                if shape_val == self.ACTIVE_PIECE and board_val == self.BLOCK:
                    result = False
                    break
        reverse_actions[direction]()
        return result

    def move_action(self, action, direction):
        if self.can_move(direction):
            self.remove_active_piece()
            action()
            self.render_active_piece()

    def on_key_pressed(self, key):
        actions = {pygame.K_DOWN: self.active_piece.down, pygame.K_LEFT: self.active_piece.left,
                   pygame.K_RIGHT: self.active_piece.right, pygame.K_UP: self.active_piece.rotate}
        if key in actions:
            self.move_action(actions[key], key)
