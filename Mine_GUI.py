import copy
import tkinter as tk
from tkinter import messagebox

from Mine_Map import Mine_Map


class Mine_GUI(Mine_Map):
    def __init__(self, gui, x, y, n):
        '''
        init GUI
            title
            size and resizeable NOT
            object from class Mine_Map
            load images
            setup panels
        '''
        self.__gui = gui
        # GUI title
        self.__gui.title('MineSweep SES')
        # Cannot resize
        self.__gui.resizable(0, 0)
        # import images and load into dict
        # init object of Mine_Map
        self.__SIZE_X = x
        self.__SIZE_Y = y
        self.__MINE_NUM = n
        self.__Mines = Mine_Map(self.__SIZE_X, self.__SIZE_Y, self.__MINE_NUM)
        self.__images = {
            self.__Mines.Unknown_Grid:
            tk.PhotoImage(file='./Image/tile_unknown.gif'),
            self.__Mines.Unflagg_Mine:
            tk.PhotoImage(file='./Image/tile_mine.gif'),
            self.__Mines.Flagged_Grid:
            tk.PhotoImage(file='./Image/tile_flag.gif'),
            self.__Mines.UnMined_Flag:
            tk.PhotoImage(file='./Image/tile_wrong.gif'),
            self.__Mines.Flagged_Mine:
            tk.PhotoImage(file='./Image/tile_right.gif'),
            '0':
            tk.PhotoImage(file='./Image/tile_0.gif'),
            '1':
            tk.PhotoImage(file='./Image/tile_1.gif'),
            '2':
            tk.PhotoImage(file='./Image/tile_2.gif'),
            '3':
            tk.PhotoImage(file='./Image/tile_3.gif'),
            '4':
            tk.PhotoImage(file='./Image/tile_4.gif'),
            '5':
            tk.PhotoImage(file='./Image/tile_5.gif'),
            '6':
            tk.PhotoImage(file='./Image/tile_6.gif'),
            '7':
            tk.PhotoImage(file='./Image/tile_7.gif'),
            '8':
            tk.PhotoImage(file='./Image/tile_8.gif')
        }
        self.__GUI_Show_Data = False
        # setup panels of GUI
        self.__Playing_Data_Panel_Setup()
        self.__Control_Panel_Setup()
        self.__Mine_Panel_Setup()

    def __Mine_Panel_Setup(self):
        '''
        private function
        set Mine Panel in the GUI
        This panel are tk.Button array, each one have 3 binded event
            Left Click
            Right Click (also Middle Click on Windows)
            Enter the Button
        '''
        # init grids as tkinter.button
        self.__Mine_Button_List = [[
            tk.Button(self.__gui,
                      image=self.__images[self.__Mines.Unknown_Grid])
            for i in range(self.__SIZE_Y)
        ] for j in range(self.__SIZE_X)]

        for x in range(self.__SIZE_X):
            for y in range(self.__SIZE_Y):
                # bind the click of each button to their event function
                # use lambda to send arguments for event function

                # left click
                self.__Mine_Button_List[x][y].bind(
                    '<Button-1>',
                    lambda event, a=x, b=y: self.__Callback_Left(a, b))

                # right or middle click
                # Button-2
                #   Win and Linux: Middle
                #   MacOS:  Right
                self.__Mine_Button_List[x][y].bind(
                    '<Button-2>',
                    lambda event, a=x, b=y: self.__Callback_Right(a, b))
                self.__Mine_Button_List[x][y].bind(
                    '<Button-3>',
                    lambda event, a=x, b=y: self.__Callback_Right(a, b))

                # enter grid
                self.__Mine_Button_List[x][y].bind(
                    '<Enter>',
                    lambda event, a=x, b=y: self.__Callback_Enter(a, b))
                # show each button on GUI
                self.__Mine_Button_List[x][y].grid(row=x, column=y)

        self.Steps = 0
        self.__gui.update_idletasks()

    def __Playing_Data_Panel_Setup(self):
        '''
        private function
        show playing data
            Steps
            Mines
            Flags
            Data of the Grid your mouse enter
        '''
        self.__playing_data_labels = {
            'Steps': tk.Label(self.__gui, text='Steps: 0'),
            'Mines': tk.Label(self.__gui, text='Mines: 0'),
            'Flags': tk.Label(self.__gui, text='Flags: 0'),
            'Row': tk.Label(self.__gui, text='Row: ' + str(self.__SIZE_X)),
            'Col': tk.Label(self.__gui, text='Col: ' + str(self.__SIZE_Y)),
            'Data': tk.Label(self.__gui, text='')
        }

        self.__playing_data_labels['Steps'].grid(row=self.__SIZE_X + 1,
                                                 column=0,
                                                 columnspan=self.__SIZE_Y // 3)
        self.__playing_data_labels['Mines'].grid(row=self.__SIZE_X + 1,
                                                 column=self.__SIZE_Y // 3,
                                                 columnspan=self.__SIZE_Y // 3)
        self.__playing_data_labels['Flags'].grid(row=self.__SIZE_X + 1,
                                                 column=2 * self.__SIZE_Y // 3,
                                                 columnspan=self.__SIZE_Y // 3)
        self.__playing_data_labels['Row'].grid(row=self.__SIZE_X + 2,
                                               column=0,
                                               columnspan=self.__SIZE_Y // 3)
        self.__playing_data_labels['Col'].grid(row=self.__SIZE_X + 2,
                                               column=self.__SIZE_Y // 3,
                                               columnspan=self.__SIZE_Y // 3)
        self.__playing_data_labels['Data'].grid(row=self.__SIZE_X + 2,
                                                column=2 * self.__SIZE_Y // 3,
                                                columnspan=self.__SIZE_Y // 3)
        self.__gui.update_idletasks()

    def __Control_Panel_Setup(self):
        '''
        private function
        Control the Game
            Have a new game(in a new map)
            Replay this game(in the same map)
            Let Computer auto play the game
            Show what the grid is on GUI
            Quit the game
        '''
        self.__control_buttons = {
            'new_game': tk.Button(self.__gui, text='New Game'),
            'replay': tk.Button(self.__gui, text='Replay'),
            'auto_play': tk.Button(self.__gui, text='Auto Play'),
            'guide': tk.Button(self.__gui, text='GUIDE'),
            'cheat': tk.Button(self.__gui, text='CHEAT'),
            'quit': tk.Button(self.__gui, text='QUIT')
        }

        self.__control_buttons['new_game'].bind(
            '<Button-1>', lambda event: self.__Callback_New_Game())
        self.__control_buttons['replay'].bind(
            '<Button-1>', lambda event: self.__Callback_Replay())
        self.__control_buttons['auto_play'].bind(
            '<Button-1>', lambda event: self.__Callback_Auto_Play())
        self.__control_buttons['guide'].bind(
            '<Button-1>', lambda event: self.__Callback_Guide())
        self.__control_buttons['cheat'].bind(
            '<Button-1>', lambda event: self.__Callback_Cheat())
        self.__control_buttons['quit'].bind(
            '<Button-1>', lambda event: self.__Callback_Quit())

        self.__control_buttons['new_game'].grid(row=self.__SIZE_X + 3,
                                                column=0,
                                                columnspan=self.__SIZE_Y // 3)
        self.__control_buttons['replay'].grid(row=self.__SIZE_X + 3,
                                              column=self.__SIZE_Y // 3,
                                              columnspan=self.__SIZE_Y // 3)
        self.__control_buttons['auto_play'].grid(row=self.__SIZE_X + 3,
                                                 column=2 * self.__SIZE_Y // 3,
                                                 columnspan=self.__SIZE_Y // 3)
        self.__control_buttons['guide'].grid(row=self.__SIZE_X + 4,
                                             column=0,
                                             columnspan=self.__SIZE_Y // 3)
        self.__control_buttons['cheat'].grid(row=self.__SIZE_X + 4,
                                             column=self.__SIZE_Y // 3,
                                             columnspan=self.__SIZE_Y // 3)
        self.__control_buttons['quit'].grid(row=self.__SIZE_X + 4,
                                            column=2 * self.__SIZE_Y // 3,
                                            columnspan=self.__SIZE_Y // 3)

        self.__gui.update_idletasks()

    def __Callback_Left(self, x, y):
        '''
        private function
        event function of left button click a mine
            setup mines
            click the grid
        '''
        # step 1, setup mines
        if self.__Mines.Steps == 0:
            print('Game Start')
            print('init your game at (%d,%d)' % (x, y))
            # init an object from class Mine_Map
            self.__Mines.Mines_Setup(x, y)
            # Refresh GUI
            self.__GUI_Refresh(x, y)

        else:
            # click grid
            if self.__Mines.is_Unknown(x, y):
                # Use function from object Mines
                self.__Mines.Click(x, y)
            else:
                self.__Mines.Quick_Click(x, y)
            # Refresh GUI
            self.__GUI_Refresh(x, y)

    def __Callback_Right(self, x, y):
        '''
        private function
        event function of right button click a mine
            setup mines
            flag the grid
        '''
        if self.__Mines.Steps == 0:
            # step 1, setup mines
            print('Game Start')
            print('init your game at (%d,%d)' % (x, y))
            self.__Mines.Mines_Setup(x, y)
            self.__GUI_Refresh(x, y)
        else:
            # flag and unflag
            self.__Mines.Flag(x, y)
            self.__GUI_Refresh(x, y)

    def __Callback_Enter(self, x, y):
        '''
        private function
        event function of enter a grid
            show the row and column number
            show the data of this grid
        '''
        row_str = 'Row: ' + str(x)
        col_str = 'Col: ' + str(y)
        self.__playing_data_labels['Row'].configure(text=row_str)
        self.__playing_data_labels['Col'].configure(text=col_str)
        if self.__GUI_Show_Data:
            self.__playing_data_labels['Data'].configure(
                text=self.__Mines.Get_Data_Map()[x][y])
        else:
            self.__playing_data_labels['Data'].configure(text='')

        self.__gui.update_idletasks()

    # auto play
    def __Callback_Auto_Play(self):
        '''
        private function
        finish this game by computer
        '''
        # copy a Mine_Map
        # DO NOT USE '=', it's reference not copy
        new_Mine = copy.deepcopy(self.__Mines)

        # finish and record how to play in the new Mine_Map
        Operate_List = new_Mine.Auto_Play()

        # using the record oprations, finish this game
        # showing on the GUI step by step
        for op in Operate_List:
            x = op[0]
            y = op[1]
            f = op[2]
            if f == 1:
                if self.__Mines.Show_Map[x][y] == self.__Mines.Unknown_Grid:
                    self.__Mines.Click(x, y)
                    # time.sleep(0.25)
            elif f == 2:
                self.__Mines.Flag(x, y)
            self.__GUI_Refresh(x, y)

    def __Callback_Cheat(self):
        '''
        private function
        show data on GUI or NOT
        '''
        self.__GUI_Show_Data = not self.__GUI_Show_Data

    # have a new game
    def __Callback_New_Game(self):
        '''
        private function
        have a new game
        '''
        # refresh the data panel
        self.__playing_data_labels['Steps'].configure(text='')
        self.__playing_data_labels['Mines'].configure(text='')
        self.__playing_data_labels['Flags'].configure(text='')
        # re_init opject
        self.__Mines = Mine_Map(self.__SIZE_X, self.__SIZE_Y, self.__MINE_NUM)
        # reset panels
        self.__Mine_Panel_Setup()
        self.__Playing_Data_Panel_Setup()
        self.__Control_Panel_Setup()

    # replay game in  the same map
    def __Callback_Replay(self):
        '''
        private function
        play in the same map again
        '''
        # reset object
        self.__Mines.Replay()
        # reset panels
        self.__Mine_Panel_Setup()
        self.__Playing_Data_Panel_Setup()
        self.__Control_Panel_Setup()

    def __Callback_Quit(self):
        '''
        private function
        quit this game
        '''
        self.__gui.destroy()

    # upgrade showing on GUI
    def __GUI_Refresh(self, x, y):
        '''
        private function
        refresh the GUI
        '''
        # refresh the grid with operation firstly
        M = self.__Mines.Show_Map[x][y]
        self.__Mine_Button_List[x][y].configure(image=self.__images[M])
        # refresh all other grids
        for i in range(self.__SIZE_X):
            for j in range(self.__SIZE_Y):
                M = self.__Mines.Show_Map[i][j]
                self.__Mine_Button_List[i][j].configure(image=self.__images[M])

        # refresh data panel
        step_str = 'Steps: ' + str(self.__Mines.Steps)
        flag_num = self.__Mines.Flag_Num()
        flag_str = 'Flags: ' + str(flag_num)
        mine_str = 'Mines: ' + str(self.__MINE_NUM - flag_num)
        print(step_str, '\n', flag_str, '\n', mine_str)

        self.__playing_data_labels['Steps'].configure(text=step_str)
        self.__playing_data_labels['Mines'].configure(text=mine_str)
        self.__playing_data_labels['Flags'].configure(text=flag_str)
        self.__gui.update()
        self.__Message()

    def __Callback_Guide(self):
        title = 'User Guide'
        f = open('./User_Guide.txt', encoding='UTF-8')
        message = f.read()

        messagebox.showinfo(title=title, message=message)
        self.__Control_Panel_Setup()

    # Message box
    def __Message(self):
        '''
        private function
        message bow of win or die
        '''
        S = self.__Mines.Status
        if S == self.__Mines.die:
            messagebox.showerror(title='DIED', message='You are died!!!')

        elif S == self.__Mines.win:
            messagebox.showinfo(title='WINNING',
                                message='You are the winner!!!')
            self.__Callback_New_Game()
