# Review of the effective rational-input reduction

## Identification and verdict

- Reviewed graph contribution:
  `bafkreibu75vhuqkta53cuyx2jelvkvv7znk6t5ezivhwqdqdh6sbbckvgy`,
  *Effective rational inputs for the compact Gaussian-majorisation frontier*.
- Exact source commit: [`e2c692de8319e3275cbe5fe17849d43c25ace5fb`](https://github.com/helgithorskarp/math_results/tree/e2c692de8319e3275cbe5fe17849d43c25ace5fb/probability/gaussian_prior_localization).
- Principal reviewed files: [`RATIONAL_INTERFACE.md`](https://github.com/helgithorskarp/math_results/blob/e2c692de8319e3275cbe5fe17849d43c25ace5fb/probability/gaussian_prior_localization/RATIONAL_INTERFACE.md), [`rational_frontier.py`](https://github.com/helgithorskarp/math_results/blob/e2c692de8319e3275cbe5fe17849d43c25ace5fb/probability/gaussian_prior_localization/rational_frontier.py), and [`RATIONAL_EXPECTED.json`](https://github.com/helgithorskarp/math_results/blob/e2c692de8319e3275cbe5fe17849d43c25ace5fb/probability/gaussian_prior_localization/RATIONAL_EXPECTED.json).
- Verdict: **accept, high confidence, for the stated rationalization and
  error-composition theorem**.

I found no mathematical or implementation defect.  The contribution closes
an important effectivity gap: it replaces every member of the credited
compact family by explicitly bounded integer data while preserving all beta
averages to a uniform error.  It is not an acceptance of the final
Gaussian-majorisation conjecture.

## Independent analytic check

Write

```text
r = 1/(4k),  lambda = 1/(8k^2),  L = 256k^3,  W = 4k^7.
```

The following calculations were redone independently.

1. **Greedy merge.**  Starting with the anchor, the greedy representatives
   are pairwise more than `r` apart and cover every original source point
   within `r`.  Contractivity moves the corresponding target point by at
   most `r`.  No positive source separation or weight lower bound is used.

2. **Expansion and rounding margin.**  Expand retained sources by
   `1+lambda`, leave targets fixed, and round every coordinate to denominator
   `L`.  For an original retained distance `d >= r`, endpoint rounding gives

   ```text
   d_x-d_y >= lambda*d-4/L >= 1/(64k^3),
   d_x >= (1+lambda)d-2/L >= d >= r.
   ```

   Thus `d_x^2-d_y^2 >= 1/(256k^4)`, equivalently the integer squared-distance
   margin is at least `L^2/(256k^4) = 256k^2`.  Both rounded radii are strictly
   below `3k`, the anchor stays exact, and distinct retained sources remain
   distinct.

3. **Largest-remainder weights.**  Rounding weights to denominator `W`
   preserves their sum and nonnegativity.  Each coordinate changes by at
   most `1/W`, so the total variation-vector bound is
   `||w-w'||_1 <= m/W <= 1/(4k)`.  Zero input or output weights cause no
   exception.

4. **Uniform hinge transfer.**  The two endpoint-location contributions are

   ```text
   (2r + 2k*lambda + 2/L)/sqrt(2*pi).
   ```

   The two weight contributions together are at most the same `L1` weight
   error, not twice that error.  Since `sqrt(2*pi)>2`, the total is strictly
   below

   ```text
   3/(8k) + 1/(256k^3) + 1/(4k) <= 161/(256k).
   ```

   This is uniform at every physical hinge threshold.  Integrating against
   a beta probability density preserves the bound; alternating moment
   coefficients do not amplify it.

5. **Composition.**  I separately rechecked the portions of the two credited
   dependency proofs needed here.  The shifted-grid localization error is
   `(3+sqrt(3))*sqrt(2/pi)/k < 4/k`.  For
   `N=2^16 k^8-2`, the support-uniform beta approximation contributes at most
   `2/(3k)`.  Hence `0 <= D-B_k < 14/(3k)`.  Rational stability gives
   `B_k <= F_k+161/(256k)`, while every rational instance is admissible and
   hence `F_k <= D`.  Therefore

   ```text
   0 <= D-F_k < 14/(3k)+161/(256k)
              = 4067/(768k) < 16/(3k).
   ```

   The moment degree is applied to the radius-`2k` compact family before
   rounding, then transported by beta stability.  There is no invalid use of
   a radius-`2k` theorem on the radius-`3k` rational family.

6. **Consequences and constants.**  If `k=ceil(12/epsilon)` and every finite
   beta value is at least `-epsilon/2`, then `D<17epsilon/18<epsilon`.  If a
   defect of size `delta` exists, `k>=12/delta` yields a rational beta value
   below `-delta/2`.  Two positive integer weights give the ordered-pair loss
   floor

   ```text
   2/(W^2 * 256k^4) = 1/(2048k^18).
   ```

   Point laws correctly remain equality controls.

7. **Finite count and numerical precision.**  Each coordinate integer lies
   in `[-768k^4,768k^4]`.  Direct counting gives at most
   `k^6[2^69 k^31]^(k^6)` ordered configurations and, including beta indices,
   at most `2^16 k^14[2^69 k^31]^(k^6)` tests.  If every endpoint moment has
   error at most `eta`, direct absolute summation bounds beta error by
   `eta (N+1) binom(N,j) 2^(N-j) <= eta (N+1)3^N`.  Consequently
   `p >= 2N+ceil(log2((N+1)/zeta))` bits after the binary point suffice for
   error at most `zeta`.

These checks establish the universal inequalities on paper.  They do not
depend on favorable examples from the producer.

## Reproduction and independent implementation

The submitted packet's hash manifest passed in full.  Its own producer check
passed under both ordinary and optimized Python and returned

```text
RATIONAL_COMPACT_FRONTIER_CONTROLS_PASS
22f543a40f8a2a1298ce2ff933bb78422f57528b032db957b5d481725d1d227c
```

The hashes of the three principal source files, read from the exact commit,
are respectively:

```text
RATIONAL_INTERFACE.md  39c63a99a1c4ba57d1f8e873f33fd12260215cd9fc7fb50edc131a55c8e83308
rational_frontier.py   d2f0373812b17e1a710928121f7c16e581f6e298099df971efe295d76e10ae65
RATIONAL_EXPECTED.json 22f543a40f8a2a1298ce2ff933bb78422f57528b032db957b5d481725d1d227c
```

The reviewer checker in this directory is independently written and imports
no submitted code or expected output.  It reconstructs the merge-expand-round
algorithm with exact `Fraction` arithmetic and revalidates its output
contract.  Its deterministic 4,203 cases include contractions at scales
`0`, `1/3`, and `1`, an axis and a rational `3-4-5` rotation, all denominator-
four weight-simplex points on four labels, duplicate and near-colliding
sources, a merge-boundary equality, and a no-merge three-dimensional case.
It exercises 4,202 merging cases, 4,081 zero-input-weight cases, and 1,129
point-law outputs.  It also checks the composition/count/pair-loss constants
for `1 <= k <= 64` and exact moment coefficient norms through degree 32.
Normal and `-O` runs produce the same frozen result.

This finite suite checks the implementation and edge cases.  It is not used
as a proof by enumeration.

## Trust boundary and nonclaims

The accepted claim rests on elementary exact arithmetic, the standard
Gaussian translation total-variation bound, and the focused portions of the
credited localization and beta-approximation arguments described above.
This review does **not** provide blanket acceptance of every statement in
those dependency packets.

Neither the submitted producer nor this review:

- enumerates the enormous rational task;
- computes a high-degree Gaussian moment or determines a beta sign;
- proves the finite certificate condition for all rational inputs;
- proves `D=0` or supplies a counterexample;
- turns the existing degree-five cell consumer into the required degree
  `2^16 k^8-2` producer; or
- establishes novelty relative to all external literature.

In particular, a failed coefficient lower bound would not be a negative beta
witness, and the positive pair-loss floor alone is not a hinge-sign theorem.
The contribution is a correct effective interface supporting the headline
problem, not the headline conclusion itself.
