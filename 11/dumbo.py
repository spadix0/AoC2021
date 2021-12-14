#!/usr/bin/env python3
from array import array
from itertools import count, chain

chainit = chain.from_iterable

N8 = tuple((Δx, Δy)
           for Δy in range(-1,1+1)
           for Δx in range(-1,1+1)
           if Δx or Δy)


def main():
    from sys import argv
    with open(argv[1]) as file:
        grid, w = read(file)

    print('part[1]:', run(grid, w))
    print('part[2]:', find_allflash(grid, w))


def run(grid, w, steps=100):
    nflash = 0
    for _ in range(steps):
        grid, n = step(grid, w)
        nflash += n
    return nflash


def find_allflash(grid, w):
    for i in count(1):  # pragma: no branch
        grid, n = step(grid, w)
        if n == len(grid):
            return i


def step(grid, w):
    grid = array('B', (z+1 for z in grid))
    nflash = 0
    while flash := [ i for i,z in enumerate(grid) if z > 9 ]:
        nflash += len(flash)
        for i0 in flash:
            grid[i0] = 0
            x0,y0 = i0%w, i0//w
            for Δx,Δy in N8:
                x,y = x0+Δx, y0+Δy
                if 0 <= x < w and 0 <= y < w and grid[i := w*y + x]:
                    grid[i] += 1
    return grid, nflash


def read(file):
    row0 = array('B', parse_row(file.readline()))
    w = len(row0)
    return array('B', chain(row0, chainit(parse_row(l) for l in file))), w


def parse_row(line):
    return (int(c) for c in line.strip())


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    grid = read(data('ex0.txt'))
    assert run(*grid, 10) == 204
    assert run(*grid) == 1656

def test1_ex1(data):
    grid = read(data('ex1.txt'))
    assert run(*grid, 1) == 9
    assert run(*grid, 2) == 9

def test1_answer(data):
    assert run(*read(data('input.txt'))) == 1649


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex0(data):
    assert find_allflash(*read(data('ex0.txt'))) == 195

def test2_answer(data):
    assert find_allflash(*read(data('input.txt'))) == 256


#------------------------------------------------------------------------------
def test_ex0(ascript):
    assert ascript('ex0.txt') == '''\
part[1]: 1656
part[2]: 195
'''

def test_ex1(ascript):
    assert ascript('ex1.txt') == '''\
part[1]: 259
part[2]: 6
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 1649
part[2]: 256
'''
