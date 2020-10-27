import tkinter as tk

from Mine_GUI import Mine_GUI

SIZE_X = 12
SIZE_Y = 24
MINE_NUM = (SIZE_X * SIZE_Y) // 8

if __name__ == '__main__':
    windows = tk.Tk()
    minesweep_GUI = Mine_GUI(windows, SIZE_X, SIZE_Y, MINE_NUM)
    windows.mainloop()
