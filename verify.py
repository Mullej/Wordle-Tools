'''
combined_wordlist.txt -> 12972 words accepted by the official wordle game. It's length is equivalent to: |official_allowed_guesses| + |future_answers| + |past_answers| - |discrepancies| = |official_allowed_guesses| + |shuffled_real_wordles|
discrepancies.txt -> 22 words past that was not supposed to become a wordle, but ended up as one. Thus, these words are a subset of official_allowed_guesses and past_answers.
future_answers.txt -> 828 words that will become wordles. Equivalent to: combined_wordlist - official_allowed_guesses - past_answers
official_allowed_guesses.txt -> 10657 allowed guesses game that will never become wordles themselves.
past_answers.txt -> 1511 new bank of past answers.
shuffled_real_wordles.txt -> 2315 wordle answers i.e. future_answers on day 0
'''

FILES = ('combined_wordlist.txt', 'discrepancies.txt', 'future_answers.txt', 'official_allowed_guesses.txt', 'past_answers.txt', 'shuffled_real_wordles.txt', 'todays_wordle.txt')
WORDCOUNT = {'combined_wordlist.txt' : 12972, 'discrepancies.txt' : 22, 'official_allowed_guesses.txt' : 10657, 'shuffled_real_wordles.txt' : 2315}

class WordDataError(Exception):
    def __init__(self, filename, /, quantity = 'N/A'):
        self.filename = filename
        self.quantity = quantity

    def __str__(self):
        return f'{self.quantity} misplaced words in {self.filename}'

class WordLengthError(WordDataError):
    def __str__(self):
        return f'Incorrect length by {self.quantity} in {self.filename}'

class WordListManager:
    def __init__(self):
        self.dic = {}
        for file in FILES:
            with open(f'word_data/{file}', 'r') as f:
                self.dic[file] = set(f)
        
        self.lengths = list(map(lambda x: len(self.dic[x]), self.dic))
    
    def return_dictionary(self):
        return self.dic
    
    def check_lengths(self):
        check = ('combined_wordlist.txt', 'official_allowed_guesses.txt', 'shuffled_real_wordles.txt')
        
        for c in check:
            if not len(self.dic[c]) == WORDCOUNT[c]: 
                raise WordLengthError(c, len(self.dic[c]) - WORDCOUNT[c])

    def check_sets(self):
        if not self.dic['future_answers.txt'] & self.dic['past_answers.txt'] == set({}):
            raise WordDataError('future_answers.txt and/or past_answers.txt', f'{len(self.dic['future_answers.txt'] & self.dic['past_answers.txt'])}')
        
        if not self.dic['official_allowed_guesses.txt'] ^ self.dic['future_answers.txt'] ^ self.dic['past_answers.txt'] | self.dic['discrepancies.txt'] == self.dic['combined_wordlist.txt']:
            raise WordDataError('future_answers.txt, past_answers.txt, and/or discrepancies.txt', 
                                f'{len((self.dic['official_allowed_guesses.txt'] ^ self.dic['future_answers.txt'] ^ self.dic['past_answers.txt'] | self.dic['discrepancies.txt']) ^ self.dic['combined_wordlist.txt'])}')
        
        #^ since they should be disjoint
        if not self.dic['shuffled_real_wordles.txt'] ^ self.dic['official_allowed_guesses.txt'] == self.dic['combined_wordlist.txt']:
            raise WordDataError('shuffled_real_wordles.txt and/or official_allowed_guesses.txt', 
                                f'{len((self.dic['shuffled_real_wordles.txt'] & self.dic['official_allowed_guesses.txt']) ^ self.dic['combined_wordlist.txt'])}')
