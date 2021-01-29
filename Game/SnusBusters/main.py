import pygame
import os
import sys
import random
import datetime as dt

width, height = 800, 800
FPS = 600

os.chdir('Game\\SnusBusters\\')

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)

    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def name_pic_render(x, y):
    image = load_image('ghostbuster.png')
    screen.blit(image, (x, y))


def menu_pic_render(x, y):
    image = load_image('menu.png')
    screen.blit(image, (x, y))


class Ghost(pygame.sprite.Sprite):
    image_1 = load_image("ghost_1.jpg")
    image_1 = pygame.transform.scale(image_1, (170, 176))

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Ghost.image_1
        self.size_x = 190
        self.size_y = 196

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y

    def update(self):
        self.rect.y += 1
        if self.rect.y >= 996:
            self.rect.y = -196


def settings_render():
    image = load_image('settings.png')
    screen.blit(image, (180, 200))


def game_options_render():
    image = load_image('game.png')
    screen.blit(image, (180, 200))


def start_screen():
    name_run = pygame.USEREVENT + 1
    pygame.time.set_timer(name_run, 10)
    name_x, name_y = -800, 0
    name_is_shown = False

    ghosts = pygame.sprite.Group()
    Ghost(0, -200, ghosts)
    Ghost(625, -400, ghosts)
    Ghost(0, -600, ghosts)
    Ghost(625, -800, ghosts)
    Ghost(0, -1000, ghosts)
    Ghost(625, -1200, ghosts)

    menu_mov = pygame.USEREVENT + 1
    pygame.time.set_timer(menu_mov, 10)
    menu_x, menu_y = 180, 1200
    menu_is_shown = False
    settings_are_shown = False
    game_options = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.MOUSEBUTTONDOWN and name_is_shown and menu_is_shown:
                x, y = event.pos

                if 285 <= x <= 471 and 459 <= y <= 525:
                    settings_are_shown = True
                    menu_is_shown = False
                    settings_render()
                if 285 <= x <= 471 and 348 <= y <= 420:
                    game_options = True
                    menu_is_shown = False
                    game_options_render()
            if event.type == pygame.MOUSEBUTTONDOWN and settings_are_shown:
                x, y = event.pos

                if 216 <= x <= 310 and 222 <= y <= 256:
                    menu_is_shown = True
                    settings_are_shown = False

            if event.type == pygame.MOUSEBUTTONDOWN and game_options:
                x, y = event.pos

                if 216 <= x <= 310 and 222 <= y <= 256:

                    menu_is_shown = True
                    game_options = False
                elif 313 <= x <= 449 and 412 <= y <= 448:
                    return 'simple'
                elif 313 <= x <= 449 and 488 <= y <= 518:
                    return 'medium'
                elif 313 <= x <= 449 and 557 <= y <= 584:
                    return 'hard'

            if event.type == name_run:
                screen.fill((42, 42, 42))
                name_pic_render(name_x, name_y)
                if name_x + 800 <= 800:
                    name_x += 10
                else:
                    name_is_shown = True

                if settings_are_shown:
                    settings_render()
                    x, y = pygame.mouse.get_pos()
                    if 216 <= x <= 310 and 222 <= y <= 256:
                        pygame.draw.line(screen, (0, 255, 0), (205, 243), (253, 212), 5)
                        pygame.draw.line(screen, (0, 255, 0), (205, 243), (253, 275), 5)
                if game_options:
                    game_options_render()
                    x, y = pygame.mouse.get_pos()
                    if 216 <= x <= 310 and 222 <= y <= 256:
                        pygame.draw.line(screen, (0, 255, 0), (205, 243), (253, 212), 5)
                        pygame.draw.line(screen, (0, 255, 0), (205, 243), (253, 275), 5)
                    elif 313 <= x <= 449 and 412 <= y <= 448:
                        pygame.draw.line(screen, (0, 255, 0), (313, 448), (449, 448), 5)
                    elif 313 <= x <= 449 and 488 <= y <= 518:
                        pygame.draw.line(screen, (0, 255, 0), (313, 518), (449, 518), 5)
                    elif 313 <= x <= 449 and 557 <= y <= 584:
                        pygame.draw.line(screen, (0, 255, 0), (313, 584), (463, 584), 5)
                if name_is_shown and (menu_is_shown or settings_are_shown or game_options):
                    ghosts.draw(screen)
                    ghosts.update()
            if event.type == menu_mov and name_is_shown and not settings_are_shown and not game_options:

                menu_pic_render(menu_x, menu_y)
                if menu_y >= 200:
                    menu_y -= 15
                else:
                    menu_is_shown = True
                if menu_is_shown:
                    x, y = pygame.mouse.get_pos()
                    if 285 <= x <= 471 and 459 <= y <= 525:
                        pygame.draw.line(screen, (0, 255, 0), (287, 526), (472, 526), 5)
                        pygame.draw.line(screen, (0, 255, 0), (472, 456), (472, 526), 5)
                        pygame.draw.line(screen, (0, 255, 0), (287, 456), (287, 526), 5)
                        pygame.draw.line(screen, (0, 255, 0), (287, 456), (472, 456), 5)
                    elif 285 <= x <= 471 and 348 <= y <= 420:
                        pygame.draw.line(screen, (0, 255, 0), (287, 349), (287, 413), 5)
                        pygame.draw.line(screen, (0, 255, 0), (287, 349), (471, 349), 5)
                        pygame.draw.line(screen, (0, 255, 0), (471, 413), (287, 413), 5)
                        pygame.draw.line(screen, (0, 255, 0), (471, 413), (471, 349), 5)
        pygame.display.flip()
        clock.tick(FPS)


