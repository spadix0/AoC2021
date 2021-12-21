#!/usr/bin/env python3
from math import copysign
from itertools import count, chain, product, permutations, combinations
from collections import Counter

chainit = chain.from_iterable


def main():
    from sys import argv
    with open(argv[1]) as file:
        scns = read(file)

    pos = locate_scanners(scns)
    print('part[1]:', count_unique(scns))
    print('part[2]:', max_dist1(pos))


def count_unique(it):
    return len(set(chainit(it)))


def max_dist1(pts):
    return max(dist1(s0, s1) for s0,s1 in combinations(pts, 2))


def locate_scanners(scns):
    # track matched scanner positions relative to scanner 0
    pos = [ None for _ in scns ]
    pos[0] = (0,0,0)

    found = [ 0 ]
    for i in found:                                     # pragma: no branch
        dst = scns[i]
        # project dst beacons onto each axis for quick pre-filter
        proj = [ project(dst, k) for k in range(3) ]

        for j, src, p in zip(count(), scns, pos):
            if not p and (m := match_scanner(dst, proj, src)):
                pos[j], scns[j] = m
                found.append(j)

        if len(found) >= len(scns):
            break

    assert all(pos)
    return pos


# search for transform from src scanner to dst that meets minimum overlap
def match_scanner(dst, proj, src):
    return first(
        m for axis in match_projections(proj, src)
        if (m := match_orients(dst, src, axis))
    )


# quick pre-filter by matching 1D projections (>12x faster)
def match_projections(proj, src):
    # check src x-axis against both orientations of each dst axis
    sx = project(src, 0)
    return (a for k,p in enumerate(proj, 1)
            if (a := check_proj(sx, p, 1) and k
                or check_proj(sx, p, -1) and -k))


# check 1D offset by Hough transform
def check_proj(p0, p1, s):
    return Counter(s*x1 - x0 for x0,x1 in product(p0, p1)) \
        .most_common(1)[0][1] >= 12


# full/slow overlap search over (4) orientations around axis
def match_orients(s0, s1, axis):
    return first(
        m for r in orientations
        if r[abs(axis)-1] == copysign(1, axis) and
            (m := check_overlap(s0, [ reorient(p1, r) for p1 in s1 ]))
    )


# check 3D offset by Hough transform
def check_overlap(s0, s1):
    match = Counter(
        tuple(x0 - x1 for x0,x1 in zip(p0, p1))
        for p0,p1 in product(s0, s1))

    best = match.most_common(2)
    assert best[1][1] < 12
    Δp, n = best[0]
    if n >= 12:
        # transform matched beacons relative to scanner 0
        return Δp, [ translate(p, Δp) for p in s1 ]


# filter proper rotations using "signature" (determinant of permutation matrix)
def signature(*r):
    return 1 if sum(i == j for i,j in enumerate(r)) != 1 else -1

orientations = tuple(
    (si*(i+1), sj*(j+1), sk*(k+1))
    for i,j,k in permutations(range(3))
    for si,sj,sk in product((1, -1), repeat=3)
    if signature(i, j, k)*si*sj*sk > 0
)
assert len(orientations) == 24
assert len(set(orientations)) == 24


def project(pts, axis):
    return [ p[axis] for p in pts ]


def reorient(p, r):
    return tuple(p[i-1] if i > 0 else -p[-i-1]
                 for i in r)


def translate(p, Δp):
    return tuple(u + Δu for u,Δu in zip(p, Δp))


# Manhattan distance (ℓ1 norm) between 2 points
def dist1(p0, p1):
    return sum(abs(x1 - x0) for x0,x1 in zip(p0, p1))


def first(it):
    return next(it, None)


def read(file):
    return [ read_scanner(file) for _ in file ]


def read_scanner(file):
    pts = [ ]
    while (l := file.readline().strip()):
        pts.append(tuple(int(c) for c in l.split(',')))

    return pts


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    scns = read(data('ex0.txt'))
    assert locate_scanners(scns) == [
        (0, 0, 0),
        (68, -1246, -43),
        (1105, -1205, 1229),
        (-92, -2380, -20),
        (-20, -1133, 1061),
    ]
    assert count_unique(scns) == 79

def test1_answer(data):
    locate_scanners(scns := read(data('input.txt')))
    assert count_unique(scns) == 320


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex0(data):
    assert max_dist1(locate_scanners(read(data('ex0.txt')))) == 3621

def test2_answer(data):
    assert max_dist1(locate_scanners(read(data('input.txt')))) == 9655


#------------------------------------------------------------------------------
def test_ex0(ascript):
    assert ascript('ex0.txt') == '''\
part[1]: 79
part[2]: 3621
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 320
part[2]: 9655
'''
