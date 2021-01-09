from AssetManager import assetManager
import pygame
import random
from game_config import config


class StartScreen:
    def __init__(self, fps, screen):
        self.fps = fps
        self.width, self.height = config.get_list_values('width', 'height')
        self.screen = screen
        self.animate = False
        self.timer = None
        self.render()

    def render(self, dt=None):
        self.draw_background()
        self.draw_text()
        if self.animate:
            self.timer += dt
            self.draw_animate()

    def draw_background(self):
        bg = pygame.transform.scale(assetManager.load_image('start_tetris.jpg'), (self.width, self.height))
        self.screen.blit(bg, (0, 0))

    def start_animate(self):
        self.timer = 0
        self.animate = True

    def draw_animate(self):
        for i in range(15000):
            self.screen.fill(pygame.Color('white'),
                             (random.random() * self.width,
                              random.random() * self.height, 1, 1))
        if self.timer > 2000:
            pass

    def draw_text(self):
        text_lines = ["Тетрис", "Нажмите любую клавишу"]
        offset_x, offset_y = 0, 0
        line_offset = 10
        color = pygame.Color('white')
        font_size = 40
        font = pygame.font.SysFont('comicsans', font_size)
        text_rendered_lines = []
        for text_line in text_lines:
            string_rendered = font.render(text_line, True, color)
            rect = string_rendered.get_rect()
            rect.x = offset_x
            rect.y = offset_y
            offset_y += rect.height + line_offset
            text_rendered_lines.append((string_rendered, rect))
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

    def on_event(self, event):
        if event.type == pygame.KEYUP:
            self.start_animate()

    def update(self):
        pass
