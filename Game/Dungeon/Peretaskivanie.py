import pygame
import os

pygame.init()
size = width, height = 1000, 1000
pygame.display.set_caption('Перетаскивание')
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
fps = 120
step = 80
running = True
x = 80


def load_image(name, color_key=None):
    fullname = os.path.join('Res', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Character(pygame.sprite.Sprite):
    def __init__(self, *group, x, y, name):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(*group)
        self.image = load_image(f'{name}.png')
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y
        self.def_rect = self.rect.copy()
        self.click = False
        self.name = name
        self.health = 0
        self.armor = 0
        self.damage = 0

    def sprite(self, state=None):
        if state == 1:
            self.image = load_image(f'{self.name}.png')
        elif state == 2:
            self.image = load_image(f'{self.name}_attack.png')
        else:
            self.image = load_image(f'{self.name}_death.png')

    def update(self, *args):
        if 'pos' in str(args[0]):
            if args[0].type == pygame.MOUSEBUTTONUP and args[0].button == 1:
                self.click = False
                # self.rect = self.def_rect.copy()

            if (args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos)) or self.click:
                mous_x, mous_y = args[0].pos
                self.sprite(state=2)
                self.click = True
                self.rect.center = (mous_x, mous_y)

            else:
                self.sprite(state=1)


class Assassin(Character):
    def __init__(self, x, y):
        Character.__init__(self, x=x, y=y, name='Assassin')


class Berserk(Character):
    def __init__(self, x, y):
        Character.__init__(self, x=x, y=y, name="berserk")


clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

heros = [Assassin(x=0, y=0)]

# for i in heros:
#     print(list(i.rect.center)[0] + x, list(i.rect.center)[1])
#     i.rect.center = [list(i.rect.center)[0] + x, list(i.rect.center)[1]]
#     x += step

all_sprites.add(heros)
key = pygame.key.get_pressed()
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        last = (key[pygame.K_RIGHT], key[pygame.K_1], key[pygame.K_2], key[pygame.K_LEFT])
        key = pygame.key.get_pressed()

        if last == (key[pygame.K_RIGHT], key[pygame.K_1], key[pygame.K_2], key[pygame.K_LEFT]):
            change = True
        else:
            change = False

        if event.type == pygame.QUIT:
            running = False

        if key[pygame.K_RIGHT] and (key[pygame.K_1] or key[pygame.K_2]) and not change and len(heros) < 4:
            all_sprites.remove(heros)
            if key[pygame.K_1]:
                a = Assassin(x=x, y=0)

            if key[pygame.K_2]:
                a = Berserk(x=x, y=0)

            x += step
            heros.append(a)
            all_sprites.add(heros)

        if key[pygame.K_LEFT] and len(heros) > 0 and not change:
            all_sprites.remove(heros)
            heros = heros[:-1]
            x -= step
            all_sprites.add(heros)

        if key[pygame.K_SPACE]:
            for i in heros:
                i.sprite(2)

    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    all_sprites.update(event)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
