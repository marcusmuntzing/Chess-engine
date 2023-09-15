"""
This class is responsible for storing all the information about the current state of the chess game
Determine valid moves
Log all the moves
"""

class GameState():

    def __init__(self) -> None:
        #Board 8x8 2d list where each element has 2 chars. 1st char color of piece, 2nd represents type.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB","bN", "bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR", "wN", "wB", "wK", "wQ", "wB","wN", "wR"]
        ]

        self.whiteToMove = True
        self.moveLog = []

    """
    Takes a move as parametter and executes it, however it does not work with castling & enpassant and piece promotion
    """

    def makeMove(self, move):
        if self.board[move.startRow][move.startCol] != '--':
            self.board[move.startRow][move.startCol] = '--'
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move)
            self.whiteToMove = not self.whiteToMove


    """
    Undo the moves 
    """
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #Switch turns back


    """
    All moves considering checks
    """
    def getValidMoves(self):
        return self.getAllPossibleMoves() 


    """
    All moves without considering checks
    """
    def getAllPossibleMoves(self):
        moves = []
        for row in range(len(self.board)): # Number of rows
            for col in range(len(self.board[row])): # Number of cols in given row
                turn = self.board[row][col][0] #Gives which color we are on, on given row
                if (turn =="w" and self.whiteToMove) and (turn == "b" and not self.whiteToMove):
                    piece = self.board[row][col][1] # What piece is we on?
                    if piece == "p":
                        self.getPawnMoves(row,col,moves)
                    elif piece == "R":
                        self.getRookMoves(row,col,moves)



    """
    Get moves for each piece
    """

    def getPawnMoves(self,row,col, moves):
        pass
        
    def getRookMoves(self,row,col, moves):
        pass


class Move():


    ranksToRows = {"1": 7,"2":6,"3":5,"4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v:k for k,v in ranksToRows.items()}

    filesToCols = {"a":0, "b": 1, "c":2, "d":3, "e":4, "f":5,"g":6, "h":7}
    colsToFiles = {v:k for k,v in filesToCols.items()}



    def __init__(self, startSq, endSq, board) -> None:
        #StartSq and endSq are tuples of positions!
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
        
    
    def getRankFile(self, r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]



