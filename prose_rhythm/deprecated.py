def _u_to_v(self, word):
    '''
    Convert u in word to v.
    :param word: string
    :return: string
    '''
    word = list(word.lower())

    # u at beginning of the word
    if word[0] == 'u' and word[1] in self.VOWELS and word[1] != 'u':
        word[0] = 'v'
    elif word[0] == 'u' and word[1] == 'u' and word[2] not in self.VOWELS:
        word[0] = 'v'
    elif word[0] == 'u' and word[1] == 'u' and word[2] in self.VOWELS:
        word[1] = 'v'

    # u in word
    for char in word:
        char_index = word.index(char)
        if char_index != len(word) - 1 and char == 'u':
            # consonant + u + vowel (that's not i)
            if len(word) > char_index + 2 and word[char_index - 1] not in self.VOWELS and word[
                char_index + 1] in self.VOWELS and word[
                char_index + 1] != 'u' and word[char_index + 1] != 'i' and word[
                char_index + 2] in self.VOWELS:
                word[char_index] = 'v'
            # vowel preceeds u and vowel follows
            if len(word) > 2 and word[char_index - 1] in self.VOWELS and word[char_index + 1] in self.VOWELS and word[
                char_index + 1] != 'u':
                word[char_index] = 'v'
            # consonant + u + u + vowel
            if len(word) > 3 and word[char_index - 1] not in self.VOWELS and word[char_index + 1] == 'u' and word[
                char_index + 2] in self.VOWELS:
                word[char_index + 1] = 'v'
            # consonant + u + i + consonant
            if len(word) > char_index + 2 and word[char_index - 1] not in self.VOWELS and word[
                char_index + 1] == 'i' and word[
                char_index + 2] not in self.VOWELS:
                word[char_index] = 'v'
            # i + u + u + vowel
            if len(word) > 3 and word[char_index - 1] == 'i' and word[char_index + 1] == 'u' and word[
                char_index + 2] in self.VOWELS:
                word[char_index + 1] = 'v'
    return ''.join(word)

    def _i_to_j(self, word):
        '''
        Convert i in word to j.
        :param word: string
        :return: string
        '''
        PREFIXES = ['ab', 'ad', 'ante', 'circum', 'cum', 'in', 'inter', 'ob', 'per', 'praeter', 'sub', 'subter', 'super', 'con']

        word_prefix = [prefix for prefix in PREFIXES if word.startswith(prefix)]
        word_prefix_end_index = len(word_prefix[0]) if len(word_prefix) == 1 else None

        word = list(word.lower())

        # i at the beginning of a word
        if word[0] == 'i' and word[1] in self.VOWELS:
            word[0] = 'j'

        # word has prefix
        if word_prefix_end_index != None and word_prefix_end_index < len(word) - 1 and word[word_prefix_end_index] == 'i':
            # prefix + i + vowel
            if word[word_prefix_end_index + 1] in self.VOWELS:
                word[word_prefix_end_index] = 'j'
            #prefix + i + consonant
            else:
                word.insert(word_prefix_end_index, 'j')

        return ''.join(word)

    def _i_u_to_j_v(self):
        '''
        Convert all u's and i's to v's and j's.
        Note that u to v converter must be used before i to j converter.
        :return:
        '''
        converted_text = []
        for word in self.text.split(' '):
            converted_word = self._i_to_j(self._u_to_v(word))
            converted_text.append(converted_word)
        return ' '.join(converted_text)