import copy
import os
import random
import sys
import unittest

from Mine_Map import Mine_Map

# Adjust recursive tree limits
# default is 1000?
sys.setrecursionlimit(10000)
# block print
sys.stdout = open(os.devnull, 'w')
'''
    unittest for Class Mine_Map
    test:
        win a game
        loss a game
        replay a game
        auto play a game with wrong flags
'''


class Mine_Test(unittest.TestCase):
    SIZE_X = 128
    SIZE_Y = 128
    MINE_NUM_1 = (SIZE_X * SIZE_Y) // 8

    # init map and setup mines
    def setUp(self):
        self.Mines_1 = Mine_Map(self.SIZE_X, self.SIZE_Y, self.MINE_NUM_1)
        x = random.randint(0, self.SIZE_X - 1)
        y = random.randint(0, self.SIZE_Y - 1)
        self.Mines_1.Mines_Setup(x, y)

    # test win the game, flag each mine
    def test_Win_Game(self):
        Mine_List = self.Mines_1.Get_Mine_List()
        for grid in Mine_List:
            x = grid[0]
            y = grid[1]
            self.Mines_1.Flag(x, y)
        status = self.Mines_1.Status
        self.assertEqual(status, self.Mines_1.win)

    # test die in the game, find one mine and click it
    def test_Died_Game(self):
        Mine_List = self.Mines_1.Get_Mine_List()
        L = len(Mine_List)
        Click_Mine = random.randint(0, L - 1)
        for i in range(L):
            grid = Mine_List[i]
            x = grid[0]
            y = grid[1]
            if i != Click_Mine:
                self.Mines_1.Flag(x, y)
            elif i == Click_Mine:
                self.Mines_1.Click(x, y)
        status = self.Mines_1.Status
        self.assertEqual(status, self.Mines_1.die)

    # test replay the game
    def test_Replay_Map(self):
        # record old map
        Old_Map = self.Mines_1.Get_Data_Map()
        Mine_List = self.Mines_1.Get_Mine_List()
        # click mine and died
        x = (Mine_List[0])[0]
        y = (Mine_List[0])[1]
        self.Mines_1.Click(x, y)
        Old_status = self.Mines_1.Status
        self.Mines_1.Replay()
        New_Map = self.Mines_1.Get_Data_Map()
        New_status = self.Mines_1.Status
        # whether the map is same
        self.assertEqual(Old_Map, New_Map)
        # status test
        self.assertEqual(Old_status, self.Mines_1.die)
        self.assertEqual(New_status, self.Mines_1.alive)

    def test_Auto_Play(self):
        gird_list = []

        while len(gird_list) < self.MINE_NUM_1:
            x = random.randint(0, self.SIZE_X - 1)
            y = random.randint(0, self.SIZE_Y - 1)
            gird_list.append([x, y])
            self.Mines_1.Flag(x, y)

        # DO NOT USE '=', it's reference not copy
        new_Mine = copy.deepcopy(self.Mines_1)
        # Get operate list from a new object
        Operate_List = new_Mine.Auto_Play()
        new_Mine_status = new_Mine.Status
        # finish operates
        for op in Operate_List:
            x = op[0]
            y = op[1]
            f = op[2]
            if f == 1:
                if self.Mines_1.Show_Map[x][y] == self.Mines_1.Unknown_Grid:
                    self.Mines_1.Click(x, y)
            elif f == 2:
                self.Mines_1.Flag(x, y)
        status = self.Mines_1.Status
        self.assertEqual(status, self.Mines_1.win)
        self.assertEqual(new_Mine_status, new_Mine.win)


if __name__ == "__main__":
    unittest.main(verbosity=2)
