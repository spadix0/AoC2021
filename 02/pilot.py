#!/usr/bin/env python3
from itertools import accumulate
from operator import mul


def main():
    from sys import argv
    with open(argv[1]) as file:
        cmds = read(file)

    print('part[1]:', mul(*track_position(cmds)))
    print('part[2]:', mul(*track_aimed(cmds)))


def track_position(cmds):
    return sum(Δp for Δp,_ in cmds), sum(Δd for _,Δd in cmds)


def track_aimed(cmds):
    aim = accumulate(Δa for _,Δa in cmds)  # pragma: no branch
    return (sum(Δp for Δp,_ in cmds),
            sum(Δp*a for (Δp,_),a in zip(cmds, aim)))


def read(file):
    return [ parse_cmd(l) for l in file ]


def parse_cmd(cmd):
    match cmd.split():
        case ('forward', n): return (int(n), 0)
        case ('down', n): return (0, int(n))
        case ('up', n): return (0, -int(n))
        case _: raise ValueError(cmd)  # pragma: no cover


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    cmds = read(data('ex0.txt'))
    assert cmds == [ (5,0), (0,5), (8,0), (0,-3), (0,8), (2,0) ]
    assert track_position(cmds) == (15, 10)

def test1_answer(data):
    cmds = read(data('input.txt'))
    assert len(cmds) == 1000
    assert track_position(cmds) == (2007, 747)


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex0(data):
    assert track_aimed(read(data('ex0.txt'))) == (15, 60)

def test2_answer(data):
    assert track_aimed(read(data('input.txt'))) == (2007, 668080)


#------------------------------------------------------------------------------
def test_ex0(ascript):
    assert ascript('ex0.txt') == '''\
part[1]: 150
part[2]: 900
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 1499229
part[2]: 1340836560
'''
