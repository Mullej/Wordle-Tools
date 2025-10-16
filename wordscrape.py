from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.request import Request
from datetime import datetime
import json, time

URLS = ('https://www.fiveforks.com/wordle/','https://www.nytimes.com/svc/wordle/v2/')
ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class AllPastAnswersScraper:
    '''
    The scraping object is attached to one specified URL
    You will need to create anoter instance to access a different site
    ''' 
    def __init__(self, *, index):

        self.url = URLS[index]
        self.url_name = urlparse(self.url).hostname
        self.lines = None

    def extract_past_answers(self):
        match self.url_name:
            case 'www.fiveforks.com':
                self.get_lines()
                self.past_answers = fiveforks_archive(self.lines)
            case 'www.rockpapershotgun.com':
                self.past_answers = rps_archive(self.lines)
            case 'www.nytimes.com':
                self.past_answers = nyt_archive()
    
    def store_past_answers(self, *, dir='word_data', name='past_answers.txt'):
        '''Exception raised if past_answers isn't a subset of scraped past answers'''

        new_list = list(map(lambda x: x+'\n', self.past_answers))
        with open(f'{dir}/{name}', 'r') as f:
            old_list = list(f)
        
        if not len(set(new_list)) == len(new_list) or not len(set(old_list)) == len(old_list):
            raise Exception('Duplicates in list')
        
        if not set(old_list).issubset(set(new_list)) :
            raise Exception('Old list is not subset')
        
        if set(old_list) == set(new_list):
            print('All past words are already recorded')
            return

        with open(dir+'/'+name, 'w') as f:
            try:
                i = input(f'Add {len(set(new_list) - set(old_list))} to {dir}/{name}? Y/N ' )
            except Exception:
                print('Aborted') 
            else:
                if i in {'Y', 'y'}: 
                    f.write(''.join(new_list))
                    print('Done')
                else:
                    raise Exception('Aborted')
    
    def get_lines(self):
        req = Request(self.url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7')
        self.lines = list(urlopen(req))
                
class TodaysWordle:
    
    def __init__(self):
        self.url = 'https://www.nytimes.com/svc/wordle/v2/' + formatted_date() + '.json'

    def get_wordle(self):
        self.dat = json.loads(list(urlopen(self.url))[0])
        self.todays_wordle = self.dat['solution']
        return self.todays_wordle
    
    def store_todays_wordle(self, *, dir='word_data', name='todays_wordle'):
        #check for name conflict
        self.get_wordle()
        with open(dir+'/'+name+'.txt', 'w') as f:
            f.write(self.todays_wordle)

class UpdatePastAnswers:
    '''Update archive instead of scraping the whole list.'''

#store dates
def fiveforks_archive(lines):
    if b'CIGAR 0 06/19/21</div>\n' not in lines:
        raise Exception('Bad data')
    
    #decoding to ascii doesn't work?
    lines = list(map(lambda x: x.decode(), lines))
    
    j = lines.index('CIGAR 0 06/19/21</div>\n')
    lines = lines[0:j+1]
    lines.reverse()
    
    z = list(map(lambda x: set(x[0:5]).issubset(set(ALPHA)) or x[6:7].isdigit(), lines))
    del lines[z.index(False):]

    j = dict(map(lambda t: (t[0:5].lower(), t[len(t)-15: len(t)-7]), lines))
    
    with open('word_data/word_dates.json', 'w') as f:
        json.dump(j, f)

    return list(map(lambda x: x[0:5].lower(), lines))

def update_future_answers(*, dir='word_data', name='future_answers'):
    '''Leaves out today's wordle (for now)'''

    with open(f'{dir}/{name}.txt', 'r') as f:
        a = set(f)
    
    with open(f'{dir}/past_answers.txt', 'r') as f:
        b = set(f)

    try:
        i = input(f'Remove {len(a&b)} words? Y/N ')
    except Exception:
        print('Aborted')
    else: 

        if i in {'Y', 'y'}:
            with open(f'{dir}/{name}.txt', 'w') as f:
                f.write(''.join(a - b))
        else:
            raise Exception("Aborted")

def nyt_archive():
    wordlist = []
    s = time.time()
    for d in DateIterator():
        req = Request(f'https://www.nytimes.com/svc/wordle/v2/{d}.json')
        #not sure which is fastest
        #dict(json.loads(list(urlopen(req))[0])['id']. or maybe create the list first and then convert to json
        wordlist.append(json.loads(urlopen(req).read())['solution'])
        
    print(time.time()-s)
    return wordlist

class DateIterator:

    def __init__(self):
        self.start_date_ordinal = 737959
        self.todays_ordinal = datetime.today().toordinal()

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.start_date_ordinal >= self.todays_ordinal:
            raise StopIteration
         
        self.start_date_ordinal += 1
        return datetime.fromordinal(self.start_date_ordinal).strftime('%Y-%m-%d')

def formatted_date():
    return datetime.today().strftime('%Y-%m-%d')

def lookup():
    pass 

def validate():
    '''Checks that word lists have the correct sizes and are without duplicates. Checks if past_answers is correct length, etc.'''

def rps_archive(lines):
    return []

def nyt_verify():
    pass