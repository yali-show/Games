import sys
import random
# to use PILL have had to install package Pillow
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW



config_game = {
    'BOARD_WIDTH': 864,
    'BOARD_HEIGHT': 864,
    'DELAY': 300,
    'DOT_SIZE': 10,
    'MAX_RAND_POS': 27,
    'SPEED_CHANGE': 10,
    'HANDLE_AFTER': '',
    'FONT_COLORS' : 'white',
}


snake_config = {
    'dots':  0,
    'moveX': 0,
    'moveY': 0
}

game_status = {
    'in_game': False,
    'score': 0,
    'score_remember_state': 0,
    'speed': 10
}

apple_config = {
    'appleX': 100,
    'appleY': 190
}

images = {
    'dot': "",
    'head': "",
    'apple': ""
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

    game_status['in_game'] = True
    game_status['score'] = 0
    snake_config['dots'] = 3

    # Змінні для руху змії
    snake_config['moveX'] = config_game['DOT_SIZE']
    snake_config['moveY'] = 0

    # Початкові координати яблука
    apple_config['appleX'] = 100
    apple_config['appleY'] = 190

    load_images()

    create_objects(board)
    locate_apple(board)
    board.bind_all("<Key>", on_key_pressed)

    # перший запуск таймера для перемалювання обьєктів

    config_game['HANDLE_AFTER'] = root.after(config_game['DELAY'], on_timer)

    board.pack()
    m_frame.pack()




def load_images():
    """
    Заргузка зображень які формують змію та яблука
    """

    try:
        idot = Image.open("dot1.png")
        images['dot'] = ImageTk.PhotoImage(idot)
        ihead = Image.open("snakes_head.png")
        images['head'] = ImageTk.PhotoImage(ihead)
        iapple = Image.open("apple.png")
        images['apple'] = ImageTk.PhotoImage(iapple)

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
    canvas_obj.create_text(
            250, 10, text="Speed: {0}".format(game_status['speed']),
            tag="speed", fill="black"
    )
    # створити яблуко
    canvas_obj.create_image(
            apple_config['appleX'], apple_config['appleY'],
            image=images['apple'],
            anchor=NW, tag="apple"
    )

    # змій - голова та 2 секції
    canvas_obj.create_image(50, 50, image=images['head'], anchor=NW, tag="head")
    canvas_obj.create_image(30, 50, image=images['dot'],  anchor=NW, tag="dot")
    canvas_obj.create_image(40, 50, image=images['dot'],  anchor=NW, tag="dot")


def locate_apple(canvas_obj):
    """
    Розташування яблук по полотну (canvas).
    """

    apple = canvas_obj.find_withtag("apple")
    canvas_obj.delete(apple[0])

    r = random.randint(0, config_game['MAX_RAND_POS'])
    apple_config['appleX'] = r * config_game['DOT_SIZE']
    r = random.randint(0, config_game['MAX_RAND_POS'])
    apple_config['appleY'] = r * config_game['DOT_SIZE']

    canvas_obj.create_image(
            apple_config['appleX'], apple_config['appleY'], 
            anchor=NW, image=images['apple'], tag="apple"
    )



def on_key_pressed(event):
    """
    Управління змійкою через стрілки на клавіатурі 
    """

    key = event.keysym
    LEFT_CURSOR_KEY = "Left"
    if key == LEFT_CURSOR_KEY and snake_config['moveX'] <= 0:
        snake_config['moveX'] = -config_game['DOT_SIZE']
        snake_config['moveY'] = 0

    RIGHT_CURSOR_KEY = "Right"
    if key == RIGHT_CURSOR_KEY and snake_config['moveX'] >= 0:
        snake_config['moveX'] = config_game['DOT_SIZE']
        snake_config['moveY'] = 0

    UP_CURSOR_KEY = "Up"
    if key == UP_CURSOR_KEY and snake_config['moveY'] <= 0:
        snake_config['moveX'] = 0
        snake_config['moveY'] = -config_game['DOT_SIZE']

    DOWN_CURSOR_KEY = "Down"
    if key == DOWN_CURSOR_KEY and snake_config['moveY'] >= 0:
        snake_config['moveX'] = 0
        snake_config['moveY'] = config_game['DOT_SIZE']

    PAUSE_CURSOR_KEY = "space"
    if key == PAUSE_CURSOR_KEY:
        if config_game['HANDLE_AFTER'] == '':
            on_timer()
        else:
            root.after_cancel(config_game['HANDLE_AFTER'])
            config_game['HANDLE_AFTER'] = ''




def draw_score_speed(canvas_obj):
    """
    Відображення рахунку гри
    """

    score = canvas_obj.find_withtag("score")
    speed = canvas_obj.find_withtag("speed")
    canvas_obj.itemconfigure(score, text="Score: {0}".format(game_status['score']))
    canvas_obj.itemconfigure(speed, text="Speed: {0}".format(game_status['speed']))


def check_crash(canvas_obj):
    """
    Перевірка на зіткнення з іншими обьєктами
    """

    dots = canvas_obj.find_withtag("dot")
    head = canvas_obj.find_withtag("head")

    x1, y1, x2, y2 = canvas_obj.bbox(head)
    overlap = canvas_obj.find_overlapping(x1, y1, x2, y2)

    for dot in dots:
        for over in overlap:
            if over == dot:
                game_status['in_game'] = False

        if x1 < 0:
            game_status['in_game'] = False

        if x1 > config_game['BOARD_WIDTH'] - config_game['DOT_SIZE']:
            game_status['in_game'] = False

        if y1 < 0:
            game_status['in_game'] = False

        if y1 > config_game['BOARD_HEIGHT']  - config_game['DOT_SIZE']:
            game_status['in_game'] = False


def check_apple_touch(canvas_obj):
    """
    Перевірка на е що не стовкнулась голова змія з яблуком 
    """
    # отримуємо об'єкт за тегом
    apple = canvas_obj.find_withtag("apple")
    head =  canvas_obj.find_withtag("head")
    x1, y1, x2, y2 = canvas_obj.bbox(head)
    overlap = canvas_obj.find_overlapping(x1, y1, x2, y2)

    for ovr in overlap:
        if apple[0] == ovr:
            game_status['score'] += 1
            x, y = canvas_obj.coords(apple)
            canvas_obj.create_image(x, y, image=images['dot'], anchor=NW, tag="dot")
            locate_apple(canvas_obj)


def move_snake(canvas_obj):
    """
    Рух змія по полотну
    """

    dots = canvas_obj.find_withtag("dot")
    head = canvas_obj.find_withtag("head")

    items = dots + head
    n = 0
    while n < len(items)-1:
        # отримати координати оброблємого об'єкту  
        c1 = canvas_obj.coords(items[n])
        
        # отримати координати наступного об'єкту+
        c2 = canvas_obj.coords(items[n+1])
        
        canvas_obj.move(items[n], c2[0]-c1[0], c2[1]-c1[1])
        n += 1

    canvas_obj.move(head, snake_config['moveX'], snake_config['moveY'])


def game_over():
    global board
    """
    Видалити усі обьєкти з поля і сповістити про кінець гри
    """

    board.delete(ALL)
    board.create_text(board.winfo_width() / 2, board.winfo_height()/2,
            text="GAME OVER \nYour score: {0}".format(game_status['score']),
            fill="black"
    )

def speed_background_change():

    if game_status['score'] % 2 == 0:
        if game_status['score_remember_state'] !=  game_status['score']:
            game_status['score_remember_state'] = game_status['score']
            game_status['speed'] += 10
            config_game['DELAY'] -= config_game['SPEED_CHANGE']
            
            while True:
                color = random.choice(['green', 'cyan', 'white', 'pink', 'yellow', 'orange'])
                if config_game['FONT_COLORS'] != color:
                    break
            config_game['FONT_COLORS'] = color
            board.configure(background=color)





def on_timer():
    global board, root
    """
    Створює ігровий цикл подій 
    """

    draw_score_speed(board)
    check_crash(board)

    if game_status['in_game']:
        check_apple_touch(board)
        move_snake(board)
        config_game['HANDLE_AFTER'] = root.after(config_game['DELAY'], on_timer)
        speed_background_change()
    else:
        game_over()


def main():
    global root , board 
    root = Tk()
    init_game(root)

    ico = Image.open('snake_icon.png')
    photo = ImageTk.PhotoImage(ico)
    root.wm_iconphoto(False, photo)
    root.mainloop()


if __name__ == '__main__':
    main()
