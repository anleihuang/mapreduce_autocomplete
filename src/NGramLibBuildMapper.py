#!/usr/bin/env python3

import sys
import re

def _read_file(filename):
    content = filename.read()
    # split content into stentences
    sentences = re.split(r' *[\.\?!][\'"\)\]]* *', content)
    for line in sentences:
        # we only care about alphabetic words
        # so replace all no alpha to space
        line = line.strip().lower().replace("\n", " ")
        line = re.sub("[^a-z]", " ", line)
        yield line.split()

def main(separator = "\\t"):
    """Job 1 Mapper - NGramLibBuild
    Dexcription: To Build N-Gram Libarary
    :param : nGramNumber

    input: files on HDFS
    outputKey: word(s)
    outputVal: 1
    """
    # input comes from STDIN (standard input)
    data = _read_file(sys.stdin)
    for words in data:
        len_words = len(words)
        if len_words < 2:
            continue
            
        for i in range(len_words):
            phrase_lst = []
            phrase_lst.append(words[i])
            # skip n-gram = 1 as is not needed
            # j startsed with n-gram = 2
            for j in range(1, len_words - i): 
                if j > nGramNumber - 1:
                    break
                phrase_lst.append(" ")
                phrase_lst.append(words[i + j])
                print("{PHRASE}{SEP}{VAL}".format(PHRASE = "".join(map(str, phrase_lst)), SEP = separator, VAL = 1))
            

if __name__ == "__main__":
    if len(sys.argv) > 1:
        nGramNumber = sys.argv[1]
    else:
        # set the N-gram granuality as default 3
        nGramNumber = 3 
    main()