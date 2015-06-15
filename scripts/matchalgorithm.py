import nltk
from nltk.corpus import wordnet as wn

def match(original, typed):
    origWords = original.lower().split(" ")
    typedWords = typed.lower().split(" ")
    forNLTK = nltk.Text(nltk.word_tokenize(typed))
    points = 0
    length = lambda x: len(origWords)*x
    if origWords == typedWords:
        return 1.0
    def add(): points += 1
    matchPts = len([w for w in origWords if w in typedWords])/length(1.0)
    excessPts = len([w for w in typedWords if w not in origWords])/length(2.0)
    #similarPts = [wn.synset(w) for w in origWords]
    points = matchPts - excessPts
    print forNLTK
    #print similarPts
    return points


def lemmalist(str):
    syn_set = []
    for synset in wn.synsets(str):
        for item in synset.lemma_names:
            syn_set.append(item)
    return syn_set


def wordMatch(original, typed):
    origWords = original.lower().split(" ")
    typedWords = typed.lower().split(" ")
    points = 0
    for word in origWords:
        if word.lower() in typedWords:
            points += 1
            return points

test1 = "Man riding a bicycle with a banana"
test2= "man riding a bike with a fruit"

print match(test1, test2)
            
    
syns = wn.synsets("man")
for i in syns:
    for x in i.lemma_names:
        print x

