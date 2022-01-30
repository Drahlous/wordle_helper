# Wordle Helper

Work in progress.

Program to help solve word guessing games.

## Usage:

The tool is available as a docker image.
To show a sample game, run the command:
`docker run --rm -ti mattstachowiak/wordle_helper`

If you want to peek around inside and edit the code, open the container to the bash shell:
`docker run --rm -ti mattstachowiak/wordle_helper bash`
`python3 simulate_game.py`

```
 1. Decide on the word you want to guess, run check_valid to make sure it's still a valid guess

 2. Once you submit your guess on the website, enter the results you see for each letter

       - If the letter has a green background, you've put it in the correct place:
           mark this character with "CharacterStatus.VALID"

       - If the letter has a yellow backgroud, it is present in the word, but at a different location:
           mark this character with "CharacterStatus.MISPLACED"

       - If the letter has a black background, it doesn't occur anywhere in the word:
           mark it with "CharacterStatus.INVALID"

 3. Submit these results by running my_game.update:
       The program will print all remaining potential guesses
       Pick one of the words you see, and return to step (1)
```

