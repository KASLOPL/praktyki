from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivymd.app import MDApp
import mysql.connector
import AI


class LobbyWindow(Screen):
    '''Definiowanie okna używanych przez aplikacje'''

class MainWindow(Screen):
    '''Definiowanie okna używanych przez aplikacje'''


class WindowManager(ScreenManager):
    '''Definiowanie okna używanych przez aplikacje'''

class XorOWindow(Screen):
    '''Definiowanie okna używanych przez aplikacje'''

class Code(MDApp):
    '''Główna klasa zawierająca funkcje i metody potrzebne do gry'''

    def build(self):
        # Ustawienia aplikacji i zwracanie wyglądu z pliku kv
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('style.kv')

    def to_selection(self):
        '''Zmienia wyświetlane okno na XorO'''

        self.root.current = "XorO"

    def to_game(self):
        '''Zmienia wyświetlane okno na XorO'''

        self.root.current = "main"
        self.on_load()

    def if_ai(self, x_or_o):
        '''Metoda zmienia zmienne przechowywujace symbole AI i gracza'''

        self.to_game()
        self.is_bot = True
        self.player_symbol = x_or_o
        if x_or_o == "X":
            self.ai_symbol = "O"
        else:
            self.ai_symbol = "X"

        if x_or_o == "O":
            self.press("","")

    def on_load(self):
        '''Metoda aktualizuje statysyki'''
        self.stats_1()
        self.stats_2()

    def stats_1(self):
        '''Metoda wypisuje pierwsze statystyki na ekran'''

        data_base = mysql.connector.connect(host="localhost", user="root", password="", database="kolko_wyniki")
        my_cursor=data_base.cursor()

        select_query_x="select count(id_meczu) from wyniki where wynik=1"
        select_query_o="select count(id_meczu) from wyniki where wynik=0"

        my_cursor.execute(select_query_x)
        resultx = my_cursor.fetchall()
        resultx = resultx[0]
        my_cursor.execute(select_query_o)
        resulto = my_cursor.fetchall()
        resulto = resulto[0]

        self.root.ids.main_window.ids.stats.text=f"X won {resultx[0]} times | O won {resulto[0]} times"

    def stats_2(self):
        '''Metoda wypisuje drugie statystyki na ekran'''

        data_base = mysql.connector.connect(host="localhost", user="root", password="", database="kolko_wyniki")
        my_cursor=data_base.cursor()

        count_id="select count(id_meczu) from wyniki"
        count_x="select count(id_meczu) from wyniki where wynik=1"
        count_o="select count(id_meczu) from wyniki where wynik=0"
        count_tie="select count(id_meczu) from wyniki where wynik=2"

        my_cursor.execute(count_id)
        result_id = my_cursor.fetchall()
        result_id = result_id[0]
        my_cursor.execute(count_x)
        resultx = my_cursor.fetchall()
        resultx = resultx[0]
        my_cursor.execute(count_o)
        resulto = my_cursor.fetchall()
        resulto = resulto[0]
        my_cursor.execute(count_tie)
        result_tie = my_cursor.fetchall()
        result_tie = result_tie[0]
        x_prc = resultx[0]/result_id[0]
        o_prc = resulto[0]/result_id[0]
        tie_prc = result_tie[0]/result_id[0]

        self.root.ids.main_window.ids.stats2.text=f"X wins: {int(round(x_prc, 2)*100)}% | O wins: {int(round(o_prc, 2)*100)}% | Ties: {int(round(tie_prc, 2)*100)}%"   

    # Zmianna do sprawdzania czyja kolej
    turn = "X"
    # Zmienna do sprawdzania czy ktoś wygrał
    winner = False
    # Zmienna do sprawdzania czy jest remis
    tie_q = False
    # Zmienna określająca tryb gry
    is_bot = False
    # Podczas gry z botrm określa jakim znakiem gra gracz
    player_symbol = ""
    # Podczas gry z botrm określa jakim znakiem gra bot
    ai_symbol = ""

    def check_winner(self):
        '''Metoda sprawdza czy ktoś mecz się zakończył'''

        # Poziomo
        if self.root.ids.main_window.ids.btn1.text != "" and self.root.ids.main_window.ids.btn1.text == self.root.ids.main_window.ids.btn2.text and self.root.ids.main_window.ids.btn2.text == self.root.ids.main_window.ids.btn3.text:
            self.end_game(self.root.ids.main_window.ids.btn1, self.root.ids.main_window.ids.btn2, self.root.ids.main_window.ids.btn3)

        if self.root.ids.main_window.ids.btn4.text != "" and self.root.ids.main_window.ids.btn4.text == self.root.ids.main_window.ids.btn5.text and self.root.ids.main_window.ids.btn5.text == self.root.ids.main_window.ids.btn6.text:
            self.end_game(self.root.ids.main_window.ids.btn4, self.root.ids.main_window.ids.btn5, self.root.ids.main_window.ids.btn6)
            
        if self.root.ids.main_window.ids.btn7.text != "" and self.root.ids.main_window.ids.btn7.text == self.root.ids.main_window.ids.btn8.text and self.root.ids.main_window.ids.btn8.text == self.root.ids.main_window.ids.btn9.text:
            self.end_game(self.root.ids.main_window.ids.btn7, self.root.ids.main_window.ids.btn8, self.root.ids.main_window.ids.btn9)
            
        # Pionowo
        if self.root.ids.main_window.ids.btn1.text != "" and self.root.ids.main_window.ids.btn1.text == self.root.ids.main_window.ids.btn4.text and self.root.ids.main_window.ids.btn4.text == self.root.ids.main_window.ids.btn7.text:
            self.end_game(self.root.ids.main_window.ids.btn1, self.root.ids.main_window.ids.btn4, self.root.ids.main_window.ids.btn7)

        if self.root.ids.main_window.ids.btn2.text != "" and self.root.ids.main_window.ids.btn2.text == self.root.ids.main_window.ids.btn5.text and self.root.ids.main_window.ids.btn5.text == self.root.ids.main_window.ids.btn8.text:
            self.end_game(self.root.ids.main_window.ids.btn2, self.root.ids.main_window.ids.btn5, self.root.ids.main_window.ids.btn8)
            
        if self.root.ids.main_window.ids.btn3.text != "" and self.root.ids.main_window.ids.btn3.text == self.root.ids.main_window.ids.btn6.text and self.root.ids.main_window.ids.btn6.text == self.root.ids.main_window.ids.btn9.text:
            self.end_game(self.root.ids.main_window.ids.btn3, self.root.ids.main_window.ids.btn6, self.root.ids.main_window.ids.btn9)

        # Po skosie
        if self.root.ids.main_window.ids.btn1.text != "" and self.root.ids.main_window.ids.btn1.text == self.root.ids.main_window.ids.btn5.text and self.root.ids.main_window.ids.btn5.text == self.root.ids.main_window.ids.btn9.text:
            self.end_game(self.root.ids.main_window.ids.btn1, self.root.ids.main_window.ids.btn5, self.root.ids.main_window.ids.btn9)

        if self.root.ids.main_window.ids.btn3.text != "" and self.root.ids.main_window.ids.btn3.text == self.root.ids.main_window.ids.btn5.text and self.root.ids.main_window.ids.btn5.text == self.root.ids.main_window.ids.btn7.text:
            self.end_game(self.root.ids.main_window.ids.btn3, self.root.ids.main_window.ids.btn5, self.root.ids.main_window.ids.btn7)
        
        self.tie()

    def tie(self):
        '''Metoda sprawdza czy i wykonuje akcje związane z remisem'''
        if not self.winner and self.root.ids.main_window.ids.btn1.text != ""\
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
            
            insert_query="insert into wyniki (id_meczu, wynik) values(null, 2)"

            data_base = mysql.connector.connect(host="localhost", user="root", password="", database="kolko_wyniki")
            my_cursor=data_base.cursor()

            my_cursor.execute(insert_query)
            data_base.commit()

    def end_game(self, a, b, c):
        '''Metoda kończąca grę, przyjmuje jako argumenty 3 przyciski które są w wygranym rzędzie'''
        self.winner = True

        a.color = "red"
        b.color = "red"
        c.color = "red"

        self.disable_all_buttons()

        self.root.ids.main_window.ids.score.text = f"{a.text} Wins"

        if a.text=="X":
            db_winner= 1
        else:
            db_winner= 0

        data_base = mysql.connector.connect(host="localhost", user="root", password="", database="kolko_wyniki")
        my_cursor=data_base.cursor()

        insert_query=f"insert into wyniki (id_meczu, wynik) values(null, {db_winner})"

        my_cursor.execute(insert_query)
        data_base.commit()

        self.stats_1()
        self.stats_2()

    # Wyłączaneie wszystkich przycisków
    def disable_all_buttons(self):
        '''Metoda wyłącza wszystki buttony'''
        self.root.ids.main_window.ids.btn1.disabled = True
        self.root.ids.main_window.ids.btn2.disabled = True
        self.root.ids.main_window.ids.btn3.disabled = True
        self.root.ids.main_window.ids.btn4.disabled = True
        self.root.ids.main_window.ids.btn5.disabled = True
        self.root.ids.main_window.ids.btn6.disabled = True
        self.root.ids.main_window.ids.btn7.disabled = True
        self.root.ids.main_window.ids.btn8.disabled = True
        self.root.ids.main_window.ids.btn9.disabled = True

    def on_press(self, btn, btn_s):
        '''Metoda wywoływana klknięciem w przycisk, przyjmuje jako argumenty id klikniętego przycisku'''
        if not self.is_bot:
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
            if self.turn =="X" and self.turn == self.player_symbol:
                AI.Data().data(btn_s, "X")

                btn.text = "X"
                btn.disabled = True
                self.root.ids.main_window.ids.score.text = "O's Turn!"
                self.turn = "O"

            elif self.turn =="X" and self.turn != self.player_symbol:
                move = AI.Data().move("X")
                self.press_by_ai(move)
                self.turn= "O"

            elif self.turn =="O" and self.turn != self.player_symbol:
                move = AI.Data().move("O")
                self.press_by_ai(move)
                self.turn= "X"

            elif self.turn =="O" and self.turn == self.player_symbol:
                AI.Data().data(btn_s, "O")

                btn.text = "O"
                btn.disabled = True
                self.root.ids.main_window.ids.score.text = "X's Turn!"
                self.turn = "X"

        self.check_winner()
        self.root.md_bg_color= 0,0,0,1
        if self.turn !=self.player_symbol and not self.winner and not self.tie_q and self.is_bot:
            self.press("","")

    def press_by_ai(self, btn):
        '''Metoda wciska przycisk wybrany przez AI'''
        if btn==1:
            self.root.ids.main_window.ids.btn1.text = self.ai_symbol
            self.root.ids.main_window.ids.btn1.disabled = True
        elif btn==2:
            self.root.ids.main_window.ids.btn2.text = self.ai_symbol
            self.root.ids.main_window.ids.btn2.disabled = True
        elif btn==3:
            self.root.ids.main_window.ids.btn3.text = self.ai_symbol
            self.root.ids.main_window.ids.btn3.disabled = True
        elif btn==4:
            self.root.ids.main_window.ids.btn4.text = self.ai_symbol
            self.root.ids.main_window.ids.btn4.disabled = True
        elif btn==5:
            self.root.ids.main_window.ids.btn5.text = self.ai_symbol
            self.root.ids.main_window.ids.btn5.disabled = True
        elif btn==6:
            self.root.ids.main_window.ids.btn6.text = self.ai_symbol
            self.root.ids.main_window.ids.btn6.disabled = True
        elif btn==7:
            self.root.ids.main_window.ids.btn7.text = self.ai_symbol
            self.root.ids.main_window.ids.btn7.disabled = True
        elif btn==8:
            self.root.ids.main_window.ids.btn8.text = self.ai_symbol
            self.root.ids.main_window.ids.btn8.disabled = True
        elif btn==9:
            self.root.ids.main_window.ids.btn9.text = self.ai_symbol
            self.root.ids.main_window.ids.btn9.disabled = True

        self.turn="X"

    def restart(self):
        '''Metoda wykonuje wszystkie akcje związane z resetoowaniem gry'''

        self.turn = "X"

        self.root.ids.main_window.ids.btn1.disabled = False
        self.root.ids.main_window.ids.btn2.disabled = False
        self.root.ids.main_window.ids.btn3.disabled = False
        self.root.ids.main_window.ids.btn4.disabled = False
        self.root.ids.main_window.ids.btn5.disabled = False
        self.root.ids.main_window.ids.btn6.disabled = False
        self.root.ids.main_window.ids.btn7.disabled = False
        self.root.ids.main_window.ids.btn8.disabled = False
        self.root.ids.main_window.ids.btn9.disabled = False

        AI.Data().restart()

        self.root.ids.main_window.ids.btn1.text = ""
        self.root.ids.main_window.ids.btn2.text = ""
        self.root.ids.main_window.ids.btn3.text = ""
        self.root.ids.main_window.ids.btn4.text = ""
        self.root.ids.main_window.ids.btn5.text = ""
        self.root.ids.main_window.ids.btn6.text = ""
        self.root.ids.main_window.ids.btn7.text = ""
        self.root.ids.main_window.ids.btn8.text = ""
        self.root.ids.main_window.ids.btn9.text = ""

        self.root.ids.main_window.ids.btn1.color = "gray"
        self.root.ids.main_window.ids.btn2.color = "gray"
        self.root.ids.main_window.ids.btn3.color = "gray"
        self.root.ids.main_window.ids.btn4.color = "gray"
        self.root.ids.main_window.ids.btn5.color = "gray"
        self.root.ids.main_window.ids.btn6.color = "gray"
        self.root.ids.main_window.ids.btn7.color = "gray"
        self.root.ids.main_window.ids.btn8.color = "gray"
        self.root.ids.main_window.ids.btn9.color = "gray"

        self.root.ids.main_window.ids.score.text = "X GOES FIRST!"

        self.winner = False
        self.tie_q = False

        if self.is_bot and self.ai_symbol == "X":
            self.press("", "")

if __name__=="__main__":
    Code().run()
