import os 

FILES = ('combined_wordlist.txt', 'discrepancies.txt', 'future_answers.txt', 'official_allowed_guesses.txt', 'past_answers.txt', 'shuffled_real_wordles.txt', 'todays_wordle.txt')
STR = ("'''\ncombined_wordlist.txt -> {} words accepted by the official wordle game. It's length is equivalent to: |official_allowed_guesses| + |future_answers| + |past_answers| - |discrepancies| = |official_allowed_guesses| + |shuffled_real_wordles|\n"
       "discrepancies.txt -> {} words past that was not supposed to become a wordle, but ended up as one. Thus, these words are a subset of official_allowed_guesses and past_answers.\n"
       "future_answers.txt -> {} words that will become wordles. Equivalent to: combined_wordlist - official_allowed_guesses - past_answers\n"
       "official_allowed_guesses.txt -> {} allowed guesses game that will never become wordles themselves.\n"
       "past_answers.txt -> {} new bank of past answers.\nshuffled_real_wordles.txt -> 2315 wordle answers i.e. future_answers on day 0\n"
)

class DocStringUpdater:
    def __init__(self):
        self.__backedup = False

    def backup_main(self):
        with open('main.py') as f:
            x = f.read()
        with open('main_backup/main.py', 'w') as g:
            g.write(x)
        self.__backedup = True

    def create_new_text(self):
        if self.__backedup == False:
            print('No backup!')
            return
        
        with open('main.py') as f:
            old_lines = f.readlines()

        i = self.get_cutoff_index(old_lines)
        d = self.get_file_sizes_dict()
        s = STR.format(d['combined_wordlist.txt'], d['discrepancies.txt'], d['future_answers.txt'], d['official_allowed_guesses.txt'], d['past_answers.txt'])
        new_lines = s+''.join(old_lines[i::])
        self.new_lines = new_lines

    def write_to_file(self, /, *, f='main.py'):
        if self.__backedup == False:
            print('No backup!')
            return
        
        with open(f, 'w') as g:
            g.write(self.new_lines)

    def get_cutoff_index(self, program_text_as_array):
        return [i for i in enumerate(program_text_as_array) if i[1] == "'''\n"][1][0]
    
    def get_files_in_dir(self, *, dir='word_data'):
        fs = [f for f in os.listdir(f'./{dir}/') if f[-4:]=='.txt']
        return tuple(fs)

    def get_file_sizes_dict(self, *, dir='word_data'): 
        d = {}
        for n in self.get_files_in_dir():
            with open(f'{dir}/{n}') as f:
                d[n] = len(list(f))
        return d
    
def update():
    DSU = DocStringUpdater()
    DSU.backup_main()
    DSU.create_new_text()
    DSU.write_to_file()