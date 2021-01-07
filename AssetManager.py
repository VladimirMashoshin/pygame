import os
import sys
import pygame


class AssetManager:
    def __init__(self):
        self.assets = {}

    def load_image(self, name, colorkey=None):
        if (name, colorkey) in self.assets:
            return self.assets[(name, colorkey)]

        fullname = os.path.join('data', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        self.assets[(name, colorkey)] = image
        return self.assets[(name, colorkey)]

    def load_level(self, filename):
        if (filename,) in self.assets:
            return self.assets[(filename,)]
        filename = os.path.join('data', filename)
        if not os.path.isfile(filename):
            print(f"Файл с уровнем '{filename}' не найден")
            sys.exit()
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        self.assets[(filename,)] = list(map(lambda x: x.ljust(max_width, '.'), level_map))
        return self.assets[(filename,)]


assetManager = AssetManager()