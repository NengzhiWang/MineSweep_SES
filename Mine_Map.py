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
    #   '2' self.win
    #   '3' dead

    # init the map with the first click at grid (x,y)
    def __init__(self, x, y, n):
        self.SIZE_X = x
        self.SIZE_Y = y
        self.MINE_NUM = n

        self.Unknown_Grid = '□'
        self.Flagged_Grid = 'F'
        self.Unflagg_Mine = '*'
        self.UnMined_Flag = 'X'
        self.Flagged_Mine = '√'

        self.inited = 'a'
        self.alive = 'b'
        self.win = 'c'
        self.die = 'd'

        self.Mine_Map = [[0 for i in range(self.SIZE_Y)]
                         for i in range(self.SIZE_X)]
        self.Flag_Map = [[0 for i in range(self.SIZE_Y)]
                         for i in range(self.SIZE_X)]
        self.Data_Map = [[0 for i in range(self.SIZE_Y)]
                         for i in range(self.SIZE_X)]
        self.Show_Map = [[self.Unknown_Grid for i in range(self.SIZE_Y)]
                         for i in range(self.SIZE_X)]

        self.Status = self.inited
        self.Mine_List = []
        self.Steps = 0

    def Mines_Setup(self, x, y):
        print('first click at (%d,%d)' % (x, y))
        self.Status = self.alive

        init_grid = [x, y]
        # random set mine
        # grid (x,y) is not available for a mine
        # grid point have most 1 mine
        while len(self.Mine_List) < self.MINE_NUM:
            random_x = random.randint(0, self.SIZE_X - 1)
            random_y = random.randint(0, self.SIZE_Y - 1)
            random_grid = [random_x, random_y]
            # the grid first clicked must not a mine
            # one mine in one grid
            if random_grid != init_grid and random_grid not in self.Mine_List:
                self.Mine_List.append(random_grid)
                self.Mine_Map[random_x][random_y] = 1

        # upgrade the full map
        # for each empty grid, it shows the number of mines in 8 nearby grids
        for x_i in range(self.SIZE_X):
            for y_i in range(self.SIZE_Y):
                if self.Mine_Map[x_i][y_i] == 0:
                    total_mine = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            px = x_i + dx
                            py = y_i + dy
                            inRange_x = (px >= 0 and px < self.SIZE_X)
                            inRange_y = (py >= 0 and py < self.SIZE_Y)
                            if inRange_x and inRange_y:
                                total_mine += self.Mine_Map[px][py]
                    self.Data_Map[x_i][y_i] = str(total_mine)
                else:
                    self.Data_Map[x_i][y_i] = 'M'
        # print(len(self.Mine_List))
        self.Print_Mines()
        self.Click(x, y)

    def Click(self, x, y):
        if self.Status == self.alive:
            # can only click a unknown grid
            print('click at grid(%d,%d)' % (x, y))
            self.Steps += 1
            if self.Show_Map[x][y] == self.Unknown_Grid:
                # click a mine, dead !
                if self.Data_Map[x][y] == 'M':
                    self.Status = self.die
                    print('died')
                    self.End_Show()
                else:
                    # expand the displayed range recursively
                    self.Show_Upgrade(x, y)

    def Show_Upgrade(self, x, y):
        # recursive termination
        # out the range
        if x < 0 or x >= self.SIZE_X:
            return
        if y < 0 or y >= self.SIZE_Y:
            return
        # find a mine
        if self.Data_Map[x][y] == 'M':
            return
        # find shown grid
        if self.Show_Map[x][y] != self.Unknown_Grid:
            return

        else:
            if self.Data_Map[x][y] != '0':
                # mine nearby, only upgrade this grid, no recursive
                self.Show_Map[x][y] = self.Data_Map[x][y]
            elif self.Data_Map[x][y] == '0':
                # no mine nearby, upgrade this grid and 8 nearby grids
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
        if self.Status == self.alive:
            # upgrade the show map with flags
            S = self.Show_Map[x][y]
            # can only flag an unknown grid or disflag a flagged grid
            if S != self.Flagged_Grid and S != self.Unknown_Grid:
                return
            else:
                print('flag at grid(%d,%d)' % (x, y))
                self.Steps += 1

                if self.Flag_Map[x][y] == 0:
                    # flag
                    self.Flag_Map[x][y] = 1
                    self.Show_Map[x][y] = self.Flagged_Grid

                elif self.Flag_Map[x][y] == 1:
                    # disflag
                    self.Flag_Map[x][y] = 0
                    self.Show_Map[x][y] = self.Unknown_Grid

                if self.Flag_Map == self.Mine_Map:
                    # Flagged all mines, you self.win !
                    self.Status = self.win
                    print('win')
                    self.End_Show()

    def Expand(self, x, y):
        if self.Steps != 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    px = x + dx
                    py = y + dy
                    inRange_x = (px >= 0 and px < self.SIZE_X)
                    inRange_y = (py >= 0 and py < self.SIZE_Y)
                    if inRange_x and inRange_y:
                        if [px, py] not in self.Mine_List:
                            if self.Show_Map[px][py] != '0':
                                self.Click(px, py)

    def Replay(self):
        if self.Steps != 0:
            for i in range(self.SIZE_X):
                for j in range(self.SIZE_Y):
                    self.Flag_Map[i][j] = 0
                    self.Show_Map[i][j] = self.Unknown_Grid
                    self.Steps = 1
                    self.Status = self.alive

    def End_Show(self):
        # self.died, upgrade the Show_Map
        if self.Status == self.die:
            for x_i in range(self.SIZE_X):
                for y_i in range(self.SIZE_Y):
                    isFlag = self.Flag_Map[x_i][y_i]
                    isMine = self.Mine_Map[x_i][y_i]
                    if isFlag == 0 and isMine == 0:
                        # no flag, no mine
                        self.Show_Map[x_i][y_i] = self.Data_Map[x_i][y_i]
                    elif isFlag == 1 and isMine == 0:
                        # have flag, no mine
                        self.Show_Map[x_i][y_i] = self.UnMined_Flag
                    elif isFlag == 0 and isMine == 1:
                        # no flag, have mine
                        self.Show_Map[x_i][y_i] = self.Unflagg_Mine
                    elif isFlag == 1 and isMine == 1:
                        # have flag, have mine
                        self.Show_Map[x_i][y_i] = self.Flagged_Mine
        elif self.Status == self.win:
            for x_i in range(self.SIZE_X):
                for y_i in range(self.SIZE_Y):
                    isFlag = self.Flag_Map[x_i][y_i]
                    if isFlag == 1:
                        # have flag and mine
                        self.Show_Map[x_i][y_i] = self.Flagged_Mine
                    else:
                        # no flag and mine
                        self.Show_Map[x_i][y_i] = self.Data_Map[x_i][y_i]

    def Disp_All(self):
        # print all data of gird
        for x in range(self.SIZE_X):
            for y in range(self.SIZE_Y):
                D = self.Data_Map[x][y]
                print(D, end=' ')

            print(' ')
        print('\n')

    def Disp_UI(self):
        for x in range(self.SIZE_X):
            for y in range(self.SIZE_Y):
                D = self.Show_Map[x][y]
                print(D, end=' ')

            print(' ')
        print('\n')

    def Print_Mines(self):

        for i in range(len(self.Mine_List)):
            mine = self.Mine_List[i]
            x = mine[0]
            y = mine[1]
            print('%d \t Mine at (%d,%d)' % (i + 1, x, y))

    def is_Unknown(self, x, y):
        grid_data = self.Show_Map[x][y]
        return (grid_data == self.Unknown_Grid)

    def Get_Flag_List(self):
        flag_list = []
        for i in range(self.SIZE_X):
            for j in range(self.SIZE_Y):
                if self.Flag_Map[i][j] == 1:
                    flag_list.append([i, j])
        return flag_list

    def Flag_Num(self):
        Flags = 0
        for i in range(self.SIZE_X):
            for j in range(self.SIZE_Y):
                Flags += int(self.Flag_Map[i][j] == 1)
        return Flags

    def Known_Grid(self):
        Grid_List = []
        for i in range(self.SIZE_X):
            for j in range(self.SIZE_Y):
                grid = [i, j]
                D = self.Show_Map[i][j]
                if D not in [
                        self.Unknown_Grid, self.Flagged_Grid,
                        self.UnMined_Flag, self.UnMined_Flag, self.Flagged_Mine
                ]:
                    Grid_List.append(grid)
        return Grid_List
