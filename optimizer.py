import time
import list_operations as op

ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class IdealTriple:
    def __init__(self, future_answers):
        self.future_answers = future_answers

    def ideal_triple(self):
        self.ideals = count_similarity(generate_triples(find_candidates(self.future_answers)), self.future_answers)
        return self.ideals[0][0]

#maybe use collections module
def find_candidates(li):
    candidates = []

    a= op.letterFrequency(li)

    split = a[15:]
    frequencyCull = [i[0] for i in split]
    for w in li:
        candidates.append(w)
        for letter in frequencyCull:
            if letter in w:
                candidates.pop()
                break

    for i in range(len(candidates)):
        if len(set(candidates[i])) != len(candidates[i]):
            candidates[i] = None
    l = []
    for i in range(len(candidates)):
        if candidates[i] != None:
            l.append(candidates[i])
    candidates = l

    return candidates

def generate_triples(candidates):
    c = candidates
    start = time.time()
    triples = []

    for first in range(0,len(c)):
        for second in range(first+1, len(c)):
            for third in range(second+1, len(c)):
                if op.disjoint(c[first], c[second]) and op.disjoint(c[first], c[third]) and op.disjoint(c[second], c[third]):
                    triples.append((c[first], c[second], c[third]))

    print(time.time()-start)
    print(f'# of triples: {len(triples)}')
    return triples

def count_similarity(triples, l):
    x = []
    for t in triples:
        count = 0
        for w in l:
            for i in range(5):
                count+= (t[0][i]+t[1][i]+t[2][i]).count(w[i])
        x.append((t, count))
    return sorted(x, key=lambda x: x[1])[::-1]
