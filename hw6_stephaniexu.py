"""
15-110 Hw6 - Language Modeling Project
Name: Stephanie Xu
AndrewID: stephanx
"""

import hw6_language_tests as test

project = "Language" # don't edit this

### WEEK 1 ###

def loadBook(filename):
    f = open(filename, "r")
    f = f.read()
    text = f.split("\n")
    corpus = []
    for sentence in text:
        split =  sentence.split()
        corpus.append(split)
    return list(filter(None, corpus)) 

def getCorpusLength(corpus):
    count = 0
    for sentence in corpus:
        count += len(sentence)
    return count

def buildVocabulary(corpus):
    newCorpus = []
    for sentence in corpus:
        for word in sentence:
            if word not in newCorpus:
                newCorpus.append(word)
    return newCorpus

def countUnigrams(corpus):
    counter = {}
    for sentence in corpus:
        for word in sentence:
            if word not in counter:
                counter[word] = 1
            elif word in counter:
                counter[word] += 1
    return counter

def getStartWords(corpus):
    start = []
    for sentence in corpus:
        if sentence[0] not in start:
                start.append(sentence[0])
    return start

def countStartWords(corpus):
    counter = {}
    for sentence in corpus:
        if sentence[0] not in counter:
            counter[sentence[0]] = 1
        elif sentence[0] in counter:
            counter[sentence[0]] += 1
    return counter

def countBigrams(corpus):
    bigram = {}
    for sentence in corpus:
        for word in range(len(sentence)-1):
            if sentence[word] not in bigram:
                bigram[sentence[word]] = {}
            if sentence[word+1] not in bigram[sentence[word]]:
                bigram[sentence[word]][sentence[word+1]] = 1
            elif sentence[word+1] in bigram[sentence[word]]:
                bigram[sentence[word]][sentence[word+1]] += 1
    return bigram


### WEEK 2 ###

def buildUniformProbs(unigrams):
    prob = []
    n = len(unigrams)
    for unigram in unigrams:
        prob += [1/n]
    return prob

def buildUnigramProbs(unigrams, unigramCounts, totalCount):
    list = []
    d = unigramCounts
    for unigram in unigrams:
        count = d[unigram]
        prob = count/totalCount
        list += [prob]
    return list

'''
def buildBigramProbs(unigramCounts, bigramCounts):
    d = {}
    for word in bigramCounts.keys():
        d[word] = {}
        totalCounts = unigramCounts[word]
        for key1, value1 in bigramCounts.items():
            if word == key1:
                for key2, value2 in value1.items():
                    counts = value2
                    if "words" not in d[word]:
                        d[word]["words"] = [key2]
                    else:
                        d[word]["words"] += [key2]
                    prob = counts/totalCounts
                    if "probs" not in d[word]:
                        if prob == 1.0:
                            d[word]["probs"] = [1]
                        else:
                            d[word]["probs"] = [prob]
                    else:
                        d[word]["probs"] += [prob]
    return d
'''

def buildBigramProbs(unigramCounts, bigramCounts):
    d = {}
    for prevWord in bigramCounts.keys():
        words = []
        probs = []
        temp = {}
        for key,value in bigramCounts[prevWord].items():
            words.append(key)
            probs.append(value/unigramCounts[prevWord])
        temp["words"] = words
        temp["probs"] = probs
        d[prevWord] = temp
    return d


def getTopWords(count, words, probs, ignoreList):
    d = {}
    highestProb = 0
    potential = {}
    for i in range(len(words)):
        if words[i] not in d and words[i] not in ignoreList:
            if probs[i] >= highestProb:
                potential[words[i]] = probs[i]
    if len(potential) == count:
        return potential
    else:
        highestValues =  []
        for key,value in potential.items():
            if value > 0:
                if value not in highestValues:
                    highestValues.append(value)
        highestValues = sorted(highestValues)[::-1]
        while len(d) != count:
            for i in range(len(highestValues)):
                for key,value in potential.items():
                    if value == highestValues[i]:
                        d[key] = value
                        if len(d) == count:    
                            return d

from random import choices
def generateTextFromUnigrams(count, words, probs):
    sentence = ""
    wordsList = []
    for i in range(count):
        wordsList.append(choices(words, weights = probs))
    for words in wordsList:
        for i in words:
            sentence += i + " "
    return sentence


def generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs):
    sentence = ""
    list = []
    if len(list) == 0:
        startWord = choices(startWords, weights = startWordProbs)
        list += startWord
    for word in list:
        if len(list) < count:
            if word == ".":
                startWord = choices(startWords, weights = startWordProbs)
                list += startWord
            else:
                nextWord = choices(bigramProbs[word]["words"], weights = bigramProbs[word]["probs"])
                list += nextWord
        elif len(list) == count:
            for words in list:
                sentence += words + " "
            return sentence



### WEEK 3 ###

ignore = [ ",", ".", "?", "'", '"', "-", "!", ":", ";", "by", "around", "over",
           "a", "on", "be", "in", "the", "is", "on", "and", "to", "of", "it",
           "as", "an", "but", "at", "if", "so", "was", "were", "for", "this",
           "that", "onto", "from", "not", "into" ]
