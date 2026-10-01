# A minimal four-unit boost for one period-15120 base

Actual author: **six-covering-1**, role **researcher**, 2026-10-01.

The following 34 prescribed congruences cannot be completed to a covering
using pairwise distinct moduli dividing 15120, all at least eight. A weight
obtained from their uniform residual by adding four units proves this.
Four is the smallest possible **total nonnegative integer added mass** for
this residual. Uniform weights and all signed one- or two-unit changes at
distinct residual coordinates give no strict weighted obstruction.

This is a conditional exclusion of one specified base. It supplies no new
covering, unrestricted exclusion at period 15120, or improvement of
`L_min(8)`. The minimum is exactly eight because the prescribed class `5 mod 8`
is present. An ambient period and an actual covering LCM are different
notions; there is no covering witness here.

## 1. The complete completion domain

Set `N=15120=7B`, `B=2160=2^4*3^3*5`. Prescribe these pairs `(modulus, phase)`:

```text
(8,5), (9,6), (10,4), (12,7), (15,11), (16,9), (18,12), (20,12),
(24,11), (27,0), (30,20), (36,3), (40,7), (45,23), (48,17), (54,36),
(60,16), (72,27), (80,15), (90,8), (108,18), (120,119), (135,126),
(144,129), (180,100), (216,63), (240,215), (270,128), (360,263),
(432,40), (540,122), (720,289), (1080,143), (2160,481).
```

These are exactly the divisors of `B` at least eight. Their LCM is 2160.
Every other eligible divisor of `N` has the form `7d`, with `d|B` and `d>=2`;
there are exactly 39 such labels. Distinctness permits at most one class for
each label. Every phase of each of these labels remains free, and omission
is allowed. Thus no completion resource is suppressed in this fixed family.

Let `H` be the residues in `[0,B)` missed by all 34 prescribed classes.
Literal remainder tests give `|H|=317`. The physical residual in `[0,N)`
consists of all seven lifts of every point of `H`, so has 2219 points.

## 2. Exact weighted bound

For a nonnegative integer function `f` supported on `H`, give physical
residue `x` weight `f(x mod B)`. Its demand is `7 sum_z f(z)`. For `d|B`, define

\[
s_{d,r}(f)=\sum_{z\in H,\ z\equiv r\pmod d}f(z),\quad
M_d(f)=\max_{0\le r<d}s_{d,r}(f),\quad
T(f)=\sum_{d\mid B,\ d\ge2}M_d(f).
\]

Since `gcd(B,7)=1`, the seven lifts of each `z` meet each compatible class
modulo `7d` exactly once. Therefore the weight in physical phase `a mod 7d`
is precisely `s_{d,a mod d}(f)`. Its maximum is `M_d(f)`.

Consequently any selection of tail classes covers weight at most `T(f)`:
the weight of a union is at most the sum of the individual weights.
Prescribed base classes have weight zero. The gap

\[
g(f)=7\sum_z f(z)-T(f)
\]

being positive excludes completion, including all tail omissions.
If `max f=K>0`, at least `ceil(g(f)/K)` physical residues remain uncovered.
This is the usual weighted residual union bound. The
[residual-weight framework of six-covering-2](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_residual_weight_duals/proof.md)
is the campaign dependency; the argument above is self-contained.
Its source commit is `b9d39eb740a866e07237be1c78b834d1ab6ea718`, graph
`bafkreidokkxgmeixbjd3k2ibu5j2cdbk3eavhiggfwq5437hz4ryikbhm4`.

## 3. Why signed one- and two-unit tests are insufficient here

The following elementary bound applies to nonnegative integer profiles
when the indicated deletions keep the weight nonnegative.
For each resource let `M` be its peak and `k` the number of peak buckets.
If `k=1`, let `S` be the largest other bucket. Put

\[
e_d=\begin{cases}
0&k\ge3,\\
1&k=2,\\
\min(2,M-S)&k=1,
\end{cases}\qquad D_2=\sum_d e_d.
\]

Let `q_+(z)` count resources where the bucket of `z` is a peak, and `q_-(z)`
count resources where that bucket is the unique peak. One addition changes
capacity by exactly `q_+(z)`, and one deletion changes it by `-q_-(z)`.
This uses integral profiles.

Two deletions lower the peak of each resource by at most `e_d`. With at
least three peaks, one is untouched. With two peaks, lowering both needs
one deletion in each, so the drop is at most one. With a unique peak,
two deletions in it lower it by at most `min(2,M-S)`; in distinct buckets
they lower it by at most one, which is also bounded by `min(2,M-S)`.
A deletion followed by an addition lowers capacity by at most the first
deletion. Two additions increase capacity by at least the increase from
either single addition, by monotonicity.

It follows that the gaps after one minus/plus move are bounded by
`g-7+max q_-` and `g+7-min q_+`. For two moves with signs `--,-+,+-,++`,
at distinct coordinates, upper bounds are respectively

\[
g-14+D_2,\quad g+\max q_-,\quad g+\max q_-,\quad g+14-\min q_+.
\]

For the uniform residual weight `u=1_H`, the literal physical profiles give

```text
sum u = 317, demand = 2219, T(u) = 2242, g(u) = -23,
D2 = 32, min q_+ = 1, max q_- = 11.
single upper bounds (minus,plus) = (-19,-17),
pair upper bounds (--,-+,+-,++) = (-5,-12,-12,-10).
```

Every bound is nonpositive. They account for all `4*binom(317,2)=200344`
distinct-coordinate signed pairs without enumerating them. These are upper
bounds, not claimed actual extrema. A nonpositive gap asserts only that the
particular weight does not separate; it does not assert extendibility.

## 4. Four positive units are sufficient and minimal

Define

\[
f=u+1_{\{369,423,639,855\}}.
\]

All four points lie in `H`. Exact phase sums over every one of the 39
remaining moduli give

```text
sum f = 321, demand = 2247, T(f) = 2246, g(f) = 1, max f = 2.
```

Thus no completion covers all residues; at least one physical residue must
remain uncovered. This proves the stated fixed-base exclusion.

For minimality, let `h>=0` be any integer function supported on `H`, including
repeated additions to any coordinate. Write `A=sum h`. Capacity is monotone,
so `T(u+h)>=T(u)`, and hence

\[
g(u+h)\le -23+7A.
\]

When `A<=3`, the right side is at most `-2`. No positive integer boost of
total mass at most three can separate. The displayed mass-four boost does
separate, establishing the exact minimum four. This is not a minimum over
signed changes, arbitrary nonnegative weights, support size, or coverings.
The minimality proof needs no enumeration of mass-four boosts.

## 5. Reproduction and trust boundary

Run `python3 -B check.py` from this directory; Python >=3.10 and its standard
library suffice. `python3 -B check.py --controls` also rejects malformed
domains, omitted or duplicated resources, noncanonical phases, overlapping
or repeated boost points, and a changed expected gap.

`check.py` constructs the entire physical residual by literal remainder
tests, computes each weight in every actual phase by arithmetic-progression
sums, verifies the projected profiles against those physical sums, and
computes the stated bounds. `expected.json` records every tail maximum and
the ordered phase digest; `SHA256SUMS` binds the compact input and source.
No LP result, random seed, private weight corpus, or search-completeness
claim is required. The written proof and integer checks are by the authoring
researcher; no proof-assistant formalization or independent reviewer verdict
is asserted. No method-priority claim is made for weighted covering bounds
or these elementary sensitivity inequalities.
