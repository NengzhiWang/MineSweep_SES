# MineSweeper_SES

Final project for the course 项目实践 in 2020 spring.

> Team Member: 汪能志 周瀛 马明慧 杨雨薇

# Content

## Overview

This project was designed based on the requirements of [PracticeOfComputingUsingPython/08_ClassDesign/Minesweeper](http://www.cse.msu.edu/~cse231/PracticeOfComputingUsingPython/08_ClassDesign/Minesweeper/) from [http://www.cse.msu.edu/~cse231/PracticeOfComputingUsingPython/](http://www.cse.msu.edu/~cse231/PracticeOfComputingUsingPython/).

We completed the main algorithms of minesweeper, and implemented a simple graphical user interface by ` tkinter `.

The project has a unit test file to test key algorithms. The unit testing process is done primarily through GitHub and Travis CI.

## Class for data structures and algorithms

We created a class called ` Mine_Map` for minesweeper in the file  './Mine_Map.py'. It contains data structures for storing map data and provides the following functions.

1. Based on the first selected grid, mines are randomly placed on the map and the number of mines around each grid is calculated.

2. If the player clicks a unknown grid, the number is now visible to the player.

3. If the player clicks a grid without mine, ripple effect takes place uncovering all the blanks in the neighborhood until either the grid boundary is reached or a number is reached along its path. The ripple effect is implemented by recursion. . On larger maps, the following errors may occur ` RecursionError: maximum recursion depth exceeded in comparison ` due to the limitation of ` sys.setrecursionlimit() `

4. If the player clicks a grid with mine, the game is over.

5. If the player clicks a not unknown grid, and the number of flags nearby equal to the number of mines nearby, all unknown grids nearby will be shown automatically. If there is a wrong flag, the game is over.

6. Player can mark a grid or unmark a grid.

7. When the player marks all the mines, the game is won.

8. Automatically finish a game.

9. Clear all operations except setting mines.

## Class for GUI

In file './Mine_GUI.py', we described the layout of the graphical user interface and defined event function in GUI.

Class ` Mine_GUI ` have a object of Class ` Mine_Map `.

Actions on GUI controls trigger event functions and call the functions of the ` Mine_Map ` object. Subsequently, the GUI will change the displayed content according to the change of the data in the ` Mine_Map ` object.

## Unit test

File './unit_test.py' includes four unit test.

1. Win the game

2. Game Over

3. Automatically finish a game

4. Clear all operations except setting mines

# Files 

* Mine_Map.py

Class for data structures and algorithms

* Mine_GUI.py

Class for GUI

* minesweeper_CLI.py

Play and print the data of minesweeper in the command-line interface.

* minesweeper_GUI.py

Play the minesweeper in GUI.

* unit_test.py

Unit test.

# Result

* CLI

<div align=center>
<img height='500' width='360' src='https://github.com/NengzhiWang/MineSweep_SES/blob/master/README%20Image/CLI%20Play.jpg' alt='CLI'>
</div>

* GUI

<div align=center>
<img height='501' width='332' src='https://github.com/NengzhiWang/MineSweep_SES/blob/master/README%20Image/GUI.jpg' alt='GUI'>
</div>

* Auto Play

<div align=center>
<img height='446' width='320' src='https://github.com/NengzhiWang/MineSweep_SES/blob/master/README%20Image/Auto%20Play.gif' alt='Auto play'>
</div>

* Local Unit Test

<div align=center>
<img height='150' width='370' src='https://github.com/NengzhiWang/MineSweep_SES/blob/master/README%20Image/Unit%20Test.jpg' alt='Local unit test'>
</div>

* Travis CI

<div align=center>
<img height='750' width='525' src='https://github.com/NengzhiWang/MineSweep_SES/blob/master/README%20Image/Travis%20Test.png' alt='Travis Test'>
</div>
