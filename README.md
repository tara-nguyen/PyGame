# My First Game

### Overview

- Mini-football game written in Python 3.7.8
- PyGame version 1.9.6
- Branches (in order of date created):
  - [`master`](https://github.com/tara-nguyen/pygame-football#branch-master)
  - [`add-goalkeeper`](https://github.com/tara-nguyen/pygame-football#branch-add-goalkeeper)
  - [`outfielder-movements`](https://github.com/tara-nguyen/pygame-football#branch-outfielder-movements)

### Branch `master`

List of modules:
- `ClassesForMyFirstGame` – contains classes `Game`, `Background`, `Goal`, `Player`, and `Ball`
- `CroppingImages` – contains two functions for cropping images in PyGame
- `LineParams` – contains two functions for getting parameters related to a line connecting two points on the screen
- `MoveFunctions` – contains functions for moving objects in PyGame
- `MyFirstGame` – main program for the game, from which the game is initiated; no classes used
- `MyFirstGameUsingClassesVer1` – main program for the game using classes

### Branch `add-goalkeeper`

#### Changes from `master`

**New modules:**
- `MyFirstGameUsingClassesVer2` – main program, from which the game is initiated
- `NonplayerClasses` – contains classes `Game`, `Background`, `Goal`, and `Ball`
- `PlayerClasses` – contains classes `Player`, `Goalkeeper`, and `Outfielder`

**Unused modules:**
- `ClassesForMyFirstGame`
- `MyFirstGame`
- `MyFirstGameUsingClassesVer1`

**Changes from `MyFirstGameUsingClassesVer1` to `MyFirstGameUsingClassesVer2`:**
- Add goalkeeper.
- Add `processMovements()` function.

**Changes to `NonplayerClasses`:**
- Add `addToLists()` and `getLists()` methods to the `Game` class.
- Add `load()` method to the `Background` class.
- Add two functions, `isBetween()` and `getTrig()`, which do not belong to any class.

**Changes to `Ball`:**
- Add `load()` method.
- Put the ball at a fixed position at the start of the program. After the player scores, the ball will be returned to this position.
- Reduce the speed.
- Remove the `getSinCos()` method (repaced by the `getTrig()` function in the `NonplayerClasses` module).
- Rename `moveBall()` to `move()`. Modify that method to accommodate goalkeeper movements.
- Modify the `hitPlayer()` method to accommodate the presence of multiple players.

**Changes to `PlayerClasses`:**
- Add two classes, `Goalkeeper` and `Outfielder`, which are children of the `Player` class.
- Rename `setStartPos()` to `setFootStartPos()`.
- Add `adjustFootStartPos()` method to the `Player` class.
- Split the `blit()` method into `blitFeet()` and `blitBody()`.
- Remove the `getSinCos()` method (repaced by the `getTrig()` function in the `NonplayerClasses` module).
- Move the `move()` method in the `Player` class to the `Outfielder` class. The `Goalkeeper` class has its own `move()` method.
- Modify the `updatePlayer()` and `updateFoot()` methods to accommodate movements of multiple players.
- Split the `kickBall()` method in the `Player` class into: `prepareBallKick()`, `updateKickingFoot()`, and `checkBallTouch()` in that class, plus the `kickBall()` method in each of the child classes.

### Branch `outfielder-movements`

#### Changes from `add-goalkeeper`

**New modules:**
- `MyFirstGameUsingClassesVer3` – main program, from which the game is initiated
- `MoveFunctionsUpdated` – updated version of the `MoveFunctions` module

**Unused modules:**
- `MoveFunctions`

**Changes to `LineParams`:**
- Add three functions: `getIntersect()`, `getDistToLine()`, `isBetween()`, and `checkSide()`.

**Changes from `MoveFunctions` to `MoveFunctionsUpdated`:**
- Split big chunks of a function into several other functions for neatness.
- Add code for diagonal movements.
- Rename most of the functions.

**Changes from `MyFirstGameUsingClassesVer2` to `MyFirstGameUsingClassesVer3`:**
- Move the `processMovements()` function to the `Game` class in the `NonplayerClasses` module.

**Changes to `NonplayerClasses`:**
- Add `processMovements()` method to the `Game` class (moved from the main program).
- Remove the `addToLists()` method, the `getLists()` method, and the `isBetween()` function because they are unnecessary.

**Changes to `Goal`:**
- Remove the `getCenter()` and `getCenterPos()` methods because they are unnecessary.

**Changes to `Ball`:**
- Remove the following methods: `setVelocity()`, `getVelocity()`, `setFinalStep1()`, `setFinalStep2()`, `hitGoalPosts()`, `checkBouncing()`, `hitPlayer()`, and `checkGoal()`.
- Rename `setFinalStepSB()`, `setFinalStepGP()`, and `bounceBack()` to `approachScrBounds()`, `approachGoalPosts()`, and `bounceOff()`, respectively.
- Add `approachPlayer()` method.
- Modify code for setting final step (`approachScrBounds()`, `approachGoalPosts()`, and `approachPlayer()`) before the ball hits the screen boundaries, the goal posts, or a player.
- Modify the `move()` method so that the ball makes only one movement per keypress.
- Rename `resetBall()` and `updateBall()` to `reset()` and `update()`, respectively.

**Changes to `PlayerClasses`:**
- Add `getCorners()` and `getShoulderAngle()` methods to the `Player` class.
- Combine the `getMidpoint()` method and the `getRotation()` method into one and remove the former.
- Combine the three methods for moving players into one method called `move()` in the `Player` class. Remove the `move()` method in the `Outfielder` class.
- Rename `updatePlayer()` to `updateAll()`.
- Combine the `prepareBallKick()` and `updateKickingFoot()` methods into one method called `kickBall()` in the `Player` class. Remove the `kickBall()` methods in the `Goalkeeper` and `Outfielder` classes.
- Rename the `move()` method in the `Goalkeeper` class to `moveAcross()`.
