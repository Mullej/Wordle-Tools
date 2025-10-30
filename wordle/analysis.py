import optimizer, json

#Fastest way to find the inverse of a map?
#Use cases maybe
def search_word_dates(search):
    with open("word_data/word_dates.json") as j:
        d1 = json.load(j)
    a = d1.items()
    d2 = {i[1]: i[0] for i in a}
    try:
        return d1[search]
    except KeyError:
        pass
    try:
        return d2[search]
    except KeyError:
        pass
    return None

def get_ideal_triple(future_answers):
    return optimizer.IdealTriple(future_answers).ideal_triple()
