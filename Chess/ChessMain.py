"""
This is our main driver file. It is responsible for displaying game state object and user input
"""


import pygame as p 
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8 #Dimension of chessboard 
SQ_SIZE = HEIGHT//DIMENSION # Square Size 
MAX_FPS = 15 #Animation Wise 
IMAGES = {}

"""
Global Dictionary of images -> Will only be called once each game 
"""

def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ","bp","bR","bN","bB","bK","bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Chess/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


"""
Main driver for our game. Will handle user input and graphics
"""

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = [] #Used to compare user moves to see if in validMoves list...
    moveMade = False # Flag variable for when move is made, we dont want to call valid moves each time
    loadImages() #Load Images only once 
    running = True
    sqSelected = () # No Square selected, keep track of last click of the user (tuple: (row, col))
    playerClicks = [] # Keep track of player clicks (two tuples: [(6,4), (4,4)])

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running=False

            #Mouse Handelrs
        
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #x,y location of mouse 
                col = location[0]// SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row,col):
                    sqSelected = () #Unselect 
                    playerClicks = [] #Clear player clicks 
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected) # Append for both 1st and 2nd clicks
                
                if len(playerClicks) == 2: #After 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    moveMade = True
                    sqSelected = () # Resetting the user clicks 
                    playerClicks = []


                

            #Key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
        
        if moveMade:
            validMoves =  gs.getValidMoves()
            moveMade = False

        
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


"""
 Responsible for all graphics within current gamestate
"""

def drawGameState(screen,gs):
    drawBoard(screen) # Will draw squares on the board
    drawPieces(screen, gs.board) #Draw pieces ontop of squares 


"""
Draw the squares on the board. Top-left is always light.
"""

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]

    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row+col) % 2)]
            p.draw.rect(screen, color, p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            



"""
Draw pieces on the board based on current state of Game. 
"""

def drawPieces(screen,board):
    
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--": # not Empty square
                screen.blit(IMAGES[piece], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE,SQ_SIZE)) 





if __name__ == "__main__":
    main()