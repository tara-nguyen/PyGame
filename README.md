# My First Game

A mini-game of football/soccer in PyGame.

List of files:
- `ClassesForMyFirstGame.py` – contains classes Game, Background, Goal, Player, and Ball
- `CroppingImages.py` – contains two functions for cropping images in PyGame
- `LineParams.py` – contains two functions for getting parameters related to a line connecting two points on the screen
- `MoveFunctions.py` – contains an update function, a function that checks for screen boundaries, and three functions for moving objects in PyGame
- `MyFirstGame.py` – main program for the game without using classes; all functions are defined at the top of the program
- `MyFirstGameUsingClasses.py` – main program for the game using the classes defined in `ClassesForMyFirstGame.py`

### Branch `add-goalkeeper`

#### Changes from `master` branch

Changes to the game in general, to the screen, and to the background:
- Add `addToLists()` and `getLists()` methods to the `Game` class
- Reduce the screen size.
- Add `load()` method to the `Background` class.

Changes to the goal:
- Reduce the height.

Changes to the player:
- Add two classes, `Goalkeeper` and `Outfielder`, which are children of the `Player` class.
- Add `getFootSize()`, `getBodySize()`, and `adjustFeetStartPos()` methods to the `Player` class.
- Split the `blit()` method into two: `blitFeet()` and `blitBody()`.
- Draw two players, a goalkeeper and an outfielder/striker, onto the screen.
- Modify the `updatePlayer()` and `updateFoot()` methods to accommodate multiple players' movements.

Changes to the ball:
- Add `load()` method.
- Put the ball at a fixed position at the start of the program. After the player scores, the ball will be returned to this position.
- Reduce the speed.
- Modify the `hitPlayer()` method to accommodate the presence of multiple players.
