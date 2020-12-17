import pygame
import os
import random

pygame.init()
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Wheel')
fps = 60
deg = 0
data = eval(open('user data.txt', 'r').read())


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


def rot_center(image, rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect, angle


clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

coefficients_image = load_image('Cof.png')
coefficients = pygame.sprite.Sprite(all_sprites)
coefficients.image = coefficients_image
coefficients.rect = coefficients.image.get_rect()
coefficients.rect.right = width + 40

new_deg_image = load_image('new.png')
new_deg = pygame.sprite.Sprite(all_sprites)
new_deg.image = new_deg_image
new_deg.rect = new_deg.image.get_rect()
new_deg.rect.center = width - 70, height // 2

hero_image = load_image('wheel4.png')
hero = pygame.sprite.Sprite(all_sprites)
hero.image = hero_image
hero.rect = hero.image.get_rect()
hero.rect.center = width // 2, height // 2
defhero_image = load_image('wheel4.png')
defhero = pygame.sprite.Sprite()
defhero.image = hero_image

arrow_image = load_image('arrow.png')
arrow = pygame.sprite.Sprite(all_sprites)
arrow.image = arrow_image
arrow.rect = arrow.image.get_rect()
arrow.rect.center = width // 2, height // 2 - 180

running = True
spin = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        key = pygame.key.get_pressed()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not spin:
            mous_x, mous_y = pygame.mouse.get_pos()
            if (mous_x in range(list(new_deg.rect)[0], list(new_deg.rect)[0] + list(new_deg.rect)[2])) and (mous_y in range(list(new_deg.rect)[1], list(new_deg.rect)[1] + list(new_deg.rect)[3])):
                hero.image, hero.rect, deg = rot_center(defhero.image, hero.rect, 0)
        if key[pygame.K_LEFT]:
            speed -= 1
        if key[pygame.K_RIGHT]:
            speed += 1
        if key[pygame.K_SPACE]:
            speed = 0
        if event.type == pygame.MOUSEBUTTONDOWN and (event.button in [4, 5])and not spin:
            deg = 0
            cof = random.choice([-1, 1])
            speed = random.randint(10, 25) * cof
            spin = True
    if spin:
        if (speed >= 0 and cof == 1) or (speed <= 0 and cof == -1):
            if speed < 5 and cof == 1 or speed > -5 and cof == -1:
                speed -= 0.03 * cof
            elif speed < 9 and cof == 1 or speed > -9 and cof == -1:
                speed -= 0.06 * cof
            else:
                speed -= 0.09 * cof
            if speed <= 0 and cof == 1 or speed >= 0 and cof == -1:
                spin = False
                print(deg)
            hero.image, hero.rect, deg = rot_center(defhero.image, hero.rect, (deg - speed) % 360)

    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()