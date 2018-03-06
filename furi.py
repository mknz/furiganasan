# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from janome.tokenizer import Tokenizer
import jctconv

TOKENS_KANJI = re.compile(u'[一-龠]+')  # kanji
TOKENS_KATAKANA = re.compile(u'[ァ-ヾ]+')  # katakana

def exist_kanji(string):
    res = TOKENS_KANJI.findall(string)  # check if it contains kanji
    if res != []:
        return True
    else:
        return False


def kanji_pos(string):
    '''Get kanji positions in the string. Assume only one kanji and hiragana pair.'''
    m = re.search(TOKENS_KANJI, string)
    if m is not None:
        return [m.start(), m.end()]
    else:
        return None


def non_kanji_pos(string):
    '''Get non-kanji positions in the string. Assume only one kanji and hiragana pair.'''
    kidx = kanji_pos(string)

    if kidx is None:
        return None

    kstart = kidx[0]
    kend = kidx[1]
    if kstart == 0:
        nstart = kend
        nend = len(string)
    else:
        nstart = 0
        nend = kstart

    return [nstart, nend]


def get_kanji_part_yomi(surface, reading):
    '''Get yomi of kanji part of the string. Assume only one kanji part.'''
    nkidx = non_kanji_pos(surface)
    if nkidx is None:
        return None

    non_kanji = surface[nkidx[0]:nkidx[1]]
    yomi = re.sub(jctconv.hira2kata(non_kanji), '', reading)

    # case of two separated hiragana part
    surface2 = surface[nkidx[1]:]
    nkidx2 = non_kanji_pos(surface2)
    if nkidx2 is None:
        return jctconv.kata2hira(yomi)

    non_kanji2 = surface2[nkidx2[0]:nkidx2[1]]
    yomi = re.sub(jctconv.hira2kata(non_kanji2), '', yomi)

    return jctconv.kata2hira(yomi)


def split_at_hiragana(surface, reading):
    '''Split at hiragana.'''
    kidx = kanji_pos(surface)
    if kidx is None:  # only non-kanji
        return [surface, reading]

    rest = surface[kidx[1]:]
    kidx2 = kanji_pos(rest)

    if kidx2 is None:  # only one kanji + hiragana
        return [surface, reading]

    hira = rest[:kidx2[0]]  # multiple kanji
    if hira == "々": # since this character is somehow defined as non-kanji
        return [surface, reading]

    m = re.search(r'(.*?' + jctconv.hira2kata(hira) + ')(.*)', reading)
    return [surface[:kidx[1]] + hira, m.group(1), surface[kidx[1]+1:], m.group(2)]


def create_yomi(s, r):
    '''Assumes one kanji-hiragana pair.'''
    kidx = kanji_pos(s)  # kanji index
    nkidx = non_kanji_pos(s)  # non-kanji index
    kyomi = get_kanji_part_yomi(s, r)

    rstring = ''
    if kyomi is None:
        rstring += s
    else:
        if kidx[0] < nkidx[0]:  # kanji + hiragana
            rstring += s[kidx[0]:kidx[1]]
            rstring += '('
            rstring += kyomi
            rstring += ')'
            rstring += s[nkidx[0]:nkidx[1]]
        else:  # hiragana + kanji + hiragana
            rstring += s[nkidx[0]:nkidx[1]]
            rstring += s[kidx[0]:kidx[1]]
            rstring += '('
            rstring += kyomi
            rstring += ')'
            rstring += s[kidx[1]:]

    return rstring


def add_yomi(string):
    t = Tokenizer()
    tokens = t.tokenize(string)

    rstring = ''
    for token in tokens:
        s = token.surface
        r = token.reading

        while True:
            res = split_at_hiragana(s, r)
            if len(res) > 2:
                rstring += create_yomi(res[0], res[1])
                s, r = res[2], res[3]
            else:
                break

        rstring += create_yomi(res[0], res[1])

    return rstring
