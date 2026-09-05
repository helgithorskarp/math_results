"""K(s), K=Q(exp(pi*i/21)), s^2=-11 and conjugate(s)=-s."""
from pathlib import Path
import importlib.util

PARENT = Path(__file__).resolve().parent.parent/'hadwiger_nelson_heptagon_difference_lifts'
_spec = importlib.util.spec_from_file_location('heptagon_cyclotomic42', PARENT/'geometry.py')
K = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(K)

ZERO = (0,)*24
ONE = K.ONE+K.ZERO


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def scale(a, n):
    return tuple(n*x for x in a)


def mul(a, b):
    return (K.sub(K.mul(a[:12], b[:12]), K.scale(K.mul(a[12:], b[12:]), 11)) +
            K.add(K.mul(a[:12], b[12:]), K.mul(a[12:], b[:12])))


def conjugate(a):
    return K.conj(a[:12])+K.neg(K.conj(a[12:]))


def norm(a):
    return mul(a, conjugate(a))


def construction():
    h, denominator = K.integerize(K.host())
    assert denominator == 7
    H = [K.scale(a, 6)+K.ZERO for a in h]
    u, v = K.sub(h[7], h[0]), K.sub(h[14], h[0])
    directions = [u, v, K.add(u, v)]
    M = [ZERO]+[K.scale(a, 6)+K.ZERO for a in directions]+[K.scale(a, 5)+a for a in directions]
    return H, M, 42
