# Rational quadrature certificate

Actual author: **six-reviewer-3**, independent mathematical reviewer.
This documents the scalar certificate and its independently proved
quadrature remainder. The geometry and its continuum reduction are in
[REVIEW.md](REVIEW.md). The program imports none of the original researcher's
code and reads no numerical proof input.

## Square roots and angle representation

For rational \(0\le x\le4\), `root(x)` brackets \(\sqrt{x}\) on the
\(10^{-18}\) grid by integer bisection. The starting integers are zero
and \(2\cdot10^{18}\); 64 fixed iterations suffice since the starting
width is less than \(2^{61}\). An exact square returns its exact root;
otherwise the integer interval must finish with width one and the exact
squared endpoint inequalities are verified. This never uses a float.

On every production argument,
\[
 \arccos x=2\int_0^{\sqrt{(1-x)/(1+x)}}\frac{dt}{1+t^2}.
\]
The positive root argument is checked to be at most four and its square
root at most two. The function is evaluated at both outward root bounds;
the integrand is positive, so the lower endpoint supplies a lower bound
and the upper endpoint an upper bound. For an interval in \(x\), inverse
cosine monotonicity reverses the endpoints. The special arguments \(1\)
and \(-1\) give zero and \(4\int_0^1dt/(1+t^2)=\pi\), respectively.
The implementation deliberately makes no claim to accept every valid
inverse-cosine argument near \(-1\) with the fixed root domain: all actual
arguments in this certificate satisfy the inspected bounds, and a domain
failure rejects the run.

## Self-contained Simpson error bound

For \(f(t)=1/(1+t^2)\),
\[
 f^{(4)}(t)=\frac{24(1-10t^2+5t^4)}{(1+t^2)^5},\qquad
 |f^{(4)}(t)|\le24\quad(t\ge0).
\]
One direct proof of the inequality is
\(f(t)=\tfrac12((1+it)^{-1}+(1-it)^{-1})\); four differentiations give
\(12((1+it)^{-5}+(1-it)^{-5})\), with modulus at most
\(24/(1+t^2)^{5/2}\le24\). This complex identity proves an elementary
real bound; no complex arithmetic is used by the program.

For a single Simpson pair on \([0,2]\), let
\[
 \mathcal E(g)=\int_0^2g(t)dt-\frac{g(0)+4g(1)+g(2)}3.
\]
This annihilates polynomials through degree three. Taylor's integral
remainder at zero and interchange of the continuous integrals yield
\(\mathcal E(g)=\int_0^2K(u)g^{(4)}(u)du\), where applying the functional
to \((t-u)_+^3/6\) gives
\[
 K(u)=\begin{cases}
 u^3(3u-4)/72,&0\le u\le1,\\
 (2-u)^3(2-3u)/72,&1\le u\le2.
 \end{cases}
\]
Both pieces are nonpositive and their negative integrals sum to \(1/90\).
For a pair with grid step \(h\), rescaling therefore bounds its error
by \(\sup|g^{(4)}|h^5/90\).
With an even \(n\) panels on \([0,z]\), summing \(n/2\) such pairs gives
\[
 |\text{integral}-\text{composite Simpson sum}|
 \le\frac{\sup|g^{(4)}|z^5}{180n^4}.
\]
The certificate fixes **\(n=256\)**, so for this integrand the exact
error bound is \(24z^5/(180\cdot256^4)\). The proof works at every outward
rational endpoint, not merely at the true irrational angle argument.

Every rational node value is separately rounded outward on a \(10^{-24}\)
grid before accumulation. All Simpson weights are positive. The exact
rounded weighted sum therefore brackets the exact Simpson sum; adding
the proved error gives a rigorous integral enclosure. Flooring each node
prevents denominator growth without an unaccounted roundoff error. The
nonnegative lower bound may also be replaced by zero. All operations are
integer/Fraction operations.

## From endpoint intervals to the entire theorem

The direct support-foot formula in REVIEW.md reconstructs the perimeter
using two inverse cosines and a positive square-root product. Every domain
condition and sign needed for interval multiplication is checked. The
program proves the cap-domain conditions uniformly through endpoint
values of a concave quadratic and an increasing quadratic. The written
derivatives prove \(J_e(c)\) decreasing. Thus each literal closed cell
\([a,b]\) uses the lower enclosure of \(J_e(b)\) minus the upper enclosure
of \(6\arccos(a-e)\); no derivative of their difference is presumed.

The original band uses five equal cells of width \(1/125\); the strengthened
band uses forty equal cells of width \(1/1000\). Both start at \(14/25\)
and end at \(3/5\). Contiguity and strict positivity are enforced by the
literal endpoint construction and explicit guards. After all rigorous
enclosures, results are rounded outward on the exact \(10^{-6}\) grid.
All 45 complete records are in EXPECTED.json. For the original cover the
minimum gap is \(21111/500000>1/25\); for the stronger cover it is
\(9031/500000>1/100\).

The checker also verifies the wider-band degree bound
\(187/475<1/2\) and the negative perimeter-route control at tolerance
\(1/40\). That negative interval is not a counterexample to the geometric
theorem. Controls check exact squares, the zero angle, a basic pi enclosure,
Simpson exactness on four monomials, and the quartic error corresponding
to the kernel mass. Seven deliberately invalid conditions are rejected,
including a false gap, invalid hemisphere band and failed wider-band cover.

## Reproduction and trust boundary

Use Python 3.11 or later, standard library only:
```bash
python3 -B round-two/six-reviewer-3/hexagon-capacity-audit/audit.py
python3 -B round-two/six-reviewer-3/hexagon-capacity-audit/replay.py
```
The latter compares complete normal/optimized evidence under serial fixed
180-second guards. Observed CPython 3.11.2 results are in VALIDATION.json;
EXPECTED.json is comparison output, not an input needed by the proof code.
Source hashes are in SHA256SUMS. INPUTS.json records target provenance only.
No floating computation, solver, external certificate, coordinate data,
private ledger or large omitted artifact is part of the mathematical proof.
The remaining trust is the written analysis/geometry and CPython's exact
arithmetic implementation; neither is represented as formally verified.
