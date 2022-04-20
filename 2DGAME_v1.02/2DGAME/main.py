from game import *

game=Game()
""""
The main part only run game_loop in game.py
Use game_loop to control the whole game's running
"""
while game.running:
    game.game_loop()