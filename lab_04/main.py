# Подключение библиотек
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror
# Подключение функции расчета минимального круга
from backend import calc_circle


# Класс приложения
# noinspection PyAttributeOutsideInit
class Geometry:
    # Инициализация окна
    def __init__(self, window):
        self.root = window
        self.root.title('Geometry ZharinovMA IU7-22B')
        self.root.geometry('1030x771+200+0')
        self.root.resizable(0, 0)
        self.font = ('Times New Roman', 14)
        self.points = set()
        self.circle_id = None

        s = ttk.Style()
        s.configure('.', font=self.font)
        for i in range(5):
            self.root.columnconfigure(index=i, weight=1+10*(i % 2))
        # self.root.columnconfigure(index=5, weight=4)

        self.root.rowconfigure(index=0, weight=1)
        self.root.rowconfigure(index=1, weight=50)

        self.configure_gui()

    # Создание виджетов
    def configure_gui(self):
        params = {'sticky': 'nsew', 'padx': 5, 'pady': 5, 'row': 0, 'column': 0}

        label_x = ttk.Label(self.root, anchor='e', text='X')
        label_x.grid(**params)
        params['column'] += 1
        self.entry_x = ttk.Entry(self.root, font=self.font)
        self.entry_x.grid(**params)
        params['column'] += 1

        label_y = ttk.Label(self.root, anchor='e', text='Y')
        label_y.grid(**params)
        params['column'] += 1
        self.entry_y = ttk.Entry(self.root, font=self.font)
        self.entry_y.grid(**params)
        params['column'] += 1

        btn_enc = ttk.Button(self.root, text='Добавить', command=self.btn_point_action)
        btn_enc.grid(**params)
        params['column'] = 0
        params['row'] += 1

        params['padx'] = 15
        params['pady'] = 15
        self.canvas = tk.Canvas(self.root, bg='white', width=1000, height=700)
        self.canvas.grid(columnspan=5, **params)
        self.canvas.bind('<Button-1>', self.canvas_add_point)

    # Обработка нажатия на холст
    def canvas_add_point(self, event):
        self.add_point(event.x, event.y)

    # Обработка нажатия кнопки добавления точки
    def btn_point_action(self):
        try:
            x = int(self.entry_x.get())
            y = int(self.entry_y.get())
        except ValueError:
            showerror(title='Error', message='Некорректные целые координаты точки!')
            return

        if x < 1 or x >= int(self.canvas['width']) - 1:
            showerror(title='Error', message=f'Координата х должна быть от 1 до {int(self.canvas['width'])-1}!')
            return
        if y < 1 or y >= int(self.canvas['height']) - 1:
            showerror(title='Error', message=f'Координата y должна быть от 1 до {int(self.canvas['height'])-1}!')
            return

        self.add_point(x, y)

    # Добавить точку по координатам
    def add_point(self, x, y):
        self.points.add((x, y))
        radius = 1
        self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill='#000000', outline='#000000')
        self.update_circle()

    # Обновить нарисованную окружность
    def update_circle(self):
        if self.circle_id is not None:
            self.canvas.delete(self.circle_id)
        if len(self.points) == 0:
            return
        (x, y), rad = calc_circle(tuple(self.points))
        rad = round(rad) + 1
        self.circle_id = self.canvas.create_oval(x - rad, y - rad, x + rad, y + rad, outline='#FF0000')

    # Запуск основного цикла программы
    def run(self):
        self.root.mainloop()


# Основная функция
def main():
    window = tk.Tk()
    gui = Geometry(window)
    gui.run()


if __name__ == '__main__':
    main()
