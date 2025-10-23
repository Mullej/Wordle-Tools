'''
combined_wordlist.txt -> 12972 words accepted by the official wordle game. It's length is equivalent to: |official_allowed_guesses| + |future_answers| + |past_answers| - |discrepancies| = |official_allowed_guesses| + |shuffled_real_wordles|
discrepancies.txt -> 22 words past that was not supposed to become a wordle, but ended up as one. Thus, these words are a subset of official_allowed_guesses and past_answers.
future_answers.txt -> 828 words that will become wordles. Equivalent to: combined_wordlist - official_allowed_guesses - past_answers
official_allowed_guesses.txt -> 10657 allowed guesses game that will never become wordles themselves.
past_answers.txt -> 1511 new bank of past answers.
shuffled_real_wordles.txt -> 2315 wordle answers i.e. future_answers on day 0
'''
import os 

FILES = ('combined_wordlist.txt', 'discrepancies.txt', 'future_answers.txt', 'official_allowed_guesses.txt', 'past_answers.txt', 'shuffled_real_wordles.txt', 'todays_wordle.txt')

def get_files_in_dir(*, dir='word_data'):
    fs = [f for f in os.listdir(f'./{dir}/') if f[-4:]=='.txt']
    return tuple(fs)
    

def get_file_sizes_dict(*, dir='word_data'): 
    d = {}
    for n in get_files_in_dir():
        with open(f'{dir}/{n}') as f:
            d[n] = len(list(f))
    return d