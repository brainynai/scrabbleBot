from collections import deque
import pickle
import os


class Settings:
    pickleName = 'pickleTrie.pckl'
    inputFile = 'lowerWords.txt'

    letterVal = {'a':1 , 'b':3, 'c':3, 'd':2, 'e':1,
                    'f':4, 'g':2, 'h':4, 'i':1, 'j':8,
                    'k':5, 'l':1, 'm':3, 'n':1, 'o':1,
                    'p':3, 'q':10, 'r':1, 's':1, 't':1,
                    'u':1, 'v':8, 'w':4, 'x':8, 'y':4, 'z':10}


class Trie:
    topNode = None
    searchResults = []
    
    def __init__(self):
        self.leafs = {}
        self.word = None

        if Trie.topNode is None:
            Trie.topNode = self

    def addWord(self, word, pos=0):
        if pos == len(word):
            self.word = word
            #print(f'added {word}, {pos}')
            return
        else:
            nextLetter = word[pos]
            if nextLetter in self.leafs:
                self.leafs[nextLetter].addWord(word, pos+1)
            else:
                self.leafs[nextLetter] = Trie()
                self.leafs[nextLetter].addWord(word, pos+1)

    def buildFromFile(self, filename=Settings.inputFile):
        pass  

    def scrabbleSearch(self, letterList):
        if not self.word is None:
            Trie.searchResults.append(self.word)
            
        tried = set()    
        for i in range(len(letterList)):
            c = letterList.popleft()
            if c in self.leafs and c not in tried:
                self.leafs[c].scrabbleSearch(letterList)
                tried.add(c)
            letterList.append(c)

    @staticmethod
    def pickleTrie():
        if Trie.topNode is None:
            return
        
        with open(Settings.pickleName, 'wb') as f:
            pickle.dump(Trie.topNode, f)

    @staticmethod
    def loadPickleTrie():
        with open(Settings.pickleName, 'rb') as f:
            pickledTrie = pickle.load(f)

        print('Loaded trie from file.')
        Trie.topNode = pickledTrie

        return pickledTrie

    @staticmethod
    def getNextFromFile(filename=Settings.inputFile):
        with open(filename) as f:
            for line in f:
                word = line.strip()
                if word.isalpha():
                    yield word
        yield None

    @staticmethod
    def getResults():
        l = Trie.searchResults
        Trie.searchResults = []
        return l

def scoreWordList(wordList):
    scoredList = [(word, sum(Settings.letterVal[char] for char in word)) for word in wordList]
    return scoredList

def main():
    if os.path.exists(Settings.pickleName):
        t = Trie.loadPickleTrie()
    else:
        t = Trie()
        with open(Settings.inputFile) as f:
            for word in f:
                if word.strip().isalpha():
                    t.addWord(word.strip())  #TODO: words are sorted. Can add a lot faster

    t.scrabbleSearch(deque('qzalkjag'))
    foundWords = Trie.getResults()
    scoredWords = sorted(scoreWordList(foundWords), key=lambda x:x[1], reverse=True)
    print('\n'.join(f'{word} : {score}' for word, score in scoredWords[:100]))

    if not os.path.exists(Settings.pickleName):
        t.pickleTrie()


if __name__ == '__main__':
    main()

    
