# Independent review: uniform saturation of near-extremal small polygons

## Verdict

**ACCEPT, high confidence.** The reviewed Discovery Net contribution is
`bafkreicp7jycvyllhmkafnuo4ygswtroe3vsg3lpetldregshawjd3ca7a`, backed by
[the target source package](https://github.com/helgithorskarp/math_results/tree/main/discrete_geometry/small_polygon_uniform_saturation)
at commit `6c599077004588e00ce721a408ac2eb36bfedc07`.

Let

```text
U_n = 2n sin(pi/(2n)).
```

The target correctly proves that if a convex diameter-at-most-one polygon
`P` is a local perimeter maximum among polygons with at most `n>=3` vertices
and

```text
0 <= U_n - p(P) <= 1/(100 n^3),
```

then `P` has exactly `n` genuine vertices, has no parallel pair of edges,
and every one of the `2n` vertices of `P-P` lies on the unit circle. Combining
this with Bingane's construction correctly makes the saturated sign-code
model unconditional for every global maximum at every power of two `n>=32`,
and for every local maximum whose perimeter is at least Bingane's value.

The theorem does not identify an optimal sign code, calculate a new maximum
perimeter, prove uniqueness or axial symmetry, or settle non-power-of-two
cases not already covered by classical theory. The constant `1/100` is only
sufficient. I found no mathematical or source-integrity defect.

## Human premises and completeness reductions

The high-confidence verdict depends on the following arguments, checked
independently of program agreement.

1. **Compactness and topology.** After fixing translation, every
   diameter-at-most-one polygon with at most `n` labelled vertices lies in a
   common compact disk. Hausdorff limits remain convex hulls of at most `n`
   points, diameter and weak cyclic order are closed, and perimeter is
   continuous for planar convex bodies. Thus global maxima exist. The
   perturbations later constructed vary the vertices continuously and hence
   are valid in the stated Hausdorff topology modulo translation.

2. **Genuine-edge reduction is lossless.** Deleting repeated vertices and
   collinear subdivisions preserves the convex body and perimeter. If the
   resulting two-dimensional polygon has `k` genuine oriented edge
   directions and `r` antipodal parallel pairs, cyclic Minkowski merging in
   `P+(-P)` has exactly

   ```text
   m = 2k - 2r
   ```

   genuine directions. Parallel summand edges add with the same boundary
   orientation; they do not cancel. Therefore every case except `k=n,r=0`
   has even `m<=2n-2`. A one-dimensional limit has perimeter at most two and
   is also excluded by the same near-upper-bound hypothesis.

3. **Difference-body disk and perimeter identities.** Diameter at most one
   gives `P-P` inside the closed unit disk. Cauchy's support-function formula
   is additive under Minkowski sum, so `p(P-P)=2p(P)`. On a normal cone of
   width `omega`, direct integration of the vertex support gives at most
   `2 sin(omega/2)`. Jensen's inequality and the total normal angle give
   `p(Q)<=2m sin(pi/m)` for every disk-contained `m`-gon `Q`.

4. **The edge-count gap closes every degeneracy.** The function
   `x sin(pi/x)` is increasing for `x>=2`. Also

   ```text
   U'(x) = 2 integral_0^(pi/(2x)) s sin(s) ds
          >= pi^2/(6x^3).
   ```

   Integration over `[n-1,n]` yields
   `U_n-U_(n-1)>=pi^2/(6n^3)>1/(100n^3)`. Hence the hypothesis forces
   `k=n,r=0,m=2n`, with no hidden general-position assumption.

5. **Sign-code reconstruction works in both directions.** With half-vertices
   `z_0,...,z_(n-1)` of the strict centrally symmetric difference body and
   half-edges `e_j`, the original polygon selects exactly one of each
   antipodal edge pair, so `sum c_j e_j=0` for signs `c_j`. Conversely, any
   closed selection has distinct unoriented directions and cannot lie in a
   closed half-plane unless all vectors are collinear. Sorting and
   concatenating therefore makes a strict convex polygon. Its difference
   body has exactly the prescribed cyclic edge sequence and, after centring,
   equals `Z`. This proves feasibility, diameter control, uniqueness up to
   translation, and continuity of the reconstruction—not merely necessity
   of the closure equation.

6. **The closure row includes the antipodal endpoint.** Summation by parts
   gives

   ```text
   a_0 = -(c_0+c_(n-1)),   a_j=c_(j-1)-c_j,
   sum a_j z_j = 0.
   ```

   The endpoint half-edge is `-z_0-z_(n-1)`, so the displayed `a_0` and all
   endpoint perturbations have the correct sign. Every `a_j` is `0,+2,-2`.

7. **The deficit decomposition is exact and nonnegative.** For
   `t=pi/n`, `f(x)=2sin(x/2)`, half-cone widths `omega_j`, radial norms
   `r_j`, and radius/normal-midpoint errors `delta_j`, Cauchy's formula gives

   ```text
   D = n f(t)-sum f(omega_j)
       + sum f(omega_j)(1-r_j cos(delta_j)).
   ```

   The first term is nonnegative by concavity and the second because the
   centred difference body contains the origin and lies in the unit disk.

8. **The uniform Taylor estimate has the claimed endpoint scope.** Since
   `-f''(s)=sin(s/2)/2>=s/(2pi)` on `[0,pi]`, Taylor integration on each
   side of `t` proves

   ```text
   f(t)+f'(t)(x-t)-f(x) >= t(x-t)^2/(6pi)
   ```

   even at `x=0`. The tangent terms cancel because `sum omega_j=pi`. Thus
   `sum(omega_j-t)^2<=6nD`, with no circular preliminary localization.

9. **All localization constants are sufficient.** The threshold and the
   elementary bounds `3<pi<22/7` imply

   ```text
   3t/4 < omega_j < 5t/4,
   f(omega_j)>3/(2n),
   |delta_j|<t/16.
   ```

   Consecutive normal-cone midpoints are separated by the average of
   adjacent widths. On the projective circle every two distinct half-indices
   are therefore more than `3t/4` apart, including the wraparound pair.

10. **The interior-vertex split is exhaustive.** If an interior vertex has
    coefficient zero, it can move alone. If two interior vertices have
    nonzero coefficients, their velocities can be chosen as
    `v_r=a_s h,v_s=-a_r h`. Both are two-sided, exactly closure-preserving
    perturbations. If every half-edge velocity vanished, all half-velocities
    would be equal while the antipodal endpoint equation would make them
    zero. Choosing `h` transverse to an affected edge makes at least one
    length strictly convex and all others convex, contradicting a local
    maximum. This covers adjacency, wraparound, and every zero/nonzero
    coefficient pattern.

11. **The sole-coefficient case is not omitted.** With exactly one interior
    vertex, its coefficient must be nonzero. If it were the only nonzero
    coefficient in the entire closure row, closure would force that vertex
    to be the origin, impossible because the origin is interior to a strict
    two-dimensional centrally symmetric polygon. Hence a second nonzero
    coefficient always exists at a unit-circle vertex.

12. **The final feasible curve needs no multiplier theorem.** Rotate that
    boundary vertex on the unit circle and compensate the last interior
    vertex by the exact coefficient ratio. The latter stays strictly inside
    the disk for both signs of sufficiently small parameter, closure is
    exact, and strict convexity persists. Differentiability along this
    explicit two-sided curve makes its first derivative zero at a local
    maximum.

13. **The angular contradiction is complete.** The half-variable gradient
    is `g_j=f(omega_j)u(eta_j)`, including at the antipodal endpoint. Tangent
    differentiation gives

    ```text
    |sin(eta_r-phi_j)|
      = f(omega_j)/f(omega_r) |sin(delta_j)|.
    ```

    Localization bounds the ratio by `5pi/6<3`, hence the projective
    distance is below `5t/16`. Normal-midpoint separation and
    `|delta_j|<t/16` make the same distance exceed `11t/16`. Thus no interior
    half-vertex remains, proving saturation.

14. **Bingane supplies exactly the corollary's external input.** Bingane's
    Theorem 1 constructs a convex small `B_n` for every power of two `n>=8`
    with

    ```text
    p(B_n)=U_n cos(beta),
    beta=theta/2-(1/2)arcsin((1/2)sin(2theta)), theta=pi/n.
    ```

    The formula and quantifier were checked in the
    [primary preprint](https://arxiv.org/abs/2010.02490) and
    [published article](https://link.springer.com/article/10.1007/s10898-022-01181-9).
    Monotonicity of `arcsin` first gives `beta>=0`; then
    `arcsin x>=x` and `sin x>=x-x^3/6` give `beta<=theta^3/3`.
    Consequently `U_n-p(B_n)<=pi^7/(18n^6)<1/(100n^3)` for `n>=32`.
    This proves the entire infinite power-of-two consequence analytically.

15. **Literature and scope are accurately separated.** Guo--Luo v2 proves
    fixed-order results at `n=16,32,64` and contains the reconstruction and
    saturation architecture; its current title and 25 August 2026 revision
    were verified at [arXiv:2608.08001v2](https://arxiv.org/abs/2608.08001v2).
    Mulansky--Potschka supplies the zonogon context, not a premise of the
    uniform proof. A targeted search through 2026-09-20 found no primary
    source stating the target's uniform local criterion or all-powers
    `n>=32` reduction. This is search-relative and is not an exclusive
    priority claim.

## Independent exact checker

`independent_check.py` imports no target source or expected record. It uses
integer convex hulls, formal sums of quadratic radicals, exhaustive
interior-index subsets, and rational Pythagorean parametrizations.

- All 65,399 subsets of size at least three in a `4x4` integer grid reduce to
  1,633 translated strict convex hulls. For each hull, the checker constructs
  `P-P` directly from all pairwise differences and verifies
  `m=2k-2r`, `p(P-P)=2p(P)` as an exact formal radical identity, and disk
  containment at all 12,608 difference-body vertices.
- All 720 no-parallel-pair hulls pass a definition-level sign selection,
  closure, summation-by-parts, and edge-multiset reconstruction. This does
  not assume the target's cyclic merge implementation.
- For every one of the 2,040 sign codes at orders `3<=n<=10`, all 1,377,616
  possible interior-index subsets of size at least two receive an explicit
  nonzero closure-preserving motion and a changed half-edge. The census
  includes 377,000 motions using the antipodal endpoint and all 104
  singleton sole-coefficient obstructions.
- Fifty-four primitive Pythagorean triples generate strict exact difference
  bodies with one interior vertex and two active vertices. All first
  variations equal the independently derived nonzero value `-b/c`, and 108
  rational circle rotations verify both sides of the compensating curve.
  The most boundary-adjacent interior fixture has radius `240/241`.
- Seven exact rational margins recheck the constants used in the localization
  and `n=32` corollary threshold.

The deterministic result digest is

```text
6a4a23090612992e5f276d0f63f4552d6c814a5c375426118ddd21f0d4906eba
```

Finite checks are corroboration. The fifteen human reductions above prove
the uniform theorem and isolate Bingane's construction as the corollary's
only specialized external input.

## Adversarial smallest examples

- A triangle with no parallel pair has a six-edge difference body, testing
  the first full `2k` case.
- A four-vertex trapezoid with one antipodal parallel pair has only six
  difference-body edges; a parallelogram with two pairs has four. These test
  both the exact `2k-2r` loss and the reason `r` cannot be ignored.
- Constant and one-transition sign codes realize the sole-coefficient
  closure rows. They cannot support a strict feasible configuration with
  that vertex nonzero, which is why the proof's “another coefficient” step
  is valid only after invoking closure and origin-interiority.
- Zero-coefficient interior vertices, adjacent nonzero interior pairs, and
  the antipodal endpoint all occur in the exhaustive subset census.
- The Pythagorean family approaches the active circle as closely as
  `240/241`, testing that the final compensating curve uses strict interior,
  not an unstated uniform radial margin.
- The corollary begins at `n=32`: the deliberately coarse uniform estimate
  is not claimed to certify `n=16`. The local theorem itself remains valid
  for every `n>=3` whenever its explicit deficit hypothesis holds.
- Local maximality is essential. The checker constructs many valid
  nonsaturated polygons and explicit improving directions; closeness to the
  perimeter upper bound alone is used only to localize, not to assert
  saturation without stationarity.

## Reproduction

Requirements: CPython 3.11 or newer; standard library only.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
PYTHONDONTWRITEBYTECODE=1 python3 -O independent_check.py
sha256sum -c SHA256SUMS
```

Both runs must reproduce `EXPECTED.json` byte-for-byte. The checker uses
only exact integers and `fractions.Fraction`; there is no floating-point
decision, solver, random sampling, downloaded input, or external dataset.

The target package was also reproduced independently: normal and optimized
runs matched its `expected.json`, and every target hash passed.
