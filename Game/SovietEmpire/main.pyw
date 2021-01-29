import pygame
import os
import sys
from collections import deque

os.chdir('Game\\SovietEmpire\\')


def load_image(name):
    fullname = os.path.join('data/' + name)
    image = pygame.image.load(fullname)
    return image


win_points = {'red': 0,
              'blue': 0}
pygame.init()
screen_size = (800, 650)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('SOVIET EMPIRE II')
FPS = 50

tile_images = {
    'empty': load_image('grass.png'),
    'river': load_image('river.png'),
    'coast1': load_image('coast1.png'),
    'coast2': load_image('coast2.png')
}

tile_width = tile_height = 50


class ScreenFrame(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 500, 500)


class SpriteGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class River(Tile):
    def __init__(self, pos_x, pos_y):
        super().__init__('river', pos_x, pos_y)
        self.frames = [load_image('river.png'), load_image('river2.png'),
                       load_image('river3.png'), load_image('river4.png')]
        self.cur_frame = 0
        self.k = 0

    def update(self):
        self.k += 1
        if self.k == 20:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.k = 0


roads = [[None for j in range(10)] for i in range(10)]
buildings = [[None for j in range(10)] for i in range(10)]
buildings_colors = [[None for j in range(10)] for i in range(10)]
buildings_armies = [[0 for j in range(10)] for i in range(10)]
war_map = [[0 for j in range(10)] for i in range(10)]
war_map_colors = [[None for j in range(10)] for i in range(10)]


class Road(Sprite):
    def __init__(self, color, pos_x, pos_y):
        super().__init__(sprite_group)
        self.color = color
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.update()
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self):
        fn = ''
        if self.pos_y < 9:
            if roads[self.pos_y + 1][self.pos_x]:
                fn += 'S'
        if self.pos_x > 0:
            if roads[self.pos_y][self.pos_x - 1]:
                fn += 'W'
        if self.pos_y > 0:
            if roads[self.pos_y - 1][self.pos_x]:
                fn += 'N'
        if self.pos_x < 9:
            if roads[self.pos_y][self.pos_x + 1]:
                fn += 'E'
        if fn:
            self.image = load_image('roads/' + self.color + '/' + fn + '.png')
        else:
            self.image = load_image('roads/' + self.color + '/' + 'notconnected.png')


class TownBuilding():
    def __init__(self, town_sprite):
        self.handicrafts = 20
        self.rural = 10
        self.fish = 0
        self.sprite = town_sprite


class CastleBuilding():
    def __init__(self, castle_sprite):
        self.handicrafts = 10
        self.rural = 0
        self.fish = 0
        self.sprite = castle_sprite


class ChurchBuilding():
    def __init__(self, church_sprite):
        self.handicrafts = 0
        self.rural = 0
        self.fish = 0
        self.sprite = church_sprite


class ManorBuilding():
    def __init__(self, manor_sprite):
        self.handicrafts = 0
        self.rural = 0
        self.fish = 0
        self.sprite = manor_sprite


class ArableBuilding():
    def __init__(self, arable_sprite):
        self.handicrafts = 0
        self.rural = 25
        self.fish = 0
        self.sprite = arable_sprite


class FishingGroundsBuilding():
    def __init__(self, fishing_grounds_sprite):
        self.handicrafts = 0
        self.rural = 5
        self.fish = 3
        self.sprite = fishing_grounds_sprite
        self.color = self.sprite.color
        self.pos_x = self.sprite.pos[0]
        self.pos_y = self.sprite.pos[1]
        self.update()
        self.rect = self.sprite.image.get_rect().move(
            tile_width * self.pos_x, tile_height * self.pos_y)

    def update(self):
        pass


class PlayerCursor(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = load_image('cur3.png')
        self.cur_frame = 0
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.frames = [load_image('cur3.png'), load_image('cur2.png'), load_image('cur.png'),
                       load_image('cur.png'), load_image('cur.png'), load_image('cur2.png')]
        self.pos = (pos_x, pos_y)
        self.k = 0

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0], tile_height * self.pos[1])

    def update(self):
        self.k += 1
        if self.k == 10:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.k = 0


class PlayerProduction():
    def __init__(self, color):
        self.color = color
        self.handicrafts_produced = 0
        self.rural_produced = 0
        self.fish_produced = 0

    def update(self, handicrafts, rural, fish):
        self.handicrafts_produced += handicrafts
        self.rural_produced += rural
        self.fish_produced += fish


class Town(Sprite):
    def __init__(self, color, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = load_image(color + 'town3.png')
        self.cur_frame = 0
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.frames = [load_image(color + 'town3.png'), load_image(color + 'town2.png'),
                       load_image(color + 'town.png'),
                       load_image(color + 'town.png'), load_image(color + 'town.png'),
                       load_image(color + 'town2.png')]
        self.pos = (pos_x, pos_y)
        self.k = 0

    def update(self):
        self.k += 1
        if self.k == 7:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.k = 0


class Castle(Sprite):
    def __init__(self, color, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = load_image(color + 'castle.png')
        self.cur_frame = 0
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)
        self.k = 0


class Church(Sprite):
    def __init__(self, color, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = load_image(color + 'church.png')
        self.cur_frame = 0
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)
        self.k = 0


class Manor(Sprite):
    def __init__(self, color, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = load_image(color + 'manor.png')
        self.cur_frame = 0
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)
        self.k = 0


class Arable(Sprite):
    def __init__(self, color, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = load_image(color + 'arable.png')
        self.cur_frame = 0
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)
        self.k = 0


class FishingGrounds(Sprite):
    def __init__(self, color, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = load_image(color + 'fishing_grounds.png')
        self.color = color
        self.cur_frame = 0
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)
        self.k = 0


class Treasury():
    def __init__(self, color):
        self.color = color
        self.current_money = 6000
        self.income = 0
        self.costs = 0
        self.military = 0
        self.diplomacy = 0
        self.defence = 0
        self.deficit = 0
        self.loan = 0
        self.interest = 0

    def current_money_update(self):
        self.current_money += self.income
        self.current_money -= self.costs

    def income_update(self, k):
        self.income += k

    def costs_update(self, military, defence, deficit):
        self.military = military
        self.diplomacy = 0
        self.defence = defence
        self.deficit = deficit
        self.interest = 300 if self.loan else 0
        self.costs = sum([self.military, self.diplomacy, self.defence, self.deficit, self.interest])


player = None
clock = pygame.time.Clock()
sprite_group = SpriteGroup()
hero_group = SpriteGroup()


def terminate():
    pygame.quit()
    sys.exit


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), screen_size)
    screen.blit(fon, (0, 0))

    new_game_button = load_image('newGameBtn.png')
    new_game_button_rect = new_game_button.get_rect(bottomleft=(35, 424))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if new_game_button_rect.collidepoint(pygame.mouse.get_pos()):
                    return
        screen.blit(new_game_button, new_game_button_rect)
        pygame.display.flip()
        clock.tick(FPS)


