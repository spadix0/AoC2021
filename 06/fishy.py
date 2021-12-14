#!/usr/bin/env python3
RESET = 6
INIT = 8
N = INIT+1


def main():
    from sys import argv
    with open(argv[1]) as file:
        hist = read(file)

    print('part[1]:', sum(run(hist, range(80))))
    print('part[2]:', sum(run(hist, range(80, 256))))


def run(hist, r):
    for i in r:
        step(hist, i)
    return hist


def step(hist, i):
    hist[(RESET+1+i)%N] += hist[i%N]


def read(file):
    hist = [ 0 for _ in range(N) ]
    for s in file.read().split(','):
        hist[int(s)] += 1
    return hist


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    hist = read(data('ex0.txt'))
    assert sum(run(hist, range(18))) == 26
    assert sum(run(hist, range(18, 80))) == 5934

def test1_answer(data):
    assert sum(run(read(data('input.txt')), range(80))) == 349549


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex0(data):
    assert sum(run(read(data('ex0.txt')), range(256))) == 26984457539

def test2_answer(data):
    assert sum(run(read(data('input.txt')), range(256))) == 1589590444365


#------------------------------------------------------------------------------
def test_ex0(ascript):
    assert ascript('ex0.txt') == '''\
part[1]: 5934
part[2]: 26984457539
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 349549
part[2]: 1589590444365
'''
