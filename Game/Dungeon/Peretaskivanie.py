import os
import random

import pygame

pygame.init()
size = width, height = 1920, 1080  # Размер окна
pygame.display.set_caption('Dungeon')
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
rounds = 0
fps = 600  # Отклик
step = 80  # Пробел между персонажами
running = True
x = 80  # Координата первого персонажа
y = 400  # Отступ от верха экрана
my_name = 0  # Номер персонажа


# Функция загрузки изображений
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


# Шанс попадания
def chance(rate=50):
    res = random.randint(0, 100)
    print(res)
    rate = 100 - rate
    if rate == 50:
        return random.choice([0, 1])
    if res >= rate:
        return 1
    else:
        return 0


# Отрисовка текста
def draw(screen, view, x, y, cent, size=50, color=None):
    set_color = (0, 0, 0)

    if color == 'Green':
        set_color = (0, 255, 55)
    elif color == 'Yellow':
        set_color = (255, 255, 0)
    elif color == 'Red':
        set_color = (255, 40, 40)

    font = pygame.font.Font(None, size)
    text = font.render(view, True, set_color)
    if cent:
        text_x = x - text.get_width() // 2
        text_y = y - text.get_height() // 2
    else:
        text_x = x
        text_y = y

    screen.blit(text, (text_x, text_y))


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = load_image(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


# Класс персонажа
class Character(pygame.sprite.Sprite):
    def __init__(self, *group, x, y, name=f'my_{my_name}', sprite_name):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(*group)
        self.chance = 0  # Дефолтный шанс попадения
        self.image = load_image(f'{sprite_name}.png')  # Загрузка изображения
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
            self.image = load_image(f'{self.sprite_name}.png')
        elif state == 2:
            self.image = load_image(f'{self.sprite_name}_attack.png')
        else:
            self.image = load_image(f'{self.sprite_name}_death.png')
            self.health = 0

        if 'enemy' in self.name:
            self.image = pygame.transform.flip(self.image, True, False)

    # Обновление действий с персонадами
    def update(self, *args):
        if 'pos' in str(args[0]) and not self.health <= 0:
            if args[0].type == pygame.MOUSEBUTTONUP and args[0].button == 1 and self.rect.collidepoint(
                    args[0].pos) and self.click:
                self.click = False
                for i in args[1]:
                    if self.rect.colliderect(i.rect) and i.name != self.name and not i.health <= 0 and not self.flag \
                            and self.name[:-1] != i.name[:-1]:

                        self.flag = True
                        print('-------------------------')
                        res = chance(self.chance)
                        print(f'{i.health} - {self.damage - (i.armor / 2)}')
                        print(f'health: {i.health}, armor: {i.armor}')
                        if (self.damage - (i.armor / 2)) > 0:
                            i.health -= int(self.damage - (i.armor / 2)) * res

                        else:
                            i.health -= 1 * chance(self.chance) * res
                        if i.armor >= self.damage * 0.1:
                            i.armor -= self.damage * 0.1 * res
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

        # Проверка на смерть
        if self.health <= 0 and not self.is_death:
            self.sprite()
            self.is_death = True
            self.rect = self.image.get_rect()
            self.rect.bottomleft = self.def_rect


# Класс Ассасина
class Assassin(Character):
    def __init__(self, x, y, name=f'my_{my_name}'):
        Character.__init__(self, x=x, y=y, name=name, sprite_name='Assassin')
        self.chance = 80
        self.health = 150
        self.def_health = self.health
        self.damage = 40
        self.armor = 30


# Класс Берсерка
class Berserk(Character):
    def __init__(self, x, y, name=f'my_{my_name}'):
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
heros = [Assassin(x=x, y=y)]
x += step

# Assassin(x=500, y=y, name='enemy_name_1'), Berserk(x=500 + step, y=y, name='enemy_name_2'),
#          Assassin(x=500 + step * 2, y=y, name='enemy_name_3'), Berserk(x=500 + step * 3, y=y, name='enemy_name_4')

# Генерация рандомных врагов
enemy = [eval(random.choice(['Assassin', 'Berserk']) + i) for i in
         ["(x=500, y=y, name='enemy_name_1')", "(x=500 + step, y=y, name='enemy_name_2')",
          "(x=500 + step * 2, y=y, name='enemy_name_3')", "(x=500 + step * 3, y=y, name='enemy_name_4')"]]
# for i in heros:
#     print(list(i.rect.center)[0] + x, list(i.rect.center)[1])
#     i.rect.center = [list(i.rect.center)[0] + x, list(i.rect.center)[1]]
#     x += step

all_sprites.add(heros)
all_sprites.add(enemy)
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

        # Добавление персонажей
        if key[pygame.K_RIGHT] and (key[pygame.K_1] or key[pygame.K_2]) and not change and len(heros) < 4:
            all_sprites.remove(heros)
            my_name += 1
            if key[pygame.K_1]:
                a = Assassin(x=x, y=y)  # Добавить Ассасина

            if key[pygame.K_2]:
                a = Berserk(x=x, y=y)  # Добавить Берсерка

            x += step
            heros.append(a)
            all_sprites.add(heros)

        if key[pygame.K_LEFT] and len(heros) > 0 and not change:  # Убрать последнего персонажа
            all_sprites.remove(heros)
            my_name -= 1
            heros = heros[:-1]
            x -= step
            all_sprites.add(heros)

    screen.fill((255, 255, 255))
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)
    all_sprites.draw(screen)
    all_sprites.update(event, heros + enemy)
    for i in heros + enemy:  # Отрисовка здоровья
        if i.def_health * 0.75 <= i.health <= i.def_health:
            color = 'Green'

        elif i.def_health * 0.50 <= i.health <= i.def_health * 0.75:
            color = 'Yellow'

        else:
            color = 'Red'
        draw(screen=screen, view=str(i.health), x=i.rect.center[0], y=i.rect.bottom - 90, cent=True, size=40,
             color=color)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
