import pygame
import random
from Variables import *
pygame.init()

#Check Valid Move Options on Board for Pieces
def checkMoveOptions(pieces, locations, turns):
    global castleMoves
    moveList = []
    totalMoveList = []
    castleMoves = []

    #Goes Through Each Movelist per Piece
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
            if inCheck == False:
                moveList, castleMoves = checkKingMoves(location, turns)
            
        totalMoveList.append(moveList)

    return totalMoveList

#Check Possible Moves for Selected Piece
def checkPossibleMoves():
    global inCheck
    global intersectingMoves
    global checkmate
    checkmate = False

    if turn < 2:
        moveOptionsList = whiteMoveOptions
        king_position = whitePiecesLocation[whitePieces.index('King')]
        enemy_moves = blackMoveOptions
        enemy_positions = blackPiecesLocation
    else:
        moveOptionsList = blackMoveOptions
        king_position = blackPiecesLocation[blackPieces.index('King')]
        enemy_moves = whiteMoveOptions
        enemy_positions = whitePiecesLocation

    possibleMoveOptions = moveOptionsList[selection]

    intersectingMoves = []

    # Check if the king is in check
    if kingInCheck():
        inCheck = True
        # Find the attacker's position
        attacker_piece = None  # Initialize the attacker's piece
        for i, moves in enumerate(enemy_moves):
            if king_position in moves:
                attacker_piece = enemy_positions[i]
                print(attacker_piece)  # Get the position of the attacking piece
                break  # Exit the loop once we've found the attacker's position

        # Check if the selected piece can intercept the attacker or block its path
        if selection != -1:
            for move in possibleMoveOptions:
                # Check if the move is to capture the checking piece
                if move == attacker_piece:
                    intersectingMoves.append(move)
                # Check if a friendly piece can block the path of the attacker
                elif selectedPiece != 'King' and isBetween(king_position, move, attacker_piece):
                    intersectingMoves.append(move)
                # Check if the king can escape the check
                elif selectedPiece == 'King' and not kingInCheckAfterMove(king_position, move, enemy_moves):
                    intersectingMoves.append(move)
            # If no piece can intercept, block, or the selected piece is the king, allow the king to move to safety
            if not intersectingMoves:
                for move in possibleMoveOptions:
                    if selectedPiece == 'King' and not kingInCheckAfterMove(king_position, move, enemy_moves):
                        intersectingMoves.append(move)

        #Check for checkmate
        if len(intersectingMoves) == 0:
            checkmate = True

    else:
        # If the king is not in check, allow any possible move for the selected piece
        intersectingMoves = possibleMoveOptions

    return intersectingMoves

#Check if pos2 (Blocking Move) is between pos1 (King in Check) and pos3 (Enemy Attacker) horizontally, vertically, or diagonally
def isBetween(pos1, pos2, pos3):
    #Horizontal (Same x coordinate, pos2 y coordinate is between pos1 and pos3)
    if (pos1[0] == pos2[0] == pos3[0] and (pos1[1] < pos2[1] < pos3[1] or pos1[1] > pos2[1] > pos3[1])):
        return True

    # Vertical (Same y coordinate, pos2 x coordinate is between pos1 and pos3)
    elif (pos1[1] == pos2[1] == pos3[1] and (pos1[0] < pos2[0] < pos3[0] or pos1[0] > pos2[0] > pos3[0])):
        return True

    # Diagonal (pos2 x and y coordinates are between pos1 and pos3)
    elif abs(pos1[0] - pos2[0]) == abs(pos1[1] - pos2[1]) and abs(pos1[0] - pos3[0]) == abs(pos1[1] - pos3[1]) and abs(
            pos2[0] - pos3[0]) == abs(pos2[1] - pos3[1]):
        return True

    return False

#Check if king is in check after moving
def kingInCheckAfterMove(king_position, move, enemy_moves):
    # Simulate the king's move and check if it is still under attack after the move
    for moves in enemy_moves:
        if move in moves:
            return True
    return False

#Check Possible Pawn Moves
def checkPawnMoves(position, color):
    moveList = []
#White Pawn Moves
    if color == 'White':
        if (position[0], position[1] - 1) not in whitePiecesLocation and (position[0], position[1] - 1) not in blackPiecesLocation and position[1] > 0:
            moveList.append((position[0], position[1] - 1))
            if (position[0], position[1] - 2) not in whitePiecesLocation and (position[0], position[1] - 2) not in blackPiecesLocation and position[1] == 6:
                moveList.append((position[0], position[1] - 2))

        #Capture Moves
        if (position[0] + 1, position[1] - 1) in blackPiecesLocation:
            moveList.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in blackPiecesLocation:
            moveList.append((position[0] - 1, position[1] - 1))

        #En Passant Capture Checking
        if (position[0] + 1, position[1] - 1) == blackEnPassant:
            moveList.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) == blackEnPassant:
            moveList.append((position[0] - 1, position[1] - 1))
            
#Black Pawn Moves
    else:
        if (position[0], position[1] + 1) not in whitePiecesLocation and (position[0], position[1] + 1) not in blackPiecesLocation and position[1] < 7:
            moveList.append((position[0], position[1] + 1))
            if (position[0], position[1] + 2) not in whitePiecesLocation and (position[0], position[1] + 2) not in blackPiecesLocation and position[1] == 1:
                moveList.append((position[0], position[1] + 2))

        #Capture Moves
        if (position[0] + 1, position[1] + 1) in whitePiecesLocation:
            moveList.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in whitePiecesLocation:
            moveList.append((position[0] - 1, position[1] + 1))

        #En Passant Capture Checking
        if (position[0] + 1, position[1] + 1) == whiteEnPassant:
            moveList.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) == whiteEnPassant:
            moveList.append((position[0] - 1, position[1] + 1))

    return moveList

