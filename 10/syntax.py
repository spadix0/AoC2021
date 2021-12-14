#!/usr/bin/env python3
from functools import reduce
from statistics import median

closer = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

err_score = {
    None: 0,
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

cpl_score = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def main():
    from sys import argv
    with open(argv[1]) as file:
        code = read(file)

    print('part[1]:', error_score(code))
    print('part[2]:', completion_score(code))


def error_score(code):
    return sum(err_score[parse(l)[1]] for l in code)


def completion_score(code):
    return median(_cpl_score_line(cpl)
                  for l in code
                  if (cpl := parse(l)[0]))


def _cpl_score_line(cpl):
    return reduce(lambda a,c: 5*a + cpl_score[c], cpl, 0)


def parse(line):
    ctx = [ ]
    for c in line:
        if m := closer.get(c):
            ctx.append(m)
        elif c != ctx.pop():
            return (), c
    ctx.reverse()
    return ctx, None


def read(file):
    return [ l.strip() for l in file ]


if __name__ == '__main__':
    main()


#------------------------------------------------------------------------------
# part 1 examples

def test1_ex0(data):
    code = read(data('ex0.txt'))
    assert [ parse(l)[1] for l in code ] == [
        None,
        None,
        '}',
        None,
        ')',
        ']',
        None,
        ')',
        '>',
        None
    ]
    assert error_score(code) == 26397

def test1_answer(data):
    assert error_score(read(data('input.txt'))) == 319329


#------------------------------------------------------------------------------
# part 2 examples

def test2_ex0(data):
    code = read(data('ex0.txt'))
    assert [ ''.join(parse(l)[0]) for l in code ] == [
        '}}]])})]',
        ')}>]})',
        '',
        '}}>}>))))',
        '',
        '',
        ']]}}]}]}>',
        '',
        '',
        '])}>'
    ]

    for l,cs in [
            ('}}]])})]', 288957),
            (')}>]})', 5566),
            ('}}>}>))))', 1480781),
            (']]}}]}]}>', 995444),
            ('])}>', 294),
    ]:
        assert _cpl_score_line(l) == cs

    assert completion_score(code) == 288957

def test2_answer(data):
    assert completion_score(read(data('input.txt'))) == 3515583998


#------------------------------------------------------------------------------
def test_ex0(ascript):
    assert ascript('ex0.txt') == '''\
part[1]: 26397
part[2]: 288957
'''

def test_input(ascript):
    assert ascript('input.txt') == '''\
part[1]: 319329
part[2]: 3515583998
'''
