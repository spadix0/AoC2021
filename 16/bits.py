#!/usr/bin/env python3
from math import inf
from itertools import count, chain
from functools import reduce
from operator import mul, gt, lt, eq
from enum import IntEnum
from collections import namedtuple

chainit = chain.from_iterable


class Type(IntEnum):
    ADD = 0
    MUL = 1
    MIN = 2
    MAX = 3
    LIT = 4
    GT = 5
    LT = 6
    EQ = 7


class Packet(namedtuple('Packet', 'ver type val')):
    __slots__ = ()

    @staticmethod
    def read(file):
        return parse_packet(read(file))[1]

    def sum_versions(self):
        acc = self.ver
        if self.type != Type.LIT:
            acc += sum(p.sum_versions() for p in self.val)
        return acc

    def evaluate(self):
        sub = (p.evaluate() for p in self.val)
        match self.type:
            case Type.ADD: return sum(sub)
            case Type.MUL: return reduce(mul, sub)
            case Type.MIN: return min(sub)
            case Type.MAX: return max(sub)
            case Type.LIT: return self.val[0]
            case Type.GT: return int(gt(*sub))
            case Type.LT: return int(lt(*sub))
            case Type.EQ: return int(eq(*sub))


def main():
    from sys import argv
    with open(argv[1]) as file:
        pkt = Packet.read(file)

    print('part[1]:', pkt.sum_versions())
    print('part[2]:', pkt.evaluate())


def parse_packet(bits):
    type = Type(parse_bits(bits[3:6]))
    if type == Type.LIT:
        n, val = parse_literal(bits[6:])
        n += 6
    elif bits[6] == 0:
        n, val = parse_seq(bits[22:], nbits=parse_bits(bits[7:22]))
        n += 22
    else:
        n, val = parse_seq(bits[18:], nsub=parse_bits(bits[7:18]))
        n += 18

    assert n <= len(bits)
    return n, Packet(parse_bits(bits[:3]), type, val)


def parse_seq(bits, nbits=inf, nsub=inf):
    i, seq = 0, [ ]
    while i < nbits and len(seq) < nsub:
        n, sub = parse_packet(bits[i:])
        i += n
        seq.append(sub)

    return i, tuple(seq)


def parse_literal(lit):
    val = 0
    for i in count(0, 5):  # pragma: no branch
        val = val<<4 | parse_bits(lit[i+1:i+5])
        if not lit[i]:
            return i+5, (val,)


def parse_bits(bits):
    return int(''.join(str(b) for b in bits), 2)


def read(file):
    hexbits = tuple(
        bytes(int(b) for b in f'{i:04b}')
        for i in range(16))
    return bytes(chainit(hexbits[int(c, 16)]
                         for c in file.read().strip()))


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    bits = read(data('ex0.txt'))
    assert ''.join(str(b) for b in bits) == '110100101111111000101000'
    n, pkt = parse_packet(bits)
    assert n == 21
    assert pkt == Packet(6, Type.LIT, (2021,))
    assert pkt.sum_versions() == 6

def test1_ex1(data):
    bits = read(data('ex1.txt'))
    assert ''.join(str(b) for b in bits) == \
        '00111000000000000110111101000101001010010001001000000000'
    n, pkt = parse_packet(bits)
    assert n == 49
    assert pkt == Packet(1, Type(6), (
        Packet(6, Type.LIT, (10,)),
        Packet(2, Type.LIT, (20,)),
    ))
    assert pkt.sum_versions() == 9

def test1_ex2(data):
    bits = read(data('ex2.txt'))
    assert ''.join(str(b) for b in bits) == \
        '11101110000000001101010000001100100000100011000001100000'
    n, pkt = parse_packet(bits)
    assert n == 51
    assert pkt == Packet(7, Type(3), (
        Packet(2, Type(4), (1,)),
        Packet(4, Type(4), (2,)),
        Packet(1, Type(4), (3,)),
    ))
    assert pkt.sum_versions() == 14

def test1_exs(data):
    assert Packet.read(data('ex3.txt')).sum_versions() == 16
    assert Packet.read(data('ex4.txt')).sum_versions() == 12
    assert Packet.read(data('ex5.txt')).sum_versions() == 23
    assert Packet.read(data('ex6.txt')).sum_versions() == 31

def test1_answer(data):
    assert Packet.read(data('input.txt')).sum_versions() == 986


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex0(data):
    assert Packet.read(data('ex0.txt')).evaluate() == 2021

def test2_ops(data):
    assert Packet.read(data('ex7.txt')).evaluate() == 3
    assert Packet.read(data('ex8.txt')).evaluate() == 54
    assert Packet.read(data('ex9.txt')).evaluate() == 7
    assert Packet.read(data('exA.txt')).evaluate() == 9

def test2_rel(data):
    assert Packet.read(data('exB.txt')).evaluate() == 1
    assert Packet.read(data('exC.txt')).evaluate() == 0
    assert Packet.read(data('exD.txt')).evaluate() == 0

def test2_exp(data):
    assert Packet.read(data('exE.txt')).evaluate() == 1

def test2_answer(data):
    assert Packet.read(data('input.txt')).evaluate() == 18234816469452


#------------------------------------------------------------------------------
def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 986
part[2]: 18234816469452
'''
