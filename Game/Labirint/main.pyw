import pygame
import os
import Options
import random

os.chdir('Game\\Labirint\\')


class Scorebar(pygame.sprite.Sprite):
    def __init__(self, players):
        self.players = players

    def draw(self):
        counter = 1
        for i in board.Players:
            font = pygame.font.Font(None, 70)
            text = font.render(f"Score:{i.GetScore()}", True, (pygame.Color(i.GetPlayerColor())))
            screen.blit(text, ((Options.menu[0] - 100), Options.menu[1] + 70 * counter))
            counter += 1


class Player(pygame.sprite.Sprite):
    def __init__(self, X, Y, color, PosInSell, PlayerNo):
        self.score = 0
        self.X = X
        self.Y = Y
        self.PlayerNo = PlayerNo

        self.color = color
        self.PosInSell = PosInSell

    def draw(self):
        pygame.draw.ellipse(screen, pygame.Color(self.color),
                            (Options.LeftIndent + self.X * Options.SpriteSize + self.PosInSell[0],
                             Options.TopIndent + self.Y * Options.SpriteSize + self.PosInSell[1],
                             Options.SpriteSize / 2,
                             Options.SpriteSize / 2),
                            5)

    def SetCords(self, X, Y):
        self.X = X
        self.Y = Y

    def GetX(self):
        return self.X

    def GetNo(self):
        return self.PlayerNo

    def GetY(self):
        return self.Y

    def GetScore(self):
        return self.score

    def RiseScore(self):
        self.score += 1

    def GetPlayerColor(self):
        return self.color


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(Options.Spritedirectory + image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Element(pygame.sprite.Sprite):
    def __init__(self, Xpos, Ypos, Type, RotatePos, X, Y):
        pygame.sprite.Sprite.__init__(self)

        self.X = X
        self.Y = Y
        self.Xpos = Xpos
        self.Ypos = Ypos
        self.Type = Type
        self.RotatePos = RotatePos
        self.goal = -1

        self.image_file = GetImageFileName(self.Type)

        self.image = pygame.image.load(Options.Spritedirectory + self.image_file)
        self.image = pygame.transform.rotate(self.image, RotatePos)
        self.rect = self.image.get_rect(topleft=(Xpos, Ypos))

    def EraseGoal(self):
        self.goal = -1
        self.Draw()

    def SetElementGoal(self, PlayerNo):
        # print(" SetElementGoal:PlayerNo = ", PlayerNo)
        self.goal = PlayerNo
        self.DrawGoal()

    def GetGoal(self):
        return self.goal

    def Draw(self):
        screen.blit(self.image, self.rect)

    def DrawGoal(self):
        PlayerNo = self.GetGoal()
        # print(" DrawGoal:PlayerNo = ", PlayerNo)
        if PlayerNo != -1:
            color = Options.PlayersStandartPoses[PlayerNo][2]
            pygame.draw.line(screen, pygame.Color(color), (self.Xpos + 10, self.Ypos + 10),
                             (self.Xpos + Options.SpriteSize - 10, self.Ypos + Options.SpriteSize - 10), 10)
            pygame.draw.line(screen, pygame.Color(color), (self.Xpos + 10, self.Ypos + Options.SpriteSize - 10),
                             (self.Xpos + Options.SpriteSize - 10, self.Ypos + 10), 10)

    def about(self):
        return (self.X, self.Y)

    def GetParams(self):
        return (self.Type, self.RotatePos, self.X, self.Y, self.Xpos, self.Ypos)

    def GetTypeRot(self):
        return (self.Type, self.RotatePos)

    def GetX(self):
        return self.X

    def GetY(self):
        return self.Y

    def GetXPos(self):
        return self.Xpos

    def SetX(self, X):
        self.X = X
        self.Xpos = Options.LeftIndent + Options.SpriteSize * X

    def SetY(self, Y):
        self.Y = Y
        self.Ypos = Options.TopIndent + Options.SpriteSize * Y

    def GetRotatePos(self):
        return self.RotatePos

    def SetRotatePos(self, RotatePos):
        self.RotatePos = RotatePos

    def GetYPos(self):
        return self.Ypos

    def Hit(self, MousePos):
        if self.Xpos <= MousePos[0] and self.Xpos + Options.SpriteSize >= MousePos[0] and self.Ypos <= MousePos[
            1] and self.Ypos + Options.SpriteSize >= MousePos[1]:
            return True
        else:
            return False


class Board():
    def __init__(self):
        self.board = [[0] * 7 for _ in range(7)]
        self.Arrows = []
        self.Turn = 0
        self.TurnType = True
        self.Players = []

        self.FreeEl = Element(9.5 * Options.SpriteSize + Options.LeftIndent,
                              0.75 * Options.SpriteSize + Options.TopIndent, 1, random.randint(0, 3) * 90, 9, 1)
        screen.blit(self.FreeEl.image, self.FreeEl.rect)

        self.CashEl = Element(10 * Options.SpriteSize + Options.LeftIndent,
                              2 * Options.SpriteSize + Options.TopIndent, 3, 0 * 90, 10, 1)
        # screen.blit(self.CashEl.image, self.CashEl.rect)

        self.AddImmobileSprites()
        self.AddSpritesInRandomMethod()
        self.AddArrows()

    def SetGoal(self, PlayerNo, X, Y):
        Old = self.FindGoalElement(PlayerNo)
        if Old:
            Old.EraseGoal()
        New = self.SelectEl(X, Y)
        New.SetElementGoal(PlayerNo)

    def FindGoalElement(self, PlayerNo):
        for i in self.board:
            for j in i:
                if j.GetGoal() == PlayerNo:
                    return j
        return False

    def FindGoalFreeEls(self, PlayerNo):
        res = []
        for i in self.board:
            for j in i:
                if j.GetGoal() == -1 and PlayerNo != j.GetGoal():
                    res.append(j)
        return res

    def SetRandomGoal(self, PlayerNo):
        Old = self.FindGoalElement(PlayerNo)
        if Old:
            Old.EraseGoal()

        FreeEls = self.FindGoalFreeEls(PlayerNo)
        NewGoalEl = random.choice(FreeEls)
        NewGoalEl.SetElementGoal(PlayerNo)

    def SetRotatePos(self, RotatePos):
        self.FreeEl.SetRotatePos(RotatePos)

    def MoveFreeEement(self, RotateRightSide):
        RotatePos = self.FreeEl.RotatePos
        print(RotatePos)
        RotateTo = 0
        if RotateRightSide:
            if RotatePos == 0:
                RotateTo = 90
            elif RotatePos == 90:
                RotateTo = 180
            elif RotatePos == 180:
                RotateTo = 270
            elif RotatePos == 270:
                RotateTo = 0
        else:
            if RotatePos == 0:
                RotateTo = 270
            elif RotatePos == 90:
                RotateTo = 0
            elif RotatePos == 180:
                RotateTo = 90
            elif RotatePos == 270:
                RotateTo = 180
        self.FreeEl.SetRotatePos(RotateTo)
        self.FreeEl.image = pygame.image.load(Options.Spritedirectory + self.FreeEl.image_file)
        self.FreeEl.image = pygame.transform.rotate(self.FreeEl.image, RotateTo)
        screen.blit(self.FreeEl.image, self.FreeEl.rect)

    def PosibleMove(self, X, Y, Direction):
        From = self.SelectEl(X, Y)
        if Direction == 1:  # Up
            if Y == 0:
                return False
            To = self.SelectEl(X, Y - 1)
            if From.GetTypeRot() in Options.PosibleMovesUp and To.GetTypeRot() in Options.PosibleMovesDown:
                return True
            else:
                return False
        elif Direction == 4:  # Right:
            if X == 6:
                return False
            To = self.SelectEl(X + 1, Y)
            # print("From = ", From.GetTypeRot())
            # print("To = ", To.GetTypeRot())
            if From.GetTypeRot() in Options.PosibleMovesRight and To.GetTypeRot() in Options.PosibleMovesLeft:
                return True
            else:
                return False
        elif Direction == 3:  # Down:
            if Y == 6:
                return False
            To = self.SelectEl(X, Y + 1)
            if From.GetTypeRot() in Options.PosibleMovesDown and To.GetTypeRot() in Options.PosibleMovesUp:
                return True
            else:
                return False
        elif Direction == 2:  # Left:
            if X == 0:
                return False
            To = self.SelectEl(X - 1, Y)
            if From.GetTypeRot() in Options.PosibleMovesLeft and To.GetTypeRot() in Options.PosibleMovesRight:
                return True
            else:
                return False

    def IsWay(self, FromX, FromY, ToX, ToY):
        a = [[100] * 7 for _ in range(7)]
        a[FromX][FromY] = 0
        n = 0
        Found = True
        while a[ToX][ToY] <= 100 and n <= 49 and Found:
            Found = False
            for x in range(7):
                for y in range(7):
                    if a[x][y] == n:
                        Found = True
                        if self.PosibleMove(x, y, 1):  # Up
                            if a[x][y - 1] > n + 1:
                                a[x][y - 1] = n + 1
                        if self.PosibleMove(x, y, 2):  # Left
                            if a[x - 1][y] > n + 1:
                                a[x - 1][y] = n + 1
                        if self.PosibleMove(x, y, 3):  # Down
                            if a[x][y + 1] > n + 1:
                                a[x][y + 1] = n + 1
                        if self.PosibleMove(x, y, 4):  # Right
                            if a[x + 1][y] > n + 1:
                                a[x + 1][y] = n + 1
            n += 1
        # print(n)
        # print(a)
        return not a[ToX][ToY] == 100

    def NextAction(self):
        self.TurnType = not self.TurnType
        menu.ChangeType()
        if self.TurnType:
            self.Turn += 1
            if self.Turn == 4:
                self.Turn = 0
            menu.ChangePlayer(self.Turn)

    def CurentPlayer(self):
        return self.Players[self.Turn]

    def DrawAll(self):
        CreateBackground()
        screen.blit(self.FreeEl.image, self.FreeEl.rect)
        for i in self.board:
            for j in i:
                screen.blit(j.image, j.rect)
                j.DrawGoal()
        for i in self.Players:
            i.draw()
        self.AddArrows()

    def CreatePlayers(self, N):
        for i in range(N):
            # print(i)
            NewPlayer = Player(Options.PlayersStandartPoses[i][0],
                               Options.PlayersStandartPoses[i][1],
                               Options.PlayersStandartPoses[i][2],
                               Options.PlayersStandartPoses[i][3], i)
            self.Players.append(NewPlayer)
            self.SetRandomGoal(i)

    def SelectEl(self, X, Y):
        for Row in self.board:
            for El in Row:
                if El.GetX() == X and El.GetY() == Y:
                    return El

    def MoveElement(self, El, NewX, NewY):
        # print("Двигаем ", El.GetParams(), " в ", (NewX, NewY))
        El.SetX(NewX)
        El.SetY(NewY)
        # print("После перемещения ", El.GetParams())
        El.rect = El.image.get_rect(topleft=(El.GetXPos(), El.GetYPos()))
        screen.blit(El.image, El.rect)

    def FindPlayers(self, X, Y):
        res = []
        for i in self.Players:
            if i.GetX() == X and i.GetY() == Y:
                res.append(i)
        return res

    def MoveRow(self, Y, Direction):
        if Direction:
            BadEl = self.SelectEl(6, Y)
            # print("BadEl = ", BadEl.GetParams())
            # print("FreeEl = ", self.FreeEl.GetParams())
            self.SetFree(BadEl)
            for i in range(5, -1, -1):
                # print(i)
                self.MoveElement(self.SelectEl(i, Y), i + 1, Y)
            self.MoveElement(BadEl, 0, Y)
            self.ExtractCash(BadEl)
            for i in self.Players:
                if i.GetY() == Y:
                    if i.GetX() == 6:
                        i.SetCords(0, Y)
                    else:
                        i.SetCords(i.GetX() + 1, Y)

        else:
            BadEl = self.SelectEl(0, Y)
            # print("BadEl = ", BadEl.GetParams())
            # print("FreeEl = ", self.FreeEl.GetParams())
            self.SetFree(BadEl)
            for i in range(1, 7):
                # print(i)
                self.MoveElement(self.SelectEl(i, Y), i - 1, Y)
            self.MoveElement(BadEl, 6, Y)
            self.ExtractCash(BadEl)
            for i in self.Players:
                if i.GetY() == Y:
                    if i.GetX() == 0:
                        i.SetCords(6, Y)
                    else:
                        i.SetCords(i.GetX() - 1, Y)

    def MoveCol(self, X, Direction):
        if Direction:
            BadEl = self.SelectEl(X, 6)
            # print("BadEl = ", BadEl.GetParams())
            # print("FreeEl = ", self.FreeEl.GetParams())
            self.SetFree(BadEl)
            for i in range(5, -1, -1):
                # print(i)
                self.MoveElement(self.SelectEl(X, i), X, i + 1)
            self.MoveElement(BadEl, X, 0)
            self.ExtractCash(BadEl)
            for i in self.Players:
                if i.GetX() == X:
                    if i.GetY() == 6:
                        i.SetCords(X, 0)
                    else:
                        i.SetCords(X, i.GetY() + 1)
        else:
            BadEl = self.SelectEl(X, 0)
            # print("BadEl = ", BadEl.GetParams())
            # print("FreeEl = ", self.FreeEl.GetParams())
            self.SetFree(BadEl)
            for i in range(1, 7):
                # print(i)
                self.MoveElement(self.SelectEl(X, i), X, i - 1)
            self.MoveElement(BadEl, X, 6)
            self.ExtractCash(BadEl)
            for i in self.Players:
                if i.GetX() == X:
                    if i.GetY() == 0:
                        i.SetCords(X, 6)
                    else:
                        i.SetCords(X, i.GetY() - 1)

    def SetFree(self, El):
        # print("Записываем в свободный элемент  = ", El.GetParams())
        self.SetCash(self.FreeEl)
        NewFreeParams = El.GetParams()
        self.FreeEl.Type = NewFreeParams[0]
        self.FreeEl.RotatePos = NewFreeParams[1]
        # print("Свободный элемент  = ", self.FreeEl.GetParams())

        self.FreeEl.image_file = GetImageFileName(self.FreeEl.Type)

        self.FreeEl.image = pygame.image.load(Options.Spritedirectory + self.FreeEl.image_file)
        self.FreeEl.image = pygame.transform.rotate(self.FreeEl.image, self.FreeEl.RotatePos)
        screen.blit(self.FreeEl.image, self.FreeEl.rect)

    def SetCash(self, El):
        # print("Записываем в кэш в элемент ", El.GetParams())
        NewCashParams = El.GetParams()
        self.CashEl.Type = NewCashParams[0]
        self.CashEl.RotatePos = NewCashParams[1]

        # self.CashEl.image_file = GetImageFileName(self.CashEl.Type)

        # self.CashEl.image = pygame.image.load(Options.Spritedirectory + self.CashEl.image_file)
        # self.CashEl.image = pygame.transform.rotate(self.CashEl.image, self.CashEl.RotatePos)
        # screen.blit(self.CashEl.image, self.CashEl.rect)
        # print("Кэш = ", El.GetParams())

    def ExtractCash(self, El):
        # print("Извлекаем из кэша в элемент ", El.GetParams())
        # print("Кэш в момент извлечения", self.CashEl.GetParams())
        CashParams = self.CashEl.GetParams()
        El.Type = CashParams[0]
        El.RotatePos = CashParams[1]
        # print("Элемент после извлечения из кэша", El.GetParams())
        El.image_file = GetImageFileName(El.Type)
        El.image = pygame.image.load(Options.Spritedirectory + El.image_file)
        El.image = pygame.transform.rotate(El.image, El.RotatePos)
        screen.blit(El.image, El.rect)

    def GetPushedSprite(self, Position):
        for CurRow in self.board:
            for CurEl in CurRow:
                if CurEl.Hit(Position):
                    return CurEl

    def GetPushedArrow(self, Position):
        for CurArr in self.Arrows:
            if CurArr.Hit(Position):
                return CurArr

    def AddImmobileSprites(self):
        Xcounter = 0
        Ycounter = 0
        for i in Options.NotPosibleToMoveMapSprites:
            Sprite = Element(Options.SpriteSize * i[0] + Options.LeftIndent,
                             Options.SpriteSize * i[1] + Options.TopIndent,
                             i[2], i[3], i[0], i[1])
            screen.blit(Sprite.image, Sprite.rect)
            self.board[Xcounter][Ycounter] = Sprite
            Xcounter += 2
            if Xcounter == 8:
                Xcounter = 0
                Ycounter += 2

    def AddSpritesInRandomMethod(self):
        FreePlacesToAddSprites = Options.FreePlacesToAddSprites
        random.shuffle(FreePlacesToAddSprites)
        for i in range(Options.RotateSprites):
            Cords = FreePlacesToAddSprites.pop(0)
            Sprite = Element(Cords[0] * Options.SpriteSize + Options.LeftIndent,
                             Cords[1] * Options.SpriteSize + Options.TopIndent, 1, random.randint(0, 3) * 90, Cords[0],
                             Cords[1])
            screen.blit(Sprite.image, Sprite.rect)
            self.board[Cords[0]][Cords[1]] = Sprite
        for i in range(Options.LineSprites):
            Cords = FreePlacesToAddSprites.pop(0)
            Sprite = Element(Cords[0] * Options.SpriteSize + Options.LeftIndent,
                             Cords[1] * Options.SpriteSize + Options.TopIndent, 2, random.randint(0, 3) * 90, Cords[0],
                             Cords[1])
            screen.blit(Sprite.image, Sprite.rect)
            self.board[Cords[0]][Cords[1]] = Sprite
        for i in range(Options.CrossSprites):
            Cords = FreePlacesToAddSprites.pop(0)
            Sprite = Element(Cords[0] * Options.SpriteSize + Options.LeftIndent,
                             Cords[1] * Options.SpriteSize + Options.TopIndent, 3, random.randint(0, 3) * 90, Cords[0],
                             Cords[1])
            screen.blit(Sprite.image, Sprite.rect)
            self.board[Cords[0]][Cords[1]] = Sprite

    def AddArrows(self):
        for i in range(1, 4):
            arrow = Arrow(Options.LeftIndent - Options.SpriteSize + (i * (Options.SpriteSize * 2)),
                          Options.TopIndent - Options.SpriteSize, 180, (i - 1) * 2 + 1, -1)
            screen.blit(arrow.image, arrow.rect)
            self.Arrows.append(arrow)

        for i in range(1, 4):
            arrow = Arrow(Options.LeftIndent - Options.SpriteSize + (i * (Options.SpriteSize * 2)),
                          Options.TopIndent + Options.SpriteSize * 7, 0, (i - 1) * 2 + 1, 7)
            screen.blit(arrow.image, arrow.rect)
            self.Arrows.append(arrow)

        for i in range(3):
            arrow = Arrow(Options.LeftIndent - Options.SpriteSize,
                          (Options.TopIndent + Options.SpriteSize) + (i * 2 * Options.SpriteSize), 270, -1, (i) * 2 + 1)
            screen.blit(arrow.image, arrow.rect)
            self.Arrows.append(arrow)

        for i in range(3):
            arrow = Arrow(Options.LeftIndent + (7 * Options.SpriteSize),
                          (Options.TopIndent + Options.SpriteSize) + (i * 2 * Options.SpriteSize), 90, 7, (i) * 2 + 1)
            screen.blit(arrow.image, arrow.rect)
            self.Arrows.append(arrow)


class Arrow(pygame.sprite.Sprite):
    def __init__(self, Xpos, Ypos, RotatePos, X, Y):
        pygame.sprite.Sprite.__init__(self)

        self.Xpos = Xpos
        self.Ypos = Ypos
        self.X = X
        self.Y = Y
        self.RotatePos = RotatePos

        self.image = pygame.image.load(Options.Spritedirectory + Options.ArrowFile)
        self.image = pygame.transform.rotate(self.image, RotatePos)
        self.rect = self.image.get_rect(topleft=(Xpos, Ypos))

    def HorOrVert(self):
        if self.RotatePos == 90 or self.RotatePos == 270:
            return True
        else:
            return False

    def Direction(self):
        if self.RotatePos == 180 or self.RotatePos == 270:
            return True
        else:
            return False

    def GetX(self):
        return self.X

    def GetY(self):
        return self.Y

    def GetXPos(self):
        return self.XPos

    def GetYPos(self):
        return self.YPos

    def GetRotatePos(self):
        return self.RotatePos

    def Hit(self, MousePos):
        if self.Xpos <= MousePos[0] and self.Xpos + Options.SpriteSize >= MousePos[0] and self.Ypos <= MousePos[
            1] and self.Ypos + Options.SpriteSize >= MousePos[1]:
            return True
        else:
            return False

    def about(self):
        return (self.X, self.Y, self.RotatePos)


class Statusmenu(pygame.sprite.Sprite):
    def __init__(self, player=0, type=False):
        self.player = player
        self.type = type

    def ChangeType(self):
        self.type = not self.type

    def ChangePlayer(self, player):
        self.player = player

    def draw(self):
        font = pygame.font.Font(None, 50)
        if self.type:
            text = font.render(f"Ходит фишкой", True, pygame.Color(Options.PlayersStandartPoses[self.player][2]))
        else:
            text = font.render(f"Двигает карточки", True, pygame.Color(Options.PlayersStandartPoses[self.player][2]))
        text_x = Options.menu[0] - text.get_width() // 2
        text_y = Options.menu[1] // 2 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, pygame.Color(Options.PlayersStandartPoses[self.player][2]),
                         (text_x - 10, text_y - 10,
                          text_w + 20, text_h + 20), 7)


