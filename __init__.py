import os
import re
import shutil
from sw import *

ini = os.path.join(app_ini_dir(), 'syn_complete_from_text.ini')
ini0 = os.path.join(os.path.dirname(__file__), 'options.sample.ini')
if os.path.isfile(ini0) and not os.path.isfile(ini):
    shutil.copyfile(ini0, ini)
options = ini

def get_option(option, default):
    sresult = ini_read(options, 'main', option, default)
    if not sresult: sresult = default
    return sresult

def str_to_bool(sbool):
    return sbool.lower() == 'true'

option_lexers = get_option('lexers', '-,ini files,markdown,restructuredtext,properties')
option_min_len = int(get_option('min_len', '3'))
option_case_sens = str_to_bool(get_option('case_sens', 'true'))
option_use_acp = str_to_bool(get_option('use_acp', 'true'))
option_all_tabs = str_to_bool(get_option('all_tabs', 'false'))
option_prefix = get_option('prefix', 'w')
option_description = get_option('description', '')

def isword(s):
    return s.isalnum() or s=='_'

def is_text_with_begin(s, begin):
    if option_case_sens:
        return s.startswith(begin)
    else:
        return s.upper().startswith(begin.upper())


def get_words_list():
    text = ''
    if option_all_tabs:
        for h in ed_handles():
            text = text + '\n' + Editor(h).get_text_all()
    else:
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

def get_main_word(w):
    pos = w.find(' ')
    if pos > 0:
        pos2 = w.find(' ', pos+1)
        if pos2 > 0:
            return w[pos+1:pos2]
        else:
            return w[pos+1:len(w)]
    else:
        return w


def check_word(w, word1, word2):
    word = get_main_word(w)
    return is_text_with_begin(word, word1) and word != word1 and word != (word1+word2)

def get_acp_type(w):
    return w[0:w.find(' ')]

def get_acp_descr(w):
    pos = w.find('|')
    if pos > 0:
        return w[pos+1:len(w)]
    else:
        return

def get_acp_words(word1, word2):
    sfile = os.path.join(app_exe_dir(), 'Data', 'autocomplete', ed.get_prop(PROP_LEXER_CARET, '') + '.acp')
    if os.path.isfile(sfile):
        with open(sfile) as f:
            acp_lines = list(f)
            f.close()
        if not acp_lines: return
        acp_words = [get_main_word(w)+'|'+get_acp_type(w)+'|'+get_acp_descr(w) for w in acp_lines
                     if check_word(w, word1, word2)]
        #print('get_words_from_acp:', acp_words)
        return acp_words

class Command:
    def config(self):
        if os.path.isfile(ini):
            file_open(ini)
        else:
            print('Config file not created yet')

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

        if option_use_acp and word1:
            acp_words = get_acp_words(word1, word2)
        else:
            acp_words = []

        file_words = [w+'|'+option_prefix+'|'+option_description for w in words
                     if check_word(w, word1, word2)]

        #print('acp_words:', acp_words)
        #print('file_words:', file_words)
        words = []
        if acp_words:
            words = acp_words

        if file_words:
            words.extend(file_words)

        #print('word:', word)
        #print('list:', words)

        ed.complete('\n'.join(words), len(word1), True)
        return True
