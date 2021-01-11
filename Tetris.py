from Board import Board
from Piece import Piece
from shapes import shapes
from Next_figure import Next_figure
from game_config import config
import random
import pygame


class Tetris(Board):
    def __init__(self, fps, screen):
        self.screen = screen
        self.running = True
        self.confirmed_lose = False
        self.stack_rating = 0
        main_font = pygame.font.SysFont('lucidasansroman', 60)
        self.title_tetris = main_font.render('TETRIS', True, pygame.Color('white'))
        screen.blit(self.title_tetris, (330, 10))
        next_title = pygame.font.SysFont('lucidasansroman', 15)
        self.next_tetris = next_title.render('next figure:', True, pygame.Color('white'))
        screen.blit(self.next_tetris, (390, 90))
        rating_title = pygame.font.SysFont('lucidasansroman', 15)
        self.rating_tetris = rating_title.render('current rating:', True, pygame.Color('white'))
        screen.blit(self.rating_tetris, (380, 190))
        rating_num = pygame.font.SysFont('lucidasansroman', 30)
        self.rating_display = rating_num.render(str(self.stack_rating), True, pygame.Color('yellow'))
        screen.blit(self.rating_display, (380, 220))
        width = 10
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
        self.next_piece = Piece([['00000', '00000', '00110', '01100', '00000']], 0, 0)
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
        self.display_next_figure()
        self.screen.blit(self.title_tetris, (330, 10))
        self.screen.blit(self.next_tetris, (390, 90))
        self.screen.blit(self.rating_tetris, (380, 190))
        self.screen.blit(self.rating_display, (410, 220))
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
            if self.check_for_lose():
                size = 100
                normal_size = 40
                color = pygame.Color('Orange')
                main_font = pygame.font.SysFont('Arial', size)
                font = pygame.font.SysFont('Arial', normal_size)
                text = ['Вы проиграли!', 'Нажмите любую кнопку чтобы выйти']
                rendered = [main_font.render(text[0], True, color), font.render(text[1], True, color)]
                rects = [rendered[0].get_rect(), rendered[1].get_rect()]
                width = max(rects[0].width, rects[1].width)
                height = 10 + rects[0].height + rects[1].height
                surface = pygame.Surface((width, height), pygame.SRCALPHA)
                rects[1].y += 110
                for i in range(2):
                    text = rendered[i]
                    rect = rects[i]
                    rect.x = width // 2 - rect.width // 2
                    surface.blit(text, rect)
                x = config.get_value('width') // 2 - width // 2
                y = config.get_value('height') // 2 - height // 2
                self.screen.blit(surface, pygame.Rect(x, y, width, height))
                self.running = False
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
        self.stack_rating = 100 + int(self.stack_rating)

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

    def display_next_figure(self):
        next_fig = Next_figure(self.next_piece.shape, self.stack_active_piece_color, self.screen)

    def create_active_piece(self):
        if len(self.next_piece.shape) < 2:
            self.active_piece = Piece(self.get_random_shape(), 0, 0)
            self.next_piece = Piece(self.get_random_shape(), 0, 0)
        else:
            self.active_piece = self.next_piece
            self.next_piece = Piece(self.get_random_shape(), 0, 0)

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

    def check_for_lose(self):
        for i in range(self.width):
            if self.board[1][i] == self.BLOCK:
                return True
        return False

    def confirm_lose(self):
        self.confirmed_lose = True
