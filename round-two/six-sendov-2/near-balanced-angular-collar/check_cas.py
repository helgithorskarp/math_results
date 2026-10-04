"""Same-author dense QQ cross-check. Does not import the Fraction engine.

All rational identities are cleared as entire polynomials. The even-family
moments are derived from the literal squared root levels rather than Newton
recurrence. Requires SymPy 1.14.0. No numerical root finding is used.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sympy as s

t, D, z = s.symbols("t D z")
F = s.Rational
checks = {}


def require(ok, label):
    if not ok:
        raise ValueError(label)
    checks[label] = True


def zero(expr):
    return s.Poly(s.expand(expr), t, domain=s.QQ).is_zero


def coeffs(expr, variable=t):
    p = s.Poly(s.expand(expr), variable, domain=s.QQ)
    return [str(p.nth(i)) for i in range(max(0, p.degree()) + 1)]


inverse_odd = s.expand((1+t)*(1-t+t**2)-1)
inverse_cubic = s.expand((1+t)**2*(1-2*t+3*t**2)-1)
ratio = (4+3*t)/(1+t)**2
ratio_derivative_numerator = s.cancel(s.diff(ratio, t)*(1+t)**3)
require(zero(inverse_odd-t**3), "entire inverse-odd Taylor remainder")
require(zero(inverse_cubic-4*t**3-3*t**4),
        "entire inverse-cubic Taylor remainder")
require(zero(ratio_derivative_numerator+5+3*t),
        "entire monotone inverse-cubic remainder ratio derivative")

Dmax = F(1, 729)
tau = F(1, 27)
m, B, R, L, c = F(29, 100), F(41, 100), F(1, 480), F(40), F(1, 8)
Tmax = 8*tau
require(tau**2 == Dmax, "entire exact square-root endpoint")
require(c-tau > m**2, "all original lower magnitude license")
require(c+tau < B**2, "all original upper magnitude license")
require(3*B < 5*m, "entire strict four-plus-four sign-count comparison")
require(L*tau**3 < R < m, "whole central root search collar")
deriv_lower, S1coef = 8/(B+R)**2, 512/m
require(L*deriv_lower > S1coef, "strict IVT signs for all 0<D<=Dmax")
require(ratio_derivative_numerator.subs(t, -Tmax) < 0 and Tmax < 1,
        "ratio monotone over entire dimensionless deviation interval")
ratio_max = ratio.subs(t, -Tmax)
require(ratio_max == F(2268, 361),
        "whole sharp endpoint inverse-cubic remainder envelope")
S3coef = B*c**(-5)*ratio_max
K1, K2, K = 2*L*S3coef, 24*L**2/(m-R)**4, F(12500000)
require(K1+K2 < K, "complete sum of two central-mass Taylor losses")
bound = 2/(c-tau)+(K/32)*Dmax**2
require(bound == F(237004387, 10097379), "whole final angular rational bound")
require(bound < F(47, 2), "strict high-C exclusion")
margin = F(47, 2)-bound
require(margin == F(568039, 20194758), "whole threshold separation margin")
mass_comparison = s.expand(2*t*(1+t)**2-((1+t)**2-1))
require(zero(mass_comparison-3*t**2-2*t**3),
        "entire mass-to-angular upper comparison")

# Dense polynomial construction of every literal octic coefficient.
f = s.Poly((z**2-c)**2*((z**2-c)**2-D/4), z)
fc = [f.nth(8-i) for i in range(9)]
printed = [1, 0, -F(1, 2), 0, F(3, 32)-D/4, 0,
           -F(1, 128)+D/16, 0, F(1, 4096)-D/256]
require(all(s.Poly(a-b, D, domain=s.QQ).is_zero
            for a, b in zip(fc, printed)),
        "all nine coefficients of literal sharp even family")

# Direct paired real squared-root moments, a different derivation from
# the native engine's Newton recurrence. D>0 and D<1/16 are in PROOF.md.
h = s.sqrt(D)/2
powers = [F(8)]
for k in range(1, 6):
    if k % 2:
        powers.append(F(0))
    else:
        j = k//2
        powers.append(s.expand(4*c**j+2*(c-h)**j+2*(c+h)**j))
require(powers[1] == powers[3] == powers[5] == 0,
        "whole sharp even-family odd moments")
require(powers[2] == 1, "whole sharp even-family norm")
require(powers[4] == c+D, "whole sharp even-family fourth moment")

# Literal inverse-square sum, then rational normalization over QQ[D].
S2_actual = s.cancel(4/c+2/(c-h)+2/(c+h))
S2_den = c**2-D/4
S2_num = s.cancel(S2_actual*S2_den)
m0 = s.cancel(64/S2_actual)
m_num, m_den = 1-16*D, 1-8*D
require(s.cancel(m0-m_num/m_den) == 0,
        "entire central mass of literal sharp even family")
p = s.cancel(1-m0)
require(s.cancel(p-8*D/m_den) == 0,
        "entire complementary mass of sharp even family")
lower_num = s.cancel((1-m0**2-p**2)*m_den**2/D)
upper_num = s.cancel((1-m0**2)*m_den**2/D)
require(s.Poly(lower_num-(16-256*D), D, domain=s.QQ).is_zero,
        "entire sharp-family lower squeeze")
require(s.Poly(upper_num-(16-192*D), D, domain=s.QQ).is_zero,
        "entire sharp-family upper squeeze")
require(lower_num.subs(D, 0) == upper_num.subs(D, 0) == 16,
        "whole two sharp-limit squeeze constants")
require(s.Poly(upper_num-lower_num-64*D, D, domain=s.QQ).is_zero,
        "whole nonnegative sharp-limit squeeze gap")
require(1-16*Dmax > 0, "sharp even-family positive-root domain")
generic_upper, repeated_upper = (1-F(1, 7))/F(47, 2), (1-F(1, 6))/F(47, 2)
require(F(47, 2)*generic_upper == 1-F(1, 7),
        "whole seven-mass high-C endpoint")
require(F(47, 2)*repeated_upper == 1-F(1, 6),
        "whole six-mass high-C endpoint")
require(Dmax < repeated_upper < generic_upper,
        "whole nonempty necessary high-C bands")

record = {
    "actual_agent": "six-sendov-2",
    "role": "researcher",
    "domain": "QQ; characteristic0; whole polynomial identities and rational endpoint signs",
    "parameters": {k: str(v) for k, v in [
        ("Dmax", Dmax), ("sqrt_Dmax", tau), ("m", m), ("B", B),
        ("R", R), ("L", L), ("c", c)]},
    "whole_identities": {
        "inverse_odd_remainder": coeffs(inverse_odd),
        "inverse_cubic_remainder": coeffs(inverse_cubic),
        "ratio_derivative": coeffs(ratio_derivative_numerator),
        "mass_upper_comparison": coeffs(mass_comparison),
        "entire_even_family_octic_coefficients_descending": [coeffs(a, D) for a in fc],
        "entire_even_family_moments": [coeffs(a, D) for a in powers],
        "even_family_central_S2_numerator": coeffs(S2_num, D),
        "even_family_central_S2_denominator": coeffs(S2_den, D),
        "even_family_central_mass_numerator": coeffs(m_num, D),
        "even_family_central_mass_denominator": coeffs(m_den, D),
        "even_family_lower_squeeze_numerator": coeffs(lower_num, D),
        "even_family_upper_squeeze_numerator": coeffs(upper_num, D)},
    "bounds": {k: str(v) for k, v in [
        ("central_derivative_lower", deriv_lower), ("S1_coefficient", S1coef),
        ("S3_ratio_max", ratio_max), ("S3_coefficient", S3coef),
        ("K1", K1), ("K2", K2), ("K1_plus_K2", K1+K2), ("K", K),
        ("angular_upper", bound), ("threshold_margin", margin),
        ("generic_upper_D", generic_upper), ("repeated_upper_D", repeated_upper)]},
    "whole_checks": checks,
    "check_count": len(checks),
    "uniform_domain": "all real eight-vectors with mu1=mu3=mu5=0,mu2=1,0<D=mu4-1/8<=1/729; all multiplicities retained",
    "estimate": "C<16/(1-8sqrt(D))+390625 D^2<=237004387/10097379<47/2",
    "central_critical_root_bound": "abs(sigma)<40 D^(3/2)<1/480",
    "calibrating_leading_constant": 16,
    "limit16_prior_art": "8753 and independent REVIEW8806, stronger full balanced sphere",
    "sharp_family": "(z^2-1/8)^2[(z^2-1/8)^2-D/4]",
    "ordinary_bridges": [
        "real symmetric full spectral compression", "IVT/strict logarithmic derivative",
        "Taylor with signed original-root distance license",
        "full spectral masses grouped by eigenspace", "sharp-limit squeeze"],
    "unformalized": True, "independently_unreviewed": True,
    "proof_status": "ordinary author proof; not formally verified"}


def canonical(value):
    return json.dumps(value, sort_keys=True, indent=2)+"\n"


def unique_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError("duplicate expected field: "+key)
        out[key] = value
    return out


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=Path)
parser.add_argument("--expected", type=Path, default=Path(__file__).with_name("EXPECTED.json"))
args = parser.parse_args()
raw = canonical(record).encode()
saved = json.loads(args.expected.read_text(), object_pairs_hook=unique_object)
if canonical(saved) != raw.decode():
    raise ValueError("entire expected record/type mismatch")
if args.output:
    args.output.write_bytes(raw)
print(json.dumps({
    "actual_agent": "six-sendov-2", "role": "researcher",
    "engine": "SymPy dense QQ/literal paired moments", "sympy": s.__version__,
    "check_count": len(checks), "entire_expected_compared": True,
    "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}, sort_keys=True))
