import random
from poker.combinations import CombinationType

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
