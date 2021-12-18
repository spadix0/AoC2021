#!/usr/bin/env python3
from math import inf, ceil, floor, sqrt


def main():
    from sys import argv
    with open(argv[1]) as file:
        tgt = read(file)

    print('part[1]:', maxheight(calc_Δy0max(tgt)))
    print('part[2]:', ilen(all_trajectories(tgt)))


def maxheight(Δy0):
    # it takes Δy0 steps for Δy to reach 0
    return intsum(Δy0) if Δy0 > 0 else 0


def all_trajectories(tgt):
    (txmin, txmax), _ = tgt
    Δy0max = calc_Δy0max(tgt)
    return (
        (Δx0, Δy0)
        for Δx0 in range(calc_Δx0min(tgt), txmax+1)
        if (nrange := steps_forΔx0(tgt, Δx0))
        for Δy0 in Δy0_forsteps(tgt, nrange, Δy0max)
        if ranges_intersect(nrange, steps_forΔy0(tgt, Δy0))
    )


# tight bound on step range for given initial horizontal velocity
def steps_forΔx0(tgt, Δx0):
    (txmin, txmax), _ = tgt
    Δx1min = ceil(steps_tosum(Δx0, txmax))
    Δx1max = floor(steps_tosum(Δx0, txmin))
    return (Δx0 - Δx1max + 1,
            Δx0 - Δx1min + 1 if Δx1min > 1 else inf)


# tight bound on step range for given initial vertical velocity
def steps_forΔy0(tgt, Δy0):
    _, (tymin, tymax) = tgt
    return (Δy0 + ceil(steps_tosum(Δy0, tymax)),
            Δy0 + floor(steps_tosum(Δy0, tymin)))


# tight bound on initial vertical velocities for given step range
def Δy0_forsteps(tgt, nrange, Δy0max):
    _, (tymin, tymax) = tgt
    nmin, nmax = nrange
    return range(
        ceil(tymin/nmin + (nmin - 1)/2),
        floor(min(tymax/nmax + (nmax - 1)/2, Δy0max)) + 1)


# max initial vertical velocity that can hit target range
def calc_Δy0max(tgt):
    _, (tymin, tymax) = tgt

    # NB y always returns to 0 (for Δy0 > 0)
    # ⇒ y=0 must not be in target area (or initial speed is unbounded)
    # ⇒ max final speed bounded by max target distance from 0
    assert not (tymin <= 0 <= tymax)

    if tymax > 0:
        Δy0max, Δy1max = tymax, -tymax
    else:
        Δy0max, Δy1max = -tymin - 1, tymin

    # assuming max y is compatible w/some x...
    assert Δy0max - Δy1max + 1 >= calc_Δx0min(tgt)
    return Δy0max


# min initial horizontal velocity to reach target range
def calc_Δx0min(tgt):
    txmin = tgt[0][0]
    return ceil((sqrt(1 + 8*txmin)-1) / 2)


def read(file):
    return parse_target(file.read())


def parse_target(line):
    return tuple(
        tuple(sorted(int(v) for v in axis.split('=')[1].split('..')))
        for axis in line.strip().split(': ')[1].split(', ')
    )


def ranges_intersect(r0, r1):
    return r0[0] <= r0[1] and r0[0] <= r1[1] and \
        r1[0] <= r1[1] and r1[0] <= r0[1]


# consume iterator to count elements
def ilen(it):
    return sum(1 for _ in it)


# closed form solution for n in: sum = Σi ∀i∈[i0,i0-n]
def steps_tosum(i0, sum1):
    return (sqrt(max(0, 4*i0*(i0+1) - 8*sum1 + 1)) + 1) / 2


# closed form for Σi ∀i∈[1,n]
def intsum(n):
    return n*(n + 1)//2


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    tgt = read(data('ex0.txt'))
    assert tgt == ((20, 30), (-10, -5))
    assert calc_Δy0max(tgt) == 9
    assert maxheight(9) == 45

def test1_above():
    tgt = ((32, 64), (8, 16))
    assert calc_Δy0max(tgt) == 16
    assert maxheight(16) == 136

def test1_answer(data):
    tgt = read(data('input.txt'))
    assert tgt == ((201, 230), (-99, -65))
    assert maxheight(calc_Δy0max(tgt)) == 4851


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex0(data):
    assert ilen(all_trajectories(read(data('ex0.txt')))) == 112

def test2_answer(data):
    assert ilen(all_trajectories(read(data('input.txt')))) == 1739


#------------------------------------------------------------------------------
def test_ex0(ascript):
    assert ascript('ex0.txt') == '''\
part[1]: 45
part[2]: 112
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 4851
part[2]: 1739
'''
