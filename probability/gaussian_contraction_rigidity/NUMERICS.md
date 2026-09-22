# Finite-check contract

All source arithmetic uses arbitrary-precision integers and
fractions.Fraction. The theorem in PROOF.md is analytic and does not
depend on these checks.

The fixtures are four explicitly listed discrete input/output
configurations in dimensions one and two. Exact checks validate probability
normalization, support radius, and every pairwise contraction inequality.
The first fixture is a translated reflection; the others are an absolute
value fold, clipping of an exceptional atom, and a coordinate contraction
of a square. No enumeration of all contractions is claimed.

For each fixture, five rational unit-circle points parameterize (5).
The norm identity and the velocity identity divided by pi are checked
for every ordered point pair. Thus the trigonometric constants are
checked algebraically, without evaluating sine or pi numerically.

Double centering is checked entry by entry against directly computed
centered inner products. These fixtures have diagonal cross-covariance
and covariance, allowing exact optimal orthogonal alignment and an exact
covariance lower bound without a numerical eigensolver. The trace identity,
Gram norm estimate, and final rigid-motion estimate are all checked.

## Independent finite entropy formula

For an integer $m\ge2$, variance one, and a discrete law in dimension $n$,
completing the square gives

$$
\int f^m=(2\pi)^{-n(m-1)/2}m^{-n/2}
\mathbb E\exp\left(-\frac1{2m}\sum_{i<j}|X_i-X_j|^2\right).
$$

The expectation is enumerated over all ordered replica tuples, with their
exact product probabilities, for $m=2,3,4$. The common Gaussian prefactor
cancels in the entropy difference. This calculation does not use the
lifted dissipation identity, so it checks the bound through a different
finite formula. It remains an author check, not an independent reviewer.

## Rational enclosures

The exact real obligations are to enclose each replica exponential, its
positive weighted sum, the logarithm of the output/input ratio, and the
explicit lower bound $c_\alpha D$ in (1)--(2) with $s=1$.

For $0\le x\le1/2$, sum the exponential series through degree 32.
Its omitted tail is at most its first omitted term divided by
$1-x/34$, since all subsequent term ratios are at most $x/34$.
Halving and squaring reduce other positive arguments to this interval;
reciprocal intervals treat negative arguments. Exponential endpoints
are rounded outward to multiples of $2^{-160}$ using integer floor
and ceiling. This bounds denominator growth without floating point.

For $1\le x\le2$, use $z=(x-1)/(x+1)$ and the first 80 terms of
$\log x=2\sum_{j\ge0}z^{2j+1}/(2j+1)$.
The remaining tail is at most
$2z^{161}/(161(1-z^2))$. Scaling by powers of two covers all positive
arguments; the sign of the scaling exponent determines interval
orientation. Logarithm is evaluated at the ratio interval endpoints.
Invalid nonpositive arguments are rejected. Precision and term counts
are fixed in advance, with no search for a desired sign.

For each nonisometric fixture the lower entropy-gap endpoint must exceed
the upper $c_\alpha D$ endpoint. The reflection fixture is handled by
exact equality of the replica sums, giving a zero gap. Displayed intervals
in EXPECTED.json are rounded outward to a $10^{-12}$ grid; comparisons
use the full rational bounds before display rounding.

The exact input cases, interval algorithms, and analytic remainder
estimates define coverage. There is no unrecorded subdivision, sampling,
or numerical quadrature. Normal and optimized Python runs must produce
identical bytes. Interpreter/integer/Fraction semantics, the source,
and ordinary mathematical reasoning about the remainders form the
computational trust boundary.
