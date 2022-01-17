#!/usr/bin/env python3
from typing import NamedTuple
import re


def main():
    from sys import argv
    with open(argv[1]) as file:
        digs = read(file)

    pairs = match_pairs(digs)

    print('part[1]:', extremum(digs, pairs, max))
    print('part[2]:', extremum(digs, pairs, min))


def extremum(digs, pairs, sel):
    val = [ 0 for _ in digs ]

    for i, j in pairs:
        Δ = digs[j].A + digs[i].B
        lmin, lmax = max(1, 1-Δ), min(9, 9-Δ)
        assert 1 <= lmin <= lmax <= 9
        assert 1 <= lmin+Δ <= lmax+Δ <= 9
        l = val[i] = sel(lmin, lmax)
        val[j] = l + Δ

    return int(''.join(str(v) for v in val))


def match_pairs(digs):
    pairs = [ None for _ in digs ]
    stack = [ ]

    for i, d in enumerate(digs):
        assert 0 <= d.B < d.N+1 - 9
        if d.D == 1:
            stack.append(i)
            assert 9 < d.A < d.M
        else:
            j = stack.pop()
            assert pairs[i] is None and pairs[j] is None
            assert digs[j].N + 1 == d.M == d.D
            pairs[i], pairs[j] = j, i

    return [ (i, j) for i, j in enumerate(pairs) if i < j ]


class DigitParams(NamedTuple):
    A: int
    B: int
    D: int
    M: int
    N: int


def read(file):
    return [
        parse_template(''.join(file.readline() for _ in range(18)))
        for _ in range(14)
    ]


def parse_template(s):
    m = digit_re.match(s)
    assert m
    assert m['X'] != m['C'] != m['U'] != m['X'] != m['V'] != m['C']
    return DigitParams(**{ k: int(m[k]) for k in DigitParams.__annotations__ })


digit_re = re.compile(r'''
    \s* inp \s+ (?P<X>[w-y])            # Xi = next digit

    \s* mul \s+ (?P<C>[w-y]) \s+ 0      # Ci = 0
    \s* add \s+ (?P=C) \s+ z            #  = Zp
    \s* mod \s+ (?P=C) \s+ (?P<M>\d+)   #  = Zp % M

    \s* div \s+ z \s+ (?P<D>\d+)        # z = Zp / Di

    \s* add \s+ (?P=C) \s+ (?P<A>-?\d+) # Ci = Zp%M + Ai
    \s* eql \s+ (?P=C) \s+ (?P=X)       #  = Xi == Zp%M + Ai
    \s* eql \s+ (?P=C) \s+ 0            #  = Xi != Zp%M + Ai

    \s* mul \s+ (?P<U>[w-y]) \s+ 0      # U = 0
    \s* add \s+ (?P=U) \s+ (?P<N>\d+)   #  = N
    \s* mul \s+ (?P=U) \s+ (?P=C)       #  = N * Ci
    \s* add \s+ (?P=U) \s+ 1            #  = 1 + N*Ci
    \s* mul \s+ z \s+ (?P=U)            # z = Zp/Di*(1 + N*Ci)

    \s* mul \s+ (?P<V>[w-y]) \s+ 0      # V = 0
    \s* add \s+ (?P=V) \s+ (?P=X)       #  = Xi
    \s* add \s+ (?P=V) \s+ (?P<B>-?\d+) #  = Xi + Bi
    \s* mul \s+ (?P=V) \s+ (?P=C)       #  = (Xi + Bi)*Ci
    \s* add \s+ z \s+ (?P=V)            # Zn = Zp/Di*(1 + N*Ci) + (Xi + Bi)*Ci
    $
''', re.VERBOSE)


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_answer(data):
    digs = read(data('input.txt'))
    assert extremum(digs, match_pairs(digs), max) == 65984919997939


#------------------------------------------------------------------------------
# part 2 examples

def test2_answer(data):
    digs = read(data('input.txt'))
    assert extremum(digs, match_pairs(digs), min) == 11211619541713


#------------------------------------------------------------------------------
def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 65984919997939
part[2]: 11211619541713
'''
