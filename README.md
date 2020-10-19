# PyGame Mini-Football

**Overview**
- Mini-football game written in Python 3.7.8
- PyGame version 1.9.6
- Branches (in order of date created):
  - [`master`](https://github.com/tara-nguyen/pygame-football#branch-master)
  - [`add-goalkeeper`](https://github.com/tara-nguyen/pygame-football#branch-add-goalkeeper)
  - [`outfielder-movements`](https://github.com/tara-nguyen/pygame-football#branch-outfielder-movements)

## Branch `master`

**Original modules (before any other branch was created):**
- `ClassesForMyFirstGame` – contains classes `Game`, `Background`, `Goal`, `Player`, and `Ball`
- `CroppingImages` – contains two functions for cropping images in PyGame
- `LineParams` – contains functions for obtaining parameters related to lines and points on the screen
- `MoveFunctions` – contains functions for moving objects in PyGame
- `MyFirstGame` – original main program, from which the game is initiated; no classes used
- `MyFirstGameUsingClassesVer1` – main program using classes from `ClassesForMyFirstGame`

**Modules added from other branches**
- `MyFirstGameUsingClassesVer2` – main program in branch [`add-goalkeeper`](https://github.com/tara-nguyen/pygame-football#branch-add-goalkeeper)
- `MyFirstGameUsingClassesVer3` – main program in branch [`outfielder-movements`](https://github.com/tara-nguyen/pygame-football#branch-outfielder-movements)
- `MoveFunctionsUpdated` – updated version of `MoveFunctions`
- `NonplayerClasses` – contains classes `Game`, `Background`, `Goal`, and `Ball`
- `PlayerClasses` – contains classes `Player`, `Goalkeeper`, and `Outfielder`

## Branch `add-goalkeeper`

**Overview**
- Developed from [`master`](https://github.com/tara-nguyen/pygame-football#branch-master) - [repos at initial commit](https://github.com/tara-nguyen/pygame-football/tree/4a8ffb20957ad7faba00bda1d9cf337846650662)
- [Add a goalkeeper who is able to move between goal posts, catch the ball, and kick it back to the outfielder.](https://github.com/tara-nguyen/pygame-football/milestone/1)

**New modules:**
- `MyFirstGameUsingClassesVer2` – main program, from which the game is initiated
- `NonplayerClasses` – adated from `ClassesForMyFirstGame`; contains classes `Game`, `Background`, `Goal`, and `Ball`
- `PlayerClasses` – adated from `ClassesForMyFirstGame`; contains classes `Player`, `Goalkeeper`, and `Outfielder`

**Unused modules:**
- `ClassesForMyFirstGame`
- `MyFirstGame`
- `MyFirstGameUsingClassesVer1`

**Changes from `MyFirstGameUsingClassesVer1` to `MyFirstGameUsingClassesVer2`:**
- Add goalkeeper
- Add `processMovements()` function

**Changes from `ClassesForMyFirstGame` to `NonplayerClasses`, excluding changes to `Ball` class:**
- Remove `Player` class
- Add to `Game`: `addToLists()` and `getLists()` methods
- Add to `Background`: `load()` method
- Add `isBetween()` and `getTrig()` functions, outside of the classes

**Changes to `Ball` class in `NonplayerClasses`:**
- Add method `load()`
- Remove `getSinCos()`
- Rename `moveBall()` to `move()` and modify it to accommodate goalkeeper movements
- Modify `hitPlayer()` to accommodate the presence of multiple players

**Changes from `ClassesForMyFirstGame` to `PlayerClasses`:**
- Keep only `Player` class and remove the rest
- Add classes: `Goalkeeper` and `Outfielder`
- Rename `setStartPos()` to `setFootStartPos()`
- Add to `Player`: `adjustFootStartPos()` method
- Split `blit()` into `blitFeet()` and `blitBody()`
- Remove `getSinCos()`
- Move `move()` method from `Player` to `Outfielder`. `Goalkeeper` has its own `move()` method
- Modify `updatePlayer()` and `updateFoot()` to accommodate movements of multiple players
- Split `kickBall()` method in `Player` into:
  - `prepareBallKick()`, `updateKickingFoot()`, and `checkBallTouch()` in `Player`; and
  - `kickBall()` in `Goalkeeper` and in `Outfielder`

## Branch `outfielder-movements`

**Overview**
- Developed from [`add-goalkeeper`](https://github.com/tara-nguyen/pygame-football#branch-add-goalkeeper)
- [Enable outfielder to move in any direction using only the arrow keys.](https://github.com/tara-nguyen/pygame-football/milestone/2)
- [Fix strange ball behavior](https://github.com/tara-nguyen/pygame-football/milestone/4)

**New modules:**
- `MyFirstGameUsingClassesVer3` – main program, from which the game is initiated
- `MoveFunctionsUpdated` – updated version of `MoveFunctions`

**Unused modules:**
- `MoveFunctions`

**Changes to `LineParams`:**
- Add functions: `getIntersect()`, `getDistToLine()`, `isBetween()`, and `checkSide()`

**Changes from `MoveFunctions` to `MoveFunctionsUpdated`:**
- Split big chunks of a function into several other functions for neatness
- Add code for diagonal movements
- Rename most of the functions

**Changes from `MyFirstGameUsingClassesVer2` to `MyFirstGameUsingClassesVer3`:**
- Move `processMovements()` function to `Game` in `NonplayerClasses`

**Changes to `Game` class:**
- Add to `Game`: `processMovements()` method (moved from `MyFirstGameUsingClassesVer3`)
- Remove: `addToLists()`, `getLists()`, and `isBetween()`

**Changes to `Goal` class in `NonplayerClasses`:**
- Remove `getCenter()` and `getCenterPos()`

**Changes to `Ball` class in `NonplayerClasses`:**
- Remove: `setVelocity()`, `getVelocity()`, `setFinalStep1()`, `setFinalStep2()`, `hitGoalPosts()`, `checkBouncing()`, `hitPlayer()`, and `checkGoal()`
- Rename:
  - `setFirstStep()` to `setStep1`,
  - `setStep()` to `setStep2()`,
  - `setFinalStepSB()` to `approachScrBounds()`,
  - `setFinalStepGP()` to `approachGoalPosts()`,
  - `bounceBack()` to `bounceOff()`,
  - `resetBall()` to `reset()`, and
  - `updateBall()` to `update()`
- Add methods: `getNewStep1()`, `getNewStep2()`, and `approachPlayer()`
- Modify code for setting final step (`approachScrBounds()`, `approachGoalPosts()`, and `approachPlayer()`)
- Modify `bounceOff()` to accommodate changing both lateral and vertical steps at the same time
- Modify `move()` so that the ball makes only one movement per keypress

**Changes to `PlayerClasses`:**
- Add to `Player`: `getCorners()` and `getShoulderAngle()` methods
- Move code for `getMidpoint()` into `getRotation()` and remove `getMidpoint()`
- Combine `moveStraight()`, `moveToBall()`, and `moveAroundBall()` into one method called `move()` in `Player`. Remove `move()` method in `Outfielder`
- Rename: 
  - `updatePlayer()` to `updateAll()`
  - `move()` in `Goalkeeper` to `moveAcross()`
- Combine `prepareBallKick()` and `updateKickingFoot()` into one method called `kickBall()` in `Player`. Remove `kickBall()` methods in `Goalkeeper` and `Outfielder`
