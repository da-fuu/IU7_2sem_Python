# Подключение библиотек
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from backend import decode_file, encode_file


# Класс приложения
# noinspection PyAttributeOutsideInit
class Steganography:
    # Инициализация окна
    def __init__(self, window):
        self.filename = ''
        self.file_opened = False
        self.root = window
        self.root.title('Steganography ZharinovMA IU7-22B')
        self.root.geometry('1000x700+200+50')
        self.root.resizable(0, 0)

        s = ttk.Style()
        s.configure('.', font=('Times New Roman', 14))
        self.root.columnconfigure(index=0, weight=1)
        self.root.columnconfigure(index=1, weight=1)
        self.root.rowconfigure(index=0, weight=1)
        self.root.rowconfigure(index=1, weight=1)
        self.root.rowconfigure(index=2, weight=10)

        self.configure_gui()

    # Создание виджетов
    def configure_gui(self):
        params = {'sticky': 'nsew', 'padx': 5, 'pady': 5, 'row': 0, 'column': 0}

        btn_file = ttk.Button(self.root, text='Выбрать файл', command=self.choose_file)
        btn_file.grid(**params)
        params['column'] += 1
        self.file_label = ttk.Label(self.root, text='Файл не выбран', width=20)
        self.file_label.grid(**params)
        params['column'] = 0
        params['row'] += 1

        btn_enc = ttk.Button(self.root, text='Закодировать', command=self.encode)
        btn_enc.grid(**params)
        params['column'] += 1
        btn_enc = ttk.Button(self.root, text='Раскодировать', command=self.decode)
        btn_enc.grid(**params)
        params['column'] = 0
        params['row'] += 1

        self.io_entry = tk.Text(self.root)
        self.io_entry.grid(columnspan=2, **params)

    # Выбор файла
    def choose_file(self):
        filename = askopenfilename(filetypes=[('BMP images', '*.bmp')])
        if filename == '':
            return
        self.filename = filename
        try:
            with open(self.filename, 'rb'):
                pass
            self.file_opened = True
            self.file_label['text'] = self.filename
        except OSError:
            self.file_opened = False
            self.file_label['text'] = 'Файл не выбран'
            showerror('Error', 'Invalid file name')

    # Зашифровать ввод в файл
    def encode(self):
        if not self.file_opened:
            showerror('Error', 'File not opened')
            return
        str_to_encode = self.io_entry.get('1.0', tk.END).removesuffix('\n')
        if not encode_file(self.filename, str_to_encode):
            showerror('Error', 'Text too large')
            return

    # Расшифровать строку из файла
    def decode(self):
        if not self.file_opened:
            showerror('Error', 'File not opened')
            return
        decoded_str = decode_file(self.filename)
        if decoded_str is None:
            showerror('Error', 'Invalid file')
            return
        self.io_entry.delete('1.0', tk.END)
        self.io_entry.insert('1.0', decoded_str)

    # Запуск основного цикла программы
    def run(self):
        self.root.mainloop()


# Основная функция
def main():
    window = tk.Tk()
    gui = Steganography(window)
    gui.run()


if __name__ == '__main__':
    main()
