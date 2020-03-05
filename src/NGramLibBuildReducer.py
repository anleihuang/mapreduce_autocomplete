#!/usr/bin/env python3

import sys
from itertools import groupby

def _read_from_mapper(premapout, seperator = "\t"):
    for line in premapout:
        yield line.strip().split(seperator, 1)


def main(seperator ="\\t"):
    """Job 1 Reducer - NGramLibBuild
    Dexcription: To Build N-Gram Libarary
    :param : nGramNumber

    inputKey: word(s)
    inputVal: 1
    outputKey: word(s)
    outputVal: Sum of the frequency
    """
    data = _read_from_mapper(sys.stdin, seperator = seperator)

    # grouping key: x[0] which is key
    for key, group in groupby(data, lambda x: x[0]):
        try:
            total_count = 0
            for key, count in group:
                total_count += int(count)
            print ("{KEY}{SEP}{CNT}".format(KEY = key, SEP = seperator, CNT = total_count))
        except ValueError:
            pass

if __name__ == "__main__":
    main()