#!/usr/bin/env python3
from math import inf
from itertools import count
from heapq import heappush, heappop


def main():
    from sys import argv
    with open(argv[1]) as file:
        init = read(file)

    print('part[1]:', search(init))
    print('part[2]:', search(unfold(*init)))


part2_extra = '''\
  #D#C#B#A#
  #D#B#A#C#
'''

# add extra room occupants for part 2
def unfold(hall, rooms):
    bonus = [ parse_line(l) for l in part2_extra.split() ]
    return hall, [
        r[:1] + bytes(b[i] for b in bonus) + r[1:]
        for i, r in enumerate(rooms)
    ]


# heuristic guided state space search (A*).
# A* avoids 33-45% of state expansions over Dijkstra's for these problems
def search(init):
    # cached distance (energy) of single move for each type
    dists = [ int(10**i) for i in range(-1, 4) ]

    bystate = { }       # actual distance (energy) to each reached state
    bycost = { }        # bin of states for each weighted cost value
    heap = [ ]          # maintain minimum available weighted cost

    # mutable copies of working state
    hall = bytearray()  # hallway occupancy map w/intersections flagged
    fill = bytearray()  # count of residents remaining to move into each room
    evicts = []         # list of squatters in each room to move out before fill

    def add_state(dist, cost):
        st = (bytes(hall), bytes(fill), *evicts)
        if bystate.get(st, inf) > dist:
            bystate[st] = dist

            #assert cost == dist + est_remaining(hall, fill, evicts, dists)
            if q := bycost.get(cost):
                q.append(st)
            else:
                bycost[cost] = [ st ]
                heappush(heap, cost)

    # move squatter from hall to their home
    def movein(a, x):
        f = fill[i := a - 1]
        fill[i] = f - 1
        hall[x] = 0
        return dists[a]*(f + abs(2*a - x))

    # maintain state invariant by moving all possible amphipods into their
    # destination room, which significantly reduces state expansions.
    # moves to home are always on a shortest path, so do not change total
    # heuristic cost (added distance already included in estimated residual).
    # hoary mess from manually unrolling loops for almost 2x faster
    def flush_home():
        d = 0
        moving = True
        while moving:
            moving = False
            if (a := hall[5]) and not evicts[a-1] \
                    and (a > 1 or not hall[3]) \
                    and (a < 4 or not hall[7]):
                d += movein(a, 5)
                moving = True
            if (a := hall[3]) and not evicts[a-1] \
                    and (a < 3 or not hall[5]) \
                    and (a < 4 or not hall[7]):
                d += movein(a, 3)
                moving = True
            if (a := hall[7]) and not evicts[a-1] \
                    and (a > 2 or not hall[5]) \
                    and (a > 1 or not hall[3]):
                d += movein(a, 7)
                moving = True

            for a, ev in enumerate(evicts, 1):
                while ev and (v := ev[0]) and not evicts[v-1] \
                        and not any(hall[2*min(v,a)+1 : 2*max(v,a) : 2]):
                    ev = evicts[i := a-1] = ev[1:]
                    y = fill[i] - len(ev)
                    f = fill[j := v-1]
                    fill[j] = f - 1
                    d += dists[v]*(f + y + 2*abs(a - v))
                    moving = moving or not ev

        if (a := hall[1]) and not evicts[a-1] and not any(hall[3:2*a:2]):
            d += movein(a, 1)
        if (a := hall[0]) and not evicts[a-1] and not hall[1] \
                and not any(hall[3:2*a:2]):
            d += movein(a, 0)
        if (a := hall[9]) and not evicts[a-1] and not any(hall[2*a+1:9:2]):
            d += movein(a, 9)
        if (a := hall[10]) and not evicts[a-1] and not hall[9] \
                and not any(hall[2*a+1:9:2]):
            d += movein(a, 10)

        return d

    # generate neighboring states by smiting visitors to hall
    def gen_evictions(hall0, fill0, evicts0):
        for a, f, r0 in zip(count(1), fill0, evicts0):
            if not r0:
                continue

            v, nr = r0[0], len(r0) - 1
            x0, y0 = 2*a, f - nr
            c = dists[v]

            Δx1 = -1
            for Δx, h in enumerate(hall0[x0-1::-1], 1):
                if h & 0x7f: break
                elif not h: Δx1 = Δx
            x1 = x0 - Δx1

            for x, h in enumerate(hall0[x1:], x1):
                if h & 0x7f:
                    break
                elif not h:
                    hall[:], fill[:], evicts[:] = hall0, fill0, evicts0
                    hall[x] = v
                    evicts[a-1] = r0[1:]

                    Δx = abs(x - x0)
                    Δd = c*(y0 + Δx)
                    # incremental cost not accounted by previous estimate
                    if v == a:
                        Δc = 2*Δd
                    else:
                        xv = 2*v
                        Δc = c*(Δx + abs(xv-x) - abs(xv-x0))

                    yield Δd, Δc

    hall[:], fill[:], evicts[:] = init[0], *grok_rooms(init[1])

    # flag hallway intersections
    for x, h in enumerate(hall):
        if 2 <= x <= 8 and x%2 == 0:
            assert not h
            hall[x] = 0x80

    # NB time to fully evaluate heuristic is significant for 70K states
    # (52% of total time!), so incremental updates are used after init
    add_state(flush_home(), est_remaining(hall, fill, evicts, dists))

    while heap:  # pragma: no branch
        c0 = heappop(heap)

        for s0 in bycost[c0]:
            d0 = bystate[s0]
            if not sum(s0[1]):
                return d0

            for Δd, Δc in gen_evictions(s0[0], s0[1], s0[2:]):
                add_state(d0 + Δd + flush_home(), c0 + Δc)

        del bycost[c0]


