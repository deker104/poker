from layout import Layout

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

    def check_is_combination_not_used(self, combination):
        if combination in self.used_combinations:
            print('Combination was already used in this game, please choose other combination')
            return False
        return True

    def get_points(self, combination):
        if combination not in self.used_combinations:
            points = self.layout.get_points(combination)
            self.used_combinations[combination] = points
            return points
        return 0

    def end_turn(self):
        self.layout.unlock_dices()
        self.score += sum(self.used_combinations.values())