def fire_render(x, y):
    image = load_image('fire.png')
    screen.blit(image, (x, y))


class HomeTown:
    def __init__(self):
        self.health = 1000
        self.x = 0
        self.y = 770
        self.max_health = 1000

    def render(self, screen):
        x = self.x
        y = self.y
        len_x = 800
        len_y = 8
        pygame.draw.rect(screen, (255, 255, 255), ((x, y), (len_x, len_y)))
        new_x = self.health / self.max_health * len_x
        if self.health > 0:
            pygame.draw.rect(screen, (0, 255, 0), ((x, y), (new_x, len_y)))


class Patron:
    def __init__(self, x, y, speed, damage):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage

    def move(self):
        self.y -= self.speed

    def render_shot(self):
        pygame.draw.circle(screen, 'red', (self.x, self.y), 5)
        self.move()


class Enemy:

    def __init__(self, speed, xp, damage):
        self.r = random.randint(60, width - 60)
        self.x = self.r
        self.y = 0
        self.speed = speed
        self.max_health = xp
        self.health = xp
        self.damage = damage
        self.image = load_image('ghost_1.jpg')
        self.image = pygame.transform.scale(self.image, (50, 50))

    def render(self, screen):
        screen.blit(self.image, (self.x - 25, self.y - 25))
        len_x = 100
        len_y = 10
        x = self.x - len_x // 2
        y = self.y - 50
        pygame.draw.rect(screen, (0, 0, 0), ((x, y), (len_x, len_y)), 2)
        pygame.draw.rect(screen, (255, 255, 255), ((x, y), (len_x, len_y)))
        new_x = self.health / self.max_health * len_x
        pygame.draw.rect(screen, (0, 255, 0), ((x, y), (new_x, len_y)))

    def move(self):
        self.y += self.speed


class Hero:
    def __init__(self, speed):
        self.x = width // 2
        self.y = height - 65
        self.speed = speed
        self.image = load_image('hero.png')
        self.image = pygame.transform.scale(self.image, (160, 30))

    def render(self, screen):
        screen.blit(self.image, (self.x - 80, self.y))

    def move_left(self):
        if self.x - 80 > 0:
            self.x -= self.speed

    def move_right(self):
        if self.x + 80 < 800:
            self.x += self.speed


class Timer:
    def __init__(self, time, gap):
        self.timing = time
        self.gap = gap
        self.interval = dt.timedelta(seconds=self.gap)

    def run(self):
        now = dt.datetime.now()
        if now >= self.timing + self.interval:
            self.timing = dt.datetime.now()
            return True
        return False


