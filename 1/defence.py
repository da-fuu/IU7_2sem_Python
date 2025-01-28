import tkinter as tk
import tkinter.ttk as ttk


def err():
    timeout_label['text'] = 'Некорректные данные!'


def calc(_):
    try:
        boat_speed = float(boat_entry.get())
    except ValueError:
        err()
        return
    try:
        river_speed = float(river_entry.get())
    except ValueError:
        err()
        return
    speed = boat_speed + flag.get() * river_speed
    if speed < 10 ** -7:
        err()
        return
    try:
        path = float(path_entry.get())
    except ValueError:
        err()
        return
    if path < 10 ** -7:
        err()
        return
    timeout_label['text'] = str(round(path/speed, 6))


root = tk.Tk()
root.title('Defence ZharinovMA IU7-22B')
root.geometry('700x600+200+50')
root.resizable(False, False)
for c in range(3):
    root.columnconfigure(index=c, weight=1)
for r in range(6):
    root.rowconfigure(index=r, weight=1)
s = ttk.Style()
s.configure('.', font=('Helvetica', 20))
flag = tk.IntVar(value=1)
along_btn = ttk.Radiobutton(text='По течению', value=1, variable=flag)
again_btn = ttk.Radiobutton(text='Против', value=-1, variable=flag)
common = {'sticky': 'nsew', 'padx': 5, 'pady': 5}
along_btn.grid(row=2, column=0, columnspan=2, **common)
again_btn.grid(row=3, column=0, columnspan=2, **common)

boat_entry = ttk.Entry(root, background='#FFFFFF', font=('Helvetica', 20))
boat_entry.grid(row=0, column=1, **common)
river_entry = ttk.Entry(root, background='#FFFFFF', font=('Helvetica', 20))
river_entry.grid(row=1, column=1, **common)

boat_label = ttk.Label(root, text='U лодки')
boat_label.grid(row=0, column=0, **common)
boat_label = ttk.Label(root, text='U реки')
boat_label.grid(row=1, column=0, **common)
path_label = ttk.Label(root, text='Расстояние')
path_label.grid(row=4, column=0, **common)

path_entry = ttk.Entry(root, background='#FFFFFF', font=('Helvetica', 20))
path_entry.grid(row=4, column=1, **common)

time_label = ttk.Label(root, text='Время')
time_label.grid(row=5, column=0, **common)
timeout_label = ttk.Label(root, background='#FFFFFF')
timeout_label.grid(row=5, column=1, **common)
eq_btn = ttk.Button(root, text='X', command=calc)
eq_btn.grid(row=5, column=2, **common)

root.mainloop()
