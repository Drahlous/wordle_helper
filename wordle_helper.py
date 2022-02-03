#!/bin/python3
from collections import defaultdict
import string
from enum import Enum, auto
import subprocess

class Game():
    class CharacterStatus(Enum):
        VALID = auto()
        MISPLACED = auto()
        INVALID = auto()

    def __init__(self):
        self.potential_words = set(sorted(self.get_word_list()))
        self.required_characters = set()
        self.character_positions = [set(string.ascii_lowercase) for _ in range(5)]
        best_word = self.get_next_best_word()
        print(f'To start, you should probably choose: "{best_word}"...\n\n\n')

    # We'll build our own wordlist from the american dictionary
    def get_word_list(self):
        p = subprocess.run('./get_words.sh', stdout=subprocess.PIPE)
        return p.stdout.decode('utf-8').splitlines()

    # Remove a word from our list of potential words
    def remove_word(self, word):
        self.potential_words.discard(word)

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

    # Print the list of words that we could still submit as a guess
    def print_remaining_words(self):
        print('Here are the remaining words you might choose from:')
        words = sorted(list(self.potential_words))
        num_columns = 10
        rows = [words[i:i+num_columns] for i in range(0, len(words), num_columns)]
        for row in rows:
            print(' '.join(row))
        print()

    # Just use a brute force solution, 
    # the search space is limited to american-english words
    def get_word_score_brute_force(self, word):
        remaining_words = set(self.potential_words.copy())
        for (index, char) in enumerate(word):
            for remaining_word in list(remaining_words):
                if remaining_word[index] == char:
                    remaining_words.discard(remaining_word)
        return len(self.potential_words) - len(remaining_words)

    # Greedy Algorithm, pick the word that will eliminate the most other words
    def get_next_best_word_brute_force(self):
        max_score = 0
        best_word = None

        for word in self.potential_words:
            score = self.get_word_score(word)
            if score > max_score or best_word is None:
                best_word, max_score = word, score
        return (best_word, max_score)

    def build_prefix_tree(self, wordlist):
        tree_list = [{} for _ in range(5)]
        # Build the tree
        for word in wordlist:
            prev = None
            for tree, char in zip(tree_list, word):
                
                if prev is None:
                    prev = 'Start'
                tree.setdefault(char, {'parents': {}})
                tree[char]["parents"].setdefault(prev, 0)
                tree[char]["parents"][prev] += 1
                prev = char
        return tree_list

    def get_word_score(self, prefix_tree, word):
        prev = None
        score = 0
        for tree, char in zip(prefix_tree, word):
            for parent in filter(lambda x: x != prev, tree[char]['parents']):
                score += tree[char]['parents'][parent]
            prev = char
        return score

    def get_next_best_word_from_tree(self, prefix_tree):
        max_score = 0
        best_word = None
        for word in self.potential_words:
            score = self.get_word_score(prefix_tree, word)
            if score > max_score or best_word is None:
                best_word, max_score = word, score
        return (best_word, max_score)        
                
    def get_next_best_word(self):
        prefix_tree = self.build_prefix_tree(self.potential_words)
        return self.get_next_best_word_from_tree(prefix_tree)


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
