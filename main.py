import pygame
from Tetris import Tetris
from StartScreen import StartScreen

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Tetris game')
    width, height = 600, 600
    size = width, height
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 60
    running = True
    game_started = False
    game = StartScreen(fps, screen)
    """game = Tetris(fps, screen)"""
    while running:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if not game_started:
                    game = Tetris(fps, screen)
                    game_started = True
                game.on_key_pressed(event.key)
        screen.fill(pygame.Color('black'))
        game.render(screen)
        game.update()
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