def victiry_render():
    image = load_image('victory.png')
    screen.blit(image, (180, 200))


def lose_render():
    image = load_image('lose.png')
    screen.blit(image, (180, 200))


def back_render():
    image = load_image('back.png')
    screen.blit(image, (0, 0))


if __name__ == '__main__':

    pygame.init()
    pygame.display.set_caption('Игра')
    size = width, height
    screen = pygame.display.set_mode(size)

    enemies = []
    patrons = []

    enemy = pygame.USEREVENT + 1
    pygame.time.set_timer(enemy, 10)
    clock = pygame.time.Clock()
    hero = pygame.USEREVENT + 1
    aftergame = pygame.USEREVENT + 1
    pygame.time.set_timer(hero, 10)

    running = True
    enemy_is_spoted = False

    player_shot = False
    victory = False
    game_ended = False
    lose = False
    lvl = start_screen()

    if lvl == 'simple':
        lvl = 'Лёгкий'
        speed_of_enemy = 0.75
        speed_of_player = 3
        enemy_spot_speed = 3
        enemy_xp = 100
        enemy_damage = 100
        player_damage = 50
    elif lvl == 'medium':
        lvl = 'Средний'
        speed_of_enemy = 1
        speed_of_player = 3
        enemy_spot_speed = 2
        enemy_xp = 100
        enemy_damage = 250
        player_damage = 34
    else:
        lvl = 'Сложный'
        speed_of_enemy = 1.25
        speed_of_player = 3
        enemy_spot_speed = 2
        enemy_xp = 100
        enemy_damage = 340
        player_damage = 25
    speed_of_patron = 5

    kills = 0
    enemies_last = 50
    game_started = True
    game_timer = Timer(dt.datetime.now(), enemy_spot_speed)
    player = Hero(speed_of_player)
    home = HomeTown()
    f = 0
    while running:
        if lvl == 'simple' or lvl == 'Лёгкий':
            lvl = 'Лёгкий'
            speed_of_enemy = 0.75
            speed_of_player = 3
            enemy_spot_speed = 3
            enemy_xp = 100
            enemy_damage = 100
            player_damage = 50
            if f == 0:
                enemies_last = 10
                f = 1
        elif lvl == 'medium' or lvl == 'Средний':
            lvl = 'Средний'
            speed_of_enemy = 1
            speed_of_player = 3
            enemy_spot_speed = 2
            enemy_xp = 100
            enemy_damage = 250
            player_damage = 34
            if f == 0:
                enemies_last = 35
                f = 1
        elif lvl == 'hard' or lvl == 'Сложный':
            lvl = 'Сложный'
            speed_of_enemy = 1.25
            speed_of_player = 3
            enemy_spot_speed = 2
            enemy_xp = 100
            enemy_damage = 340
            player_damage = 25
            if f == 0:
                enemies_last = 50
                f = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]:
                player.move_left()
            if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
                player.move_right()

            if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) \
                    and game_started:
                player_shot = True
                fire_render(player.x - 17, player.y - 26)
                p = Patron(player.x, player.y, speed_of_patron, player_damage)

                patrons.append(p)

            if event.type == enemy and game_started:
                screen.fill((42, 42, 42))
                for en in enemies:
                    en.move()

                    if en.y >= 770:
                        home.health -= en.damage
                        enemies.remove(en)

                    en.render(screen)

                    if home.health <= 0:
                        lose = True
                        game_ended = True
                        game_started = False
            if event.type == pygame.MOUSEBUTTONDOWN and game_started:
                x, y = event.pos
                if 41 <= x <= 143 and 22 <= y <= 47:
                    lvl = start_screen()
                    game_ended = False
                    lose = False
                    game_started = True
                    kills = 0
                    f = 0
                    patrons = []
                    enemies = []
                    player = Hero(speed_of_player)
                    home = HomeTown()
            if event.type == hero and game_started:

                if player_shot:
                    for p in patrons:
                        p.render_shot()
                        if p.y <= - 20:
                            patrons.remove(p)

                        for e in enemies:
                            if e.y - 25 <= p.y - 5 <= e.y + 25 and e.x - 25 <= p.x + 5 <= e.x + 30:

                                e.health -= p.damage

                                patrons.remove(p)
                                if e.health <= 0:
                                    kills += 1
                                    enemies_last -= 1
                                    enemies.remove(e)
                                    if kills % 5 == 0:
                                        enemy_spot_speed -= 0.25
                                        speed_of_enemy += 0.25
                                        game_timer = Timer(dt.datetime.now(), enemy_spot_speed)

                                    if enemies_last == 0:
                                        game_started = False
                                        game_ended = True
                                        victory = True

                font = pygame.font.Font(None, 35)
                lvl_text = font.render(f'Уровень: {lvl}', True, (100, 255, 100))
                en_last = font.render(f'Призраков осталось: {str(enemies_last)}', True, (100, 255, 100))
                kills_text = font.render(f'Убийств: {str(kills)}', True, (100, 255, 100))
                home_xp = font.render(f'ХП: {str(home.health)}', True, (100, 255, 100))
                back_render()
                screen.blit(home_xp, (650, 700))
                screen.blit(kills_text, (600, 90))
                screen.blit(lvl_text, (550, 10))
                screen.blit(en_last, (500, 50))
                x, y = pygame.mouse.get_pos()
                if 41 <= x <= 143 and 22 <= y <= 47:
                    pygame.draw.line(screen, (0, 255, 0), (23, 33), (83, 5),  5)
                    pygame.draw.line(screen, (0, 255, 0), (23, 33), (83, 61), 5)
                home.render(screen)
                player.render(screen)

            if event.type == aftergame:
                if victory:
                    victiry_render()
                    x, y = pygame.mouse.get_pos()
                    if 217 <= x <= 408 and 331 <= y <= 360:
                        pygame.draw.line(screen, (0, 255, 0), (217, 360), (370, 360), 5)
                    elif 322 <= x <= 567 and 493 <= y <= 521:
                        pygame.draw.line(screen, (0, 255, 0), (327, 530), (565, 530), 5)

                elif lose:
                    lose_render()
                    x, y = pygame.mouse.get_pos()
                    if 203 <= x <= 326 and 380 <= y <= 419:
                        pygame.draw.line(screen, (255, 0, 0), (203, 419), (326, 419), 5)
                    elif 362 <= x <= 588 and 474 <= y <= 506:
                        pygame.draw.line(screen, (255, 0, 0), (362, 506), (588, 506), 5)
            if lose and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if 203 <= x <= 326 and 380 <= y <= 419:
                    lvl = start_screen()
                    game_ended = False
                    lose = False
                    game_started = True
                    kills = 0
                    f = 0
                    patrons = []
                    enemies = []
                    player = Hero(speed_of_player)
                    home = HomeTown()
                elif 362 <= x <= 588 and 474 <= 506:
                    game_ended = False
                    lose = False
                    game_started = True
                    kills = 0
                    f = 0
                    patrons = []
                    enemies = []
                    player = Hero(speed_of_player)
                    home = HomeTown()
            if victory and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if 217 <= x <= 408 and 331 <= y <= 360:
                    lvl = start_screen()
                    game_ended = False
                    victory = False
                    game_started = True
                    kills = 0
                    f = 0
                    patrons = []
                    enemies = []
                    player = Hero(speed_of_player)
                    home = HomeTown()
                elif 322 <= x <= 567 and 493 <= y <= 521:
                    game_ended = False
                    victory = False
                    game_started = True
                    kills = 0
                    f = 0
                    patrons = []
                    enemies = []
                    player = Hero(speed_of_player)
                    home = HomeTown()
        if game_timer != None:
            if game_timer.run():
                # print('Создаю врага')
                a = Enemy(speed_of_enemy, enemy_xp, enemy_damage)
                enemies.append(a)

        for en in enemies:
            if en.y >= height + 20:
                enemies.remove(en)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
