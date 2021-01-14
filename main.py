import pygame
from Tetris import Tetris
from main_menu import main_menu

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Tetris game')
    music_game_over = pygame.mixer.Sound('game_over.mp3')
    width, height = 600, 600
    size = width, height
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 60
    exit_confirmed = False
    new_max = -10
    count_starts_tetris = 0
    while not exit_confirmed:
        pygame.mixer.music.load('Music_for_game.mp3')
        pygame.mixer.music.play(-1)
        music_win = pygame.mixer.Sound('music_win.mp3')
        pygame.mixer.music.set_volume(20)
        running = True
        game_started = False
        menu = main_menu(fps, screen)
        while not game_started and running:
            if new_max > 0 and count_starts_tetris > 0:
                out = open('stack_max.txt', 'w')
                out.write(str(new_max))
                out.close()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    exit_confirmed = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        menu.set_current_chose((menu.get_current_chose() - 1) % 2)
                    elif event.key == pygame.K_DOWN:
                        menu.set_current_chose((menu.get_current_chose() + 1) % 2)
                    elif event.key == pygame.K_SPACE:
                        if menu.get_current_chose() == 0:
                            game_started = True
                        else:
                            running = False
                            exit_confirmed = True
            menu.draw()
        stack_rating = 0
        inp = open('stack_max.txt')
        it_spic = []
        data = inp.readlines()
        max_rating = int(data[-1])
        inp.close()
        game = Tetris(fps, screen, stack_rating, max_rating, music_win)
        count_starts_tetris += 1
        while running:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    exit_confirmed = True
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
            if not game.running:
                pygame.mixer.music.stop()
                music_game_over.play()
                running = False
                new_max = game.get_max_rating_value()
                out = open('stack_max.txt', 'w')
                out.write(str(new_max))
                out.close()
                while not game.confirmed_lose:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                            game.confirm_lose()
    pygame.quit()
