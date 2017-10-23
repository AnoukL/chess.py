# Anouk Luypaert
# Chess, Homework 4
# November 2016

White=1
Black=2

# pc = (chess) piece

class Chesspiece:
    def __init__(self, colour, abbr, name, pos=None):
        self.colour = colour
        self.pos = pos
        self.abbr = abbr
        self.name = name

    def __str__(self):
        colours = {1: "White ", 2 : "Black "}
        
        if self.name != "horse":
            return colours[self.colour] + str(self.name)
        else:
            if self.colour == 1:
                return "White " +str(self.name)
            else:
                return "Black " + str(self.name)

    def get_colour(self):
        return self.colour

    def valid_moves(self, chessboard, colour=None):
        return []

    def is_king_safe(self, moves, Sbord, colour=None):
        """ Simulates pc's moves on chess bord to see if the moves would
        endanger the king. colour is only used to avoid infinite loops. """
        pos_compet_moves = []
        
        # For each move this makes a backup of the original setup, then
        # simulates the move and checks if any of the opponent's moves can
        # slay the king
        for pos in moves:
            original_pos = self.pos
            original_pc = Sbord.stuk_op(pos)
            Sbord.verplaats(self, pos)
            for row in Sbord.bord:
                for pc in row:
                    try:
                        if pc.colour != self.colour:
                            for zet in pc.valid_moves(Sbord, pc.colour):
                                try:
                                    if Sbord.stuk_op(zet).name == "king" \
                                   and Sbord.stuk_op(zet).colour != pc.colour:
                                        pos_compet_moves.append(pos)
                                except AttributeError:
                                    continue
                    except AttributeError:     
                        continue       
            Sbord.plaats(self, original_pos)
            if original_pc == None:
                Sbord.bord[8 - pos[0]][pos[1] - 1 ] = "."
            else:
                Sbord.bord[8 - pos[0]][pos[1] - 1 ] = original_pc
                
        # Remove each move that makes it possible for the opponent to slay
        # the king.
        for pos in pos_compet_moves:
            if pos in moves:
                moves.remove(pos)

        return moves

    def straight_moves(self, chessboard, row_dir, col_dir):
        """ Calculates valid moves given a chess board, a direction for
        the row (0 = constant, 1 = up, -1 = down) and a direction for
        the column (0 = constant, 1 = right, -1 = left). It can only be used
        for pcs that move in straight lines: bishop, queen and rook. """
        
        moves = []
        row, col = self.pos[0] + row_dir, self.pos[1] + col_dir

        while 0 < row < 9 and 0 < col < 9:
            if chessboard.stuk_op((row, col)) != None:
                if chessboard.stuk_op((row, col)).colour != self.colour:
                    moves.append((row, col))
                break # once the pc meets another pc, movement is stopped
            else:
                moves.append((row, col))
                row += row_dir
                col += col_dir
                
        return moves

        
