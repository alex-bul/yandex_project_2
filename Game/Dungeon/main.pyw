import os
import random
import time
import pygame
from os import path
import sys
import sqlite3

guest = False
os.chdir('Game\\Dungeon\\')

try:
    coin, login1, login2, *argss = sys.argv[1:]
except:
    guest = True
print(sys.argv[1:])

pygame.init()
size = width, height = 1920, 1080  # Размер окна
pygame.display.set_caption('Dungeon')
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
rounds = 0
fps = 600  # Отклик
step = 80  # Пробел между персонажами
running = True
player_1_x = width // 2 - 200  # Координата первого персонажа
player_2_x = width // 2 + 150
y = 400  # Отступ от верха экрана
player_1_name = 0  # Номер персонажа
player_2_name = 0
player_1_sum_health = 0
player_2_sum_health = 0
enter = False
end_change = False
end_game = False
win = ''


# Функция загрузки изображений
def load_image(name, color_key=None, scale=None):
    fullname = path.join('Res', name)
    try:
        image = pygame.image.load(fullname)
        if scale:
            image = pygame.transform.scale(image, scale)
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


# Шанс попадания
def chance(rate=50):
    res = random.randint(0, 100)
    print(res)
    rate = 100 - rate
    if rate == 50:
        return random.choice([0, 1])
    if res >= rate:
        return 1 * random.gauss(1, 0.2)
    else:
        return 0


# Отрисовка текста
def draw(screen, view, x, y, cent, size=50, color=None):
    set_color = (0, 0, 0)

    if color == 'Green':
        set_color = (0, 255, 55)
    elif color == 'Yellow':
        set_color = (248, 252, 45)
    elif color == 'Red':
        set_color = (255, 50, 50)

    font = pygame.font.Font(None, size)
    text = font.render(view, True, set_color)
    if cent:
        text_x = x - text.get_width() // 2
        text_y = y - text.get_height() // 2
    else:
        text_x = x
        text_y = y

    screen.blit(text, (text_x, text_y))


def update_data_base(winner, loser):
    con = sqlite3.connect("..//..//Res/data.db")
    cur = con.cursor()
    cur.execute(f"""UPDATE data SET score = score + '{coin}' WHERE login = '{winner}'""")
    cur.execute(f"""UPDATE data SET score = score - '{coin}' WHERE login = '{loser}'""")
    result = list(cur.execute(f"""SELECT * FROM data where login = '{winner}'""").fetchone())
    with open('..//..//user data.txt', 'w') as f:
        f.write(str(result))
    con.commit()
    con.close()


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = load_image(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


# Класс персонажа
class Character(pygame.sprite.Sprite):
    def __init__(self, *group, x, y, name=f'my_{player_1_name}', sprite_name):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(*group)
        if 'player_2' in name:
            self.motion = [1, 1.5]
        else:
            self.motion = [0, 0.5]
        self.scale = None
        self.chance = 0  # Дефолтный шанс попадения
        self.image = load_image(f'{sprite_name}.png', scale=self.scale)  # Загрузка изображения
        self.rect = self.image.get_rect()
        self.name = name  # Имя персонажа
        self.rect.bottomleft = x, y  # Положение спрайта
        self.def_rect = self.rect.bottomleft  # Стандартное положение
        self.click = False
        self.is_death = False
        self.sprite_name = sprite_name
        self.health = 1  # Количество Здоровья
        self.def_health = self.health
        self.armor = 1  # Количество Брони
        self.damage = 1  # Количество Размер урона
        self.flag = False

    # Смена спрайта
    def sprite(self, state=None):
        if state == 1:
            self.image = load_image(f'{self.sprite_name}.png', scale=self.scale)
        elif state == 2:
            self.image = load_image(f'{self.sprite_name}_attack.png', scale=self.scale)
        else:
            self.image = load_image(f'{self.sprite_name}_death.png', scale=self.scale)
            self.health = 0

        if 'player_2' in self.name:
            self.image = pygame.transform.flip(self.image, True, False)

    # Обновление действий с персонадами
    def update(self, *args):
        global rounds, end_change
        if 'pos' in str(args[0]) and not self.health <= 0 and rounds % 2 in self.motion and not end_game:
            if args[0].type == pygame.MOUSEBUTTONUP and args[0].button == 1 and self.rect.collidepoint(
                    args[0].pos) and self.click:
                self.click = False

                for i in args[1]:
                    if self.rect.colliderect(i.rect) and i.name != self.name and not i.health <= 0 and not self.flag \
                            and self.name[:-1] != i.name[:-1]:
                        if self.sprite_name == 'Assassin':
                            rounds -= 0.5
                        end_change = True
                        self.flag = True
                        print('-------------------------')
                        res = chance(self.chance)
                        print(f'{i.health} - {self.damage - (i.armor / 2)}')
                        print(f'health: {i.health}, armor: {i.armor}')
                        if res == 0:
                            draw(screen, view='Miss', x=i.rect.center[0], y=i.rect.center[1], cent=True, size=50,
                                 color='Red')
                            pygame.display.flip()
                            time.sleep(0.5)
                        else:
                            draw(screen, view=str(-int(self.damage - (i.armor / 2) * res)), x=i.rect.center[0],
                                 y=i.rect.center[1], cent=True, size=50, color='Red')

                            pygame.display.flip()
                            time.sleep(0.5)
                        if (self.damage - (i.armor / 2)) * res > 0:
                            i.health -= int(self.damage - (i.armor / 2) * res)

                        else:
                            i.health -= int(1 * res)
                        if i.armor >= int(self.damage * 0.1 * res):
                            i.armor -= int(self.damage * 0.1 * res)
                        print(f'health: {i.health}, armor: {i.armor}')
                        rounds += 1
                self.rect.bottomleft = self.def_rect

            if (args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos)) or self.click:
                mous_x, mous_y = args[0].pos
                self.sprite(state=2)
                self.click = True
                self.flag = False
                self.rect.center = (mous_x, mous_y)

            else:
                self.sprite(state=1)

        # Проверка на смерть
        if self.health <= 0 and not self.is_death:
            self.sprite()
            self.is_death = True
            self.rect = self.image.get_rect()
            self.rect.bottomleft = self.def_rect