# (under)estimate minimum possible remaining distance to goal state
# by moving each amphipod directly to destination, ignoring others
# (admissible and consistent heuristic for A*)
def est_remaining(hall, fill, evicts, dists):
    c = sum(abs(x - 2*a)*dists[a]           # move from hall to home doorway
            for x, a in enumerate(hall)
            if not a & 0x80)

    for a, f, r in zip(count(1), fill, evicts):
        z = f - len(r)
        c += z*(z+1)//2 * dists[a]          # move residents into unoccupied
        c += sum(
            (y + 2*abs(v - a))*dists[v]     # evict visitors to home doorway
            + y*dists[a]                    # move residents in from doorway
            for y, v in enumerate(r, z + 1)
            if v != a
        )

    return c


# determine state vector from complete occupancy map of rooms
def grok_rooms(rooms):
    # number of spaces remaining to fill in each room
    rem = bytes(
        count_evicts(*ir)
        for ir in enumerate(rooms, 1)
    )

    return rem, [
        # evictions for each room
        r[:y].lstrip(b'\0')
        for r, y in zip(rooms, rem)
    ]


# count spaces that are empty or need emptied before room can fill
# (effective remaining height of room)
def count_evicts(a0, room):
    h = 0
    for y, a in enumerate(room, 1):
        if a != a0:
            # state invariant – occupants at back of room
            assert a or not any(room[:y])
            h = y
    return h


def read(file):
    lines = [
        parse_line(l)
        for l in file.read().split()[1:-1]
    ]

    # NB amphipod burrow configuration is hardcoded throughout:
    assert len(lines[0]) == 11                  # fixed hall width
    assert not any(lines[0][2:9:2])             # assumed hall doorway indices
    assert all(len(l) == 4 for l in lines[1:])  # fixed number of rooms

    return lines[0], [
        bytes(l[i] for l in lines[1:])          # transpose rooms
        for i in range(4)
    ]


def parse_line(line):
    return bytes(max(0, ord(c) - ord('A') + 1)
                 for c in line.replace('#', ''))


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    assert search(read(data('ex0.txt'))) == 12521

def test1_answer(data):
    assert search(read(data('input.txt'))) == 15338


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex0(data):
    assert search(unfold(*read(data('ex0.txt')))) == 44169

def test2_answer(data):
    assert search(unfold(*read(data('input.txt')))) == 47064


#------------------------------------------------------------------------------
def test_ex0(ascript):
    assert ascript('ex0.txt') == '''\
part[1]: 12521
part[2]: 44169
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 15338
part[2]: 47064
'''
