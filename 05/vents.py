#!/usr/bin/env python3
from collections import Counter


def main():
    from sys import argv
    with open(argv[1]) as file:
        lines = read(file)

    print('part[1]:', count_overlaps(mark_grid_aa(lines)))
    print('part[2]:', count_overlaps(mark_grid(lines)))


def count_overlaps(grid):
    return sum(int(n > 1) for n in grid.values())


def mark_grid_aa(lines):
    return mark_grid(filter_aa(lines))


def mark_grid(lines):
    grid = Counter()
    for (x,y),(x1,y1) in lines:
        Δx,Δy = sgn(x1 - x), sgn(y1 - y)
        while True:
            grid[x,y] += 1
            if x == x1 and y == y1: break
            x,y = x+Δx, y+Δy
    return grid


def filter_aa(lines):
    return [ l for l in lines if l[0][0] == l[1][0] or l[0][1] == l[1][1] ]


def sgn(x):
    if x > 0: return 1
    if x < 0: return -1
    return 0


def read(file):
    return [ tuple(tuple((int(c) for c in s.split(',')))
                   for s in l.split(' -> '))
             for l in file ]


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    lines = read(data('ex0.txt'))
    assert len(lines) == 10
    lines = filter_aa(lines)
    assert len(lines) == 6
    assert count_overlaps(mark_grid(lines)) == 5

def test1_answer(data):
    assert count_overlaps(mark_grid_aa(read(data('input.txt')))) == 6687


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex0(data):
    assert count_overlaps(mark_grid(read(data('ex0.txt')))) == 12

def test2_answer(data):
    assert count_overlaps(mark_grid(read(data('input.txt')))) == 19851


#------------------------------------------------------------------------------
def test_ex0(ascript):
    assert ascript('ex0.txt') == '''\
part[1]: 5
part[2]: 12
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 6687
part[2]: 19851
'''
