from poker.player import Player
from poker.combinations import CombinationType
from poker.game import Game

if __name__ == "__main__":
    print("Enter the names of all players (comma-separated): ")
    player_names = [i.strip() for i in input().split(",")]
    game = Game(player_names)
    game.start_game()