#Check if En Passant is Available
def checkEnPassant(oldCoordinates, newCoordinates):
    #For White
    if turn <= 1:
        index = whitePiecesLocation.index(oldCoordinates)
        enPassant = (newCoordinates[0], newCoordinates[1] + 1)
        piece = whitePieces[index]
    #For Black
    else:
        index = blackPiecesLocation.index(oldCoordinates)
        enPassant = (newCoordinates[0], newCoordinates[1] - 1)
        piece = blackPieces[index]
    if piece == 'Pawn' and abs(oldCoordinates[1] - newCoordinates[1]) > 1:
        pass
    else:
        enPassant = (111, 111)
    return enPassant

#Check if Pawn is able to be Promoted 
def checkPawnPromotion():
    pawnIndex = []
    whitePromotion = False
    blackPromotion = False
    promotionIndex = -1

    #White Promotion
    for i in range(len(whitePieces)):
        if whitePieces[i] == 'Pawn':
            pawnIndex.append(i)

    for i in range(len(pawnIndex)):
        if whitePiecesLocation[pawnIndex[i]][1] == 0:
            whitePromotion = True
            promotionIndex = pawnIndex[i]
    pawnIndex = []

    #Black Promotion
    for i in range(len(blackPieces)):
        if blackPieces[i] == 'Pawn':
            pawnIndex.append(i)

    for i in range(len(pawnIndex)):
        if blackPiecesLocation[pawnIndex[i]][1] == 7:
            blackPromotion = True
            promotionIndex = pawnIndex[i]

    return whitePromotion, blackPromotion, promotionIndex

#Allow Selection of Promotion Piece
def checkPawnPromotionSelection():
    mousePosition = pygame.mouse.get_pos()
    leftClick = pygame.mouse.get_pressed()[0]
    xPosition = mousePosition[0] // 110
    yPosition = mousePosition[1] // 110
    #For White
    if whitePromote and leftClick and xPosition > 7 and yPosition < 4:
        whitePieces[promoteIndex] = whitePromotions[yPosition]
        promoteSFX.play()
    #For Black
    elif blackPromote and leftClick and xPosition > 7 and yPosition < 4:
        blackPieces[promoteIndex] = blackPromotions[yPosition]
        promoteSFX.play()

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

        #Appends Movement To a Pathway
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

        #Appends Movement To a Pathway
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
    #Takes the 2 Existing movelists of the Rook and Bishop since Queen is a combo of the 2
    moveList = checkBishopMoves(position, color)
    moveList2 = checkRookMoves(position, color)
    
    for i in range(len(moveList2)):
        moveList.append(moveList2[i])
    
    return moveList

#Check Possible King Moves
def checkKingMoves(position, color):
    moveList = []
    castlingMoves = checkCastling()
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

    return moveList, castlingMoves

#Check for Possible Castling From Selected King
def checkCastling():
    #King Not in Check, Rook or King Never Moved, Tiles Between the Two are Empty, and King Does Not Pass Through or Land on Tile Being Attacked
    castlingMoves = [] #Stored as [((kingCoordinates), (rookCoordinates))]
    rookIndices = []
    rookPosition = []
    kingIndex = 0
    kingPosition = (0, 0)
    #Castling For White
    if turn > 1:
        for i in range(len(whitePieces)):
            if whitePieces[i] == 'Rook':
                rookIndices.append(whiteMoved[i])
                rookPosition.append(whitePiecesLocation[i])
            if whitePieces[i] == 'King':
                kingIndex = i
                kingPosition = whitePiecesLocation[i]

        if not whiteMoved[kingIndex] and False in rookIndices and not inCheck:
            for i in range(len(rookIndices)):
                castle = True
                if rookPosition[i][0] > kingPosition[0]:
                    emptyTiles = [(kingPosition[0] + 1, kingPosition[1]), (kingPosition[0] + 2, kingPosition[1])]
                else:
                    emptyTiles = [(kingPosition[0] - 1, kingPosition[1]), (kingPosition[0] - 2, kingPosition[1]), (kingPosition[0] - 3, kingPosition[1])]
                for j in range(len(emptyTiles)):
                    if emptyTiles[j] in whitePiecesLocation or emptyTiles[j] in blackPiecesLocation or emptyTiles[j] in blackMoveOptions or rookIndices[i]:
                        castle = False
                if castle:
                    castlingMoves.append((emptyTiles[1], emptyTiles[0]))

    #Castling For Black
    else:
        for i in range(len(blackPieces)):
            if blackPieces[i] == 'Rook':
                rookIndices.append(blackMoved[i])
                rookPosition.append(blackPiecesLocation[i])
            if blackPieces[i] == 'King':
                kingIndex = i
                kingPosition = blackPiecesLocation[i]

        if not blackMoved[kingIndex] and False in rookIndices and not inCheck:
            for i in range(len(rookIndices)):
                castle = True
                if rookPosition[i][0] > kingPosition[0]:
                    emptyTiles = [(kingPosition[0] + 1, kingPosition[1]), (kingPosition[0] + 2, kingPosition[1])]
                else:
                    emptyTiles = [(kingPosition[0] - 1, kingPosition[1]), (kingPosition[0] - 2, kingPosition[1]), (kingPosition[0] - 3, kingPosition[1])]
                for j in range(len(emptyTiles)):
                    if emptyTiles[j] in blackPiecesLocation or emptyTiles[j] in whitePiecesLocation or emptyTiles[j] in whiteMoveOptions or rookIndices[i]:
                        castle = False
                if castle:
                    castlingMoves.append((emptyTiles[1], emptyTiles[0]))

    return castlingMoves

