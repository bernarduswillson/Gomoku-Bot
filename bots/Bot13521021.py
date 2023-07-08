import random
from game import Board
import globals as globals

class Bot13521021(object):
    """
    Bot player
    """

    def __init__(self):
        self.player = None

        """
            TODO: Ganti dengan NIM kalian
        """
        self.NIM = "13521021"
        self.blockedFour = []
        self.blockedThree = []
        self.blockedGap = []

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board, return_var):

        try:
            location = self.get_input(board)
            if isinstance(location, str):  # for python3
                location = [int(n, 10) for n in location.split(",")]
            move = board.location_to_move(location)
        except Exception as e:
            move = -1

        while move == -1 or move not in board.availables:
            if globals.stop_threads:
                return
            try:
                location = self.get_input(board)
                if isinstance(location, str):  # for python3
                    location = [int(n, 10) for n in location.split(",")]
                move = board.location_to_move(location)
            except Exception as e:
                move = -1
        return_var.append(move) 

    def __str__(self):
        return "{} a.k.a Player {}".format(self.NIM,self.player)
    
    def get_input(self, board : Board) -> str:
        """
            Parameter board merepresentasikan papan permainan. Objek board memiliki beberapa
            atribut penting yang dapat menjadi acuan strategi.
            - board.height : int (x) -> panjang papan
            - board.width : int (y) -> lebar papan
            Koordinat 0,0 terletak pada kiri bawah

            [x,0] [x,1] [x,2] . . . [x,y]                               
            . . . . . . . . . . . . . . .  namun perlu diketahui        Contoh 4x4: 
            . . . . . . . . . . . . . . .  bahwa secara internal        11 12 13 14 15
            . . . . . . . . . . . . . . .  sel-sel disimpan dengan  =>  10 11 12 13 14
            [2,0] [2,1] [2,2] . . . [2,y]  barisan interger dimana      5  6  7  8  9
            [1,0] [1,1] [1,2] . . . [1,y]  kiri bawah adalah nol        0  1  2  3  4
            [0,0] [0,1] [0,2] . . . [0,y]          
                                 
            - board.states : dict -> Kondisi papan. 
            Key dari states adalah integer sel (0,1,..., x*y)
            Value adalah integer 1 atau 2:
            -> 1 artinya sudah diisi player 1
            -> 2 artinya sudah diisi player 2

            TODO: Tentukan x,y secara greedy. Kembalian adalah sebuah string "x,y"
        """

        # check if it is the first move
        if len(board.states) == 0 or len(board.states) == 1:
            # if middle is available, put in the middle
            if board.location_to_move([board.height // 2, board.width // 2]) in board.availables:
                return f"{board.height // 2},{board.width // 2}"
            # if middle is not available, put in 0,0
            else:
                return f"0,0"
            
        # check if can 5 in a row, if yes, do it
        # gap
        isWin, type, moves = self.fillGap(board, self.player)
        if isWin:
            moveNum = moves[0]
            moveCoor = board.move_to_location(moveNum)
            valid = self.isValid(board, moveNum)
            if valid:
                return f"{moveCoor[0]},{moveCoor[1]}"
        # 4 in a row
        isWin, type, moves = self.isFour(board, self.player)
        if isWin:
            fill = self.fillFour(board, moves, type)
            if fill != None:
                return fill
            
        # check if opponent's gap can cause 5 in a row, if yes, block it
        isGap, gap, moves = self.fillGap(board, 3 - self.player)
        if isGap:
            moveNum = gap
            moveCoor = board.move_to_location(moveNum)
            valid = self.isValid(board, moveNum)
            if valid:
                self.blockedGap.append(moves)
                return f"{moveCoor[0]},{moveCoor[1]}"

        # check if opponent is 4 in a row
        isFour, type, moves = self.isFour(board, 3 - self.player)
        if isFour:
            fill = self.fillFour(board, moves, type)
            if fill != None:
                return fill
                    
        # check if opponent is 3 in a row
        isThree, type, moves = self.isThree(board, 3 - self.player)
        if isThree:
            fill = self.fillThree(board, moves, type)
            if fill != None:
                return fill

        # scoring with 2 attempts
        pos, direction, secondPos, sencondDirection = self.score(board, self.player)
        fill = self.fillScore(board, pos, self.player, direction)
        if fill != None:
            return fill
        else:
            fill = self.fillScore(board, secondPos, self.player, sencondDirection)
            if fill != None:
                return fill

        # if there is no winning or blocking move, put in random    
        x = random.randint(0, board.height - 1)
        y = random.randint(0, board.width - 1)
        return f"{x},{y}"
    
    # check if there is 3 in a row
    def isThree(self, board: Board, player: int):
        # player's move
        player_moves = []
        for move in board.states:
            if board.states[move] == player:
                player_moves.append(move)

        player_moves.sort()
        
        # check horizontal
        for move in player_moves:
            if move + 1 in player_moves and move + 2 in player_moves:
                if ((move + 1) % 8 == 0 or (move + 2) % 8 == 0) or ([move, move + 1, move + 2] in self.blockedThree):
                    pass
                else:
                    return True, "h", [move, move + 1, move + 2]
            
        # check vertical
        for move in player_moves:
            if move + 8 in player_moves and move + 16 in player_moves:
                if ([move, move + 8, move + 16] in self.blockedThree):
                    pass
                else:
                    return True, "v", [move, move + 8, move + 16]
            
        # check diagonal
        for move in player_moves:
            if move + 7 in player_moves and move + 14 in player_moves:
                if ((move + 7) % 8 == 0 or (move + 14) % 8 == 0) or ([move, move + 7, move + 14] in self.blockedThree):
                    pass
                else:
                    return True, "d", [move, move + 7, move + 14]
            elif move + 9 in player_moves and move + 18 in player_moves:
                if ((move + 9) % 8 == 0 or (move + 18) % 8 == 0) or ([move, move + 9, move + 18] in self.blockedThree):
                    pass
                else:
                    return True, "d", [move, move + 9, move + 18]
                
        return False, None, None
    
    # choose where to fill in 3 in a row
    def fillThree(self, board: Board, moves: list, type: str):
        if type == "h":
            # right edge
            if moves[0] % 8 == 7:
                moveNum = moves[0] - 1
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid:
                    self.blockedThree.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
            # middle and left edge
            else:
                moveNum = moves[2] + 1
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid:
                    self.blockedThree.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
                else:
                    moveNum = moves[0] - 1
                    moveCoor = board.move_to_location(moveNum)
                    valid = self.isValid(board, moveNum)
                    if valid:
                        self.blockedThree.append(moves)
                        return f"{moveCoor[0]},{moveCoor[1]}"
            
        elif type == "v":
            # top edge
            if moves[2] > 55:
                moveNum = moves[0] - 8
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid:
                    self.blockedThree.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
            # middle and bottom edge
            else:
                moveNum = moves[2] + 8
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid:
                    self.blockedThree.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
                else:
                    moveNum = moves[0] - 8
                    moveCoor = board.move_to_location(moveNum)
                    valid = self.isValid(board, moveNum)
                    if valid:
                        self.blockedThree.append(moves)
                        return f"{moveCoor[0]},{moveCoor[1]}"
            
        elif type == "d":
            # bottom left edge
            if moves[0] == 0:
                moveNum = moves[2] + 9
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid:
                    self.blockedThree.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
            # bottom right edge
            elif moves[0] == 7:
                moveNum = moves[2] + 7
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid:
                    self.blockedThree.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
            # top left edge
            elif moves[2] == 56:
                moveNum = moves[0] - 7
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid:
                    self.blockedThree.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
            # top right edge
            elif moves[2] == 63:
                moveNum = moves[0] - 9
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid:
                    self.blockedThree.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
            # middle ascending
            elif moves[0] + 9 == moves[1]:
                moveNum = moves[0] - 9
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid:
                    self.blockedThree.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
            # middle descending
            elif moves[0] + 7 == moves[1]:
                moveNum = moves[0] - 7
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid:
                    self.blockedThree.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
                
        return None
   
    # check if there is 4 in a row
    def isFour(self, board: Board, player: int):
        # player's move
        player_moves = []
        for move in board.states:
            if board.states[move] == player:
                player_moves.append(move)

        player_moves.sort()
        
        # check horizontal
        for move in player_moves:
            if move + 1 in player_moves and move + 2 in player_moves and move + 3 in player_moves:
                if ((move + 1) % 8 == 0 or (move + 2) % 8 == 0 or (move + 3) % 8 == 0) or ([move, move + 1, move + 2, move + 3] in self.blockedFour):
                    pass
                else:
                    return True, "h", [move, move + 1, move + 2, move + 3]
            
        # check vertical
        for move in player_moves:
            if (move + 8 in player_moves and move + 16 in player_moves and move + 24 in player_moves):
                if ([move, move + 8, move + 16, move + 24] in self.blockedFour):
                    pass
                else:
                    return True, "v", [move, move + 8, move + 16, move + 24]
            
        # check diagonal
        for move in player_moves:
            if move + 9 in player_moves and move + 18 in player_moves and move + 27 in player_moves:
                if ((move + 9) % 8 == 0 or (move + 18) % 8 == 0 or (move + 27) % 8 == 0) or ([move, move + 9, move + 18, move + 27] in self.blockedFour):
                    pass
                else:
                    return True, "d", [move, move + 9, move + 18, move + 27]
            if move + 7 in player_moves and move + 14 in player_moves and move + 21 in player_moves:
                if ([move, move + 7, move + 14, move + 21] in self.blockedFour):
                    pass
                else:
                    return True, "d", [move, move + 7, move + 14, move + 21]

        return False, None, None
    
    # choose where to fill in 4 in a row
    def fillFour(self, board: Board, moves: list, type: str):
        if type == "h":
            # left edge
            if moves[0] % 8 == 0:
                moveNum = moves[3] + 1
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid:
                    self.blockedFour.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
            # middle and right edge
            else:
                moveNum = moves[0] - 1
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid:
                    self.blockedFour.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
                else:
                    moveNum = moves[3] + 1
                    moveCoor = board.move_to_location(moveNum)
                    valid = self.isValid(board, moveNum)
                    if valid:
                        self.blockedFour.append(moves)
                        return f"{moveCoor[0]},{moveCoor[1]}"
            
        elif type == "v":
            # bottom edge
            if moves[0] < 8:
                moveNum = moves[3] + 8
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid:
                    self.blockedFour.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
            # middle and top edge
            else:
                moveNum = moves[0] - 8
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid:
                    self.blockedFour.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
                else:
                    moveNum = moves[3] + 8
                    moveCoor = board.move_to_location(moveNum)
                    valid = self.isValid(board, moveNum)
                    if valid:
                        self.blockedFour.append(moves)
                        return f"{moveCoor[0]},{moveCoor[1]}"
            
        elif type == "d":
            # bottom left edge
            if moves[0] == 0:
                moveNum = moves[3] + 9
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid:
                    self.blockedFour.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
            # bottom right edge
            elif moves[0] == 7:
                moveNum = moves[3] + 7
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid:
                    self.blockedFour.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
            # top left edge
            elif moves[3] == 56:
                moveNum = moves[0] - 7
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid:
                    self.blockedFour.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
            # top right edge
            elif moves[3] == 63:
                moveNum = moves[0] - 9
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid:
                    self.blockedFour.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
            # middle ascending
            elif moves[0] + 9 == moves[1]:
                moveNum = moves[0] - 9
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid:
                    self.blockedFour.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
            # middle descending
            elif moves[0] + 7 == moves[1]:
                moveNum = moves[0] - 7
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid:
                    self.blockedFour.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
                
        return None
    
    # check if gap can cause 5 in a row, returns the gap
    def fillGap(self, board: Board, player: int):
        # player's move
        player_moves = []
        for move in board.states:
            if board.states[move] == player:
                player_moves.append(move)

        player_moves.sort()
        
        # check horizontal
        for move in player_moves:
            move1 = move + 1
            move2 = move + 2
            move3 = move + 3
            move4 = move + 4
            check = ((move1) % 8 == 0 or (move2) % 8 == 0 or (move3) % 8 == 0 or (move4) % 8 == 0) or ([move, move1, move2, move3, move4] in self.blockedGap)
            if (move2 in player_moves and move3 in player_moves and move4 in player_moves):
                if check:
                    pass
                else:
                    return True, move1, [move, move1, move2, move3, move4]
            elif (move1 in player_moves and move3 in player_moves and move4 in player_moves):
                if check:
                    pass
                else:
                    return True, move2, [move, move1, move2, move3, move4]
            elif (move1 in player_moves and move2 in player_moves and move4 in player_moves):
                if check:
                    pass
                else:
                    return True, move3, [move, move1, move2, move3, move4]
                
        # check vertical
        for move in player_moves:
            move1 = move + 8
            move2 = move + 16
            move3 = move + 24
            move4 = move + 32
            check = ([move, move1, move2, move3, move4] in self.blockedGap)
            if (move2 in player_moves and move3 in player_moves and move4 in player_moves):
                if check:
                    pass
                else:
                    return True, move1, [move, move1, move2, move3, move4]
            elif (move1 in player_moves and move3 in player_moves and move4 in player_moves):
                if check:
                    pass
                else:
                    return True, move2, [move, move1, move2, move3, move4]
            elif (move1 in player_moves and move2 in player_moves and move4 in player_moves):
                if check:
                    pass
                else:
                    return True, move3, [move, move1, move2, move3, move4]
                
        # check diagonal
        for move in player_moves:
            move1 = move + 9
            move2 = move + 18
            move3 = move + 27
            move4 = move + 36
            check = ((move1) % 8 == 0 or (move2) % 8 == 0 or (move3) % 8 == 0 or (move4) % 8 == 0) or ([move, move1, move2, move3, move4] in self.blockedGap)
            if (move2 in player_moves and move3 in player_moves and move4 in player_moves):
                if check:
                    pass
                else:
                    return True, move1, [move, move1, move2, move3, move4]
            elif (move1 in player_moves and move3 in player_moves and move4 in player_moves):
                if check:
                    pass
                else:
                    return True, move2, [move, move1, move2, move3, move4]
            elif (move1 in player_moves and move2 in player_moves and move4 in player_moves):
                if check:
                    pass
                else:
                    return True, move3, [move, move1, move2, move3, move4]
            elif (move1 in player_moves and move2 in player_moves and move3 in player_moves):
                if check:
                    pass
                else:
                    return True, move4, [move, move1, move2, move3, move4]
                
            move1 = move + 7
            move2 = move + 14
            move3 = move + 21
            move4 = move + 28
            check = ([move, move1, move2, move3, move4] in self.blockedGap)
            if (move2 in player_moves and move3 in player_moves and move4 in player_moves):
                if check:
                    pass
                else:
                    return True, move1, [move, move1, move2, move3, move4]
            elif (move1 in player_moves and move3 in player_moves and move4 in player_moves):
                if check:
                    pass
                else:
                    return True, move2, [move, move1, move2, move3, move4]
            elif (move1 in player_moves and move2 in player_moves and move4 in player_moves):
                if check:
                    pass
                else:
                    return True, move3, [move, move1, move2, move3, move4]
        
        return False, None, None  
            
    # score
    def score(self, board: Board, player: int):
        # opponent's move -120
        # player's move +120
        # available move +60
        # divide by distance, closer is better

        # player's move
        player_moves = []
        for move in board.states:
            if board.states[move] == player:
                player_moves.append(move)
        player_moves.sort()

        # opponent's move
        opponent_moves = []
        for move in board.states:
            if board.states[move] == 3 - player:
                opponent_moves.append(move)
        opponent_moves.sort()

        # available moves
        available_moves = board.availables

        scoreList = []

        for move in player_moves:

            score = 0
            # check 5 rows rightside
            rightMoves = []
            for i in range(1, 5):
                rightMoves.append(move + i)
            for i in range(0, 4):
                if rightMoves[i] in player_moves:
                    score += 120 / (i + 1)
                elif rightMoves[i] in opponent_moves:
                    score -= 120 / (i + 1)
                elif rightMoves[i] in available_moves:
                    score += 60 / (i + 1)
            scoreList.append(score)

            score = 0
            # check 5 rows leftside
            leftMoves = []
            for i in range(1, 5):
                leftMoves.append(move - i)
            for i in range(0,4):
                if leftMoves[i] in player_moves:
                    score += 120 / (i + 1)
                elif leftMoves[i] in opponent_moves:
                    score -= 120 / (i + 1)
                elif leftMoves[i] in available_moves:
                    score += 60 / (i + 1)
            scoreList.append(score)

            score = 0
            # check 5 rows upside
            upMoves = []
            for i in range(1, 5):
                upMoves.append(move + 8 * i)
            for i in range(0,4):
                if upMoves[i] in player_moves:
                    score += 120 / (i + 1)
                elif upMoves[i] in opponent_moves:
                    score -= 120 / (i + 1)
                elif upMoves[i] in available_moves:
                    score += 60 / (i + 1)
            scoreList.append(score)

            score = 0
            # check 5 rows downside
            downMoves = []
            for i in range(1, 5):
                downMoves.append(move - 8 * i)
            for i in range(0,4):
                if downMoves[i] in player_moves:
                    score += 120 / (i + 1)
                elif downMoves[i] in opponent_moves:
                    score -= 120 / (i + 1)
                elif downMoves[i] in available_moves:
                    score += 60 / (i + 1)
            scoreList.append(score)

            score = 0
            # check 5 rows diagonal uprightside
            uprightMoves = []
            for i in range(1, 5):
                uprightMoves.append(move + 9 * i)
            for i in range(0,4):
                if uprightMoves[i] in player_moves:
                    score += 120 / (i + 1)
                elif uprightMoves[i] in opponent_moves:
                    score -= 120 / (i + 1)
                elif uprightMoves[i] in available_moves:
                    score += 60 / (i + 1)
            scoreList.append(score)

            score = 0
            # check 5 rows diagonal downrightside
            downrightMoves = []
            for i in range(1, 5):
                downrightMoves.append(move - 7 * i)
            for i in range(0,4):
                if downrightMoves[i] in player_moves:
                    score += 120 / (i + 1)
                elif downrightMoves[i] in opponent_moves:
                    score -= 120 / (i + 1)
                elif downrightMoves[i] in available_moves:
                    score += 60 / (i + 1)
            scoreList.append(score)

            score = 0
            # check 5 rows diagonal upleftside
            upleftMoves = []
            for i in range(1, 5):
                upleftMoves.append(move + 7 * i)
            for i in range(0,4):
                if upleftMoves[i] in player_moves:
                    score += 120 / (i + 1)
                elif upleftMoves[i] in opponent_moves:
                    score -= 120 / (i + 1)
                elif upleftMoves[i] in available_moves:
                    score += 60 / (i + 1)
            scoreList.append(score)

            score = 0
            # check 5 rows diagonal downleftside
            downleftMoves = []
            for i in range(1, 5):
                downleftMoves.append(move - 9 * i)
            for i in range(0,4):
                if downleftMoves[i] in player_moves:
                    score += 120 / (i + 1)
                elif downleftMoves[i] in opponent_moves:
                    score -= 120 / (i + 1)
                elif downleftMoves[i] in available_moves:
                    score += 60 / (i + 1)
            scoreList.append(score)
        
        # find the best move
        bestMove = 0
        bestScore = 0
        for i in range(len(scoreList)):
            if scoreList[i] > bestScore:
                bestScore = scoreList[i]
                bestMove = i

        move = bestMove // 8
        dir = bestMove % 8

        if dir == 0:
            direction = "right"
        elif dir == 1:
            direction = "left"
        elif dir == 2:
            direction = "up"
        elif dir == 3:
            direction = "down"
        elif dir == 4:
            direction = "upright"
        elif dir == 5:
            direction = "downright"
        elif dir == 6:
            direction = "upleft"
        elif dir == 7:
            direction = "downleft"

        # find second best move
        secondBestMove = 0
        secondBestScore = 0
        for i in range(len(scoreList)):
            if scoreList[i] > secondBestScore and i != bestMove:
                secondBestScore = scoreList[i]
                secondBestMove = i

        secondMove = secondBestMove // 8
        secondDir = secondBestMove % 8

        if secondDir == 0:
            secondDirection = "right"
        elif secondDir == 1:
            secondDirection = "left"
        elif secondDir == 2:
            secondDirection = "up"
        elif secondDir == 3:
            secondDirection = "down"
        elif secondDir == 4:
            secondDirection = "upright"
        elif secondDir == 5:
            secondDirection = "downright"
        elif secondDir == 6:
            secondDirection = "upleft"
        elif secondDir == 7:
            secondDirection = "downleft"        

        return move, direction, secondMove, secondDirection
    
    # fill the board with scoring move
    def fillScore(self, board: Board, pos: int, player: int, direction: str):
        # player's move
        player_moves = []
        for move in board.states:
            if board.states[move] == player:
                player_moves.append(move)
        player_moves.sort()

        move = player_moves[pos]

        if direction == "right":
            for i in range(1, 5):
                moveNum = move + i
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid and moveNum % 8 != 0:
                    return f"{moveCoor[0]},{moveCoor[1]}"
        elif direction == "left":
            for i in range(1, 5):
                moveNum = move - i
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid and moveNum % 8 != 7:
                    return f"{moveCoor[0]},{moveCoor[1]}"
        elif direction == "up":
            for i in range(1, 5):
                moveNum = move + 8 * i
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid and moveNum < 64:
                    return f"{moveCoor[0]},{moveCoor[1]}"
        elif direction == "down":
            for i in range(1, 5):
                moveNum = move - 8 * i
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid and moveNum >= 0:
                    return f"{moveCoor[0]},{moveCoor[1]}"
        elif direction == "upright":
            for i in range(1, 5):
                moveNum = move + 9 * i
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid and moveNum < 64 and moveNum % 8 != 0:
                    return f"{moveCoor[0]},{moveCoor[1]}"
        elif direction == "downright":
            for i in range(1, 5):
                moveNum = move - 7 * i
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid and moveNum >= 0 and moveNum % 8 != 0:
                    return f"{moveCoor[0]},{moveCoor[1]}"
        elif direction == "upleft":
            for i in range(1, 5):
                moveNum = move + 7 * i
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid and moveNum < 64 and moveNum % 8 != 7:
                    return f"{moveCoor[0]},{moveCoor[1]}"
        elif direction == "downleft":
            for i in range(1, 5):
                moveNum = move - 9 * i
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                if valid and moveNum >= 0 and moveNum % 8 != 7:
                    return f"{moveCoor[0]},{moveCoor[1]}"
        
        return None
            
    
    # check if the move is valid
    def isValid(self, board: Board, move: int) -> bool:
        return move in board.availables

