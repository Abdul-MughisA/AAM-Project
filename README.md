# Logic Express

A top-down 2D game about trains.

## Elements
There are 3 main elements.
- Player
- Train
- Obstacles

## Obstacles

### Logs
- Can be pushed from any direction
    - Pushed horizontally, roll until they hit something
    - Pushed vertically, moves one block
### Stumps
- Moved by player
- No other obstacle can move over the stump
### Water
- Cannot be moved by player
- Logs can go over water
- If water is greater than pushed object, object falls into the water, behaves part of the ground
### Lava (water)
- Logs destroyed
- Bricks behave as floor items
### Sheeps
- Moves randomly
- Can be pushed
### Cows
- Moves until hits something, then changes direction
- Cannot be pushed
### Bricks
- 1-by-1
- Pushable by 1 tile
- Takes a long time to push (they are heavy)
### Demons (2 types)
- Sheep demons act like sheep
- Cow demons act like cows
- If they run into train, train explodes
## Behaviour
- Train is constantly moving across a track (implemented through a tile-based system)
- The player can move around freely (using WASD or arrows for left-hand support)
    - Push obstacles
- Boost mechanic/lever
- Train/TfL worker killed when train explodes (train explodes when obstacle hit)

## Scope
- Rail building
- Water
- Exploding train
- Mazes & logic puzzles

A'yaan Abdul-Mughis
