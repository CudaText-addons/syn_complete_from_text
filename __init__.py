import re
from sw import *

# '-' means none-lexer
option_lexers = '-,ini files,markdown,restructuredtext,properties,'
option_min_len = 3
option_case_sens = False
prefix = 'w'
  

def isword(s):
    return s.isalnum() or s=='_'

def is_text_with_begin(s, begin):
    if option_case_sens:
        return s.startswith(begin)
    else:
        return s.upper().startswith(begin.upper())


def get_words_list():
    text = ed.get_text_all()
    regex = r'\w{%d,}'%option_min_len
    l = re.findall(regex, text)
    if not l: return
    l = sorted(list(set(l)))
    return l


def get_word(x, y):
    if x==0: return
    n = ed.xy_pos(x, y)

    n0 = n
    while (n0>0) and isword(ed.get_text_substr(n0-1, 1)):
        n0 -= 1
    text1 = ed.get_text_substr(n0, n-n0)

    n0 = n
    while isword(ed.get_text_substr(n0, 1)):
        n0 += 1
    text2 = ed.get_text_substr(n, n0-n)

    return (text1, text2)


class Command:
    def on_complete(self, ed_self):
        carets = ed.get_carets()
        if carets: return
        x0, y0 = ed.get_caret_xy()

        lex = ed.get_prop(PROP_LEXER_CARET, '')
        if not lex: lex='-'
        allow = ','+lex.lower()+',' in ','+option_lexers.lower()+','
        if not allow: return

        words = get_words_list()
        #print('words:', words) ##
        word = get_word(x0, y0)
        #print('get_word:', word) ##
        if not words: return
        if not word: return
        word1, word2 = word

        words = [w+'|'+prefix for w in words 
                 if is_text_with_begin(w, word1) 
                 and w!=word1 
                 and w!=(word1+word2)
                 ]
        #print('word:', word)
        #print('list:', words)

        ed.complete('\n'.join(words), len(word1), True)
        return True
