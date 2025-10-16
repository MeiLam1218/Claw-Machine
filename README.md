# Claw Machine Game 🐢

## Description
A cute pixel art claw machine game built with Pygame! Catch adorable chubby turtles by controlling the claw. Each round gives you 6 coins and 15 seconds per coin to try your luck. Catch 5 or more turtles to win!

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Claw Machine game:
```bash
python "Claw Machine.py"
```

## How to Play

### Game Flow
1. **Start**: Press ENTER to insert a coin
2. **Position**: Use arrow keys to move the claw left/right
3. **Drop**: Press SPACE to drop the claw
4. **Grab**: Press SPACE again to close the claw and catch a turtle!
5. **Repeat**: Use all 6 coins in one round (15 seconds per coin)
6. **Win**: Catch 5 or more turtles to win the round!
7. **Play Again**: Click the "PLAY AGAIN" button to start a new round

### Controls
- **ENTER** - Insert a coin to start playing
- **← →** or **A/D** - Move claw left and right
- **SPACE** (first press) - Drop the claw down
- **SPACE** (second press) - Close the claw to grab
- **Mouse Click** - Click "PLAY AGAIN" button after round ends

## Game Features
- 🐢 **Cute Chubby Turtles** - Round, adorable pixel art turtle dolls in 5 colors:
  - Green
  - Dark Green
  - Grey Blue
  - Yellow-Green
  - Dark Blue
- 🪙 **Coin System** - 6 coins per round
- ⏱️ **Timer System** - 15 seconds per coin with color-coded countdown:
  - White text (>10 seconds remaining)
  - Orange text (6-10 seconds remaining)
  - Red text (≤5 seconds remaining)
- 🏆 **Win Condition** - Catch 5 or more turtles to win the round
- 🎮 **Precise Control** - Two-step claw operation (drop & close)
- 🎯 **14 Turtles** - Multiple turtles to catch in each round
- 🔄 **Endless Rounds** - Play again as many times as you want
- 🖱️ **Mouse Support** - Click the button to play again
- ✨ **Pixel Art Style** - Retro gaming aesthetic
- 💚 **Hover Effects** - Interactive button with visual feedback

## Game Mechanics
- Position the claw carefully over a turtle
- Press SPACE to start descending
- Press SPACE again at the right moment to close the claw
- The claw will automatically ascend after closing
- Successfully caught turtles are added to your score!
- Each coin has a 15-second time limit - the timer resets for each coin
- When time runs out, the coin is lost and you move to the next one
- Catch 5 or more turtles to see the victory screen!

## Project Structure
```
interactive experience/
├── Claw Machine.py   # Main game file
├── README.md         # This file
└── requirements.txt  # Python dependencies
```

## Requirements
- Python 3.7 or higher
- Pygame 2.5.0 or higher

## Tips for Success
- Watch the turtle positions carefully before dropping
- Time your claw close precisely when it's over a turtle
- The claw needs to be centered over the turtle for a successful grab
- Keep an eye on the timer - don't waste precious seconds!
- The timer color changes to warn you when time is running low
- You need to catch at least 5 turtles out of 6 attempts to win!

## Contributing
Feel free to add your own features and improvements to this project.

## License
This project is for educational purposes at PolyU.

## Credits
Created as part of the Interactive Experience course at PolyU.
