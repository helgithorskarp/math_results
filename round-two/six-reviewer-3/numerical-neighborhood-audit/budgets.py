"""Exact universal analytic budgets in u=sqrt(eta), delta; no eta samples."""
from dataclasses import dataclass, replace
from fractions import Fraction as Q
from math import comb, factorial


def need(condition, message):
    if not condition:
        raise ValueError(message)


@dataclass(frozen=True)
class Monomial:
    coefficient: Q
    u: int = 0
    delta: int = 0

    def __post_init__(self):
        object.__setattr__(self, 'coefficient', Q(self.coefficient))
        need(type(self.u) is int and type(self.delta) is int, 'integral sqrt-eta/delta exponents')

    def __mul__(self, other):
        other = box(other)
        return Monomial(self.coefficient * other.coefficient, self.u + other.u, self.delta + other.delta)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = box(other)
        need(other.coefficient > 0, 'positive symbolic divisor')
        return Monomial(self.coefficient / other.coefficient, self.u - other.u, self.delta - other.delta)

    def __rtruediv__(self, other):
        return box(other) / self

    def __pow__(self, exponent):
        need(type(exponent) is int, 'integral symbolic power')
        need(self.coefficient > 0 or exponent >= 0, 'nonzero negative power')
        return Monomial(self.coefficient**exponent, self.u * exponent, self.delta * exponent)

    def record(self):
        return {'coefficient': str(self.coefficient), 'sqrt_eta_exponent': self.u, 'delta_exponent': self.delta}


def box(value):
    return value if isinstance(value, Monomial) else Monomial(value)


def power2(exponent, u=0, delta=0):
    return Monomial(Q(2)**exponent, u, delta)


U = Monomial(1, 1)
ETA = U**2
DELTA = Monomial(1, 0, 1)
UMAX, DMAX = Q(1, 256), Q(1, 2)


class Certificates:
    def __init__(self):
        self.rows = []

    def comparison(self, name, terms, right, strict=True):
        terms = terms if isinstance(terms, (tuple, list)) else [terms]
        ratios = [box(term) / right for term in terms]
        for ratio in ratios:
            need(ratio.coefficient >= 0, 'nonnegative majorant: ' + name)
            need(ratio.u >= 0 and ratio.delta >= 0, 'uncovered singular ratio: ' + name)
        upper = sum((x.coefficient * UMAX**x.u * DMAX**x.delta for x in ratios), Q(0))
        need(upper < 1 if strict else upper <= 1, 'unproved whole-domain budget: ' + name)
        self.rows.append({'name': name, 'normalized_nonnegative_monomials': [x.record() for x in ratios], 'upper_on_complete_domain': str(upper), 'strict': strict})

    def equal(self, name, left, right):
        need(left == right, 'symbolic exponent/constant identity: ' + name)
        self.rows.append({'name': name, 'identity': left.record()})


@dataclass(frozen=True)
class Domains:
    name: str
    rho: Monomial
    inverse: Monomial
    B1: Monomial
    B2: Monomial
    tail: Monomial
    target: Monomial
    radial: Monomial
    free: Monomial
    raw: Monomial
    critical: Monomial
    coefficient: Monomial
    original: bool = False


def domains(original=False):
    if original:
        rho, inverse, B1, B2 = power2(-60), power2(10, -4), power2(70), power2(136)
    else:
        rho, inverse, B1, B2 = power2(-27), power2(9, -3), power2(37), power2(70)
    tail = 1 / (8 * inverse * B2)
    target = 1 / (64 * inverse**2 * B1 * B2)
    radial = target**2 / (2**22 if original else 2**31)
    free = DELTA * ETA**2 * target**3 / (2**23 if original else 2**20)
    raw = free / 4
    critical = (ETA**2 if original else U**3) * raw / 2**10
    coefficient = ETA * critical**6 / 2**7
    return Domains('original9315' if original else 'independent_larger_domain', rho, inverse, B1, B2, tail, target, radial, free, raw, critical, coefficient, original)


