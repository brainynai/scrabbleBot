from collections import deque

class trie:
    searchResults = []
    
    def __init__(self):
        self.leafs = {}
        self.word = None

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
                self.leafs[nextLetter] = trie()
                self.leafs[nextLetter].addWord(word, pos+1)

    def scrabbleSearch(self, letterList):
        #print(f'Node: {self.word}')
        if not self.word is None:
            #print(self.word)
            trie.searchResults.append(self.word)
            
        tried = []    
        for i in range(len(letterList)):
            c = letterList.popleft()
            if c in self.leafs and c not in tried:
                #print(f'down for {c} with {letterList}')
                self.leafs[c].scrabbleSearch(letterList)
                tried.append(c)
            letterList.append(c)

    @staticmethod
    def getResults():
        l = trie.searchResults
        trie.searchResults = []
        return l


def main():
    t = trie()
    with open('lowerWords.txt') as f:
        for word in f:
            if word.strip().isalpha():
                t.addWord(word.strip())

    t.scrabbleSearch(deque('pplea'))
    foundWords = trie.getResults()
    print('\n'.join(sorted(foundWords, key=len)))


if __name__ == '__main__':
    main()

    
