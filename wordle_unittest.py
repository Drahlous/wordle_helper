
import wordle_helper as wh
import unittest

class TestWordleHelper(unittest.TestCase):
    def test_best_score(self):
      my_game = wh.Game()
      my_game.potential_words = [
          'aaa',
          'aab',
          'bbb',
        ]
      (best_word, score) = my_game.pick_best_word()
      self.assertEquals(best_word, 'aab')
      self.assertEquals(score, 3)