def certificate(p):
    c = Certificates()
    rho = p.rho
    root_radius = power2(-16)
    c.comparison('raw rho below1/16', rho, box(Q(1, 16)))
    c.comparison('radicand displacement below2rho', [rho, 16 * rho**2], 2 * rho)
    c.comparison('radicand lower modulus above1/4', [2 * rho, Q(1, 4)], box(1))
    c.comparison('free/heavy base coordinate modulus below3', [2, rho], box(3))
    c.comparison('heavy moment m less4rho', Q(7, 2) * rho, 4 * rho)
    c.comparison('moment n less22rho', Q(43, 2) * rho, 22 * rho)
    c.comparison('heavy critical displacement less64rho', [45 * ETA * rho, 6 * U * rho], 64 * rho)
    c.comparison('small critical displacement less64rho', [ETA * rho, U * rho], 64 * rho)
    c.comparison('perturbed critical modulus below1', [Q(1, 32), 64 * rho], box(1))

    S = sum((Q(9, 9-k) * comb(8, k) * Q(1, 32)**k for k in range(1, 9)), Q(0))
    need((1 - UMAX**2)**9 - S > Q(1, 2), 'uniform original constant modulus above1/2')
    c.comparison('root derivative lower bound1/64', box(Q(1, 64)), box(9 * Q(15, 32)**8))
    c.comparison('root disks are disjoint', 2 * root_radius, power2(-13))
    psecond = 72 * (1 + Q(1, 2**16) + Q(1, 32))**7
    c.comparison('root Taylor second derivative below128', box(psecond), box(128))
    c.comparison('root contour p0 exceeds radius/128', [64 * root_radius, Q(1, 128)], box(Q(1, 64)))
    if p.original:
        perturbation = box(3 * 9 * 8 * 64 * 3**7)
        c.comparison('all nine original root Rouche circles', perturbation * rho, root_radius / 128)
    else:
        c.comparison('actual weighted heavy-critical motion below7sqrteta*rho', [45 * ETA * rho, 6 * U * rho], 7 * U * rho)
        c.comparison('actual weighted small-critical motion below7sqrteta*rho', [ETA * rho, U * rho], 7 * U * rho)
        c.comparison('root-disk integration factors bounded9/8', [1, root_radius, Q(1, 32), 7 * U * rho], box(Q(9, 8)))
        perturbation = (3 * 9 * 8 * 7 * Q(9, 8)**7) * U
        c.comparison('all nine original root Rouche circles', perturbation * rho, root_radius / 128)
    c.comparison('each complexified half-normal bounded2', box(((1 + Q(1, 2**16))**2 + 1) / 2), box(2))
    c.comparison('branch reciprocal distance greater15/16', [UMAX**2, Q(1, 32), Q(15, 16)], box(1))
    c.comparison('reciprocal product variation less512rho', [132 * rho, 4096 * rho**2], 512 * rho)
    c.comparison('reciprocal product variation less1/4', 512 * rho, box(Q(1, 4)))
    c.comparison('reciprocal product modulus greater1/2', box(Q(1, 2)), box(Q(15, 16)**2 - Q(1, 4)))

    center_inverse = 800 * U**-3 if p.original else 400 * U**-3
    c.comparison('actual raw four-tail inverse covered', center_inverse, p.inverse)
    c.comparison('sixteen-variable Cauchy first derivative', factorial(1) * 32 * 32 / rho, p.B1, False)
    c.comparison('sixteen-variable Cauchy second derivative', factorial(2) * 32 * 32**2 / rho**2, p.B2, False)
    c.comparison('full tail is inside raw rho/2', 2 * p.tail, rho)
    c.comparison('free and normal targets smaller than tail', p.target, p.tail)
    c.comparison('actual tail contraction at most1/8', p.inverse * p.B2 * p.tail, box(Q(1, 8)), False)
    c.comparison('center contraction drift less tail/4', [p.inverse * p.B1 * p.target, p.inverse * p.target], p.tail / 4)
    c.comparison('inactive original half-normal variation below eta/8', p.B1 * p.tail, ETA / 8)
    c.comparison('real heavy/small h separation', 7 * rho, box(Q(1, 2)))
    c.comparison('actual real reciprocal distances greater1/2', [UMAX**2, Q(1, 32), 64 * rho, Q(1, 2)], box(1))

    K2 = power2(16) / p.target**2
    K3 = 6 * power2(20) / p.target**3
    c.comparison('post-elimination second derivative Cauchy bound', factorial(2) * 32 * 32**2 / p.target**2, K2, False)
    c.comparison('post-elimination third derivative Cauchy bound', factorial(3) * 32 * 32**3 / p.target**3, K3, False)
    c.comparison('entire inward box inside target d/2', 2 * p.radial, p.target)
    c.comparison('free Euclidean ball inside inward max box', p.free, p.radial)
    gradient_loss = Q(1, 64) if p.original else Q(1, 32768)
    c.comparison('all four individual radial derivative variations', K2 * p.radial, box(gradient_loss), False)
    c.comparison('full eliminated Taylor energy loss below delta eta squared', K3 * p.free / 6, DELTA * ETA**2, False)
    c.comparison('twelve free coordinates: Euclidean entry sqrt12*t<R', 12 * p.raw**2, p.free**2)
    c.comparison('raw box realizes the full tail', p.raw, p.tail)
    c.comparison('raw actual four normals enter inward box', p.B1 * p.raw, p.radial)
    c.comparison('all three critical circles remain disjoint', p.critical, ETA / 4)
    c.comparison('all critical circles lie inside unit disk', [Q(1, 32), p.critical], box(1))
    c.comparison('heavy root Rouche product dominates small cluster minimum', p.critical**5, Q(9, 64) * U**5)
    c.comparison('coefficient derivative36*ccoef on every critical circle', 36 * p.coefficient, ETA * p.critical**6)
    c.comparison('all six free u and heavy mean enter raw t', p.critical / ETA, p.raw / 1024, False)
    c.comparison('all six free h enter raw t', p.critical / U, p.raw / 1024, False)
    c.comparison('heavy squared-opening T enters raw t', 5 * p.critical / U, 5 * p.raw / 1024, False)
    c.comparison('total h moment V enters raw t including eta divisor', 8 * p.critical / U**3, 8 * p.raw / 1024, False)
    c.comparison('total hu moment M enters raw t', [16 * p.critical / ETA, 16 * p.critical / U, 8 * p.critical**2 / U**3], 40 * p.raw / 1024)
    c.comparison('free u/h and y,T,V,M transportation is within t', box(Q(40, 1024)), box(1))
    return {'name': p.name, 'constant_modulus_budget_S': str(S), 'literal_original_root_polynomial_perturbation_majorant': perturbation.record(), 'radii': {name: getattr(p, name).record() for name in ['rho', 'inverse', 'B1', 'B2', 'tail', 'target', 'radial', 'free', 'raw', 'critical', 'coefficient']}, 'K2': K2.record(), 'K3': K3.record(), 'individual_gradient_loss': str(gradient_loss), 'complete_domain': {'sqrt_eta': ['positive', str(UMAX)], 'delta': ['positive', str(DMAX)]}, 'certified_whole_domain_comparisons': c.rows}


