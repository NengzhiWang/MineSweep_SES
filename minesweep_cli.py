from Mine_Map import Mine_Map

SIZE_X = 5
SIZE_Y = 5
MINE_NUM = 5
if __name__ == "__main__":

    Mine = Mine_Map(SIZE_X, SIZE_Y, MINE_NUM)

    Continue_Game = True
    while Mine.Status != Mine.win and Mine.Status != Mine.die:

        if Mine.Status == Mine.inited:
            print('Game Start!')
            print('Map Size (%d,%d)' % (Mine.SIZE_X, Mine.SIZE_Y))
            print('init your game')
            x = int(input('x='))
            y = int(input('y='))
            if 0 <= x < SIZE_X and 0 <= y < SIZE_Y:
                Mine.Mines_Setup(x, y)
                Mine.Disp_UI()
            else:
                print('out of range')
        else:
            x = int(input('x='))
            y = int(input('y='))
            if 0 <= x < SIZE_X and 0 <= y < SIZE_Y:
                do = input('1 is click, 2 is flag \t')
                if do == '1':
                    Mine.Click(x, y)
                elif do == '2':
                    Mine.Flag(x, y)
                Mine.Disp_UI()
            else:
                print('out of range')
