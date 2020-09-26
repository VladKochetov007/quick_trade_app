import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
import platform
import threading

plt = platform.system()
if plt == 'Darwin':
    from tkmacosx import Button
else:
    from tkinter import Button


def clear(root):
    for widget in root.winfo_children():
        widget.destroy()


def open_img(path, size=(30, 30)):
    image = Image.open(path)
    image = image.resize(size, Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    return image


class App(object):
    def build_canvas(self):
        self.canvas = tk.Canvas(self.root)
        self.canvas.place(relx=0, rely=0, relheight=1, relwidth=1)

    def _init_(self):
        print('srt')
        import quick_trade.trading_sys
        import quick_trade.utils

        df = quick_trade.utils.get_binance_data()
        self.trader = quick_trade.trading_sys.PatternFinder(df=df)
        print('load')
        self.loading = False
        self.looped = True
        self.pre_main()
        self.root.update()

    def __init__(self):
        self.loading = True
        self.looped = False
        self.trading_dats = {'secret-api': 'non set',
                             'public-api': 'non set'}
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
        self.button_theme = Button()
        self._language = 'lang'

        thread = threading.Thread(target=self._init_)
        thread.start()
        self.pre_main()

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

    def back(self, screen='self.pre_main'):
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
        self.back()
        self.root.title('trading selector')
        self.root['bg'] = self.theme
        width = self.screen_width // 2
        button_realtime = Button(self.root,
                                 bg=self.theme,
                                 fg=self.anti_back,
                                 text='realtime trading' if self.lang == 'en' else 'трейдинг в реальном времени',
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
        text_realtime.place(x=width // 2, y=round(width / 1.465813674530188) + 45)
        self.root.mainloop()

    def realtime_trade(self):
        clear(self.root)
        self.root.title('realtime trading')
        self.back(screen=self.main_screen)
        top = tk.Toplevel(self.root)
        top.title('binance keys')
        top.geometry('725x160')
        top['bg'] = self.theme

        def keys_api_set():
            self.trading_dats['public-api'] = self.message.get()
            self.trading_dats['secret-api'] = self.message2.get()
            print(self.trading_dats)
            top.destroy()

        self.message = tk.StringVar()
        entry = tk.Entry(top, textvariable=self.message, width=55, bg=self.theme, fg=self.anti_back, bd=3)  # public
        label1 = tk.Label(top,
                          text='public key' if self.lang == 'en' else 'Публичный ключ',
                          fg=self.anti_back,
                          bg=self.theme,
                          bd=0)
        label1.place(y=10, x=10)
        entry.place(x=160, y=10)
        self.message2 = tk.StringVar()
        entry = tk.Entry(top, textvariable=self.message2, width=55, bg=self.theme, fg=self.anti_back, bd=3)  # secret
        label2 = tk.Label(top,
                          text='Secret key' if self.lang == 'en' else 'Секретный ключ',
                          fg=self.anti_back,
                          bg=self.theme,
                          bd=0)
        label2.place(y=60, x=10)
        entry.place(x=160, y=60)
        submit_button = Button(top,
                               text='Submit' if self.lang == 'en' else 'Подтвердить',
                               width=100,
                               command=keys_api_set,
                               bg=self.theme,
                               fg=self.anti_back)
        submit_button.place(x=362-50, y=110)
        top.mainloop()

    def pre_main(self):
        clear(self.root)
        self.root.title("quick_trade")
        self._language = 'Language:' if self.lang == 'en' else 'Язык:'
        self.root.configure(background=self.theme)
        # logo
        self.__img_ = open_img('../qutr.PNG',
                               size=(self.screen_width // 3,
                                     round(self.screen_height // 3 / 1.5)))
        label_ = tk.Label(self.root, image=self.__img_,
                          bd=0, bg=self.theme)
        label_.pack()

        # continue
        if not self.loading:
            if self.lang == 'ru':
                img_path = '../rus_continue.PNG'
            else:
                img_path = '../eng_continue.PNG'
            img_lang_continue = open_img(img_path, (200, 50))
            label2 = Button(self.root, image=img_lang_continue, bd=0, command=self.main_screen,
                            bg=self.theme)
        else:
            label_text = 'loading...' if self.lang == 'en' else 'Загрузка...'
            label2 = tk.Label(fg=self.anti_back,
                              text=label_text,
                              bg=self.theme)
        label2.pack(side='bottom', expand=self.screen_height // 10)

        # settings
        if self.theme == self.backgrounds['light']:
            img_path = '../settings_icon.PNG'
        else:
            img_path = '../setting_white.PNG'
        im3 = open_img(img_path,
                       (40, 40))
        label3 = Button(self.root, image=im3, bd=5, command=self.build_settings, bg=self.theme)
        label3.place(x=self.screen_width - 70, y=0)
        if not self.looped:
            self.root.mainloop()
            self.looped = True

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
