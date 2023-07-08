import globals as globals

class Human(object):
    """
    human player
    """

    def __init__(self):
        self.player = None
        self.NIM = 'Human'

    def set_player_ind(self, p):
        self.player = p

    def get_input(self) -> str:
        location = input("Your move: ")
        return location
        
    def get_action(self, board, return_var):
        try:
            location = self.get_input()
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
        return "Human {}".format(self.player)