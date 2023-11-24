from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivymd.app import MDApp
import mysql.connector
import AI


class LobbyWindow(Screen):
    '''#*Definiowanie okna używanych przez aplikacje'''
    pass

class MainWindow(Screen):
    '''#*Definiowanie okna używanych przez aplikacje'''
    pass

class WindowManager(ScreenManager):
    '''#*Definiowanie okna używanych przez aplikacje'''
    pass

class XorOWindow(Screen):
    '''#*Definiowanie okna używanych przez aplikacje'''
    pass

class Code(MDApp):
    '''#*Główna klasa zawierająca funkcje i metody potrzebne do gry'''

    data_base = mysql.connector.connect(host="localhost", user="root", password="", database="kolko_wyniki")
    my_cursor=data_base.cursor()
    
    def site_connection(self):
        '''Pomocnik'''
        return self.root.ids.main_window.ids

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('style.kv')

    def to_selection(self):
        '''#*Zmienia wyświetlane okno na XorO'''

        self.root.current = "XorO"

    def to_game(self):
        '''#*Zmienia wyświetlane okno na XorO'''

        self.root.current = "main"
        self.on_load()

    def if_ai(self, x_or_o):
        '''#*Metoda zmienia zmienne przechowywujace symbole AI i gracza'''

        self.to_game()
        self.is_bot = True
        self.player_symbol = x_or_o
        if x_or_o == "X":
            self.ai_symbol = "O"
        else:
            self.ai_symbol = "X"

        if x_or_o == "O":
            self.on_press("","")

    def on_load(self):
        '''#*Metoda aktualizuje statysyki'''
        self.stats_1()
        self.stats_2()

    def stats_1(self):
        '''#*Metoda wypisuje pierwsze statystyki na ekran'''
        select_query_x="select count(id_meczu) from wyniki where wynik=1"
        select_query_o="select count(id_meczu) from wyniki where wynik=0"

        self.my_cursor.execute(select_query_x)
        resultx = self.my_cursor.fetchall()
        resultx = resultx[0]
        self.my_cursor.execute(select_query_o)
        resulto = self.my_cursor.fetchall()
        resulto = resulto[0]

        self.site_connection().stats.text=f"X won {resultx[0]} times | O won {resulto[0]} times"

    def stats_2(self):
        '''#*Metoda wypisuje drugie statystyki na ekran'''

        count_id="select count(id_meczu) from wyniki"
        count_x="select count(id_meczu) from wyniki where wynik=1"
        count_o="select count(id_meczu) from wyniki where wynik=0"
        count_tie="select count(id_meczu) from wyniki where wynik=2"

        self.my_cursor.execute(count_id)
        result_id = self.my_cursor.fetchall()
        result_id = result_id[0]
        self.my_cursor.execute(count_x)
        resultx = self.my_cursor.fetchall()
        resultx = resultx[0]
        self.my_cursor.execute(count_o)
        resulto = self.my_cursor.fetchall()
        resulto = resulto[0]
        self.my_cursor.execute(count_tie)
        result_tie = self.my_cursor.fetchall()
        result_tie = result_tie[0]
        x_prc = resultx[0]/result_id[0]
        o_prc = resulto[0]/result_id[0]
        tie_prc = result_tie[0]/result_id[0]

        self.site_connection().stats2.text=f"X wins: {int(round(x_prc, 2)*100)}% | O wins: {int(round(o_prc, 2)*100)}% | Ties: {int(round(tie_prc, 2)*100)}%"   

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
        '''#*Metoda sprawdza czy ktoś mecz się zakończył'''

        # Poziomo
        if self.site_connection().btn1.text != "" and self.site_connection().btn1.text == self.site_connection().btn2.text and self.site_connection().btn2.text == self.site_connection().btn3.text:
            self.end_game(self.site_connection().btn1, self.site_connection().btn2, self.site_connection().btn3)

        if self.site_connection().btn4.text != "" and self.site_connection().btn4.text == self.site_connection().btn5.text and self.site_connection().btn5.text == self.site_connection().btn6.text:
            self.end_game(self.site_connection().btn4, self.site_connection().btn5, self.site_connection().btn6)
            
        if self.site_connection().btn7.text != "" and self.site_connection().btn7.text == self.site_connection().btn8.text and self.site_connection().btn8.text == self.site_connection().btn9.text:
            self.end_game(self.site_connection().btn7, self.site_connection().btn8, self.site_connection().btn9)
            
        # Pionowo
        if self.site_connection().btn1.text != "" and self.site_connection().btn1.text == self.site_connection().btn4.text and self.site_connection().btn4.text == self.site_connection().btn7.text:
            self.end_game(self.site_connection().btn1, self.site_connection().btn4, self.site_connection().btn7)

        if self.site_connection().btn2.text != "" and self.site_connection().btn2.text == self.site_connection().btn5.text and self.site_connection().btn5.text == self.site_connection().btn8.text:
            self.end_game(self.site_connection().btn2, self.site_connection().btn5, self.site_connection().btn8)
            
        if self.site_connection().btn3.text != "" and self.site_connection().btn3.text == self.site_connection().btn6.text and self.site_connection().btn6.text == self.site_connection().btn9.text:
            self.end_game(self.site_connection().btn3, self.site_connection().btn6, self.site_connection().btn9)

        # Po skosie
        if self.site_connection().btn1.text != "" and self.site_connection().btn1.text == self.site_connection().btn5.text and self.site_connection().btn5.text == self.site_connection().btn9.text:
            self.end_game(self.site_connection().btn1, self.site_connection().btn5, self.site_connection().btn9)

        if self.site_connection().btn3.text != "" and self.site_connection().btn3.text == self.site_connection().btn5.text and self.site_connection().btn5.text == self.site_connection().btn7.text:
            self.end_game(self.site_connection().btn3, self.site_connection().btn5, self.site_connection().btn7)
        
        self.tie()

    def tie(self):
        '''#*Metoda sprawdza czy i wykonuje akcje związane z remisem'''
        if not self.winner and self.site_connection().btn1.text != ""\
        and self.site_connection().btn2.text != ""\
        and self.site_connection().btn3.text != ""\
        and self.site_connection().btn4.text != ""\
        and self.site_connection().btn5.text != ""\
        and self.site_connection().btn6.text != ""\
        and self.site_connection().btn7.text != ""\
        and self.site_connection().btn8.text != ""\
        and self.site_connection().btn9.text != ""    :
            self.site_connection().score.text = "IT'S A TIE!!!"
            self.tie_q = True
            
            insert_query="insert into wyniki (id_meczu, wynik) values(null, 2)"

            self.my_cursor.execute(insert_query)
            self.data_base.commit()

    def end_game(self, a, b, c):
        '''#*Metoda kończąca grę, przyjmuje jako argumenty 3 przyciski które są w wygranym rzędzie'''
        self.winner = True
        a.color = "red"
        b.color = "red"
        c.color = "red"

        self.all_buttons("disablbed", True)
        self.site_connection().score.text = f"{a.text} Wins"

        if a.text=="X":
            db_winner= 1
        else:
            db_winner= 0

        insert_query=f"insert into wyniki (id_meczu, wynik) values(null, {db_winner})"
        self.my_cursor.execute(insert_query)
        self.data_base.commit()

        self.stats_1()
        self.stats_2()

    def on_press(self, btn, btn_s):
        '''#*Metoda wywoływana klknięciem w przycisk, przyjmuje jako argumenty id klikniętego przycisku'''
        if not self.is_bot:
            if self.turn =="X":
                btn.text = "X"
                btn.disabled = True
                self.site_connection().score.text = "O's Turn!"
                self.turn = "O"
            else:
                btn.text = "O"
                btn.disabled = True
                self.site_connection().score.text = "X's Turn!"
                self.turn = "X"
        else:
            if self.turn =="X" and self.turn == self.player_symbol:
                AI.Data().data(btn_s, "X")

                btn.text = "X"
                btn.disabled = True
                self.site_connection().score.text = "O's Turn!"
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
                self.site_connection().score.text = "X's Turn!"
                self.turn = "X"

        self.check_winner()
        self.root.md_bg_color= 0,0,0,1
        if self.turn !=self.player_symbol and not self.winner and not self.tie_q and self.is_bot:
            self.on_press("","")

    def press_by_ai(self, btn):
        '''#*Metoda wciska przycisk wybrany przez AI'''
        self.site_connection()["btn"+str(btn)].text = self.ai_symbol
        self.site_connection()["btn"+str(btn)].disabled = True

    def all_buttons(self, action, value):
        '''#*Metoda zmienia podną właściwość dla wszystkich przycisków'''
        if action == "disabled":
            for i in range(1,10):
                btn = "btn"+str(i)
                self.site_connection()[btn].disabled = value
        if action == "color":
            for i in range(1,10):
                btn = "btn"+str(i)
                self.site_connection()[btn].color = value
        if action == "text":
            for i in range(1,10):
                btn = "btn"+str(i)
                self.site_connection()[btn].text = value

    def restart(self):
        '''#*Metoda wykonuje wszystkie akcje związane z resetoowaniem gry'''
        AI.Data().restart()
        self.turn = "X"

        self.all_buttons("disabled", False)
        self.all_buttons("text", "")
        self.all_buttons("color", "gray")

        self.site_connection().score.text = "X GOES FIRST!"

        self.winner = False
        self.tie_q = False

        if self.is_bot and self.ai_symbol == "X":
            self.on_press("", "")

if __name__=="__main__":
    Code().run()
