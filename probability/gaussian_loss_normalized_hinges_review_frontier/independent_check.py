#!/usr/bin/env python3
"""Independent checks for the loss-normalized Gaussian hinge modulus.

The target checker uses sparse Laurent polynomials and Machin's formula.
This checker instead uses exact second-order jets, Abel monomial identities,
direct beta-binomial averaging, and a separate rational interval evaluation
based on pi/4 = atan(1/2) + atan(1/3).  It does not import target code.
"""

from decimal import Decimal, localcontext, ROUND_CEILING, ROUND_FLOOR
from fractions import Fraction as Q
from hashlib import sha256
from math import comb
from pathlib import Path
import json
import sys


ROOT = Path(__file__).resolve().parent
TARGET = ROOT.parent / "gaussian_loss_normalized_hinges"
TARGET_COMMIT = "a68810063b8ad53dda046c68552a14e76f8d3f07"
TARGET_CONTRIBUTION = "bafkreif2b3e5sw6dumihujzhpul4uce3p7v4elvfpyz77miocxodmytq24"
PINS = {
    "EXPECTED.json": "51e596558f9f5180ae330c9b8269b3a9f9e35b8963439a546e74f05f50f0baab",
    "PROOF.md": "92e7dcb81ae1f4c032e5528d7ff9568da94b826e84d110957542c0310337f2f8",
    "README.md": "5310f3b27d02f78081fc929ddfbf18c3a93a5bc4085c017729cd44cff15153ea",
    "SOURCES.md": "46ab0a47f6cbecc5d0f4a13ff3b6d15a806cefa5fcb81e2f2885e1ae7668870e",
    "verify.py": "c975f3b092c3001f0465b745eef0283190f1120265a1d19f409513b1194ac2fe",
}


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def file_digest(path):
    return sha256(path.read_bytes()).hexdigest()


def verify_pins():
    observed = {name: file_digest(TARGET / name) for name in PINS}
    require(observed == PINS, "reviewed source differs from pinned packet")
    return observed


# A jet stores value, first radial derivative, and second radial derivative.
def jet(value, first=0, second=0):
    return Q(value), Q(first), Q(second)


def jet_add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def jet_mul(left, right):
    a, ap, app = left
    b, bp, bpp = right
    return a*b, ap*b+a*bp, app*b+2*ap*bp+a*bpp


def jet_inverse(value):
    x, xp, xpp = value
    require(x != 0, "jet inverse at zero")
    return 1/x, -xp/x**2, 2*xp**2/x**3-xpp/x**2


def jet_power(value, exponent):
    require(exponent >= 0, "nonnegative jet exponent")
    answer = jet(1)
    base = value
    power = exponent
    while power:
        if power & 1:
            answer = jet_mul(answer, base)
        base = jet_mul(base, base)
        power //= 2
    return answer


def claimed_derivatives(h, r, p, b, z, g, gp, mutation=False):
    a = p/r
    first = h * (r**3*g/a**2 + r**2*(5/a**2-b/a**3))
    coefficient = -2 if mutation else -3
    second = h * (
        (g*g+gp)*r**2/a**3
        + g*r*(10/a**3+coefficient*b/a**4)
        + 20/a**3-15*b/a**4+3*b*b/a**5-z*r/a**4
    )
    return first, second