#Draws the Main Menu
def drawMainMenu():
    command = 0
    screen.blit(mediumFont.render('Hunter Flati Chess Project', True, 'white'), (243, 100))
    screen.blit(mediumFont.render('CSCI 4890', True, 'white'), (380, 200))

    playCPUButton = Button('      Play CPU', (300, 350))
    playCPUButton.draw()
    if playCPUButton.checkClicked():
        command = 1

    playMultiplayerButton = Button(' Play Multiplayer', (300, 475))
    playMultiplayerButton.draw()
    if playMultiplayerButton.checkClicked():
        command = 2

    tutorialButton = Button('       Tutorial', (300, 600))
    tutorialButton.draw()
    if tutorialButton.checkClicked():
        command = 3

    return command
 
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
            pygame.draw.line(screen, 'black', (50 + (100 * i), 0), (50 + (100 * i), 850), 3)

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
        screen.blit(mediumFont.render('8', True, 'white'), (15, 25))
        screen.blit(mediumFont.render('7', True, 'white'), (15, 125))
        screen.blit(mediumFont.render('6', True, 'white'), (15, 225))
        screen.blit(mediumFont.render('5', True, 'white'), (15, 325))
        screen.blit(mediumFont.render('4', True, 'white'), (15, 425))
        screen.blit(mediumFont.render('3', True, 'white'), (15, 525))
        screen.blit(mediumFont.render('2', True, 'white'), (15, 625))
        screen.blit(mediumFont.render('1', True, 'white'), (15, 725))
        #Column Letters
        screen.blit(mediumFont.render('a', True, 'white'), (90, 793))
        screen.blit(mediumFont.render('b', True, 'white'), (190, 793))
        screen.blit(mediumFont.render('c', True, 'white'), (290, 793))
        screen.blit(mediumFont.render('d', True, 'white'), (390, 793))
        screen.blit(mediumFont.render('e', True, 'white'), (490, 793))
        screen.blit(mediumFont.render('f', True, 'white'), (590, 793))
        screen.blit(mediumFont.render('g', True, 'white'), (690, 793))
        screen.blit(mediumFont.render('h', True, 'white'), (790, 793))

        #Forfeit Button
        screen.blit(smallFont.render('FORFEIT', True, 'white'), (858, 858))

        #Promotion Text
        if whitePromote or blackPromote:
            pygame.draw.rect(screen, color, [0, 850, 850, 100])
            pygame.draw.rect(screen, 'black', [0, 850, 850, 100], 4)
            screen.blit(largeFont.render('Select Piece to Promote Pawn', True, 'white'), (15, 865))

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

#Draws Pawn Promotion Menu
def drawPawnPromotion():
    pygame.draw.rect(screen, 'gray63', [847, 0, 153, 420])
    if whitePromote:
        borderColor = 'white'
        for i in range(len(whitePromotions)):
            piece = whitePromotions[i]
            index = pieces.index(piece)
            screen.blit(whitePictures[index], (882, 20 + 100 * i))
    elif blackPromote:
        borderColor = 'black'
        for i in range(len(blackPromotions)):
            piece = blackPromotions[i]
            index = pieces.index(piece)
            screen.blit(blackPictures[index], (882, 20 + 100 * i))
    pygame.draw.rect(screen, borderColor, [847, 0, 153, 420], 6)

#Draws Castling on Board From Selected King
def drawCastling(moves):
    if turn < 2:
        color = 'dodgerblue'
    else:
        color = 'firebrick1'

    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0][0] * 100 + 100, moves[i][0][1] * 100 + 50), 10, 5)
        screen.blit(smallestFont.render('King', True, 'black'), (moves[i][0][0] * 100 + 75, moves[i][0][1] * 100 + 50))
        pygame.draw.circle(screen, color, (moves[i][1][0] * 100 + 100, moves[i][1][1] * 100 + 50), 10, 5)
        screen.blit(smallestFont.render('Rook', True, 'black'), (moves[i][1][0] * 100 + 75, moves[i][1][1] * 100 + 50))
        pygame.draw.line(screen, color, (moves[i][0][0] * 100 + 100, moves[i][0][1] * 100 + 50), (moves[i][1][0] * 100 + 100, moves[i][1][1] * 100 + 50), 2)

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
                    inCheck = True
                    if counter < 15:
                        pygame.draw.rect(screen, 'gold', [whitePiecesLocation[kingIndex][0] * 100 + 52, whitePiecesLocation[kingIndex][1] * 100 + 1, 100, 100], 5)
                        checkSFX.play()

    else:
        if 'King' in blackPieces:
            kingIndex = blackPieces.index('King')
            kingLocation = blackPiecesLocation[kingIndex]

            for i in range(len(whiteMoveOptions)):
                if kingLocation in whiteMoveOptions[i]:
                    inCheck = True
                    if counter < 15:
                        pygame.draw.rect(screen, 'gold', [blackPiecesLocation[kingIndex][0] * 100 + 52, blackPiecesLocation[kingIndex][1] * 100 + 1, 100, 100], 5)
                        checkSFX.play()

#Defines when the King is in check
def kingInCheck():
    king_index = -1
    king_location = ''
    enemy_moves = []
    inCheck = False

    if turn < 2:
        #White's turn
        king_index = whitePieces.index('King')
        king_location = whitePiecesLocation[king_index]
        enemy_moves = blackMoveOptions
    else:
        #Black's turn
        king_index = blackPieces.index('King')
        king_location = blackPiecesLocation[king_index]
        enemy_moves = whiteMoveOptions

    for moves in enemy_moves: #Pawn Forward Move Technically In List
        if king_location in moves:
            inCheck = True
            break  #Exit the loop as soon as it finds one move that puts the king in check

    return inCheck

