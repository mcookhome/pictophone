from cStringIO import StringIO
import sys
import nltk
from nltk.corpus import wordnet as wn

test1 = "Man riding a bicycle with a banana"
test2= "man riding a bike with a fruit"

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout
    def __str__(self):
        return str(self._stringio.getvalue().splitlines())

def generateSyns(word):
    syns = []
    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            print lemma.name()

def findSynPts(origWords, typedWords):
    print origWords
    allSyns1 = []
    for w in origWords:
        with Capturing() as syns1:
            generateSyns(w)
        allSyns1.append(syns1)
    print allSyns1
        
    

def match(original, typed):
    #Prepare the strings
    origWords = original.lower().split(" ")
    typedWords = typed.lower().split(" ")
    forNLTK = nltk.Text(nltk.word_tokenize(typed))
    points = 0
    length = lambda x: len(origWords)*x

    #Exact match
    if origWords == typedWords:
        return 1.0
    
    #Check for exact words matches, check for difference in length
    matchPts = len([w for w in origWords if w in typedWords])/length(1.0)
    excessPts = len([w for w in typedWords if w not in origWords])/length(2.0)

    #Check for synonyms
    findSynPts(origWords, typedWords)
    
    points = matchPts - excessPts
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

match(test1, test2)

