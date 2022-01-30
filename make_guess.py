#!/bin/python3
import string
from enum import Enum, auto
import subprocess

class CharacterStatus(Enum):
    VALID = auto()
    MISPLACED = auto()
    INVALID = auto()

def get_words():
    return subprocess.run('./get_words.sh', stdout=subprocess.PIPE).stdout.decode('utf-8')

words = set(get_words().splitlines())

positions = [set(string.ascii_lowercase) for _ in range(5)]
required_characters = set()
final_answer = [None for _ in range(5)]


def print_status(char_positions, required):
    print('Current Status:')
    print('Required Characters: ' + str(required))
    for alph in char_positions:
        print(sorted(alph))
    print('\n\n')

# Check if the input word meets current conditions
def check_valid(char_positions, required, word):
    for letter in required:
        if letter not in word:
            #print(word + ' NOT valid, does not contain a required char')
            return False

    for (letter, alphabet) in zip(word, char_positions):
        if letter not in alphabet:
            #print(word + ' NOT valid, ' + letter + ' is not in alphabet: ' + str(alphabet))
            return False
    print(word + ' is a potential answer')
    return True

# Update our knowledge of the positions
def update(char_positions, result):
    if all(status == CharacterStatus.VALID for status in result):
        print("Congratulations, you found the correct word!")

    for (pos, (char, status)) in enumerate(result):
        # If this spot is valid:
        # - Remove every other character from this location's alphabet
        # - Remove this character from the dictionaries of all other positions
        if status is CharacterStatus.VALID:
            # only needed if duplicates are not allowed: list(map(lambda x: x.discard(char), char_positions))
            char_positions[pos] = set(char)

        # If this spot is invalid, remove it from every alphabet
        elif status is CharacterStatus.INVALID:
            list(map(lambda x: x.discard(char), char_positions))

        # If the character is misplaced:
        # - Add to the 'required' set
        # - Remove from this position's dictionary
        elif status is CharacterStatus.MISPLACED:
            char_positions[pos].discard(char)
            required_characters.add(char)

    print_status(positions, required_characters)
    for word in list(words):
        if not check_valid(char_positions, required_characters, word):
            words.discard(word)


## Game Start
check_valid(positions, required_characters, 'adieu')
update(positions, [
    ('a', CharacterStatus.INVALID),
    ('d', CharacterStatus.MISPLACED),
    ('i', CharacterStatus.INVALID),
    ('e', CharacterStatus.INVALID),
    ('u', CharacterStatus.MISPLACED)
])

# Excluded = A, I, E
# Must have D, but not in [1]
# Must have U, but not in [4]

check_valid(positions, required_characters, 'drunk')
update(positions, [
    ('d', CharacterStatus.MISPLACED),
    ('r', CharacterStatus.INVALID),
    ('u', CharacterStatus.VALID),
    ('n', CharacterStatus.INVALID),
    ('k', CharacterStatus.INVALID)
])
# Excluded = A, I, E, R, N, K
# Must have D, but not in [1]
# Must have U, but not in [4]
# U, is in [2]

check_valid(positions, required_characters, 'would')
update(positions, [
    ('w', CharacterStatus.INVALID),
    ('o', CharacterStatus.VALID),
    ('u', CharacterStatus.VALID),
    ('l', CharacterStatus.VALID),
    ('d', CharacterStatus.VALID)
])

print(words)

check_valid(positions, required_characters, 'could')
update(positions, [
    ('c', CharacterStatus.VALID),
    ('o', CharacterStatus.VALID),
    ('u', CharacterStatus.VALID),
    ('l', CharacterStatus.VALID),
    ('d', CharacterStatus.VALID)
])
quit()