#Game Over
def drawGameOver():
    if winner == 'White':
        pygame.draw.rect(screen, 'white', [150, 250, 600, 300])
        pygame.draw.rect(screen, 'black', [150, 250, 600, 300], 4)
        screen.blit(mediumFont.render(f'{winner} Won The Match', True, 'black'), (220, 270))
        screen.blit(mediumFont.render(f'Press ENTER to Play Again', True, 'black'), (165, 350))
        screen.blit(mediumFont.render(f'OR', True, 'black'), (415, 410))
        screen.blit(mediumFont.render(f'Press ESC to Quit', True, 'black'), (260, 470))
    else:
        pygame.draw.rect(screen, 'black', [150, 250, 600, 300])
        pygame.draw.rect(screen, 'white', [150, 250, 600, 300], 4)
        screen.blit(mediumFont.render(f'{winner} Won The Match', True, 'white'), (220, 270))
        screen.blit(mediumFont.render(f'Press ENTER to Play Again', True, 'white'), (165, 350))
        screen.blit(mediumFont.render(f'OR', True, 'white'), (415, 410))
        screen.blit(mediumFont.render(f'Press ESC to Quit', True, 'white'), (260, 470))
                    
#Game Loop
blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')

#AI Move Function
def makeSmartMove():
    global turn, blackPiecesLocation, blackMoveOptions

    #Black's turn (AI's turn)
    if turn == 2: 
        #Evaluate available moves based on simple strategy
        best_move_score = float('-inf')
        best_moves = []

        #Iterate over black pieces
        for piece_index, possible_moves in enumerate(blackMoveOptions):
            piece = blackPiecesLocation[piece_index]
            for move in possible_moves:
                #Simulate the move and evaluate the resulting board state
                score = evaluateMove(piece, move)
                if score > best_move_score:
                    best_move_score = score
                    best_moves = [(piece, move)]  #Start new list with better move
                elif score == best_move_score:
                    best_moves.append((piece, move))  #Add to existing list of equally good moves

        #Make a random choice among the best moves found
        if best_moves:
            piece_index, new_location = random.choice(best_moves)
            #Find the index of the piece's current location
            current_location_index = blackPiecesLocation.index(piece_index)
            #Update the piece's location with the new location
            blackPiecesLocation[current_location_index] = new_location
            turn = 0

        if new_location in possibleMoves and selection != -1:
            blackEnPassant = checkEnPassant(blackPiecesLocation[selection], new_location)
            blackPiecesLocation[selection] = new_location
            blackMoved[selection] = True

        #White Piece Captured
        if new_location in whitePiecesLocation:
            landedOnWhitePiece = whitePiecesLocation.index(new_location)
            blackCaptured.append(whitePieces[landedOnWhitePiece])
            #If Statement for White King in Check
            if whitePieces[landedOnWhitePiece] == 'King':
                winner = 'Black'

            whitePieces.pop((landedOnWhitePiece))
            whitePiecesLocation.pop(landedOnWhitePiece)
            whiteMoved.pop(landedOnWhitePiece)

        #White En Passant Piece Captured
        if new_location == whiteEnPassant:
            landedOnWhitePiece = whitePiecesLocation.index((whiteEnPassant[0], whiteEnPassant[1] - 1))
            blackCaptured.append(whitePieces[landedOnWhitePiece])
            whitePieces.pop((landedOnWhitePiece))
            whitePiecesLocation.pop(landedOnWhitePiece)
            whiteMoved.pop(landedOnWhitePiece)

#Assigns Point Values to Pieces To Allow AI to Choose what to Attack
def evaluateMove(piece, move):
    piece_value = 0 #Initialize piece value
    move_score = 0 #Initialize move score

    #Assign values to pieces
    if piece == 'Pawn':
        piece_value = 1
    elif piece == 'Knight':
        piece_value = 3
    elif piece == 'Bishop':
        piece_value = 3
    elif piece == 'Rook':
        piece_value = 5
    elif piece == 'Queen':
        piece_value = 9
    elif piece == 'King':
        piece_value = 100 #High value to prioritize king safety

    #Evaluate move based on destination square
    destination = move
    if destination in whitePiecesLocation:
        captured_piece = whitePieces[whitePiecesLocation.index(destination)]
        captured_value = 0
        if captured_piece == 'Pawn':
            captured_value = 1
        elif captured_piece == 'Knight':
            captured_value = 3
        elif captured_piece == 'Bishop':
            captured_value = 3
        elif captured_piece == 'Rook':
            captured_value = 5
        elif captured_piece == 'Queen':
            captured_value = 9
        elif captured_piece == 'King':
            #Capturing the king is the ultimate goal
            captured_value = 1000

        move_score += captured_value - piece_value  #Account for piece value difference

    #Return the total move score
    return move_score

#Main Menu
while runMainMenu:
    screen.fill(color)
    timer.tick(fps)

    if mainMenu:
        command = drawMainMenu()
        if command == 1:
            runCPUGame = True
            runMainMenu = False
        if command == 2:
            runGame = True
            runMainMenu = False
        if command == 3:
            runTutorial = True
            runMainMenu = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runMainMenu = False

    pygame.display.flip()

