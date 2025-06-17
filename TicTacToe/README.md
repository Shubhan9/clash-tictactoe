# Clash Royale Tic Tac Toe 🎮

A fun twist on the classic Tic Tac Toe game, themed with Clash Royale sound effects and clean UI. Play solo against a minimax AI or challenge a friend in PvP mode.

---

## 🎮 How to Play

- **X = Player 1**, **O = Player 2 / AI**
- First player to align 3 marks (row, column, or diagonal) wins.
- In PvP mode, a random Clash Royale sound plays after each move.
- On game end (win/loss/draw), themed sounds and a popup are triggered.

---

## 🕹 Controls

| Key         | Action                          |
|-------------|---------------------------------|
| `G`         | Toggle between PvP and AI mode  |
| `R`         | Reset the game                  |
| `0`         | Set AI to Easy (random)         |
| `1`         | Set AI to Hard (minimax)        |

Mouse click on any square to make your move.

---

## 🧠 AI Details

- **Level 0 (Easy):** Chooses random available squares.
- **Level 1 (Hard):** Implements the Minimax algorithm for perfect play.

---

## 🔊 Sound Triggers

| Event          | Sound Played                            |
|----------------|------------------------------------------|
| Win            | `win.mp3`                                |
| Loss           | `loss.mp3`                               |
| Draw           | `win.mp3` (or customize this if needed)  |
| PvP Move       | Random clash sound from `sound_effects/` |
| Background     | Looped `bg.mp3`                          |

---

## 🚀 How to Run

1. Make sure you have Python 3 installed.
2. Install dependencies:
   ```bash
   pip install pygame numpy
Ensure your working directory contains all files, and that all sound files are inside the sound_effects/ folder.

Run the game:
python main.py

---

## Video Demo 
For a demonstration check working.mp4 file in this repo
