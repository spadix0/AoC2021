#!/usr/bin/env python3
zet = frozenset


def main():
    from sys import argv
    with open(argv[1]) as file:
        notes = read(file)

    print('part[1]:', unique_outputs(notes))
    print('part[2]:', sum_outputs(notes))


def unique_outputs(notes):
    return sum(int(len(p) in (2, 3, 4, 7))
               for _,out in notes
               for p in out)


def sum_outputs(notes):
    return sum(encode(out, decode(inp)) for inp,out in notes)


def decode(inp):
    inp = sorted(inp, key=len)
    digs = [ None for _ in range(10) ]
    digs[1], digs[7], digs[4], *unk, digs[8] = inp

    def finddig(n, pat):
        for i,p in enumerate(unk):
            if len(p) == n and p >= pat:
                del unk[i]
                return p
        assert None # pragma: no cover

    digs[3] = finddig(5, digs[7])		# 3 = 7+dg
    digs[5] = finddig(5, digs[4]-digs[1])	# 5 = 4-1+afg
    digs[2] = finddig(5, zet())			# 2 = only remaining x5
    digs[9] = finddig(6, digs[4]|digs[5])	# 9 = 5+4
    digs[6] = finddig(6, digs[8]-digs[4]|digs[5]) # 6 = 8-4+5
    assert len(unk) == 1
    digs[0] = unk[0]
    return { p:i for i,p in enumerate(digs) }


def encode(out, dec):
    return sum(dec[p] * 10**i for i,p in enumerate(reversed(out)))


def read(file):
    return [ tuple(tuple(zet(p) for p in s.split())
                   for s in l.strip().split('|'))
             for l in file ]


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    notes = read(data('ex0.txt'))
    assert len(notes) == 1
    assert len(notes[0]) == 2
    assert len(notes[0][0]) == 10
    assert len(notes[0][1]) == 4
    assert unique_outputs(notes) == 0

def test1_ex1(data):
    notes = read(data('ex1.txt'))
    assert len(notes) == 10
    assert unique_outputs(notes) == 26

def test1_answer(data):
    assert unique_outputs(read(data('input.txt'))) == 330


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex0(data):
    inp,out = read(data('ex0.txt'))[0]
    dec = decode(inp)
    assert dec == {
        zet('acedgfb'): 8,
        zet('cdfbe'): 5,
        zet('gcdfa'): 2,
        zet('fbcad'): 3,
        zet('dab'): 7,
        zet('cefabd'): 9,
        zet('cdfgeb'): 6,
        zet('eafb'): 4,
        zet('cagedb'): 0,
        zet('ab'): 1,
    }
    assert encode(out, dec) == 5353

def test2_ex1(data):
    assert sum_outputs(read(data('ex1.txt'))) == 61229

def test2_answer(data):
    assert sum_outputs(read(data('input.txt'))) == 1010472


#------------------------------------------------------------------------------
def test_ex0(ascript):
    assert ascript('ex0.txt') == '''\
part[1]: 0
part[2]: 5353
'''

def test_ex1(ascript):
    assert ascript('ex1.txt') == '''\
part[1]: 26
part[2]: 61229
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 330
part[2]: 1010472
'''