#Tutorial Screen
tutorialPage = 1
while runTutorial:
    if command == 3:
        mainMenu = False
        screen.fill(color)
        timer.tick(fps)
        #Pieces Tutorial Page
        if tutorialPage == 1:
            pygame.draw.rect(screen, 'black', [50, 100, 110, 110], 4)
            pygame.draw.rect(screen, 'black', [50, 230, 110, 110], 4)
            pygame.draw.rect(screen, 'black', [50, 360, 110, 110], 4)
            pygame.draw.rect(screen, 'black', [50, 490, 110, 110], 4)
            pygame.draw.rect(screen, 'black', [50, 620, 110, 110], 4)
            pygame.draw.rect(screen, 'black', [50, 750, 110, 110], 4)
            screen.blit(largeFont.render('The Pieces:', True, 'white'), (15, 15))
            screen.blit(whitePawn, (75, 123))
            screen.blit(smallFont.render('The Pawn:', True, 'white'), (170, 100))
            screen.blit(smallestFont.render('The Pawn may only move forward one square at a time, except for their very first', True, 'white'), (170, 135))
            screen.blit(smallestFont.render('move where they can move forward two squares. Pawns can only capture one', True, 'white'), (170, 160))
            screen.blit(smallestFont.render('square diagonally in front of them. They can never move or capture backward.', True, 'white'), (170, 185))
            screen.blit(whiteRook, (63, 245))
            screen.blit(smallFont.render('The Rook:', True, 'white'), (170, 230))
            screen.blit(smallestFont.render('The Rook may move as far as it wants, but only forward, backward, and to the sides.', True, 'white'), (170, 265))
            screen.blit(whiteKnight, (63, 375))
            screen.blit(smallFont.render('The Knight:', True, 'white'), (170, 360))
            screen.blit(smallestFont.render('The Knight may move two squares in one direction, and then one square at a', True, 'white'), (170, 395))
            screen.blit(smallestFont.render('90-degree angle, just like the shape of an “L”.', True, 'white'), (170, 420))
            screen.blit(whiteBishop, (63, 505))
            screen.blit(smallFont.render('The Bishop:', True, 'white'), (170, 490))
            screen.blit(smallestFont.render('The Bishop may move as far as it wants, but only diagonally', True, 'white'), (170, 525))
            screen.blit(whiteQueen, (63, 635))
            screen.blit(smallFont.render('The Queen:', True, 'white'), (170, 620))
            screen.blit(smallestFont.render('The Queen may move in any one straight direction - forward, backward, sideways,', True, 'white'), (170, 655))
            screen.blit(smallestFont.render('or diagonally - as far as she wishes', True, 'white'), (170, 680))
            screen.blit(whiteKing, (63, 765))
            screen.blit(smallFont.render('The King:', True, 'white'), (170, 750))
            screen.blit(smallestFont.render('The King may only move one square in any direction - up, down, to the sides, or', True, 'white'), (170, 785))
            screen.blit(smallestFont.render('diagonally. When the king is attacked by another piece this is called "check".', True, 'white'), (170, 810))
            screen.blit(smallestFont.render('The king may never move himself into check (where he could be captured).', True, 'white'), (170, 835))

            rightArrowRect = pygame.draw.rect(surface, color, [875, 875, 75, 75])
            screen.blit(surface, rightArrowRect)
            screen.blit(rightArrow, (875, 875))
            if rightArrowRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                tutorialPage = 2
                pageFlipSFX.play()

            leftArrowRectMainMenu = pygame.draw.rect(surface, color, [875, 25, 75, 75])
            screen.blit(surface, leftArrowRectMainMenu)
            screen.blit(leftArrow, (875, 25))
            if leftArrowRectMainMenu.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                runTutorial = False
                drawMainMenu()
                mainMenu = True

        #Special Moves Tutorial Page
        if tutorialPage == 2:
            screen.fill(color)
            timer.tick(fps)
            #Pawn Promotion
            screen.blit(largeFont.render('The Special Rules:', True, 'white'), (15, 15))
            pawnPromotionClick = pygame.draw.rect(surface, color, [100, 100, 350, 350])
            screen.blit(surface, pawnPromotionClick)
            screen.blit(pawnPromotionPictureSmall, (100, 100))
            pygame.draw.rect(screen, 'black', [100, 100, 350, 350], 4)
            screen.blit(smallFont.render('Pawn Promotion', True, 'white'), (160, 450))
            if pawnPromotionClick.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                tutorialPage = 3
                pageFlipSFX.play()

            #En Passant
            enPassantClick = pygame.draw.rect(surface, color, [550, 100, 350, 350])
            screen.blit(surface, enPassantClick)
            screen.blit(enPassantPictureSmall, (550, 100))
            pygame.draw.rect(screen, 'black', [550, 100, 350, 350], 4)
            screen.blit(smallFont.render('En Passant', True, 'white'), (650, 450))
            if enPassantClick.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                tutorialPage = 4
                pageFlipSFX.play()

            #Castling
            castlingClick = pygame.draw.rect(surface, color, [325, 500, 350, 350])
            screen.blit(surface, castlingClick)    
            screen.blit(castlingPictureSmall, (325, 500))
            pygame.draw.rect(screen, 'black', [325, 500, 350, 350], 4)
            screen.blit(smallFont.render('Castling', True, 'white'), (450, 850))
            if castlingClick.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                tutorialPage = 5
                pageFlipSFX.play()

            leftArrowRect = pygame.draw.rect(surface, color, [75, 875, 75, 75])
            screen.blit(surface, leftArrowRect)
            screen.blit(leftArrow, (75, 875))
            if leftArrowRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                tutorialPage = 1
                pageFlipSFX.play()

        #Pawn Promotion Page
        if tutorialPage == 3:
            screen.fill(color)
            timer.tick(fps)
            screen.blit(largeFont.render('Pawn Promotion', True, 'white'), (275, 15))
            screen.blit(pawnPromotionPictureBig, (200, 100))
            pygame.draw.rect(screen, 'black', [200, 100, 600, 600], 4)
            screen.blit(smallestFont.render('A Pawn may be promoted to a Rook, Knight, Bishop or Queen', True, 'white'), (200, 700))
            screen.blit(smallestFont.render('if it reaches the other side of the board', True, 'white'), (200, 725))

            leftArrowRectP3 = pygame.draw.rect(surface, color, [75, 875, 75, 75])
            screen.blit(surface, leftArrowRectP3)
            screen.blit(leftArrow, (75, 875))
            if leftArrowRectP3.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                tutorialPage = 1
                pageFlipSFX.play()

        #En Passant Page
        if tutorialPage == 4:
            screen.fill(color)
            timer.tick(fps)
            screen.blit(largeFont.render('En Passant', True, 'white'), (350, 15))
            screen.blit(enPassantPictureBig, (200, 100))
            pygame.draw.rect(screen, 'black', [200, 100, 600, 600], 4)
            screen.blit(smallestFont.render("If a Pawn moves out two squares on its first move, and by", True, 'white'), (200, 700))
            screen.blit(smallestFont.render("doing so lands to the side of an opponent's Pawn that other", True, 'white'), (200, 725))
            screen.blit(smallestFont.render("Pawn has the option of capturing the first Pawn as it passes by.", True, 'white'), (200, 750))
            screen.blit(smallestFont.render("This special move must be done immediately after the first", True, 'white'), (200, 775))
            screen.blit(smallestFont.render("Pawn has moved past, otherwise the option to capture it is no", True, 'white'), (200, 800))
            screen.blit(smallestFont.render("longer available", True, 'white'), (200, 825))

            leftArrowRectP4 = pygame.draw.rect(surface, color, [75, 875, 75, 75])
            screen.blit(surface, leftArrowRectP4)
            screen.blit(leftArrow, (75, 875))
            if leftArrowRectP4.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                tutorialPage = 1
                pageFlipSFX.play()

        #Castling Page
        if tutorialPage == 5:
            screen.fill(color)
            timer.tick(fps)
            screen.blit(largeFont.render('Castling', True, 'white'), (375, 15))
            screen.blit(castlingPictureBig, (200, 100))
            pygame.draw.rect(screen, 'black', [200, 100, 600, 600], 4)
            screen.blit(smallestFont.render("On a player's turn he may move his King two squares over to", True, 'white'), (200, 700))
            screen.blit(smallestFont.render("one side and then move the Rook from that side's corner to", True, 'white'), (200, 725))
            screen.blit(smallestFont.render("right next to the King on the opposite side.", True, 'white'), (200, 750))
            screen.blit(smallestFont.render("However, in order to castle, the following conditions must", True, 'white'), (200, 775))
            screen.blit(smallestFont.render("be met:", True, 'white'), (200, 800))
            screen.blit(smallestFont.render("• It must be that King's very first move", True, 'white'), (200, 825))
            screen.blit(smallestFont.render("• It must be that Rook's very first move", True, 'white'), (200, 850))
            screen.blit(smallestFont.render("• There cannot be any pieces between the King and Rook to move", True, 'white'), (200, 875))
            screen.blit(smallestFont.render("• The King may not be in check or pass through check", True, 'white'), (200, 900))

            leftArrowRectP5 = pygame.draw.rect(surface, color, [75, 875, 75, 75])
            screen.blit(surface, leftArrowRectP5)
            screen.blit(leftArrow, (75, 875))
            if leftArrowRectP5.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                tutorialPage = 1
                pageFlipSFX.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runTutorial = False

    pygame.display.flip()

