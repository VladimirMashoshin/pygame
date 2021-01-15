from AnimatedSprite import AnimatedSprite
from AssetManager import assetManager
import pygame


class DrawSprite(AnimatedSprite):
    def __init__(self, walk, jump, die, screen):
        super().__init__(assetManager.load_image('anim_sprite.jpg'), 6, 6)
        self.walk = walk
        self.jump = jump
        self.die = die
        self.screen = screen
        self.game_over = False
        self.actions = {}
        self.actions['look'] = self.frames[26:32]
        self.actions['walk'] = self.frames[9:23]
        self.state = 'walk'
        if self.jump:
            self.state = 'look'
        elif self.walk:
            self.state = 'walk'
        self.cur_frame = self.frames.index(self.actions[self.state][0])
        self.counter = 0
        self.rect = self.rect.move(395, 305)

    def update(self):
        if self.game_over:
            return
        self.counter += 1
        if self.counter % 8 == 0:
            self.next_frame()
            if self.state == 'look':
                if self.cur_frame == 32:
                    self.walk = True
                    self.jump = False
                    anim = Animation(self.screen, True, False, False)
                    anim.update()
                else:
                    self.jump = True
            self.update_image()

    def update_image(self):
        self.image = self.frames[self.cur_frame]

    def get_state_frames(self):
        return self.actions[self.state]

    def next_frame(self):
        frames_count = len(self.get_state_frames())
        self.cur_frame += 1
        if self.cur_frame - self.frames.index(self.actions[self.state][0]) == frames_count and self.state != 'look':
            self.cur_frame = self.frames.index(self.actions[self.state][0])
            self.counter = 0
        elif self.cur_frame - self.frames.index(self.actions[self.state][0]) == frames_count and self.state == 'look':
            self.state = 'walk'
            self.cur_frame = self.frames.index(self.actions[self.state][0])
            self.counter = 0


class Animation(pygame.sprite.GroupSingle):
    def __init__(self, screen, walk=True, jump=False, die=False):
        self.walk = walk
        self.jump = jump
        self.die = die
        self.screen = screen
        super().__init__(DrawSprite(self.walk, self.jump, self.die, self.screen))
