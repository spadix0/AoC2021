#!/usr/bin/env python3
from array import array
from itertools import chain
from functools import reduce
from operator import mul

chainit = chain.from_iterable


def main():
    from sys import argv
    with open(argv[1]) as file:
        hmap,w = read(file)

    mins = find_mins(hmap, w)
    print('part[1]:', risk_level(hmap, mins))
    print('part[2]:', avoidance(fill_basins(hmap, w, mins)))


def risk_level(hmap, mins):
    return sum(hmap[i]+1 for i in mins)


def avoidance(basin):
    return reduce(mul, sorted(basin)[-3:])


def fill_basins(hmap, w, mins):
    vis = array('B', (0 if h < 9 else 1 for h in hmap))
    return [ fill_basin(vis, w, i) for i in mins ]


def fill_basin(vis, w, seed):
    front, size = [ seed ], 0
    vis[seed] = 1
    while front:
        size += 1
        i = front.pop()
        if not vis[j := i+w]: front.append(j); vis[j] = 1
        if not vis[j := i+1]: front.append(j); vis[j] = 1
        if not vis[j := i-1]: front.append(j); vis[j] = 1
        if not vis[j := i-w]: front.append(j); vis[j] = 1
    return size


def find_mins(hmap, w):
    return [ i for i in range(w+1, len(hmap)-w-1)
             if (h := hmap[i]) < hmap[i-1] and
                h < hmap[i+1] and
                h < hmap[i-w] and
                h < hmap[i+w] ]


def read(file):
    def grokrow(line):
        return chain((9,), (int(c) for c in line.strip()), (9,))

    # pad to simplify boundary conditions
    row0 = array('B', grokrow(file.readline()))
    w = len(row0)
    return array('B', chain(
        (9,)*w, row0, chainit(grokrow(l) for l in file), (9,)*w)), w


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    hmap,w = read(data('ex0.txt'))
    assert w == 12
    assert len(hmap) == w*7
    mins = find_mins(hmap, w)
    assert mins == [ 14, 22, 39, 67 ]
    assert risk_level(hmap, mins) == 15

def test1_answer(data):
    hmap,w = read(data('input.txt'))
    assert risk_level(hmap, find_mins(hmap, w)) == 633


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex0(data):
    hmap = read(data('ex0.txt'))
    assert avoidance(fill_basins(*hmap, find_mins(*hmap))) == 1134

def test2_answer(data):
    hmap = read(data('input.txt'))
    assert avoidance(fill_basins(*hmap, find_mins(*hmap))) == 1050192


#------------------------------------------------------------------------------
def test_ex0(ascript):
    assert ascript('ex0.txt') == '''\
part[1]: 15
part[2]: 1134
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 633
part[2]: 1050192
'''
