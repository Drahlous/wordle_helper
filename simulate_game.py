# Simulate a player interacting with the game:
# 1. Decide on the word you want to guess, run check_valid to make sure it's still a valid guess
#
# 2. Once you submit your guess on the website, enter the results you see for each letter
#
#       - If the letter has a green background, you've put it in the correct place:
#           mark this character with "CharacterStatus.VALID
#
#       - If the letter has a yellow backgroud, it is present in the word, but at a different location:
#           mark this character with "CharacterStatus.MISPLACED
#
#       - If the letter has a black background, it doesn't occur anywhere in the word:
#           mark it with "CharacterStatus.INVALID"
#
# 3. Submit these results by running my_game.update:
#       The program will print all remaining potential guesses
#       Pick one of the words you see, and return to step (1)

from wordle_helper import Game, CharacterStatus
def SimulatePlayer():

    ## Game Start
    my_game = Game()

    my_game.check_valid('adieu')
    my_game.update([
        ('a', CharacterStatus.INVALID),
        ('d', CharacterStatus.MISPLACED),
        ('i', CharacterStatus.INVALID),
        ('e', CharacterStatus.INVALID),
        ('u', CharacterStatus.MISPLACED)
    ])

    my_game.check_valid('drunk')
    my_game.update([
        ('d', CharacterStatus.MISPLACED),
        ('r', CharacterStatus.INVALID),
        ('u', CharacterStatus.VALID),
        ('n', CharacterStatus.INVALID),
        ('k', CharacterStatus.INVALID)
    ])

    my_game.check_valid('would')
    my_game.update([
        ('w', CharacterStatus.INVALID),
        ('o', CharacterStatus.VALID),
        ('u', CharacterStatus.VALID),
        ('l', CharacterStatus.VALID),
        ('d', CharacterStatus.VALID)
    ])

    my_game.check_valid('could')
    my_game.update([
        ('c', CharacterStatus.VALID),
        ('o', CharacterStatus.VALID),
        ('u', CharacterStatus.VALID),
        ('l', CharacterStatus.VALID),
        ('d', CharacterStatus.VALID)
    ])

if __name__ == '__main__':
    SimulatePlayer()
