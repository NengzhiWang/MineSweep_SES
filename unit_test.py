import random
import unittest
from Mine_Sweep import Mine_Map
import sys
sys.setrecursionlimit(10000)
# Adjust recursive tree limits
# default is 1000?


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


if __name__ == "__main__":
    unittest.main()