#Multiplayer Game Loop
while runGame:
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
    if not gameOver:
        whitePromote, blackPromote, promoteIndex = checkPawnPromotion()
        if whitePromote or blackPromote:
            drawPawnPromotion()
            checkPawnPromotionSelection()

    if selection != -1:
        possibleMoves = checkPossibleMoves()
        if turn < 2:   
            if checkmate:
                winner = 'Black'
        else:
            if checkmate:
                winner = 'White'

        drawMoves(possibleMoves)
        if selectedPiece == 'King':
            drawCastling(castleMoves)

#Clicking Exit Button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runGame = False

#Allowing the Game to Understand a Left Mouse Button Click for White's Turn
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not gameOver:
            xCoordinate = event.pos[0] // 110
            yCoordinate = event.pos[1] // 100
            click = (xCoordinate, yCoordinate)
            if turn <= 1:
                #Forfeit Click
                if click == (7, 8) or click == (8, 8) or click == (7, 9) or click == (8, 9):
                    winner = 'Black'
                if click in whitePiecesLocation:
                    selection = whitePiecesLocation.index(click)
                    #Check What Piece is Selected, Draws Castling Move if King is Selected
                    selectedPiece = whitePieces[selection]
                    if turn == 0:
                        turn = 1
                
                if click in possibleMoves and selection != -1:
                    whiteEnPassant = checkEnPassant(whitePiecesLocation[selection], click)
                    #Check if the Move Puts the King in Check
                    temp_location = whitePiecesLocation[selection]
                    whitePiecesLocation[selection] = click

                    #Moves While King is Not in Check
                    if not kingInCheck():
                        #The Move is Valid
                        whiteMoved[selection] = True
                        pieceMovingSFX.play()
                        blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                        whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')
                        turn = 2
                        selection = -1
                        possibleMoves = []

                    #Moves While King is in Check
                    elif kingInCheck():
                        #Checks for a Move that Intersects or Captures the Attacker of the King
                        if click in intersectingMoves:
                            whiteMoved[selection] = True
                            inCheck = False
                            pieceMovingSFX.play()
                            blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                            whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')
                            turn = 2
                            selection = -1
                            possibleMoves = []
                        #Undo Invalid Move, Leaves the King in Check
                        else:
                            whitePiecesLocation[selection] = temp_location  #Reset the moved status
                            whiteMoved[selection] = False  #Reset the moved status
                            blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                            whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')
                            turn = 0
                            selection = -1
                            possibleMoves = [] 
 
                    #Black Piece Captured
                    if click in blackPiecesLocation:
                        landedOnBlackPiece = blackPiecesLocation.index(click)
                        whiteCaptured.append(blackPieces[landedOnBlackPiece])
                        blackPieces.pop((landedOnBlackPiece))
                        blackPiecesLocation.pop(landedOnBlackPiece)
                        blackMoved.pop(landedOnBlackPiece)
                        pieceCapturedSFX.play()
                        
                        blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                        whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')
                        turn = 2
                        selection = -1
                        possibleMoves = []

                    #Black En Passant Piece Captured
                    if click == blackEnPassant:
                        landedOnBlackPiece = blackPiecesLocation.index((blackEnPassant[0], blackEnPassant[1] + 1))
                        whiteCaptured.append(blackPieces[landedOnBlackPiece])
                        blackPieces.pop((landedOnBlackPiece))
                        blackPiecesLocation.pop(landedOnBlackPiece)
                        blackMoved.pop(landedOnBlackPiece)
                        pieceCapturedSFX.play()

                        blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                        whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')
                        turn = 2
                        selection = -1
                        possibleMoves = []

                #Option For White to Castle
                elif selection != -1 and selectedPiece == 'King':
                    for k in range(len(castleMoves)):
                        if click == castleMoves[k][0]:
                            whitePiecesLocation[selection] = click
                            whiteMoved[selection] = True
                            pieceMovingSFX.play()
                            if click == (2, 7):
                                rookCoordinates = (0, 7)
                            elif click == (6, 7):
                                rookCoordinates = (7, 7)
                            rookIndex = whitePiecesLocation.index(rookCoordinates)
                            whitePiecesLocation[rookIndex] = castleMoves[k][1]

                            blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                            whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')
                            turn = 2
                            selection = -1
                            possibleMoves = []

