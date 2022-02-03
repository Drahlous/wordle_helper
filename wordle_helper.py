#!/bin/python3
from enum import Enum, auto
import string
import subprocess

class Game():
    class CharacterStatus(Enum):
        VALID = auto()
        MISPLACED = auto()
        INVALID = auto()

    def __init__(self, number_of_characters = 5):
        self.number_of_characters = number_of_characters
        self.potential_words = set(sorted(self.get_word_list()))
        self.required_characters = set()
        self.character_positions = [set(string.ascii_lowercase) for _ in range(number_of_characters)]
        best_word = self.get_next_best_word()
        print(f'To start, you should probably choose: "{best_word}"...\n\n\n')

    # We'll build our own wordlist from the american dictionary
    def get_word_list(self):
        p = subprocess.run('./get_words.sh', stdout=subprocess.PIPE)
        return p.stdout.decode('utf-8').splitlines()

    # Print the list of words that we could still submit as a guess
    def print_remaining_words(self):
        print('Here are the remaining words you might choose from:')
        words = list(self.potential_words)
        num_columns = 10
        rows = [words[i:i+num_columns] for i in range(0, len(words), num_columns)]
        for row in rows:
            print(' '.join(row))
        print()

    # Remove a word from our list of potential words
    def remove_word(self, word):
        self.potential_words.discard(word)

    # Check if the input word meets current constraints
    def check_valid(self, word):
        # If this word doesn't have one of the required characters, throw it out
        for letter in self.required_characters:
            if letter not in word:
                return False

        # If one of the letters in this word is not valid for that position, throw it out
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
            if status is self.CharacterStatus.VALID:
                self.character_positions[pos] = set(char)

            # If this spot is invalid, remove it from every alphabet
            elif status is self.CharacterStatus.INVALID:
                # If this is a required character (was previously marked MISPLACED)
                # we'll just discard it from this position
                if char in self.required_characters:
                    self.character_positions[pos].discard(char)

                # Otherwise, we can discard it from ALL positions
                else:
                    [x.discard(char) for x in self.character_positions]

            # If the character is misplaced:
            # - Add to the 'required' set
            # - Remove from this position's dictionary
            elif status is self.CharacterStatus.MISPLACED:
                self.character_positions[pos].discard(char)
                self.required_characters.add(char)

    # Remove from our search space words which no longer satisfy our constraints
    def update_word_list(self):
        for word in list(self.potential_words):
            if not self.check_valid(word):
                self.remove_word(word)


    # Greedy Algorithm, pick the word that will eliminate the most other words
    def build_trie(self, wordlist):
        trie_list = [{} for _ in range(self.number_of_characters)]
        for word in wordlist:
            prev = 'Start'
            for tree, char in zip(trie_list, word):
                tree.setdefault(char, {'parents': {}})
                tree[char]["parents"].setdefault(prev, 0)
                tree[char]["parents"][prev] += 1
                prev = char
        return trie_list

    def get_word_score(self, trie_list, word):
        prev = None
        score = 0
        for trie, char in zip(trie_list, word):
            # Filter out the parent from the word we're currently in,
            # since we already counted that one!
            for parent in filter(lambda x: x != prev, trie[char]['parents']):
                score += trie[char]['parents'][parent]
            prev = char
        return score

    def get_highest_scoring_word(self, trie_list):
        max_score = 0
        best_word = None
        for word in self.potential_words:
            score = self.get_word_score(trie_list, word)
            if score > max_score or best_word is None:
                best_word, max_score = word, score
        return (best_word, max_score)

    def get_next_best_word(self):
        trie_list = self.build_trie(self.potential_words)
        return self.get_highest_scoring_word(trie_list)


    # Update game state
    def update(self, result):

        # Unpack the guess into a string
        (letters, _) = zip(*result)
        guess = ''.join(letters)
        print(f'You guessed: {guess}')

        # Check if we've won
        if all(status == self.CharacterStatus.VALID for (_, status) in result):
            print('Congratulations, you found the correct word!')
            return

        # Update the set of valid characters for each position
        self.update_positional_knowledge(result)

        # Update the set of valid words remaining
        self.update_word_list()

        # Print the list of remaining words
        self.print_remaining_words()

        # Find the next best word
        best_word = self.get_next_best_word()
        print(f'You should probably choose: "{best_word}"...\n')
