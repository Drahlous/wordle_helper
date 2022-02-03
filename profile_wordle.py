import cProfile
import wordle_helper as wh

my_game = wh.Game()

print('Profiling brute force algorithm...')
cProfile.run('my_game.get_next_best_word_brute_force()')

print('Profiling prefix-tree algorithm...')
cProfile.run('my_game.get_next_best_word()')
