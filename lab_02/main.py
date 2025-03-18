# Подключение библиотек
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showerror
from sympy import parse_expr, diff, lambdify
from sympy.abc import x
from numpy import arange, linspace
import matplotlib.pyplot as plt
# Подключение модуля вычислений
from logic import find_012_order_roots, extract_roots


# Класс приложения
# noinspection PyAttributeOutsideInit
class RootFinder:
    # Инициализация окна
    def __init__(self, window):
        self.function = None
        self.start = self.stop = self.step = self.nmax = self.eps = None

        self.root = window
        self.root.title('RootFinder ZharinovMA IU7-22B')
        self.root.geometry('1000x700+200+50')
        self.root.resizable(0, 0)

        s = ttk.Style()
        s.configure('.', font=('Times New Roman', 14))

        for c in range(7):
            self.root.columnconfigure(index=c, weight=1)
        for r in range(2):
            self.root.rowconfigure(index=r, weight=1)
        self.root.rowconfigure(index=2, weight=30)

        self.configure_entry()
        self.configure_table()

    # Создание виджетов
    def configure_entry(self):
        params = {'sticky': 'nsew', 'padx': 5, 'pady': 5, 'row': 0, 'column': 0}

        func_label = ttk.Label(self.root, text='Функция:')
        func_label.grid(**params)
        params['column'] += 1
        self.func_entry = ttk.Entry(self.root)
        self.func_entry.grid(**params)
        self.func_entry.insert(0, 'cos(x)*x**2')
        params['column'] += 1

        start_label = ttk.Label(self.root, text='Начало:')
        start_label.grid(**params)
        params['column'] += 1
        self.start_entry = ttk.Entry(self.root)
        self.start_entry.grid(**params)
        self.start_entry.insert(0, '-10')
        params['column'] += 1

        stop_label = ttk.Label(self.root, text='Конец:')
        stop_label.grid(**params)
        params['column'] += 1
        self.stop_entry = ttk.Entry(self.root)
        self.stop_entry.grid(**params)
        self.stop_entry.insert(0, '10')
        params['column'] = 0
        params['row'] += 1

        step_label = ttk.Label(self.root, text='Шаг деления:')
        step_label.grid(**params)
        params['column'] += 1
        self.step_entry = ttk.Entry(self.root)
        self.step_entry.grid(**params)
        self.step_entry.insert(0, '0.1')
        params['column'] += 1

        nmax_label = ttk.Label(self.root, text='Число итераций:')
        nmax_label.grid(**params)
        params['column'] += 1
        self.nmax_entry = ttk.Entry(self.root)
        self.nmax_entry.grid(**params)
        self.nmax_entry.insert(0, '20')
        params['column'] += 1

        eps_label = ttk.Label(self.root, text='Точность:')
        eps_label.grid(**params)
        params['column'] += 1
        self.eps_entry = ttk.Entry(self.root)
        self.eps_entry.grid(**params)
        self.eps_entry.insert(0, '0.00001')
        params['column'] += 1
        params['row'] = 0

        process_btn = ttk.Button(self.root, text='Расчет корней', command=self.process)
        process_btn.grid(rowspan=2, **params)

    # Создать таблицу
    def configure_table(self):
        columns = ('ind', 'seg', 'root', 'val', 'num', 'err')
        columns_ru = ('№ корня', '[xi; xi+1]', 'x’', 'f(x’)', 'Количество итераций', 'Код ошибки')
        self.table = ttk.Treeview(columns=columns, show='headings')
        self.table.grid(row=2, column=0, columnspan=7, sticky='nsew', padx=5, pady=5)

        for col, ru in zip(columns, columns_ru):
            self.table.heading(col, text=ru)
        self.table.column('#1', width=80, stretch=False)
        for i in range(1, len(columns)-1):
            self.table.column(f'#{i+1}', width=150, stretch=True)
        self.table.column(f'#{len(columns)}', width=100, stretch=False)

    # Считать ввод
    def read_entries(self):
        try:
            self.start = float(self.start_entry.get())
            self.stop = float(self.stop_entry.get())
            self.step = float(self.step_entry.get())
            self.nmax = int(self.nmax_entry.get())
            self.eps = float(self.eps_entry.get())

        except ValueError:
            return -1, 'Неверный ввод параметров!'

        if not self.eps > 0 or self.nmax <= 0 or not self.step > 0 or not self.stop > self.start:
            return -2, 'Некорректные значения параметров расчета!'

        return self.read_func()

    def read_func(self):
        func_str = self.func_entry.get().removeprefix('y=')
        # noinspection PyBroadException
        try:
            self.function = parse_expr(func_str)
            for i in range(3):
                func = diff(self.function, x, i)
                x_arr = list(arange(self.start, self.stop + self.step, min(self.step, (self.stop - self.start) / 100)))
                for arg in x_arr:
                    val = func.evalf(subs={x: arg})
                    if not val.is_number or not val.is_real:
                        raise FloatingPointError
        except SyntaxError:
            return -3, 'Неверный ввод функции!'
        except FloatingPointError:
            return -4, 'Введенная функция или ее производная - комплексная или невычислимая на отрезке функция!'
        except Exception:
            return -5, 'Неверные параметры расчета!'

        return 0, None

    def update_table(self, data):
        for ind, seg in enumerate(data, start=1):
            a, b, arg, y_val, iters, err = seg
            seg_str = ' [{:.5g}; {:.5g}]'.format(a, b)
            root_info = (f' {arg: .6g}', f' {y_val: .0e}') if err == 0 else (' -', ' -')
            self.table.insert('', ind, values=(f' {ind}', seg_str, *root_info, f' {iters}', f' {err}'))

    def draw_plot(self, data):
        x_arr = linspace(self.start, self.stop, 1000)
        func = lambdify(x, self.function)

        plt.close()
        plt.plot(x_arr, [func(arg) for arg in x_arr], label='График функции')
        for i, params in enumerate((('Корни', 'r*'), ('Точки экстремума', 'g+'), ('Точки перегиба', 'bx'))):
            roots = extract_roots(data[i], func)
            if roots:
                plt.plot(*roots, params[1], label=params[0], markersize=10)
        plt.legend(loc='upper left')
        plt.grid()
        plt.show()

    # Полная обработка
    def process(self):
        self.table.delete(*self.table.get_children())

        res, message = self.read_entries()
        if res != 0:
            showerror(title='Error', message=message)
            return res

        data = find_012_order_roots(self.function, self.start, self.stop, self.step, self.nmax, self.eps)

        self.update_table(data[0])

        self.draw_plot(data)

    # Запуск основного цикла программы
    def run(self):
        self.root.mainloop()


# Основная функция
def main():
    window = tk.Tk()
    gui = RootFinder(window)
    gui.run()


if __name__ == '__main__':
    main()
