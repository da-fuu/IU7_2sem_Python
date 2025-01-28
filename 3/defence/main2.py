# Подключение библиотек
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from PIL import ImageTk, Image
from itertools import combinations


# Класс приложения
# noinspection PyAttributeOutsideInit
class MazeSolver:
    # Инициализация окна
    def __init__(self, window):
        self.filename = ''
        self.file_opened = False
        self.image = None
        self.root = window
        self.root.title('Steganography ZharinovMA IU7-22B')
        self.root.geometry('1500x800+0+10')
        self.root.resizable(0, 0)

        s = ttk.Style()
        s.configure('.', font=('Times New Roman', 14))
        self.root.columnconfigure(index=0, weight=1)
        self.root.columnconfigure(index=1, weight=1)
        self.root.rowconfigure(index=0, weight=1)
        self.root.rowconfigure(index=1, weight=1)
        self.root.rowconfigure(index=2, weight=50)

        self.configure_gui()

    # Создание виджетов
    def configure_gui(self):
        params = {'sticky': 'nsew', 'padx': 0, 'pady': 0, 'row': 0, 'column': 0}

        btn_file = ttk.Button(self.root, text='Выбрать файл', command=self.choose_file)
        btn_file.grid(**params)
        params['column'] += 1
        self.file_label = ttk.Label(self.root, text='Файл не выбран', width=20)
        self.file_label.grid(**params)
        params['column'] = 0
        params['row'] += 1

        btn_enc = ttk.Button(self.root, text='Решить', command=self.solve)
        btn_enc.grid(columnspan=2, **params)
        params['column'] = 0
        params['row'] += 1

        self.photo = tk.Canvas(self.root, height=40, width=70)
        self.photo.grid(columnspan=2, **params)

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
            return

        with Image.open(self.filename) as img:
            self.upd_image(img)

    def upd_image(self, img: Image):
        k = min(800/img.width, 700/img.height)
        self.image = ImageTk.PhotoImage(img.resize(size=(int(img.width*k), int(img.height*k)),
                                                   resample=Image.Resampling.HAMMING))
        self.photo.create_image(0, 0, anchor='nw', image=self.image)

    # Решить лабиринт
    def solve(self):
        if not self.file_opened:
            showerror('Error', 'File not opened')
            return

        solved_maze = self.solve_maze(self.get_img_matrix())
        self.upd_image(self.matrix_to_img(solved_maze))

    def get_img_matrix(self):
        matrix = []
        with Image.open(self.filename) as img:
            lst = list(img.getdata())
            for i in range(img.height):
                matrix.append(lst[img.width * i:img.width * (i + 1)])
        return matrix

    @staticmethod
    def matrix_to_img(matrix):
        mass = []
        for row in matrix:
            for pixel in row:
                mass.extend(list(pixel))
        return Image.frombytes(data=bytes(mass), size=(len(matrix[0]), len(matrix)), mode='RGB')

    # noinspection PyTypeChecker
    @staticmethod
    def solve_maze(maze_matrix):
        height = len(maze_matrix)
        width = len(maze_matrix[0])

        exits = set()
        for i in range(width):
            if sum(maze_matrix[0][i]) > 300:
                exits.add((0, i))
            if sum(maze_matrix[-1][i]) > 300:
                exits.add((height - 1, i))
        for i in range(height):
            if sum(maze_matrix[i][0]) > 300:
                exits.add((i, 0))
            if sum(maze_matrix[i][-1]) > 300:
                exits.add((i, width - 1))
        exits = list(exits)
        print('Open ends:', exits)
        for start, stop in combinations(exits, r=2):
            print('Trying from', start, 'to', stop)
            path_matrix = [[None for _ in range(width)] for _ in range(height)]
            path_matrix[start[0]][start[1]] = start
            active = [start]

            flag = False
            while not flag:
                if len(active) == 0:
                    break

                i, j = active.pop(0)

                for di, dj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    ci = i + di
                    cj = j + dj
                    if 0 <= ci < height and 0 <= cj < width:
                        if path_matrix[ci][cj] is None and sum(maze_matrix[ci][cj]) > 300:
                            path_matrix[ci][cj] = (i, j)
                            if (ci, cj) == stop:
                                flag = True
                                break
                            active.append((ci, cj))

            if not flag:
                print('fail')
                continue
            curr = stop
            while path_matrix[curr[0]][curr[1]] != curr:
                if sum(curr) < 3:
                    pass
                maze_matrix[curr[0]][curr[1]] = (255, 0, 0)
                curr = path_matrix[curr[0]][curr[1]]
            maze_matrix[curr[0]][curr[1]] = (255, 0, 0)
        return maze_matrix

    # Запуск основного цикла программы
    def run(self):
        self.root.mainloop()


# Основная функция
def main():
    window = tk.Tk()
    gui = MazeSolver(window)
    gui.run()


if __name__ == '__main__':
    main()
