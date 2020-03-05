#!/usr/bin/env python3

import sys
from itertools import groupby
from collections import defaultdict

def _read_from_mapper(premapout, seperator = "\t"):
    for line in premapout:
        yield line.strip().split(seperator, 1)

def main(seperator ="\\t"):
    """Job 2 Reducer - LanguageModel
    Dexcription: To Build Language Model
    :param : topKNumber: to get the most frequent following word(s)

    inputKey: first phrase
    inputVal: 
    outputKey: first phrase
    outputVal: SUM(following words + Sum of the frequency)
    """
    data = _read_from_mapper(sys.stdin, seperator = seperator)
    
    for phrase, group in groupby(data, lambda x: x[0]):
        try:
            dic = defaultdict(list)
            for phrase, val in group:
                # phrase = "phrase"
                # val = "following=count"
                following = val.split("=")[0]
                count = int(val.split("=")[1])
                dic[count].append(following)
            
            # iterating through dictionary
            j = 1
            for key in sorted(dic.keys() , reverse = True):
                # set the argument "topKNumber" to get only the
                # most frequent following words
                if j > topKNumber:
                    break

                for word in dic[key]:
                    # here we overwrite the seperator as ":" is for Sqoop to
                    # successfully parsing data and store to MySQL
                    print("{PHRASE}{SEP}{FOLLOWING}{SEP}{COUNT}{SEP}".format(PHRASE = phrase, SEP = ":", FOLLOWING = word, COUNT = key))
                    j += 1
        except:
            pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        topKNumber = sys.argv[1]
    else:
        # set the top-k number as default 3
        topKNumber = 3 
    main()