import numpy
import matplotlib

def graphTop50Words(corpus):
    unigram = buildVocabulary(corpus)
    unigramCounts = countUnigrams(corpus)
    totalCount = len(corpus)
    unigramProb = buildUnigramProbs(unigram, unigramCounts, totalCount)
    topWords = getTopWords(50, unigram, unigramProb, ignore)
    return barPlot(topWords,"The Top 50 Words in the Book")

def graphTopStartWords(corpus):
    start = getStartWords(corpus)
    startCount = countStartWords(corpus)
    totalCount = len(corpus)
    startProb = buildUnigramProbs(start, startCount, totalCount)
    topWords = getTopWords(50, start, startProb, ignore)
    return barPlot(topWords,"The Top 50 Starting Words in the Book")

def graphTopNextWords(corpus, word):
    unigramCounts = countUnigrams(corpus)
    bigramCounts = countBigrams(corpus)
    bigramProb = buildBigramProbs(unigramCounts,bigramCounts)
    topWords = getTopWords(10, bigramProb[word]["words"], bigramProb[word]["probs"], ignore)
    return barPlot(topWords, "The Top 10 Next Words After " + word)

def setupChartData(corpus1, corpus2, topWordCount):
    d = {}
    prob1 = []
    prob2 = []
    unigramProb1 = buildUnigramProbs(buildVocabulary(corpus1), countUnigrams(corpus1), getCorpusLength(corpus1))
    topWords1 = getTopWords(topWordCount, buildVocabulary(corpus1), unigramProb1, ignore)
    unigramProb2 = buildUnigramProbs(buildVocabulary(corpus2), countUnigrams(corpus2), getCorpusLength(corpus2))
    topWords2 = getTopWords(topWordCount, buildVocabulary(corpus2), unigramProb2, ignore)
    combined = list(topWords1.keys()) + list(topWords2.keys())
    combinedTopWords = []
    for word in combined:
        if word not in combinedTopWords:
            combinedTopWords.append(word)
    for words in combinedTopWords:
        if words in topWords1.keys():
            prob1.append(topWords1[words])
        elif words not in topWords1.keys():
            prob1.append(0)
    for words in combinedTopWords:
        if words in topWords2.keys():
            prob2.append(topWords2[words])
        elif words not in topWords2.keys():
            prob2.append(0)
    d["topWords"] = combinedTopWords
    d["corpus1Probs"] = prob1
    d["corpus2Probs"] = prob2
    return d

def graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title):
    chartData = setupChartData(corpus1, corpus2, numWords)
    return sideBySideBarPlots(chartData["topWords"], chartData["corpus1Probs"], chartData["corpus2Probs"], name1, name2, title)

def graphTopWordsInScatterplot(corpus1, corpus2, numWords, title):
    chartData = setupChartData(corpus1, corpus2, numWords)
    return scatterPlot(chartData["corpus1Probs"], chartData["corpus2Probs"], chartData["topWords"], title)


### WEEK 3 PROVIDED CODE ###

"""
Expects a dictionary of words as keys with probabilities as values, and a title
Plots the words on the x axis, probabilities as the y axis and puts a title on top.
"""
def barPlot(dict, title):
    import matplotlib.pyplot as plt
    names = list(dict.keys())
    values = list(dict.values())
    plt.bar(names, values)
    plt.xticks(names, rotation='vertical')
    plt.title(title)
    plt.show()

"""
Expects 3 lists - one of x values, and two of values such that the index of a name
corresponds to a value at the same index in both lists. Category1 and Category2
are the labels for the different colors in the graph. For example, you may use
it to graph two categories of probabilities side by side to look at the differences.
"""
def sideBySideBarPlots(xValues, values1, values2, category1, category2, title):
    import matplotlib.pyplot as plt
    x = list(range(len(xValues)))  # the label locations
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots()
    pos1 = []
    pos2 = []
    for i in x:
        pos1.append(i - width/2)
        pos2.append(i + width/2)
    rects1 = ax.bar(pos1, values1, width, label=category1)
    rects2 = ax.bar(pos2, values2, width, label=category2)
    ax.set_xticks(x)
    ax.set_xticklabels(xValues)
    ax.legend()
    plt.title(title)
    plt.xticks(rotation="vertical")
    fig.tight_layout()
    plt.show()

"""
Expects two lists of probabilities and a list of labels (words) all the same length
and plots the probabilities of x and y, labels each point, and puts a title on top.
Note that this limits the graph to go from 0x0 to 0.02 x 0.02.
"""
def scatterPlot(xs, ys, labels, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    plt.scatter(xs, ys)

    # make labels for the points
    for i in range(len(labels)):
        plt.annotate(labels[i], # this is the text
                    (xs[i], ys[i]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0, 10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center
    plt.title(title)
    ax.plot([0, 1], [0, 1], color='black', transform=ax.transAxes)
    plt.xlim(0, 0.02)
    plt.ylim(0, 0.02)
    plt.show()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    test.week1Tests()
    print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    test.runWeek1()

    ## Uncomment these for Week 2 ##

    print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    test.week2Tests()
    print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    test.runWeek2()


    ## Uncomment these for Week 3 ##

    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    test.runWeek3()