#Allowing the Game to Understand a Left Mouse Button Click for Black's Turn
            if turn > 1:
                #Forfeit Click
                if click == (7, 8) or click == (8, 8) or click == (7, 9) or click == (8, 9):
                    winner = 'White'
                if click in blackPiecesLocation:
                    selection = blackPiecesLocation.index(click)
                    #Check What Piece is Selected, Draws Castling Move if King is Selected
                    selectedPiece = blackPieces[selection]
                    if turn == 2:
                        turn = 3

                if click in possibleMoves and selection != -1:
                    blackEnPassant = checkEnPassant(blackPiecesLocation[selection], click)
                    #Check if the Move Puts the King in Check
                    temp_location = blackPiecesLocation[selection]
                    blackPiecesLocation[selection] = click

                    #Moves While King is Not in Check
                    if not kingInCheck():
                        #The Move is Valid
                        blackMoved[selection] = True
                        pieceMovingSFX.play()
                        blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                        whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')
                        turn = 0
                        selection = -1
                        possibleMoves = []
                    
                    #Moves While King is in Check
                    elif kingInCheck():
                        #Checks for a Move that Intersects or Captures the Attacker of the King
                        if click in intersectingMoves:
                            blackMoved[selection] = True
                            inCheck = False
                            pieceMovingSFX.play()
                            blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                            whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')
                            turn = 0
                            selection = -1
                            possibleMoves = []
                        #Undo Invalid Move, Leaves the King in Check
                        else:
                            blackPiecesLocation[selection] = temp_location  #Reset the moved status
                            blackMoved[selection] = False  #Reset the moved status
                            blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                            whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')
                            turn = 2
                            selection = -1
                            possibleMoves = [] 

                    #White Piece Captured
                    if click in whitePiecesLocation:
                        landedOnWhitePiece = whitePiecesLocation.index(click)
                        blackCaptured.append(whitePieces[landedOnWhitePiece])
                        whitePieces.pop((landedOnWhitePiece))
                        whitePiecesLocation.pop(landedOnWhitePiece)
                        whiteMoved.pop(landedOnWhitePiece)
                        pieceCapturedSFX.play()

                        blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                        whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')
                        turn = 0
                        selection = -1
                        possibleMoves = []

                    #White En Passant Piece Captured
                    if click == whiteEnPassant:
                        landedOnWhitePiece = whitePiecesLocation.index((whiteEnPassant[0], whiteEnPassant[1] - 1))
                        blackCaptured.append(whitePieces[landedOnWhitePiece])
                        whitePieces.pop((landedOnWhitePiece))
                        whitePiecesLocation.pop(landedOnWhitePiece)
                        whiteMoved.pop(landedOnWhitePiece)
                        pieceCapturedSFX.play()

                        blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                        whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')
                        turn = 0
                        selection = -1
                        possibleMoves = []

                #Option For Black to Castle
                elif selection != -1 and selectedPiece == 'King':
                    for k in range(len(castleMoves)):
                        if click == castleMoves[k][0]:
                            blackPiecesLocation[selection] = click
                            blackMoved[selection] = True
                            pieceMovingSFX.play()
                            if click == (2, 0):
                                rookCoordinates = (0, 0)
                            elif click == (6, 0):
                                rookCoordinates = (7, 0)
                            rookIndex = blackPiecesLocation.index(rookCoordinates)
                            blackPiecesLocation[rookIndex] = castleMoves[k][1]

                            blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                            whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')
                            turn = 0
                            selection = -1
                            possibleMoves = []

#Reinitialize the Game
        if event.type == pygame.KEYDOWN and gameOver:
            if event.key == pygame.K_RETURN:
                gameOver = False
                winner = ''
                whitePieces = ['Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook',
                               'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn']
                whitePiecesLocation = [(0,7), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7),
                                       (0,6), (1,6), (2,6), (3,6), (4,6), (5,6), (6,6), (7,6)]
                whiteCaptured = []
                whiteMoved = [False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False]


                blackPieces = ['Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook',
                               'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn']
                blackPiecesLocation = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0),
                                       (0,1), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1)]
                blackCaptured = []
                blackMoved = [False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False]

                turn = 0
                selection = -1
                possibleMoves = []

                blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')

        #Close Game After Match Completed
        if event.type == pygame.KEYDOWN and gameOver:
            if event.key == pygame.K_ESCAPE:
                runGame = False
                mainMenu = True

    if winner != '':
        gameOver = True
        drawGameOver()
        victorySFX.play()


    pygame.display.flip()

