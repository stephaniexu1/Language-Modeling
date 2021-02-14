from random import choices

def generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs):
    sentence = ""
    lst = []
    if len(lst) == 0:
        a = choices(startWords,weights=startWordProbs)[0]
        lst += [a]
    while len(lst) <= count:
        if len(lst) < count:
            if lst[len(lst)-1] == ".":
                b = choices(startWords,weights=startWordProbs)[0]
                lst += [b]
            else:
                prevWord = lst[-1]
                c = choices(bigramProbs[prevWord]["words"],weights = bigramProbs[prevWord]["probs"])[0]
                lst += [c]
        else:
            for word in lst:
                sentence += word + " "
            return sentence