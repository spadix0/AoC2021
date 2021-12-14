#!/usr/bin/env python3

def main():
    from sys import argv
    with open(argv[1]) as file:
        data = read(file)

    print('part[1]:', power(data))
    print('part[2]:', lifesupport(data))


def power(data):
    γ = γ_rate(data)
    ε = γ ^ (1 << len(data[0]))-1
    return γ * ε


def lifesupport(data):
    o2 = filter_diags(data, 0)
    co2 = filter_diags(data, 1)
    return o2 * co2


def filter_diags(data, crit):
    for b in reversed(range(len(data[0]))):
        if len(data) == 1:
            break
        gb = γ_bit(data, b)
        data = [ d for d in data if d[b] ^ crit == gb ]
    assert len(data) == 1
    return sum(d<<b for b,d in enumerate(data[0]))


def γ_rate(data):
    return sum(γ_bit(data, b) << b for b in range(len(data[0])))


def γ_bit(data, bit):
    return int(2*sum(d[bit] for d in data) >= len(data))


def read(file):
    return [ tuple(int(b) for b in reversed(l.strip())) for l in file ]


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    diags = read(data('ex0.txt'))
    assert γ_rate(diags) == 22
    assert power(diags) == 198

def test1_answer(data):
    assert power(read(data('input.txt'))) == 2595824


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex0(data):
    diags = read(data('ex0.txt'))
    assert filter_diags(diags, 0) == 23
    assert filter_diags(diags, 1) == 10
    assert lifesupport(diags) == 230

def test2_answer(data):
    assert lifesupport(read(data('input.txt'))) == 2135254


#------------------------------------------------------------------------------
def test_ex0(ascript):
    assert ascript('ex0.txt') == '''\
part[1]: 198
part[2]: 230
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 2595824
part[2]: 2135254
'''
