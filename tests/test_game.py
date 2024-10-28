import unittest
from unittest.mock import patch

from game import *

class TestYahtzeeGame(unittest.TestCase):
    def setUp(self):
        self.player = Player("Test Player")
        self.player.layout.dice = [1, 1, 2, 3, 3]

    def test_get_points_for_aces(self):
        points = self.player.get_points(CombinationType.ACES)
        self.assertEqual(points, 2)

    def test_get_points_for_twos(self):
        points = self.player.get_points(CombinationType.TWOS)
        self.assertEqual(points, 2)

    def test_get_points_for_three_of_a_kind(self):
        self.player.layout.dice = [3, 3, 3, 2, 1]
        points = self.player.get_points(CombinationType.THREE_OF_A_KIND)
        self.assertEqual(points, 12)

    def test_get_points_for_full_house(self):
        self.player.layout.dice = [3, 3, 3, 2, 2]
        points = self.player.get_points(CombinationType.FULL_HOUSE)
        self.assertEqual(points, 25)

    def test_lock_dices(self):
        self.player.lock_dices([0, 1])
        self.assertTrue(self.player.layout.locked[0])
        self.assertTrue(self.player.layout.locked[1])
        self.assertFalse(self.player.layout.locked[2])

    def test_unlock_dices(self):
        self.player.lock_dices([0, 1])
        self.player.layout.unlock_dices()
        self.assertFalse(any(self.player.layout.locked))

    @patch('random.randint', side_effect=[1, 2, 3, 4, 5])
    def test_reroll(self, mock_randint):
        self.player.reroll()
        self.assertEqual(self.player.layout.dice, [1, 2, 3, 4, 5])

    def test_player_score(self):
        self.player.get_points(CombinationType.ACES)
        self.player.end_turn()
        self.assertEqual(self.player.score, 2)

    def test_game_flow(self):
        game = Game(["Alice", "Bob"])
        game.players[0].layout.dice = [1, 2, 3, 4, 5]
        game.players[0].get_points(CombinationType.CHANCE)
        game.players[0].end_turn()
        self.assertEqual(game.players[0].score, 15)

        game.players[1].layout.dice = [6, 6, 6, 6, 2]
        game.players[1].get_points(CombinationType.FOUR_OF_A_KIND)
        game.players[1].end_turn()
        self.assertEqual(game.players[1].score, 26)


if __name__ == '__main__':
    unittest.main()
