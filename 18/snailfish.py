#!/usr/bin/env python3
from itertools import chain, permutations
import re


def main():
    from sys import argv
    with open(argv[1]) as file:
        vals = read(file)

    print('part[1]:', sum(vals).magnitude())
    print('part[2]:', max_pairsum(vals))


def max_pairsum(vals):
    return max((a + b).magnitude() for a,b in permutations(vals, 2))


# representation of snail number binary tree
# (>10x faster than first/obvious approach w/nested tuples)

class SnailNum:
    __slots__ = 'vals tree'.split()

    def __init__(self, vals=bytes(), tree=bytes()):
        # leaf node digits ("regular numbers") are compacted in vals s.t.
        #    vals[i] is predecessor of vals[i+1] (and successor of vals[i-1])
        self.vals = vals

        # tree location of digit vals[i] is in tree[i]
        # (where left and right from location j is 2*j+1 and 2*j+2 respectively)
        self.tree = tree

    def __eq__(self, v):
        return self.vals == v.vals and self.tree == v.tree

    def __add__(self, v):
        return self.reduce(
            chain(self.vals, v.vals),
            # calculate new locations for push down to left/right subtree
            chain((i + (1 << (i+1).bit_length()-1) for i in self.tree),
                  (i + (1 << (i+1).bit_length()) for i in v.tree))
        )

    def __radd__(self, v):                              # just to enable sum()
        if v == 0:
            return self
        return NotImplemented

    @staticmethod
    def _calc_mag_weight():
        w = [ 0 for i in range(31) ]
        w[0] = 1
        for i in range(15):
            w[2*i + 1] = 3 * w[i]
            w[2*i + 2] = 2 * w[i]
        return w
    _mag_weight = _calc_mag_weight()

    def magnitude(self):
        w = self._mag_weight
        return sum(v*w[t] for v,t in zip(self.vals, self.tree))

    def reduced(self):
        return self.reduce(self.vals, self.tree)

    @staticmethod
    def reduce(src_vals, src_tree):
        vals, tree = bytearray(2), bytearray()

        # 1st pass: explode by max height only
        for v,t in (src := zip(src_vals, src_tree)):
            if t < 31:
                vals[-1] += v
                r = 0
            else:
                assert t&1 == 1
                t //= 2
                v += vals[-1]
                vals[-1] = 0
                vals[-2] += v
                r = next(src)[0]

            vals.append(r)
            tree.append(t)

        # 2nd pass: split while maintaining max height invariant
        i = 0
        while i < len(tree):
            if (v := vals[i+1]) <= 9:
                i += 1
            elif (t := tree[i]) < 15:                   # insert split node
                vals[i+1] = v // 2                      # NB can be > 9
                tree[i] = 2*t + 1
                vals.insert(i+2, (v + 1) // 2)
                tree.insert(i+1, 2*t + 2)
            else:                                       # split and explode
                vals[i+2] += (v + 1) // 2
                vals[i+1] = 0
                vals[i] = v = (vals[i] + v//2)
                if i > 0 and v > 9:
                    i -= 1                              # go back and split
                else:
                    i += 1

        return SnailNum(vals[1:-1], tree)


def read(file):
    return [ parse(l.strip()) for l in file ]


def parse(s):
    vals, tree = bytearray(), bytearray()
    i = 0
    for t in tokenize(s):
        match t:
            case '[': i = 2*i + 1
            case ']': i = (i-1) // 2
            case ',': i += 1
            case _:
                tree.append(i)
                vals.append(int(t))
    assert i == 0
    return SnailNum(vals, tree)


_token_re = re.compile(r'\s*([],[]|\d+)')

def tokenize(line):
    i = 0
    while i < len(line):
        m = _token_re.match(line, i)
        i = m.end()
        yield m[1]
    assert i == len(line)


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_parse():
    for s, exp_vals, exp_tree in [
        ( '[1,2]', [1,2], [1,2] ),
        ( '[[1,2],3]', [1,2,3], [3,4,2] ),
        ( '[9,[8,7]]', [9,8,7], [1,5,6] ),
        ( '[[1,9],[8,5]]', [1,9,8,5], [3,4,5,6] ),
        ( '[[[[1,2],[3,4]],[[5,6],[7,8]]],9]',
          [1,2,3,4, 5,6,7,8,9], [15,16,17,18, 19,20,21,22,2] ),
        ( '[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]',
          [9,3,8,0,9,6, 3,7,4,9,3], [7,17,18,19,20,10, 23,24,25,26, 6] ),
        ( '[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]',
          [1,3,5,3,1,3,8,7, 4,9,6,9,8,2,7,3], range(15, 31) ),
        ( '[[[[[1,1],[2,2]],[3,3]],[4,4]],[5,5]]',
          [1,1,2,2, 3,3,4,4,5,5], [31,32,33,34, 17,18,9,10,5,6] ),
    ]:
        act = parse(s)
        assert act.vals == bytes(exp_vals)
        assert act.tree == bytes(exp_tree)

def test1_magnitude():
    for s, exp in [
        ('[9,1]', 29),
        ('[1,9]', 21),
        ('[[9,1],[1,9]]', 129),
        ('[[1,2],[[3,4],5]]', 143),
        ('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]', 1384),
        ('[[[[1,1],[2,2]],[3,3]],[4,4]]', 445),
        ('[[[[3,0],[5,3]],[4,4]],[5,5]]', 791),
        ('[[[[5,0],[7,4]],[5,5]],[6,6]]', 1137),
        ('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]', 3488)
    ]:
        assert parse(s).magnitude() == exp

def test1_explode():
    for s, exp in [
        ( '[[[[[9,8],1],2],3],4]', '[[[[0,9],2],3],4]' ),
        ( '[7,[6,[5,[4,[3,2]]]]]', '[7,[6,[5,[7,0]]]]' ),
        ( '[[6,[5,[4,[3,2]]]],1]', '[[6,[5,[7,0]]],3]' ),
        ( '[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]',
        #  '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]' ),       # skip intermediate
        #( '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]',
          '[[3,[2,[8,0]]],[9,[5,[7,0]]]]' ),
        ( '[[[[[1,1],[2,2]],[3,3]],[4,4]],[5,5]]',
          '[[[[3,0],[5,3]],[4,4]],[5,5]]' ),
    ]:
        assert parse(s).reduced() == parse(exp)

def test1_addreduce():
    assert parse('[[[[4,3],4],4],[7,[[8,4],9]]]') + parse('[1,1]') == \
        parse('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')

def test1_sum():
    vals = [ parse(f'[{i},{i}]') for i in range(1,9) ]
    for n, exp in enumerate([
        '[1,1]',
        '[[1,1],[2,2]]',
        '[[[1,1],[2,2]],[3,3]]',
        '[[[[1,1],[2,2]],[3,3]],[4,4]]',
        '[[[[3,0],[5,3]],[4,4]],[5,5]]',
        '[[[[5,0],[7,4]],[5,5]],[6,6]]',
        '[[[[7,0],[9,5]],[6,6]],[7,7]]',
        '[[[[9,5],[6,0]],[[6,7],7]],[8,8]]'
    ]):
        assert sum(vals[:n+1]) == parse(exp)

def test1_ex0(data):
    vals = read(data('ex0.txt'))
    for n, exp in enumerate([
        '[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]',
        '[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]',
        '[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]',
        '[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]',
        '[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]',
        '[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]',
        '[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]',
        '[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]',
        '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]',
    ]):
        assert sum(vals[:n+2]) == parse(exp)

def test1_ex1(data):
    assert sum(read(data('ex1.txt'))).magnitude() == 4140

def test1_answer(data):
    assert sum(read(data('input.txt'))).magnitude() == 3654


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex1(data):
    assert max_pairsum(read(data('ex1.txt'))) == 3993

def test2_answer(data):
    assert max_pairsum(read(data('input.txt'))) == 4578


#------------------------------------------------------------------------------
def test_ex1(ascript):
    assert ascript('ex1.txt') == '''\
part[1]: 4140
part[2]: 3993
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 3654
part[2]: 4578
'''
