#!/usr/bin/env python3
from array import array
from itertools import count, chain
from functools import partial
from collections import defaultdict

chainit = chain.from_iterable

N4 = ((0,-1), (-1,0), (1,0), (0,1))


def main():
    from sys import argv
    with open(argv[1]) as file:
        map, w = read(file)

    print('part[1]:', sssp(map, w)[-1])
    print('part[2]:', sssp(*tile_map(map, w))[-1])


def tile_map(src, w, n=5, m=5):
    h = len(src) // w
    return bytes(
        (src[y*w + x] + i+j - 1)%9 + 1
        for j in range(m) for y in range(h)
        for i in range(n) for x in range(w)
    ), n*w


def sssp(cost, w):
    h = len(cost) // w
    dist = array('L', ((1<<32)-1 for _ in range(len(cost))))
    queues = defaultdict(partial(array, 'L'))

    dist[0] = 0
    queues[0].append(0)
    idp = count()

    while queues:
        for i0 in queues.pop(next(idp), ()):
            d0, x0,y0 = dist[i0], i0%w, i0//w
            for Δx,Δy in N4:
                x,y = x0+Δx, y0+Δy
                i = w*y + x
                if 0 <= x < w and 0 <= y < h and dist[i] > (d := d0 + cost[i]):
                    dist[i] = d
                    queues[d].append(i)

    return dist


def read(file):
    row0 = bytes(parse_row(file.readline()))
    w = len(row0)
    return bytes(chain(row0, chainit(parse_row(l) for l in file))), w


def parse_row(line):
    return (int(c) for c in line.strip())


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    map,w = read(data('ex0.txt'))
    assert w == 10
    assert len(map) == 100
    assert sssp(map, w)[-1] == 40

def test1_answer(data):
    assert sssp(*read(data('input.txt')))[-1] == 393


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex0(data):
    map,w = tile_map(*read(data('ex0.txt')))
    assert w == 50
    assert len(map) == 2500
    assert sssp(map, w)[-1] == 315

def test2_answer(data):
    assert sssp(*tile_map(*read(data('input.txt'))))[-1] == 2823


#------------------------------------------------------------------------------
def test_ex0(ascript):
    assert ascript('ex0.txt') == '''\
part[1]: 40
part[2]: 315
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 393
part[2]: 2823
'''
