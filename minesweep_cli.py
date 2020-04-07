from Mine_Map import Mine_Map

if __name__ == "__main__":
    Mine = Mine_Map(5, 5, 5)

    Continue_Game = True
    while Mine.Status != Mine.win and Mine.Status != Mine.die:

        if Mine.Status == Mine.inited:
            print('Game Start!')
            print('Map Size (%d,%d)' % (Mine.SIZE_X, Mine.SIZE_Y))
            print('init your game')
            x = int(input('x='))
            y = int(input('y='))
            Mine.Mines_Setup(x, y)
        else:
            x = int(input('x='))
            y = int(input('y='))
            do = input('1 is click, 2 is flag \t')
            if do == '1':
                Mine.Click(x, y)
            elif do == '2':
                Mine.Flag(x, y)

        Mine.Disp_UI()
