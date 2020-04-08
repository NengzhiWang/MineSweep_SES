import copy
import random
import sys
import unittest

from Mine_Map import Mine_Map

# Adjust recursive tree limits
# default is 1000?
sys.setrecursionlimit(10000)
'''
    unittest for Class Mine_Map
    test:
        win a game
        loss a game
        replay a game
        auto play a game with wrong flags
'''


class Mine_Test(unittest.TestCase):
    SIZE_X = 256
    SIZE_Y = 256
    MINE_NUM = (SIZE_X * SIZE_Y) // 8

    # init map and setup mines
    def setUp(self):
        self.Mines = Mine_Map(self.SIZE_X, self.SIZE_Y, self.MINE_NUM)
        x = random.randint(0, self.SIZE_X - 1)
        y = random.randint(0, self.SIZE_Y - 1)
        self.Mines.Mines_Setup(x, y)

    # test win the game, flag each mine
    def test_Win_Game(self):
        Mine_List = self.Mines.Mine_List
        for grid in Mine_List:
            x = grid[0]
            y = grid[1]
            self.Mines.Flag(x, y)
        status = self.Mines.Status
        self.assertEqual(status, self.Mines.win)

    # test die in the game, find one mine and click it
    def test_Died_Game(self):
        Mine_List = self.Mines.Mine_List
        L = len(Mine_List)
        Click_Mine = random.randint(0, L - 1)
        for i in range(L):
            grid = Mine_List[i]
            x = grid[0]
            y = grid[1]
            if i != Click_Mine:
                self.Mines.Flag(x, y)
            elif i == Click_Mine:
                self.Mines.Click(x, y)
        status = self.Mines.Status
        self.assertEqual(status, self.Mines.die)

    # test replay the game
    def test_Replay_Map(self):
        # record old map
        Old_Map = self.Mines.Data_Map
        Mine_List = self.Mines.Mine_List
        # click mine and died
        x = (Mine_List[0])[0]
        y = (Mine_List[0])[1]
        self.Mines.Click(x, y)
        Old_status = self.Mines.Status
        self.Mines.Replay()
        New_Map = self.Mines.Data_Map
        New_status = self.Mines.Status
        # whether the map is same
        self.assertEqual(Old_Map, New_Map)
        # status test
        self.assertEqual(Old_status, self.Mines.die)
        self.assertEqual(New_status, self.Mines.alive)

    def test_Auto_Play_2(self):
        # Some wrong flags
        for i in range(self.MINE_NUM):
            x = random.randint(0, self.SIZE_X - 1)
            y = random.randint(0, self.SIZE_Y - 1)
            self.Mines.Flag(x, y)

        # DO NOT USE '=', it's reference not copy
        new_Mine = copy.deepcopy(self.Mines)
        # Get operate list from a new object
        Operate_List = new_Mine.Auto_Play()
        new_Mine_status = new_Mine.Status
        # finish operates
        for op in Operate_List:
            x = op[0]
            y = op[1]
            f = op[2]
            if f == 1:
                if self.Mines.Show_Map[x][y] == self.Mines.Unknown_Grid:
                    self.Mines.Click(x, y)
            elif f == 2:
                self.Mines.Flag(x, y)
        status = self.Mines.Status
        self.assertEqual(status, self.Mines.win)
        self.assertEqual(new_Mine_status, new_Mine.win)


if __name__ == "__main__":
    unittest.main()