def end_game_screen(color, description):
    font = pygame.font.Font('data\pixel.ttf', 25)
    fon = pygame.transform.scale(load_image('victory_screen_' + color + '.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    if description == 'bankruptcy' and color == 'blue':
        string = 'Красный игрок обанкротился и продал вотчину синему'
        description_text = font.render(string, True,
                                       (255, 255, 255))
    elif description == 'bankruptcy' and color == 'red':
        string = 'Синий игрок обанкротился и продал вотчину красному'
        description_text = font.render(string, True,
                                       (255, 255, 255))
    elif description == 'domination' and color == 'blue':
        string = 'Синий игрок добился полного экономического превосходства в регионе'
        description_text = font.render(string, True,
                                       (255, 255, 255))
    elif description == 'domination' and color == 'red':
        string = 'Красный игрок добился полного экономического превосходства в регионе'
        description_text = font.render(string, True,
                                       (255, 255, 255))
    elif description == 'domination' and color == 'eq':
        string = 'Красный и синий игрок сохранили одинаковые экономические показатели'
        description_text = font.render(string, True,
                                       (255, 255, 255))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.blit(description_text, description_text.get_rect(bottomright=(775, 500)))
        pygame.display.flip()
        clock.tick(FPS)


def load_level():
    level_name = 'map.txt'
    filename = level_name
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def blue_generation():
    new_cursor = PlayerCursor(0, 9)
    return new_cursor


def red_generation():
    new_cursor = PlayerCursor(9, 0)
    return new_cursor


def base_generation(level):
    level = level[0]
    new_town, new_town2, x, y = None, None, None, None
    river_tiles = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if y == x:
                river_tiles.append(River(x, y))
            elif y == x + 1:
                Tile('coast2', x, y)
            elif y == x - 1:
                Tile('coast1', x, y)
            elif y == 9 and x == 0:
                Tile('empty', x, y)
                new_town = Town('blue', x, y)
            elif y == 0 and x == 9:
                Tile('empty', x, y)
                new_town2 = Town('red', x, y)
            else:
                Tile('empty', x, y)
    return new_town, new_town2, river_tiles, x, y


def move(cursor, movement):
    x, y = cursor.pos
    if movement == "up":
        if y > 0 and level_map[0][y - 1][x] == ".":
            cursor.move(x, y - 1)
    elif movement == "down":
        if y < max_y and level_map[0][y + 1][x] == ".":
            cursor.move(x, y + 1)
    elif movement == "left":
        if x > 0 and level_map[0][y][x - 1] == ".":
            cursor.move(x - 1, y)
    elif movement == "right":
        if x < max_x and level_map[0][y][x + 1] == ".":
            cursor.move(x + 1, y)


def road_build(x, y):
    global roads
    roads[y][x] = Road(turns[1], x, y)
    for i in roads:
        for j in i:
            if j:
                j.update()


def build():
    global red_treasury, blue_treasury, treasury_text, interest_text
    road_button = load_image('buildingsBtns/road.png')
    road_button_rect = road_button.get_rect(bottomleft=(20, 588))
    road_cost = 500
    arable_button = load_image('buildingsBtns/arable.png')
    arable_button_rect = arable_button.get_rect(bottomleft=(100, 588))
    arable_cost = 500
    manor_button = load_image('buildingsBtns/manor.png')
    manor_button_rect = manor_button.get_rect(bottomleft=(180, 588))
    manor_cost = 1000
    castle_button = load_image('buildingsBtns/castle.png')
    castle_button_rect = castle_button.get_rect(bottomleft=(260, 588))
    castle_cost = 2400
    church_button = load_image('buildingsBtns/church.png')
    church_button_rect = church_button.get_rect(bottomleft=(340, 588))
    church_cost = 1200
    fishing_grounds_button = load_image('buildingsBtns/fishing_grounds.png')
    fishing_grounds_button_rect = fishing_grounds_button.get_rect(bottomleft=(420, 588))
    fishing_grounds_cost = 1000
    back_button = load_image('backBtn.png')
    back_button_rect = back_button.get_rect(bottomleft=(20, 640))
    build_error = load_image('impossibleBuilding.png')
    build_error_rect = build_button.get_rect(bottomright=(300, 300))
    running = True
    building_impossible = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move(cursor, "up")
                elif event.key == pygame.K_DOWN:
                    move(cursor, "down")
                elif event.key == pygame.K_LEFT:
                    move(cursor, "left")
                elif event.key == pygame.K_RIGHT:
                    move(cursor, "right")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                building_impossible = False
                enemy_castle = False
                d = False
                for i in range(10):
                    for j in range(10):
                        if buildings[i][j] and buildings_colors[i][j] == turns[0][0]:
                            if (isinstance(buildings[i][j], CastleBuilding) or isinstance(buildings[i][j],
                                                                                          TownBuilding)) and abs(
                                i - cursor.pos[1]) <= 1 and abs(
                                j - cursor.pos[0]) <= 1:
                                if (cursor.pos[0] == 0 and j == 9) or (cursor.pos[0] == 9 and j == 0) or (
                                        cursor.pos[1] == 0 and i == 9) or (cursor.pos[1] == 9 and i == 0):
                                    pass
                                else:
                                    enemy_castle = True
                            d = True
                            break
                    if d:
                        break
                treasury = red_treasury if turns[0] == 'blue' else blue_treasury
                if road_button_rect.collidepoint(pygame.mouse.get_pos()):
                    connected = False
                    for i in range(10):
                        for j in range(10):
                            if roads[i][j] and ((abs(i - cursor.pos[1]) <= 1 and abs(j - cursor.pos[0]) == 0) or
                                                (abs(i - cursor.pos[1]) == 0 and abs(j - cursor.pos[0]) <= 1)):
                                if roads[i][j].color == turns[1]:
                                    connected = True

                    if enemy_castle or roads[cursor.pos[1]][cursor.pos[0]] or cursor.pos[1] == cursor.pos[0] \
                            or treasury.current_money - road_cost < -500 or not connected:
                        building_impossible = True
                    else:
                        road_build(cursor.pos[0], cursor.pos[1])
                        if turns[0] == 'blue':
                            red_treasury.current_money -= road_cost
                        else:
                            blue_treasury.current_money -= road_cost
                        treasury_text = font.render(str(round(red_treasury.current_money, 2)), True, (0, 0, 0)) \
                            if turns[0] == 'blue' else font.render(str(round(blue_treasury.current_money, 2)), True,
                                                                   (0, 0, 0))
                if castle_button_rect.collidepoint(pygame.mouse.get_pos()):
                    if enemy_castle or not roads[cursor.pos[1]][cursor.pos[0]] or cursor.pos[1] == cursor.pos[0] \
                            or treasury.current_money - castle_cost < -500 or buildings[cursor.pos[1]][cursor.pos[0]] \
                            or roads[cursor.pos[1]][cursor.pos[0]].color != turns[1]:
                        building_impossible = True
                    else:
                        if turns[0] == 'blue':
                            red_treasury.current_money -= castle_cost
                        else:
                            blue_treasury.current_money -= castle_cost
                        buildings[cursor.pos[1]][cursor.pos[0]] = CastleBuilding(Castle(turns[1],
                                                                                        cursor.pos[0], cursor.pos[1]))

                        treasury_text = font.render(str(round(red_treasury.current_money, 2)), True, (0, 0, 0)) \
                            if turns[0] == 'blue' else font.render(str(round(blue_treasury.current_money, 2)), True,
                                                                   (0, 0, 0))
                        buildings_colors[cursor.pos[1]][cursor.pos[0]] = turns[1][0]
                if manor_button_rect.collidepoint(pygame.mouse.get_pos()):
                    if enemy_castle or not roads[cursor.pos[1]][cursor.pos[0]] or cursor.pos[1] == cursor.pos[0] \
                            or treasury.current_money - manor_cost < -500 or buildings[cursor.pos[1]][cursor.pos[0]] \
                            or roads[cursor.pos[1]][cursor.pos[0]].color != turns[1]:
                        building_impossible = True
                    else:
                        if turns[0] == 'blue':
                            red_treasury.current_money -= manor_cost
                        else:
                            blue_treasury.current_money -= manor_cost
                        buildings[cursor.pos[1]][cursor.pos[0]] = ManorBuilding(Manor(turns[1],
                                                                                      cursor.pos[0], cursor.pos[1]))

                        treasury_text = font.render(str(round(red_treasury.current_money, 2)), True, (0, 0, 0)) \
                            if turns[0] == 'blue' else font.render(str(round(blue_treasury.current_money, 2)), True,
                                                                   (0, 0, 0))
                        buildings_colors[cursor.pos[1]][cursor.pos[0]] = turns[1][0]
                if church_button_rect.collidepoint(pygame.mouse.get_pos()):
                    if enemy_castle or not roads[cursor.pos[1]][cursor.pos[0]] or cursor.pos[1] == cursor.pos[0] \
                            or treasury.current_money - church_cost < -500 or buildings[cursor.pos[1]][cursor.pos[0]] \
                            or roads[cursor.pos[1]][cursor.pos[0]].color != turns[1]:
                        building_impossible = True
                    else:
                        if turns[0] == 'blue':
                            red_treasury.current_money -= church_cost
                        else:
                            blue_treasury.current_money -= church_cost
                        buildings[cursor.pos[1]][cursor.pos[0]] = ChurchBuilding(Church(turns[1],
                                                                                        cursor.pos[0], cursor.pos[1]))

                        treasury_text = font.render(str(round(red_treasury.current_money, 2)), True, (0, 0, 0)) \
                            if turns[0] == 'blue' else font.render(str(round(blue_treasury.current_money, 2)), True,
                                                                   (0, 0, 0))
                        buildings_colors[cursor.pos[1]][cursor.pos[0]] = turns[1][0]
                if arable_button_rect.collidepoint(pygame.mouse.get_pos()):
                    if enemy_castle or roads[cursor.pos[1]][cursor.pos[0]] or cursor.pos[1] == cursor.pos[0] \
                            or treasury.current_money - arable_cost < -500 or buildings[cursor.pos[1]][cursor.pos[0]]:
                        building_impossible = True
                    else:
                        if turns[0] == 'blue':
                            red_treasury.current_money -= arable_cost
                        else:
                            blue_treasury.current_money -= arable_cost
                        buildings[cursor.pos[1]][cursor.pos[0]] = ArableBuilding(Arable(turns[1],
                                                                                        cursor.pos[0], cursor.pos[1]))

                        treasury_text = font.render(str(round(red_treasury.current_money, 2)), True, (0, 0, 0)) \
                            if turns[0] == 'blue' else font.render(str(round(blue_treasury.current_money, 2)), True,
                                                                   (0, 0, 0))
                        buildings_colors[cursor.pos[1]][cursor.pos[0]] = turns[1][0]
                if fishing_grounds_button_rect.collidepoint(pygame.mouse.get_pos()):
                    connected = False
                    for i in range(10):
                        for j in range(10):
                            if roads[i][j] and ((abs(i - cursor.pos[1]) <= 1 and abs(j - cursor.pos[0]) == 0) or
                                                (abs(i - cursor.pos[1]) == 0 and abs(j - cursor.pos[0]) <= 1)):
                                if roads[i][j].color == turns[1]:
                                    connected = True

                    if roads[cursor.pos[1]][cursor.pos[0]] or cursor.pos[1] != cursor.pos[0] \
                            or treasury.current_money - fishing_grounds_cost < -500 or not connected:
                        building_impossible = True
                    else:
                        roads[cursor.pos[1]][cursor.pos[0]] = FishingGroundsBuilding(FishingGrounds(turns[1],
                                                                                                    cursor.pos[0],
                                                                                                    cursor.pos[1]))
                        buildings[cursor.pos[1]][cursor.pos[0]] = FishingGroundsBuilding(FishingGrounds(turns[1],
                                                                                                        cursor.pos[0],
                                                                                                        cursor.pos[1]))
                        buildings_colors[cursor.pos[1]][cursor.pos[0]] = turns[1][0]
                        if turns[0] == 'blue':
                            red_treasury.current_money -= fishing_grounds_cost
                        else:
                            blue_treasury.current_money -= fishing_grounds_cost
                        treasury_text = font.render(str(round(red_treasury.current_money, 2)), True, (0, 0, 0)) \
                            if turns[0] == 'blue' else font.render(str(round(blue_treasury.current_money, 2)), True,
                                                                   (0, 0, 0))
                    for i in roads:
                        for j in i:
                            if j:
                                j.update()
                if back_button_rect.collidepoint(pygame.mouse.get_pos()):
                    running = False
                if turns[1] == 'blue':
                    if loan_button_rect.collidepoint((pygame.mouse.get_pos())) and not blue_treasury.loan:
                        blue_treasury.loan = 3900
                        blue_treasury.current_money += 3000

                        treasury_text = font.render(str(round(blue_treasury.current_money, 2)), True, (0, 0, 0))
                        interest_text = font2.render(str(300), True, (0, 0, 0))
                        screen.blit(treasury_text, treasury_text.get_rect(bottomright=(750, 60)))
                elif turns[1] == 'red':
                    if loan_button_rect.collidepoint((pygame.mouse.get_pos())) and not red_treasury.loan:
                        red_treasury.loan = 3900
                        red_treasury.current_money += 3000
                        treasury_text = font.render(str(round(red_treasury.current_money, 2)), True, (0, 0, 0))
                        interest_text = font2.render(str(300), True, (0, 0, 0))
                        screen.blit(treasury_text, treasury_text.get_rect(bottomright=(750, 60)))

        screen.fill(pygame.Color("black"))
        sprite_group.draw(screen)
        hero_group.draw(screen)
        for i in river_tiles:
            i.update()
        cursor.update()
        for i in buildings:
            for j in i:
                if j:
                    j.sprite.update()

        screen.blit(panel, panel.get_rect(bottomright=(500, 650)))
        screen.blit(treasury_panel, treasury_panel.get_rect(bottomright=(801, 620)))
        screen.blit(treasury_text, treasury_text.get_rect(bottomright=(750, 60)))
        screen.blit(income_text, income_text.get_rect(bottomright=(750, 267)))
        screen.blit(costs_text, costs_text.get_rect(bottomright=(750, 373)))
        screen.blit(profit_text, profit_text.get_rect(bottomright=(750, 162)))
        screen.blit(road_button, road_button_rect)
        screen.blit(arable_button, arable_button_rect)
        screen.blit(manor_button, manor_button_rect)
        screen.blit(castle_button, castle_button_rect)
        screen.blit(church_button, church_button_rect)
        screen.blit(fishing_grounds_button, fishing_grounds_button_rect)
        screen.blit(back_button, back_button_rect)
        screen.blit(military_text, military_text.get_rect(bottomright=(750, 485)))
        screen.blit(diplomacy_text, diplomacy_text.get_rect(bottomright=(750, 507)))
        screen.blit(defence_text, defence_text.get_rect(bottomright=(750, 534)))
        screen.blit(deficit_text, deficit_text.get_rect(bottomright=(750, 551)))
        screen.blit(handicrafts_deficit_text, handicrafts_deficit_text.get_rect(bottomright=(690, 564)))
        screen.blit(rural_deficit_text, rural_deficit_text.get_rect(bottomright=(690, 574)))
        screen.blit(fish_deficit_text, fish_deficit_text.get_rect(bottomright=(690, 584)))
        if turns[1] == 'blue':
            if blue_treasury.loan == 0:
                screen.blit(loan_button, loan_button_rect)
            else:
                screen.blit(interest_text, interest_text.get_rect(bottomright=(750, 602)))
        elif turns[1] == 'red':
            if red_treasury.loan == 0:
                screen.blit(loan_button, loan_button_rect)
            else:
                screen.blit(interest_text, interest_text.get_rect(bottomright=(750, 602)))
        if building_impossible:
            screen.blit(build_error, build_error_rect)
        clock.tick(FPS)
        pygame.display.flip()


red_production = PlayerProduction('red')
blue_production = PlayerProduction('blue')


class Trade():
    def __init__(self, color):
        self.handicrafts = 5
        self.rural = 1
        self.fish = 3
        self.handicrafts_required = 25
        self.rural_required = 50
        self.fish_required = 5
        self.color = color
        self.turn = 0

    def update(self):

        base_handicrafts = 5
        base_rural = 1
        base_fish = 3
        if self.color == 'red':
            if red_production.handicrafts_produced == 0:
                self.handicrafts = base_handicrafts * self.handicrafts_required
            else:
                self.handicrafts = base_handicrafts * \
                                   1 / (red_production.handicrafts_produced / self.handicrafts_required)
            if red_production.rural_produced == 0:
                self.rural = base_handicrafts * self.fish_required
            else:
                self.rural = base_rural * \
                             1 / (red_production.rural_produced / self.rural_required)
            if red_production.fish_produced == 0:
                self.fish = base_fish * self.fish_required
            else:
                self.fish = base_fish * \
                            1 / (red_production.fish_produced / self.fish_required)
        elif self.color == 'blue':
            if blue_production.handicrafts_produced == 0:
                self.handicrafts = base_handicrafts * self.handicrafts_required
            else:
                self.handicrafts = base_handicrafts * \
                                   1 / (blue_production.handicrafts_produced / self.handicrafts_required)
            if blue_production.rural_produced == 0:
                self.rural = base_handicrafts * self.fish_required
            else:
                self.rural = base_rural * \
                             1 / (blue_production.rural_produced / self.rural_required)
            if blue_production.fish_produced == 0:
                self.fish = base_fish * self.fish_required
            else:
                self.fish = base_fish * \
                            1 / (blue_production.fish_produced / self.fish_required)

    def transport(self, pos):
        graph = {}
        for i in range(10):
            for j in range(10):
                curr_node = roads[i][j]
                if not roads[i][j]:
                    pass
                elif curr_node.color == self.color:
                    graph[(j, i)] = []
                    if curr_node.pos_y < 9:
                        if roads[curr_node.pos_y + 1][curr_node.pos_x]:
                            if roads[curr_node.pos_y + 1][curr_node.pos_x].color == self.color:
                                graph[(j, i)].append((curr_node.pos_x, curr_node.pos_y + 1))
                    if curr_node.pos_x > 0:
                        if roads[curr_node.pos_y][curr_node.pos_x - 1]:
                            if roads[curr_node.pos_y][curr_node.pos_x - 1].color == self.color:
                                graph[(j, i)].append((curr_node.pos_x - 1, curr_node.pos_y))
                    if curr_node.pos_y > 0:
                        if roads[curr_node.pos_y - 1][curr_node.pos_x]:
                            if roads[curr_node.pos_y - 1][curr_node.pos_x].color == self.color:
                                graph[(j, i)].append((curr_node.pos_x, curr_node.pos_y - 1))
                    if curr_node.pos_x < 9:
                        if roads[curr_node.pos_y][curr_node.pos_x + 1]:
                            if roads[curr_node.pos_y][curr_node.pos_x + 1].color == self.color:
                                graph[(j, i)].append((curr_node.pos_x + 1, curr_node.pos_y))

        queue = deque([pos])
        visited = {pos: None}
        if self.color == 'red':
            goal = (9, 0)
        else:
            goal = (0, 9)
        while queue:
            curr_node = queue.popleft()
            if curr_node == goal:
                break

            next_nodes = graph[curr_node]
            for next_node in next_nodes:
                if next_node not in visited:
                    queue.append(next_node)
                    visited[next_node] = curr_node
        curr_node = goal
        k = 0
        if graph[goal] == []:
            return k
        while curr_node != pos:
            curr_node = visited[curr_node]
            k += 1
        return k


start_screen()

level_map = [[[i for i in '..........']] * 10]
town, town2, river_tiles, max_x, max_y = base_generation(level_map)
roads[0][9] = Road('red', 9, 0)
roads[9][0] = Road('blue', 0, 9)
buildings[0][9] = TownBuilding(town2)
buildings[9][0] = TownBuilding(town)

buildings_colors[0][9] = 'r'
buildings_colors[9][0] = 'b'
cursor = blue_generation()
panel = load_image('panel.png')
treasury_panel = load_image('treasuryPanel.png')
end_turn_button = load_image('endTurnBtn.png')
end_turn_button_rect = end_turn_button.get_rect(bottomright=(480, 620))
build_button = load_image('buildBtn.png')
build_button_rect = build_button.get_rect(bottomright=(170, 620))
loan_button = load_image('loanBtn.png')
loan_button_rect = loan_button.get_rect(bottomright=(768, 610))
blue_treasury = Treasury('blue')
red_treasury = Treasury('red')
blue_trade = Trade('blue')
red_trade = Trade('red')
turns = ['red', 'blue']
font = pygame.font.Font('data\pixel.ttf', 20)
font2 = pygame.font.Font('data\pixel.ttf', 15)
font3 = pygame.font.Font('data\pixel.ttf', 10)
red_production.handicrafts_produced = 0
red_production.rural_produced = 0
red_production.fish_produced = 0
blue_production.handicrafts_produced = 0
blue_production.rural_produced = 0
blue_production.fish_produced = 0
red_treasury.income_update(-red_treasury.income)
blue_treasury.income_update(-blue_treasury.income)
for i in range(10):
    for j in range(10):
        if buildings[i][j] and buildings_colors[i][j] == 'r':
            red_production.update(buildings[i][j].handicrafts, buildings[i][j].rural,
                                  buildings[i][j].fish)
            red_trade.update()
        elif buildings[i][j] and buildings_colors[i][j] == 'b':
            blue_production.update(buildings[i][j].handicrafts, buildings[i][j].rural,
                                   buildings[i][j].fish)
            blue_trade.update()
red_defence = 0
blue_defence = 0
for i in range(10):
    for j in range(10):
        if buildings[i][j] and buildings_colors[i][j] == 'r' \
                and not isinstance(buildings[i][j], ArableBuilding):
            p_handicrafts = buildings[i][j].handicrafts * red_trade.handicrafts
            p_rural = buildings[i][j].rural * red_trade.rural
            p_fish = buildings[i][j].fish * red_trade.fish
            way = red_trade.transport((j, i))
            if way:
                for k in range(way):
                    p_handicrafts *= 1.2
                    p_rural *= 1.2
                    p_fish *= 1.2

            red_treasury.income_update(p_handicrafts +
                                       p_rural +
                                       p_fish)

            if isinstance(buildings[i][j], CastleBuilding):
                red_defence += 150


        elif buildings[i][j] and buildings_colors[i][j] == 'b' \
                and not isinstance(buildings[i][j], ArableBuilding):
            p_handicrafts = buildings[i][j].handicrafts * blue_trade.handicrafts
            p_rural = buildings[i][j].rural * blue_trade.rural
            p_fish = buildings[i][j].fish * blue_trade.fish

            way = blue_trade.transport((j, i))
            if way:
                for k in range(way):
                    p_handicrafts *= 1.2
                    p_rural *= 1.2
                    p_fish *= 1.2

            blue_treasury.income_update(p_handicrafts +
                                        p_rural +
                                        p_fish)

            if isinstance(buildings[i][j], CastleBuilding):
                blue_defence += 150
    blue_handicrafts_deficit = max(0, (blue_trade.handicrafts_required - blue_production.handicrafts_produced)) \
                               * blue_trade.handicrafts
    blue_rural_deficit = max(0, (blue_trade.rural_required - blue_production.rural_produced)) \
                         * blue_trade.rural
    blue_fish_deficit = max(0, (blue_trade.fish_required - blue_production.fish_produced)) \
                        * blue_trade.fish

    blue_handicrafts_deficit = max(0, (blue_trade.handicrafts_required - blue_production.handicrafts_produced)) \
                               * blue_trade.handicrafts
    blue_rural_deficit = max(0, (blue_trade.rural_required - blue_production.rural_produced)) \
                         * blue_trade.rural
    blue_fish_deficit = max(0, (blue_trade.fish_required - blue_production.fish_produced)) \
                        * blue_trade.fish
    blue_deficit = sum((blue_handicrafts_deficit, blue_rural_deficit, blue_fish_deficit))
    blue_deficit = sum((blue_handicrafts_deficit, blue_rural_deficit, blue_fish_deficit))
    blue_treasury.costs_update(0, blue_defence, blue_deficit)
    blue_treasury.costs_update(0, blue_defence, blue_deficit)

treasury_text = font.render(str(round(blue_treasury.current_money, 2)), True, (0, 0, 0))
income_text = font.render(str(round(blue_treasury.income, 2)), True, (0, 0, 0))
costs_text = font.render(str(round(blue_treasury.costs, 2)), True, (0, 0, 0))
profit_text = font.render(str(round(blue_treasury.income - blue_treasury.costs, 2)),
                          True, (0, 0, 0))
deficit_text = font2.render(str(round(blue_treasury.deficit, 2)), True, (0, 0, 0))
military_text = font2.render(str(round(blue_treasury.military, 2)), True, (0, 0, 0))
diplomacy_text = font2.render(str(round(blue_treasury.diplomacy, 2)), True, (0, 0, 0))
defence_text = font2.render(str(round(blue_treasury.defence, 2)), True, (0, 0, 0))
handicrafts_deficit_text = font3.render \
    (str(round(blue_production.handicrafts_produced, 2)) +
     '/' + str(round(blue_trade.handicrafts_required, 2)), True, (0, 0, 0))
rural_deficit_text = font3.render \
    (str(round(blue_production.rural_produced, 2)) +
     '/' + str(round(blue_trade.rural_required, 2)), True, (0, 0, 0))
fish_deficit_text = font3.render \
    (str(round(blue_production.fish_produced, 2)) +
     '/' + str(round(blue_trade.fish_required, 2)), True, (0, 0, 0))
screen.blit(treasury_text, treasury_text.get_rect(bottomright=(750, 60)))
screen.blit(income_text, income_text.get_rect(bottomright=(750, 265)))
screen.blit(defence_text, income_text.get_rect(bottomright=(750, 530)))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(cursor, "up")
            elif event.key == pygame.K_DOWN:
                move(cursor, "down")
            elif event.key == pygame.K_LEFT:
                move(cursor, "left")
            elif event.key == pygame.K_RIGHT:
                move(cursor, "right")
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if end_turn_button_rect.collidepoint(pygame.mouse.get_pos()):
                cursor.kill()
                cursor = red_generation() if turns[0] == 'red' else blue_generation()
                if turns[0] == 'red':
                    red_trade.turn += 1
                    if red_trade.turn % 8 == 0 and red_trade.turn >= 8 and red_trade.turn <= 40:
                        if red_trade.turn != 0:
                            red_trade.handicrafts_required += 5
                            red_trade.rural_required += 50
                            red_trade.fish_required += 2
                else:
                    blue_trade.turn += 1
                    if blue_trade.turn % 8 == 0 and blue_trade.turn >= 8 and blue_trade.turn <= 40:
                        if blue_trade.turn != 0:
                            blue_trade.handicrafts_required += 5
                            blue_trade.rural_required += 50
                            blue_trade.fish_required += 2
                    if blue_trade.turn == 41:
                        if blue_treasury.income > red_treasury.income:
                            end_game_screen('blue',
                                            'domination')
                        elif blue_treasury.income < red_treasury.income:
                            end_game_screen('red', 'domination')
                        elif blue_treasury.income == red_treasury.income:
                            end_game_screen('eq', 'domination')
                    if blue_treasury.current_money <= -20000:
                        end_game_screen('red', 'bankruptcy')
                    if red_treasury.current_money <= -20000:
                        end_game_screen('blue', 'bankruptcy')

                red_production.handicrafts_produced = 0
                red_production.rural_produced = 0
                red_production.fish_produced = 0
                blue_production.handicrafts_produced = 0
                blue_production.rural_produced = 0
                blue_production.fish_produced = 0
                red_treasury.income_update(-red_treasury.income)
                blue_treasury.income_update(-blue_treasury.income)
                red_defence = 0
                blue_defence = 0
                for i in range(10):
                    for j in range(10):
                        if isinstance(buildings[i][j], ManorBuilding):
                            buildings[i][j].rural = 0
                for i in range(10):
                    for j in range(10):
                        if buildings[i][j] and buildings_colors[i][j] == 'r' \
                                and isinstance(buildings[i][j], ArableBuilding):
                            rural_to_manor = buildings[i][j].rural
                            d = False
                            for i2 in range(10):
                                for j2 in range(10):
                                    if isinstance(buildings[i2][j2], ChurchBuilding) \
                                            and abs(i2 - i) <= 1 and abs(j2 - j) <= 1:
                                        rural_to_manor *= 1.5
                                        d = True
                                        break
                                if d:
                                    break
                            d = False
                            for i2 in range(10):
                                for j2 in range(10):
                                    if isinstance(buildings[i2][j2], ManorBuilding) \
                                            and abs(i2 - i) <= 1 and abs(j2 - j) <= 1:
                                        buildings[i2][j2].rural += rural_to_manor
                                        d = True
                                        break
                                if d:
                                    break
                        elif buildings[i][j] and buildings_colors[i][j] == 'b' \
                                and isinstance(buildings[i][j], ArableBuilding):
                            rural_to_manor = buildings[i][j].rural
                            d = False
                            for i2 in range(10):
                                for j2 in range(10):
                                    if isinstance(buildings[i2][j2], ChurchBuilding) \
                                            and abs(i2 - i) <= 1 and abs(j2 - j) <= 1:
                                        rural_to_manor *= 1.5
                                        d = True
                                        break
                                if d:
                                    break
                            d = False
                            for i2 in range(10):
                                for j2 in range(10):
                                    if isinstance(buildings[i2][j2], ManorBuilding) \
                                            and abs(i2 - i) <= 1 and abs(j2 - j) <= 1:
                                        buildings[i2][j2].rural += rural_to_manor
                                        d = True
                                        break
                                if d:
                                    break

                for i in range(10):
                    for j in range(10):
                        if buildings[i][j] and buildings_colors[i][j] == 'r' \
                                and not isinstance(buildings[i][j], ArableBuilding):
                            red_production.update(buildings[i][j].handicrafts, buildings[i][j].rural,
                                                  buildings[i][j].fish)
                            red_trade.update()
                        elif buildings[i][j] and buildings_colors[i][j] == 'b' \
                                and not isinstance(buildings[i][j], ArableBuilding):
                            blue_production.update(buildings[i][j].handicrafts, buildings[i][j].rural,
                                                   buildings[i][j].fish)
                            blue_trade.update()

                for i in range(10):
                    for j in range(10):
                        if buildings[i][j] and buildings_colors[i][j] == 'r' \
                                and not isinstance(buildings[i][j], ArableBuilding):
                            p_handicrafts = buildings[i][j].handicrafts * red_trade.handicrafts
                            p_rural = buildings[i][j].rural * red_trade.rural
                            p_fish = buildings[i][j].fish * red_trade.fish
                            way = red_trade.transport((j, i))
                            if way:
                                for k in range(way):
                                    p_handicrafts *= 1.18
                                    p_rural *= 1.18
                                    p_fish *= 1.18

                            red_treasury.income_update(p_handicrafts +
                                                       p_rural +
                                                       p_fish)

                            if isinstance(buildings[i][j], CastleBuilding):
                                red_defence += 150

                        elif buildings[i][j] and buildings_colors[i][j] == 'b' \
                                and not isinstance(buildings[i][j], ArableBuilding):
                            p_handicrafts = buildings[i][j].handicrafts * blue_trade.handicrafts
                            p_rural = buildings[i][j].rural * blue_trade.rural
                            p_fish = buildings[i][j].fish * blue_trade.fish

                            way = blue_trade.transport((j, i))
                            if way:
                                for k in range(way):
                                    p_handicrafts *= 1.18
                                    p_rural *= 1.18
                                    p_fish *= 1.18

                            blue_treasury.income_update(p_handicrafts +
                                                        p_rural +
                                                        p_fish)
                            if isinstance(buildings[i][j], CastleBuilding):
                                blue_defence += 150
                blue_handicrafts_deficit = max(0,
                                               (blue_trade.handicrafts_required -
                                                blue_production.handicrafts_produced)) \
                                           * blue_trade.handicrafts
                blue_rural_deficit = max(0, (blue_trade.rural_required - blue_production.rural_produced)) \
                                     * blue_trade.rural
                blue_fish_deficit = max(0, (blue_trade.fish_required - blue_production.fish_produced)) \
                                    * blue_trade.fish

                red_handicrafts_deficit = max(0, (red_trade.handicrafts_required - red_production.handicrafts_produced)) \
                                          * red_trade.handicrafts
                red_rural_deficit = max(0, (red_trade.rural_required - red_production.rural_produced)) \
                                    * red_trade.rural
                red_fish_deficit = max(0, (red_trade.fish_required - red_production.fish_produced)) \
                                   * red_trade.fish
                blue_deficit = sum((blue_handicrafts_deficit, blue_rural_deficit, blue_fish_deficit))
                red_deficit = sum((red_handicrafts_deficit, red_rural_deficit, red_fish_deficit))
                blue_treasury.costs_update(0, blue_defence, blue_deficit)
                red_treasury.costs_update(0, red_defence, red_deficit)
                if turns[0] == 'red':
                    blue_treasury.current_money_update()
                    if blue_treasury.loan > 0:
                        blue_treasury.loan -= 300
                    treasury_text = font.render(str(round(red_treasury.current_money, 2)), True, (0, 0, 0))
                    income_text = font.render(str(round(red_treasury.income, 2)), True, (0, 0, 0))
                    costs_text = font.render(str(round(red_treasury.costs, 2)), True, (0, 0, 0))
                    profit_text = font.render(str(round(red_treasury.income - red_treasury.costs, 2)),
                                              True, (0, 0, 0))
                    deficit_text = font2.render(str(round(red_treasury.deficit, 2)), True, (0, 0, 0))
                    military_text = font2.render(str(round(red_treasury.military, 2)), True, (0, 0, 0))
                    diplomacy_text = font2.render(str(round(red_treasury.diplomacy, 2)), True, (0, 0, 0))
                    defence_text = font2.render(str(round(red_treasury.defence, 2)), True, (0, 0, 0))
                    handicrafts_deficit_text = font3.render \
                        (str(round(red_production.handicrafts_produced, 2)) +
                         '/' + str(round(red_trade.handicrafts_required, 2)), True, (0, 0, 0))
                    rural_deficit_text = font3.render \
                        (str(round(red_production.rural_produced, 2)) +
                         '/' + str(round(red_trade.rural_required, 2)), True, (0, 0, 0))
                    fish_deficit_text = font3.render \
                        (str(round(red_production.fish_produced, 2)) +
                         '/' + str(round(red_trade.fish_required, 2)), True, (0, 0, 0))


                else:
                    red_treasury.current_money_update()
                    if red_treasury.loan > 0:
                        red_treasury.loan -= 300
                    treasury_text = font.render(str(round(blue_treasury.current_money, 2)), True, (0, 0, 0))
                    income_text = font.render(str(round(blue_treasury.income, 2)), True, (0, 0, 0))
                    costs_text = font.render(str(round(blue_treasury.costs, 2)), True, (0, 0, 0))
                    profit_text = font.render(str(round(blue_treasury.income - blue_treasury.costs, 2)),
                                              True, (0, 0, 0))
                    deficit_text = font2.render(str(round(blue_treasury.deficit, 2)), True, (0, 0, 0))
                    military_text = font2.render(str(round(blue_treasury.military, 2)), True, (0, 0, 0))
                    diplomacy_text = font2.render(str(round(blue_treasury.diplomacy, 2)), True, (0, 0, 0))
                    defence_text = font2.render(str(round(blue_treasury.defence, 2)), True, (0, 0, 0))
                    handicrafts_deficit_text = font3.render \
                        (str(round(blue_production.handicrafts_produced, 2)) +
                         '/' + str(round(blue_trade.handicrafts_required, 2)), True, (0, 0, 0))
                    rural_deficit_text = font3.render \
                        (str(round(blue_production.rural_produced, 2)) +
                         '/' + str(round(blue_trade.rural_required, 2)), True, (0, 0, 0))
                    fish_deficit_text = font3.render \
                        (str(round(blue_production.fish_produced, 2)) +
                         '/' + str(round(blue_trade.fish_required, 2)), True, (0, 0, 0))
                turns = turns[::-1]
                screen.blit(treasury_text, treasury_text.get_rect(bottomright=(750, 60)))
                screen.blit(income_text, income_text.get_rect(bottomright=(750, 265)))
            if build_button_rect.collidepoint((pygame.mouse.get_pos())):
                build()

            if turns[1] == 'blue':
                if loan_button_rect.collidepoint((pygame.mouse.get_pos())) and not blue_treasury.loan:
                    blue_treasury.loan = 3900
                    blue_treasury.current_money += 3000

                    treasury_text = font.render(str(round(blue_treasury.current_money, 2)), True, (0, 0, 0))
                    interest_text = font2.render(str(300), True, (0, 0, 0))
                    screen.blit(treasury_text, treasury_text.get_rect(bottomright=(750, 60)))
            elif turns[1] == 'red':
                if loan_button_rect.collidepoint((pygame.mouse.get_pos())) and not red_treasury.loan:
                    red_treasury.loan = 3900
                    red_treasury.current_money += 3000
                    treasury_text = font.render(str(round(red_treasury.current_money, 2)), True, (0, 0, 0))
                    interest_text = font2.render(str(300), True, (0, 0, 0))
                    screen.blit(treasury_text, treasury_text.get_rect(bottomright=(750, 60)))

    screen.fill(pygame.Color("black"))
    sprite_group.draw(screen)
    hero_group.draw(screen)
    for i in river_tiles:
        i.update()
    cursor.update()
    for i in buildings:
        for j in i:
            if j:
                j.sprite.update()
    screen.blit(panel, panel.get_rect(bottomright=(500, 650)))
    screen.blit(treasury_panel, treasury_panel.get_rect(bottomright=(801, 620)))
    screen.blit(treasury_text, treasury_text.get_rect(bottomright=(750, 60)))
    screen.blit(income_text, income_text.get_rect(bottomright=(750, 267)))
    screen.blit(costs_text, costs_text.get_rect(bottomright=(750, 373)))
    screen.blit(profit_text, profit_text.get_rect(bottomright=(750, 162)))
    screen.blit(military_text, military_text.get_rect(bottomright=(750, 485)))
    screen.blit(diplomacy_text, diplomacy_text.get_rect(bottomright=(750, 507)))
    screen.blit(defence_text, defence_text.get_rect(bottomright=(750, 534)))
    screen.blit(deficit_text, deficit_text.get_rect(bottomright=(750, 551)))
    screen.blit(handicrafts_deficit_text, handicrafts_deficit_text.get_rect(bottomright=(690, 564)))
    screen.blit(rural_deficit_text, rural_deficit_text.get_rect(bottomright=(690, 574)))
    screen.blit(fish_deficit_text, fish_deficit_text.get_rect(bottomright=(690, 584)))
    screen.blit(end_turn_button, end_turn_button_rect)
    screen.blit(build_button, build_button_rect)
    if turns[1] == 'blue':
        if blue_treasury.loan == 0:
            screen.blit(loan_button, loan_button_rect)
        else:
            screen.blit(interest_text, interest_text.get_rect(bottomright=(750, 602)))
    elif turns[1] == 'red':
        if red_treasury.loan == 0:
            screen.blit(loan_button, loan_button_rect)
        else:
            screen.blit(interest_text, interest_text.get_rect(bottomright=(750, 602)))
    clock.tick(FPS)
    pygame.display.flip()