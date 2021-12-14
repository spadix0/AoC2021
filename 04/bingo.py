#!/usr/bin/env python3
from itertools import chain
from collections import defaultdict, Counter


def main():
    from sys import argv
    with open(argv[1]) as file:
        draws, boards = read(file)

    scores = play(draws, boards)
    print('part[1]:', first(scores)[1])
    print('part[2]:', last(scores)[1])


def play(draws, boards):
    scores = { }
    marks = Counter()

    def board_score(winner, undrawn):
        return sum(u*is_onboard(boards[u], winner) for u in undrawn)

    for i,n in enumerate(draws):
        for win in round(boards, n, marks):
            if (winner := win[0]) not in scores:
                scores[winner] = n * board_score(winner, draws[i+1:])

    return scores


def round(boards, num, marks):
    return chain(
        (m for b,r,c in boards[num] if (m := mark(marks, (b,0,r)))),
        (m for b,r,c in boards[num] if (m := mark(marks, (b,1,c))))
    )


def mark(marks, key):
    n = marks[key] = marks[key] + 1
    assert n <= 5
    if n == 5: return key


def is_onboard(locs, board):
    return sum(int(l[0] == board) for l in locs)


def first(map): return next(iter(map.items()))
def last(map): return next(iter(reversed(map.items())))


def read(file):
    draws = [ int(s) for s in file.readline().strip().split(',') ]
    boards = defaultdict(set)

    for b,sep in enumerate(file):
        assert not sep.strip()
        for r in range(5):
            for c,s in enumerate(file.readline().split()):
                boards[int(s)].add((b, r, c))

    return draws, boards


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    draws, boards = read(data('ex0.txt'))
    assert len(draws) == 27
    assert len(boards) == 27
    assert first(play(draws, boards)) == (2, 4512)

def test1_answer(data):
    assert first(play(*read(data('input.txt')))) == (16, 33462)


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex0(data):
    assert last(play(*read(data('ex0.txt')))) == (1, 1924)

def test2_answer(data):
    assert last(play(*read(data('input.txt')))) == (91, 30070)


#------------------------------------------------------------------------------
def test_ex0(ascript):
    assert ascript('ex0.txt') == '''\
part[1]: 4512
part[2]: 1924
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 33462
part[2]: 30070
'''
