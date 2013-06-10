#coding: utf-8
import sys 
"""
0 - S - Пики
1 - D - Бубны
2 - H - Червы
3 - C - Трефы

0x2 - 2 - 2
0x3 - 3 - 3
0x4 - 4 - 4
0x5 - 5 - 5
0x6 - 6 - 6
0x7 - 7 - 7
0x8 - 8 - 8
0x9 - 9 - 9
0xa - T - 10
0xb - J - Валет
0xc - Q - Дама
0xd - K - Король
0xe - A - Туз
"""
def SquareTriple(cards,size): #Запихнем проверку на тройки и четверки в один алгоритм, в силу схожести оных
    q = 0
    cur = cards[0][0]
    for card in cards:
        if q==size:
            return cur
        else:
            if card[0] == cur:
                q+=1
            else:
                q=1
                cur = card[0]
    return cur if q == size else 0

def Street(cards):
    cur = cards[0][0]
    for card in cards[1:]:
        if int(cur,16)+1 == int(card[0],16):
            cur = card[0]
        else:
            return 0
    return cur 
def Flash(cards):
    cur = cards[0]
    for card in cards[1:]:
        if card[1] == cur[1]:
            cur = card
        else:
            return 0
    return cur[0]
def Pairs(cards):
    cur = cards[0][0]
    pairs = []
    for card in cards[1:]:
        if cur == card[0]:
            pairs.append(card[0])
            cur = card[0]
        else:
            cur = card[0]
    return sorted(pairs)
def FullHouse(cards):
    triple = SquareTriple(cards,3)
    if not triple:
        return 0
    else:
        pairs = filter(lambda a: a != triple, Pairs(cards))
        if not pairs:
            return 0
        else:
            return triple
def StreetFlash(cards):
    s = Street(cards)
    f = Flash(cards)
    if s==f:
        return s
    else:
        return 0

def Combination(cards):
    sf = StreetFlash(cards)
    if sf:
        if sf == hex(0xe):
            return hex(0x90)                                            #Флеш рояль
        else:
            return hex(0x80 + int(sf,16))                               #Стрит флеш
    else:
        sq = SquareTriple(cards,4)
        if sq:
            return hex(0x70 + int(sq,16))                               #Каре
        else:
            fh = FullHouse(cards)
            if fh:
                return hex(0x60 + int(fh,16))                           #Фуллхаус
            else:
                f = Flash(cards)
                if f:
                    return hex(0x50 + int(f,16))                        #Флеш
                else:
                    s = Street(cards)
                    if s:
                        return hex(0x40 + int(s,16))                    #Стрит
                    else:
                        t = SquareTriple(cards,3)
                        if t:
                            return hex(0x30 + int(t,16))                #Тройка
                        else:
                            p = Pairs(cards)
                            if p:
                                if len(p)==2:
                                    return hex(0x20 + int(p[-1],16))    #2 пары
                                else:
                                    return hex(0x10 + int(p[0],16))     #пара
                            else:
                                return cards[-1][0]                      #Старшая карта


if len(sys.argv) != 3:
    print "Usage: HandChecker.py <input file name> <output file name>"
else:
    outfile = open(sys.argv[2],"w")
    with open(sys.argv[1]) as incarts:
        nominals = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13,'A':14}
        colors = {'S':0,'D':1,'H':2,'C':3}    
        for line in incarts:
            f = []
            s = []
            for cart in line.split(' ')[0:5]:
                f.append([hex(nominals[cart[0]]),colors[cart[1]]])
            for cart in line.split(' ')[5:10]:
                s.append([hex(nominals[cart[0]]),colors[cart[1]]])
            f = sorted(f)
            s = sorted(s)
            first = int(Combination(f),16)
            second = int(Combination(s),16)
            print >>outfile, 1 if first > second else 2
    outfile.close()