import tkinter as tk
from tkinter import messagebox
import random


#создание окна
root = tk.Tk()
root.title("Сапер")
root.geometry("600x600")
var = tk.IntVar()
var.set(1)


#создаем интерфейс
count_mine = 10
label_mine = tk.Label(root, text=f'Осталось мин: {count_mine}', font=("Arial", 20))
label_mine.grid(row=0, column=0, columnspan=5, sticky="nsew")

### ИЗМЕНЕНО: флаг первого клика и пустое поле
first_click = True
board = [[0 for _ in range(10)] for _ in range(10)]


#создаем игровое поле
def create_board(first_r, first_c):
    board = [[0 for i in range(10)] for i in range(10)]
    mines = 10

    coo_first = set()
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            r, c = first_r + dr, first_c + dc
            if 0 <= r < 10 and 0 <= c < 10:
                coo_first.add((r, c))

    count = 0
    while count != mines:
        coord1 = random.randint(0, 9)
        coord2 = random.randint(0, 9)
        if (coord1, coord2) in coo_first:
            continue
        if board[coord1][coord2] != -1:
            board[coord1][coord2] = -1
            count += 1

    #рассчитываем числа вокруг мин
    for row in range(10):
        for col in range(10):
            if board[row][col] != -1:
                cnt = 0
                for r in range(row-1, row+2):
                    for c in range(col-1, col+2):
                        if (0 <= r < 10 and 0 <= c < 10):
                            if board[r][c] == -1:
                                cnt += 1
                board[row][col] = cnt
    return board


#создаем кнопки
buttons = [[None for i in range(10)]for i in range(10)]


for i in range(12):
    root.rowconfigure(i, weight=1, uniform="row")
    
for j in range(10):
    root.columnconfigure(j, weight=1, uniform="column")


for i in range(2, 12):
    for j in range(0, 10):
        new_game_btn = tk.Button(root, bg="lightgrey", font=("Arial", 20),
                                 state=tk.NORMAL, command=lambda r=i-2, c=j: left_click(r, c))
        new_game_btn.grid(row=i, column=j, sticky='nsew', padx=1, pady=1)
        new_game_btn.bind("<Button-3>", lambda e, r=i-2, c=j: right_click(e, r, c)) 
        buttons[i-2][j] = new_game_btn



#создаем обработку кликов
def open_empty_cells(row, col): #открываем соседние пустые клетки
    buttons[row][col].config(state=tk.DISABLED, text="", bg="white")
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 10 and 0 <= nc < 10:
                if buttons[nr][nc]['state'] == tk.NORMAL:
                    val = board[nr][nc]
                    if val == 0:
                        open_empty_cells(nr, nc)
                    elif val > 0:
                        buttons[nr][nc].config(text=str(val), state=tk.DISABLED)


def left_click(row, col): #открываем ячейку
    global first_click, board

    if first_click:
        board = create_board(row, col)
        first_click = False

    value = board[row][col]
    if value == -1:
        messagebox.showinfo("Game Over", "Вы наступили на мину!")
        return
    elif value == 0:
        open_empty_cells(row, col)
    else:
        buttons[row][col].config(text=str(value), state=tk.DISABLED)
        check_win()



def right_click(event, row, col): #ставим флаг где мина
    global count_mine
    current_text = buttons[row][col].cget("text")
    if current_text == "":
        buttons[row][col].config(text="F")
        count_mine -= 1
        check_win()
    elif current_text == "F":
        buttons[row][col].config(text="")
        count_mine += 1
    label_mine.config(text=f'Осталось мин: {count_mine}')



#проверка на победу
def check_win ():
    for row in range(10):
        for col in range(10):
            if board[row][col] == -1:
                if buttons[row][col].cget('text') != 'F':
                    return False
            else:
                if buttons[row][col]["state"] != tk.DISABLED:
                    return False
    messagebox.showinfo("WIN", "ВЫ ПОБЕДИЛИ!")
    return True


# кнопка новой игры
def new_game():
    global board, count_mine, first_click
    first_click = True
    board = [[0 for _ in range(10)] for _ in range(10)]
    count_mine = 10
    label_mine.config(text=f'Осталось мин: {count_mine}')
    for r in range(10):
        for c in range(10):
            buttons[r][c].config(text="", state=tk.NORMAL, bg="lightgrey")


button_game = tk.Button(root, bg="yellow", font=("Arial", 20), text="NEW GAME", state=tk.NORMAL, command=new_game)
button_game.grid(row=0, column=5, columnspan=5,)


root.mainloop()
