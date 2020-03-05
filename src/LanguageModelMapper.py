#!/usr/bin/env python3

import sys

def main(seperator = "\\t"):
    """Job 2 Mapper - LanguageModel
    Dexcription: To Build Language Model
    :param : threshold: to discard words that is not frequent

    inputKey: first phrase + following words
    inputVal: Sum of the frequency
    outputKey: first phrase
    outputVal: following words + Sum of the frequency
    """
    for line in sys.stdin:
        line = line.strip().split(seperator, 1)
        len_line = len(line)

        if len_line < 2:
            continue

        words = line[0].split()
        count = line[1]

        # set an aurgument threshold to discard
        # those ingrequent words
        if int(count) < threshold:
            continue

        len_words = len(words)
        key = []

        for i in range(len_words - 1):
            key.append(words[i])

        key = " ".join(map(str, key))
        outval = words[-1]

        if key:
            print( "{KEY}{SEP}{OUTVAL}={OUTCNT}".format(KEY = key, SEP = seperator, OUTVAL = outval, OUTCNT = count)
    )
           

if __name__ == "__main__":
    if len(sys.argv) > 1:
        threshold = sys.argv[1]
    else:
        # set the threshold number as default 2
        threshold = 2
    main()