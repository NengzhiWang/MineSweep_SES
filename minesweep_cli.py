from config import SIZE_X, SIZE_Y
from Mine_Sweep import Mine_Map

if __name__ == "__main__":
    MINES = Mine_Map(2, 2)
    MINES.Print_Mines()

    MINES.Disp_All()
    MINES.Disp_UI()
    while MINES.Status == '1':
        x_in = input('x=')
        y_in = input('y=')
        do = input('do=')
        x = int(x_in)
        y = int(y_in)
        if do == '1':
            MINES.Click(x, y)
        elif do == '2':
            MINES.Flag(x, y)
        MINES.Disp_UI()
