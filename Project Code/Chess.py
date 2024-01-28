import pygame

#Initialization of Pygames
pygame.init()
height = 950
width = 1000
screen = pygame.display.set_mode([width, height])
surface = pygame.Surface((width, height), pygame.SRCALPHA)
smallFont = pygame.font.SysFont('Times New Roman', 50)
largeFont = pygame.font.SysFont('Times New Roman', 65)
pygame.display.set_caption('Hunter Flati Chess Project')
timer = pygame.time.Clock()
fps = 60
color = (64, 64, 64)

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

blackPiecesLocation = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0),
                       (0,1), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1)]

blackCaptured = []

#Handles Which Player's Turn it is and List of Possible Moves to Make on That Turn
turn = 0
selection = 1111
possibleMoves = []
counter = 0
winner = ''
gameOver = False

#Draws the Board
def drawBoard():
    for i in range(32):
        column = (i % 4) - 0.75
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'cornsilk1', [500 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'cornsilk1', [600 - (column * 200), row * 100, 100, 100])

        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 100 * i), (850, 100 *i), 3)
            pygame.draw.line(screen, 'black', (50 + (100 * i), 0), (50 +(100 * i), 850), 3)

        pygame.draw.rect(screen, (85, 47, 0), [50, 800, 800, 50])
        pygame.draw.rect(screen, 'black', [50, 0, 800, 800], 4)
        pygame.draw.rect(screen, (85, 47, 0), [0, 0, 50, 850])
        pygame.draw.rect(screen, 'black', [847, 0, 153, 800], 4)
        pygame.draw.rect(screen, 'black', [0, 850, 850, 100], 4)
        pygame.draw.rect(screen, 'black', [847, 797, 153, 153], 4)

        gameplayText = ['White, Please Select a Piece', 'White, Please Select a Location', 
                        'Black, Please Select a Piece', 'Black, Please Select a Location']
        screen.blit(largeFont.render(gameplayText[turn], True, 'white'), (15, 865))
        
        #Row Numbers
        screen.blit(smallFont.render('8', True, 'white'), (15, 25))
        screen.blit(smallFont.render('7', True, 'white'), (15, 125))
        screen.blit(smallFont.render('6', True, 'white'), (15, 225))
        screen.blit(smallFont.render('5', True, 'white'), (15, 325))
        screen.blit(smallFont.render('4', True, 'white'), (15, 425))
        screen.blit(smallFont.render('3', True, 'white'), (15, 525))
        screen.blit(smallFont.render('2', True, 'white'), (15, 625))
        screen.blit(smallFont.render('1', True, 'white'), (15, 725))
        #Column Letters
        screen.blit(smallFont.render('a', True, 'white'), (90, 793))
        screen.blit(smallFont.render('b', True, 'white'), (190, 793))
        screen.blit(smallFont.render('c', True, 'white'), (290, 793))
        screen.blit(smallFont.render('d', True, 'white'), (390, 793))
        screen.blit(smallFont.render('e', True, 'white'), (490, 793))
        screen.blit(smallFont.render('f', True, 'white'), (590, 793))
        screen.blit(smallFont.render('g', True, 'white'), (690, 793))
        screen.blit(smallFont.render('h', True, 'white'), (790, 793))

#Putting the Pieces on the Board
def drawPieces():
    for i in range(len(whitePieces)):
        index = pieces.index(whitePieces[i])
        if whitePieces[i] == 'Pawn':
            screen.blit(whitePawn, (whitePiecesLocation[i][0] * 100 + 70, whitePiecesLocation[i][1] * 100 + 25))
        else:
            screen.blit(whitePictures[index], (whitePiecesLocation[i][0] * 100 + 60, whitePiecesLocation[i][1] * 100 + 12))
        
        if turn < 2:
            if selection == i:
                pygame.draw.rect(screen, 'dodgerblue', [whitePiecesLocation[i][0] * 100 + 52, whitePiecesLocation[i][1] * 100 + 1, 97, 97], 2)
        if turn >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'firebrick1', [blackPiecesLocation[i][0] * 100 + 52, blackPiecesLocation[i][1] * 100 + 1, 97, 97], 2)

    for i in range(len(blackPieces)):
        index = pieces.index(blackPieces[i])
        if blackPieces[i] == 'Pawn':
            screen.blit(blackPawn, (blackPiecesLocation[i][0] * 100 + 70, blackPiecesLocation[i][1] * 100 + 25))
        else:
            screen.blit(blackPictures[index], (blackPiecesLocation[i][0] * 100 + 60, blackPiecesLocation[i][1] * 100 + 12))

