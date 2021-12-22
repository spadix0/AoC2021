#!/usr/bin/env python3
from itertools import count, product
from collections import Counter


def main():
    from sys import argv
    with open(argv[1]) as file:
        start = read(file)

    print('part[1]:', practice(start))
    print('part[2]:', max(count_wins(start)))


def count_wins(start):
    rolls = Counter(sum(r)
                    for r in product(range(1,3+1), repeat=3)) \
                .most_common()

    # dynamic subproblem state table for current roll:
    # number of games indexed by game state:
    #   (pos[0], pos[1], score[0], score[1])
    games = Counter()
    games[(*start, 0, 0)] = 1  # starting universe

    wins0, wins1 = 0, 0

    while games:
        prev, games = games, Counter()
        for (p0p,p1p, s0p,s1p), np in prev.items():
            assert s0p < 21 and s1p < 21
            for r0, nr0 in rolls:
                p0 = (p0p + r0) % 10
                s0 = s0p + (p0+1)
                n0 = np * nr0
                if s0 >= 21:
                    wins0 += n0
                else:
                    for r1, nr1 in rolls:
                        p1 = (p1p + r1) % 10
                        s1 = s1p + (p1+1)
                        n1 = n0 * nr1
                        if s1 >= 21:
                            wins1 += n1
                        else:
                            games[p0, p1, s0, s1] += n1

    return wins0, wins1


def practice(start):
    pos = list(start)
    score = [ 0, 0 ]
    die = cyclegen(range, 1, 100+1)

    for turn in count(1):                               # pragma: no branch
        i = (turn - 1) & 1
        p = pos[i] = (pos[i] + next(die) + (next(die) + next(die))) % 10
        s = score[i] = score[i] + p + 1
        if s >= 1000:
            return 3 * turn * score[1-i]


def cyclegen(gen, *args):
    while True:
        yield from gen(*args)


def read(file):
    return tuple(int(l.split(':')[1].strip()) - 1  # convert to 0-based index
                 for l in file)


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    assert practice(read(data('ex0.txt'))) == 739785

def test1_answer(data):
    assert practice(read(data('input.txt'))) == 597600


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex0(data):
    assert count_wins(read(data('ex0.txt'))) == \
        (444356092776315, 341960390180808)

def test2_answer(data):
    assert max(count_wins(read(data('input.txt')))) == 634769613696613


#------------------------------------------------------------------------------
def test_ex0(ascript):
    assert ascript('ex0.txt') == '''\
part[1]: 739785
part[2]: 444356092776315
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 597600
part[2]: 634769613696613
'''
