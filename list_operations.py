ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def disjoint(a, b):
    try:
        return set(a).isdisjoint(set(b))
    except:
        print(set(a), set(b))        

def checkListDuplicates(l):
    t = []
    for w in l:
        if l.count(w) != 1:
            t.append(w)
    return t

def format_list(l):
    return list(map(lambda w: w[0:5], l))

def toFileString(l):
    return '\n'.join(l)+'\n'

def letterFrequency(list, n=26):
    temp = ''.join(list)
    l = [(a, temp.count(a)) for a in ALPHA.lower()]
    return sorted(l, key= lambda x: x[1])[::-1][0:n]

def checkDoubling(l):
    z = 0
    for i, m in list(enumerate(l)):
        for j in range(i+1, len(l)):
            if m[0] == l[j][0] and m[1] == l[j][1] or m[0] == l[j][1] and m[1] == l[j][0]:
                print(m, l[j])
                z+=1 