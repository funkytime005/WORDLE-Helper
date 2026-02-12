def search_wordle_dict(df, green_letters, yellow_letters, gray_letters, duplicates):
    """
    search_wordle_dict searches provided dataframe for valid words given the parameter constraints.
    
    :param dict: WORDLE dataframe. Letters seperated by column.
    :param green_letters: 5-long list of letters designated as green.
    :param yellow_letters: Dictionary of letters mapping to the positions they have been found yellow.
    :param gray_letters: List of letters designated as gray.
    :param duplicates: List of letters designated as duplicates. Used to filter words with reoccuring letters.
    """

    # Keep a copy to avoid overwriting.
    wordle_df = df.copy()

    # Start with green letters. We have a 5-long list of green letters, so we filter out words that do not have this green letter in this position
    for idx, val in enumerate(green_letters):
        if val != '': # if there is a letter here,
            wordle_df = wordle_df[wordle_df[str(idx+1)] == val]
    
    # Then gray letters.
    # We have a list of gray letters.
    # Gray comes with complications. It is possible to have a gray and yellow/green at the same time.
    # This is indicative of no duplicate letters. In that case, we don't want to remove words of that letter, we want to remove words that have two of that letter.
    # Gray and yellow/green comes with the duplicate variable which holds how many confirmed duplicates we have.
    # If we have no confirmed number of duplicates, then we won't have a value in the duplicates variable.
    for val in gray_letters:
        if val in green_letters or val in yellow_letters.keys():
            if val in duplicates.keys(): # if its in duplicates, we know exactly how many there should be
                mask = wordle_df.apply(lambda row: (row == val).sum(), axis=1) == duplicates[val]
                # .sum() statement counts the amount of entries equal to that letter in that row, and we keep all = the amount we know there are
                wordle_df = wordle_df[mask]

        else: # normal gray letter removal
            mask = (wordle_df == val).any(axis=1)
            wordle_df = wordle_df[~mask]

    # Finally, yellow letters.
    # We have a list of yellow letters and places they cannot be. If there is a green letter as well, this is also an invalid place.
    # This is because if we have a yellow letter and a green letter, that means we have a duplicate letter.
    for val in yellow_letters.keys():
        valid_pos = ['1','2','3','4','5']

        # remove any green letters. blank out the string that later we can remove it
        for i in range(len(green_letters)):
            if green_letters[i] == val:
                valid_pos[i] = ''
        # now remove from the yellow_letters variable
        for i in yellow_letters[val]:
            valid_pos[i] = ''
        # now, go back through and remove the blank positions. do this backwards to preserve positions.
        for i in range(len(valid_pos)-1, -1, -1):
            if valid_pos[i] == '':
                del valid_pos[i]
        
        # take the valid positions that our letter can be in, and mask for a letter in any of those position.
        mask = wordle_df[valid_pos].isin([val]).any(axis=1)
        wordle_df = wordle_df[mask]
        # a word might have duplicate letters. this above check does not block letters from existing in the positions they are found yellow in.
        # it simply searches for yellow letters outside of where they can't be. so we now need to also narrow any words that have been found with duplicate letters in the yellow positions.
        yellow_pos = [str(i+1) for i in yellow_letters[val]]
        mask = wordle_df[yellow_pos].isin([val]).any(axis=1) # grab all words that have letters in the yellow positions, and remove them
        wordle_df = wordle_df[~mask]

    return wordle_df