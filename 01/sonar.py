#!/usr/bin/env python3
from itertools import pairwise, accumulate


def main():
    from sys import argv
    with open(argv[1]) as file:
        depths = read(file)

    print('part[1]:', count_increases(depths))
    print('part[2]:', count_increases(sliding_window(depths, 3)))


def count_increases(depths):
    return sum(d0 < d1 for d0,d1 in pairwise(depths))


def sliding_window(data, n=3):
    return accumulate(
        (d1 - d0 for d0,d1 in zip(data, data[n:])),
        initial = sum(data[:n]))


def read(file):
    return [ int(l) for l in file ]


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    depths = read(data('ex0.txt'))
    assert len(depths) == 10
    assert count_increases(depths) == 7

def test1_answer(data):
    assert count_increases(read(data('input.txt'))) == 1752


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex0(data):
    depths = list(sliding_window(read(data('ex0.txt'))))
    assert depths == [ 607, 618, 618, 617, 647, 716, 769, 792 ]
    assert count_increases(depths) == 5

def test2_answer(data):
    assert count_increases(sliding_window(read(data('input.txt')))) == 1781


#------------------------------------------------------------------------------
def test_ex0(ascript):
    assert ascript('ex0.txt') == '''\
part[1]: 7
part[2]: 5
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 1752
part[2]: 1781
'''
