# WORDLE-Helper
## Outline
This repository holds the executables and source files of a program designed to assist a user with the game WORDLE by the New York Times.

The source files are composed of 3 Python files(main.py, styles.py, search.py), 1 csv(upper_wordle_csv.csv), and the Python virtual environment holding all of the imported libraries(.venv_linux and .venv_windows).

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
