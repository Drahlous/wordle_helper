from wordle_helper import Game

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

def SimulatePlayerJan29():

    ## Game Start
    my_game = Game()

    my_game.check_valid('adieu')
    my_game.update([
        ('a', my_game.CharacterStatus.INVALID),
        ('d', my_game.CharacterStatus.MISPLACED),
        ('i', my_game.CharacterStatus.INVALID),
        ('e', my_game.CharacterStatus.INVALID),
        ('u', my_game.CharacterStatus.MISPLACED)
    ])

    my_game.check_valid('drunk')
    my_game.update([
        ('d', my_game.CharacterStatus.MISPLACED),
        ('r', my_game.CharacterStatus.INVALID),
        ('u', my_game.CharacterStatus.VALID),
        ('n', my_game.CharacterStatus.INVALID),
        ('k', my_game.CharacterStatus.INVALID)
    ])

    my_game.check_valid('would')
    my_game.update([
        ('w', my_game.CharacterStatus.INVALID),
        ('o', my_game.CharacterStatus.VALID),
        ('u', my_game.CharacterStatus.VALID),
        ('l', my_game.CharacterStatus.VALID),
        ('d', my_game.CharacterStatus.VALID)
    ])

    my_game.check_valid('could')
    my_game.update([
        ('c', my_game.CharacterStatus.VALID),
        ('o', my_game.CharacterStatus.VALID),
        ('u', my_game.CharacterStatus.VALID),
        ('l', my_game.CharacterStatus.VALID),
        ('d', my_game.CharacterStatus.VALID)
    ])

def SimulatePlayerJan30():
    my_game = Game()
    my_game.check_valid('sales')
    my_game.update([
        ('s', my_game.CharacterStatus.INVALID),
        ('a', my_game.CharacterStatus.INVALID),
        ('l', my_game.CharacterStatus.INVALID),
        ('e', my_game.CharacterStatus.INVALID),
        ('s', my_game.CharacterStatus.INVALID)
    ])

    my_game.check_valid('corny')
    my_game.update([
        ('c', my_game.CharacterStatus.INVALID),
        ('o', my_game.CharacterStatus.INVALID),
        ('r', my_game.CharacterStatus.MISPLACED),
        ('n', my_game.CharacterStatus.VALID),
        ('y', my_game.CharacterStatus.INVALID)
    ])

    my_game.check_valid('bring')
    my_game.update([
        ('b', my_game.CharacterStatus.INVALID),
        ('r', my_game.CharacterStatus.VALID),
        ('i', my_game.CharacterStatus.INVALID),
        ('n', my_game.CharacterStatus.VALID),
        ('g', my_game.CharacterStatus.VALID)
    ])

def SimulatePlayerJan31():
    my_game = Game()

    # Note: This playthrough discovered a previously unknown rule that could cause an issue
    # 1. Make a guess that contains the same letter twice
    # 2. The solution contains a single instance of that letter
    # 3. The game will tell you that one of the instances is misplaced, while the other is INVALID
    #       This causes us to mark that character invalid for all positions, leaving us unable to find the solution

    my_game.check_valid('sores')
    my_game.update([
        ('s', my_game.CharacterStatus.INVALID),
        ('o', my_game.CharacterStatus.INVALID),
        ('r', my_game.CharacterStatus.INVALID),
        ('e', my_game.CharacterStatus.INVALID),
        ('s', my_game.CharacterStatus.INVALID)
    ])

    my_game.check_valid('palay')
    my_game.update([
        ('p', my_game.CharacterStatus.INVALID),
        ('a', my_game.CharacterStatus.INVALID),
        ('l', my_game.CharacterStatus.MISPLACED),
        ('a', my_game.CharacterStatus.INVALID),
        ('y', my_game.CharacterStatus.INVALID)
    ])

    # This guess will cause a problem, since the second "i" is marked invalid
    my_game.check_valid('blini')
    my_game.update([
        ('b', my_game.CharacterStatus.INVALID),
        ('l', my_game.CharacterStatus.MISPLACED),
        ('i', my_game.CharacterStatus.MISPLACED),
        ('n', my_game.CharacterStatus.INVALID),
        ('i', my_game.CharacterStatus.INVALID)
    ])

    my_game.check_valid('licit')
    my_game.update([
        ('l', my_game.CharacterStatus.VALID),
        ('i', my_game.CharacterStatus.VALID),
        ('c', my_game.CharacterStatus.INVALID),
        ('i', my_game.CharacterStatus.INVALID),
        ('t', my_game.CharacterStatus.VALID)
    ])

    my_game.check_valid('light')
    my_game.update([
        ('l', my_game.CharacterStatus.VALID),
        ('i', my_game.CharacterStatus.VALID),
        ('g', my_game.CharacterStatus.VALID),
        ('h', my_game.CharacterStatus.VALID),
        ('t', my_game.CharacterStatus.VALID)
    ])

if __name__ == '__main__':
    SimulatePlayerJan31()
