#!/usr/bin/env python3
from z3 import *
from struct import pack

FUNC2_TABLE = [4008446428, 58150609, 205799423, 2678651991]
FUNC4_TABLE = [4225317655, 2809032755, 91827849, 2462969875]
FUNC5_TABLE = [1154738393, 1197026425, 4005351880, 4106543864]
ROUND_NUM   = 4

HASH_CORRECT = [0x5935f1de, 0xb63725e7, 0xdfa10069, 0x4e556f64]

def func1(data):
    data = [
            data[0] + data[0] * data[1],
            data[1] + data[1] * data[2],
            data[2] + data[2] * data[3],
            data[3] + data[3] * data[0],
    ]
    return data

def func2(data):
    data = [d + t for d, t in zip(data, FUNC2_TABLE)]
    return data

def func3(data):
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

def calc_hash(data):
    for _ in range(ROUND_NUM):
        for f in (func1, func2, func3, func4, func5):
            data = f(data)
    return data

def calc_flag():
    s = Solver()
    flag = BitVecs((f'flag{i}' for i in range(4)), 32)
    for i in range(16):
        ch = LShR(flag[i // 4], (i % 4) * 8) & 0xff
        s.add(ch >= ord(' '))
        s.add(ch <= ord('~'))

    hashbv = calc_hash(flag[::])

    for hbv, hdata in zip(hashbv, HASH_CORRECT):
        s.add(hbv == hdata)

    assert s.check() == sat
    return b''.join(pack('<I', s.model()[bv].as_long()) for bv in flag).decode('ascii')

if __name__ == '__main__':
    print('TWCTF{' + calc_flag() + '}')
