#!/usr/bin/env python3
from itertools import count, repeat, chain

chainit = chain.from_iterable


def main():
    from sys import argv
    with open(argv[1]) as file:
        filt, img = read(file)

    img = enhance(filt, img, 2)
    print('part[1]:', img.count())

    img = enhance(filt, img, 50-2)
    print('part[2]:', img.count())


def enhance(filter, img, n):
    for _ in range(n):
        img = img.enhanced(filter)
    return img


class Image:
    def __init__(self, pix, bg=0):
        # NB all 0 background can filter to (all) 1!
        # ⇒ need to track bg state
        self.pix, self.bg = pix, bg

    def count(self):
        return sum(chainit(self.pix)) # + inf if self.bg

    def enhanced(self, filter):
        src, bg = self.pix, self.bg
        w, h = len(src[0]), len(src)

        # use sliding window that only updates new column
        # (this loop is ~10x faster than a more "obvious" comprehension
        #  that does 9 bounds checked src lookups for every dst pixel)
        COL0, COL12 = 0b001_001_001, 0b110_110_110
        i0 = sum(bg<<i for i in range(9))

        dst = [ bytearray(w+2) for _ in range(h+2) ]
        for y,dr in enumerate(dst, -1):
            i = i0
            for x,y0,y1,y2 in zip(count(),
                                  src[y-1] if 0 <= y-1 else repeat(bg),
                                  src[y] if 0 <= y < h else repeat(bg),
                                  src[y+1] if y+1 < h else repeat(bg)):
                i = (i<<1 & COL12) | y0<<6 | y1<<3 | y2
                dr[x] = filter[i]

            i = (i<<1 & COL12) | i0&COL0
            dr[w] = filter[i]

            i = (i<<1 & COL12) | i0&COL0
            dr[w+1] = filter[i]

        return Image(dst, filter[-1 if bg else 0])


def read(file):
    filter = parse_line(file.readline())
    file.readline()
    return filter, Image([ parse_line(l) for l in file ])


def parse_line(line):
    return bytes(int(c == '#') for c in line.strip())


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    assert enhance(*read(data('ex0.txt')), 2).count() == 35

def test1_answer(data):
    assert enhance(*read(data('input.txt')), 2).count() == 5379


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex0(data):
    assert enhance(*read(data('ex0.txt')), 50).count() == 3351

def test2_answer(data):
    assert enhance(*read(data('input.txt')), 50).count() == 17917


#------------------------------------------------------------------------------
def test_ex0(ascript):
    assert ascript('ex0.txt') == '''\
part[1]: 35
part[2]: 3351
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 5379
part[2]: 17917
'''
