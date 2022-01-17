#!/usr/bin/env python3
from itertools import count
from functools import reduce
from operator import mul


def main():
    from sys import argv
    with open(argv[1]) as file:
        steps = read(file)

    print('part[1]:', popcount(initialize(steps)))
    print('part[2]:', popcount(reboot(steps)))


def initialize(steps):
    initvol = Cuboid(((-50,50), (-50,50), (-50,50)))
    return reboot(s for s in steps
                  if not initvol.isdisjoint(s[1]))


def reboot(steps):
    core = [ ]

    for on, new in steps:
        for i in reversed(range(len(core))):
            old = core[i]

            # manual inline and unroll new.isdisjoint(old) for ~4x faster
            (ax0, ax1), (ay0, ay1), (az0, az1) = new
            (bx0, bx1), (by0, by1), (bz0, bz1) = old
            if not (ax0 > bx1 or bx0 > ax1
                    or ay0 > by1 or by0 > ay1
                    or az0 > bz1 or bz0 > az1):
                # remove overlapping cuboid
                tmp = core.pop()
                if i < len(core):
                    core[i] = tmp  # replace w/already processed

                # and split into 0 to 6 non-overlapping smaller cuboids
                core.extend(old.difference(new))

        if on:
            core.append(new)

    return core


def popcount(cubes):
    return sum(c.volume() for c in cubes)


class Cuboid(tuple):
    __slots__ = ()

    def volume(self):
        return reduce(mul, (u1+1 - u0 for u0, u1 in self))

    def isdisjoint(self, c):
        return any(u0 > v1 or v0 > u1
                   for (u0, u1), (v0, v1) in zip(self, c))

    def difference(self, sub):
        res = list(self)

        for i, (u0, u1), (v0, v1) in zip(count(), self, sub):
            if u0 < v0:
                res[i] = (u0, v0-1)
                yield Cuboid(res)
                u0 = v0

            if v1 < u1:
                res[i] = (v1+1, u1)
                yield Cuboid(res)
                u1 = v1

            res[i] = (u0, u1)


def read(file):
    return [
        ( int(line.startswith('on')),
          parse_cuboid(line.split()[1]) )
        for line in file
    ]


def parse_cuboid(s):
    return Cuboid(
        tuple(int(u)
              for u in a.split('=')[1].split('..'))
        for a in s.split(',')
    )


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    assert popcount(initialize(read(data('ex0.txt')))) == 39

def test1_ex1(data):
    assert popcount(initialize(read(data('ex1.txt')))) == 590784

def test1_ex2(data):
    assert popcount(initialize(read(data('ex2.txt')))) == 474140

def test1_answer(data):
    assert popcount(initialize(read(data('input.txt')))) == 615700


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex2(data):
    assert popcount(reboot(read(data('ex2.txt')))) == 2758514936282235

def test2_answer(data):
    assert popcount(reboot(read(data('input.txt')))) == 1236463892941356


#------------------------------------------------------------------------------
def test_ex2(ascript):
    assert ascript('ex2.txt') == '''\
part[1]: 474140
part[2]: 2758514936282235
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 615700
part[2]: 1236463892941356
'''
