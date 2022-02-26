import os, sys
import re

vokal = ['a', 'i', 'u', 'e', 'o']
awalan = ["be", "me", "pe"]


def replacer(kata, pola):
    result = kata
    for p,r in pola.items():
        result = result.replace(p, r)
    return result


def unreplacer(kata, pola):
    result = kata
    for p,r in pola.items():
        result = result.replace(r, p)
    return result


def praproses(kata):
    result = []
    tmp = ""
    i=0
    inkonsonan = False
    numkonsonan = 0
    for karakter in kata:
        iskonsonan = (karakter not in vokal)
        if iskonsonan:
            if not inkonsonan:
                inkonsonan = True
            numkonsonan += 1
            tmp += karakter
        else:
            if inkonsonan:
                inkonsonan = False

                if len(tmp)==1:
                    result += [tmp+karakter]
                else:
                    result += [tmp[0], tmp[1:]+karakter]
                tmp = ""
            else:
                result += [karakter]
    if len(tmp)>0:
        result += [tmp]
    return result


def kaidah1(listsuku):
    global vokal
    result = []
    last = ""
    i = 0
    for suku in listsuku:
        if len(suku)==1 and i>0:
            if suku in vokal:
                result += [suku]
            elif listsuku[i-1][-1] in vokal:
                if i<len(listsuku)-1 and len(listsuku[i+1])==1 and listsuku[i+1][0] in vokal:
                    result += [suku]
                else:
                    result[-1] = result[-1] + suku
        else:
            result += [suku]
        i += 1
        last = suku
    return result


def kaidah2(listsuku):
    global vokal, awalan
    dift = ["$", "%", "^", "&", "*", "("]
    if len(listsuku)>1:
        if listsuku[0] in awalan and listsuku[1][0] not in vokal and listsuku[1][0] not in dift and len(listsuku[1])>2:
            listsuku[0] += listsuku[1][0]
            listsuku[1] = listsuku[1][1:]
        #if len(listsuku[0]) == 1
        if len(listsuku[0])==1 and listsuku[0].lower() not in vokal: # to make aki, Ahad, obat, etc as 2 syllables
            listsuku = [listsuku[0]+listsuku[1]] + listsuku[2:]
    return listsuku


### TODO: wrong for "permainan" and "dia"
def kaidah3(listsuku):
    global vokal
    result = []
    last = ""
    i = 0
    for suku in listsuku:
        if len(suku)==1 and i>0:
            if listsuku[i-1][-1] in vokal:
                result[-1] = result[-1] + suku
            else:
                result += [suku]
        else:
            result += [suku]
        i += 1
        last = suku
    return result


def pecah(kata):
    kdift = {"kh":"$", "ng":"%", "ny":"^", "sy":"&", "tr":"*", "gr":"("}

    """
    print(replacer(kata, kdift))
    suku = praproses(replacer(kata, kdift))
    print(suku)
    suku = kaidah1(suku)
    print("1 ", suku)
    suku = kaidah2(suku)
    print("2 ", suku)
    suku = kaidah3(suku)
    print("3 ", suku)
    return [unreplacer(s, kdift) for s in suku]
    """

    return [unreplacer(s, kdift) for s in kaidah3(kaidah2(kaidah1(praproses(replacer(kata, kdift)))))]


def get_total_syllables(reading):
    pattern = re.compile('([^\s\w]|_)+')
    clean_reading = pattern.sub('', reading)

    reading_words = clean_reading.split()
    total_syllables = 0
    for word in reading_words:
        word_syllables = pecah(word)
        total_syllables = total_syllables + len(word_syllables)

    return total_syllables