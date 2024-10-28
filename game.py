from poker.player import Player
from poker.combinations import CombinationType

class Game:
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.current_player_index = 0

    def start_game(self):
        for _ in range(13):
            self.next_step()

    def next_step(self):
        current_player = self.players[self.current_player_index]
        print(f"It's {current_player.name}'s turn.")

        current_player.layout.roll_dice()
        print(f"Rolled dice: {current_player.layout.dice}")

        for _ in range(2):
            reroll_decision = input("Do you want to reroll some dice? (yes/no): ")
            if reroll_decision.lower() == 'yes':
                indices = input("Enter the indices of dice to lock this turn (comma-separated): ")
                indices = [int(i.strip()) for i in indices.split(",")]
                current_player.lock_dices(indices)
                current_player.reroll()
                current_player.unlock_dices()
                print(f"New dice: {current_player.layout.dice}")
            else:
                break

        used_combinations = current_player.used_combinations.keys()
        combination_choices = [combination for combination in CombinationType if combination not in used_combinations]
        print("Available combinations:")
        for i, combination in enumerate(combination_choices):
            if combination not in current_player.used_combinations:
                print(f"{i + 1}. {combination.value}")

        chosen_index = int(input("Choose a combination (number): ")) - 1
        chosen_combination = combination_choices[chosen_index]

        points = current_player.get_points(chosen_combination)
        print(f"{current_player.name} scored {points} points for {chosen_combination.value}.")

        current_player.end_turn()

        self.current_player_index = (self.current_player_index + 1) % len(self.players)

        if self.current_player_index == 0:
            print("End of round. Scores:")
            for player in self.players:
                print(f"{player.name}: {player.score} points")

if __name__ == "__main__":
    print("Enter the names of all players (comma-separated): ")
    player_names = [i.strip() for i in input().split(",")]
    game = Game(player_names)
    game.start_game()
