import tkinter as tk
from tkinter import ALL
import random
from config import config_game
global oval_coords, message_text, frog_text, start_text
COORDS = oval_coords
root = tk.Tk()
m_frame = tk.Frame(root)

board = tk.Canvas(
    root,
    width=config_game['BOARD_SIZE'],
    height=config_game['BOARD_SIZE'] - 100,
    bg='black'
)

exit_on_canvas = False



def start_game():
    global oval_coords, message_text, frog_text, start_text
    m_frame.master.title('🐸игрушка - лягушка🐸')
    oval_coords = board.create_oval(
        5, 5, 75, 75,
        fill="green"
    )

    message_text = board.create_text(
        250, 370,
        font=('Purisa', 18),
        text='СОБИРАЙ ТОЛЬКО ЗОЛОТЫЕ МОНЕТЫ!!!',
        fill="red"
    )

    frog_text = board.create_text(
        250, 30,
        font=('Purisa', 18),
        text='Игра про жабу🐸',
        fill="green"
    )

    start_text = board.create_text(
        250, 200,
        font=('Purisa', 18),
        text='**ЧТОБ НАЧАТЬ НАЖМИТЕ НА СТРЕЛКУ**',
        fill="green")
    board.bind_all("<Key>", on_key_pressed)


def on_key_pressed(event):
    key = event.keysym
    LEFT_CURSOR_KEY = "Left"

    if key == LEFT_CURSOR_KEY:
        board.delete(frog_text, message_text, start_text)
        new_coords = []
        #
        # for cords in COORDS:
        #     if COORDS[]
        # board.coords(oval_coords, new_coords)

    '''
    RIGHT_CURSOR_KEY = "Right"
    if key == RIGHT_CURSOR_KEY and snake_config['moveX'] >= 0:
        snake_config['moveX'] = config_game['DOT_SIZE']
        snake_config['moveY'] = 0

    RIGHT_CURSOR_KEY = "Up",
    if key == UP_CURSOR_KEY :
        snake_config['moveX'] = 0
        snake_config['moveY'] = -config_game['DOT_SIZE']

    DOWN_CURSOR_KEY = "Down",
    if key == DOWN_CURSOR_KEY:
        snake_config['moveX'] = 0
        snake_config['moveY'] = config_game['DOT_SIZE']

'''


def init_prank():
    m_frame.master.title('😈пранк😈')
    global exit_button
    if exit_on_canvas == True:
        exit_button.destroy()
    yes_button = tk.Button(text='Да', width=20, height=3)
    no_button = tk.Button(text='Cам', width=20, height=3)
    board.delete(ALL)

    def yes_button_pressed():
        global exit_button
        yes_button.destroy()
        no_button.destroy()
        board.delete(ALL)

        board.create_text(
            250, 150,
            font=('Purisa', 20),
            text='ТЫ ПРИЗНАЛ ЭТО\n🤣🤣🤣🤣🤣🤣🤣\n   ТЫ ДУРАЧЕК\n🤣🤣🤣🤣🤣🤣🤣',
            fill="white"
        )
        exit_button = tk.Button(text='Отмена', width=20, height=3)
        exit_button.place(x=170, y=300)
        exit_button.config(command=exit_button_event)

    def no_button_def():
        random_num_1 = random.randint(1, 300)
        random_num_2 = random.randint(1, 300)
        no_button.place(x=random_num_1, y=random_num_2)

    yes_button.config(command=yes_button_pressed)
    yes_button.place(x=50, y=300)
    no_button.config(command=no_button_def)
    no_button.place(x=300, y=300)

    text = board.create_text(
        250, 150,
        font=('Purisa', 20),
        text='Ты дурак?',
        fill="white",

    )


def exit_button_event():
    exit_button.config(text='Вернуться в начало', command=return_button_event)
    board.delete(ALL)

    board.create_text(
        250, 150,
        font=('Purisa', 20),
        text='что ты хочешь этим добиться?\nслово - не воробей,\nвылетит не споймаешь',
        fill="white"
    )


def return_button_event():
    global exit_on_canvas
    board.delete(ALL)
    exit_button.config(text='Да', command=init_prank)
    board.create_text(
        250, 150,
        font=('Purisa', 20),
        text='чел...\nты серьезно хочешь вернуться?',
        fill="white"
    )
    exit_on_canvas = True


board.pack()
start_game()
# init_prank()
root.mainloop()
