import pygame
import sys
import os
import random

pygame.init()
screen = pygame.display.set_mode((1400, 800))
pygame.display.set_caption('Snake')


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["             THE SNAKE", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (1400, 800))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont("couriernew", 60)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return  # начинаем игру
        pygame.display.flip()


def end_screen():
    intro_text = ["              THE END", "",
                  "         Tap to restart"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (1400, 800))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont("couriernew", 60)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                main()  # начинаем игру
        pygame.display.flip()


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    try:
        image = pygame.image.load(fullname)
    except pygame.error as Message:
        print(Message)
        raise SystemExit(Message)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


print(load_level("level_1"))

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('stone.png')
}
player_image = load_image('snake1.png')
food_image = load_image('food.jpg')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        if tile_type == 'wall':
            wall_group.add(self)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Food(pygame.sprite.Sprite):
    def __init__(self):
        pos_x = random.choice(range(1400))
        pos_y = random.choice(range(800))
        super().__init__(food_group, all_sprites)
        self.image = food_image
        self.add(food_group)
        self.rect = pygame.Rect(pos_x, pos_y, tile_width, tile_height)


class Player(pygame.sprite.Sprite):
    size = 50, 50

    def __init__(self, pos):
        super().__init__(player_group)
        self.add(player_group)
        self.image = player_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(pos, Player.size)

    def update(self, x, y):
        if pygame.sprite.spritecollideany(self, wall_group) is None:
            self.rect = self.rect.move(x, y)


# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
food_group = pygame.sprite.Group()


def generate_level(level):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
    return x, y


def main():
    x1_change = 0
    y1_change = 0
    a = 0
    start_screen()
    running = True
    player = None
    food = None
    clock = pygame.time.Clock()
    while running:
        if player == None:
            generate_level(load_level("level_1"))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if player is None:
                    player = Player(event.pos)
                    food = Food()
            if player is not None:
                if pygame.sprite.spritecollideany(player, wall_group) is None:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                        x1_change = 0
                        x1_change -= 20
                        y1_change = 0
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                        y1_change = 0
                        y1_change -= 20
                        x1_change = 0
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                        y1_change = 0
                        y1_change += 20
                        x1_change = 0
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                        x1_change = 0
                        x1_change += 20
                        y1_change = 0
                if pygame.sprite.spritecollideany(player, wall_group):
                    player.kill()
                    food.kill()
                    end_screen()
                if pygame.sprite.spritecollideany(player, food_group):
                    a += 1
                    food.kill()
                    food = Food()
                    print('aaaaaaaaa')
            if a == 15:
                generate_level(load_level("level_2"))
                tiles_group.draw(screen)
                player_group.draw(screen)
                food_group.draw(screen)
                pygame.display.flip()
                a = 0
        all_sprites.draw(screen)
        all_sprites.update()
        tiles_group.draw(screen)
        player_group.draw(screen)
        food_group.draw(screen)
        player_group.update(y1_change, x1_change)
        score_font = pygame.font.SysFont("comicsansms", 35)
        value = score_font.render("Ваш счёт: " + str(a), True, pygame.Color('white'))
        screen.blit(value, [0, 0])
        clock.tick(10)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()