class Pion(Chesspiece):
    def __init__(self, colour, pos=None):
        Chesspiece.__init__(self, colour, "P", "pion")

    def valid_moves(self, chessboard, colour=None):
        """ Calculates valid moves for a pawn. """

        # White pawns can only move up and black only down, so we can
        # assume that when a pawn is still on the initial row (2 or 7),
        # the pawn hasn't been moved yet. col - 1 = left,
        # col + 1 = right, row - 1 = down, row + 1 = up
        
        possible_moves = []
        row, col = self.pos

        if self.colour == 1 and row < 8: # check if pc is white
            if chessboard.stuk_op((row + 1, col)) == None:
                possible_moves.append((row + 1, col))
                if row == 2 and chessboard.stuk_op((row + 2, col)) == None: 
                        possible_moves.append((row + 2, col))
            if col > 1: # try slaying pc one up - left
                if chessboard.stuk_op((row + 1, col - 1)) != None \
                   and chessboard.stuk_op((row + 1, col - 1)).colour == 2:
                    possible_moves.append((row + 1, col - 1))    
            if col < 8: # try slaying pc one up - right
                if chessboard.stuk_op((row + 1, col + 1)) != None \
                   and chessboard.stuk_op((row + 1, col + 1)).colour == 2:
                    possible_moves.append((row + 1, col + 1))
                    
        if self.colour == 2 and row > 1: # check if pc is black
            if chessboard.stuk_op((row - 1, col)) == None:
                possible_moves.append((row - 1, col))
                if row == 7 and chessboard.stuk_op((row - 2, col)) == None: 
                    possible_moves.append((row - 2, col))                
            if col > 1: # try slaying pc one down - left
                if chessboard.stuk_op((row - 1, col - 1)) != None \
                   and chessboard.stuk_op((row - 1, col - 1)).colour == 1:
                    possible_moves.append((row - 1, col - 1))    
            if col < 8 : # try slaying pc one down - right
                if chessboard.stuk_op((row - 1, col + 1)) != None \
                   and chessboard.stuk_op((row - 1, col + 1)).colour == 1:
                    possible_moves.append((row - 1, col + 1))

        if colour == None:
            self.is_king_safe(possible_moves, chessboard)
            
        return possible_moves        

        
class Toren(Chesspiece):
    def __init__(self, colour, pos=None):
        Chesspiece.__init__(self, colour, "R", "toren")

    def valid_moves(self, chessboard, colour=None):
        """ Calculates the valid moves for a Rook. """
        
        possible_moves = self.straight_moves(chessboard, 1, 0) \
                         + self.straight_moves(chessboard, -1, 0) \
                         + self.straight_moves(chessboard, 0, 1) \
                         + self.straight_moves(chessboard, 0, -1)       

        if colour == None:
            self.is_king_safe(possible_moves, chessboard)
            
        return possible_moves

        
class horse(Chesspiece):
    def __init__(self, colour, pos=None):
        Chesspiece.__init__(self, colour, "N", "horse")

    def valid_moves(self, chessboard, colour=None):
        """ Calculates the valid moves for a knight. """

        # A knight pc can move 2 steps vertically/horizontally and then 1
        # step horizontally/vertically.The absolute value of the sum of
        # the steps in both directions should then always be 1 or 3.
        
        possible_moves = []
        row, col = self.pos

        for row_direct in [-1, 1, -2, 2]:
            for col_direct in [-1, 1, -2, 2]:
                move = (row + row_direct, col + col_direct)
                if 0 < move[0] < 9 and 0 < move[1] < 9:
                    if abs(row_direct + col_direct) == 3 \
                       or abs(row_direct + col_direct) == 1:
                        if chessboard.stuk_op(move) != None:
                            if chessboard.stuk_op(move).colour != self.colour:
                                possible_moves.append(move)
                        else:
                            possible_moves.append(move)

        if colour == None:
            self.is_king_safe(possible_moves,chessboard)
            
        return possible_moves


class Loper(Chesspiece):
    def __init__(self, colour, pos=None):
        Chesspiece.__init__(self, colour, "B", "loper")

    def valid_moves(self, chessboard, colour=None):
        """ Calculates the valid moves for a Bishop. """
        
        possible_moves = self.straight_moves(chessboard, 1, 1) \
                         + self.straight_moves(chessboard, 1, -1) \
                         + self.straight_moves(chessboard, -1, 1) \
                         + self.straight_moves(chessboard, -1, -1)

        if colour == None:
            self.is_king_safe(possible_moves,chessboard)
            
        return possible_moves


class kingin(Chesspiece):
    def __init__(self,colour, pos=None):
        Chesspiece.__init__(self, colour, "Q", "kingin")

    def valid_moves(self, chessboard, colour=None):
        """ Calculates the valid moves for a Queen. """

        possible_moves = self.straight_moves(chessboard, 1, 1) \
                         + self.straight_moves(chessboard, 1, -1) \
                         + self.straight_moves(chessboard, -1, 1) \
                         + self.straight_moves(chessboard, -1, -1) \
                         + self.straight_moves(chessboard, 1, 0) \
                         + self.straight_moves(chessboard, -1, 0) \
                         + self.straight_moves(chessboard, 0, 1) \
                         + self.straight_moves(chessboard, 0, -1) 

        if colour == None:
            self.is_king_safe(possible_moves, chessboard)
            
        return possible_moves


