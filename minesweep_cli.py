from config import SIZE_X, SIZE_Y
from Mine_Sweep import Mine_Map

if __name__ == "__main__":

    Steps = 0
    Continue_Game = True
    while Continue_Game:

        if Steps == 0:
            print('Game Start!')
            print('Map Size (%d,%d)' % (SIZE_X, SIZE_Y))
            print('init your game')
            x = int(input('x='))
            y = int(input('y='))

            Mine = Mine_Map(x, y)
            Mine.Print_Mines()
        else:
            x = int(input('x='))
            y = int(input('y='))
            do = input('1 is click, 2 is flag \t')
            if do == '1':
                Mine.Click(x, y)
            elif do == '2':
                Mine.Flag(x, y)

        Mine.Disp_UI()
        Steps += 1
        if Mine.Status != '1':
            Continue_Game = False
