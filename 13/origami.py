#!/usr/bin/env python3
from math import inf

zet = frozenset


def main():
    from sys import argv
    with open(argv[1]) as file:
        dots, folds = read(file)

    print('part[1]:', len(fold(dots, *folds[0])))

    dots = fold_all(dots, folds)
    print('part[2]:', len(dots))
    dump(dots)


def fold_all(dots, folds):
    for f in folds:
        dots = fold(dots, *f)
    return dots


def fold(dots, x0,y0):
    def mirror(x,y):
        return (x if x < x0 else 2*x0 - x,
                y if y < y0 else 2*y0 - y)
    return zet(mirror(x,y) for x,y in dots)


def dump(dots):
    (x0,y0),(x1,y1) = aabb(dots)
    for y in range(y0, y1+1):
        print('    ', end='')
        for x in range(x0, x1+1):
            print('█' if (x,y) in dots else ' ', end='')
        print()


def aabb(dots):
    (x0,y0),(x1,y1) = (inf, inf), (-inf, -inf)
    for x,y in dots:
        if x0 > x: x0 = x
        if x1 < x: x1 = x
        if y0 > y: y0 = y
        if y1 < y: y1 = y
    return (x0,y0),(x1,y1)


def read(file):
    return zet(read_dots(file)), [ parse_fold(l) for l in file ]


def read_dots(file):
    while l := file.readline().strip():
        yield tuple(int(s) for s in l.split(','))


def parse_fold(line):
    ax,u = line.split()[-1].split('=')
    return (int(u), inf) if ax == 'x' else (inf, int(u))


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    dots, folds = read(data('ex0.txt'))
    assert len(fold(dots, *folds[0])) == 17

def test1_answer(data):
    dots, folds = read(data('input.txt'))
    assert len(fold(dots, *folds[0])) == 716


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex0(data):
    assert len(fold_all(*read(data('ex0.txt')))) == 16

def test2_answer(data):
    assert len(fold_all(*read(data('input.txt')))) == 97


#------------------------------------------------------------------------------
def test_ex0(ascript):
    assert ascript('ex0.txt') == '''\
part[1]: 17
part[2]: 16
    █████
    █   █
    █   █
    █   █
    █████
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 716
part[2]: 97
    ███  ███   ██  █  █ ████ ███  █    ███ 
    █  █ █  █ █  █ █ █  █    █  █ █    █  █
    █  █ █  █ █    ██   ███  ███  █    █  █
    ███  ███  █    █ █  █    █  █ █    ███ 
    █ █  █    █  █ █ █  █    █  █ █    █ █ 
    █  █ █     ██  █  █ █    ███  ████ █  █
'''
