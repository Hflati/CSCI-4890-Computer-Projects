import pygame
pygame.init()

#Initialization Variables For The Game
height = 950
width = 1000
screen = pygame.display.set_mode([width, height])
surface = pygame.Surface((width, height), pygame.SRCALPHA)
smallestFont = pygame.font.SysFont('Times New Roman', 24)
smallFont = pygame.font.SysFont('Times New Roman', 32)
mediumFont = pygame.font.SysFont('Times New Roman', 50)
largeFont = pygame.font.SysFont('Times New Roman', 65)
pygame.display.set_caption('Hunter Flati Chess Project')
timer = pygame.time.Clock()
fps = 60
color = (64, 64, 64)
mainMenu = True

#All Chess Pieces
pieces = ['Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Pawn']

#White Pieces
whitePieces = ['Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook',
               'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn']

whiteRook = pygame.image.load('..\Chess Pieces\White Pieces\White Rook.png')
whiteRook = pygame.transform.scale(whiteRook, (80, 80))
whiteRookCaptured = pygame.transform.scale(whiteRook, (45, 45))

whiteKnight = pygame.image.load('..\Chess Pieces\White Pieces\White Knight.png')
whiteKnight = pygame.transform.scale(whiteKnight, (80, 80))
whiteKnightCaptured = pygame.transform.scale(whiteKnight, (45, 45))

whiteBishop = pygame.image.load('..\Chess Pieces\White Pieces\White Bishop.png')
whiteBishop = pygame.transform.scale(whiteBishop, (80, 80))
whiteBishopCaptured = pygame.transform.scale(whiteBishop, (45, 45))

whiteKing = pygame.image.load('..\Chess Pieces\White Pieces\White King.png')
whiteKing = pygame.transform.scale(whiteKing, (80, 80))
whiteKingCaptured = pygame.transform.scale(whiteKing, (45, 45))

whiteQueen = pygame.image.load('..\Chess Pieces\White Pieces\White Queen.png')
whiteQueen = pygame.transform.scale(whiteQueen, (80, 80))
whiteQueenCaptured = pygame.transform.scale(whiteQueen, (45, 45))

whitePawn = pygame.image.load('..\Chess Pieces\White Pieces\White Pawn.png')
whitePawn = pygame.transform.scale(whitePawn, (60, 60))
whitePawnCaptured = pygame.transform.scale(whitePawn, (45, 45))

whitePictures = [whiteRook, whiteKnight, whiteBishop, whiteQueen, whiteKing, whitePawn]
whitePicturesCaptured = [whiteRookCaptured, whiteKnightCaptured, whiteBishopCaptured, whiteQueenCaptured, whiteKingCaptured, whitePawnCaptured]
whitePromotions = ['Rook', 'Knight', 'Bishop', 'Queen']
whiteMoved = [False, False, False, False, False, False, False, False,
              False, False, False, False, False, False, False, False]

whitePiecesLocation = [(0,7), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7),
                       (0,6), (1,6), (2,6), (3,6), (4,6), (5,6), (6,6), (7,6)]

whiteCaptured = []

#Black Pieces
blackPieces = ['Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook',
               'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn']

blackRook = pygame.image.load('..\Chess Pieces\Black Pieces\Black Rook.png')
blackRook = pygame.transform.scale(blackRook, (80, 80))
blackRookCaptured = pygame.transform.scale(blackRook, (45, 45))

blackKnight = pygame.image.load('..\Chess Pieces\Black Pieces\Black Knight.png')
blackKnight = pygame.transform.scale(blackKnight, (80, 80))
blackKnightCaptured = pygame.transform.scale(blackKnight, (45, 45))

blackBishop = pygame.image.load('..\Chess Pieces\Black Pieces\Black Bishop.png')
blackBishop = pygame.transform.scale(blackBishop, (80, 80))
blackBishopCaptured = pygame.transform.scale(blackBishop, (45, 45))

blackKing = pygame.image.load('..\Chess Pieces\Black Pieces\Black King.png')
blackKing = pygame.transform.scale(blackKing, (80, 80))
blackKingCaptured = pygame.transform.scale(blackKing, (45, 45))

