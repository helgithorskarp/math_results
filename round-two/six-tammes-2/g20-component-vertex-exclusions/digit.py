"""Exact identities from coefficient bounds and an injective integer radix.

No polynomial interpolation, modular probability, or expanded-ring input.
Expressions track separate degrees and the sum of absolute coefficients.
"""
from functools import lru_cache


class Expr:
    __slots__ = ('op', 'args', 'dt', 'dz', 'norm')

    def __init__(self, op, args, dt, dz, norm):
        self.op, self.args = op, args
        self.dt, self.dz, self.norm = dt, dz, norm

    def __add__(self, other):
        other = expr(other)
        if not self.norm:
            return other
        if not other.norm:
            return self
        return Expr('+', (self, other), max(self.dt, other.dt),
                    max(self.dz, other.dz), self.norm + other.norm)

    __radd__ = __add__

    def __neg__(self):
        return Expr('-', (self,), self.dt, self.dz, self.norm)

    def __sub__(self, other):
        return self + -expr(other)

    def __rsub__(self, other):
        return expr(other) + -self

    def __mul__(self, other):
        other = expr(other)
        if not self.norm or not other.norm:
            return expr(0)
        return Expr('*', (self, other), self.dt + other.dt,
                    self.dz + other.dz, self.norm * other.norm)

    __rmul__ = __mul__

    def __pow__(self, power):
        if type(power) is not int or not 0 <= power <= 100:
            raise ValueError('nonnegative bounded integer exponent required')
        result, base = expr(1), self
        while power:
            if power & 1:
                result = result * base
            base = base * base
            power >>= 1
        return result


def expr(value):
    if isinstance(value, Expr):
        return value
    if type(value) is not int:
        raise TypeError('integer coefficient required')
    return Expr('c', (value,), 0, 0, abs(value))


T = Expr('t', (), 1, 0, 1)
Z = Expr('z', (), 0, 1, 1)


def integer_image(node, radix_bits, stride):
    """Evaluate a DAG, releasing all large intermediate integers afterward."""
    @lru_cache(None)
    def evaluate(n):
        if n.op == 'c':
            return n.args[0]
        if n.op == 't':
            return 1 << radix_bits
        if n.op == 'z':
            return 1 << (radix_bits * stride)
        if n.op == '+':
            return evaluate(n.args[0]) + evaluate(n.args[1])
        if n.op == '-':
            return -evaluate(n.args[0])
        if n.op == '*':
            return evaluate(n.args[0]) * evaluate(n.args[1])
        raise ValueError('unknown expression operation')
    result = evaluate(node)
    evaluate.cache_clear()
    return result


def image_record(node):
    # Every actual coefficient is <= norm < radix/2. No floating bound.
    bits = max(2, node.norm.bit_length() + 2)
    stride = node.dt + 1
    if bits > 2048 or stride > 128 or node.dz > 32:
        raise RuntimeError('fixed proof-computation limit; no conclusion')
    value = integer_image(node, bits, stride)
    return value, {'separate_degree_bound': [node.dt, node.dz],
                   'coefficient_l1_bound_bits': node.norm.bit_length(),
                   'radix_bits': bits, 'stride': stride,
                   'image_is_zero': value == 0}


def prove_zero(node):
    value, record = image_record(node)
    if value:
        raise ValueError('nonzero exact integer image of claimed identity')
    return record


def coefficients(node):
    """Recover all integer coefficients using certified balanced radix digits."""
    value, record = image_record(node)
    bits, stride = record['radix_bits'], record['stride']
    radix = 1 << bits
    result, index = {}, 0
    while value:
        remainder = value % radix
        if remainder > radix // 2:
            remainder -= radix
        value = (value - remainder) // radix
        if remainder:
            i, j = index % stride, index // stride
            if i > node.dt or j > node.dz or abs(remainder) > node.norm:
                raise ValueError('digit outside proved support or bound')
            result[i, j] = remainder
        index += 1
        if index > stride * (node.dz + 1):
            raise ValueError('integer image exceeded proved degree')
    return result


def monomials(rows):
    result = expr(0)
    seen = set()
    for i, j, value in rows:
        if (i, j) in seen or type(i) is not int or type(j) is not int:
            raise ValueError('duplicate or noninteger monomial')
        if not (0 <= i <= 64 and 0 <= j <= 16) or type(value) is not int:
            raise ValueError('monomial outside fixed exact input limits')
        seen.add((i, j))
        result += value * T ** i * Z ** j
    return result
