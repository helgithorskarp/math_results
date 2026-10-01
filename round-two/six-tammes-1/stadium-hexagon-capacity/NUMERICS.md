# Exact enclosure contract

Actual author: six-tammes-1, researcher. Every operation in the two checkers
uses CPython arbitrary integers and `fractions.Fraction`. No hardware floating
rounding, numerical library, solver or external data is used.

The target is the five endpoint comparisons in PROOF.md (10)--(11). Analytic
monotonicity reduces each complete parameter cell to its two declared endpoints.
The six endpoints are exactly `i/125`, `i=70,...,75`. Each right endpoint
evaluates `J`, each left endpoint evaluates the six-edge budget. The fixed
partition covers `[14/25,3/5]` with no gaps. Square-root and inverse-trigonometric
arguments and positive interval products are checked before use.

## Primary representation

For a nonnegative rational `x=p/q`, with `D=2^80`, take
`m=isqrt(floor(p D^2/q))`. Then `m/D<=sqrt(x)<=(m+1)/D`.
If equality is exact, both endpoints are `m/D`. The program explicitly verifies
the squared endpoint inequalities. These are rational bounds, not 80-bit
floating numbers.

For `0<=u<=1`,

    acos(u)=2 atan(sqrt((1-u)/(1+u))).

The map on the right is decreasing in `u`, so an interval `[a,b]` is evaluated
at its reversed endpoints with outward square-root bounds. For positive `x`,
the fixed `N=32` alternating arctangent sum has bounds

    sum(j=0..N-1) (-1)^j x^(2j+1)/(2j+1)
      <=atan(x)
      <=that sum+x^(2N+1)/(2N+1).

The formula follows by integrating the finite geometric identity for
`1/(1+t^2)`: the remainder has positive sign for even `N` and is at most
the displayed next term. The prototype restricts `x<=1`; all production
arguments are much smaller. The endpoint evaluations here are well separated
from the inverse-function branch boundaries. `acos(1)=0` and rejection of
an argument greater than one are explicit controls.

## Separate representation

`audit.py` imports no primary code. It bisects rational square-root brackets
for exactly 96 steps, terminating early only on an exact square. It evaluates

    acos(x)=pi/2-asin(x).

For `0<=x<=3/4`, use 64 terms of the positive arcsine series

    asin(x)=sum(n>=0) a_n x^(2n+1),
    a_0=1, a_(n+1)/a_n=(2n+1)^2/[2(n+1)(2n+3)].

This is the integrated binomial series for `(1-x^2)^(-1/2)`.
The coefficients are positive and at most one, so after `N=64` terms the
omitted positive tail is at most `x^(2N+1)/(1-x^2)`. Every production angle
input fits the declared `3/4` domain. The exact zero-angle endpoint is handled
separately. Monotonicity of the arcsine evaluates each interval at its endpoints.

The `pi` bracket comes from

    pi=16 atan(1/5)-4 atan(1/239),

using fixed20-term even alternating sums. To check the identity without a
decimal `pi` input, put `A=atan(1/5)`, `B=atan(1/239)`.
Then `tan(2A)=5/12`, `tan(4A)=120/119`, and `tan(4A-B)=1` exactly.
Also `0<4A-B<pi/2`: `A>B>0` and `2A<pi/4`. Therefore `4A-B=pi/4`.
The audit checks the rational tangent identity and the elementary bounds
`3<pi_lower<pi_upper<22/7`. This is a rigorous bracket, not a decimal constant.

## Output and controls

The final component bounds are rounded outward to rational multiples of
`10^-6`; lower bounds are floored and upper bounds ceiled with integer/Fraction
arithmetic. Differences use the lower stadium bound minus the upper edge bound.
Both implementations independently establish all five gaps greater than `1/25`,
then their full rounded endpoint/cell records agree entry by entry.

Both also establish a negative comparison at `c=14/25`, tolerance `1/40`.
It explains a limit of this scalar certificate and is not treated as an actual
packing counterexample. A perfect-square root and zero-angle case are checked;
the primary checker rejects a real argument outside the inverse-function domain.
No Python `assert` supplies a mathematical check, so optimized runs retain them.

`EXPECTED.json` and `AUDIT_EXPECTED.json` are compact output receipts, not proof
inputs. The exact source, remainder arguments, finite partition and geometric
interpretation are all needed for the theorem. Two implementations by the
author sharing Python/Fraction are not independent researcher review.
