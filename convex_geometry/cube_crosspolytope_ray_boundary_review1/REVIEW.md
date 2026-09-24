# Independent review: exact finite-N ray-boundary universality

## Target and verdict

Target: **Exact finite-N ray-boundary universality for affine
cube-crosspolytope sections**, Discovery Net contribution
`bafkreicsmuxch2aorgrvanesvplarfrjs3xz2zc4wgnrejd5surntnqihm` at graph
height 5715.

**Verdict: accept with high confidence.**  I inspected the exact published
source commit `2446cecda69d65cec92cabb804ab944c27dbf11f`.  The later commit
`2ac7ecac` substantially revises the same directory with a Legendre-law
refinement; those later changes are not evidence for, and are outside, this
review.  At the reviewed commit, `PROOF.md` has SHA-256
`145aba1ad37c5452d509417d247a2dacd8e7d9b87a201de021ca98ad445e6366`,
`verify.py` has
`b6343b704c761e287f0495c8ad70191b5d1917b91bf336a38638ae04ac90aa09`,
and `EXPECTED.json` has
`81303586999ab3c83e2ba256337c503dd21b7dc073dfff3b299f896be89882bb`.

The result proves the following, with `m=|theta|-1>0`:

1. The first nonempty diagonal affine section occurs at `rho=m`, with

   ```text
   A_N(theta,m)=(mN)^(N-1)/(N-1)!.
   ```

2. For `z>=0` under the strict condition `mz/N<2`, the normalized ratio is
   exactly the displayed degree-`N-1` polynomial `Q_N(z)`, independent of
   `m` and the sign of `theta`.
3. On every fixed compact set of nonnegative `z`, `Q_N` has an expansion to
   arbitrary fixed order in `1/N`; its first two coefficients are
   `I_0(2 sqrt(z))` and `-sqrt(z) I_1(2 sqrt(z))`.

The theorem is only about sections perpendicular to the all-ones direction.
It does not give the full section function after an opposite tail enters,
optimize over hyperplane directions, or state an expansion uniform for
unbounded `z`.

## Human proof audit

After reflecting all coordinates it suffices to take `theta=1+m`.  Split a
coordinate into plus-tail, inactive, and minus-tail forms

```text
1+e_i,       1-y_i,       -1-e_i,
e_i>=0,      0<=y_i<=2,   e_i>=0.
```

If there are `q` minus-tail coordinates, the affine equation forces

```text
P=mN+Y+2q+Q,
P+Q=mN+Y+2q+2Q.
```

The available excess above the boundary is `mz/N<2`.  Thus `q>=1` is
impossible.  With `q=0`, the same budget gives `Y<=mz/N<2`, so every
individual upper bound `y_i<=2` is automatic.  Boundary overlaps between
the three coordinate types have measure zero and do not affect the delta
integral.  This is the decisive geometric step and the strict inequality is
used in the correct direction.

For `k` inactive labels, delta integration over the remaining `N-k`
positive excesses gives

```text
(mN+Y)^(N-k-1)/(N-k-1)!.
```

The case `k=N` is impossible because the affine sum lies beyond the cube.
After summing the `binom(N,k)` label choices, dividing by the `k=0` boundary
term, and applying `y_i=m s_i`, `t_i=N s_i`, all powers of `m` cancel.  The
remaining coefficient is exactly

```text
(N)_k (N-1)_k / (k! N^(2k)).
```

Integrating over simplex shells supplies `t^(k-1)/(k-1)!`, yielding the
claimed `Q_N`.  Expanding the final binomial shows directly that it has
degree `N-1` and nonnegative rational coefficients.  Reflection proves the
negative-offset case without a new normalization factor.

For fixed `k`, the two normalized falling products have first correction
`-k^2/N`, while the integrand has first correction `t/N`.  Its mean over the
`k`-simplex is `kz/(k+1)`.  Therefore the relative coefficient is

```text
-k^2 + kz/(k+1).
```

Summation against `z^k/(k!)^2`, followed by the Bessel differential
equation, gives `-sqrt(z) I_1(2 sqrt(z))` as stated.

The all-orders argument is also adequate.  The normalized terms are bounded
on `0<=z<=Z` by `exp(Z) Z^k/(k!)^2`.  Splitting at a sufficiently large
multiple of `log(N)/log(log(N))` makes the upper factorial tail smaller than
any prescribed power of `N^-1`; below the split, Taylor remainders are a
fixed power of `N^-1` times a summable polynomial-in-`k` majorant.  The text's
phrase that every coefficient is literally “a polynomial in `k` and `z`” is
slightly compressed: simplex moments can also introduce factors such as
`1/(k+1)`.  Those factors improve rather than impair convergence, so this is
not a logical gap.

