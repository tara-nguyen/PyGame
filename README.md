# My First Game

#### A mini-game of football/soccer in PyGame.

List of files in the repos:
- `ClassesForMyFirstGame.py` – contains classes `Game`, `Background`, `Goal`, `Player`, and `Ball`
- `CroppingImages.py` – contains two functions for cropping images in PyGame
- `LineParams.py` – contains two functions for getting parameters related to a line connecting two points on the screen
- `MoveFunctions.py` – contains an `update` function, a function that checks for screen boundaries, and three functions for moving objects in PyGame
- `MyFirstGame.py` – main program for the game without using classes; all functions are defined at the top of the program
- `MyFirstGameUsingClassesVer1.py` – main program for the game using the classes defined in `ClassesForMyFirstGame.py`
- `MyFirstGameUsingClassesVer2.py` – main program for the game using the classes defined in `NonplayerClasses.py` and in `PlayerClasses.py`.
- `NonplayerClasses.py` – contains classes `Game`, `Background`, `Goal`, and `Ball`; specific to the `add-goalkeeper` branch
- `PlayerClasses.py` – contains class `Player`; specific to the `add-goalkeeper` branch

### Branch `add-goalkeeper`

#### Changes from `master` branch

Changes to the main program:
- Add goalkeeper.
- Add `processMovements()` function.

Changes to the `NonplayerClasses` module:
- Add `addToLists()` and `getLists()` methods to the `Game` class.
- Add `load()` method to the `Background` class.
- Add two functions, `isBetween()` and `getTrig()`, which do not belong to any class.
- Remove the `getSinCos()` method from the `Ball` class.

Changes to the screen:
- Reduce the screen size.

Changes to the goal:
- Reduce the height.

Changes to the ball:
- Add `load()` method.
- Put the ball at a fixed position at the start of the program. After the player scores, the ball will be returned to this position.
- Reduce the speed.
- Rename `moveBall()` into `move()`. Modify that method to allow goalkeeper movements.
- Modify the `hitPlayer()` method to accommodate the presence of multiple players.

Changes to the `PlayerClasses` module:
- Add two classes, `Goalkeeper` and `Outfielder`, which are children of the `Player` class.
- Rename `setStartPos()` to `setFootStartPos()`.
- Add `adjustFootStartPos()` method to the `Player` class.
- Split the `blit()` method into two: `blitFeet()` and `blitBody()`.
- Remove the `getSinCos()`.
- Move the `move()` method in the `Player` class to the `Outfielder` class. The `Goalkeeper` class has its own `move()` method.
- Modify the `updatePlayer()` and `updateFoot()` methods to accommodate multiple players' movements.
- Split the `kickBall()` method in the `Player` class into: `prepareBallKick()`, `updateKickingFoot()`, and `checkBallTouch()` in that class, as well as the `kickBall()` method in each of the child classes.
- Draw two players, a goalkeeper and an outfielder/striker, onto the screen.

### Branch `outfielder-movements`

#### Changes from `add-goalkeeper` branch

Changes to the `MoveFunctions` module:
- Add code for diagonal movements to the `moveStraight()` function.
- Add `reachedBound1()` function.
- Rename the old `reachedBoundaries()` function to `reachedBound2()`.