class king(Chesspiece):
    def __init__(self, colour, pos=None):
        Chesspiece.__init__(self, colour, "K", "king")

    def valid_moves(self, chessboard, colour=None):
        """ Calculates the valid moves for a King. """
        possible_moves = []
        row, col = self.pos

        for row_direct in [-1, 0, 1]:
            for col_direct in [-1, 0, 1]:
                move = (row + row_direct, col + col_direct)
                if 0 < move[0] < 9 and 0 < move[1] < 9:
                    if chessboard.stuk_op(move) != None:
                        if chessboard.stuk_op(move).colour != self.colour:
                            possible_moves.append(move)
                    else:
                        possible_moves.append(move)

        if colour == None:
            self.is_king_safe(possible_moves,chessboard)

        return possible_moves


class chessboard:
    """ Defines a chess board as a list of lists. """ 
    # Rules for positions on chess board vs the index in list of lists:
    # pc.pos[0] = the row position of pc on the chess board,
    # pc.pos[1] = the column position of pc on the chess board
    # (8 - pos[0]) is then the index of the list in the lists,
    # (pos[1] - 1) is then the position in that list.
    # So if pc.pos is (5,1), its position in the lists is bord[3][0] 

    def __init__(self):
        self.bord = []
        for row in range(8):
            new_row = []
            for column in range(8):
                new_row.append(".")
            self.bord.append(new_row)

    def __str__(self):
        output = ""
        columns = [" ", "a", "b", "c", "d", "e", "f", "g", "h"]
        colours = { 1: "w", 2: "b"}

        for column in columns:
            output += column + "\t"
        output += "\n"

        index = 8
        for row in self.bord:
            output += str(index) + "\t"
            for item in row:
                if item == ".":
                    output += str(item) + " \t"
                else:
                    output += item.abbr + colours[item.colour] + "\t"
            index -= 1
            if index > 0: # don't print a new line when all rows are printed
                output += "\n"
                
        return output

    def plaats(self, stuk, pos):
        """ Puts a piece on a given position. """
        row, column = 8 - pos[0], pos[1] - 1
        self.bord[row][column] = stuk
        stuk.pos = pos

    def verwijder(self, stuk):
        """ Removes a piece from the board. """
        row, column = 8 - stuk.pos[0], stuk.pos[1] - 1
        self.bord[row][column] = "."
        stuk.pos = None

    def verplaats(self, stuk, pos):
        """ Moves a piece to a different position. """
        self.verwijder(stuk)
        self.plaats(stuk, pos)

    def waar_is(self, stuk):
        """ Returns a piece's location. """
        return stuk.pos

    def stuk_op(self, pos):
        """ Returns the piece that's on a given location. """
        row, column = 8 - pos[0], pos[1] - 1             
        if self.bord[row][column] != ".":
            return self.bord[row][column]
         
    def zet_begin_positie(self):
        """ Puts all pieces on the chessbord. """
        
        # "all_pcs" gives a list of all column positions per pc.
        # "functions" maps each pc to the class function, so you can
        # iterate over all_pieces and call the function. "colours" lists
        # the row positions per color, Whiteh the first item being the row
        # for the pawns and the second item the row for other pieces.
        
        all_pcs = {"pion" : [1, 2, 3, 4, 5, 6, 7, 8], "toren" : [1, 8],
                      "king" : [5], "kingin" : [4], "loper" : [3, 6],
                      "horse" : [2, 7]}
        functions = {"pion" : Pion, "toren" : Toren, "king" : king,
                     "kingin" : kingin, "loper" : Loper, "horse" : horse}
        colours = { Black : [7, 8],  White: [2, 1]}
                      
        for colour in colours:
            for item in all_pcs:
                if item == "pion":
                    row = colours[colour][0]
                else:
                    row = colours[colour][1] 
                for column in all_pcs[item]:
                    self.plaats(functions[item](colour), (row, column))

    def speel(self, Chesspiece, pos):
        """ Move a piece to another position if the move is valid. """

        opties = Chesspiece.valid_moves(self)

        if opties == []:
            print("Dit Chesspiece heeft geen mogelijke zetten.")    
        else:
            if pos in opties:
                self.verplaats(Chesspiece, pos)
            else:
                print("Ongeldige zet: " + str(Chesspiece) +
                      " kan enkel verplaatst worden naar: " + str(opties))

    def schaak(self, colour):
        """ Checks if the given colour is check. """
        pos_king = ()
        opponent_moves = []
        
        for row in self.bord:
            for pc in row:
                try:
                    if pc.name == "king" and pc.colour == colour:
                        pos_king = pc.pos
                    elif pc.colour != colour:
                        for pos in pc.valid_moves(self):
                            opponent_moves.append(pos)
                except AttributeError:
                    continue

        return pos_king in set(opponent_moves)     

    def are_there_moves(self, colour):
        """ Checks if there is a piece of the given colour that can still
        move. """
        for row in self.bord:
            for pc in row:
                try:
                    if pc.colour == colour and pc.valid_moves(self) != []:
                           return True
                except AttributeError:
                    continue
        return False
     
    def schaakmat(self, colour):
        """ Checks if the given colour is checkmate. """
        return self.schaak(colour) and not self.are_there_moves(colour)

    def pat(self, colour):           
        return not self.schaak(colour) and not self.are_there_moves(colour)

