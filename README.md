# tkinter-chess

**Autonomous Chess Playing Application**

About the program
- A chess game made using Python (tkinter GUI Library). It's capable of playing against the user using a a probabilistic algorithm.
- The algorithm calculates the best possible move by simulating multiple games over next two rounds and chooses the one with maximum probability of winning points (or in tight situations, minimum probability of losing points).

How to play
- Download the "game.pyw" file onto your device, and run it using a Python 3 interpreter

Quirks and Features
- If you edit the variable in line 17 (NUMBER_OF_HUMAN_PLAYERS) to '0' and run the program, the chess engine will play against itself from both sides.
- Similarly if you change that variable to '2', the game can be used by two users to play against each other.
