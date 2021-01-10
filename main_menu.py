from AssetManager import assetManager
import pygame
from game_config import config


class main_menu:
    def __init__(self, fps, screen):
        self.fps = fps
        self.screen = screen
        self.width, self.height = config.get_list_values('width', 'height')
        self.current_chose = 0
        self.draw()

    def draw(self):
        self.draw_background()
        self.draw_text(self.current_chose)

    def draw_background(self):
        bg = pygame.transform.scale(assetManager.load_image('start_tetris.jpg'), (self.width, self.height))
        self.screen.blit(bg, (0, 0))

    def draw_text(self, current_chose):
        text_lines = ['Tetris', 'Управлениe: стрелки, Space', 'Играть', 'Выход']
        offset_x, offset_y = 0, 0
        line_offset = 10
        font_size = 40
        font_header_size = 80
        normal_font = pygame.font.SysFont('comicsans', font_size)
        header_font = pygame.font.SysFont('comicsans', font_header_size)
        color = pygame.Color('grey')
        highlited_color = pygame.Color('red')
        text_rendered_lines = []
        cur_line = 0
        for text_line in text_lines:
            if cur_line == 0:
                string_rendered = header_font.render(text_line, True, color)
            elif cur_line == current_chose + 2:
                string_rendered = normal_font.render(text_line, True, highlited_color)
            else:
                string_rendered = normal_font.render(text_line, True, color)
            rect = string_rendered.get_rect()
            rect.x = offset_x
            rect.y = offset_y
            offset_y += rect.height + line_offset
            text_rendered_lines.append((string_rendered, rect))
            cur_line += 1
        width = max(*text_rendered_lines, key=lambda x: x[1].width)[1].width
        height = offset_y
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        for text_line in text_rendered_lines:
            text, rect = text_line
            rect.x = width // 2 - rect.width // 2
            surface.blit(text, rect)
        x = self.width // 2 - width // 2
        y = self.height // 2 - height // 2
        self.screen.blit(surface, pygame.Rect(x, y, width, height))

    def on_event(self, game_started, running, event):
        pass
        # if event.type == pygame.QUIT:
        #     running = False
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_UP:
        #         self.current_chose = (self.current_chose - 1) % 2
        #     if event.key == pygame.K_DOWN:
        #         self.current_chose = (self.current_chose + 1) % 2
        #     if event.type == pygame.K_SPACE:
        #         pass

    def get_current_chose(self):
        return self.current_chose

    def set_current_chose(self, new):
        self.current_chose = new
