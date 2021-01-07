import pygame
from Tetris import Tetris
from StartScreen import StartScreen

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('')
    width, height = 800, 800
    size = width, height
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 60
    running = True
    game = StartScreen(fps)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                game.on_key_pressed(event.key)

        screen.fill(pygame.Color('black'))
        game.render(screen)
        game.update()
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
