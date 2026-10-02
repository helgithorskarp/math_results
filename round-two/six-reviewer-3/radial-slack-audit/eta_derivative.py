"""Full interval eta derivatives, with a fixed tail on a complete rectangle."""
from prior import I, F, need, cx, derivative
from normal import partials, determinant2


class Dual:
    def __init__(self, value=0, dot=0):
        if isinstance(value, Dual):
            self.value, self.dot = value.value, value.dot
        else:
            self.value, self.dot = I(value), I(dot)
    def __add__(self, b):
        b = Dual(b)
        return Dual(self.value + b.value, self.dot + b.dot)
    __radd__ = __add__
    def __neg__(self):
        return Dual(-self.value, -self.dot)
    def __sub__(self, b):
        return self + -Dual(b)
    def __rsub__(self, b):
        return Dual(b) + -self
    def __mul__(self, b):
        b = Dual(b)
        return Dual(self.value * b.value, self.dot * b.value + self.value * b.dot)
    __rmul__ = __mul__
    def inv(self):
        need(not self.value.lo <= 0 <= self.value.hi, 'nonzero whole-rectangle dual divisor')
        return Dual(self.value.inv(), -self.dot / self.value.square())
    def __truediv__(self, b):
        return self * Dual(b).inv()
    def __rtruediv__(self, b):
        return Dual(b) * self.inv()
    def __pow__(self, n):
        need(type(n) is int and n >= 0, 'nonnegative dual power')
        out = Dual(1)
        for _ in range(n):
            out *= self
        return out
    def __eq__(self, b):
        b = Dual(b)
        return self.value == b.value and self.dot == b.dot


def multiplier_derivatives(box, c):
    box, c = list(map(Dual, box)), Dual(c)
    eta = Dual(I(0, F(1, 65536)), I(1))
    p, qs = partials(eta, box)
    zp = [0] + derivative(p)
    phases = [-F(1, 2) + eta * box[3], -c + eta * box[4]]
    J, cr = [], []
    combo = cx.primitive(cx.scale(cx.convolution(cx.power([-eta * box[0], 1], 6), [1 - eta, -1]), 9), 1 - eta)
    for tau in phases:
        sine2 = 1 - tau * tau
        den = cx.circle(zp, tau)
        J.append([-cx.ratio(cx.circle(q, tau), den, sine2)[0][0] for q in qs[:2]])
        cr.append(cx.ratio(cx.circle(combo, tau), den, sine2)[0][0])
    determinant = determinant2(J)
    need(determinant.value.lo > 0, 'regular even block throughout derivative rectangle')
    W = 1 + eta * box[5]
    weights = [cr[1] / (W**3 * determinant), -cr[0] / (W**3 * determinant)]
    return {'even_matrix_eta_derivatives': [[x.dot.record() for x in row] for row in J],
            'even_determinant_eta_derivative': determinant.dot.record(),
            'individual_multiplier_eta_derivatives': [x.dot.record() for x in weights]}, [x.dot for x in weights]