def controls():
    p = domains()
    damage = [
        ('original-root Rouche collar too large', replace(p, rho=2*p.rho)),
        ('understated first raw Cauchy derivative', replace(p, B1=p.B1/2)),
        ('understated second raw Cauchy derivative', replace(p, B2=p.B2/2)),
        ('lost half eta in actual raw inverse', replace(p, inverse=power2(9, -2))),
        ('understated original normal inverse', replace(p, inverse=p.inverse/2)),
        ('uncontrolled nonlinear tail contraction', replace(p, tail=16*p.tail)),
        ('target product not preserved by contraction', replace(p, target=16*p.target)),
        ('individual radial derivative loss too large', replace(p, radial=16*p.radial)),
        ('post-elimination Taylor loss exceeds energy gap', replace(p, free=2*p.free)),
        ('missing twelve-dimensional infinity-to-Euclidean factor', replace(p, raw=2*p.raw)),
        ('heavy total h moment not controlled', replace(p, critical=1024*p.critical)),
        ('critical-circle Rouche coefficient overflow', replace(p, coefficient=8*p.coefficient)),
    ]
    rejected = []
    for name, bad in damage:
        try:
            certificate(bad)
        except ValueError as error:
            rejected.append({'damage': name, 'rejected_by': str(error)})
        else:
            raise ValueError('mathematical damage accepted: ' + name)
    # Missing limits and negative exponents cannot be declared covered.
    invalid = []
    for name, bad in [('zero symbolic divisor', Monomial(0)), ('negative symbolic divisor', Monomial(-1))]:
        try:
            _ = ETA / bad
        except ValueError:
            invalid.append(name)
        else:
            raise ValueError('invalid symbolic domain accepted')
    for name, term in [('uncovered eta0 inverse', U**-1), ('uncovered k-gap inverse', DELTA**-1)]:
        try:
            Certificates().comparison(name, term, box(1))
        except ValueError:
            invalid.append(name)
        else:
            raise ValueError('singular ratio accepted')
    return {'mathematical_damage_rejections': rejected, 'invalid_domain_rejections': invalid}
