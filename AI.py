from enum import Enum

class Data():
    '''class Data() recives data from main file'''

    # Tablica z całą planszą
    board = ["", "", "", "", "", "", "", "", ""]

    # Funkcja imortująca kliknięcia z pliku main
    def data(self, btn_s, x_o):
        move = self.switch(btn_s)
        self.writing(move, x_o)

    # Funkcja przypisująca wykonane ruchy do tablicy board
    def writing(self, move, x_o):
        self.board[move-1] = x_o
        print(self.board)

    # Funkcja wywołująca funkcje która zwraca na którym polu ma zostać postawiony znak
    def move(self, x_or_o):
        print(x_or_o)
        move = MiniMax_AI().best_move(self.board, x_or_o)
        self.board[move-1]= x_or_o
        print(self.board)
        return move

    # Funkcja resetująca tablice "board"
    def restart(self):
        for x in range(9):
            self.board[x]= ""

    # Funkcja zmieniająca np. "btn1" na 1
    def switch(self, btn):
        if btn=="btn1":
            return 1
        if btn=="btn2":
            return 2
        if btn=="btn3":
            return 3
        if btn=="btn4":
            return 4
        if btn=="btn5":
            return 5
        if btn=="btn6":
            return 6
        if btn=="btn7":
            return 7
        if btn=="btn8":
            return 8
        if btn=="btn9":
            return 9

# Główna klasa zawierająca cały kod algorytmu MiniMax (AI)   
class MiniMax_AI():

    # Funkcja określa kto gra którym znakiem
    def HumanAI(self, x_or_o):
        
        if x_or_o == "X":

            AIPlayer = "X"
            HumanPlayer = "O"
        
        else:
            AIPlayer = "O"
            HumanPlayer = "X"

        return AIPlayer, HumanPlayer

    # Funkcja zawierająca algorytm MiniMax
    def minimax(self, board, depth, Maximizing, AIPlayer, HumanPlayer):
        
        # Sprawdzanie czy kotś wygrał lub zremisował
        result = self.checkWinner(board)
        # Jeśli ktoś wygrał lub zremisował zwraca wynik
        if result is not None:
            if AIPlayer == "O":
                score = PointsForO[result].value
            else:
                score = PointsForX[result].value
            return score

        # Algorytm dla gracza maksymalizującego wynik
        if Maximizing == True:
            BestScoreMax = float('-inf')
            for maxi in range(9):
                if board[maxi] == "":
                    board[maxi] = AIPlayer
                    score = self.minimax(board, depth + 1, False, AIPlayer, HumanPlayer)
                    board[maxi] = ""
                    BestScoreMax = max(score, BestScoreMax)
            return BestScoreMax
        
        #Algorytm dla gracza minimalizującego wynik
        elif Maximizing == False:
            BestScoreMin = float('inf')
            for mini in range(9):
                if board[mini] == "":
                    board[mini] = HumanPlayer
                    score = self.minimax(board, depth + 1, True, AIPlayer, HumanPlayer)
                    board[mini] = ""
                    BestScoreMin = min(score, BestScoreMin)
            return BestScoreMin

    def best_move(self, board, x_or_o):

        result = self.HumanAI(x_or_o)
        AIPlayer = result[0]
        HumanPlayer = result[1]

        BestScore = float('-inf')
        Move = None

        # Sprawdzanie każdego wolnego miejsca i określanie wyniku dla tego miejsca
        for i in range(9):
            if board[i] == "":
                board[i] = AIPlayer
                score = self.minimax(board, 0, False, AIPlayer, HumanPlayer)
                board[i]=""
                if score>BestScore:
                    BestScore = score
                    Move = i
        return Move+1

    
    # Funkcja zwracająca True jeżeli planasza jest całą zapełniona
    def IsBoardFull(self, board):
        for i in range(9):
            if board[i]=="":
                return False
        return True
    
    # Funkcja sprawdzającza czy ktoś wygrał
    def checkWinner(self, board):

        winner = False

        # Poziomo
        if board[0]!="" and board[0] == board[1] == board[2]:
            winner = True
            return board[0]
        if board[3]!="" and board[3] == board[4] == board[5]:
            winner = True
            return board[3]
        if board[6]!="" and board[6] == board[7] == board[8]:
            winner = True
            return board[6]
        
        # Pionowo
        if board[0]!="" and board[0] == board[3] == board[6]:
            winner = True
            return board[0]
        if board[1]!="" and board[1] == board[4] == board[7]:
            winner = True
            return board[1]
        if board[2]!="" and board[2] == board[5] == board[8]:
            winner = True
            return board[2]
        
        # Na skos
        if board[0]!="" and board[0] == board[4] == board[8]:
            winner = True
            return board[0]
        if board[2]!="" and board[2] == board[4] == board[6]:
            winner = True
            return board[2]
        
        if winner==False and self.IsBoardFull(board)==True:
            return "Tie"
        else:
            return None 

# Enum zwracające wynik dla każdego z końców gry jeśli gramczem maksymalizującym jest O
class PointsForO(Enum):
    X = -1
    O = 1
    Tie = 0

    # Enum zwracające wynik dla każdego z końców gry jeśli gramczem maksymalizującym jest X
class PointsForX(Enum):
    X = 1
    O = -1
    Tie = 0