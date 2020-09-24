#!/usr/bin/python
# -*- coding: utf-8 -*-
import platform
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

plt = platform.system()
if plt == 'Darwin':
    from tkmacosx import Button, SFrame
else:
    from tkinter import Button, SFrame


def clear(root):
    for widget in root.winfo_children():
        widget.destroy()


def open_img(path, size=(30, 30)):
    image = Image.open(path)
    image = image.resize(size, Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    return image


class App(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('700x500')
        self.listbox = 'listbox'
        self.backgrounds = {'dark': '#333',
                            'light': 'white'}
        self.background_ = 'dark'
        self.theme = 'dark'
        self.anti_back = self.backgrounds['light' if self.background_ == 'dark' else 'dark']
        self.lang = 'en'
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenwidth()
        self.build_loading_root()
        self.button_theme = Button()
        self._language = 'lang'

    @property
    def theme(self):
        pass

    @theme.setter
    def theme(self, value):
        self.background_ = value
        self.anti_back_key = 'light' if self.background_ == 'dark' else 'dark'
        self.anti_back = self.backgrounds[self.anti_back_key]

    @theme.getter
    def theme(self):
        return self.backgrounds[self.background_]

    def change_lang(self, event):
        if self.listbox.get() == ' English ':
            self.lang = 'en'
        elif self.listbox.get() == ' Русский ':
            self.lang = 'ru'

    def change_theme(self):
        self.theme = self.anti_back_key
        path = self.get_theme_img()
        self.button_theme.configure(image=open_img(path))

    def back(self, screen='self.build_loading_root'):
        """

        :type screen: any
        """
        if isinstance(screen, str):
            screen = eval(screen)
        button2 = Button(self.root,
                         text='b a c k' if self.lang == 'en' else 'н а з а д',
                         bd=0,
                         bg=self.anti_back,
                         fg=self.theme,
                         width=self.screen_width,
                         height=30,
                         command=screen)
        button2.place(x=0, y=0)

    def get_theme_img(self):
        if self.theme == self.backgrounds['light']:
            path = '../sun.PNG'
        else:
            path = '../moon.PNG'
        return path

    def main_screen(self):
        clear(self.root)

        self.frame = SFrame(self.root, bg=self.theme)
        self.frame.pack(expand=1, fill='both')

        self.back()
        self.root.title('trading selector')
        self.root['bg'] = self.theme
        width = self.screen_width // 2
        button_realtime = Button(self.root,
                                 bg=self.theme,
                                 fg=self.anti_back,
                                 command=self.realtime_trade,
                                 image=open_img('../realtime.PNG', (width,
                                                                    round(width / 1.465813674530188))),
                                 bd=0)
        button_realtime.place(x=width // 2, y=50)
        text_realtime = Button(self.root,
                               bg=self.theme,
                               fg=self.anti_back,
                               text='realtime trading' if self.lang == 'en' else 'трейдинг в реальном времени',
                               command=self.realtime_trade,
                               width=width + 33,
                               bd=0)
        text_realtime.place(x=width // 2, y=round(width / 1.465813674530188) + 400)
        self.root.mainloop()

    def realtime_trade(self):
        clear(self.root)
        self.back(screen=self.main_screen)
        text = tk.Text(self.root, height=100, width=129)
        text.place(x=100, y=110)
        self.root.title('realtime trading')

    def build_loading_root(self):
        clear(self.root)
        self.root.title("quick_trade")
        self._language = 'Language:' if self.lang == 'en' else 'Язык:'
        self.root.configure(background=self.theme)
        # logo
        img = open_img('../qutr.PNG',
                       size=(self.screen_width // 3,
                             round(self.screen_height // 3 / 1.5)))
        label = tk.Label(self.root, image=img,
                         bd=0, bg=self.theme)
        label.pack()

        # continue
        if self.lang == 'ru':
            img_path = '../rus_continue.PNG'
        else:
            img_path = '../eng_continue.PNG'
        img_lang_continue = open_img(img_path, (200, 50))
        label2 = Button(self.root, image=img_lang_continue, bd=0, command=self.main_screen,
                        bg=self.theme)
        label2.pack(side='bottom', expand=self.screen_height // 10)

        # settings
        if self.theme == self.backgrounds['light']:
            img_path = '../settings_icon.PNG'
        else:
            img_path = '../setting_white.PNG'
        im3 = open_img(img_path,
                       (40, 40))
        label3 = Button(self.root, image=im3, bd=0, command=self.build_settings, bg=self.theme)
        label3.place(x=self.screen_width - 70, y=0)

        self.root.mainloop()

    def build_settings(self):
        clear(self.root)
        self.root.title('settings')
        self.root['bg'] = self.theme
        labelx = tk.Label(self.root,
                          text=self._language,
                          bg=self.theme,
                          fg=self.anti_back)

        self.listbox = ttk.Combobox(self.root, height=123, textvariable=tk.StringVar())
        self.listbox['values'] = (' English ',
                                  ' Русский ')
        self.listbox.current(0 if self.lang == 'en' else 1)
        self.listbox.place(x=100, y=60)
        self.listbox.bind("<<ComboboxSelected>>", self.change_lang)

        self.listbox.current()
        labelx.place(x=30, y=60)

        self.back()

        label_theme = tk.Label(self.root, text='Theme:' if self.lang == 'en' else 'Тема:', bg=self.theme,
                               fg=self.anti_back)
        label_theme.place(x=30, y=100)

        path = self.get_theme_img()
        self.button_theme = Button(self.root,
                                   bd=0,
                                   bg=self.theme,
                                   width=40,
                                   height=40,
                                   command=self.change_theme,
                                   image=open_img(path))
        self.button_theme.place(x=100, y=100)

        self.root.mainloop()


app = App()