#Check Valid Move Options on Board for Pieces
def checkMoveOptions(pieces, locations, turns):
    moveList = []
    totalMoveList = []

    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'Pawn':
            moveList = checkPawnMoves(location, turns)
        elif piece == 'Rook':
            moveList = checkRookMoves(location, turns)
        elif piece == 'Knight':
            moveList = checkKnightMoves(location, turns)
        elif piece == 'Bishop':
            moveList = checkBishopMoves(location, turns)
        elif piece == 'Queen':
            moveList = checkQueenMoves(location, turns)
        elif piece == 'King':
            moveList = checkKingMoves(location, turns)

        totalMoveList.append(moveList)

    return totalMoveList

#Check Possible Moves for Selected Piece
def checkPossibleMoves():
    if turn < 2:
        moveOptionsList = whiteMoveOptions
    else:
        moveOptionsList = blackMoveOptions

    possibleMoveOptions = moveOptionsList[selection]

    return possibleMoveOptions

#Check Possible Pawn Moves
def checkPawnMoves(position, color):
    moveList = []
#White Pawn Moves
    if color == 'White':
        if (position[0], position[1] - 1) not in whitePiecesLocation and (position[0], position[1] - 1) not in blackPiecesLocation and position[1] > 0:
            moveList.append((position[0], position[1] - 1))

        if (position[0], position[1] - 2) not in whitePiecesLocation and (position[0], position[1] - 2) not in blackPiecesLocation and position[1] == 6:
            moveList.append((position[0], position[1] - 2))

        if (position[0] + 1, position[1] - 1) in blackPiecesLocation:
            moveList.append((position[0] + 1, position[1] - 1))

        if (position[0] - 1, position[1] - 1) in blackPiecesLocation:
            moveList.append((position[0] - 1, position[1] - 1))
#Black Pawn Moves
    else:
        if (position[0], position[1] + 1) not in whitePiecesLocation and (position[0], position[1] + 1) not in blackPiecesLocation and position[1] < 7:
            moveList.append((position[0], position[1] + 1))

        if (position[0], position[1] + 2) not in whitePiecesLocation and (position[0], position[1] + 2) not in blackPiecesLocation and position[1] == 1:
            moveList.append((position[0], position[1] + 2))

        if (position[0] + 1, position[1] + 1) in whitePiecesLocation:
            moveList.append((position[0] + 1, position[1] + 1))

        if (position[0] - 1, position[1] + 1) in whitePiecesLocation:
            moveList.append((position[0] - 1, position[1] + 1))

    return moveList

#Check Possible Rook Moves
def checkRookMoves(position, color):
    moveList = []
    if color == 'White':
        enemyList = blackPiecesLocation
        friendList = whitePiecesLocation
    
    else:
        enemyList = whitePiecesLocation
        friendList = blackPiecesLocation

#Checks Up, Down, Left, and Right Directions
    for i in range(4):
        pathway = True
        chain = 1

#Check Up 
        if i == 0:
            x = 0
            y = -1

#Check Down
        elif i == 1:
            x = 0
            y = 1

#Check Left
        elif i == 2:
            x = -1
            y = 0

#Check Right
        else:
            x = 1
            y = 0

        while pathway:
            if(position[0] + (chain * x), position[1] + (chain * y)) not in friendList and 0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moveList.append((position[0] + (chain * x), position[1] + (chain * y)))

                if(position[0] + (chain * x), position[1] + (chain * y)) in enemyList:
                    pathway = False
                chain += 1

            else:
                pathway = False

    return moveList

#Check Possible Knight Moves
def checkKnightMoves(position, color):
    moveList = []
    if color == 'White':
        friendList = whitePiecesLocation
    
    else:
        friendList = blackPiecesLocation

