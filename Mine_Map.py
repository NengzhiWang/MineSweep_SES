import random


class Mine_Map:
    def __init__(self, x, y, n):
        '''
        init
            generate 2-D lists for Mine data
            Data in the 2-D lists
        '''
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
        # Mine_Map: location of mines
        #   1 for mine
        #   0 for empty
        self.__Mine_Map = [[0 for i in range(self.SIZE_Y)]
                           for i in range(self.SIZE_X)]

        # Flag_Map: location of flags
        #   1 for flag
        #   0 for empty
        self.__Flag_Map = [[0 for i in range(self.SIZE_Y)]
                           for i in range(self.SIZE_X)]

        # Data_Map: data in each grid
        #   'M' for mine
        #   str(int) for number of mines nearby
        self.__Data_Map = [[0 for i in range(self.SIZE_Y)]
                           for i in range(self.SIZE_X)]

        # Show_Map: figure shown in GUI
        self.Show_Map = [[self.Unknown_Grid for i in range(self.SIZE_Y)]
                         for i in range(self.SIZE_X)]

        self.Status = self.inited
        self.__Mine_List = []
        # self.__Flag_List = []
        self.Steps = 0

    def Mines_Setup(self, x, y):
        '''
        setup Mines with first click at [x, y]
        have a save zone of # 8-nearby and [x, y] itself
        '''
        print('first click at (%d,%d)' % (x, y))
        self.Status = self.alive

        self.__init_grid = [x, y]
        Save_Zone = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                Save_Zone.append([x + dx, y + dy])
        # random set mine
        # grid (x,y) is not available for a mine
        # grid point have most 1 mine
        while len(self.__Mine_List) < self.MINE_NUM:
            random_x = random.randint(0, self.SIZE_X - 1)
            random_y = random.randint(0, self.SIZE_Y - 1)
            grid = [random_x, random_y]
            # the grid first clicked must not a mine
            # one mine in one grid
            if grid not in Save_Zone and grid not in self.__Mine_List:
                self.__Mine_List.append(grid)
                self.__Mine_Map[random_x][random_y] = 1
        self.__Map_Setup()
        self.Click(x, y)

    def __Map_Setup(self):
        '''
        private function
        upgrade the full map
        for each empty grid, it shows the number of mines in 8 nearby grids
        '''
        for x_i in range(self.SIZE_X):
            for y_i in range(self.SIZE_Y):
                if self.__Mine_Map[x_i][y_i] == 0:
                    total_mine = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            px = x_i + dx
                            py = y_i + dy
                            inRange_x = (px >= 0 and px < self.SIZE_X)
                            inRange_y = (py >= 0 and py < self.SIZE_Y)
                            if inRange_x and inRange_y:
                                total_mine += self.__Mine_Map[px][py]
                    self.__Data_Map[x_i][y_i] = str(total_mine)
                else:
                    self.__Data_Map[x_i][y_i] = 'M'
        self.Print_Mines()

    def Click(self, x, y):
        '''
        Click at grid [x, y]
        '''
        if self.Status == self.alive:
            # can only click a unknown grid
            print('click at grid(%d,%d)' % (x, y))
            self.Steps += 1
            if self.Show_Map[x][y] == self.Unknown_Grid:
                # click a mine, dead !
                if self.__Data_Map[x][y] == 'M':
                    self.Status = self.die
                    print('died')
                    self.__End_Show()
                else:
                    # show new grids recursively
                    self.__Show_Upgrade(x, y)

    def Quick_Click(self, x, y):
        '''
        quick click all 8 nearby grids
        need: flags nearby = mines nearby
        '''
        if self.Status == self.alive:
            NearbyFlag = str(self.NearbyFlag_Num(x, y))
            if NearbyFlag == self.Show_Map[x][y]:
                self.Steps += 1
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        px = x + dx
                        py = y + dy
                        inRange_x = (px >= 0 and px < self.SIZE_X)
                        inRange_y = (py >= 0 and py < self.SIZE_Y)
                        if inRange_x and inRange_y:
                            # if self.Show_Map[px][py] == self.Unknown_Grid:
                            if self.is_Unknown(px, py):
                                if self.__Data_Map[px][py] == 'M':
                                    self.Status = self.die
                                    print('died')
                                    self.__End_Show()
                                else:
                                    D = self.__Data_Map[px][py]
                                    self.Show_Map[px][py] = D

    def __Show_Upgrade(self, x, y):
        '''
        private function
        upgrade Show_Map
        '''
        # recursive termination
        # out the range
        if x < 0 or x >= self.SIZE_X:
            return
        if y < 0 or y >= self.SIZE_Y:
            return
        # find a mine
        if self.__Data_Map[x][y] == 'M':
            return
        # find shown grid
        if self.Show_Map[x][y] != self.Unknown_Grid:
            return

        else:
            if self.__Data_Map[x][y] != '0':
                # mine nearby, only upgrade this grid, no recursive
                self.Show_Map[x][y] = self.__Data_Map[x][y]
            elif self.__Data_Map[x][y] == '0':
                # no mine nearby, upgrade this grid and 8 nearby grids
                self.Show_Map[x][y] = self.__Data_Map[x][y]
                # 4 nearby
                self.__Show_Upgrade(x - 1, y)
                self.__Show_Upgrade(x + 1, y)
                self.__Show_Upgrade(x, y - 1)
                self.__Show_Upgrade(x, y + 1)
                # 8 nearby
                self.__Show_Upgrade(x + 1, y + 1)
                self.__Show_Upgrade(x - 1, y + 1)
                self.__Show_Upgrade(x - 1, y - 1)
                self.__Show_Upgrade(x + 1, y - 1)

    def Flag(self, x, y):
        '''
        flag or unflag in a grid
        '''
        if self.Status == self.alive:
            # upgrade the show map with flags
            S = self.Show_Map[x][y]
            # can only flag an unknown grid or disflag a flagged grid
            if S != self.Flagged_Grid and S != self.Unknown_Grid:
                return
            else:
                print('flag at grid(%d,%d)' % (x, y))
                self.Steps += 1

                if self.__Flag_Map[x][y] == 0:
                    # flag
                    self.__Flag_Map[x][y] = 1
                    self.Show_Map[x][y] = self.Flagged_Grid
                    # self.__Flag_List.append([x, y])
                elif self.__Flag_Map[x][y] == 1:
                    # disflag
                    self.__Flag_Map[x][y] = 0
                    self.Show_Map[x][y] = self.Unknown_Grid
                    # self.__Flag_List.remove([x, y])

                if self.__Flag_Map == self.__Mine_Map:
                    # Flagged all mines, you self.win !
                    self.Status = self.win
                    print('win')
                    self.__End_Show()

    def __Expand(self, x, y, operate_list):
        '''
        private function
        click all nearby no-mine grid
        '''
        if self.Steps != 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    px = x + dx
                    py = y + dy
                    inRange_x = (px >= 0 and px < self.SIZE_X)
                    inRange_y = (py >= 0 and py < self.SIZE_Y)
                    if inRange_x and inRange_y:
                        if [px, py] not in self.__Mine_List:
                            if self.Show_Map[px][py] != '0':
                                self.Click(px, py)
                                operate_list.append([px, py])

    def Auto_Play(self):
        '''
        auto_play
        return a list of operations
        this method need the grids of mine
        '''
        Operate_List = []
        if self.Status == self.alive:
            # remove all flags in the map
            for each_flag in self.Get_Flag_List():
                x = each_flag[0]
                y = each_flag[1]
                self.Flag(x, y)
                Operate_List.append([x, y, 2])

            Total_Grid = self.SIZE_X * self.SIZE_Y
            operate_list_cache_1 = []
            operate_list_cache_2 = []
            # Click not mine grid, until all no mine grid is known
            # record operations in List
            while len(self.__Get_Known_Grids()) < Total_Grid - self.MINE_NUM:
                Known_List = self.__Get_Known_Grids()
                for x in range(self.SIZE_X):
                    for y in range(self.SIZE_Y):
                        grid = [x, y]
                        not_mine = grid not in self.__Mine_List
                        is_known = grid in Known_List
                        not_operate = [x, y] not in operate_list_cache_1
                        not_0 = (self.Show_Map[x][y] != '0')
                        if not_mine and is_known and not_operate and not_0:
                            self.__Expand(x, y, operate_list_cache_2)
                            operate_list_cache_1.append([x, y])

            # Remove repeat clicks in List
            for op in operate_list_cache_2:
                x = op[0]
                y = op[1]
                if [x, y] not in self.__Mine_List:
                    if [x, y, 1] not in Operate_List:
                        Operate_List.append([x, y, 1])
            # Flag mines
            for x in range(self.SIZE_X):
                for y in range(self.SIZE_Y):
                    grid = [x, y]
                    # Flag_list = self.Get_Flag_List()
                    if grid in self.__Mine_List:
                        if grid not in self.Get_Flag_List():
                            self.Flag(x, y)
                            Operate_List.append([x, y, 2])

        return Operate_List

    def Replay(self):
        '''
        replay game
        reset Flag_Map and Show_Map
        '''
        if self.Steps != 0:
            for i in range(self.SIZE_X):
                for j in range(self.SIZE_Y):
                    self.__Flag_Map[i][j] = 0
                    self.Show_Map[i][j] = self.Unknown_Grid
                    self.Steps = 0
                    self.Status = self.alive

    def __End_Show(self):
        '''
        change the data shown in UI when died or win
        '''
        if self.Status == self.die:
            for x_i in range(self.SIZE_X):
                for y_i in range(self.SIZE_Y):
                    isFlag = self.__Flag_Map[x_i][y_i]
                    isMine = self.__Mine_Map[x_i][y_i]
                    if isFlag == 0 and isMine == 0:
                        # no flag, no mine
                        self.Show_Map[x_i][y_i] = self.__Data_Map[x_i][y_i]
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
                    isFlag = self.__Flag_Map[x_i][y_i]
                    if isFlag == 1:
                        # have flag and mine
                        self.Show_Map[x_i][y_i] = self.Flagged_Mine
                    else:
                        # no flag and mine
                        self.Show_Map[x_i][y_i] = self.__Data_Map[x_i][y_i]

    def Disp_All(self):
        '''
        print all data of gird
        '''
        for x in range(self.SIZE_X):
            for y in range(self.SIZE_Y):
                D = self.__Data_Map[x][y]
                print(D, end=' ')

            print(' ')
        print('\n')

    def Disp_UI(self):
        '''
        print Show_Map
        '''
        for x in range(self.SIZE_X):
            for y in range(self.SIZE_Y):
                D = self.Show_Map[x][y]
                print(D, end=' ')

            print(' ')
        print('\n')

    def Print_Mines(self):
        '''
        print the grids of mines
        '''
        for i in range(len(self.__Mine_List)):
            mine = self.__Mine_List[i]
            x = mine[0]
            y = mine[1]
            print('%d \t Mine at (%d,%d)' % (i + 1, x, y))

    def Get_Flag_List(self):
        '''
        return the grids with flag
        '''
        flag_list = []
        for i in range(self.SIZE_X):
            for j in range(self.SIZE_Y):
                if self.__Flag_Map[i][j] == 1:
                    flag_list.append([i, j])
        return flag_list

    def Flag_Num(self):
        '''
        return the number of flags
        '''
        return len(self.Get_Flag_List())

    def __Get_Known_Grids(self):
        '''
        return the grids of NOT_unknow
        '''
        Grid_List = []
        for i in range(self.SIZE_X):
            for j in range(self.SIZE_Y):
                grid = [i, j]
                D = self.Show_Map[i][j]
                if D != self.Unknown_Grid:
                    Grid_List.append(grid)
        return Grid_List

    def NearbyFlag_Num(self, x, y):
        '''
        return the number of flags in 8 nearby
        '''
        NearbyFlags = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                px = x + dx
                py = y + dy
                inRange_x = (px >= 0 and px < self.SIZE_X)
                inRange_y = (py >= 0 and py < self.SIZE_Y)
                if inRange_x and inRange_y:
                    NearbyFlags += self.__Flag_Map[px][py]
        return NearbyFlags

    def Nearby_Unknow_Num(self, x, y):
        '''
        return the number of unknow grids in 8 nearby
        '''
        Nearby_Unknow = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                px = x + dx
                py = y + dy
                inRange_x = (px >= 0 and px < self.SIZE_X)
                inRange_y = (py >= 0 and py < self.SIZE_Y)
                if inRange_x and inRange_y:
                    if self.is_Unknown(x, y):
                        Nearby_Unknow += 1
        return Nearby_Unknow

    def is_Unknown(self, x, y):
        '''
        return whether grid [x, y] is unknow
        '''
        grid_data = self.Show_Map[x][y]
        return (grid_data == self.Unknown_Grid)

    def Get_Data_Map(self):
        return self.__Data_Map

    def Get_Mine_List(self):
        return self.__Mine_List
