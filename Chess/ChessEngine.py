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

        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves, "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
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
                if (turn =="w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[row][col][1] # What piece is we on?

                    self.moveFunctions[piece](row, col) #Call our move function, instead of multiple if statements 


        return moves



    """
    Get moves for each piece
    """

    def getPawnMoves(self,row,col, moves): # Black and white pawn moves 
        if self.whiteToMove: # White Pawns 
            if self.board[row-1][col] == "--":  # 1 square pawn advance 
                moves.append(Move((row,col), (row-1,col), self.board))
                if row == 6 and self.board[row-2][col] == "--": # 2 square pawn advance
                    moves.append(Move((row,col), (row-2,col), self.board))

            if col-1 >= 0: # Dont want to move us out of the board - Captures to left
                if self.board[row-1][col-1][0] == "b": #Enemy piece to capture 
                    moves.append(Move((row,col), (row-1,col-1), self.board))

            if col+1 < 7: #Captures to the right
                if self.board[row-1][col+1][0] == "b":
                    moves.append(Move((row,col), (row-1,col+1), self.board))

        else:
            if self.board[row+1][col] == "--":
                moves.append(Move((row,col), (row+1, col), self.board))

                if (row == 1) and (self.board[row+2][col] == "--"):
                    moves.append(Move((row,col), (row+2, col), self.board))
            if col - 1 >= 0: # Black Capture left 
                if self.board[row+1][col-1][0] == "w":
                    moves.append(Move((row,col), (row+1, col-1), self.board))

            if col +  1 <= 7: # Black capture right 
                if self.board[row+1][col+1][0] =="w":
                    moves.append(Move((row,col), (row+1, col+1), self.board))
                



    def getRookMoves(self,row,col, moves):
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        enmy_color = "b" if self.whiteToMove else "w"

        for d in directions:
            for i in range(1,8):
                endrow = row + d[0] * i
                endcol = col + d[1] * i
                if 0 <= endrow < 8 and 0 <= endcol < 8:
                    endpiece = self.board[endrow][endcol]
                    if endpiece == "--": # Empty space 
                        moves.append(Move((row,col), (endrow, endcol), self.board))
                    elif endpiece[0] == enmy_color:
                        moves.append(Move(row,col), (endrow, endcol), self.board)
                    else:
                        break
                else:
                    break






    def getKnightMoves(self,row,col, moves):
        directions = [(2,1), (2, -1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2),(-1,-2)]
        ally_piece = "w" if self.whiteToMove  else "b"

        for d in directions: 
            for i in range(1, 8):
                endrow = row + d[0] 
                endcol = col + d[1] 
                if 0 <= endrow < 8 and 0<= endcol < 8: # The move is on the board
                    endpiece = self.board[endrow][endcol]
                    if endpiece != ally_piece:
                        moves.append(Move((row,col), (endrow, endcol), self.board))
                   



    def getBishopMoves(self,row,col, moves):
        directions = [(-1,1), (-1,-1), (1,-1),(1,1)]
        enmy_color = "b" if self.whiteToMove else "w"

        for d in directions:
            for i in range(1,8):
                endrow = row + d[0] * i
                endcol = col + d[1] * i 
                if 0 <= endrow < 8 and 0<= endcol < 8: # The move is on the board
                    endpiece = self.board[endrow][endcol]
                    if endpiece == "--":
                        moves.append(Move((row,col), (endrow,endcol), self.board))
                    elif endpiece[0] == enmy_color:
                        moves.append(Move((row,col), (endrow,endcol), self.board))
                        break
                    else:
                        break
                else:
                    break




    def getQueenMoves(self,row,col, moves):
        self.getRookMoves(row,col, moves)
        self.getBishopMoves(row,col,moves)



    def getKingMoves(self,row,col, moves):
        directions = [(1,0), (1,-1), (1,1), (-1,1), (-1,-1), (0,-1), (0,1), (-1,0)]
        allycolor = "w" if self.whiteToMove else "b"

        
        for i in range(8):
            endrow = row + directions[i][0]
            endcol = row + directions[i][1]
            if 0<= endrow < 8 and 0 <= endcol < 8:
                endpiece = self.board[endrow][endcol]
                if endpiece != allycolor:
                    moves.append(Move((row,col), (endrow, endcol), self.board))
            


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
        self.moveID = self.startRow * 1000 + self.startCol *100 + self.endRow*10 + self.endCol




    
    """
    Overriding the equals method 
    """
    def __eq__(self, other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False



    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
        
    
    def getRankFile(self, r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]



