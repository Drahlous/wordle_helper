
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
      (best_word, score) = my_game.get_next_best_word()
      self.assertEqual(best_word, 'aab')
      self.assertEqual(score, 3)


    def test_tree(self):
      my_game = wh.Game()
      my_game.potential_words = [
          'aaa',
          'bab',
          'cca',
        ]
      print(my_game.get_next_best_word_from_tree())