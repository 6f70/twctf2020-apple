#!/usr/bin/env python3
from z3 import *
from struct import pack, unpack

#FLAG        = b'Koit5uH@Rin9orou'
FLAG        = b'Rin9oWoT@berun9o'

func2_table = [4008446428, None, 205799423, 2678651991]

FUNC4_TABLE = [4225317655, 2809032755, 91827849, 2462969875]
FUNC5_TABLE = [1154738393, 1197026425, 4005351880, 4106543864]
ROUND_NUM   = 4

def func1(data):
    data = [
            data[0] + data[0] * data[1],
            data[1] + data[1] * data[2],
            data[2] + data[2] * data[3],
            data[3] + data[3] * data[0],
    ]
    return data

def func2(data):
    data = [d + t for d, t in zip(data, func2_table)]
    return data

def func3_fake(data):
    data = [
            data[0] + URem(data[0], data[1]),
            data[1] + URem(data[1], data[2]),
            data[2] + URem(data[2], data[3]),
            data[3] + URem(data[3], data[0]),
    ]
    return data

def func3_real(data):
    rem_or_sqr = lambda x, y: If(y == 0, x * x, URem(x, y))
    data = [
            data[0] + rem_or_sqr(data[0], data[1]),
            data[1] + rem_or_sqr(data[1], data[2]),
            data[2] + rem_or_sqr(data[2], data[3]),
            data[3] + rem_or_sqr(data[3], data[0]),
    ]
    return data

def func4(data):
    data = [d - t for d, t in zip(data, FUNC4_TABLE)]
    return data

def func5(data):
    data = [d ^ t for d, t in zip(data, FUNC5_TABLE)]
    return data

def bvs2long(data):
    s = Solver()
    bvs = BitVecs((f'bvs{i}' for i in range(4)), 32)
    for bv, h in zip(bvs, data):
        s.add(bv == h)

    assert s.check() == sat
    return [s.model()[bv].as_long() for bv in bvs]

def _calc_hash(data, funclist, dump):
    for _ in range(ROUND_NUM):
        for f in funclist:
            if dump:
                print("state    : " + ' '.join('{0:08x}'.format(v) for v in bvs2long(data)))

            data = f(data)

    return data

def calc_hash_real(data, dump=False):
    return _calc_hash(data, (func1, func2, func3_real, func4, func5), dump)

def calc_hash_fake(data, dump=False):
    return _calc_hash(data, (func1, func2, func3_fake, func4, func5), dump)

def calc_flag(hashdata, real=False, exclude=None):
    s = Solver()
    flag = BitVecs((f'flag{i}' for i in range(4)), 32)
    for i in range(16):
        ch = LShR(flag[i // 4], (i % 4) * 8) & 0xff
        s.add(ch >= ord(' '))
        s.add(ch <= ord('~'))

    hashbv = calc_hash_real(flag[::]) if real else calc_hash_fake(flag[::])

    if exclude:
        s.add(
            Not(
                And(
                    *(f == e for f, e in zip(flag, exclude))
                )
            )
        )

    for hbv, hdata in zip(hashbv, hashdata):
        s.add(hbv == hdata)

    if s.check() == sat:
        return [s.model()[bv].as_long() for bv in flag]
    elif s.check() == unsat:
        return None
    else:
        assert False

def set_func2_table(flag):
    trapidx = func2_table.index(None)
    trapval = BitVec('trapval', 32)
    func2_table[trapidx] = trapval

    data = func1(flag)
    data = func2(data)

    s = Solver()
    s.add(data[trapidx] == 0)

    assert s.check() == sat
    func2_table[trapidx] = s.model()[trapval].as_long()

if __name__ == '__main__':
    flag = [BitVecVal(v, 32) for v in unpack('<4I', FLAG)]
    print('flag     : ' + ' '.join(f'{h:08x}' for h in unpack('<4I', FLAG)))

    set_func2_table(flag[::])
    print('f2table  : ' + ' '.join(f'{v:08x}' for v in func2_table))

    hash_fake = bvs2long(calc_hash_fake(flag[::]))
    print('fake     : ' + ' '.join(f'{h:08x}' for h in hash_fake))
    hash_real = bvs2long(calc_hash_real(flag[::]))
    print('real     : ' + ' '.join(f'{h:08x}' for h in hash_real))

    print('Calculating flag with real hashfunc......')
    calc_flag_real = calc_flag(hash_real, real=True)
    print('flag     : ' + ' '.join(f'{v:08x}' for v in calc_flag_real))
    assert list(calc_flag_real) == list(unpack('<4I', FLAG))

    print('Calculating another flag with real hashfunc......')
    calc_flag_anth = calc_flag(hash_real, real=True, exclude=unpack('<4I', FLAG))
    assert calc_flag_anth is None
    print('No flags found.')

    print('Calculating flag with fake hashfunc......')
    calc_flag_fake = calc_flag(hash_real, real=False)
    assert calc_flag_fake is None
    print('No flags found.')
