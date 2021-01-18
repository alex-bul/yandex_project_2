import pygame
import os
import random
import sqlite3

pygame.init()
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Wheel')
fps = 60
deg = 0
bet = 100
summ = 100
chose = ''
data = eval(open('user data.txt', 'r').read())
coin = data[-1]


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


def results():
    global coin, chose, deg
    if ((0 <= deg <= 25.5) or (77 <= deg <= 128.5) or (180 <= deg <= 231.5) or (
            334.5 <= deg <= 360)) and chose == 'Black':
        coin += bet * 2
    elif (283 <= deg <= 334.5) and chose == 'Green':
        coin += bet * 5
    elif ((25.5 <= deg <= 77) or (128.5 <= deg <= 180) or (231.5 <= deg <= 283)) and chose == 'Red':
        coin += bet * 2
    update_data_base()


def update_data_base():
    con = sqlite3.connect("Res/data.db")
    cur = con.cursor()
    cur.execute(f"""UPDATE data SET score = '{coin}' WHERE login = '{data[2]}'""")
    result = list(cur.execute(f"""SELECT * FROM data where login = '{data[2]}'""").fetchone())
    with open('user data.txt', 'w') as f:
        f.write(str(result))
    con.commit()
    con.close()


def draw(screen, view, x, y, cent, size=50):
    font = pygame.font.Font(None, size)
    text = font.render(view, True, (0, 0, 0))
    if cent:
        text_x = x - text.get_width() // 2
        text_y = y - text.get_height() // 2
    else:
        text_x = x
        text_y = y

    screen.blit(text, (text_x, text_y))


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

black_image = load_image('black.png')
black = pygame.sprite.Sprite(all_sprites)
black.image = black_image
black.rect = black.image.get_rect()
black.rect.center = width - 70 * 2 - 20, height // 2

red_image = load_image('red.png')
red = pygame.sprite.Sprite(all_sprites)
red.image = red_image
red.rect = red.image.get_rect()
red.rect.center = black.rect.center[0] - 90, black.rect.center[1]

green_image = load_image('green.png')
green = pygame.sprite.Sprite(all_sprites)
green.image = green_image
green.rect = green.image.get_rect()
green.rect.center = red.rect.center[0] - 90, red.rect.center[1]

add_bet_image = load_image('+.png')
add_bet = pygame.sprite.Sprite(all_sprites)
add_bet.image = add_bet_image
add_bet.rect = add_bet.image.get_rect()
add_bet.rect.center = red.rect.center[0] - 90, red.rect.center[1] + 100

deduct_bet_image = load_image('-.png')
deduct_bet = pygame.sprite.Sprite(all_sprites)
deduct_bet.image = deduct_bet_image
deduct_bet.rect = deduct_bet.image.get_rect()
deduct_bet.rect.center = add_bet.rect.center[0] + 90, add_bet.rect.center[1]

add_sum_image = load_image('+.png')
add_sum = pygame.sprite.Sprite(all_sprites)
add_sum.image = add_sum_image
add_sum.rect = add_sum.image.get_rect()
add_sum.rect.center = add_bet.rect.center[0], add_bet.rect.center[1] + 130

deduct_sum_image = load_image('-.png')
deduct_sum = pygame.sprite.Sprite(all_sprites)
deduct_sum.image = deduct_sum_image
deduct_sum.rect = deduct_sum.image.get_rect()
deduct_sum.rect.center = add_sum.rect.center[0] + 90, add_sum.rect.center[1]

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
            for i in [new_deg, black, red, green, add_bet, deduct_bet, add_sum, deduct_sum]:
                if (mous_x in range(list(i.rect)[0], list(i.rect)[0] + list(i.rect)[2])) and (
                        mous_y in range(list(i.rect)[1], list(i.rect)[1] + list(i.rect)[3])):
                    centre = i.rect.center
                    print(centre)
                    if centre == (1130, 400) and deg != 0:
                        print('deg = 0')
                        coin -= 10
                        hero.image, hero.rect, deg = rot_center(defhero.image, hero.rect, 0)
                    elif centre == (1040, 400):
                        chose = 'Black'
                    elif centre == (950, 400):
                        chose = 'Red'
                    elif centre == (860, 400):
                        chose = 'Green'
                    elif centre == (860, 500):
                        bet += summ
                    elif centre == (950, 500) and summ < bet:
                        bet -= summ
                    elif centre == (860, 630):
                        summ += 10
                    elif centre == (950, 630) and summ >= 10:
                        summ -= 10

        if key[pygame.K_LEFT]:
            speed -= 1
        if key[pygame.K_RIGHT]:
            speed += 1
        if key[pygame.K_SPACE]:
            speed = 0
        if event.type == pygame.MOUSEBUTTONDOWN and (
                event.button in [4, 5]) and not spin and chose != '' and bet <= coin:
            deg = 0
            cof = random.choice([-1, 1])
            speed = random.randint(10, 25) * cof
            coin -= bet
            spin = True
            update_data_base()
    if spin:
        if (speed >= 0 and cof == 1) or (speed <= 0 and cof == -1):
            if speed < 5 and cof == 1 or speed > -5 and cof == -1:
                speed -= 0.03 * cof
            elif speed < 9 and cof == 1 or speed > -9 and cof == -1:
                speed -= 0.06 * cof
            else:
                speed -= 0.09 * cof
            if speed <= 0 and cof == 1 or speed >= 0 and cof == -1:
                results()
                spin = False
                print(deg)
            hero.image, hero.rect, deg = rot_center(defhero.image, hero.rect, (deg - speed) % 360)

    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    clock.tick(fps)
    draw(screen, view=f'You Chose: {chose}', x=825, y=290, cent=False, size=40)
    draw(screen, view=f'You Bet: {bet}', x=825, y=325, cent=False, size=40)
    draw(screen, view=f'Sum to change: {summ}', x=825, y=550, cent=False, size=40)
    draw(screen, view=f'You Coin: {coin}', x=width // 2, y=30, cent=True, size=50)
    pygame.display.flip()
pygame.quit()
