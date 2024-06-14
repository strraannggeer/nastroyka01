import tkinter as tk
from tkinter import messagebox
import pyttsx3
import random
from PIL import Image, ImageTk, ImageSequence

# Настройка синтеза речи
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Скорость речи
voices = engine.getProperty('voices')
# Найдем голос с русской локализацией
for voice in voices:
    if "russian" in voice.languages:
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('volume', 1.0)  # Громкость на максимум


def speak(text, callback=None):
    engine.say(text)
    engine.runAndWait()
    if callback:
        callback()


def check_winner(board, player):
    for row in board:
        if all(s == player for s in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


def is_draw(board):
    return all(all(cell != " " for cell in row) for row in board)


def get_random_joke():
    jokes = [
        "Ходите аккуратно, а то клетка не выдержит!",
        "Думаете, это правильный ход? Посмотрим!",
        "Интересный выбор! Посмотрим, что из этого выйдет!",
        "Вот это поворот! Кто бы мог подумать!",
        "Эта клетка точно выдержит ваш ход?"
    ]
    return random.choice(jokes)


def on_click(row, col):
    global current_player, game_running
    if not game_running:
        return
    if board[row][col] == " ":
        board[row][col] = current_player
        buttons[row][col].config(image=orc_gif if current_player == "X" else archer_gif, state=tk.DISABLED)
        buttons[row][col].image = orc_gif if current_player == "X" else archer_gif  # Сохраняем ссылку на изображение

        if check_winner(board, current_player):
            game_running = False
            winner = 'орк' if current_player == 'X' else 'лучник'
            root.after(100, lambda: speak(f"Игрок {winner} победил! Отличная работа, {winner}!",
                                          lambda: messagebox.showinfo("Игра окончена", f"Игрок {winner} победил!")))
        elif is_draw(board):
            game_running = False
            root.after(100, lambda: speak("Ничья! Это была жестокая битва, и никто не вышел победителем.",
                                          lambda: messagebox.showinfo("Игра окончена", "Ничья!")))
        else:
            current_player = "O" if current_player == "X" else "X"
            update_turn_label()
            root.after(100, lambda: speak(f"{get_random_joke()} Сейчас ходит {'Орк' if current_player == 'X' else 'Лучник'}.", lambda: None))
    else:
        speak("Эта ячейка уже занята. Попробуйте снова.")


def start_game():
    global board, current_player, game_running
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    game_running = True
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(state=tk.NORMAL, bg="#3b3b3b", image='', text=' ')
    update_turn_label()
    speak("Начнем игру. Сейчас ходит орк. Пусть победит сильнейший!")


def stop_game():
    global game_running
    game_running = False
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(state=tk.DISABLED)
    speak("Игра остановлена. Кто-то испугался?")


def update_turn_label():
    turn_label.config(text="Сейчас ходит: ", fg="white")
    turn_label_value.config(text=f"{'Орк' if current_player == 'X' else 'Лучник'}",
                            fg="green" if current_player == "X" else "red")


def create_gui():
    global root, buttons, board, current_player, game_running, turn_label, turn_label_value, orc_gif, archer_gif, orc_frames, archer_frames
    root = tk.Tk()
    root.title("Крестики-нолики")
    root.configure(bg="#000000")  # Черный фон для атмосферы

    # Загрузка изображений
    orc_img = Image.open("orc.gif")
    archer_img = Image.open("archer.gif")

    # Установка размера кнопок
    button_size = (100, 100)  # Размер кнопок

    orc_frames = [ImageTk.PhotoImage(frame.resize(button_size, Image.Resampling.LANCZOS)) for frame in ImageSequence.Iterator(orc_img)]
    archer_frames = [ImageTk.PhotoImage(frame.resize(button_size, Image.Resampling.LANCZOS)) for frame in ImageSequence.Iterator(archer_img)]

    orc_gif = orc_frames[0]
    archer_gif = archer_frames[0]

    buttons = []
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    game_running = False

    # Шрифты в стиле Warcraft II
    font_style = ("Times New Roman", 18, "bold")
    button_font_style = ("Times New Roman", 24, "bold")

    turn_label = tk.Label(root, text="Сейчас ходит: ", font=font_style, fg="white", bg="#000000")
    turn_label.grid(row=0, column=0, columnspan=2, sticky="e")
    turn_label_value = tk.Label(root, text="Орк", font=font_style, fg="green", bg="#000000")
    turn_label_value.grid(row=0, column=2, sticky="w")

    for row in range(3):
        button_row = []
        for col in range(3):
            button = tk.Button(root, text=" ", font=button_font_style, width=5, height=2, bg="#3b3b3b",
                               command=lambda r=row, c=col: on_click(r, c))
            button.grid(row=row + 1, column=col, padx=5, pady=5)
            button_row.append(button)
        buttons.append(button_row)

    start_button = tk.Button(root, text="Старт", font=font_style, command=start_game, bg="#006400", fg="#FFD700")
    start_button.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=5)

    stop_button = tk.Button(root, text="Стоп", font=font_style, command=stop_game, bg="#8B0000", fg="#FFD700")
    stop_button.grid(row=5, column=0, columnspan=3, sticky="nsew", pady=5)

    root.after(500, lambda: speak(
        "Добро пожаловать в игру Крестики-нолики! Нажмите 'Старт', чтобы начать игру. Приготовьтесь к битве века!"))

    root.mainloop()


def animate(label, frames, delay=100):
    def update(frame_index):
        frame = frames[frame_index]
        frame_index = (frame_index + 1) % len(frames)
        label.config(image=frame)
        label.image = frame
        root.after(delay, update, frame_index)

    update(0)


if __name__ == "__main__":
    create_gui()
