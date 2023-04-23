# Tkinter Chess - An Autonomous Chess Playing Application  

With the modern andvancements in computer chess world like Deep Blue and AlphaZero, I wanted to try my hand at creating my own chess player algorithm. I went about making it the way I myself would play the game, which is basically trying to think a few moves ahead in time and choose the move thats gives me the most expected points.  
  
As I later found out, this algorithm is a primitive version of Reinforcement Learning.

![image](https://user-images.githubusercontent.com/83920669/233861228-5d4ebc82-4f3f-4459-a2a6-e51a77c72790.png)


About the program
- A chess game made using Python (tkinter GUI Library) capable of playing against the user using a probabilistic algorithm.
- The algorithm calculates the best possible move by simulating multiple games till depth of two moves and chooses the one with maximum probability of winning points (or in adverse situations, minimum probability of losing points).
- In other words a greedy algorithm that uses concepts of estimated costs and rewards from Reinforcement Learing.

How to play
- Download the "game.pyw" file onto your device, and run it using a Python 3 interpreter

Quirks and Features
- If you edit the variable in line 17 (NUMBER_OF_HUMAN_PLAYERS) to '0' and run the program, the chess engine will play against itself from both sides.
- Similarly if you change that variable to '2', the game can be used by two users to play against each other.
