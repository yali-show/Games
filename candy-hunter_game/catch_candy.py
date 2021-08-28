import sys
import random
# to use PILL have had to install package Pillow
import tkinter

from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW
root = tkinter.Tk
screen_width = root.winfo_screenwidth()

config_game = {
    'BOARD_WIDTH': screen_width,
    'BOARD_HEIGHT': screen_width,
    'DELAY': 300,
    'CANDY_SIZE': 10,
    'MAX_RAND_POS': 27,
    'HANDLE_AFTER': '',
    'FONT_COLORS' : 'white',
}
game_status = {
    'score': 0,
}
candy_config = {
    'candyX' : '',
    'candyY' : ''
}

images = {
    'candy' : ""
}

def init_game(root):
    """
    Ініціалізація гри.
    """
    global board

    m_frame = Frame(root)
    board = Canvas(m_frame,
        width=config_game['BOARD_WIDTH'],
        height=config_game['BOARD_HEIGHT'],
        background=config_game['FONT_COLORS'],
        highlightthickness=0
    )

    m_frame.master.title('Python')
    game_status['score'] = 0

    load_images()

    create_objects(board)

    config_game['HANDLE_AFTER'] = root.after(config_game['DELAY'], on_timer)

    board.pack()
    m_frame.pack()

def load_images():
        """
        Заргузка зображень які формують змію та яблука
        """

    try:
        icandy = Image.open("candy.jpg")
        images['candy'] = ImageTk.PhotoImage(icandy)

    except IOError as e:
        print(e)
        sys.exit(1)

def create_objects(canvas_obj):
    """
    Створити обьєкти на полотні
    """
    #  текс для score
    canvas_obj.create_text(
        40, 10, text="Score: {0}".format(game_status['score']),
        tag="score", fill="black"
    )
    canvas_obj.create_image(
        candy_config['candyX'], candy_config['candyY'],
        image=images['candy'],
        anchor=NW, tag="candy"
    )

def locate_candy(canvas_obj):
    candy = canvas_obj.find_withtag("candy")
    canvas_obj.delete(candy[0])
    r = random.randint(0, config_game['MAX_RAND_POS'])
    candy_config['candyX'] = r * config_game['DOT_SIZE']
    r = random.randint(0, config_game['MAX_RAND_POS'])
    candy_config['candyY'] = r * config_game['DOT_SIZE']

    canvas_obj.create_image(
        apple_config['appleX'], apple_config['appleY'],
        anchor=NW, image=images['apple'], tag="apple"
    )