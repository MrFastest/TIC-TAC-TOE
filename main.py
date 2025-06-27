from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
import random

class TicTacToeGame(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.rows = 3
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.hard_mode = True  
        self.show_difficulty_popup()

    def show_difficulty_popup(self):
        self.reset_board()  # Reset the board before showing the popup
        popup_layout = BoxLayout(orientation='vertical')
        popup_label = Label(text="Choose Difficulty Level", font_size=24)
        normal_button = Button(text="Normal", size_hint=(1, 0.3))
        hard_button = Button(text="Hard", size_hint=(1, 0.3))

        popup = Popup(title="Select Difficulty", content=popup_layout, size_hint=(0.6, 0.4), auto_dismiss=False)
        normal_button.bind(on_press=lambda instance: self.set_difficulty(False, popup))
        hard_button.bind(on_press=lambda instance: self.set_difficulty(True, popup))

        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(normal_button)
        popup_layout.add_widget(hard_button)
        popup.open()

    def set_difficulty(self, hard, popup):
        self.hard_mode = hard
        popup.dismiss()
        self.create_board()

    def create_board(self):
        self.clear_widgets()
        for row in range(3):
            for col in range(3):
                btn = Button(font_size=32, on_press=self.make_move)
                self.add_widget(btn)
                self.buttons[row][col] = btn

    def make_move(self, btn):
        if btn.text == "" and self.current_player == "X":
            for row in range(3):
                for col in range(3):
                    if self.buttons[row][col] == btn:
                        self.board[row][col] = "X"
                        btn.text = "X"
                        if self.check_winner("X"):
                            self.show_result("User (X) wins!")
                            return
                        self.current_player = "O"
                        self.computer_move()
                        return

    def computer_move(self):
        if self.hard_mode:
            best_score = float('-inf')
            best_move = None
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == "":
                        self.board[row][col] = "O"
                        score = self.minimax(self.board, 0, False)
                        self.board[row][col] = ""
                        if score > best_score:
                            best_score = score
                            best_move = (row, col)
            if best_move:
                row, col = best_move
                self.board[row][col] = "O"
                self.buttons[row][col].text = "O"
        else:
            empty_cells = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == ""]
            if empty_cells:
                row, col = random.choice(empty_cells)
                self.board[row][col] = "O"
                self.buttons[row][col].text = "O"

        if self.check_winner("O"):
            self.show_result("Computer (O) wins!")
            return
        if self.is_draw():
            self.show_result("It's a draw!")
            return
        self.current_player = "X"

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner("O"):
            return 1
        if self.check_winner("X"):
            return -1
        if not any("" in row for row in board):
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == "":
                        board[row][col] = "O"
                        score = self.minimax(board, depth + 1, False)
                        board[row][col] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == "":
                        board[row][col] = "X"
                        score = self.minimax(board, depth + 1, True)
                        board[row][col] = ""
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        for row in range(3):
            if all(self.board[row][col] == player for col in range(3)):
                return True
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def is_draw(self):
        return all(self.board[row][col] != "" for row in range(3) for col in range(3))

    def show_result(self, message):
        popup_layout = BoxLayout(orientation='vertical')
        popup_label = Label(text=message, font_size=24)
        close_button = Button(text="Restart", size_hint=(1, 0.3))
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)
        popup = Popup(title="Game Over", content=popup_layout, size_hint=(0.5, 0.5), auto_dismiss=False)
        close_button.bind(on_press=lambda instance: (popup.dismiss(), self.show_difficulty_popup()))
        popup.open()

    def reset_board(self):
        for row in range(3):
            for col in range(3):
                self.board[row][col] = ""
                if self.buttons[row][col]:
                    self.buttons[row][col].text = ""
        self.current_player = "X"

class TicTacToeApp(App):
    def build(self):
        return TicTacToeGame()

if __name__ == "__main__":
    TicTacToeApp().run()
