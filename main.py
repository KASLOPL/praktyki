from kivy.lang import Builder
from kivymd.app import MDApp
import mysql.connector
import AI
from kivy.uix.screenmanager import ScreenManager, Screen

class LobbyWindow(Screen):
    pass

class MainWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class XorOWindow(Screen):
    pass

# Main klasa
class Code(MDApp):

    def build(self):
        # Ustawienia aplikacji i zwracanie wyglądu z pliku kv
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('style.kv')
    
    def toSelection(self):
        self.root.current = "XorO"

    def press_PvP(self):
        self.root.current = "main"
        self.on_load()

    def press_PvE(self):
        self.root.current = "main"
        self.on_load()

    def IsAI(self, XorO):
        self.press_PvE()
        self.IsBot = True
        self.PlayerSymbol = XorO
        if XorO == "X":
            self.AISymbol = "O"
        else:
            self.AISymbol = "X"

        if XorO == "O":
            self.press("","")

    def on_load(self):
        self.Stats1()
        self.Stats2()

    # Wpisywanie odpowiedzich wyników do Labelów
    def Stats1(self):

        # Połączenie z bazą danych oraz stworzenie obiektu kursor
        DataBase = mysql.connector.connect(host="localhost", user="root", password="", database="kolko_wyniki")
        MyCursor=DataBase.cursor()

        # Zapytania wyciągające z tabeli ile razy wygrał X a ile O
        SelectQueryX="select count(id_meczu) from wyniki where wynik=1"
        SelectQueryO="select count(id_meczu) from wyniki where wynik=0"

        # Zapisywanie do zmiennej wyniku zapytania
        MyCursor.execute(SelectQueryX)
        ResultX = MyCursor.fetchall()
        ResultX = ResultX[0]

        # Zapisywanie do zmiennej wyniku zapytania
        MyCursor.execute(SelectQueryO)
        ResultO = MyCursor.fetchall()
        ResultO = ResultO[0]

        # Zapisywanie wyników do "stats"
        self.root.ids.main_window.ids.stats.text=f"X won {ResultX[0]} times | O won {ResultO[0]} times"

    def Stats2(self):
        # Połączenie z bazą danych oraz stworzenie obiektu kursor
        DataBase = mysql.connector.connect(host="localhost", user="root", password="", database="kolko_wyniki")
        MyCursor=DataBase.cursor()

        # Wszystkie zapyania SQL potrzebne do tej funkcji
        CountId="select count(id_meczu) from wyniki"
        CountX="select count(id_meczu) from wyniki where wynik=1"
        CountO="select count(id_meczu) from wyniki where wynik=0"
        CountTie="select count(id_meczu) from wyniki where wynik=2"

        # Zapisywanie do zmiennej wyniku zapytania
        MyCursor.execute(CountId)
        ResultId = MyCursor.fetchall()
        ResultId = ResultId[0]

        # Zapisywanie do zmiennej wyniku zapytania
        MyCursor.execute(CountX)
        ResultX = MyCursor.fetchall()
        ResultX = ResultX[0]

        # Zapisywanie do zmiennej wyniku zapytania
        MyCursor.execute(CountO)
        ResultO = MyCursor.fetchall()
        ResultO = ResultO[0]

        # Zapisywanie do zmiennej wyniku zapytania
        MyCursor.execute(CountTie)
        ResultTie = MyCursor.fetchall()
        ResultTie = ResultTie[0]

        # Obliczanie procętów potrzebnych do statystyk
        X_prc = ResultX[0]/ResultId[0]
        O_prc = ResultO[0]/ResultId[0]
        Tie_prc = ResultTie[0]/ResultId[0]

        # Zapisywanie wyników do "stats2"
        self.root.ids.main_window.ids.stats2.text=f"X wins: {int(round(X_prc, 2)*100)}% | O wins: {int(round(O_prc, 2)*100)}% | Ties: {int(round(Tie_prc, 2)*100)}%"        
    
    # Zmianna do sprawdzania czyja kolej
    turn = "X"
    # Zmienna do sprawdzania czy ktoś wygrał
    winner = False
    # Zmienna do sprawdzania czy jest remis
    tie_q = False
    # Zmienna określająca tryb gry
    IsBot = False
    # Podczas gry z botrm określa jakim znakiem gra gracz
    PlayerSymbol = ""

    AISymbol = ""

    # Funkcja do sprawdzania czy ktoś wygrał
    def checkWinner(self):

        # Poziomo
        if self.root.ids.main_window.ids.btn1.text != "" and self.root.ids.main_window.ids.btn1.text == self.root.ids.main_window.ids.btn2.text and self.root.ids.main_window.ids.btn2.text == self.root.ids.main_window.ids.btn3.text:
            self.EndGame(self.root.ids.main_window.ids.btn1, self.root.ids.main_window.ids.btn2, self.root.ids.main_window.ids.btn3)

        if self.root.ids.main_window.ids.btn4.text != "" and self.root.ids.main_window.ids.btn4.text == self.root.ids.main_window.ids.btn5.text and self.root.ids.main_window.ids.btn5.text == self.root.ids.main_window.ids.btn6.text:
            self.EndGame(self.root.ids.main_window.ids.btn4, self.root.ids.main_window.ids.btn5, self.root.ids.main_window.ids.btn6)
            
        if self.root.ids.main_window.ids.btn7.text != "" and self.root.ids.main_window.ids.btn7.text == self.root.ids.main_window.ids.btn8.text and self.root.ids.main_window.ids.btn8.text == self.root.ids.main_window.ids.btn9.text:
            self.EndGame(self.root.ids.main_window.ids.btn7, self.root.ids.main_window.ids.btn8, self.root.ids.main_window.ids.btn9)
            
        # Pionowo
        if self.root.ids.main_window.ids.btn1.text != "" and self.root.ids.main_window.ids.btn1.text == self.root.ids.main_window.ids.btn4.text and self.root.ids.main_window.ids.btn4.text == self.root.ids.main_window.ids.btn7.text:
            self.EndGame(self.root.ids.main_window.ids.btn1, self.root.ids.main_window.ids.btn4, self.root.ids.main_window.ids.btn7)

        if self.root.ids.main_window.ids.btn2.text != "" and self.root.ids.main_window.ids.btn2.text == self.root.ids.main_window.ids.btn5.text and self.root.ids.main_window.ids.btn5.text == self.root.ids.main_window.ids.btn8.text:
            self.EndGame(self.root.ids.main_window.ids.btn2, self.root.ids.main_window.ids.btn5, self.root.ids.main_window.ids.btn8)
            
        if self.root.ids.main_window.ids.btn3.text != "" and self.root.ids.main_window.ids.btn3.text == self.root.ids.main_window.ids.btn6.text and self.root.ids.main_window.ids.btn6.text == self.root.ids.main_window.ids.btn9.text:
            self.EndGame(self.root.ids.main_window.ids.btn3, self.root.ids.main_window.ids.btn6, self.root.ids.main_window.ids.btn9)

        # Po skosie
        if self.root.ids.main_window.ids.btn1.text != "" and self.root.ids.main_window.ids.btn1.text == self.root.ids.main_window.ids.btn5.text and self.root.ids.main_window.ids.btn5.text == self.root.ids.main_window.ids.btn9.text:
            self.EndGame(self.root.ids.main_window.ids.btn1, self.root.ids.main_window.ids.btn5, self.root.ids.main_window.ids.btn9)

        if self.root.ids.main_window.ids.btn3.text != "" and self.root.ids.main_window.ids.btn3.text == self.root.ids.main_window.ids.btn5.text and self.root.ids.main_window.ids.btn5.text == self.root.ids.main_window.ids.btn7.text:
            self.EndGame(self.root.ids.main_window.ids.btn3, self.root.ids.main_window.ids.btn5, self.root.ids.main_window.ids.btn7)
        
        self.tie()

    # Sprawdzanie czy jest remis
    def tie(self):
        if self.winner == False and self.root.ids.main_window.ids.btn1.text != ""\
        and self.root.ids.main_window.ids.btn2.text != ""\
        and self.root.ids.main_window.ids.btn3.text != ""\
        and self.root.ids.main_window.ids.btn4.text != ""\
        and self.root.ids.main_window.ids.btn5.text != ""\
        and self.root.ids.main_window.ids.btn6.text != ""\
        and self.root.ids.main_window.ids.btn7.text != ""\
        and self.root.ids.main_window.ids.btn8.text != ""\
        and self.root.ids.main_window.ids.btn9.text != ""    :
            self.root.ids.main_window.ids.score.text = "IT'S A TIE!!!"
            self.tie_q = True
            
            # Wpisywanie remisu do tabeli wyniki
            InsertQuery="insert into wyniki (id_meczu, wynik) values(null, 2)"

            # Połączenie z bazą danych oraz stworzenie obiektu kursor
            DataBase = mysql.connector.connect(host="localhost", user="root", password="", database="kolko_wyniki")
            MyCursor=DataBase.cursor()

            # wysyłanie zapytania do bazy danych
            MyCursor.execute(InsertQuery)
            DataBase.commit()


    # Funkcja kończonca grę
    def EndGame(self, a, b, c):
        self.winner = True

        # Pokolorawanie wygrywającej lini
        a.color = "red"
        b.color = "red"
        c.color = "red"

        # Wyłączaenie wszystkich przycisków
        self.DisableAllButtons()

        # Wypisujemy kto wygrał
        self.root.ids.main_window.ids.score.text = f"{a.text} Wins"

        # Zmiana X i O na inta
        if a.text=="X":
            db_winner= 1
        else:
            db_winner= 0

        # Połączenie z bazą danych oraz stworzenie obiektu kursor
        DataBase = mysql.connector.connect(host="localhost", user="root", password="", database="kolko_wyniki")
        MyCursor=DataBase.cursor()

        # Zapytanie wpisujące rekord do tabeli
        InsertQuery=f"insert into wyniki (id_meczu, wynik) values(null, {db_winner})"

        # Wysyłanie zapytania do bazy danych
        MyCursor.execute(InsertQuery)
        DataBase.commit()

        self.Stats1()
        self.Stats2()

    # Wyłączaneie wszystkich przycisków
    def DisableAllButtons(self):
        self.root.ids.main_window.ids.btn1.disabled = True
        self.root.ids.main_window.ids.btn2.disabled = True
        self.root.ids.main_window.ids.btn3.disabled = True
        self.root.ids.main_window.ids.btn4.disabled = True
        self.root.ids.main_window.ids.btn5.disabled = True
        self.root.ids.main_window.ids.btn6.disabled = True
        self.root.ids.main_window.ids.btn7.disabled = True
        self.root.ids.main_window.ids.btn8.disabled = True
        self.root.ids.main_window.ids.btn9.disabled = True

    # Funkcja którą wywołuje wciśniecię któregokolwiek pola na planszy
    def press(self, btn, btn_s):
        # Zmienić na onButtonClick

        if self.IsBot == False:

            # Ten if powoduje pojawienie się X lub O i wyłączanie przycisków po ich naciśnięciu
            if self.turn =="X":

                btn.text = "X"
                btn.disabled = True
                self.root.ids.main_window.ids.score.text = "O's Turn!"
                self.turn = "O"
            else:

                btn.text = "O"
                btn.disabled = True
                self.root.ids.main_window.ids.score.text = "X's Turn!"
                self.turn = "X"
        else:
            if self.turn =="X" and self.turn == self.PlayerSymbol:
                
                # Przesyłanie które pole zostało kliknięte do pliku AI
                AI.Data().data(btn_s, "X")

                btn.text = "X"
                btn.disabled = True
                self.root.ids.main_window.ids.score.text = "O's Turn!"
                self.turn = "O"
            elif self.turn =="X" and self.turn != self.PlayerSymbol:
                move = AI.Data().move("O")
                self.PressByAI(move)
                self.turn= "O"

            elif self.turn =="O" and self.turn != self.PlayerSymbol:

                # Wywołanie ruchu wykonywanego przez AI
                move = AI.Data().move("X")
                self.PressByAI(move)
                self.turn= "X"
            
            elif self.turn =="O" and self.turn == self.PlayerSymbol:
                # Przesyłanie które pole zostało kliknięte do pliku AI
                AI.Data().data(btn_s, "O")

                btn.text = "O"
                btn.disabled = True
                self.root.ids.main_window.ids.score.text = "X's Turn!"
                self.turn = "X"

        # Nastęne akcje
        self.checkWinner()
        self.root.md_bg_color= 0,0,0,1
        if self.turn !=self.PlayerSymbol and self.winner == False and self.tie_q == False and self.IsBot== True:
            self.press("","")

    # Zmiana liczby na id przycisku
    def PressByAI(self, btn):
        if btn==1:
            self.root.ids.main_window.ids.btn1.text = self.AISymbol
            self.root.ids.main_window.ids.btn1.disabled = True
        elif btn==2:
            self.root.ids.main_window.ids.btn2.text = self.AISymbol
            self.root.ids.main_window.ids.btn2.disabled = True
        elif btn==3:
            self.root.ids.main_window.ids.btn3.text = self.AISymbol
            self.root.ids.main_window.ids.btn3.disabled = True
        elif btn==4:
            self.root.ids.main_window.ids.btn4.text = self.AISymbol
            self.root.ids.main_window.ids.btn4.disabled = True
        elif btn==5:
            self.root.ids.main_window.ids.btn5.text = self.AISymbol
            self.root.ids.main_window.ids.btn5.disabled = True
        elif btn==6:
            self.root.ids.main_window.ids.btn6.text = self.AISymbol
            self.root.ids.main_window.ids.btn6.disabled = True
        elif btn==7:
            self.root.ids.main_window.ids.btn7.text = self.AISymbol
            self.root.ids.main_window.ids.btn7.disabled = True
        elif btn==8:
            self.root.ids.main_window.ids.btn8.text = self.AISymbol
            self.root.ids.main_window.ids.btn8.disabled = True
        elif btn==9:
            self.root.ids.main_window.ids.btn9.text = self.AISymbol
            self.root.ids.main_window.ids.btn9.disabled = True

        self.turn="X"

    # Funkcja do resetowania gry
    def restart(self):

        # Zawsze zaczyna X więc zmieniam zmienną turn na "X"
        self.turn = "X"

        # Przywracam przyciski tak aby znowu można było w nie klikać
        self.root.ids.main_window.ids.btn1.disabled = False
        self.root.ids.main_window.ids.btn2.disabled = False
        self.root.ids.main_window.ids.btn3.disabled = False
        self.root.ids.main_window.ids.btn4.disabled = False
        self.root.ids.main_window.ids.btn5.disabled = False
        self.root.ids.main_window.ids.btn6.disabled = False
        self.root.ids.main_window.ids.btn7.disabled = False
        self.root.ids.main_window.ids.btn8.disabled = False
        self.root.ids.main_window.ids.btn9.disabled = False

        # Resetowanie tablicy w pliku AI
        AI.Data().restart()

        # Czyszcze przyciski tak aby nie było na nich żadnych napisów
        self.root.ids.main_window.ids.btn1.text = ""
        self.root.ids.main_window.ids.btn2.text = ""
        self.root.ids.main_window.ids.btn3.text = ""
        self.root.ids.main_window.ids.btn4.text = ""
        self.root.ids.main_window.ids.btn5.text = ""
        self.root.ids.main_window.ids.btn6.text = ""
        self.root.ids.main_window.ids.btn7.text = ""
        self.root.ids.main_window.ids.btn8.text = ""
        self.root.ids.main_window.ids.btn9.text = ""

        # Resetuje kolory przycisków
        self.root.ids.main_window.ids.btn1.color = "gray"
        self.root.ids.main_window.ids.btn2.color = "gray"
        self.root.ids.main_window.ids.btn3.color = "gray"
        self.root.ids.main_window.ids.btn4.color = "gray"
        self.root.ids.main_window.ids.btn5.color = "gray"
        self.root.ids.main_window.ids.btn6.color = "gray"
        self.root.ids.main_window.ids.btn7.color = "gray"
        self.root.ids.main_window.ids.btn8.color = "gray"
        self.root.ids.main_window.ids.btn9.color = "gray"

        # Przywracam Label "score" do wartości początkowaj
        self.root.ids.main_window.ids.score.text = "X GOES FIRST!"

        # Resetowanie zmiennej winner
        self.winner = False
        self.tie_q = False

        if self.IsBot == True and self.AISymbol == "X":
            self.press("", "")

if __name__=="__main__":
    #BuildClass().run()
    Code().run()