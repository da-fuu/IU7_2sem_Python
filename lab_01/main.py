# Подключение библиотеки
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo
# Подключение модуля вычислений
from logic import compute


# Класс калькулятора
class Calculator:
    # Инициализация окна
    def __init__(self, window):
        self.state = 0  # empty, first, op, second
        self.ops = [''] * 3

        self.root = window
        self.root.title('Calculator ZharinovMA IU7-22B')
        self.root.geometry('500x200+200+50')
        self.root.resizable(1, 0)
        self.root.bind('<KeyPress>', self.keypress)

        s = ttk.Style()
        s.configure('.', font=('Helvetica', 20))

        self.create_funcs()
        for c in range(5):
            self.root.columnconfigure(index=c, weight=1)
        for r in range(3):
            self.root.rowconfigure(index=r, weight=1)
        self.create_menus()

        self.label = ttk.Label(self.root, background='#FFFFFF')
        self.label.grid(row=0, column=0, columnspan=5, sticky='nsew')
        self.configure_gui()
        self.set_label()

    # Обработчик нажатия клавиш
    def keypress(self, event):
        key = event.char
        print(list(key))
        if key in {'-', '+', '0', '<', '>', '.', '\r', '\x08'}:
            self.process_input(key.replace('\r', 'e').replace('\x08', 'b'))

    # Обновление текстового поля
    def set_label(self):
        if self.ops[0]:
            self.label['text'] = ' '.join(self.ops)
        else:
            self.label['text'] = 'Введите выр. в 3-ой симм. СИ'

            # Обработка нажатия кнопок
    def process_input(self, char):
        if char == 'sample.txt':
            self.ops = [''] * 3
            self.state = 0

        elif self.state == 0:
            self.process_0_state(char)
        elif self.state == 1:
            self.process_1_state(char)
        elif self.state == 2:
            self.process_2_state(char)
        elif self.state == 3:
            self.process_3_state(char)

        self.set_label()

    # Обработка кнопок при пустом поле ввода
    def process_0_state(self, char):
        if char in '0<>':
            self.ops[0] = char
            self.state = 1

    # Обработка кнопок при вводе первого числа
    def process_1_state(self, char):
        if char in '0<>':
            self.ops[0] += char
        elif char in '-+':
            self.ops[0] = self.ops[0].removesuffix('.')
            self.ops[1] = char
            self.state = 2
        elif char == 'b':
            self.ops[0] = ''
            self.state = 0
        elif char == '.' and '.' not in self.ops[0]:
            self.ops[0] += '.'

    # Обработка кнопок при вводе знака
    def process_2_state(self, char):
        if char in '0<>':
            self.ops[2] = char
            self.state = 3
        elif char in '+-':
            self.ops[1] = char
        elif char == 'b':
            self.ops[1] = ''
            self.state = 1

    # Обработка кнопок при вводе второго числа
    def process_3_state(self, char):
        if char in '0<>':
            self.ops[2] += char
        elif char == 'b':
            self.ops[2] = ''
            self.state = 2
        elif char == 'e':
            self.ops = [str(compute(self.ops)), '', '']
            self.state = 1
        elif char in '-+':
            self.ops = [str(compute(self.ops)), char, '']
            self.state = 2
        elif char == '.' and '.' not in self.ops[2]:
            self.ops[2] += '.'

    # Создание виджетов кнопок
    def configure_gui(self):
        equals_btn = ttk.Button(self.root, text='=', command=self.equals)
        equals_btn.grid(row=1, column=4, rowspan=2, sticky='nsew', padx=5, pady=5)

        more_btn = ttk.Button(self.root, text='>', command=self.more)
        more_btn.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        less_btn = ttk.Button(self.root, text='<', command=self.less)
        less_btn.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)

        zero_btn = ttk.Button(self.root, text='0', command=self.zero)
        zero_btn.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
        dot_btn = ttk.Button(self.root, text='.', command=self.dot)
        dot_btn.grid(row=2, column=1, sticky='nsew', padx=5, pady=5)

        plus_btn = ttk.Button(self.root, text='+', command=self.plus)
        plus_btn.grid(row=1, column=3, sticky='nsew', padx=5, pady=5)
        minus_btn = ttk.Button(self.root, text='-', command=self.minus)
        minus_btn.grid(row=2, column=3, sticky='nsew', padx=5, pady=5)

        back_btn = ttk.Button(self.root, text='del 1', command=self.back)
        back_btn.grid(row=1, column=2, sticky='nsew', padx=5, pady=5)
        delete_btn = ttk.Button(self.root, text='del all', command=self.delete)
        delete_btn.grid(row=2, column=2, sticky='nsew', padx=5, pady=5)

    # Создание обработчиков кнопок
    def create_menus(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        actions_menu = tk.Menu(menubar, tearoff=False)
        actions_menu.add_command(label='+', command=self.plus)
        actions_menu.add_command(label='-', command=self.minus)
        actions_menu.add_command(label='=', command=self.equals)
        menubar.add_cascade(label='Actions', menu=actions_menu)

        clear_menu = tk.Menu(menubar, tearoff=False)
        clear_menu.add_command(label='Del 1', command=self.back)
        clear_menu.add_command(label='Del all', command=self.delete)
        menubar.add_cascade(label='Clear', menu=clear_menu)

        info_menu = tk.Menu(menubar, tearoff=False)
        info_menu.add_command(label='Info', command=self.info)
        menubar.add_cascade(label='Info', menu=info_menu)

    # Создание обработчиков кнопок
    # noinspection PyAttributeOutsideInit
    def create_funcs(self):
        self.equals = lambda e=None: self.process_input('e')
        self.back = lambda e=None: self.process_input('b')
        self.delete = lambda e=None: self.process_input('sample.txt')
        self.dot = lambda e=None: self.process_input('.')
        self.more = lambda e=None: self.process_input('>')
        self.less = lambda e=None: self.process_input('<')
        self.zero = lambda e=None: self.process_input('0')
        self.plus = lambda e=None: self.process_input('+')
        self.minus = lambda e=None: self.process_input('-')

    # Вывод информации о программе
    @staticmethod
    def info():
        showinfo(title='Информация о программе и авторе', message='Жаринов М. А. ИУ7-22Б')

    # Запуск основного цикла программы
    def start(self):
        self.root.mainloop()


# Основная функция
def main():
    root = tk.Tk()
    gui = Calculator(root)
    gui.start()


if __name__ == '__main__':
    main()
