import pygame
import os

pygame.init()
size = width, height = 1000, 1000
pygame.display.set_caption('Перетаскивание')
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
fps = 6000
step = 100
running = True
click = False
position = (10, 20)
cursor_pos = 0
x = 0


class Assasin(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('Assassin2.png')
        self.state = load_image('Assassin2.png')
        self.attack = load_image('Assassin_attack.png')
        self.rect = self.image.get_rect()


class Berserk(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('berserk.png')
        self.state = load_image('berserk.png')
        self.attack = load_image('berserk_attack.png')
        self.rect = self.image.get_rect()


# pers = [Assasin(), Berserk()]


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


clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

g = [Assasin()]
print(g)
for i in g:
    print(list(i.rect.center)[0] + x, list(i.rect.center)[1])
    i.rect.center = [list(i.rect.center)[0] + x, list(i.rect.center)[1]]
    x += step

all_sprites.add(g)
key = pygame.key.get_pressed()
clock = pygame.time.Clock()
click_on = False
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
        if key[pygame.K_RIGHT] and (key[pygame.K_1] or key[pygame.K_2]) and not change:
            all_sprites.remove(g)
            if key[pygame.K_1]:
                a = Assasin()
            if key[pygame.K_2]:
                a = Berserk()
            print(a)
            a.rect.center = [list(a.rect.center)[0] + x, list(a.rect.center)[1]]
            x += step
            g.append(a)
            all_sprites.add(g)

        if key[pygame.K_LEFT] and len(g) > 0 and not change:
            all_sprites.remove(g)
            g = g[:-1]
            x -= step
            all_sprites.add(g)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] - position[0] < 100 and event.pos[1] - position[1] < 100 and not click_on:
                click_on = True
                cursor_pos = event.pos
            click = True
        if event.type == pygame.MOUSEBUTTONUP:
            click = False
            print(event.type)
            click_on = False
            position = (10, 20)
        if event.type == pygame.MOUSEMOTION:
            if click_on:
                position = (position[0] + event.pos[0] - cursor_pos[0], position[1] + event.pos[1] - cursor_pos[1])
                cursor_pos = event.pos
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or click:
            for i in g:
                i.image = i.attack
        else:
            for i in g:
                i.image = i.state
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, pygame.Color(0, 255, 0), (position[0], position[1], 100, 100))
    all_sprites.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
