# corpus of words that may be used in the context of the application
words = "buy to sell transfer send deposit withdraw stake borrow lend pay back payback redeem points convert usdt usd pkr sol eth btc"


# counter for all words in the corpus, which will be used to calculate the probability of a word
def counter(words):
    words = words.split()
    myDict = {}
    for word in words:
        myDict[word] = myDict.get(word, 0) + 1
    return myDict


# words stored with their counts (how many times they appear in the corpus)
WORDS = counter(words)


# calculate the probability of a word based on its frequency in the corpus
def P(word, N=sum(WORDS.values())):
    return (
        WORDS.get(word, 0) / N
    )  # probability of 0 means the word does not exist in the corpus


# strain out only the words that exist in WORDS (aka the right words)
def known(words):
    return set(w for w in words if w in WORDS)


# generate possible spelling corrections for a given word
def candidates(word):
    # return the first set of known words that are either the word itself, or one edit away, or two edits away, or just the word itself if no known words are found
    return known([word]) or known(edits1(word)) or known(edits2(word)) or [word]


# main function to correct a misspelled word based on max probability
def correction(word):
    return max(
        candidates(word.lower()), key=P
    )  # return the candidate with the highest probability


# bruteforcing all types of edits that are only 1 edit away from the word
def edits1(word):
    letters = (
        "abcdefghijklmnopqrstuvwxyz"  # all possible letters that can be used for edits
    )
    splits = [
        (word[:i], word[i:]) for i in range(len(word) + 1)
    ]  # split the word into all possible pairs of left and right substrings (i acts like a cursor that moves through the word)

    # 3 essential edits: insert, delete, replace
    inserts = [
        L + c + R for L, R in splits for c in letters
    ]  # inserting letters at every possible position in the word
    deletes = [
        L + R[1:] for L, R in splits if R
    ]  # deleting every character from the word
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]

    transposes = [
        L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1
    ]  # transpose the first two characters of the right substring

    return set(
        deletes + transposes + replaces + inserts
    )  # return only unique edits that are 1 edit away from the word


# bruteforcing all types of edits that are 2 edits away from the word
def edits2(word):
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


# separating commands from text and correcting any misspelled words in the commands
def command_parser(text):
    words = text.lower().split()
    commands = []
    for i in range(len(words)):
        word = words[i]
        if word == "to" or word.startswith("@") or word.isdigit():
            commands.append(word)
        else:
            commands.append(correction(word))
    return commands
