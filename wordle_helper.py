#!/bin/python3
import string
from enum import Enum, auto
import subprocess

def get_words():
    p = subprocess.run('./get_words.sh', stdout=subprocess.PIPE)
    return p.stdout.decode('utf-8').splitlines()

class CharacterStatus(Enum):
    VALID = auto()
    MISPLACED = auto()
    INVALID = auto()

class Game():
    def __init__(self):
        self.potential_words = set(get_words())
        self.required_characters = set()
        self.character_positions = [set(string.ascii_lowercase) for _ in range(5)]

    # Check if the input word meets current constraints
    def check_valid(self, word):
        # If this word doesn't have one of the required characters, throw out the word
        for letter in self.required_characters:
            if letter not in word:
                return False
        # If one of the letters in this word is not valid for that position, throw out the word
        for (letter, alphabet) in zip(word, self.character_positions):
            if letter not in alphabet:
                return False
        # Otherwise, the word could be a valid choice
        return True

    # Update our knowledge of the positions
    def update_positional_knowledge(self, result):
        for (pos, (char, status)) in enumerate(result):
            # If this spot is valid:
            # - Remove every other character from this location's alphabet
            # - Remove this character from the dictionaries of all other positions
            if status is CharacterStatus.VALID:
                self.character_positions[pos] = set(char)

            # If this spot is invalid, remove it from every alphabet
            elif status is CharacterStatus.INVALID:
                [x.discard(char) for x in self.character_positions]

            # If the character is misplaced:
            # - Add to the 'required' set
            # - Remove from this position's dictionary
            elif status is CharacterStatus.MISPLACED:
                self.character_positions[pos].discard(char)
                self.required_characters.add(char)

    # Remove from our search space words which no longer satisfy our constraints
    def update_word_list(self):
        for word in list(self.potential_words):
            if not self.check_valid(word):
                self.potential_words.discard(word)

    # Print the list of words that we could still submit as a guess
    def print_remaining_words(self):
        print('Here are the remaining words you might choose from:')
        [print(word) for word in sorted(list(self.potential_words))]
        print()

    # Update game state
    def update(self, result):
        # Check if we've won
        if all(status == CharacterStatus.VALID for (_, status) in result):
            print('Congratulations, you found the correct word!')
            return

        # Update the set of valid characters for each position
        self.update_positional_knowledge(result)

        # Update the set of valid words remaining
        self.update_word_list()
        self.print_remaining_words()

