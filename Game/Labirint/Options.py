# Screen
Screen = 1000, 700
menu = 815, 100

# BackGround
BackGroundFileName = "dirt2.png"
BackGroundSizeImageX = 64
BackGroundSizeImageY = 64

# Sprites
Spritedirectory = 'data/'
Type1Sprite = 'Rotate.png'  # Rotate  1
Type2Sprite = '2ways.png'  # Line    2
Type3Sprite = '3ways.png'  # Cross   3
ArrowFile = 'Arrow.png'
SpriteSize = 64

# MapSprites
NotPosibleToMoveMapSprites = [[0, 0, 1, 0], [2, 0, 3, 270], [4, 0, 3, 270], [6, 0, 1, 270],
                              [0, 2, 3, 0], [2, 2, 3, 0], [4, 2, 3, 270], [6, 2, 3, 180],
                              [0, 4, 3, 0], [2, 4, 3, 90], [4, 4, 3, 180], [6, 4, 3, 180],
                              [0, 6, 1, 90], [2, 6, 3, 90], [4, 6, 3, 90], [6, 6, 1, 180]]

FreePlacesToAddSprites = [(1, 0), (3, 0), (5, 0),
                          (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1),
                          (1, 2), (3, 2), (5, 2),
                          (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3),
                          (1, 4), (3, 4), (5, 4),
                          (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5),
                          (1, 6), (3, 6), (5, 6),
                          ]
PosibleMovesUp = [(1, 90), (1, 180), (2, 0), (2, 180), (3, 0), (3, 90), (3, 180)]
PosibleMovesDown = [(1, 0), (1, 270), (2, 0), (2, 180), (3, 0), (3, 270), (3, 180)]
PosibleMovesLeft = [(1, 180), (1, 270), (2, 90), (2, 270), (3, 90), (3, 180), (3, 270)]
PosibleMovesRight = [(1, 0), (1, 90), (2, 90), (2, 270), (3, 0), (3, 90), (3, 270)]


RotateSprites = 15
LineSprites = 12
CrossSprites = 6

# indent (отступы)
LeftIndent = 150
TopIndent = 50

# players
PlayersStandartPoses = [[0, 0, 'blue', (4, 4)],
                        [6, 6, 'green', (4, 28)],
                        [0, 6, 'orange', (28, 4)],
                        [6, 0, 'red', (28, 28)]]
