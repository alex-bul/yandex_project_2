from config import *

import math
import random
import time
import pygame
import sys
import os
import json

os.chdir('Game\\CrazyFox\\')

all_sprites = pygame.sprite.Group()
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)

user_data_file = 'user_data.json'
running = True
game_run = False
SPRITE_CHANGE_OFFSET = 11
speed = DEFAULT_SPEED
time_start = time.time()


def get_record():
    with open(user_data_file, 'r') as file:
        return json.loads(file.read())['record']


def set_record(value):
    with open(user_data_file, 'w') as file:
        file.write(json.dumps({
            "record": value
        }))


def load_image(file_name, colorkey=None):
    fullname = file_name
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
    return image


def calculate_SPRITE_CHANGE_OFFSET():
    return max(SPRITE_CHANGE_OFFSET - (speed // SPRITE_CHANGE_OFFSET), 5)


def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(load_image(image), 5, 1)
        self.cur_frame = 0

        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.default_y = SCREEN_SIZE[1] * SIZE_SKY - self.rect.h
        self.rect.y = self.default_y
        self.rect.x = 20

        self.is_jumping = False
        self.is_falling = False
        self.jump_speed_buster = 1

        self.effects = {}

    def set_image(self, image):
        old_y = self.rect.y
        self.frames = []
        self.cut_sheet(load_image(image), 5, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.default_y = SCREEN_SIZE[1] * SIZE_SKY - self.rect.h
        if self.is_jumping:
            self.is_jumping = False
            self.is_falling = True
            self.rect.y = old_y
        elif not self.is_falling:
            self.rect.y = self.default_y
        else:
            self.rect.y = old_y

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def jump(self):
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        if not self.is_falling:
            self.is_jumping = True

    def start_effect(self, name, effect_type, value):
        global speed
        if effect_type == 'speed_up':
            print(name, effect_type, value)
            self.effects[name] = {'start_time': time.time(), 'type': effect_type, 'speed_end': speed}
            speed *= value
        elif effect_type == 'jump_speed_down':
            self.effects[name] = {'start_time': time.time(), 'type': effect_type}
            self.jump_speed_buster = value

    def update(self):
        self.check_effects()
        if self.is_jumping:
            self.rect = self.rect.move(0, -math.ceil(
                DINO_JUMP_SPEED * (self.rect.y - self.default_y + DINO_JUMP_HEIGNT) / 100 * (
                            DEFAULT_SPEED / speed) * self.jump_speed_buster))
            if (self.rect.y - self.default_y + DINO_JUMP_HEIGNT) / 100 <= 0.1:
                self.is_jumping = False
                self.is_falling = True
        elif self.is_falling:
            if self.default_y - self.rect.y < DINO_FALL_SPEED:
                self.rect = self.rect.move(0, self.default_y - self.rect.y)
                self.is_falling = False
            else:
                c = (self.rect.y - self.default_y + DINO_JUMP_HEIGNT) / 100 * self.jump_speed_buster
                self.rect = self.rect.move(0, math.ceil(DINO_FALL_SPEED * (c if c < 0.9 else 1)))
        else:
            offset = calculate_SPRITE_CHANGE_OFFSET()
            self.cur_frame = (self.cur_frame + 1) % (len(self.frames) * offset)
            self.image = self.frames[self.cur_frame // offset]
            self.mask = pygame.mask.from_surface(self.image)

    def check_effects(self):
        global speed
        for name, data in self.effects.copy().items():
            if time.time() - data['start_time'] > BONUS_DURATION:
                if data['type'] == 'speed_up':
                    speed = data['speed_end']
                elif data['type'] == 'jump_speed_down':
                    self.jump_speed_buster = 1
                self.effects.pop(name)

    def is_affected_speed(self):
        return 'speed_up' in map(lambda x: x['type'], self.effects.values())

    def can_broke(self):
        return 'Опьянение' in self.effects.keys()


class Object(pygame.sprite.Sprite):
    def __init__(self, image, step, x=None, y=None):
        super().__init__(all_sprites)
        self.image = load_image(image)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x if x else SCREEN_SIZE[0]
        self.rect.y = y if y else SCREEN_SIZE[1] * SIZE_SKY - self.rect.h
        self.step = -step

        self.is_broken = False
        self.broken_direction = 0
        self.broken_speed = (-0.1 * random.randint(5, 10), 0.1 * random.randint(5, 10))
        self.broken_rotate_angle = random.randint(0, 60)

    def update(self):
        if self.is_broken:
            try:
                self.rect = self.rect.move([i * BROKE_ENEMY_SPEED * self.broken_direction for i in self.broken_speed])
                self.image = rot_center(self.image, self.broken_rotate_angle * -self.broken_direction)
                self.broken_rotate_angle -= 1
            except ValueError:
                pass
        else:
            self.rect = self.rect.move(self.step, 0)

    def is_hidden(self):
        return self.rect.right + self.rect.w < 0 or \
               self.rect.left + self.rect.w < 0 or \
               self.rect.top + self.rect.h < 0 or \
               self.rect.bottom + self.rect.h < 0

    def broke(self, direction):
        self.is_broken = True
        self.broken_direction = direction

    def get_far(self):
        return SCREEN_SIZE[0] - self.rect.x


class DecorationObject(Object):
    def __init__(self, image, step, offset_y):
        super().__init__(image, step, SCREEN_SIZE[0] + random.randint(15, 30), None)
        self.rect.y = SCREEN_SIZE[1] * SIZE_SKY - ((self.rect.h + random.randint(5, 20)) * offset_y)


class Enemy(Object):
    def __init__(self, image, step, x=None, y=None):
        super().__init__(image, step, x, y)
        self.image = load_image(image)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x if x else SCREEN_SIZE[0]
        self.rect.y = y if y else SCREEN_SIZE[1] * SIZE_SKY - self.rect.h
        self.step = -step

    def broke(self, direction):
        self.is_broken = True
        self.broken_direction = direction

    def update(self):
        global game_run, time_end_game, current_record
        if pygame.sprite.collide_mask(self, dino) and not self.is_broken:
            if dino.can_broke():
                self.broke(-1)
            elif not IMMORTAL:
                game_run = False
                time_end_game = time.time()
                if current_record < game_map.score:
                    set_record(game_map.score)
                    current_record = game_map.score
        if self.is_broken:
            try:
                self.rect = self.rect.move([i * BROKE_ENEMY_SPEED * self.broken_direction for i in self.broken_speed])
                self.image = rot_center(self.image, self.broken_rotate_angle * -self.broken_direction)
                self.broken_rotate_angle -= 1
            except ValueError:
                pass
        else:
            self.rect = self.rect.move(self.step, 0)


class AnimateEnemy(Enemy):
    def __init__(self, image, step, x=None, y=None):
        self.frames = []
        self.cut_sheet(load_image(image), *animate_sprites[image.split('/')[-1]])
        self.cur_frame = 0
        super().__init__(image, step, x, y)
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        offset = calculate_SPRITE_CHANGE_OFFSET()
        self.cur_frame = (self.cur_frame + 1) % (len(self.frames) * offset)
        self.image = self.frames[self.cur_frame // offset]
        super().update()


class Bird(AnimateEnemy):
    def __init__(self, image, step, x=None, y=None):
        y = y if y else SCREEN_SIZE[1] * SIZE_SKY - dino.rect.h - random.randint(10, 30)
        super().__init__(image, step, x, y)


class Tornado(AnimateEnemy):
    def __init__(self, image, step, x=None, y=None):
        super().__init__(image, step, x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x += SPEED_TORNADO * DEFAULT_SPEED

    def update(self):
        if self.rect.x >= SCREEN_SIZE[0] and not self.is_broken:
            font = pygame.font.Font(None, 50)
            text = font.render(f"!", True, (255, 255, 255))
            pygame.draw.circle(screen, (255, 59, 59), (SCREEN_SIZE[0] - WARNING_RADIUS * 1.5,
                                                       SCREEN_SIZE[1] * SIZE_SKY - WARNING_RADIUS * 3.5),
                               WARNING_RADIUS)
            screen.blit(text, (SCREEN_SIZE[0] - WARNING_RADIUS * 1.5 - text.get_width() // 2 - 1,
                               SCREEN_SIZE[1] * SIZE_SKY - WARNING_RADIUS * 3.5 - text.get_height() // 2 + 2))

        offset = calculate_SPRITE_CHANGE_OFFSET()
        self.cur_frame = (self.cur_frame + 1) % (len(self.frames) * offset)
        self.image = self.frames[self.cur_frame // offset]
        super().update()

    def check_colide(self, obj):
        if pygame.sprite.collide_mask(self, obj):
            obj.broke(-1)

    def get_far(self):
        return SCREEN_SIZE[0] - self.rect.x - SPEED_TORNADO * DEFAULT_SPEED


class Bonus(Object):
    def __init__(self, image, step, effect_object, x=None, y=None):
        super().__init__(image, step, x, y)
        self.effect_object = effect_object
        for i in list(filter(lambda x: not isinstance(x, Bonus), game_map.ground_objects)):
            if pygame.sprite.collide_mask(self, i):
                self.rect.x = self.rect.x + i.rect.w * random.choice([1.5, -1.5])

    def update(self):
        if pygame.sprite.collide_mask(self, dino):
            dino.start_effect(*self.effect_object)
            self.rect.x = -self.rect.w
        super().update()


class Map:
    def __init__(self, screen, SCREEN_SIZE):
        self.screen = screen
        self.SCREEN_SIZE = SCREEN_SIZE
        self.ground_objects = []
        self.decoration = []
        self.tech_score = 0
        self.score = 0
        self.next_enemy_distance = self.calculate_next_enemy_distance()

        self.disaster = None
        self.last_bonus_spawn = 0

    def clear(self):
        effect_list = dino.effects.keys()
        if 'Опьянение' in effect_list:
            self.screen.fill((245, random.randint(100, 170), 47))
            pygame.draw.rect(self.screen, (random.randint(100, 170), 52, 235),
                             (0, 0, self.SCREEN_SIZE[0], self.SCREEN_SIZE[1] * SIZE_SKY), 0)
        elif 'Галлюцинация'in effect_list:
            self.screen.fill(COLOR_SKY)
            pygame.draw.rect(self.screen, COLOR_EARTH,
                             (0, 0, self.SCREEN_SIZE[0], self.SCREEN_SIZE[1] * SIZE_SKY), 0)
        else:
            self.screen.fill(COLOR_EARTH)
            pygame.draw.rect(self.screen, COLOR_SKY, (0, 0, self.SCREEN_SIZE[0], self.SCREEN_SIZE[1] * SIZE_SKY), 0)

    def update(self):
        self.clear()
        self.spawn_enemy()
        self.spawn_decoration()
        self.spawn_bonus()

        if game_run:
            font = pygame.font.Font(None, 50)
            text = font.render(f"Счёт: {self.score}", True, (100, 255, 100))
            text_x = SCREEN_SIZE[0] - text.get_width()
            text_y = 0
            screen.blit(text, (text_x, text_y))
            if current_record:
                text_record = font.render(f"Рекорд: {current_record}", True, (93, 232, 93))
                text_x = SCREEN_SIZE[0] - text.get_width() - text_record.get_width() - 20
                text_y = 0
                screen.blit(text_record, (text_x, text_y))

            score_text_height = text.get_height()

            for i, (effect_name, data) in enumerate(list(dino.effects.items())):
                font = pygame.font.Font(None, 30)
                text = font.render(f"{effect_name} закончится через: "
                                   f"{BONUS_DURATION - int(time.time() - data['start_time'])}",
                                   True, (252, 198, 3))
                text_y = (score_text_height + 10) * (i + 1)
                text_x = SCREEN_SIZE[0] - text.get_width()
                screen.blit(text, (text_x, text_y))

        for i, obj in enumerate(self.ground_objects.copy()):
            if obj.is_hidden():
                self.ground_objects.pop(i)
                all_sprites.remove(obj)
                if not isinstance(obj, Bonus):
                    self.score += 1
                if isinstance(obj, Tornado):
                    self.disaster = None
        if self.disaster:
            for i in filter(lambda x: not isinstance(x, Tornado), self.ground_objects):
                self.disaster.check_colide(i)

    def random_select_next(self):
        path = 'src/enemy/'
        select = random.randint(1, 12)
        if select < 2 and self.score >= TORNADO_SCORE_START  and not self.disaster:
            self.disaster = Tornado(f'{path}tornado.png', SPEED_TORNADO)
            return self.disaster
        elif select < 4 and self.score >= BIRD_SCORE_START:
            return Bird(f'{path}bird.png', SPEED_BIRD)
        else:
            return Enemy(f'{path}{random.randint(1, ENEMY_SKIN_COUNT)}.png', SPEED_CACTUS)

    def spawn_enemy(self):
        if self.ground_objects:
            if self.ground_objects[-1].get_far() >= self.next_enemy_distance:
                self.ground_objects.append(self.random_select_next())
                self.next_enemy_distance = self.calculate_next_enemy_distance()
        else:
            self.ground_objects.append(self.random_select_next())

    def spawn_decoration(self):
        path = "src/decoration/"
        if random.randint(1, 40) == 1:
            if random.randint(0, 1):
                self.decoration.append(
                    DecorationObject(f"{path}sky_{random.randint(1, 2)}.png",
                                     SPEED_CACTUS, random.randint(3, SCREEN_SIZE[1] * SIZE_SKY // 70)))
            else:
                self.decoration.append(DecorationObject(f"{path}ground_{random.randint(1, 4)}.png", SPEED_CACTUS,
                                                        -random.randint(1, SCREEN_SIZE[1] * SIZE_EARTH // 75)))

    def spawn_bonus(self):
        path = "src/bonus/"
        if time.time() - self.last_bonus_spawn > MIN_BONUS_FREQUENCY and len(dino.effects.items()) == 0:
            if random.randint(1, BONUS_CHANCE_SPAWN) == 1:
                image_name, data = random.choice(list(effects.items()))
                self.ground_objects.append(Bonus(f"{path}{image_name}", SPEED_CACTUS, data))
                self.last_bonus_spawn = time.time()

    @staticmethod
    def calculate_next_enemy_distance():
        return random.randint(dino.rect.w * 4, DISTANCE_BETWEEN_ENEMY_MAX)


def draw_guide():
    FONT_COLOR = (240, 240, 240)
    OUTLINE_COLOR = (200, 200, 200)
    DESCRIPTION_COLOR = (220, 220, 220)
    start_y = SCREEN_SIZE[1] // 10
    rules = ['↑|пробел - прыжок', '↓ - пригнуться',
             # 'R - начать заново'
             ]
    main_title = "Лиса погибла!" if time_end_game else "Crazy FOX"

    font = pygame.font.Font('src/fonts/bahnschrift.ttf', 60)
    text = font.render(main_title, True, OUTLINE_COLOR)
    screen.blit(text, ((SCREEN_SIZE[0] - text.get_width()) // 2 + 3, start_y))
    text = font.render(main_title, True, FONT_COLOR)
    screen.blit(text, ((SCREEN_SIZE[0] - text.get_width()) // 2, start_y))

    start_y += text.get_height() + 20
    font = pygame.font.Font('src/fonts/calibri.ttf', 30)

    for i in rules:
        text = font.render(i, True, OUTLINE_COLOR)
        screen.blit(text, ((SCREEN_SIZE[0] - text.get_width()) // 2 + 1, start_y))
        text = font.render(i, True, FONT_COLOR)
        screen.blit(text, ((SCREEN_SIZE[0] - text.get_width()) // 2, start_y))
        start_y += text.get_height() + 10
    start_y += 10
    font = pygame.font.Font('src/fonts/calibri.ttf', 20)

    text = font.render("Проходите препятствия и подбирайте бустеры", True, OUTLINE_COLOR)
    screen.blit(text, ((SCREEN_SIZE[0] - text.get_width()) // 2, start_y))
    text = font.render("Проходите препятствия и подбирайте бустеры", True, FONT_COLOR)
    screen.blit(text, ((SCREEN_SIZE[0] - text.get_width()) // 2, start_y))
    start_y += text.get_height() + 10
    start_y += 20

    text = font.render("Нажмите ↑|пробел чтобы начать", True, DESCRIPTION_COLOR)
    screen.blit(text, ((SCREEN_SIZE[0] - text.get_width()) // 2, start_y))
    pygame.display.flip()
    start_y += text.get_height() + 5

    text = font.render("Нажмите ESC чтобы выйти", True, DESCRIPTION_COLOR)
    screen.blit(text, ((SCREEN_SIZE[0] - text.get_width()) // 2, start_y))
    pygame.display.flip()


dino = MainCharacter("src/character/fox.png")
game_map = Map(screen, SCREEN_SIZE)
game_map.clear()
all_sprites.draw(screen)
pygame.display.flip()

time_end_game = 0
current_record = get_record()
while running:
    if speed < MAX_GAME_SPEED and not dino.is_affected_speed():
        speed = int(DEFAULT_SPEED + (time.time() - time_start))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and not game_run \
                    and time.time() - time_end_game > 0.500:
                speed = DEFAULT_SPEED
                all_sprites = pygame.sprite.Group()
                time_start = time.time()
                game_run = True
                game_map = Map(screen, SCREEN_SIZE)
                dino = MainCharacter("src/character/fox.png")
            elif event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                is_space_not_down = True
        if game_run:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    dino.jump()
                    is_space_not_down = False
                elif event.key == pygame.K_DOWN:
                    dino.set_image("src/character/fox_tilt.png")
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    dino.set_image("src/character/fox.png")

    if game_run:
        game_map.update()
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(speed)
    else:
        draw_guide()