#CPU Game Loop
while runCPUGame:
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
    if not gameOver:
        whitePromote, blackPromote, promoteIndex = checkPawnPromotion()
        if whitePromote or blackPromote:
            drawPawnPromotion()
            checkPawnPromotionSelection()

    if selection != -1:
        possibleMoves = checkPossibleMoves()
        if turn < 2:   
            if checkmate:
                winner = 'Black'
        else:
            if checkmate:
                winner = 'White'

        drawMoves(possibleMoves)
        if selectedPiece == 'King':
            drawCastling(castleMoves)

#Clicking Exit Button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runGame = False

#Allowing the Game to Understand a Left Mouse Button Click for White's Turn
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not gameOver:
            xCoordinate = event.pos[0] // 110
            yCoordinate = event.pos[1] // 100
            click = (xCoordinate, yCoordinate)
            if turn <= 1:
                #Forfeit Click
                if click == (7, 8) or click == (8, 8) or click == (7, 9) or click == (8, 9):
                    winner = 'Black'
                if click in whitePiecesLocation:
                    selection = whitePiecesLocation.index(click)
                    #Check What Piece is Selected, Draws Castling Move if King is Selected
                    selectedPiece = whitePieces[selection]
                    if turn == 0:
                        turn = 1
                
                if click in possibleMoves and selection != -1:
                    whiteEnPassant = checkEnPassant(whitePiecesLocation[selection], click)
                    #Check if the Move Puts the King in Check
                    temp_location = whitePiecesLocation[selection]
                    whitePiecesLocation[selection] = click

                    #Moves While King is Not in Check
                    if not kingInCheck():
                        #The Move is Valid
                        whiteMoved[selection] = True
                        pieceMovingSFX.play()
                        blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                        whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')
                        turn = 2
                        selection = -1
                        possibleMoves = []

                    #Moves While King is in Check
                    elif kingInCheck():
                        #Checks for a Move that Intersects or Captures the Attacker of the King
                        if click in intersectingMoves:
                            whiteMoved[selection] = True
                            inCheck = False
                            pieceMovingSFX.play()
                            blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                            whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')
                            turn = 2
                            selection = -1
                            possibleMoves = []
                        #Undo Invalid Move, Leaves the King in Check
                        else:
                            whitePiecesLocation[selection] = temp_location  #Reset the moved status
                            whiteMoved[selection] = False  #Reset the moved status
                            blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                            whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')
                            turn = 0
                            selection = -1
                            possibleMoves = [] 
 
                    #Black Piece Captured
                    if click in blackPiecesLocation:
                        landedOnBlackPiece = blackPiecesLocation.index(click)
                        whiteCaptured.append(blackPieces[landedOnBlackPiece])
                        blackPieces.pop((landedOnBlackPiece))
                        blackPiecesLocation.pop(landedOnBlackPiece)
                        blackMoved.pop(landedOnBlackPiece)
                        pieceCapturedSFX.play()
                        
                        blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                        whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')
                        turn = 2
                        selection = -1
                        possibleMoves = []

                    #Black En Passant Piece Captured
                    if click == blackEnPassant:
                        landedOnBlackPiece = blackPiecesLocation.index((blackEnPassant[0], blackEnPassant[1] + 1))
                        whiteCaptured.append(blackPieces[landedOnBlackPiece])
                        blackPieces.pop((landedOnBlackPiece))
                        blackPiecesLocation.pop(landedOnBlackPiece)
                        blackMoved.pop(landedOnBlackPiece)
                        pieceCapturedSFX.play()

                        blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                        whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')
                        turn = 2
                        selection = -1
                        possibleMoves = []

                #Option For White to Castle
                elif selection != -1 and selectedPiece == 'King':
                    for k in range(len(castleMoves)):
                        if click == castleMoves[k][0]:
                            whitePiecesLocation[selection] = click
                            whiteMoved[selection] = True
                            pieceMovingSFX.play()
                            if click == (2, 7):
                                rookCoordinates = (0, 7)
                            elif click == (6, 7):
                                rookCoordinates = (7, 7)
                            rookIndex = whitePiecesLocation.index(rookCoordinates)
                            whitePiecesLocation[rookIndex] = castleMoves[k][1]

                            blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                            whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')
                            turn = 2
                            selection = -1
                            possibleMoves = []

#Allowing the Game to Understand Black AI's turn      
            if turn == 2:
                makeSmartMove()
                blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')
                selection = -1
                possibleMoves = []

#Reinitialize the Game
        if event.type == pygame.KEYDOWN and gameOver:
            if event.key == pygame.K_RETURN:
                gameOver = False
                winner = ''
                whitePieces = ['Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook',
                               'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn']
                whitePiecesLocation = [(0,7), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7),
                                       (0,6), (1,6), (2,6), (3,6), (4,6), (5,6), (6,6), (7,6)]
                whiteCaptured = []
                whiteMoved = [False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False]


                blackPieces = ['Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook',
                               'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn', 'Pawn']
                blackPiecesLocation = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0),
                                       (0,1), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1)]
                blackCaptured = []
                blackMoved = [False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False]

                turn = 0
                selection = -1
                possibleMoves = []

                blackMoveOptions = checkMoveOptions(blackPieces, blackPiecesLocation, 'Black')
                whiteMoveOptions = checkMoveOptions(whitePieces, whitePiecesLocation, 'White')

        #Close Game After Match Completed
        if event.type == pygame.KEYDOWN and gameOver:
            if event.key == pygame.K_ESCAPE:
                runCPUGame = False
                mainMenu = True

    if winner != '':
        gameOver = True
        drawGameOver()
        victorySFX.play()

    pygame.display.flip()
pygame.quit()