words = []
with open('words.txt') as f:
    for word in f:
            if word.strip().isalpha():
                lword = word.lower()
                words.append(lword)
                
with open('lowerWords.txt', 'a') as f2:
    f2.write('\n'.join(words))
