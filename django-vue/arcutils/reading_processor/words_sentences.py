import re

def word_count(str):
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts


def get_total_words(str):
    #return len(clean_text(str).split())
    #return len(re.findall("[a-zA-Z\-_]+", str)) # count layang-layang as 1 word
    return len(re.findall("[a-zA-Z_]+", str)) # count layang-layang as 2 words


def get_total_sentences(str):
    return str.count('.') + str.count('?') + str.count('!')