import random
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

from config import *
from Mine_Sweep import Mine_Map


class Mine_GUI:
    def __init__(self, gui):
        self.gui = gui
        self.gui.title('MineSweep SES')
        # import images and load into dict
        self.images = {
            Unknown_Grid: tk.PhotoImage(file='./Image/tile_unknown.gif'),
            Unflagg_Mine: tk.PhotoImage(file='./Image/tile_mine.gif'),
            Flagged_Grid: tk.PhotoImage(file='./Image/tile_flag.gif'),
            UnMined_Flag: tk.PhotoImage(file='./Image/tile_wrong.gif'),
            Flagged_Mine: tk.PhotoImage(file='./Image/tile_right.gif'),
            "0": tk.PhotoImage(file='./Image/tile_0.gif'),
            "1": tk.PhotoImage(file='./Image/tile_1.gif'),
            "2": tk.PhotoImage(file='./Image/tile_2.gif'),
            "3": tk.PhotoImage(file='./Image/tile_3.gif'),
            "4": tk.PhotoImage(file='./Image/tile_4.gif'),
            "5": tk.PhotoImage(file='./Image/tile_5.gif'),
            "6": tk.PhotoImage(file='./Image/tile_6.gif'),
            "7": tk.PhotoImage(file='./Image/tile_7.gif'),
            "8": tk.PhotoImage(file='./Image/tile_8.gif')
        }

        self.Mine_Panel_Setup()
        self.Playing_Data_Panel_Setup()
        self.Control_Panel_Setup()

    def Mine_Panel_Setup(self):

        # init grids as tkinter.button
        self.Button_List = [[
            tk.Button(self.gui, image=self.images[Unknown_Grid])
            for i in range(SIZE_Y)
        ] for j in range(SIZE_X)]

        for x in range(SIZE_X):
            for y in range(SIZE_Y):
                # bind the click of each button to their event function
                # use lambda to send arguments for event function

                # left
                self.Button_List[x][y].bind(
                    '<Button-1>',
                    lambda event, a=x, b=y: self.Callback_Left(a, b))
                # right
                self.Button_List[x][y].bind(
                    '<Button-3>',
                    lambda event, a=x, b=y: self.Callback_Right(a, b))
                # show each button on GUI
                self.Button_List[x][y].grid(row=x, column=y)
        self.Steps = 0
        dt = datetime.now()
        self.start = 3600 * dt.hour + 60 * dt.minute + dt.second
        self.gui.update_idletasks()

    def Playing_Data_Panel_Setup(self):
        # playing data shown
        self.playing_data_labels = {
            'time': tk.Label(self.gui, text='00:00:00'),
            'Mines': tk.Label(self.gui, text='Mines: 0'),
            'Flags': tk.Label(self.gui, text='Flags: 0')
        }

        self.playing_data_labels['time'].grid(row=SIZE_X + 1,
                                              column=0,
                                              columnspan=SIZE_Y // 3)
        self.playing_data_labels['Mines'].grid(row=SIZE_X + 1,
                                               column=SIZE_Y // 3,
                                               columnspan=SIZE_Y // 3)
        self.playing_data_labels['Flags'].grid(row=SIZE_X + 1,
                                               column=2 * SIZE_Y // 3,
                                               columnspan=SIZE_Y // 3)
        self.gui.update_idletasks()

    def Control_Panel_Setup(self):
        # playing data shown
        self.control_buttons = {
            'new_game': tk.Button(self.gui, text='new game'),
            'replay': tk.Button(self.gui, text='replay'),
            'auto_play': tk.Button(self.gui, text='auto play')
        }
        self.control_buttons['auto_play'].bind('<Button-1>',
                                               self.Callback_Auto_Play)

        self.control_buttons['new_game'].grid(row=SIZE_X + 2,
                                              column=0,
                                              columnspan=SIZE_Y // 3)
        self.control_buttons['replay'].grid(row=SIZE_X + 2,
                                            column=SIZE_Y // 3,
                                            columnspan=SIZE_Y // 3)
        self.control_buttons['auto_play'].grid(row=SIZE_X + 2,
                                               column=2 * SIZE_Y // 3,
                                               columnspan=SIZE_Y // 3)
        self.gui.update_idletasks()

    # event function of left button click
    def Callback_Left(self, x, y):
        if self.Steps == 0:
            print('Game Start')
            print('init your game at (%d,%d)' % (x, y))
            # init an object from class Mine_Map
            self.Mines = Mine_Map(x, y)
            # Refresh GUI
            self.GUI_Refresh(x, y)
            self.Message()

        else:
            # Use function from object Mines
            self.Mines.Click(x, y)
            # Refresh GUI
            self.GUI_Refresh(x, y)
            self.Message()

        self.Steps += 1

    # event function of right button click
    def Callback_Right(self, x, y):
        if self.Steps == 0:
            print('Game Start')
            print('init your game at (%d,%d)' % (x, y))
            self.Mines = Mine_Map(x, y)
            self.GUI_Refresh(x, y)
            self.Message()
        else:
            self.Mines.Flag(x, y)
            self.GUI_Refresh(x, y)
            self.Message()

        self.Steps += 1

    def Callback_Auto_Play(self, event):
        if self.Steps != 0:
            Mine_List = self.Mines.Mine_Grid()
            operate_list = []
            while self.Mines.Status == alive:
                x = random.sample(range(SIZE_X), 1)[0]
                y = random.sample(range(SIZE_Y), 1)[0]
                grid = [x, y]
                if self.Mines.is_Unknown(x, y):
                    if grid not in operate_list:
                        operate_list.append(grid)
                        if grid not in Mine_List:
                            self.Mines.Click(x, y)
                        elif grid in Mine_List:
                            self.Mines.Flag(x, y)
                    self.GUI_Refresh(x, y)
            self.Message()

    # upgrade showing on GUI
    def GUI_Refresh(self, x, y):
        # refresh the grid with operation firstly
        M = self.Mines.Show_Map[x][y]
        self.Button_List[x][y].configure(image=self.images[M])
        # refresh all other grids
        for i in range(SIZE_X):
            for j in range(SIZE_Y):
                M = self.Mines.Show_Map[i][j]
                self.Button_List[i][j].configure(image=self.images[M])
        # refresh playing data
        dt = datetime.now()
        time_now = 3600 * dt.hour + 60 * dt.minute + dt.second
        time_cost = (time_now - self.start)
        sec = str(int(time_cost % 60)).rjust(2, '0')
        min = str(int(time_cost // 60)).rjust(2, '0')
        hour = str(int(time_cost // 3600)).rjust(2, '0')
        time_str = str(hour) + ':' + str(min) + ':' + str(sec)
        flag_num = self.Mines.Flag_Num()
        flag_str = 'Flags: ' + str(flag_num)
        mine_str = 'Mines: ' + str(MINE_NUM - flag_num)
        self.playing_data_labels['time'].configure(text=time_str)
        self.playing_data_labels['Mines'].configure(text=mine_str)
        self.playing_data_labels['Flags'].configure(text=flag_str)
        self.gui.update_idletasks()

    # Message box
    def Message(self):
        S = self.Mines.Status
        if S == die:
            messagebox.showerror(title="DIED", message="You are died!!!")
        elif S == win:
            messagebox.showinfo(title="WINNING",
                                message="You are the winner!!!")


if __name__ == "__main__":
    windows = tk.Tk()
    # windows.title("Mine_Sweeper SES")
    minesweep_GUI = Mine_GUI(windows)

    windows.mainloop()