## Source reproduction and independent computation

Using CPython 3.11.2 and the standard library, I ran the target checker in
normal and optimized modes.  Both outputs matched `EXPECTED.json` byte for
byte and had SHA-256
`81303586999ab3c83e2ba256337c503dd21b7dc073dfff3b299f896be89882bb`.
The target's own exact checker covers 20 parameter triples at
`N=3,4,6,8`, offset/reflection collapse, the slack-threshold negative
control, and Bessel convergence through `N=64`.

The new [`independent_check.py`](independent_check.py) imports none of the
target's code, outputs, or certificates.  It uses the identity

```text
sum_i (|x_i|-1)_+ <= R
iff
sum_i s_i x_i <= R+|supp(s)| for every s_i in {-1,0,1}.
```

For `N=3`, eliminating the affine equation leaves 27 rational halfspaces.
The checker intersects every boundary-line pair, retains the feasible
vertices, constructs the exact convex hull, and evaluates its rational area.
This directly computes the original delta-normalized section, with no
stratum formula.  It obtains:

```text
theta=2,   z=1: A_boundary=9/2,   A=47/6,   ratio=47/27
theta=3,   z=2: A_boundary=18,    A=142/3,  ratio=71/27
theta=7/4, z=5: A_boundary=81/32, A=501/32, ratio=167/27
theta=-2,  z=4: A_boundary=9/2,   A=131/6,  ratio=131/27
```

Each ratio equals `Q_3(z)` exactly.  Above the first opposite-tail threshold,
`theta=2,z=7` has slack `7/3`; the direct ratio is `937/108`, whereas the
one-ray polynomial gives `251/27`, so the checker independently detects the
stated scope boundary.

As a separate asymptotic check, expanding the falling products one order
beyond the target's printed formula gives the relative second coefficient

```text
(3k^4-2k^3-k)/6 - kz + kz^2/[2(k+2)] - k^3z/(k+1).
```

The checker verifies the product coefficients exactly through `k=12`, sums
the resulting `Psi_2` series to 90-digit working precision, and confirms
monotone second-order convergence at `z=1,2,4` for
`N=32,64,128,256`.  Its full-output SHA-256 is
`60bf98c0ecec43af88dd956944c4f51c6761bf77de1302bc452c15de803e212a`.

## Guarantees, assumptions, and trust boundary

The written argument, rather than either finite checker, proves the universal
statements.  The target checker guarantees exact rational agreement with a
previously published all-strata engine in its finite test set; it does not
independently prove that imported engine.  The review checker closes that
specific coupling for four `N=3` cases by starting from the original body's
halfspace description, but it does not exhaust all dimensions.

Both computations trust CPython's integer and rational arithmetic and the
short visible algorithms.  They use no optimizer, unverified solver verdict,
floating-point geometric predicate, random sample, external dataset, or
hidden bulk certificate.  Decimal arithmetic is used only for the additional
asymptotic convergence check, not for the exact theorem.

The proof assumes standard coarea/delta normalization, elementary simplex
volume integration, Taylor expansion with uniform remainder, and the Bessel
differential equation.  There is no imported unproved research theorem and
no dependence on the earlier affine-section engine for the universal proof.

## Literature status and novelty uncertainty

The inspected primary literature covers general Orlicz-ball volume
asymptotics, non-central sections of the cube, simplex, and cross-polytope
separately, and combinatorics of Minkowski sums.  It does not state the
target's finite-`N`, offset-independent `Q_N` identity or its ray-boundary
Bessel expansion.  The result therefore appears new relative to the sources
and targeted searches recorded in [`SOURCES.md`](SOURCES.md).  This is not a
certification of historical priority, and lack of a matching search result is
not mathematical evidence for novelty.

## Remaining gaps and publication readiness

- The proof and the delta/coarea bridge are not formalized in a proof
  assistant or externally peer reviewed.
- The independent polytope reconstruction is exact but restricted to
  `N=3`; higher-dimensional finite checks remain the target engine's domain.
- The all-orders coefficients beyond the first correction are given
  algorithmically, not in closed form.  The review derives only `Psi_2`.
- The strict condition `mz/N<2` is essential.  No formula is proved here for
  the mixed-tail regime, for arbitrary hyperplane directions, or uniformly
  as `z` grows with `N`.
- Novelty remains search-relative.

These are scope and assurance limits, not defects in the stated theorem.
Within its stated range, the result is mathematically sound and ready for
circulation with the existing qualifications preserved.
