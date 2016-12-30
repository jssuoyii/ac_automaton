import ac_automaton
import sys


class Filter(object):
    def __init__(self):
        bad_words = set()
        fp = open(sys.argv[1], 'rb')
        for word in fp:
            bad_words.add(word.strip('\n').decode('utf-8'))
        fp.close()
        self.ac = ac_automaton.Ac_automaton(bad_words)

    def get(self, text=''):
        text = text.decode('utf-8')
        ret = self.ac.search(text)
        if next(ret, None) == None:
            return False
        return True

    def replaced(self, text='', replaced_char='*'):
        replaced_text = ''
        text = text.decode('utf-8')
        charlist = list(text)
        ret = self.ac.search(text)
        print charlist
        for p in ret:
            charlist[p[0] + 1 - len(p[1]):p[0] + 1] = replaced_char * len(p[1])
        replaced_text = ''.join(charlist)
        return replaced_text
