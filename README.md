# WORDLE-Helper
## Outline
This repository holds the executables and source files of a program designed to assist a user with the game WORDLE by the New York Times.

The source files are composed of 3 Python files(main.py, styles.py, search.py), 1 CSV(upper_wordle_csv.csv), and the Python virtual environment holding all of the imported libraries(.venv_linux and .venv_windows).

## How the game works, how the program helps
WORDLE is a game developed by the New York Times. You are given 6 chances to guess a 5 letter word. You gain information by guessing a word and receiving feedback on each letter. A letter marked as gray indicates that letter does not exist in the word or that there are no more duplicates of that letter in that word. A letter marked as yellow indicates that the letter does exist in the word, but at a different location. A letter marked as green indicates that the letter is in the correct position.

I ran into a common issue that at times I would have the information of my previous guesses in front of me and not be able to think of a word that would either grant me more information or be a legal/good guess. So the program I developed aims to intuitively allow a user to submit their current game state and retrieve a list of words that would put the user one step closer to the answer. This program does not work with any information theory to aid the user in guessing the word in as few guesses as possible(as done similarly in this very interesting [3Blue1Brown video]([url](https://www.youtube.com/watch?v=v68zYyaEmEA)) which inspired me to start this project), as I wanted to keep the spirit of WORDLE being the user tackling the puzzle rather than my developed program. Therefore, I decided to keep the program's usefulness to the end of just providing a list of possible words given the information.

## How to use the program
Opening the program has you greeted with this window:

<img width="958" height="682" alt="bb5d79bc029519e370b723503ecf323f" src="https://github.com/user-attachments/assets/116f0f98-006d-4ff6-8f4a-7483ab5c2d2e" />

Starting from the left is a 6 by 5 grid of white squares. These are the buttons and text input for the guesses a user has already made. Realistically, a user would only ever use the program for 5 of the 6 guesses, as the 6th would be game over, however for consistency to the original game's design I chose to have all 6 available to input.

Moving right is a large box above two buttons labelled 'Reset' and 'Submit'. Hitting the button 'Reset' returns the user to this current program state, a blank submission. Hitting the button 'Submit' takes the current program state, error checks the submission, and, in the large box above the two buttons, displays either the accumulated error messages to correct or the list of valid words to try.

Moving to the functionality of the program, lets say that a user has already tried two guesses for the WORDLE for February 16th, 2026, they have tried the words 'SLATE'(a common opener) and 'WORST' and received this information:

<img width="361" height="145" alt="image" src="https://github.com/user-attachments/assets/f9e3ce82-deb5-4682-b04a-b4b702ed4109" />

The user would then try to pass this information to the program. So we start by entering the two words, SLATE and WORST:

<img width="958" height="682" alt="4b474091386ca723a41fe9747e1118c8" src="https://github.com/user-attachments/assets/1d23de6f-d76e-4940-970d-210e42bbdd70" />

However, we now see that we lack the colors that we have learned which provide us that valuable information. The way that I have developed this program to work, is that each letter display is a button. Clicking on these buttons cycles the letter to be gray, yellow, then green, back to gray. So now, we can select the right colors, and hit Submit:

<img width="958" height="682" alt="4b474091386ca723a41fe9747e1118c8" src="https://github.com/user-attachments/assets/49a89510-efbf-452f-b77d-24d667bb2612" />

Looking at our options, we see a couple words to try, most of which might not be words we recognize. The program does take into account WORDLE words that are legal but not necessarily in the rotation of possible solutions, so uncommon or older words are likely to appear, such as 'ROIST' and 'ROYST'. We also notice that among all of the words to try, we have the green letters O, S, and T in the appropriate positions, as well as an R at the beginning, since we have a yellow R in one of the only other spots where a letter can go. Since A is labeled as gray, 'ROAST' is ommitted. Otherwise, 'ROOST' definitely seems like a common enough word that would likely be a WORDLE solution, so we try 'ROOST':

<img width="385" height="448" alt="image" src="https://github.com/user-attachments/assets/3697f77a-7f27-406c-93b3-ab81f3dc72fc" />

Leading to a solution in 3 guesses! Not bad!


## The Files
All files are annotated that the thought process in their development is explained as well as a basic understanding of what each portion achieves is conveyed.
### main.py
The central python file which is referenced to run the program unpackaged. Holds the setup of the UI, button event resolutions, as well as the error-checking algorithms. Since the error-checking algorithm requires interaction with front-end UI elements, it has not been seperated into its own file.

### styles.py
A supplementary python file which holds all of the styling for different UI elements. 

### search.py
A supplementary python file which holds the search algorithm of the WORDLE word database. After main.py reads the input into a code-readable format for searching, the search algorithm returns a list of valid words to input as the next guess.

### upper_wordle_csv.csv
A data file holding all of the valid WORDLE words. Data is formatted that each letter of a word is seperated into its own column, that it forms a Nx5 sized dataset where N is the total number of valid words.

## Using the Program
Inside the dist folder are two files: main.exe and main. main.exe is intended to run on Windows systems. main is intended to run on Linux systems. As I do not own Apple products, I was not able to compile the program for use on an Apple system. Not intended to be used on mobile devices and tablets.

Through my own testing, the font size and window size do interact differently with different screen sizes.

Alternatively, if a user would like to run the program unpackaged, a user would clone or download the repo, open the appropriate virtual environment respective to their system, using the appriopriate command while in the project directory:

LINUX: `source .venv_linux/bin/activate` 

WINDOWS: `.\.venv_windows\Scripts\activate` if in CMD, `.\.venv_windows\Scripts\Activate.ps1` if in Powershell 

Then, running the following commands to run main.py while in the project directory:

Linux: `./.venv/bin/python ./main.py`

Windows: `& ".\.venv_windows/Scripts/python.exe" ".\main.py"`
