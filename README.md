# PyGame Mini-Football

**Overview**
- Mini-football game written in Python 3.7.8
- PyGame version 1.9.6
- Branches (in order of date created):
  - [`master`](https://github.com/tara-nguyen/pygame-football#branch-master)
  - [`add-goalkeeper`](https://github.com/tara-nguyen/pygame-football#branch-add-goalkeeper)
  - [`outfielder-movements`](https://github.com/tara-nguyen/pygame-football#branch-outfielder-movements)

## Branch `master`

List of modules:
- `ClassesForMyFirstGame` – contains classes `Game`, `Background`, `Goal`, `Player`, and `Ball`
- `CroppingImages` – contains two functions for cropping images in PyGame
- `LineParams` – contains two functions for getting parameters related to a line connecting two points on the screen
- `MoveFunctions` – contains functions for moving objects in PyGame
- `MyFirstGame` – main program for the game, from which the game is initiated; no classes used
- `MyFirstGameUsingClassesVer1` – main program for the game using classes

## Branch `add-goalkeeper`

**Overview**
- Created from `master` - [repos at initial commit](https://github.com/tara-nguyen/pygame-football/tree/4a8ffb20957ad7faba00bda1d9cf337846650662)
- [Add a goalkeeper who is able to move between goal posts, catch the ball, and kick it back to the outfielder.](https://github.com/tara-nguyen/pygame-football/milestone/1)

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

**Changes to `NonplayerClasses`, excluding changes to `Ball` class:**
- Add to `Game`: `addToLists()` and `getLists()` methods.
- Add to `Background`: `load()` method.
- Add two functions, `isBetween()` and `getTrig()`, which do not belong to any class.

**Changes to `Ball` class in `NonplayerClasses`:**
- Add `load()` method.
- Remove `getSinCos()` method.
- Rename `moveBall()` to `move()`. Modify it to accommodate goalkeeper movements.
- Modify `hitPlayer()` to accommodate the presence of multiple players.

**Changes to `PlayerClasses`:**
- Add two classes, `Goalkeeper` and `Outfielder`, which are children of the `Player` class.
- Rename `setStartPos()` to `setFootStartPos()`.
- Add to `Player`: `adjustFootStartPos()` method.
- Split `blit()` into `blitFeet()` and `blitBody()`.
- Remove `getSinCos()` method.
- Move the `move()` method from `Player` to `Outfielder`. `Goalkeeper` has its own `move()` method.
- Modify `updatePlayer()` and `updateFoot()` to accommodate movements of multiple players.
- Split the `kickBall()` method in `Player` into:
  - `prepareBallKick()`, `updateKickingFoot()`, and `checkBallTouch()` in `Player`; and
  - `kickBall()` in `Goalkeeper` and in `Outfielder`.

## Branch `outfielder-movements`

**Overview**
- Created from `add-goalkeeper`
- [Enable outfielder to move in any direction using only the arrow keys.](https://github.com/tara-nguyen/pygame-football/milestone/2)

**New modules:**
- `MyFirstGameUsingClassesVer3` – main program, from which the game is initiated
- `MoveFunctionsUpdated` – updated version of the `MoveFunctions` module

**Unused modules:**
- `MoveFunctions`

**Changes to `LineParams`:**
- Add functions: `getIntersect()`, `getDistToLine()`, `isBetween()`, and `checkSide()`.

**Changes from `MoveFunctions` to `MoveFunctionsUpdated`:**
- Split big chunks of a function into several other functions for neatness.
- Add code for diagonal movements.
- Rename most of the functions.

**Changes from `MyFirstGameUsingClassesVer2` to `MyFirstGameUsingClassesVer3`:**
- Move the `processMovements()` function to the `Game` class in `NonplayerClasses`.

**Changes to `Game` class:**
- Add to `Game`: `processMovements()` (moved from `MyFirstGameUsingClassesVer3`).
- Remove methods and functions: `addToLists()`, `getLists()`, and `isBetween()`.

**Changes to `Goal` class in `NonplayerClasses`:**
- Remove methods: `getCenter()` and `getCenterPos()`.

**Changes to `Ball` class in `NonplayerClasses`:**
- Remove methods: `setVelocity()`, `getVelocity()`, `setFinalStep1()`, `setFinalStep2()`, `hitGoalPosts()`, `checkBouncing()`, `hitPlayer()`, and `checkGoal()`.
- Rename:
  - `setFirstStep()` to `setStep1`,
  - `setStep()` to `setStep2()`,
  - `setFinalStepSB()` to `approachScrBounds()`,
  - `setFinalStepGP()` to `approachGoalPosts()`,
  - `bounceBack()` to `bounceOff()`,
  - `resetBall()` to `reset()`, and
  - `updateBall()` to `update()`
- Add methods: `getNewStep1()`, `getNewStep2()`, and `approachPlayer()`.
- Modify code for setting final step (`approachScrBounds()`, `approachGoalPosts()`, and `approachPlayer()`) before the ball hits the screen boundaries, the goal posts, or a player.
- Modify `bounceOff()` to accommodate changing both lateral and vertical steps at the same time.
- Modify `move()` so that the ball makes only one movement per keypress.

**Changes to `PlayerClasses`:**
- Add `getCorners()` and `getShoulderAngle()` methods to the `Player` class.
- Combine the `getMidpoint()` method and the `getRotation()` method into one and remove the former.
- Combine the three methods for moving players into one method called `move()` in the `Player` class. Remove the `move()` method in the `Outfielder` class.
- Rename `updatePlayer()` to `updateAll()`.
- Combine the `prepareBallKick()` and `updateKickingFoot()` methods into one method called `kickBall()` in the `Player` class. Remove the `kickBall()` methods in the `Goalkeeper` and `Outfielder` classes.
- Rename the `move()` method in the `Goalkeeper` class to `moveAcross()`.
