#!/usr/bin/env python3
from itertools import count, chain


def main():
    from sys import argv
    with open(argv[1]) as file:
        herds = read(file)

    print(run_fixed(*herds))


def run_fixed(*prev):
    for i in count(1):  # pragma: no branch
        if (next := step(*prev)) == prev:
            return i
        prev = next


def step(he, hs, w):
    he = move_E(he, hs, w)
    hs = move_S(he, hs, w)
    return he, hs, w


def move_E(he, hs, w):
    mask = [ re | rs for re, rs in zip(he, hs) ]
    s = w - 1
    M = (1<<w) - 1
    return [
        c&(m>>1 | m<<s) | (c<<1 | c>>s) & ~m & M
        for c, m in zip(he, mask)
    ]


def move_S(he, hs, w):
    mask = [ re | rs for re, rs in zip(he, hs) ]
    return [
        sc&sm | dc&~dm
        for sc,dc, dm,sm in zip(hs, chain(hs[-1:], hs[:-1]),
                                mask, chain(mask[1:], mask[:1]))
    ]


def read(file):
    he, hs = [ ], [ ]
    for line in file:
        re, rs, w = parse_row(line.strip())
        he.append(re)
        hs.append(rs)

    return he, hs, w


def parse_row(row):
    # separate bit masks >32x faster than merged bytes w/generic move
    return (sum(1<<x for x,c in enumerate(row) if c == '>'),
            sum(1<<x for x,c in enumerate(row) if c == 'v'),
            len(row))


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# examples

def check_steps(steps):
    prev = None
    for pat in steps:
        exp = read(pat.split())
        if prev:
            act = step(*prev)
            assert act == exp
        prev = exp

def test_adj():
    check_steps([
        '...>>>>>...',
        '...>>>>.>..',
        '...>>>.>.>.',
    ])

def test_order():
    check_steps([
        '''\
            ..........
            .>v....v..
            .......>..
            ..........
        ''',  '''\
            ..........
            .>........
            ..v....v>.
            ..........
        '''
    ])

def test_wrap():
    check_steps([
        '''\
            ...>...
            .......
            ......>
            v.....>
            ......>
            .......
            ..vvv..
        ''', '''\
            ..vv>..
            .......
            >......
            v.....>
            >......
            .......
            ....v..
        ''', '''\
            ....v>.
            ..vv...
            .>.....
            ......>
            v>.....
            .......
            .......
        ''', '''\
            ......>
            ..v.v..
            ..>v...
            >......
            ..>....
            v......
            .......
        ''', '''\
            >......
            ..v....
            ..>.v..
            .>.v...
            ...>...
            .......
            v......
        ''',
    ])


def test1_ex0(data):
    assert run_fixed(*read(data('ex0.txt'))) == 58

def test1_answer(data):
    assert run_fixed(*read(data('input.txt'))) == 489


#------------------------------------------------------------------------------
def test_ex0(ascript):
    assert ascript('ex0.txt') == '''\
58
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
489
'''
