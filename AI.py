from enum import Enum

class Data():
    '''class Data() recives data from main file'''

    # Tablica z całą planszą
    board = ["", "", "", "", "", "", "", "", ""]

    def data(self, btn_s, x_o):
        '''Metoda zapisuje ruch gracza do listy'''
        move = self.switch(btn_s)
        self.board[move-1] = x_o

    def move(self, x_or_o):
        '''Metoda wywołuje Klase MiniMax i zapisująca ruch do listy'''
        move = MiniMaxAI().get_best_move(self.board, x_or_o)
        self.board[move-1]= x_or_o
        return move

    def restart(self):
        '''Metoda czyści tablice z planszą'''
        for x in range(9):
            self.board[x]= ""

    def switch(self, btn):
        '''Metoda zwraca id przycisku na podstawie stringa np: btn3 zwraca 3'''
        return int(btn[3])

class MiniMaxAI():
    '''Klasa zawierająca metody które zwracają najlepszy ruch w danej pozycji'''

    def human_ai(self, x_or_o):
        '''Metoda zwraca symbol którym gra grasz oraz którym gra AI'''

        if x_or_o == "X":
            ai_player = "X"
            human_player = "O"

        else:
            ai_player = "O"
            human_player = "X"

        return ai_player, human_player

    def minimax(self, board, depth, maximizing, ai_player, human_player):
        '''Metoda zwraca ocene pozycji dla podanej planszy w liście "board"'''

        result = self.get_winner(board)
        if result is not None:
            if ai_player == "O":
                score = PointsForO[result].value
            else:
                score = PointsForX[result].value
            return score

        if maximizing:
            best_score_max = float('-inf')
            for maxi in range(9):
                if board[maxi] == "":
                    board[maxi] = ai_player
                    score = self.minimax(board, depth + 1, False, ai_player, human_player)
                    board[maxi] = ""
                    best_score_max = max(score, best_score_max)
            return best_score_max

        elif not maximizing:
            best_score_min = float('inf')
            for mini in range(9):
                if board[mini] == "":
                    board[mini] = human_player
                    score = self.minimax(board, depth + 1, True, ai_player, human_player)
                    board[mini] = ""
                    best_score_min = min(score, best_score_min)
            return best_score_min

    def get_best_move(self, board, x_or_o):
        '''Metoda zwraca najlepszy ruch w pozycji, 
        przyjmuje jako argumenty plansze oraz symbol którym gra AI'''

        result = self.human_ai(x_or_o)
        ai_player = result[0]
        human_player = result[1]
        best_score = float('-inf')
        move = None

        for i in range(9):
            if board[i] == "":
                board[i] = ai_player
                score = self.minimax(board, 0, False, ai_player, human_player)
                board[i]=""
                if score>best_score:
                    best_score = score
                    move = i
        return move+1

    def is_board_full(self, board):
        '''Funkcja zwraca True jeżeli lista "board" jest pełna'''
        for i in range(9):
            if board[i]=="":
                return False
        return True

    def get_winner(self, board):
        '''Funkcja sprawdza czy ktoś wygrał. Jeśli ktoś wygrał zwraca kto'''
        winner = False

        # Poziomo
        for x in range(0,9,3):
            if  board[x]!="" and board[x] == board[x+1] == board[x+2]:
                winner = True
                return board[x]
        # Pionowo
        for x in range(3):
            if board[x]!="" and board[x] == board[x+3] == board[x+6]:
                winner = True
                return board[x]
        # Na skos
        if board[0]!="" and board[0] == board[4] == board[8]:
            winner = True
            return board[0]
        if board[2]!="" and board[2] == board[4] == board[6]:
            winner = True
            return board[2]

        if not winner and self.is_board_full(board):
            return "Tie"
        else:
            return None

class PointsForO(Enum):
    '''Enum z wynikami końcówek gry jeśli graczem maksymalizującym jest O'''
    X = -1
    O = 1
    Tie = 0
class PointsForX(Enum):
    '''Enum z wynikami końcówek gry jeśli graczem maksymalizującym jest O'''

    X = 1
    O = -1
    Tie = 0
