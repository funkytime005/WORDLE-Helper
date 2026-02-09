#modules
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QComboBox, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtCore import Qt
import pandas as pd
import numpy as np
from styles import *
from search import *

#Class
class Wordle_App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.settings()

        self.color_state = np.ones((6,5), dtype=int) * -1
        self.word_pos = 0
        self.word_set = pd.read_csv('/home/jkuri005/PROJECTS/Wordle/upper_wordle_csv.csv', index_col=0)

        self.cut_word_set = self.word_set.copy()

    def initUI(self):
        # grid of wordle entries
        # Concept is to input a word, and then click the letters to match the color inputted
        # meaning that clicking letters should update from gray to yellow to green back to gray
        grid = QGridLayout()
        self.wordle_buttons = []
        for row in range(6):
            row_buttons = []
            for col in range(5):
                # create button
                button = QPushButton()
                # button settings
                button.setFixedSize(100,100)
                button.setStyleSheet(button_default)
                # use a lambda to pass button coords to handler
                button.clicked.connect(lambda x, r=row, c=col: self.matrix_button_handler(r,c))
                # add widget
                grid.addWidget(button, row, col)
                # store the reference
                row_buttons.append(button)
            # store the row of references
            self.wordle_buttons.append(row_buttons)
        
        # Reset Button
        self.reset = QPushButton("Reset")
        self.reset.setFixedSize(200,100)
        self.reset.clicked.connect(self.reset_app)

        # Submit Button
        self.submit = QPushButton("Submit")
        self.submit.setFixedSize(200,100)
        self.submit.clicked.connect(self.submit_state)

        # Word Results
        self.text_box = QTextEdit()
        self.text_box.setReadOnly(True)

        # Layout
        self.master = QHBoxLayout()
        self.col = QHBoxLayout()
        self.row = QVBoxLayout()
        
        self.col.addWidget(self.reset)
        self.col.addWidget(self.submit)

        self.row.addWidget(self.text_box)
        self.row.addLayout(self.col)
        
        self.master.addLayout(grid)
        self.master.addLayout(self.row)

        self.setLayout(self.master)

        self.setFocusPolicy(Qt.StrongFocus)


    def settings(self):
        self.setWindowTitle('Wordle Suggestor')
        self.setGeometry(2250,250,1200,1000)

    def matrix_button_handler(self, row, col):
        """
        Button handler for button matrix.
        Cycles color of button from gray > yellow > green > gray ...
        """
        clicked_button = self.wordle_buttons[row][col]
        self.color_state[row][col] += 1

        match self.color_state[row][col]:
            case 0:
                # print(f"Set {row},{col} color to gray")
                clicked_button.setStyleSheet(button_gray)
            case 1:
                # print(f"Set {row},{col} color to yellow")
                clicked_button.setStyleSheet(button_yellow)
            case 2: 
                # print(f"Set {row},{col} color to green")
                clicked_button.setStyleSheet(button_green)
            case _: # reset to 0
                # print(f"Set {row},{col} color to gray")
                clicked_button.setStyleSheet(button_gray)
                self.color_state[row][col] = 0
    
    def keyPressEvent(self, event):
        key = event.key()
        key_text = event.text()

        # if it's a letter and we aren't full, add it to the next box
        if key_text.isalpha() and self.word_pos < 30:
            row = self.word_pos // 5
            col = self.word_pos - (row*5)
            self.wordle_buttons[row][col].setText(key_text.upper())

            self.word_pos += 1
            # print(f"Set {row},{col} text to {key_text}")
        # if it's backspace, clear the last edited button and move back a box
        elif key == Qt.Key_Backspace and self.word_pos > 0:
            self.word_pos -= 1

            row = self.word_pos // 5
            col = self.word_pos - (row*5)
            self.wordle_buttons[row][col].setText("")

    def submit_state(self):
        # check if the current state is valid, if not throw errors
        err_string = """"""

        # No submission
        if self.word_pos == 0:
            err_string += "No words have been inputted."
            self.text_box.setText(err_string)
            return
        # not a full submission
        if self.word_pos%5 != 0:
            err_string += f"There is an incomplete word at row {(self.word_pos//5) + 1}.\n"
        
        word_inputs = pd.DataFrame(columns=['1','2','3','4','5'])
        # not a valid word, not all colors set, or repeated word
        for r in range(0, self.word_pos, 5):
            # check if a valid word
            row = self.wordle_buttons[r//5]
            sr = pd.Series([row[0].text(), row[1].text(), row[2].text(), row[3].text(), row[4].text()], index=['1','2','3','4','5'])
            
            # Mask to see if the series matches any row in the wordle database
            if not ((self.word_set[sr.index] == sr).all(axis=1)).any():
                err_string += f"The word {sr['1']+sr['2']+sr['3']+sr['4']+sr['5']} at row {(r//5) + 1} is not a valid word.\n"

            # check if all colors filled in for this row
            if (self.color_state[r//5] == -1).any():
                err_string += f"Row {(r//5) + 1} has unselected colors.\n"

            # check if the word has already been guessed previously
            if ((word_inputs[sr.index] == sr).all(axis=1)).any():
                err_string += f"The word {sr['1']+sr['2']+sr['3']+sr['4']+sr['5']} at row {(r//5) + 1} has already been used.\n"
            else:
                word_inputs = pd.concat([word_inputs, sr.to_frame().T], ignore_index=True)
        

        # if a valid word, pull words of each line into a readable format by code
        # we also now need to check if the colors are valid
        
        gray_letters = []
        yellow_letters = {}
        green_letters = ['', '', '', '', '']
        duplicates = {} # holds how many confirmed duplicates we have

        history = {} # holds yellow letters of found green letters. useful if duplicate letters appear.

        gray_added = [] # holds gray letters created this word. useful in error checking.

        for i in range(self.word_pos):
            # matrix position
            row = i//5
            col = i%5

            # reset the added variables per word
            if col == 0:
                gray_added = []

            cur_letter = self.wordle_buttons[row][col].text()
            # print(cur_letter)
            match self.color_state[row][col]:
                case 0: # adding gray
                    if cur_letter == green_letters[col]:
                        # print("  green > gray")
                        err_string += f"The letter {cur_letter} in column {col+1} became gray in the same column it was previously green.\n"
                        
                    
                    # yellow turns gray without finding green first. 
                    # if green was found previously, any yellow was moved to history. Therefore if the gray letter is in yellow_letters, it is illegal.
                    # the only case where this is complicated is if there is a green or yellow of the same letter in this word that has not been seen yet.
                    
                    # first check if it is in yellow
                    if cur_letter in yellow_letters.keys():
                        greens = self._list_of_color_indices(row, 2)
                        yellows = self._list_of_color_indices(row, 1)
                        # now check if it wont turn a different color this word
                        if (cur_letter not in greens) and (cur_letter not in yellows): # or empty
                            # there is no green or yellow letter this word, meaning error
                            # print("  yellow > gray")
                            err_string += f"The letter {cur_letter} in row {row+1}, col {col+1} became gray when it was previously yellow. Only legal if it stays yellow in this word or becomes/stays green in this word\n"
                        # else there is a yellow or green in this, meaning this gray is significant of the limit of duplicates in this word


                    # a gray is present when it should be green or yellow.
                    # if green was found previously, and it is not present and there is no yellow to point to it's existence, this gray should be yellow.
                    if cur_letter in green_letters:
                        # logic will be, if in current word the number of significant stored greens present plus the amount of significant yellows present matches
                        # or beats the number of significant stored greens, then it is legal
                        greens = 0
                        num_compete = 0
                        for idx,val in enumerate(green_letters):
                            if val == cur_letter:
                                num_compete += 1 # num stored in green letters increment
                                if self.wordle_buttons[row][idx].text() == cur_letter:
                                    greens += 1 # num greens stored in current word
                        yellows = len([val for val in self._list_of_color_indices(row, 1) if val == cur_letter]) # num yellows of current word
                        # if in current word num(yellows) + num(greens) >= num(stored in green_letters) then it's legal
                        if yellows + greens < num_compete:
                            err_string += f"The letter {cur_letter} in row {row+1}, col {col+1} is marked as gray when it should be yellow or green.\n"
                    
                    # if there is a gray and a green in the same word, we do not have a duplicate letter. History and yellow_letter for that letter can be deleted.
                    greens = self._list_of_color_indices(row, 2)
                    if cur_letter in greens:
                        if cur_letter in history.keys():
                            del history[cur_letter]
                        if cur_letter in yellow_letters.keys():
                            del yellow_letters[cur_letter]
                        
                    # if we have have a confirmation of how many of this letter is supposed to exist, add it to duplicates. if it's just zero, then don't add it.
                    cnt = 0
                    for idx,val in enumerate(self.wordle_buttons[row]):
                        if val.text() == cur_letter and self.color_state[row][idx] != 0:
                            cnt += 1
                    if cnt != 0:
                        duplicates[cur_letter] = cnt

                    # if we picked up no errors, add it to the list
                    if err_string == "":
                        if cur_letter not in gray_letters:
                            # print(f"Adding {cur_letter} to gray_letters")
                            gray_letters.append(cur_letter)

                            # print("adding to gray_added")
                            gray_added.append(cur_letter)

                case 1: # adding yellow
                    # green turns yellow in same column
                    if cur_letter == green_letters[col]:
                        # print("  green > yellow")
                        err_string += f"The letter {cur_letter} in column {col+1} became yellow in the same column it was green.\n"

                    # gray turns yellow
                    if cur_letter in gray_letters and cur_letter not in gray_added:
                        # legal if it wasn't gray in a previous word and made gray this word.
                        # if it is added later in the word, this technically qualifies as a green > gray error rather than gray > green
                        # print("  gray > yellow")
                        err_string += f"The letter {cur_letter} in row {row+1}, col {col+1} became yellow when it was previously gray.\n"
                    
                    # if it is already green and that green is not in this word, then we want to add to history.
                    # if it is green in the same word, then there is a duplicate letter.
                    #   > history should be moved back to yellow, and new position added if relevant.
                    # if two or more yellow in the same word, then there is a duplicate letter.
                    #   > history should be added back if relevant, and new positions added if relevant.

                    # grab the instances of green in this word
                    greens = self._list_of_color_indices(row, 2)
                    # if green is in this word
                    if cur_letter in greens: # duplicate letter
                        if cur_letter in history.keys(): # move history back to yellow
                            yellow_letters[cur_letter] = history.pop(cur_letter)
                            # letter will be added later
                    # if there is green just not in this word
                    elif cur_letter in green_letters: # add to history
                        # print(f"adding {cur_letter} to history")
                        # if entry doesn't exist yet, add it
                        if cur_letter not in history.keys(): 
                            # print("doesnt exist")
                            history[cur_letter] = [col]
                        # otherwise if the column hasn't been added yet, add it    
                        elif col not in history[cur_letter]: 
                            # print("exists")
                            history[cur_letter].append(col)
                        continue # it should not add to yellow_letters but we did not add to the err_string

                    # if we are reintroducing this letter as yellow or otherwise confirming through this yellow letter that there is a duplicate, we want to move history back to yellow_letters
                    if greens.count(cur_letter) >= 1: # duplicate letter
                        if cur_letter in history.keys(): # move history back to yellow
                            yellow_letters[cur_letter] = history.pop(cur_letter)
                            # letter will be added later

                    # if we picked up no errors, add it to the list
                    if err_string == "":
                        # if entry doesn't exist yet, add it
                        if cur_letter not in yellow_letters.keys(): 
                            # print(f"adding {cur_letter} to yellow_letters")
                            yellow_letters[cur_letter] = [col]

                        # otherwise if the column hasn't been added yet, add it
                        elif col not in yellow_letters[cur_letter]: 
                            # print(f"adding {cur_letter} to yellow_letters")
                            yellow_letters[cur_letter].append(col)
                    
                    
                case 2: # adding green
                    # green letter changes in same column
                    if green_letters[col] != '' and green_letters[col] != cur_letter:
                        # print("  green double")
                        err_string += f"The letter {cur_letter} and {green_letters[col]} in column {col+1} are both marked as green.\n"
                    # yellow letter becomes green in same column
                    if cur_letter in yellow_letters.keys(): # if it's even yellow
                        if col in yellow_letters[cur_letter]: # if it was yellow in this column
                            # print("  yellow > green")
                            err_string += f"The letter {cur_letter} in column {col+1} became green in the same column it was yellow.\n"
                    # gray turns green
                    if cur_letter in gray_letters and cur_letter not in gray_added:
                        # legal if it was made gray this word. means no duplicates. if it turns gray later in the word, handled in green > gray
                        # print("  gray > green")
                        err_string += f"The letter {cur_letter} in row {row+1} became green when it was previously gray.\n"

                    # if we picked up no errors, add it to the list
                    if err_string == "":
                        # print(f"adding {cur_letter} to green_letters")
                        green_letters[col] = cur_letter
                        

                    # move yellow letters to history if exists
                    if cur_letter in yellow_letters.keys():
                        # print(f"yellow letter {cur_letter} with positions {yellow_letters[cur_letter]} moved to history.")
                        history[cur_letter] = yellow_letters.pop(cur_letter)


        # If it's all valid in the end.
        self.text_box.setText(err_string)
        # print()
        # print(gray_letters)
        # print(yellow_letters)
        # print(green_letters)
        # print(duplicates)
        # print(history)
        if err_string != "":
            return
        
            
        # call function which returns list of valid words
        ret_df = search_wordle_dict(self.word_set, green_letters, yellow_letters, gray_letters, duplicates)

        # add words to/replace words in text box
        if len(ret_df) == 0:
            self.text_box.setText("Search has returned empty. This is likely due to the set of words inputted not yielding any valid words. Check to see if your words have all the correct colors.")

        else:
            word_string = ""
            for row_idx,row_val in ret_df.iterrows():
                word_string += row_val['1'] + row_val['2'] + row_val['3'] + row_val['4'] + row_val['5'] + '\n'
            self.text_box.setText(word_string)


    def _list_of_color_indices(self, row, color_ind):
        indices = np.where(self.color_state[row] == color_ind)[0] # retrieve all indices matching color_ind
        if indices.size != 0: # there are matches
            letter_set = []
            for idx in indices: # add all green letters found this word
                letter_set.append(self.wordle_buttons[row][idx].text())
            return letter_set
        return []

    def reset_app(self):
        """
        Functionality for reset button.
        Resets the wordle matrix to default state.
        """
        for row in range(6):
            for col in range(5):
                self.wordle_buttons[row][col].setStyleSheet(button_default)
                self.wordle_buttons[row][col].setText("")
                self.color_state[row][col] = -1
        self.word_pos = 0
        self.text_box.setText("")
        self.cut_word_set = self.word_set.copy()


if __name__ in "__main__":
    app = QApplication([])
    main = Wordle_App()
    main.show()
    app.exec_()