#All Knight Moves (2 Squares One Direction, 1 Square Another)
    targetSquares = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]

    for i in range(8):
        targets = (position[0] + targetSquares[i][0], position[1] + targetSquares[i][1])

        if targets not in friendList and 0 <= targets[0] <= 7 and 0 <= targets[1] <= 7:
            moveList.append(targets)

    return moveList

#Check Possible Bishop Moves
def checkBishopMoves(position, color):
    moveList = []
    if color == 'White':
        enemyList = blackPiecesLocation
        friendList = whitePiecesLocation
    
    else:
        enemyList = whitePiecesLocation
        friendList = blackPiecesLocation

#Checks NorthEast, NorthWest, SouthEast, and SouthWest Directions
    for i in range(4):
        pathway = True
        chain = 1

#Check NorthEast
        if i == 0:
            x = 1
            y = -1

#Check NorthWest
        elif i == 1:
            x = -1
            y = -1

#Check SouthEast
        elif i == 2:
            x = 1
            y = 1

#Check SouthWest
        else:
            x = -1
            y = 1

        while pathway:
            if(position[0] + (chain * x), position[1] + (chain * y)) not in friendList and 0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moveList.append((position[0] + (chain * x), position[1] + (chain * y)))

                if(position[0] + (chain * x), position[1] + (chain * y)) in enemyList:
                    pathway = False
                chain += 1

            else:
                pathway = False

    return moveList

#Check Possible Queen Moves
def checkQueenMoves(position, color):
    moveList = checkBishopMoves(position, color)
    moveList2 = checkRookMoves(position, color)
    
    for i in range(len(moveList2)):
        moveList.append(moveList2[i])
    
    return moveList

#Check Possible King Moves
def checkKingMoves(position, color):
    moveList = []
    if color == 'White':
        friendList = whitePiecesLocation
    
    else:
        friendList = blackPiecesLocation

#All King Moves (1 Square in Any Direction)
    targetSquares = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]

    for i in range(8):
        targets = (position[0] + targetSquares[i][0], position[1] + targetSquares[i][1])

        if targets not in friendList and 0 <= targets[0] <= 7 and 0 <= targets[1] <= 7:
            moveList.append(targets)

    return moveList

#Draws Possible Moves on Board
def drawMoves(moves):
    if turn < 2:
        #color = 'dodgerblue'
        for i in range(len(moves)):
            screen.blit(surface, (0, 0))
            pygame.draw.rect(surface, (30, 144, 255, 100), [moves[i][0] * 100 + 56, moves[i][1] * 100 + 5, 90, 90])
            screen.blit(surface, (0, 0))
            pygame.draw.rect(surface, (0, 0, 0, 0), [moves[i][0] * 100 + 56, moves[i][1] * 100 + 5, 90, 90])
            

    else:
        #color = 'firebrick1'
        for i in range(len(moves)):
            screen.blit(surface, (0, 0))
            pygame.draw.rect(surface, (255, 48, 48, 100), [moves[i][0] * 100 + 56, moves[i][1] * 100 + 5, 90, 90])
            screen.blit(surface, (0, 0))
            pygame.draw.rect(surface, (0, 0, 0, 0), [moves[i][0] * 100 + 56, moves[i][1] * 100 + 5, 90, 90])

#Draws Captured Pieces
def drawCapturedPieces():
#Draws Captured Black Pieces 
    for i in range(len(whiteCaptured)):
        capturedPiece = whiteCaptured[i]
        index = pieces.index(capturedPiece)
        screen.blit(blackPicturesCaptured[index], (865, 20 + 50 * i))

#Draws Captured White Pieces 
    for i in range(len(blackCaptured)):
        capturedPiece = blackCaptured[i]
        index = pieces.index(capturedPiece)
        screen.blit(whitePicturesCaptured[index], (935, 20 + 50 * i))

