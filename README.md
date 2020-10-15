# My First Game

#### A mini-game of football/soccer in PyGame.

List of files:
- `ClassesForMyFirstGame.py` – contains classes `Game`, `Background`, `Goal`, `Player`, and `Ball`
- `CroppingImages.py` – contains two functions for cropping images in PyGame
- `LineParams.py` – contains two functions for getting parameters related to a line connecting two points on the screen
- `MoveFunctions.py` – contains functions for moving objects in PyGame
- `MoveFunctionsUpdated.py` – updated version of `MoveFunctions` module; specific to `outfielder-movements` branch and all branches created afterward
- `MyFirstGame.py` – main program for the game without using classes; all functions are defined at the top of the program
- `MyFirstGameUsingClassesVer1.py` – main program for the game using the classes defined in `ClassesForMyFirstGame.py`
- `MyFirstGameUsingClassesVer2.py` – main program for the game using the classes defined in `NonplayerClasses` and `PlayerClasses` modules.
- `NonplayerClasses.py` – contains classes `Game`, `Background`, `Goal`, and `Ball`; specific to `add-goalkeeper` branch and all branches created afterward
- `PlayerClasses.py` – contains class `Player`; specific to `add-goalkeeper` branch and all branches created afterward

### Branch `add-goalkeeper`

#### Changes from `master` branch

Changes to the main program:
- Add goalkeeper.
- Add `processMovements()` function.

Changes to the `NonplayerClasses` module:
- Add `addToLists()` and `getLists()` methods to the `Game` class.
- Add `load()` method to the `Background` class.
- Add two functions, `isBetween()` and `getTrig()`, which do not belong to any class.

Changes to the screen:
- Reduce the screen size.

Changes to the goal:
- Reduce the height.

Changes to the ball:
- Add `load()` method.
- Put the ball at a fixed position at the start of the program. After the player scores, the ball will be returned to this position.
- Reduce the speed.
- Remove the `getSinCos()` method (repaced by the `getTrig()` function in the `NonplayerClasses` module).
- Rename `moveBall()` into `move()`. Modify that method to accommodate goalkeeper movements.
- Modify the `hitPlayer()` method to accommodate the presence of multiple players.

Changes to the `PlayerClasses` module:
- Add two classes, `Goalkeeper` and `Outfielder`, which are children of the `Player` class.
- Rename `setStartPos()` to `setFootStartPos()`.
- Add `adjustFootStartPos()` method to the `Player` class.
- Split the `blit()` method into `blitFeet()` and `blitBody()`.
- Remove the `getSinCos()` method (repaced by the `getTrig()` function in the `NonplayerClasses` module).
- Move the `move()` method in the `Player` class to the `Outfielder` class. The `Goalkeeper` class has its own `move()` method.
- Modify the `updatePlayer()` and `updateFoot()` methods to accommodate multiple players' movements.
- Split the `kickBall()` method in the `Player` class into: `prepareBallKick()`, `updateKickingFoot()`, and `checkBallTouch()` in that class, as well as the `kickBall()` method in each of the child classes.
- Draw two players, a goalkeeper and an outfielder/striker, onto the screen.

### Branch `outfielder-movements`

#### Changes from `add-goalkeeper` branch

Changes to the `LineParams` module:
- Add `checkSide()` function.

Changes to the module used for handling object movements:
- Add code for diagonal movements.
- Split big chunks of a function into several other functions for neatness.

Changes to the main program:
- Move the `processMovements()` function to the `Game` class in the `NonplayerClasses` module.

Changes to the `NonplayerClasses` module:
- Add `processMovements()` method to the `Game` class (moved from the main program).
- Remove the `addToLists()` method, the `getLists()` method, and the `isBetween()` function because they are unnecessary.

Changes to the goal:
- Remove the `getCenter()` and `getCenterPos()` methods because they are unnecessary.
Changes to the ball:
- Remove the `setVelocity()` and `getVelocity()` methods because they are not used.
- Add `setFinalStepSB()` and `setFinalStepGP()` methods, based on the original `setFinalStep2()` method.
- The new `setFinalStep2()` method is a combination of `setFinalStepSB()` and `setFinalStepGP2()`.
- Modify code for setting the final step, as well as the `hitGoalPosts()` and `checkBouncing()` methods, to accommodate the ball hitting the goal posts from below the goal line.
- Add code (to the `hitPlayer()` method) for setting the final step before the ball hits a player.

Changes to the `PlayerClasses` module:
- Add `getCorners()` and `getShoulderAngle()` methods to the `Player` class.
- Combine the `getMidpoint()` method and the `getRotation()` method into one and remove the former.
- Combine the `prepareBallKick()` and `updateKickingFoot()` methods into one method called `kickBall()` in the `Player` class. Remove the `kickBall()` methods in the `Goalkeeper` and `Outfielder` classes.
