'''
combined_wordlist.txt -> 12972 words accepted by the official wordle game. It's length is equivalent to: |official_allowed_guesses| + |future_answers| + |past_answers| - |discrepancies| = |official_allowed_guesses| + |shuffled_real_wordles|
discrepancies.txt -> 22 words past that was not supposed to become a wordle, but ended up as one. Thus, these words are a subset of official_allowed_guesses and past_answers.
future_answers.txt -> 828 words that will become wordles. Equivalent to: combined_wordlist - official_allowed_guesses - past_answers
official_allowed_guesses.txt -> 10657 allowed guesses game that will never become wordles themselves.
past_answers.txt -> 1511 new bank of past answers.
shuffled_real_wordles.txt -> 2315 wordle answers i.e. future_answers on day 0
'''

import list_operations as op
import wordscrape as scrape
import optimizer, verify

def content_dictionary(file_names, /, *, dir='word_data'):

    names = tuple(map(lambda s: s[:len(s)-4], file_names))
    
    l = []
    for n in file_names:
        if type(n) is not ''.__class__:
            raise TypeError('file_names content not type str')
        
        with open(dir+'/'+n, 'r') as f:        
            l.append(tuple(op.format_list(list(f))))
    
    return dict(zip(names, l))
    

#needs to update discrepancies
def update_lists():
    scrape.TodaysWordle().store_todays_wordle()
    scraper = scrape.AllPastAnswersScraper(index=0)
    scraper.extract_past_answers()
    scraper.store_past_answers()
    scrape.update_future_answers()

def get_ideal_triple(future_answers):
    return optimizer.IdealTriple(future_answers).ideal_triple()

def verify_data():
    v = verify.WordListManager()
    try:
        v.check_sets()
    except Exception: 
        pass
    v.check_lengths()

if __name__ == '__main__':
    verify_data()
    import sys
    
    if len(sys.argv) >= 2:
        match sys.argv[1]:
            case 'update_lists':
                update_lists()
            case 'commands':
                print('update_lists')
            case _:
                print('Unrecognized arguments')

    FILES = ('combined_wordlist.txt', 'official_allowed_guesses.txt', 'past_answers.txt', 'shuffled_real_wordles.txt', 'discrepancies.txt', 'future_answers.txt')
    cd = content_dictionary(FILES) 

    verify_data()


#docstring updater
#upload word_data to github
#compile list of all allowed guesses not in a common dictionary
#probability updater
#discrepancy updater
#add requirementes