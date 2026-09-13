from family import *
from math import lcm

def f_local(x, bits=3):
    a, b, c, d = x
    require(c == d == 0, 'c == d == 0')
    den = lcm(a.denominator, b.denominator)
    aa = int(a * den)
    bb = int(b * den)
    de = (den & -den).bit_length() - 1
    nb = 16
    while True:
        mod = 1 << nb
        r = K.root33(nb)
        n = (aa + bb * r) * pow(den >> de, -1, mod) % mod
        if n:
            val = (n & -n).bit_length() - 1
            if val + bits <= nb:
                return (val - de, (n >> val) % (1 << bits))
        nb *= 2
        require(nb < 4096, 'nb < 4096')

def e_val(x):
    return f_local(norm(x), 3)[0] // 2
