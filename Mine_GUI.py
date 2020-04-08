import copy
import tkinter as tk
from tkinter import messagebox

from Mine_Map import Mine_Map


class Mine_GUI(Mine_Map):
    def __init__(self, gui, x, y, n):

        self.gui = gui
        self.gui.title('MineSweep SES')
        # import images and load into dict
        # init object of Mine_Map
        self.SIZE_X = x
        self.SIZE_Y = y
        self.MINE_NUM = n
        self.Mines = Mine_Map(self.SIZE_X, self.SIZE_Y, self.MINE_NUM)
        self.images = {
            self.Mines.Unknown_Grid:
            tk.PhotoImage(file='./Image/tile_unknown.gif'),
            self.Mines.Unflagg_Mine:
            tk.PhotoImage(file='./Image/tile_mine.gif'),
            self.Mines.Flagged_Grid:
            tk.PhotoImage(file='./Image/tile_flag.gif'),
            self.Mines.UnMined_Flag:
            tk.PhotoImage(file='./Image/tile_wrong.gif'),
            self.Mines.Flagged_Mine:
            tk.PhotoImage(file='./Image/tile_right.gif'),
            '0': tk.PhotoImage(file='./Image/tile_0.gif'),
            '1': tk.PhotoImage(file='./Image/tile_1.gif'),
            '2': tk.PhotoImage(file='./Image/tile_2.gif'),
            '3': tk.PhotoImage(file='./Image/tile_3.gif'),
            '4': tk.PhotoImage(file='./Image/tile_4.gif'),
            '5': tk.PhotoImage(file='./Image/tile_5.gif'),
            '6': tk.PhotoImage(file='./Image/tile_6.gif'),
            '7': tk.PhotoImage(file='./Image/tile_7.gif'),
            '8': tk.PhotoImage(file='./Image/tile_8.gif')
        }

        # setup panels of GUI
        self.Playing_Data_Panel_Setup()
        self.Control_Panel_Setup()
        self.Mine_Panel_Setup()

    def Mine_Panel_Setup(self):

        # init grids as tkinter.button
        self.Button_List = [[
            tk.Button(self.gui, image=self.images[self.Mines.Unknown_Grid])
            for i in range(self.SIZE_Y)
        ] for j in range(self.SIZE_X)]

        for x in range(self.SIZE_X):
            for y in range(self.SIZE_Y):
                # bind the click of each button to their event function
                # use lambda to send arguments for event function

                # left
                self.Button_List[x][y].bind(
                    '<Button-1>',
                    lambda event, a=x, b=y: self.Callback_Left(a, b))

                # right or middle
                # Button-2
                #   Win and Linux: Middle
                #   MacOS:  Right
                self.Button_List[x][y].bind(
                    '<Button-2>',
                    lambda event, a=x, b=y: self.Callback_Right(a, b))
                self.Button_List[x][y].bind(
                    '<Button-3>',
                    lambda event, a=x, b=y: self.Callback_Right(a, b))

                # enter grid
                self.Button_List[x][y].bind(
                    '<Enter>',
                    lambda event, a=x, b=y: self.Callback_Enter(a, b))
                # show each button on GUI
                self.Button_List[x][y].grid(row=x, column=y)

        self.Steps = 0
        self.gui.update_idletasks()

    def Playing_Data_Panel_Setup(self):
        # playing data shown
        self.playing_data_labels = {
            'Steps': tk.Label(self.gui, text='Steps: 0'),
            'Mines': tk.Label(self.gui, text='Mines: 0'),
            'Flags': tk.Label(self.gui, text='Flags: 0'),
            'Row': tk.Label(self.gui, text='Row: ' + str(self.SIZE_X)),
            'Col': tk.Label(self.gui, text='Col: ' + str(self.SIZE_Y))
        }

        self.playing_data_labels['Steps'].grid(row=self.SIZE_X + 1,
                                               column=0,
                                               columnspan=self.SIZE_Y // 3)
        self.playing_data_labels['Mines'].grid(row=self.SIZE_X + 1,
                                               column=self.SIZE_Y // 3,
                                               columnspan=self.SIZE_Y // 3)
        self.playing_data_labels['Flags'].grid(row=self.SIZE_X + 1,
                                               column=2 * self.SIZE_Y // 3,
                                               columnspan=self.SIZE_Y // 3)
        self.playing_data_labels['Row'].grid(row=self.SIZE_X + 3,
                                             column=0,
                                             columnspan=self.SIZE_Y // 3)
        self.playing_data_labels['Col'].grid(row=self.SIZE_X + 3,
                                             column=self.SIZE_Y // 3,
                                             columnspan=self.SIZE_Y // 3)
        self.gui.update_idletasks()

    def Control_Panel_Setup(self):
        # playing data shown dict
        self.control_buttons = {
            'new_game': tk.Button(self.gui, text='New Game'),
            'replay': tk.Button(self.gui, text='Replay'),
            'auto_play': tk.Button(self.gui, text='Auto Play'),
            'quit': tk.Button(self.gui, text='QUIT')
        }

        self.control_buttons['new_game'].bind(
            '<Button-1>', lambda event: self.Callback_New_Game())
        self.control_buttons['replay'].bind(
            '<Button-1>', lambda event: self.Callback_Replay())
        self.control_buttons['auto_play'].bind(
            '<Button-1>', lambda event: self.Callback_Auto_Play())
        self.control_buttons['quit'].bind('<Button-1>',
                                          lambda event: self.Callback_Quit())

        self.control_buttons['new_game'].grid(row=self.SIZE_X + 2,
                                              column=0,
                                              columnspan=self.SIZE_Y // 3)
        self.control_buttons['replay'].grid(row=self.SIZE_X + 2,
                                            column=self.SIZE_Y // 3,
                                            columnspan=self.SIZE_Y // 3)
        self.control_buttons['auto_play'].grid(row=self.SIZE_X + 2,
                                               column=2 * self.SIZE_Y // 3,
                                               columnspan=self.SIZE_Y // 3)
        self.control_buttons['quit'].grid(row=self.SIZE_X + 3,
                                          column=2 * self.SIZE_Y // 3,
                                          columnspan=self.SIZE_Y // 3)
        self.gui.update_idletasks()

    # event function of left button click
    def Callback_Left(self, x, y):
        # step 1, setup mines
        if self.Mines.Steps == 0:
            print('Game Start')
            print('init your game at (%d,%d)' % (x, y))
            # init an object from class Mine_Map
            self.Mines.Mines_Setup(x, y)
            # Refresh GUI
            self.GUI_Refresh(x, y)
            self.Message()

        else:
            # click grid
            if self.Mines.Show_Map[x][y] == self.Mines.Unknown_Grid:
                # Use function from object Mines
                self.Mines.Click(x, y)

            # Refresh GUI
            self.GUI_Refresh(x, y)
            self.Message()

    # event function of right button click
    def Callback_Right(self, x, y):
        # step 1, setup mines
        if self.Mines.Steps == 0:
            print('Game Start')
            print('init your game at (%d,%d)' % (x, y))
            self.Mines.Mines_Setup(x, y)
            self.GUI_Refresh(x, y)
            self.Message()
        # flag and unflag
        else:
            self.Mines.Flag(x, y)
            self.GUI_Refresh(x, y)
            self.Message()

    def Callback_Enter(self, x, y):
        row_str = 'Row: ' + str(x)
        col_str = 'Col: ' + str(y)
        self.playing_data_labels['Row'].configure(text=row_str)
        self.playing_data_labels['Col'].configure(text=col_str)
        self.gui.update_idletasks()

    # auto play
    def Callback_Auto_Play(self):
        # DO NOT USE '=', it's reference not copy
        new_Mine = copy.deepcopy(self.Mines)

        Operate_List = new_Mine.Auto_Play()
        # del new_Mine
        for op in Operate_List:
            x = op[0]
            y = op[1]
            f = op[2]
            if f == 1:
                self.Mines.Click(x, y)
                self.GUI_Refresh(x, y)
                self.Message()
            elif f == 2:
                self.Mines.Flag(x, y)
                self.GUI_Refresh(x, y)
                self.Message()

    # have a new game
    def Callback_New_Game(self):
        self.playing_data_labels['Steps'].configure(text='')
        self.playing_data_labels['Mines'].configure(text='')
        self.playing_data_labels['Flags'].configure(text='')
        # re_init opject
        self.Mines = Mine_Map(self.SIZE_X, self.SIZE_Y, self.MINE_NUM)
        # reset panels
        self.Mine_Panel_Setup()
        self.Playing_Data_Panel_Setup()
        self.Control_Panel_Setup()

    # replay game in  the same map
    def Callback_Replay(self):
        # reset object
        self.Mines.Replay()
        # reset panels
        self.Mine_Panel_Setup()
        self.Playing_Data_Panel_Setup()
        self.Control_Panel_Setup()

    def Callback_Quit(self):
        self.gui.destroy()

    # upgrade showing on GUI
    def GUI_Refresh(self, x, y):
        # refresh the grid with operation firstly
        M = self.Mines.Show_Map[x][y]
        self.Button_List[x][y].configure(image=self.images[M])
        # refresh all other grids
        for i in range(self.SIZE_X):
            for j in range(self.SIZE_Y):
                M = self.Mines.Show_Map[i][j]
                self.Button_List[i][j].configure(image=self.images[M])
        self.gui.update_idletasks()

        step_str = 'Steps: ' + str(self.Mines.Steps)
        flag_num = self.Mines.Flag_Num()
        flag_str = 'Flags: ' + str(flag_num)
        mine_str = 'Mines: ' + str(self.MINE_NUM - flag_num)
        print(step_str, '\n', flag_str, '\n', mine_str)

        self.playing_data_labels['Steps'].configure(text=step_str)
        self.playing_data_labels['Mines'].configure(text=mine_str)
        self.playing_data_labels['Flags'].configure(text=flag_str)
        self.gui.update_idletasks()

    # Message box
    def Message(self):
        S = self.Mines.Status
        if S == self.Mines.die:
            messagebox.showerror(title='DIED', message='You are died!!!')

        elif S == self.Mines.win:
            messagebox.showinfo(title='WINNING',
                                message='You are the winner!!!')
            # self.Callback_New_Game()
