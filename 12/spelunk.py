#!/usr/bin/env python3
from functools import cache
from collections import defaultdict


def main():
    from sys import argv
    with open(argv[1]) as file:
        adj = read(file)

    print('part[1]:', count_paths(adj))
    print('part[2]:', count_paths(adj, revisit1=True))


def count_paths(adj, revisit1=False):
    @cache
    def count_from(src, via=False, vis=frozenset()):
        assert src not in vis
        if src == 'end':
            return 1 if not via else 0

        n = 0
        if src.islower():
            if via is None and src != 'start':
                # also add paths that revisit src
                n = sum(count_from(a, src, vis)
                        for a in adj[src] if a not in vis)
            elif via == src:
                via = False
            vis = vis.union((src,))

        return n + sum(count_from(a, via, vis)
                       for a in adj[src] if a not in vis)

    return count_from('start', revisit1 and None)


def read(file):
    adj = defaultdict(set)
    for line in file:
        n0,n1 = line.strip().split('-')
        adj[n0].add(n1)
        adj[n1].add(n0)
    return adj


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    assert count_paths(read(data('ex0.txt'))) == 10

def test1_ex1(data):
    assert count_paths(read(data('ex1.txt'))) == 19

def test1_ex2(data):
    assert count_paths(read(data('ex2.txt'))) == 226

def test1_answer(data):
    assert count_paths(read(data('input.txt'))) == 4338


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex0(data):
    assert count_paths(read(data('ex0.txt')), 1) == 36

def test2_ex1(data):
    assert count_paths(read(data('ex1.txt')), 1) == 103

def test2_ex2(data):
    assert count_paths(read(data('ex2.txt')), 1) == 3509

def test2_answer(data):
    assert count_paths(read(data('input.txt')), 1) == 114189


#------------------------------------------------------------------------------
def test_ex0(ascript):
    assert ascript('ex0.txt') == '''\
part[1]: 10
part[2]: 36
'''

def test_ex1(ascript):
    assert ascript('ex1.txt') == '''\
part[1]: 19
part[2]: 103
'''

def test_ex2(ascript):
    assert ascript('ex2.txt') == '''\
part[1]: 226
part[2]: 3509
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 4338
part[2]: 114189
'''