def CreateBackground():
    for i in range(size[0] // Options.BackGroundSizeImageX + 1):
        for j in range(size[1] // Options.BackGroundSizeImageY + 1):
            BackGround = Background(Options.BackGroundFileName,
                                    [Options.BackGroundSizeImageX * i, Options.BackGroundSizeImageY * j])
            screen.blit(BackGround.image, BackGround.rect)


def MouseLeftButtonClick(board, MousePos):
    El = board.GetPushedSprite(event.pos)
    if El:
        if not board.TurnType:
            player = board.CurentPlayer()
            if board.IsWay(player.GetX(), player.GetY(), El.GetX(), El.GetY()):
                if El.goal != -1:
                    if board.Players[El.goal] == player:
                        board.SetRandomGoal(El.goal)
                        player.RiseScore()
                player.SetCords(El.GetX(), El.GetY())
                board.NextAction()

    Arr = board.GetPushedArrow(MousePos)
    if Arr and board.TurnType:
        if Arr.HorOrVert():
            board.MoveRow(Arr.GetY(), Arr.Direction())
        else:
            board.MoveCol(Arr.GetX(), Arr.Direction())
        board.NextAction()


def GetImageFileName(Type):
    if Type == 1:
        return Options.Type1Sprite
    elif Type == 2:
        return Options.Type2Sprite
    else:
        return Options.Type3Sprite


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Лабиринт')
    size = Options.Screen
    screen = pygame.display.set_mode(size)
    running = True
    CreateBackground()
    menu = Statusmenu()
    menu.draw()
    board = Board()
    board.CreatePlayers(4)
    board.DrawAll()
    scorebar = Scorebar(4)
    scorebar.draw()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # левая кнопка мыши
                    MouseLeftButtonClick(board, event.pos)
                    board.DrawAll()
                    menu.draw()
                    scorebar.draw()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    board.MoveFreeEement(True)
                elif event.key == pygame.K_RIGHT:
                    board.MoveFreeEement(False)
                board.DrawAll()
                scorebar.draw()
                menu.draw()
            pygame.display.flip()
    pygame.quit()
