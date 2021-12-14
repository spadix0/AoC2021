#!/usr/bin/env python3
from statistics import mean, median_low


def main():
    from sys import argv
    with open(argv[1]) as file:
        src = read(file)

    print('part[1]:', cost1(src, best_pos1(src)))
    print('part[2]:', cost2(src, best_pos2(src)))


def cost1(src, dst):
    return sum(abs(dst - p) for p in src)


def cost2(src, dst):
    return sum((Δp := abs(dst - p))*(Δp + 1) for p in src)//2


def best_pos1(src):
    return median_low(src)


def best_pos2(src):
    p0 = int(mean(src))
    return p0 if cost2(src, p0) < cost2(src, p0+1) else p0+1


def read(file):
    return [ int(s) for s in file.read().strip().split(',') ]


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    src = read(data('ex0.txt'))
    assert len(src) == 10
    assert best_pos1(src) == 2
    assert cost1(src, 2) == 37
    assert cost1(src, 1) == 41
    assert cost1(src, 3) == 39
    assert cost1(src, 10) == 71

def test1_input(data):
    src = read(data('input.txt'))
    p0,p1 = min(src), max(src)
    cb = cost1(src, best_pos1(src))
    for p in range(p0, p1+1):
        assert cost1(src, p) >= cb

def test1_answer(data):
    src = read(data('input.txt'))
    assert cost1(src, best_pos1(src)) == 352331


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex0(data):
    src = read(data('ex0.txt'))
    assert best_pos2(src) == 5
    assert cost2(src, 5) == 168
    assert cost2(src, 2) == 206

def test2_input(data):
    src = read(data('input.txt'))
    assert cost2(src, best_pos2(src)) == 99266250


#------------------------------------------------------------------------------
def test_ex0(ascript):
    assert ascript('ex0.txt') == '''\
part[1]: 37
part[2]: 168
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 352331
part[2]: 99266250
'''