blackQueen = pygame.image.load('..\Chess Pieces\Black Pieces\Black Queen.png')
blackQueen = pygame.transform.scale(blackQueen, (80, 80))
blackQueenCaptured = pygame.transform.scale(blackQueen, (45, 45))

blackPawn = pygame.image.load('..\Chess Pieces\Black Pieces\Black Pawn.png')
blackPawn = pygame.transform.scale(blackPawn, (60, 60))
blackPawnCaptured = pygame.transform.scale(blackPawn, (45, 45))

blackPictures = [blackRook, blackKnight, blackBishop, blackQueen, blackKing, blackPawn]
blackPicturesCaptured = [blackRookCaptured, blackKnightCaptured, blackBishopCaptured, blackQueenCaptured, blackKingCaptured, blackPawnCaptured]
blackPromotions = ['Rook', 'Knight', 'Bishop', 'Queen']
blackMoved = [False, False, False, False, False, False, False, False,
              False, False, False, False, False, False, False, False]

blackPiecesLocation = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0),
                       (0,1), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1)]

blackCaptured = []

#Tutroial Images
rightArrow = pygame.image.load('..\Misc. Images\Right Arrow.png')
rightArrow = pygame.transform.scale(rightArrow, (60, 60))

leftArrow = pygame.image.load('..\Misc. Images\Left Arrow.png')
leftArrow = pygame.transform.scale(leftArrow, (60, 60))

pawnPromotionPictureSmall = pygame.image.load('..\Misc. Images\Pawn Promotion.png')
pawnPromotionPictureSmall = pygame.transform.scale(pawnPromotionPictureSmall, (350, 350))
enPassantPictureSmall = pygame.image.load('..\Misc. Images\En Passant.png')
enPassantPictureSmall = pygame.transform.scale(enPassantPictureSmall, (350, 350))
castlingPictureSmall = pygame.image.load('..\Misc. Images\Castling.png')
castlingPictureSmall = pygame.transform.scale(castlingPictureSmall, (350, 350))
pawnPromotionPictureBig = pygame.image.load('..\Misc. Images\Pawn Promotion.png')
pawnPromotionPictureBig = pygame.transform.scale(pawnPromotionPictureBig, (600, 600))
enPassantPictureBig = pygame.image.load('..\Misc. Images\En Passant.png')
enPassantPictureBig = pygame.transform.scale(enPassantPictureBig, (600, 600))
castlingPictureBig = pygame.image.load('..\Misc. Images\Castling.png')
castlingPictureBig = pygame.transform.scale(castlingPictureBig, (600, 600))

#SFX
pieceMovingSFX = pygame.mixer.Sound('..\SFX\Piece Moving SFX.mp3')
pieceCapturedSFX = pygame.mixer.Sound('..\SFX\Piece Captured SFX.mp3')
checkSFX = pygame.mixer.Sound('..\SFX\Check SFX.mp3')
checkSFX.set_volume(0.5)
victorySFX = pygame.mixer.Sound('..\SFX\Victory SFX.mp3')
victorySFX.set_volume(0.5)
promoteSFX = pygame.mixer.Sound('..\SFX\Promote SFX.mp3')
pageFlipSFX = pygame.mixer.Sound('..\SFX\Page Flip SFX.mp3')

#Handles Which Player's Turn it is and List of Possible Moves to Make on That Turn
turn = 0
selection = -1
possibleMoves = []
counter = 0
winner = ''
gameOver = False
whiteEnPassant = (111, 111)
blackEnPassant = (111, 111)
whitePromote = False
blackPromote = False
promoteIndex = -1
global inCheck
inCheck = False
castleMoves = []
mainMenu = True
runMainMenu = True
runGame = False
runTutorial = False
runCPUGame = False

class Button:
    def __init__(self, txt, pos):
        self.text = txt
        self.pos = pos
        self.button = pygame.rect.Rect((self.pos[0], self.pos[1]), (400, 100))

    def draw(self):
        pygame.draw.rect(screen, 'light gray', self.button, 0, 10)
        pygame.draw.rect(screen, 'dark gray', [self.pos[0], self.pos[1], 400, 100], 0, 5)
        text = mediumFont.render(self.text, True, 'black')
        screen.blit(text, (self.pos[0] + 25, self.pos[1] + 20))

    def checkClicked(self):
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False