#Flashes Box Around King if in Check
def drawCheck():
    if turn < 2:
        if 'King' in whitePieces:
            kingIndex = whitePieces.index('King')
            kingLocation = whitePiecesLocation[kingIndex]

            for i in range(len(blackMoveOptions)):
                if kingLocation in blackMoveOptions[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'gold', [whitePiecesLocation[kingIndex][0] * 100 + 52, whitePiecesLocation[kingIndex][1] * 100 + 1, 100, 100], 5)

    else:
        if 'King' in blackPieces:
            kingIndex = blackPieces.index('King')
            kingLocation = blackPiecesLocation[kingIndex]

            for i in range(len(whiteMoveOptions)):
                if kingLocation in whiteMoveOptions[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'gold', [blackPiecesLocation[kingIndex][0] * 100 + 52, blackPiecesLocation[kingIndex][1] * 100 + 1, 100, 100], 5)

#Game Over
def drawGameOver():
    pygame.draw.rect(screen, 'Black', [150, 250, 600, 300])
    screen.blit(smallFont.render(f'{winner} Won The Match', True, 'white'), (220, 320))
    screen.blit(smallFont.render(f'Press ENTER to Play Again', True, 'white'), (165, 410))
            
#Game Loop
blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')

run = True
while run:
    timer.tick(fps)

    if counter < 30:
        counter += 1

    else:
        counter = 0

    screen.fill(color)
    drawBoard()
    drawPieces()
    drawCapturedPieces()
    drawCheck()

    if selection != 1111:
        possibleMoves = checkPossibleMoves()
        drawMoves(possibleMoves)

#Clicking Exit Button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

#Allowing the Game to Understand a Left Mouse Button Click for White's Turn
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not gameOver:
            xCoordinate = event.pos[0] // 110
            yCoordinate = event.pos[1] // 100
            click = (xCoordinate, yCoordinate)
            if turn <= 1:
                if click in whitePiecesLocation:
                    selection = whitePiecesLocation.index(click)
                    if turn == 0:
                        turn = 1
                if click in possibleMoves and selection != 1111:
                    whitePiecesLocation[selection] = click
                    if click in blackPiecesLocation:
                        landedOnBlackPiece = blackPiecesLocation.index(click)
                        whiteCaptured.append(blackPieces[landedOnBlackPiece])
                        # If Statement for Black King in Check
                        if blackPieces[landedOnBlackPiece] == 'King':
                            winner = 'White'
                        blackPieces.pop((landedOnBlackPiece))
                        blackPiecesLocation.pop(landedOnBlackPiece)
                    blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                    whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')
                    turn = 2
                    selection = 1111
                    possibleMoves = []

#Allowing the Game to Understand a Left Mouse Button Click for Black's Turn
            if turn > 1:
                if click in blackPiecesLocation:
                    selection = blackPiecesLocation.index(click)
                    if turn == 2:
                        turn = 3
                if click in possibleMoves and selection != 1111:
                    blackPiecesLocation[selection] = click
                    if click in whitePiecesLocation:
                        landedOnWhitePiece = whitePiecesLocation.index(click)
                        blackCaptured.append(whitePieces[landedOnWhitePiece])
                        # If Statement for White King in Check
                        if whitePieces[landedOnWhitePiece] == 'King':
                            winner = 'Black'
                        whitePieces.pop((landedOnWhitePiece))
                        whitePiecesLocation.pop(landedOnWhitePiece)
                    blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                    whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')
                    turn = 0
                    selection = 1111
                    possibleMoves = []

#Reinitialize the Game
        if event.type == pygame.KEYDOWN and gameOver:
            if event.key == pygame.K_RETURN:
                gameOver = False
                winner = ''
                whitePieces = ['Rook', 'Knight', 'Bishop', 'King', 'Queen', 'Bishop', 'Knight', 'Rook',
                               'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn']
                whitePiecesLocation = [(0,7), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7),
                                       (0,6), (1,6), (2,6), (3,6), (4,6), (5,6), (6,6), (7,6)]
                whiteCaptured = []

                blackPieces = ['Rook', 'Knight', 'Bishop', 'King', 'Queen', 'Bishop', 'Knight', 'Rook',
                               'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn']
                blackPiecesLocation = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0),
                                       (0,1), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1)]
                blackCaptured = []

                turn = 0
                selection = 1111
                possibleMoves = []

                blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')

    if winner != '':
        gameOver = True
        drawGameOver()

            

    pygame.display.flip()
pygame.quit()