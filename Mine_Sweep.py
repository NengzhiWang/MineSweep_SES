from config import *
import random


class Mine_Map:
    # Mine_Map: location of mines
    #   1 for mine
    #   0 for empty

    # Flag_Map: location of flags
    #   1 for flag
    #   0 for empty

    # Data_Map: data in each grid
    #   'M' for mine
    #   str(int) for number of mines nearby
    # Show_Map: figure shown in GUI

    # Status:
    #   '0' not init
    #   '1' playing
    #   '2' win
    #   '3' dead

    Mine_Map = [[0 for i in range(SIZE_X)] for i in range(SIZE_Y)]
    Flag_Map = [[0 for i in range(SIZE_X)] for i in range(SIZE_Y)]

    Data_Map = [[0 for i in range(SIZE_X)] for i in range(SIZE_Y)]
    Show_Map = [[Unknown_Grid for i in range(SIZE_X)] for i in range(SIZE_Y)]
    Status = '0'

    # init the map with the first click at grid (x,y)
    def __init__(self, x, y):
        self.Status = '1'

        init_pos = x * SIZE_X + y
        Mine_List = []
        # random set mine
        # grid (x,y) is not available for a mine
        # grid point have most 1 mine
        while len(Mine_List) < MINE_NUM:
            random_pos = random.sample(range(SIZE_X * SIZE_Y), 1)[0]

            if (random_pos is not init_pos) and (random_pos not in Mine_List):
                Mine_List.append(random_pos)
                self.Mine_Map[random_pos // SIZE_X][random_pos % SIZE_X] = 1

        # upgrade the full map
        # for each empty grid, it shows the number of mines in 8 nearby grids
        for x_i in range(SIZE_X):
            for y_i in range(SIZE_Y):
                if self.Mine_Map[x_i][y_i] == 0:
                    total_mine = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            px = x_i + dx
                            py = y_i + dy
                            inRange_x = (px >= 0 and px < SIZE_X)
                            inRange_y = (py >= 0 and py < SIZE_Y)
                            if inRange_x and inRange_y:
                                total_mine += self.Mine_Map[px][py]
                    self.Data_Map[x_i][y_i] = str(total_mine)
                else:
                    self.Data_Map[x_i][y_i] = 'M'

        self.Click(x, y)

    def Click(self, x, y):
        # can only click a unknown grid
        print('click at grid(%d,%d)' % (x, y))
        if self.Show_Map[x][y] == Unknown_Grid:
            # click a mine, dead !
            if self.Data_Map[x][y] == 'M':
                self.Status == '3'
                print('died')
                self.Died_Show()
            else:
                # expand the displayed range recursively
                self.Show_Upgrade(x, y)

    def Show_Upgrade(self, x, y):
        # recursive termination
        # out the range
        if x < 0 or x >= SIZE_X:
            return
        if y < 0 or y >= SIZE_Y:
            return
        # find a mine
        if self.Data_Map[x][y] == 'M':
            return
        # find shown grid
        if self.Show_Map[x][y] != Unknown_Grid:
            return

        else:
            if self.Data_Map[x][y] != '0':
                # mine nearby, only upgrade this grid, no recursive
                self.Show_Map[x][y] = self.Data_Map[x][y]
            elif self.Data_Map[x][y] == '0':
                # no mine nearby, upgrade this grid and 8 nearbu grids
                self.Show_Map[x][y] = self.Data_Map[x][y]
                # 4 nearby
                self.Show_Upgrade(x - 1, y)
                self.Show_Upgrade(x + 1, y)
                self.Show_Upgrade(x, y - 1)
                self.Show_Upgrade(x, y + 1)
                # 8 nearby
                self.Show_Upgrade(x + 1, y + 1)
                self.Show_Upgrade(x - 1, y + 1)
                self.Show_Upgrade(x, y + 1)
                self.Show_Upgrade(x, y - 1)

    def Flag(self, x, y):
        # upgrade the show map with flags
        S = self.Show_Map[x][y]
        # can only flag an unknown grid or disflag a flagged grid
        if S != Flagged_Grid and S != Unknown_Grid:
            return
        else:
            print('flag at grid(%d,%d)' % (x, y))
            if self.Flag_Map[x][y] == 0:
                # flag
                self.Flag_Map[x][y] = 1
                self.Show_Map[x][y] = Flagged_Grid

            elif self.Flag_Map[x][y] == 1:
                # disflag
                self.Flag_Map[x][y] = 0
                self.Show_Map[x][y] = Unknown_Grid

            if self.Flag_Map == self.Mine_Map:
                # Flagged all mines, you win !
                self.Status = '2'
                print('win')
                self.Win_Show()

    def Died_Show(self):
        # died, upgrade the Show_Map
        self.Status = '3'
        for x_i in range(SIZE_X):
            for y_i in range(SIZE_Y):
                isFlag = self.Flag_Map[x_i][y_i]
                isMine = self.Mine_Map[x_i][y_i]
                if isFlag == 0 and isMine == 0:
                    # no flag, no mine
                    self.Show_Map[x_i][y_i] = self.Data_Map[x_i][y_i]
                elif isFlag == 1 and isMine == 0:
                    # have flag, no mine
                    self.Show_Map[x_i][y_i] = UnMined_Flag
                elif isFlag == 0 and isMine == 1:
                    # no flag, have mine
                    self.Show_Map[x_i][y_i] = Unflagg_Mine
                elif isFlag == 1 and isMine == 1:
                    # have flag, have mine
                    self.Show_Map[x_i][y_i] = Flagged_Mine

    def Win_Show(self):
        self.Status = '2'
        for x_i in range(SIZE_X):
            for y_i in range(SIZE_Y):
                isFlag = self.Flag_Map[x_i][y_i]
                if isFlag == 1:
                    # have flag and mine
                    self.Show_Map[x_i][y_i] = Flagged_Mine
                else:
                    # no flag and mine
                    self.Show_Map[x_i][y_i] = self.Data_Map[x_i][y_i]

    def Disp_All(self):
        # print all data of gird
        for x in range(SIZE_X):
            for y in range(SIZE_Y):
                M = self.Mine_Map[x][y]
                D = self.Data_Map[x][y]

                if M == 1:
                    Out = '■'
                else:
                    if D == '0':
                        Out = '□'
                    else:
                        Out = D

                print(Out, end=' ')
            print(' ')
        print('\n')

    def Disp_UI(self):
        for x in range(SIZE_X):
            for y in range(SIZE_Y):
                D = self.Show_Map[x][y]
                print(D, end=' ')

            print(' ')
        print('\n')

    def Print_Mines(self):
        # print the grid with mine
        Mine_List = []
        for x_i in range(SIZE_X):
            for y_i in range(SIZE_Y):
                if self.Mine_Map[x_i][y_i] == 1:
                    Mine_List.append([x_i, y_i])

        for mine in Mine_List:
            x = mine[0]
            y = mine[1]
            print('Mine at (%d,%d)' % (x, y))
