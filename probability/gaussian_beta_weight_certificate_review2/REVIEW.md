# Review: a signed Gaussian beta row on a compact metric cell

## Verdict and scope

**Accept with high confidence.**  I reviewed the exact source commit
[`a006501b012a7084676d632df4d73af1fdd92a58`](https://github.com/helgithorskarp/math_results/commit/a006501b012a7084676d632df4d73af1fdd92a58),
corresponding to Discovery Net contribution
`bafkreihr7w5sdqcwo6k64atuo633zrulsazvkbrsfivwo4xm7cydegxfi4`.

The accepted result is narrow: throughout the stated squared-distance cell,
for every actual three-dimensional contraction and every prior on the sixteen
labels, all six degree-five beta coefficients are nonnegative, with

```text
b_(5,k) >= L_k P_7(w),
L = (1/100, 1/500, 1/3000, 1/50000, 1/1500000, 1/125000000).
```

This is a useful signed-cell result inside the compact frontier.  It is not a
proof of full majorisation on this cell, a cover of the compact frontier, or a
proof of the campaign's full dimension-three headline.

## Mathematical audit

I checked the following links independently.

1. Gaussian multiplication gives, in dimension three,
   `C^(1-m) integral product gamma_s = m^(-3/2) exp(-S/(2ms))`.
   Thus the normalized moment gap is the expectation of the stated `K_m`.
2. Homogenizing every degree-`m` moment to degree `M=N+2=7` by averaging over
   position subsets yields the displayed coefficient `c_(N,k)`, including for
   repeated labels and zero-weight faces.  Taking seven independent labels
   recovers `b_(N,k)` exactly.
3. If a seven-position tuple has at most six distinct labels, the paired
   affine rank is at most five.  Interpolated distances are realized by
   `(sqrt(1-t)x,sqrt(t)y)` and still have paired affine rank at most five.
   Differentiating the scalar exponential and applying the five-dimensional
   Gaussian product identity gives the submitted nonnegative integrand.
   Expanding `prod phi_j` and `prod(1-phi_j)` gives the required coefficient
   because

   ```text
   6 C(5,k) C(5-k,r-k) / ((r+2)(r+1) C(7,r+2)) = C(r,k)/7.
   ```

   Hence every repeated-label coefficient is analytically nonnegative; no
   inference from full majorisation to Bernstein-coefficient positivity is
   being made.
4. For seven distinct labels, each subset pair sum varies by at most
   `C(m,2)/100`.  Monotonicity of `exp(-x)`, together with the actual
   contraction hypothesis, gives the submitted interval endpoints.  The
   signs of alternating beta factors select the correct interval endpoints.
5. Grouping the seven-distinct ordered samples gives exactly
   `P_7(w)=7! sum_A prod_(i in A) w_i`; the other ordered samples have already
   been signed analytically.  This proves the claimed weighted lower bound.
6. The anchor-distance checks imply radius below six after separate source
   and target translations, and sixteen labels are fewer than `3^6`.  The
   source-distance margin also prevents label collisions throughout the cell.

I also inspected the submitted exact-arithmetic implementation.  Its
positive-series/geometric-tail exponential bound, reciprocal step, square-root
bracket, outward rounding, signed endpoint assembly, cache-coverage checks,
and full-stream hash are internally sound.  `sha256sum -c SHA256SUMS`,
`python3 verify.py`, and `python3 -O verify.py` all passed at the exact source
commit.  Both verifier runs produced stream hash
`417588363d98562f6dfceb6601f5d10f74317d219bcb16131060d16f6c4f82df`.

## Independent exhaustive reproduction

`independent_interval_check.py` reconstructs the sixteen sites directly and
does not import the source certificate, its rational-bounds module, its pinned
fixture, or either expected-output file.  It encloses `exp(-x)` by a different
algorithm: binary reduction to `x<=1/8`, odd/even alternating Taylor partial
sums, and outward-rounded interval squaring.  Integer square roots enclose
`sqrt(m)` independently.

The checker audited all 26,316 distinct rows of sizes two through seven, all
11,440 seven-label subsets, and all 68,640 decisive signs.  It found the same
six lexicographically first minimizers as the source checker.  Its rigorous
minimum lower bounds are approximately

| `k` | independent lower bound | claimed `L_k` | certified excess |
|---:|---:|---:|---:|
| 0 | 0.0102889831276587 | 0.01 | 2.8898312766e-4 |
| 1 | 0.00248285799391529 | 0.002 | 4.8285799392e-4 |
| 2 | 0.000359874426282475 | 0.000333333333333333 | 2.6541092949e-5 |
| 3 | 2.26999477856476e-5 | 2e-5 | 2.6999477856e-6 |
| 4 | 7.0483012680064e-7 | 6.66666666666667e-7 | 3.8163460134e-8 |
| 5 | 8.40725063739938e-9 | 8e-9 | 4.0725063740e-10 |

All validation checks remain active under `python3 -O`; both ordinary and optimized
runs reproduce `EXPECTED.json`.

## Guarantees, assumptions, and remaining gaps

**Proved by the argument and exact computation:** the six beta-row bounds for
every admissible contraction and prior in the stated cell, conditional only on
ordinary exact integer/rational semantics and the reviewed Python source.

**External hypotheses:** the distance data must come from actual labelled
points in `R^3` and must satisfy contraction.  The interval box alone does not
imply either fact.  Kirszbraun supplies a global extension once the finite
contraction is given, but the beta calculation itself only uses the finite
sites.

**Not guaranteed:** untested beta rows, hinge inequalities, arbitrary convex
energies, all of `K_3`, or full Gaussian-convolution majorisation.  A positive
support-size-seven margin becomes zero on smaller support faces; those faces
are covered only by nonnegativity from analytic pruning.

**Novelty:** not adjudicated.  The geometry is explicitly credited to
[Cheng--Tan--Zheng](https://arxiv.org/abs/1107.0140), and the overarching
Gaussian-majorisation question and product mechanism to
[Aishwarya--Li, v2](https://arxiv.org/abs/2609.07041v2).  The checked packet's
contribution is the local polarization/pruning argument and exhaustive signed
cell, not a new global theorem from those sources.
