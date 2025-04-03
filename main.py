from tkinter import *
import random
import time

# Colors and Styling
BG_COLOR = "#2C3E50"
FG_COLOR = "#ECF0F1"
BTN_COLOR = "#3498DB"
BTN_HOVER = "#2980B9"
WIN_COLOR = "#2ECC71"
TIE_COLOR = "#F1C40F"
FONT = ('consolas', 40, 'bold')


# Game Logic

def next_turn(row=None, column=None):
    global player
    if player == "X" and row is not None and column is not None:
        if buttons[row][column]['text'] == "" and check_winner() is False:
            buttons[row][column]['text'] = player
            buttons[row][column].config(bg=BTN_HOVER)
            if check_winner() is False:
                player = "O"
                label.config(text=(player + " turn"))
                window.after(500, ai_move)
            else:
                label.config(text=(check_winner() + " wins!"))


def ai_move():
    if check_winner() is False:
        move = best_move()
        if move:
            row, column = move
            buttons[row][column]['text'] = "O"
            buttons[row][column].config(bg=BTN_HOVER)
            if check_winner() is False:
                global player
                player = "X"
                label.config(text=(player + " turn"))
            else:
                label.config(text=(check_winner() + " wins!"))


# AI Move Selection

def best_move():
    best_score = -float("inf")
    move = None
    for row in range(3):
        for col in range(3):
            if buttons[row][col]['text'] == "":
                buttons[row][col]['text'] = "O"
                score = evaluate_board()
                buttons[row][col]['text'] = ""
                if score > best_score:
                    best_score = score
                    move = (row, col)
    return move


def evaluate_board():
    if check_winner() == "O":
        return 10
    elif check_winner() == "X":
        return -10
    return 0


# Check Winner Function

def check_winner():
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != "":
            for i in range(3):
                buttons[row][i].config(bg=WIN_COLOR)
            return buttons[row][0]['text']

    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != "":
            for i in range(3):
                buttons[i][column].config(bg=WIN_COLOR)
            return buttons[0][column]['text']

    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        for i in range(3):
            buttons[i][i].config(bg=WIN_COLOR)
        return buttons[0][0]['text']

    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        buttons[0][2].config(bg=WIN_COLOR)
        buttons[1][1].config(bg=WIN_COLOR)
        buttons[2][0].config(bg=WIN_COLOR)
        return buttons[0][2]['text']

    if empty_spaces() is False:
        for row in range(3):
            for column in range(3):
                buttons[row][column].config(bg=TIE_COLOR)
        return "Tie"

    return False


def empty_spaces():
    return any(buttons[row][column]['text'] == "" for row in range(3) for column in range(3))


def new_game():
    global player
    player = "X"
    label.config(text=player + " turn")
    for row in range(3):
        for column in range(3):
            buttons[row][column].config(text="", bg=BTN_COLOR)


def on_enter(e):
    e.widget.config(bg=BTN_HOVER)


def on_leave(e):
    if e.widget['text'] == "":
        e.widget.config(bg=BTN_COLOR)


# UI Setup
window = Tk()
window.title("Tic-Tac-Toe")
window.configure(bg=BG_COLOR)

player = "X"  # Player always starts
buttons = [[None] * 3 for _ in range(3)]

label = Label(window, text=player + " turn", font=('consolas', 30), bg=BG_COLOR, fg=FG_COLOR)
label.pack(pady=10)

reset_button = Button(window, text="Restart", font=('consolas', 20), bg=BTN_COLOR, fg=FG_COLOR, command=new_game)
reset_button.pack(pady=10)

frame = Frame(window, bg=BG_COLOR)
frame.pack()

for row in range(3):
    for column in range(3):
        buttons[row][column] = Button(frame, text="", font=FONT, width=5, height=2, bg=BTN_COLOR, fg=FG_COLOR,
                                      command=lambda row=row, column=column: next_turn(row, column))
        buttons[row][column].grid(row=row, column=column, padx=5, pady=5)
        buttons[row][column].bind("<Enter>", on_enter)
        buttons[row][column].bind("<Leave>", on_leave)

window.mainloop()
