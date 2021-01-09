import pygame
from Tetris import Tetris

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Tetris game')
    width, height = 600, 600
    size = width, height
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 60
    running = True
    game = Tetris(fps, screen)
    main_font = pygame.font.SysFont('lucidasansroman', 60)
    title_tetris = main_font.render('TETRIS', True, pygame.Color('white'))
    """screen.blit(title_tetris, (330, 10))"""
    next_title = pygame.font.SysFont('lucidasansroman', 15)
    next_tetris = next_title.render('next figure:', True, pygame.Color('white'))
    screen.blit(next_tetris, (390, 90))
    """pygame.display.update()"""
    while running:
        screen.blit(title_tetris, (330, 10))
        screen.blit(next_tetris, (390, 90))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                game.on_key_pressed(event.key)
        screen.fill(pygame.Color('black'))
        game.render(screen)
        game.update()
        clock.tick(fps)
    pygame.quit()
