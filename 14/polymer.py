#!/usr/bin/env python3
from itertools import pairwise
from collections import Counter


def main():
    from sys import argv
    with open(argv[1]) as file:
        seed, rules = read(file)

    print('part[1]:', runchk(seed, rules, 10))
    print('part[2]:', runchk(seed, rules, 40))


def runchk(seed, rules, n):
    return checksum(run(rules, pair_hist(seed), n), seed)


def checksum(pairs, seed):
    elems = Counter()
    # account for boundary, which is invariant across steps
    elems[seed[0]] += 1
    elems[seed[-1]] += 1

    for (l,r),n in pairs.items():
        elems[l] += n
        elems[r] += n

    hist = elems.most_common()
    return (hist[0][1] - hist[-1][1])//2  # NB pairs double count


def pair_hist(seed):
    return Counter(pairwise(seed))


def run(rules, hist, n):
    for _ in range(n):
        hist = step(rules, hist)
    return hist


def step(rules, src):
    dst = Counter()
    for sk,n in src.items():
        for dk in rules[sk]:
            dst[dk] += n
    return dst


def read(file):
    seed = tuple(file.readline().strip())
    file.readline()
    return seed, { sd[0]:sd[1] for l in file if (sd := parse_rule(l)) }


def parse_rule(line):
    s,d = line.strip().split(' -> ')
    # transform rules to precalculate generated pairs
    return tuple(s), ((s[0], d), (d, s[1]))


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    seed, rules = read(data('ex0.txt'))
    hist = pair_hist(seed)
    for exp in [
                'NCNBCHB',
                'NBCCNBBBCBHCB',
                'NBBBCNCCNBBNBNBBCHBHHBCHB',
                'NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB',
            ]:
        hist = step(rules, hist)
        assert hist == pair_hist(exp)
    assert runchk(seed, rules, 10) == 1588

def test1_answer(data):
    assert runchk(*read(data('input.txt')), 10) == 3906


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex0(data):
    assert runchk(*read(data('ex0.txt')), 40) == 2188189693529

def test2_answer(data):
    assert runchk(*read(data('input.txt')), 40) == 4441317262452


#------------------------------------------------------------------------------
def test_ex0(ascript):
    assert ascript('ex0.txt') == '''\
part[1]: 1588
part[2]: 2188189693529
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 3906
part[2]: 4441317262452
'''