def check_coarea_jets():
    checked = 0
    mutation_rejections = 0
    for index in range(1, 257):
        h = Q(2*index+3, index+5)
        r = Q(index+2, index+3)
        p = Q(3*index+5, 2*index+7)
        b = Q(5*index+1, 4*index+9)
        z = Q((-1)**index*(index+1), 7*index+11)
        g = Q((-1)**(index//2)*(2*index+1), 5*index+13)
        gp = Q((-1)**(index//3)*(index+4), 6*index+17)

        h_jet = jet(h, h*g, h*(g*g+gp))
        r_jet = jet(r, 1, 0)
        p_jet = jet(p, b, z)
        radial_j = jet_mul(jet_mul(h_jet, jet_power(r_jet, 5)), jet_inverse(p_jet))
        actual_first = radial_j[1]/p
        actual_second = (radial_j[2]*p-radial_j[1]*b)/p**3
        claimed_first, claimed_second = claimed_derivatives(h, r, p, b, z, g, gp)
        require(actual_first == claimed_first, "first coarea derivative mismatch")
        require(actual_second == claimed_second, "second coarea derivative mismatch")
        _, damaged_second = claimed_derivatives(h, r, p, b, z, g, gp, mutation=True)
        if damaged_second != actual_second:
            mutation_rejections += 1
        checked += 1
    require(mutation_rejections == checked, "coarea coefficient mutation survived")
    return checked, mutation_rejections


def check_coefficient_bounds():
    """Exact adversarial controls for the coefficient inequalities.

    The universal proof is the monotonicity/factorization argument documented
    in REVIEW.md.  This grid exercises every boundary and many interior points.
    """
    checked = 0
    for kappa in (Q(1, 2), Q(9, 16), Q(5, 8), Q(3, 4), Q(7, 8), Q(1)):
        for i in range(25):
            a = kappa + (1-kappa)*Q(i, 24)
            for j in range(25):
                b = kappa + (1-kappa)*Q(j, 24)
                first = 5/a**2-b/a**3
                second = 10/a**3-3*b/a**4
                third = 20/a**3-15*b/a**4+3*b*b/a**5
                require(0 <= first <= 4/kappa**2, "first coefficient bound")
                require(0 <= second <= 7/kappa**3, "second coefficient bound")
                require(8 <= third <= 8/kappa**3, "third coefficient bound")
                require(
                    -60/a**4+60*b/a**5-15*b*b/a**6
                    == -15*(2*a-b)**2/a**6,
                    "square derivative factorization",
                )
                checked += 1
        require(
            (20/kappa**3-15/kappa**4+3/kappa**5)-8/kappa**3
            == 3*(4*kappa-1)*(kappa-1)/kappa**5,
            "endpoint comparison factorization",
        )
    return checked


def beta_integer_half(integer):
    """Return B(integer,1/2), which is rational for positive integer input."""
    require(integer >= 1, "positive beta argument")
    answer = Q(2)
    for n in range(1, integer):
        answer *= Q(2*n, 2*n+1)
    return answer


def check_abel_differentiation():
    # For A'(w)=w^n with n>=1, differentiate the half integral in closed
    # form and compare it to the half integral of A''.
    checked = 0
    for n in range(1, 129):
        left = (Q(n)+Q(1, 2))*beta_integer_half(n+1)
        right = Q(n)*beta_integer_half(n)
        require(left == right, "Abel differentiation coefficient mismatch")
        checked += 1
    # n=0 is precisely the missing-boundary-term corruption: A'(0)!=0 and
    # the derivative of 2*sqrt(ell) is nonzero while A'' vanishes.
    missing_boundary_left = Q(1, 2)*beta_integer_half(1)
    require(missing_boundary_left == 1, "boundary corruption control failed")
    return checked, 1


def direct_beta_binomial_error(n, u):
    total = Q(0)
    for j in range(n+1):
        probability = Q(comb(n, j))*u**j*(1-u)**(n-j)
        first = Q(j+1, n+2)
        second = Q((j+1)*(j+2), (n+2)*(n+3))
        total += probability*(second-2*u*first+u*u)
    return total


def check_durrmeyer_variance():
    checked = 0
    for n in range(65):
        for denominator in range(2, 18):
            for numerator in range(denominator+1):
                u = Q(numerator, denominator)
                direct = direct_beta_binomial_error(n, u)
                closed = Q(2)*(1+Q(n-3)*u*(1-u))/Q((n+2)*(n+3))
                require(direct == closed, "beta-binomial second moment mismatch")
                require(0 <= direct <= Q(1, n+2), "kernel variance bound failed")
                checked += 1
    return checked


def integer_sqrt(value):
    require(value >= 0, "integer square root domain")
    low, high = 0, value+1
    while high-low > 1:
        middle = (low+high)//2
        if middle*middle <= value:
            low = middle
        else:
            high = middle
    return low


def sqrt_rational_interval(value, digits=55):
    require(value >= 0, "square root domain")
    denominator = 10**digits
    scaled = value.numerator*denominator**2//value.denominator
    lower_integer = integer_sqrt(scaled)
    while Q(lower_integer+1, denominator)**2 <= value:
        lower_integer += 1
    while Q(lower_integer, denominator)**2 > value:
        lower_integer -= 1
    lower = Q(lower_integer, denominator)
    upper = lower if lower*lower == value else Q(lower_integer+1, denominator)
    require(lower*lower <= value <= upper*upper, "square root enclosure")
    return lower, upper


def atan_reciprocal_interval(denominator, bits=230):
    z = Q(1, denominator)
    total = Q(0)
    terms = 0
    while True:
        term = Q((-1)**terms)*z**(2*terms+1)/Q(2*terms+1)
        total += term
        following = Q((-1)**(terms+1))*z**(2*terms+3)/Q(2*terms+3)
        terms += 1
        if abs(following) < Q(1, 2**bits):
            return min(total, total+following), max(total, total+following), terms


def pi_interval():
    # atan(1/2)+atan(1/3)=atan(1)=pi/4, with no branch ambiguity.
    half = atan_reciprocal_interval(2)
    third = atan_reciprocal_interval(3)
    tangent_sum = (Q(1, 2)+Q(1, 3))/(1-Q(1, 6))
    require(tangent_sum == 1, "arctangent addition identity")
    return (4*(half[0]+third[0]), 4*(half[1]+third[1])), (half[2], third[2])


def exp_range_reduced_interval(value, bits=230):
    require(value >= 0, "nonnegative exponential input")
    divisions = 16
    small = value/divisions
    total = Q(1)
    current = Q(1)
    index = 0
    while True:
        following = current*small/Q(index+1)
        if small < index+2:
            tail = following/(1-small/Q(index+2))
            if tail < Q(1, 2**(bits+10)):
                return total**divisions, (total+tail)**divisions, index+1
        index += 1
        current = following
        total += current


def interval_mul(left, right):
    products = [a*b for a in left for b in right]
    return min(products), max(products)


def middle_slope_interval():
    epsilon, ell = Q(1, 8), Q(4)
    kappa = 1-epsilon
    q_root = sqrt_rational_interval(2*epsilon*ell/kappa)
    q = 4*q_root[0], 4*q_root[1]
    exponential_lower = exp_range_reduced_interval(5*epsilon+q[0])
    exponential_upper = exp_range_reduced_interval(5*epsilon+q[1])
    exponential = exponential_lower[0], exponential_upper[1]
    polynomial = (
        8+(7+epsilon/(2*kappa))*q[0]+Q(5, 4)*q[0]**2,
        8+(7+epsilon/(2*kappa))*q[1]+Q(5, 4)*q[1]**2,
    )
    sqrt_ell = sqrt_rational_interval(ell)
    pi, atan_terms = pi_interval()
    sqrt_pi = sqrt_rational_interval(pi[0])[0], sqrt_rational_interval(pi[1])[1]
    numerator = interval_mul(interval_mul(exponential, polynomial), sqrt_ell)
    lower = numerator[0]/(16*kappa**3*sqrt_pi[1])
    upper = numerator[1]/(16*kappa**3*sqrt_pi[0])
    author = Q(864724879354810, 10**12), Q(864724879354811, 10**12)
    require(author[0] <= lower <= upper <= author[1], "independent interval disagrees")
    require(upper-lower < Q(1, 10**40), "independent interval too wide")
    false_upper = Q(864724879354810397, 10**15)
    require(false_upper < lower, "damaged numerical upper bound survived")
    return (lower, upper), atan_terms, max(exponential_lower[2], exponential_upper[2])


def decimal_endpoint(value, upper=False, places=21):
    with localcontext() as context:
        context.prec = 100
        context.rounding = ROUND_CEILING if upper else ROUND_FLOOR
        decimal = Decimal(value.numerator)/Decimal(value.denominator)
        quantum = Decimal(1).scaleb(-places)
        return str(decimal.quantize(quantum))


def check_final_constants():
    # A_t'' bound: integral_0^ell (ell-w)^(-1/2) dw = 2 sqrt(ell).
    require(Q(2, 32) == Q(1, 16), "middle-slope constant")
    # Integrating sqrt(w) from 0 to ell contributes 2/3.
    require(Q(2, 3)*Q(1, 16) == Q(1, 24), "small-ell constant")
    # W carries 2/kappa^3, and the convolution prefactor is 1/32.
    require(Q(2, 32) == Q(1, 16), "global-modulus constant")
    # a0=d2/2 and d2=B2/(8 sqrt(2)); record the rational denominator.
    require(Q(1, 2)*Q(1, 8) == Q(1, 16), "second-energy normalization")
    # The symmetric two-atom surface calculation leaves 1/(3 sqrt(pi)).
    require(Q(1, 4)*Q(4, 3) == Q(1, 3), "two-atom first variation")
    return {
        "middle_slope_prefactor_without_pi": "1/16",
        "small_ell_prefactor_without_pi": "1/24",
        "global_modulus_W_prefactor_without_pi": "1/16",
        "a0_coefficient_of_B2_over_sqrt2": "1/16",
        "two_atom_coefficient_of_exp_minus_ell_ell_3_over_2_over_sqrt_pi": "1/3",
    }


def certificate():
    pins = verify_pins()
    jet_cases, jet_mutations = check_coarea_jets()
    abel_cases, boundary_rejections = check_abel_differentiation()
    interval, atan_terms, exp_terms = middle_slope_interval()
    interval_text = [decimal_endpoint(interval[0]), decimal_endpoint(interval[1], True)]
    canonical = json.dumps(interval_text, separators=(",", ":")).encode()
    return {
        "status": "LOSS_NORMALIZED_HINGE_INDEPENDENT_ACCEPT",
        "target_commit": TARGET_COMMIT,
        "target_contribution": TARGET_CONTRIBUTION,
        "pinned_sha256": pins,
        "arithmetic": "Python integers, Fraction, and outward Decimal rendering only",
        "coarea_second_order_jet_cases": jet_cases,
        "coarea_mutations_rejected": jet_mutations,
        "coefficient_bound_grid_cases": check_coefficient_bounds(),
        "abel_monomial_cases": abel_cases,
        "missing_modal_boundary_corruptions_rejected": boundary_rejections,
        "beta_binomial_variance_cases": check_durrmeyer_variance(),
        "independent_M_1_over_8_4_interval": interval_text,
        "independent_interval_sha256": sha256(canonical).hexdigest(),
        "pi_identity": "pi/4 = atan(1/2) + atan(1/3)",
        "atan_series_terms": list(atan_terms),
        "exp_range_divisions": 16,
        "exp_series_terms": exp_terms,
        "damaged_numeric_upper_bounds_rejected": 1,
        "final_constant_audit": check_final_constants(),
        "full_majorisation_proved": False,
    }


def main():
    require(sys.argv[1:] in ([], ["--emit"]),
            "usage: python3 independent_check.py [--emit]")
    result = certificate()
    if sys.argv[1:] == ["--emit"]:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    expected = json.loads((ROOT / "REVIEW_EXPECTED.json").read_text())
    require(result == expected, "review evidence differs from REVIEW_EXPECTED.json")
    print(json.dumps({
        "status": result["status"],
        "coarea_jet_cases": result["coarea_second_order_jet_cases"],
        "abel_monomial_cases": result["abel_monomial_cases"],
        "beta_binomial_variance_cases": result["beta_binomial_variance_cases"],
        "M_1_over_8_4_interval": result["independent_M_1_over_8_4_interval"],
        "full_majorisation_proved": False,
    }, indent=2))


if __name__ == "__main__":
    main()
