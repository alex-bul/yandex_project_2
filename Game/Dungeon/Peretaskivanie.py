import pygame
import os
import random

pygame.init()
size = width, height = 1000, 1000
pygame.display.set_caption('Перетаскивание')
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
fps = 600
step = 80
running = True
x = 80
y = 114
my_name = 0


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
    def __init__(self, *group, x, y, name=f'my_{my_name}', sprite_name):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(*group)
        self.image = load_image(f'{sprite_name}.png')
        self.rect = self.image.get_rect()
        self.name = name
        self.rect.bottomleft = x, y
        self.def_rect = self.rect.bottomleft
        self.click = False
        self.sprite_name = sprite_name
        self.health = 1
        self.armor = 1
        self.damage = 1
        self.flag = False

    def sprite(self, state=None):
        if state == 1:
            self.image = load_image(f'{self.sprite_name}.png')
        elif state == 2:
            self.image = load_image(f'{self.sprite_name}_attack.png')
        else:
            self.image = load_image(f'{self.sprite_name}_death.png')

    def update(self, *args):
        if 'pos' in str(args[0]) and not self.health <= 0:
            if args[0].type == pygame.MOUSEBUTTONUP and args[0].button == 1 and self.rect.collidepoint(
                    args[0].pos) and self.click:
                self.click = False
                for i in args[1]:
                    if self.rect.colliderect(i.rect) and i.name != self.name and not i.health <= 0 and not self.flag:
                        self.flag = True
                        print('-------------------------')
                        print(f'{i.health} - {self.damage - (i.armor / 2)}')
                        print(f'health: {i.health}, armor: {i.armor}')
                        if (self.damage - (i.armor / 2)) > 0:
                            i.health -= self.damage - (i.armor / 2)

                        else:
                            i.health -= 1
                        if i.armor >= self.damage * 0.1:
                            i.armor -= self.damage * 0.1
                        print(f'health: {i.health}, armor: {i.armor}')
                self.rect.bottomleft = self.def_rect

            if (args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos)) or self.click:
                mous_x, mous_y = args[0].pos
                self.sprite(state=2)
                self.click = True
                self.flag = False
                self.rect.center = (mous_x, mous_y)

            else:
                self.sprite(state=1)

        if self.health <= 0:
            self.sprite()


class Assassin(Character):
    def __init__(self, x, y):
        Character.__init__(self, x=x, y=y, name=f'my_{my_name}', sprite_name='Assassin')
        self.health = 150
        self.damage = 40
        self.armor = 30


class Berserk(Character):
    def __init__(self, x, y):
        Character.__init__(self, x=x, y=y, name=f'my_{my_name}', sprite_name="berserk")
        self.health = 200
        self.damage = 80
        self.armor = 60


clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

heros = [Assassin(x=0, y=y)]

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
            my_name += 1
            if key[pygame.K_1]:
                a = Assassin(x=x, y=y)

            if key[pygame.K_2]:
                a = Berserk(x=x, y=y)

            x += step
            heros.append(a)
            all_sprites.add(heros)

        if key[pygame.K_LEFT] and len(heros) > 0 and not change:
            all_sprites.remove(heros)
            my_name -= 1
            heros = heros[:-1]
            x -= step
            all_sprites.add(heros)

        if key[pygame.K_SPACE]:
            for i in heros:
                i.sprite(2)

    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    all_sprites.update(event, heros)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
