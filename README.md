# Claw Machine Game 🐢🦉

## Description
A cute pixel art claw machine game built with Pygame! Catch adorable chubby dolls (turtles and owls) by controlling the claw. Each round gives you 12 coins and 10 seconds per coin to try your luck. Catch 5 or more dolls to win!

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
4. **Grab**: Press SPACE again to close the claw and catch a doll!
5. **Repeat**: Use all 12 coins in one round (10 seconds per coin)
6. **Win**: Catch 5 or more dolls to win the round!
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
- � **Adorable Round Owls** - Super cute chubby owl dolls in 5 colors:
  - Brown
  - Light Tan
  - Purple-Grey
  - Beige
  - Dark Brown
- 🎭 **Mixed Spawning** - 50/50 chance of turtles or owls appearing
- 🔊 **Sound Effects** - Procedurally generated sounds for:
  - Coin insertion (metallic clink)
  - Claw movement (motor whir)
  - Successful grab (cheerful chirp)
  - Doll falling (descending pitch)
  - Victory (triumphant chord progression)
- �🪙 **Coin System** - 12 coins per round (increased attempts!)
- ⏱️ **Timer System** - 10 seconds per coin with color-coded countdown:
  - White text (>6 seconds remaining)
  - Orange text (4-6 seconds remaining)
  - Red text (≤3 seconds remaining)
- 🏆 **Win Condition** - Catch 5 or more dolls to win the round
- 😱 **Slip Mechanic** - 60% chance dolls will slip and fall back down!
  - Adds realistic challenge
  - Visible falling animation with gravity
  - Makes victories more rewarding
- 🎮 **Precise Control** - Two-step claw operation (drop & close)
- 🎯 **14 Dolls** - Multiple turtles and owls to catch in each round
- 🔄 **Endless Rounds** - Play again as many times as you want
- 🖱️ **Mouse Support** - Click the button to play again
- ✨ **Pixel Art Style** - Retro gaming aesthetic
- 💚 **Hover Effects** - Interactive button with visual feedback

## Game Mechanics
- Position the claw carefully over a doll
- Press SPACE to start descending
- Press SPACE again at the right moment to close the claw
- The claw will automatically ascend after closing
- **Slip Challenge**: Even if you grab a doll, there's a 60% chance it will slip and fall back down!
  - The doll may slip when the claw is halfway up
  - Watch for the falling animation to see if you kept your catch
- Successfully caught dolls are added to your score!
- Each coin has a 10-second time limit - the timer resets for each coin
- When time runs out, the coin is lost and you move to the next one
- Catch 5 or more dolls (turtles or owls) to see the victory screen!

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
- NumPy 1.20.0 or higher (for sound generation)

## Tips for Success
- Watch the doll positions carefully before dropping
- Time your claw close precisely when it's over a doll
- The claw needs to be centered over the doll for a successful grab
- **Stay calm if a doll falls** - you have 12 coins, so keep trying!
- Position over dolls at the edges or top for potentially better grip
- Keep an eye on the timer - don't waste precious seconds!
- The timer color changes to warn you when time is running low
- You need to catch at least 5 dolls out of 12 attempts to win!
- Both turtles and owls count toward your score equally

## Contributing
Feel free to add your own features and improvements to this project.

## License
This project is for educational purposes at PolyU.

## Credits
Created as part of the Interactive Experience course at PolyU.
