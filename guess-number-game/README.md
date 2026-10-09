# 🎯 Guess the Number – Desktop Edition

## Objective
A modern, standalone desktop GUI version of the classic "Guess the Number" game, built entirely in Python using `tkinter`. No more command-line prompts—enjoy a polished interface with a dark gaming theme, interactive elements, intelligent hints, and dynamic scoring.

## Features
- **Standalone GUI App:** Fully windowed experience; no terminal input required.
- **Modern UI Design:** Clean, dark-themed layout with flat buttons, emojis, and clear typography.
- **Difficulty Modes:** EASY (1-50), MEDIUM (1-100), and HARD (1-500).
- **Persistent Statistics:** Tracks your Games Played, Win Rate, and Best Score across sessions using local JSON storage.
- **Intelligent Hint System:** Automatically provides Even/Odd and Range hints when you're struggling.
- **Robust Error Handling:** Alerts for empty inputs, out-of-range guesses, and text-in-number fields, ensuring the game never crashes.

## Technologies Used
- **Python 3.x**
- **Tkinter** (Python's standard GUI library)
- `random` for game logic
- `json` for statistics storage

## Project Structure
```text
guess-number-game/
│
├── main.py            # Main GUI application script
├── stats.json         # Automatically generated file for saving statistics
└── README.md          # Project documentation
```

## How to Play
1. Launch the application.
2. Enter your name and select a difficulty.
3. Click **START GAME**.
4. Type your guess into the box and hit **Enter** (or click **SUBMIT**).
5. Watch the feedback. If you get stuck, hints will appear automatically!
6. Check the **STATISTICS** screen to see your overall performance.

## How to Launch Without CMD (Double-Click Setup)
You can launch this application simply by double-clicking it, completely avoiding the terminal!

**Method 1: Rename the file extension (Recommended for Windows)**
1. Right-click `main.py` and rename it to `main.pyw`. 
2. The `.pyw` extension tells Windows to run the application using `pythonw.exe` in the background, which hides the black CMD window. 
3. Now you can just double-click `main.pyw` to open the game like a real desktop app!

**Method 2: Create a Shortcut**
1. Right-click on your desktop, select `New > Shortcut`.
2. For the location, type: `pythonw.exe "C:\Users\prave\OneDrive\Documents\Desktop\Cognifyz Task 1\guess-number-game\main.py"`
3. Name it "Guess the Number" and double-click the shortcut to play.

## Testing Performed
- **GUI Interactions:** Verified button clicks, Return key bindings, and screen transitions.
- **Input Validation:** Confirmed that non-numeric characters, blank submissions, and duplicate guesses trigger non-intrusive UI warnings without crashing.
- **Game Logic:** Tested score deduction limits (never drops below 0), hint thresholds (2 and 4 wrong guesses), and correct range boundaries for all difficulties.
- **Persistence:** Verified `stats.json` accurately saves and loads session history.
