#!/usr/bin/env python3
from math import pi, inf, ceil, floor, gcd, hypot, atan2, sqrt, sin, cos
from array import array
from itertools import *
from functools import partial, reduce
from operator import add, mul, or_
from collections import namedtuple, defaultdict, deque, Counter
from heapq import heapify, heappush, heappop
from io import StringIO
from hashlib import md5
import re, json

zet = frozenset
chainit = chain.from_iterable


def main():
    from sys import argv, stdin
    with open(argv[1]) as file:
        data = read(file)
    print(data)

    print('part[1]:')
    print('part[2]:')


def read(file):
    data = [ ]
    for line in file:
        line = line.strip()

    return data


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    assert read(data('ex0.txt'))

def test1_answer(data):
    assert read(data('input.txt'))


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex0(data):
    assert read(data('ex0.txt'))

def test2_answer(data):
    assert read(data('input.txt'))


#------------------------------------------------------------------------------
def test_ex0(ascript):
    assert ascript('ex0.txt') == '''\
part[1]:
part[2]:
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]:
part[2]:
'''