# Класс Ассасина
class Assassin(Character):
    def __init__(self, x, y, name=f'None'):
        Character.__init__(self, x=x, y=y, name=name, sprite_name='Assassin')
        self.chance = 80
        self.health = 150
        self.def_health = self.health
        self.damage = 35
        self.armor = 37


# Класс Берсерка
class Berserk(Character):
    def __init__(self, x, y, name=f'None'):
        Character.__init__(self, x=x, y=y, name=name, sprite_name="berserk")
        self.chance = 50
        self.health = 175
        self.def_health = self.health
        self.damage = 65
        self.armor = 60


clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
BackGround = Background('background.png', [0, 0])

# Изначальные игрои
hero_first_player = [Assassin(x=player_1_x, y=y, name=f'player_1_{player_1_name}')]
hero_second_player = [Assassin(x=player_2_x, y=y, name=f'player_2_{player_2_name}')]
player_1_x -= step
player_2_x += step

all_sprites.add(hero_first_player)
all_sprites.add(hero_second_player)
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

        if not player_1_sum_health and not player_2_sum_health:
            change = False

        if event.type == pygame.QUIT:
            running = False

        if key[pygame.K_RETURN]:
            enter = True

        # Добавление персонажей
        if (key[pygame.K_RIGHT] and (key[pygame.K_1] or key[pygame.K_2]) and not change and len(
                hero_first_player) < 4) and not enter and not end_change:
            all_sprites.remove(hero_first_player)
            player_1_name += 1
            if key[pygame.K_1]:
                a = Assassin(x=player_1_x, y=y, name=f'player_1_{player_1_name}')  # Добавить Ассасина

            elif key[pygame.K_2]:
                a = Berserk(x=player_1_x, y=y, name=f'player_1_{player_1_name}')  # Добавить Берсерка

            player_1_x -= step
            hero_first_player.append(a)
            all_sprites.add(hero_first_player)

        elif (key[pygame.K_RIGHT] and (key[pygame.K_1] or key[pygame.K_2]) and not change and len(
                hero_second_player) < 4) and enter and not end_change:

            all_sprites.remove(hero_second_player)
            player_2_name += 1
            if key[pygame.K_1]:
                a = Assassin(x=player_2_x, y=y, name=f'player_2_{player_2_name}')  # Добавить Ассасина

            elif key[pygame.K_2]:
                a = Berserk(x=player_2_x, y=y, name=f'player_2_{player_2_name}')  # Добавить Берсерка

            player_2_x += step
            hero_second_player.append(a)
            all_sprites.add(hero_second_player)

        if (key[pygame.K_LEFT] and len(
                hero_first_player) > 0 and not change) and not enter and not end_change:  # Убрать последнего персонажа
            all_sprites.remove(hero_first_player)
            player_1_name -= 1
            hero_first_player = hero_first_player[:-1]
            player_1_x += step
            all_sprites.add(hero_first_player)

        elif (key[pygame.K_LEFT] and len(hero_second_player) > 0 and not change) and enter and not end_change:
            all_sprites.remove(hero_second_player)
            player_2_name -= 1
            hero_second_player = hero_second_player[:-1]
            player_2_x -= step
            all_sprites.add(hero_second_player)

    screen.fill((255, 255, 255))
    screen.blit(BackGround.image, BackGround.rect)
    all_sprites.draw(screen)
    all_sprites.update(event, hero_first_player + hero_second_player)

    player_1_sum_health, player_2_sum_health = 0, 0
    for i in hero_first_player + hero_second_player:  # Отрисовка здоровья
        if 'player_2' not in i.name:
            player_1_sum_health += i.health
        else:
            player_2_sum_health += i.health
        if i.def_health * 0.75 <= i.health <= i.def_health:
            color = 'Green'
        elif i.def_health * 0.50 <= i.health <= i.def_health * 0.75:
            color = 'Yellow'
        else:
            color = 'Red'
        draw(screen=screen, view=str(i.health), x=i.rect.center[0], y=i.rect.bottom - 90, cent=True, size=40,
             color=color)
    if player_1_sum_health == 0 or player_2_sum_health == 0:
        end_game = True

    draw(screen=screen, view=f'{player_1_sum_health} vs {player_2_sum_health}', x=width // 2, y=y - 150, cent=True,
         size=60,
         color='Green')

    if rounds % 2 in [0, 0.5] and not end_game:
        draw(screen, view='<=', x=width // 2, y=y - 30, cent=True, size=50, color='Red')
    elif rounds % 2 in [1, 1.5] and not end_game:
        draw(screen, view='=>', x=width // 2, y=y - 30, cent=True, size=50, color='Red')
    else:
        if player_1_sum_health == 0:
            win = 'Player 2 WIN'
            if not guest:
                winner = login2
                loser = login1
                update_data_base(winner, loser)
        if player_2_sum_health == 0:
            win = 'Player 1 WIN'
            if not guest:
                winner = login1
                loser = login2
                update_data_base(winner, loser)

        draw(screen, view=win, x=width // 2, y=y - 30, cent=True, size=50, color='Red')
        pygame.display.flip()
        time.sleep(10)
        running = False

    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
