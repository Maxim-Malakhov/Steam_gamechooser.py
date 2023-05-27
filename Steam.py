from tkinter import *
from tkinter import font
from bs4 import BeautifulSoup
import requests
import webbrowser
from io import BytesIO
from PIL import Image, ImageTk
import random

genres_tags = {
    "Гонки": '699',
    "Инди": '492',
    "Казуальная игра": '597',
    "ММО": '128',
    "Приключение": '21',
    "Ролевая игра": '122',
    "Симулятор": '599',
    "Спортивная игра": '701',
    "Стратегия": '9',
    "Экшен": '19'
}

genre = "Выберите жанр"

def search():
    global game_name_label, game_link_label
    
    if genre != "Выберите жанр":
        parsing()

        game_name_label['text'] = game_name
        game_link_label['text'] = f'{game_link[:(list(game_link)).index(game_name[0])]}...'
        game_link_label['fg'] = 'blue'
        game_img_label['image'] = game_img

def parsing():
    global game_name, game_link, game_img_link, game_img
    response = requests.get('https://store.steampowered.com/search/?maxprice=free&supportedlang=russian&tags={}&ndl=1'.format(genres_tags.get(genre)))
    html = BeautifulSoup(response.content, 'html.parser')
    game = random.choice(html.find_all('a', attrs = {'data-gpnav' : "item"}))
    game_name = game.find(class_ = 'title').text
    game_link = game.attrs['href']
    game_img_link = requests.get(game.find('img').attrs['src'])
    game_img = ImageTk.PhotoImage(Image.open(BytesIO(game_img_link.content)).resize((480, 180), Image.Resampling.LANCZOS))

def callback(*args):
    global genre
    genre = variable.get()

def click_link(event):
    webbrowser.open_new(game_link)
    game_link_label['fg'] = '#551a8b'

def paint_option(option_color):
    option.config(bg = option_color, activebackground = option_color)

def paint_link():
    global link_font
    link_font.config(underline = True)
    game_link_label.config(font = link_font)

def unpaint_link():
    global link_font
    link_font.config(underline = False)
    game_link_label.config(font = link_font)

window = Tk()

window.title('Выбор игры')
window.geometry('482x300')
window['bg'] = 'white'

variable = StringVar(window)
variable.set("Выберите жанр")
variable.trace("w", callback)

option = OptionMenu(window, variable, *list(genres_tags))
option.config(font = ('Terminal', 12))
for item in range(0, int(option['menu'].index('end'))+1):
    option['menu'].entryconfig(item, font = ('Terminal', 12))
option.pack(fill = X, side = TOP)
paint_option('#ff9966')
option.bind('<Enter>', lambda e: paint_option('#ffa366'))
option.bind('<Leave>', lambda e: paint_option('#ff9966'))
option.bind('<Button-1>', lambda e: paint_option('#ff8750'))
option.bind('<ButtonRelease-1>', lambda e: paint_option('#ff9966'))

search_button = Button(text = "Поиск!", font = ('Terminal', 12),
                       bg = 'light gray', command = search)
search_button.pack(anchor = CENTER)

game_name_label = Label(window, text = '', bg = window['bg'])
game_name_label.pack()

game_link_label = Label(window, text = '', bg = window['bg'],
                        cursor = "hand2")
game_link_label.pack()
game_link_label.bind('<Enter>', lambda e: paint_link())
game_link_label.bind('<Leave>', lambda e: unpaint_link())
game_link_label.bind("<Button-1>", click_link)

link_font = font.Font(game_link_label, game_link_label.cget('font'))

game_img_label = Label(bg = window['bg'])
game_img_label.pack(anchor = CENTER)

footer_label = Label(text = "Все представленные игры бесплатные и доступны на сайте Steam®",
                     font = ('Terminal', 12), fg = 'white', bg = "#4f4f4f")
footer_label.pack(fill = X, side = BOTTOM)

window.resizable(width = False, height = False)
window.mainloop()
