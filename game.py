from enum import Enum
import random

class CombinationType(Enum):
    SKIP = "Skip"
    ACES = "Aces"
    TWOS = "Twos"
    THREES = "Threes"
    FOURS = "Fours"
    FIVES = "Fives"
    SIXES = "Sixes"
    CHANCE = "Chance"
    THREE_OF_A_KIND = "Three of a Kind"
    FOUR_OF_A_KIND = "Four of a Kind"
    FULL_HOUSE = "Full House"
    SMALL_STRAIGHT = "Small Straight"
    LARGE_STRAIGHT = "Large Straight"
    YAHTZEE = "Yahtzee"


class Layout:
    def __init__(self):
        self.dice = [0] * 5
        self.locked = [False] * 5

    def roll_dice(self):
        for i in range(5):
            if not self.locked[i]:
                self.dice[i] = random.randint(1, 6)

    def lock_dices(self, indices):
        for index in indices:
            self.locked[index] = True

    def unlock_dices(self):
        self.locked = [False] * 5

    def get_points(self, combination):
        if combination == CombinationType.ACES:
            return sum(d for d in self.dice if d == 1)
        elif combination == CombinationType.TWOS:
            return sum(d for d in self.dice if d == 2)
        elif combination == CombinationType.THREES:
            return sum(d for d in self.dice if d == 3)
        elif combination == CombinationType.FOURS:
            return sum(d for d in self.dice if d == 4)
        elif combination == CombinationType.FIVES:
            return sum(d for d in self.dice if d == 5)
        elif combination == CombinationType.SIXES:
            return sum(d for d in self.dice if d == 6)
        elif combination == CombinationType.CHANCE:
            return sum(self.dice)
        elif combination == CombinationType.THREE_OF_A_KIND:
            return self.check_n_of_a_kind(3)
        elif combination == CombinationType.FOUR_OF_A_KIND:
            return self.check_n_of_a_kind(4)
        elif combination == CombinationType.FULL_HOUSE:
            return self.check_full_house()
        elif combination == CombinationType.SMALL_STRAIGHT:
            return 30 if self.check_small_straight() else 0
        elif combination == CombinationType.LARGE_STRAIGHT:
            return 40 if self.check_large_straight() else 0
        elif combination == CombinationType.YAHTZEE:
            return 50 if self.check_yahtzee() else 0
        return 0

    def check_n_of_a_kind(self, n):
        counts = [self.dice.count(i) for i in range(1, 7)]
        if any(count >= n for count in counts):
            return sum(self.dice)
        return 0

    def check_full_house(self):
        counts = [self.dice.count(i) for i in range(1, 7)]
        if 3 in counts and 2 in counts:
            return 25
        return 0

    def check_small_straight(self):
        straights = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
        return any(s.issubset(set(self.dice)) for s in straights)

    def check_large_straight(self):
        return set(self.dice) in [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]

    def check_yahtzee(self):
        return len(set(self.dice)) == 1


class Player:
    def __init__(self, name):
        self.name = name
        self.layout = Layout()
        self.used_combinations = {}
        self.score = 0

    def reroll(self):
        self.layout.roll_dice()

    def lock_dices(self, indices):
        self.layout.lock_dices(indices)

    def unlock_dices(self):
        self.layout.unlock_dices()

    def get_points(self, combination):
        if combination not in self.used_combinations:
            points = self.layout.get_points(combination)
            self.used_combinations[combination] = points
            return points
        return 0

    def end_turn(self):
        self.layout.unlock_dices()
        self.score += sum(self.used_combinations.values())
        self.used_combinations.clear()


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

        combination_choices = [combination for combination in CombinationType]
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
    player_names = ["Alice", "Bob", "Charlie"]
    game = Game(player_names)
    game.start_game()
