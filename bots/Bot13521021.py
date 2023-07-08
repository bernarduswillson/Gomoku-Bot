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
                    print("horizontal 3")
                    return True, "h", [move, move + 1, move + 2]
            
        # check vertical
        for move in player_moves:
            if move + 8 in player_moves and move + 16 in player_moves:
                if ([move, move + 8, move + 16] in self.blockedThree):
                    pass
                else:
                    print("vertical 3")
                    return True, "v", [move, move + 8, move + 16]
            
        # check diagonal
        for move in player_moves:
            if move + 7 in player_moves and move + 14 in player_moves:
                if ((move + 7) % 8 == 0 or (move + 14) % 8 == 0) or ([move, move + 7, move + 14] in self.blockedThree):
                    pass
                else:
                    print("diagonal 3")
                    return True, "d", [move, move + 7, move + 14]
            elif move + 9 in player_moves and move + 18 in player_moves:
                if ((move + 9) % 8 == 0 or (move + 18) % 8 == 0) or ([move, move + 9, move + 18] in self.blockedThree):
                    pass
                else:
                    print("diagonal 3")
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
                    print("horizontal 4")
                    return True, "h", [move, move + 1, move + 2, move + 3]
            
        # check vertical
        for move in player_moves:
            if (move + 8 in player_moves and move + 16 in player_moves and move + 24 in player_moves):
                if ([move, move + 8, move + 16, move + 24] in self.blockedFour):
                    pass
                else:
                    print("vertical 4")
                    return True, "v", [move, move + 8, move + 16, move + 24]
            
        # check diagonal
        for move in player_moves:
            if move + 9 in player_moves and move + 18 in player_moves and move + 27 in player_moves:
                if ((move + 9) % 8 == 0 or (move + 18) % 8 == 0 or (move + 27) % 8 == 0) or ([move, move + 9, move + 18, move + 27] in self.blockedFour):
                    pass
                else:
                    print("diagonal 4")
                    return True, "d", [move, move + 9, move + 18, move + 27]
            if move + 7 in player_moves and move + 14 in player_moves and move + 21 in player_moves:
                if ([move, move + 7, move + 14, move + 21] in self.blockedFour):
                    print("diagonal 4 gagal")
                    pass
                else:
                    print("diagonal 4")
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
                print("botleft")
                if valid:
                    self.blockedFour.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
            # bottom right edge
            elif moves[0] == 7:
                moveNum = moves[3] + 7
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                print("botright")
                if valid:
                    self.blockedFour.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
            # top left edge
            elif moves[3] == 56:
                moveNum = moves[0] - 7
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                print("MASUK SINI topleft")
                if valid:
                    self.blockedFour.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
            # top right edge
            elif moves[3] == 63:
                moveNum = moves[0] - 9
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                print("topright")
                if valid:
                    self.blockedFour.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
            # middle ascending
            elif moves[0] + 9 == moves[1]:
                moveNum = moves[0] - 9
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                print("ascending")
                if valid:
                    self.blockedFour.append(moves)
                    return f"{moveCoor[0]},{moveCoor[1]}"
            # middle descending
            elif moves[0] + 7 == moves[1]:
                moveNum = moves[0] - 7
                moveCoor = board.move_to_location(moveNum)
                valid = self.isValid(board, moveNum)
                print("descending")
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
                    print("gap horizontal 1")
                    return True, move1, [move, move1, move2, move3, move4]
            elif (move1 in player_moves and move3 in player_moves and move4 in player_moves):
                if check:
                    pass
                else:
                    print("gap horizontal 2")
                    return True, move2, [move, move1, move2, move3, move4]
            elif (move1 in player_moves and move2 in player_moves and move4 in player_moves):
                if check:
                    pass
                else:
                    print("gap horizontal 3")
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
                    print("gap vertical 1")
                    return True, move1, [move, move1, move2, move3, move4]
            elif (move1 in player_moves and move3 in player_moves and move4 in player_moves):
                if check:
                    pass
                else:
                    print("gap vertical 2")
                    return True, move2, [move, move1, move2, move3, move4]
            elif (move1 in player_moves and move2 in player_moves and move4 in player_moves):
                if check:
                    pass
                else:
                    print("gap vertical 3")
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
                    print("gap diagonal 1")
                    return True, move1, [move, move1, move2, move3, move4]
            elif (move1 in player_moves and move3 in player_moves and move4 in player_moves):
                if check:
                    pass
                else:
                    print("gap diagonal 2")
                    return True, move2, [move, move1, move2, move3, move4]
            elif (move1 in player_moves and move2 in player_moves and move4 in player_moves):
                if check:
                    pass
                else:
                    print("gap diagonal 3")
                    return True, move3, [move, move1, move2, move3, move4]
            elif (move1 in player_moves and move2 in player_moves and move3 in player_moves):
                if check:
                    pass
                else:
                    print("gap diagonal 4")
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
                    print("gap diagonal 5")
                    return True, move1, [move, move1, move2, move3, move4]
            elif (move1 in player_moves and move3 in player_moves and move4 in player_moves):
                if check:
                    pass
                else:
                    print("gap diagonal 6")
                    return True, move2, [move, move1, move2, move3, move4]
            elif (move1 in player_moves and move2 in player_moves and move4 in player_moves):
                if check:
                    pass
                else:
                    print("gap diagonal 7")
                    return True, move3, [move, move1, move2, move3, move4]
        
        return False, None, None  
            
    
    # check if the move is valid
    def isValid(self, board: Board, move: int) -> bool:
        print(move)
        print(board.availables)
        return move in board.availables

