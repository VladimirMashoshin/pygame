from Board import Board
from Piece import Piece
import pygame


class Next_figure(Board):
    def __init__(self, figure, color, screen):
        self.screen = screen
        width = 5
        height = 5
        self.ACTIVE_PIECE = 1
        self.spic_colors_act = ['red', 'blue', 'orange', 'brown', 'purple', 'green', 'yellow']
        self.next_figure = Piece(figure, 0, 0)
        self.color = color
        self.color += 1
        self.color %= 7
        super().__init__(width, height, left=350, top=70, cell_size=26)
        self.border_color = pygame.Color('white')
        self.render_next_piece()

    def render_cell(self, i, j, screen):
        x, y = self.get_cell_position(i, j)
        rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        val = self.board[i][j]
        if val == self.ACTIVE_PIECE:
            pygame.draw.rect(screen, pygame.Color('black'), rect)
        elif val == self.default_value:
            pygame.draw.rect(screen, pygame.Color(self.spic_colors_act[self.color]), rect)
            pygame.display.update()
        else:
            pygame.draw.rect(screen, self.border_color, rect, width=self.border_width)

    def is_valid_pos(self, row, col):
        return 0 <= row < self.height and 0 <= col < self.width

    def render_next_piece(self):
        shape = self.next_figure.get_shape()
        for i in range(self.next_figure.size):
            for j in range(self.next_figure.size):
                board_row = i + self.next_figure.row
                board_column = j + self.next_figure.column
                if self.is_valid_pos(board_row, board_column):
                    shape_val = int(shape[i][j])
                    if shape_val == self.ACTIVE_PIECE:
                        self.board[board_row][board_column] = self.default_value
                        self.render_cell(i, j, self.screen)