def one_turn(chessboard, colour):
    """ Plays one turn of chess for a given colour. """
    columns = {"a" : 1, "b": 2, "c" : 3, "d" : 4, "e" : 5, "f" : 6, "g" : 7,
               "h" : 8}
    colours = { 1: "White", 2: "Black"}
    moved = False
    
    while not moved:
        if chessboard.schaak(colour):
            print("Opgepast!", colours[colour].capitalize(),
                  "staat schaak! Breng je king in veiligheid!")
        move = input(colours[colour] + " aan zet: ")
        try:
            start_pos = (int(move[1]), columns[move[0]])
            end_pos = (int(move[4]), columns[move[3]])
            piece_to_play = S.stuk_op(start_pos)
            try:
                if piece_to_play.colour == colour:
                    S.speel(piece_to_play, end_pos)
                    if piece_to_play.pos == end_pos and start_pos != end_pos:
                        print(S, "\n")
                        moved = True
                else:
                    print("Invalid move ! No", colours[colour],
                          "piece at position", move[:2] + ".")
            except AttributeError:
                print("There is no chesspiece at position", move[:2] + ".")
        except (IndexError, ValueError, KeyError):
            print("These are no correct positions. Try again.")
                     
if __name__ == "__main__":
    print("Welcome! A new game has been set up")
    print("You can move pieces by entering the start position of the piece you'd like",
          "to move in the form of e.g. 'e2', followed by a separator (e.g. '-')",
          "followed by the position to which you would like to move the piece",
          "e2-e4' then moves the piece at e2 to e4.")
    S = chessboard()
    S.zet_begin_positie()
    print(S, "\n")

    while True:
        one_turn(S, White) # According to the rules, white always starts.
        if S.schaakmat(Black):
            print("Proficiat! Black staat schaakmat. White is gewonnen!")
            break
        if S.pat(Black):
            print("Proficiat! Black staat pat. White is gewonnen!")
            break
        one_turn(S, Black)
        if S.schaakmat(White):
            print("Proficiat! White staat schaakmat. Black is gewonnen!")
            break
        if S.pat(White):
            print("Proficiat! White staat pat. Black is gewonnen!")
            break         
