# Подключение библиотек
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror
# Подключение функции расчета минимального круга
from backend import calc_line, enlarge


# Класс приложения
# noinspection PyAttributeOutsideInit
class Geometry:
    # Инициализация окна
    def __init__(self, window):
        self.root = window
        self.root.title('Geometry ZharinovMA IU7-22B')
        self.root.geometry('1230x771+200+0')
        self.root.resizable(0, 0)
        self.font = ('Times New Roman', 12)
        self.field = 0
        self.points = set()
        self.triangles = set()
        self.line_id = None

        s = ttk.Style()
        s.configure('.', font=self.font)
        for i in range(12):
            self.root.columnconfigure(index=i, weight=1+40*(i % 2))
        self.root.columnconfigure(index=12, weight=0)

        self.root.rowconfigure(index=0, weight=1)
        self.root.rowconfigure(index=1, weight=1)
        self.root.rowconfigure(index=2, weight=50)

        self.configure_gui()

    # Создание виджетов
    def configure_gui(self):
        params = {'sticky': 'nsew', 'padx': 3, 'pady': 3, 'row': 0, 'column': 0}

        label_x = ttk.Label(self.root, anchor='e', text='X')
        label_x.grid(**params)
        params['column'] += 1
        self.entry_x = ttk.Entry(self.root, font=self.font)
        self.entry_x.grid(**params, columnspan=5)
        params['column'] += 5
        label_y = ttk.Label(self.root, anchor='e', text='Y')
        label_y.grid(**params)
        params['column'] += 1
        self.entry_y = ttk.Entry(self.root, font=self.font)
        self.entry_y.grid(**params, columnspan=5)
        params['column'] += 5
        btn_point = ttk.Button(self.root, text='Добавить точку', command=self.btn_point_action)
        btn_point.grid(**params)
        params['column'] = 0
        params['row'] += 1

        label_x1 = ttk.Label(self.root, anchor='e', text='X1')
        label_x1.grid(**params)
        params['column'] += 1
        self.entry_x1 = ttk.Entry(self.root, font=self.font)
        self.entry_x1.grid(**params)
        params['column'] += 1
        label_y1 = ttk.Label(self.root, anchor='e', text='Y1')
        label_y1.grid(**params)
        params['column'] += 1
        self.entry_y1 = ttk.Entry(self.root, font=self.font)
        self.entry_y1.grid(**params)
        params['column'] += 1
        label_x2 = ttk.Label(self.root, anchor='e', text='X2')
        label_x2.grid(**params)
        params['column'] += 1
        self.entry_x2 = ttk.Entry(self.root, font=self.font)
        self.entry_x2.grid(**params)
        params['column'] += 1
        label_y2 = ttk.Label(self.root, anchor='e', text='Y2')
        label_y2.grid(**params)
        params['column'] += 1
        self.entry_y2 = ttk.Entry(self.root, font=self.font)
        self.entry_y2.grid(**params)
        params['column'] += 1
        label_x3 = ttk.Label(self.root, anchor='e', text='X3')
        label_x3.grid(**params)
        params['column'] += 1
        self.entry_x3 = ttk.Entry(self.root, font=self.font)
        self.entry_x3.grid(**params)
        params['column'] += 1
        label_y3 = ttk.Label(self.root, anchor='e', text='Y3')
        label_y3.grid(**params)
        params['column'] += 1
        self.entry_y3 = ttk.Entry(self.root, font=self.font)
        self.entry_y3.grid(**params)
        params['column'] += 1

        btn_triangle = ttk.Button(self.root, text='Добавить треугольник', command=self.btn_triangle_action)
        btn_triangle.grid(**params)
        params['column'] = 0
        params['row'] += 1

        params['padx'] = 15
        params['pady'] = 15
        self.canvas = tk.Canvas(self.root, bg='white', width=1200, height=700)
        self.canvas.grid(columnspan=13, **params)
        self.canvas.bind('<Button-1>', self.canvas_add_point)
        self.canvas.bind('<Button-3>', self.canvas_add_peak)

    # Обработка нажатия на холст
    def canvas_add_point(self, event):
        self.add_point(event.x, event.y)

    def canvas_add_peak(self, event):
        if self.field == 0:
            self.entry_x1.delete(0, tk.END)
            self.entry_y1.delete(0, tk.END)
            self.entry_x1.insert(0, event.x)
            self.entry_y1.insert(0, event.y)
        elif self.field == 1:
            self.entry_x2.delete(0, tk.END)
            self.entry_y2.delete(0, tk.END)
            self.entry_x2.insert(0, event.x)
            self.entry_y2.insert(0, event.y)
        else:
            self.entry_x3.delete(0, tk.END)
            self.entry_y3.delete(0, tk.END)
            self.entry_x3.insert(0, event.x)
            self.entry_y3.insert(0, event.y)
        self.field += 1
        if self.field == 3:
            self.field = 0
            self.btn_triangle_action()

    def btn_triangle_action(self):
        try:
            x1 = int(self.entry_x1.get())
            y1 = int(self.entry_y1.get())
            x2 = int(self.entry_x2.get())
            y2 = int(self.entry_y2.get())
            x3 = int(self.entry_x3.get())
            y3 = int(self.entry_y3.get())
        except ValueError:
            showerror(title='Error', message='Некорректные целые координаты точки!')
            return
        for x, y in ((x1, y1), (x2, y2), (x3, y3)):
            if x < 1 or x >= int(self.canvas['width']) - 1:
                showerror(title='Error', message=f'Координата х должна быть от 1 до {int(self.canvas['width'])-1}!')
                return
            if y < 1 or y >= int(self.canvas['height']) - 1:
                showerror(title='Error', message=f'Координата y должна быть от 1 до {int(self.canvas['height'])-1}!')
                return

        self.add_triangle(x1, y1, x2, y2, x3, y3)

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

    def add_triangle(self, x1, y1, x2, y2, x3, y3):
        self.triangles.add(((x1, y1), (x2, y2), (x3, y3)))
        self.canvas.create_line(x1, y1, x2, y2)
        self.canvas.create_line(x3, y3, x2, y2)
        self.canvas.create_line(x1, y1, x3, y3)
        self.update_line()

    # Добавить точку по координатам
    def add_point(self, x, y):
        self.points.add((x, y))
        radius = 1
        self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill='#000000', outline='#000000')
        self.update_line()

    # Обновить нарисованную окружность
    def update_line(self):
        if self.line_id is not None:
            self.canvas.delete(self.line_id)
        if len(self.points) < 2:
            return
        line = calc_line(tuple(self.points), tuple(self.triangles))
        if line is None:
            return
        enlarge(line, int(self.canvas['width']), int(self.canvas['height']))
        self.line_id = self.canvas.create_line(*line, fill='#FF0000')

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
