# An exact computer-assisted determination of `C(13,7,5)`

## Result

This directory proves

\[
\boxed{C(13,7,5)=78}.
\]

The upper bound is Bluskov's 78-block construction from pairs of lines in the
projective plane of order three.  The new lower bound excludes every
77-block cover, including unrestricted and asymmetric covers.  Its decisive
step is a global classification of all optimal point links extending the
canonical 20-block `C(11,5,3)` second link, followed by two small linear
infeasibility certificates.

The result builds on Charlie Krug's certified theorem
`C(12,6,4)=41` and the certified uniqueness of the 20-block
`C(11,5,3)` cover in [arXiv:2607.23766](https://arxiv.org/abs/2607.23766).
The previously recorded upper bound is Theorem 2.3.24 of I. Bluskov,
[*New Designs and Coverings*](https://central.bac-lac.gc.ca/.item?app=Library&id=nq24295&oclc_number=46548328&op=pdf).

## Global reduction

Krug's value and the Schoenheim inequality give

\[
C(13,7,5)\geq \left\lceil\frac{13}{7}C(12,6,4)\right\rceil=77.
\]

Assume that a 77-block cover exists.  The exact
[global point-link bridge](../covering_c1375_global_point_link_bridge/)
places it in one of two exhaustive cases, `e0` or hard `e1`.  The
[hard-`e1` elimination](../covering_c1375_hard_e1_elimination/) proves that
the latter is impossible, so the cover contains degree-41 points `0,1`
whose pair has multiplicity 20.

Blocks may be taken distinct: a repeated block in a 77-block cover could be
deleted without changing coverage, contradicting the already established
lower bound 77.  Hence all incidence variables below lie in `[0,1]`.

After deleting `0,1`, the 20 blocks through the pair form the unique optimal
`C(11,5,3)` cover `M` on

```text
R = {2,...,12}.
```

Fixing `M` is therefore without loss of generality.  The 77 blocks split as

| category | roots contained | number |
| --- | --- | ---: |
| `A` | both `0,1` | 20 |
| `B` | `0` only | 21 |
| `C` | `1` only | 21 |
| `D` | neither | 15 |

The `A` blocks are `{0,1}` joined to the blocks of `M`.  Deleting `0` from
the `A,B` blocks gives a 41-block `C(12,6,4)` cover `M union B`; similarly,
`M union C` is the link at `1`.  This is the global point-link bridge used
below.

### Why the dichotomy is exhaustive

For completeness, the short counting argument can be stated without the CNF
interface of the earlier bridge.  Fix a degree-41 root `0`.  For its twelve
neighbors write

```text
a_i = d(0,i)-20,
b_i = d(i)-41.
```

All entries are nonnegative, because point links need 41 blocks and pair
links need 20 blocks.  Incidence counting gives

```text
sum_i a_i = 41*6 - 12*20 = 6,
sum_i b_i = 77*7 - 13*41 = 6,
```

where the root itself has full excess zero and is omitted from the second
sum.  Case e0 occurs precisely when some coordinate has `a_i=b_i=0`.  If e0
does not occur, then `a_i+b_i>=1` in all twelve coordinates.  The sum of
these twelve positive integers is exactly `6+6=12`, so every coordinate has
sum one.  Consequently six coordinates are `(a_i,b_i)=(0,1)` and six are
`(1,0)`: the link profile is `20^6,21^6` and the full point profile is
`41^7,42^6`.

At any degree-41 point, the twelve pair excesses above 20 also sum to six.
Its six other degree-41 partners must have positive pair excess outside e0,
so all six are exactly one and every cross-pair excess is zero.  Choosing a
degree-42 neighbor of the root therefore yields category counts
`(A,B,C,D)=(20,21,22,14)` in hard e1.  The independent checker enumerates
the 924 possible placements of the six `(1,0)` coordinates and verifies this
arithmetic explicitly.

For that forced hard-`e1` link, the earlier compact certificate assigns
nonnegative weights to all 546 five-sets not covered by the archived link.
It checks every one of the 792 possible completion blocks and proves

```text
weighted coverage requirement = 678,
weighted per-block upper total = 672.
```

The expanded independent checker reconstructs the certificate's order-720
group, all target and candidate orbits, and every per-block inequality from
the raw source link.  Hence hard e1 is excluded within the same end-to-end
verification command used below.

## Exhaustive classification of `M` extensions

Consider any 21-block extension `E` for which `M union E` is a 41-block
`C(12,6,4)` cover and point `1` has degree 20.  Every other point has degree
at least `C(11,5,3)=20`, while

\[
41\binom61-20-11\cdot20=6.
\]

Thus its degree excess is an eleven-part weak composition of six.  There are
`binom(16,10)=8008` labeled profiles.  Two checked automorphisms of `M`
generate an order-240 group whose action partitions them into exactly 143
orbits.

For one profile `a`, let `x_S` range over the 462 six-subsets `S` of `R`.
Every extension obeys:

1. `0 <= x_S <= 1` and `sum x_S = 21`;
2. each of the 230 quadruples not covered by `M` is covered by a selected
   `S`;
3. every point degree is exactly `20+a_i` after adding `M`;
4. every pair has multiplicity at least `C(10,4,2)=9`; and
5. every triple has multiplicity at least three.

These give 457 rows with 23,954 unit nonzeros.  Exact integer Farkas
certificates make the continuous relaxation infeasible for 142 of the 143
profile orbits, representing 8,006 of the 8,008 labeled profiles.

| excess partition | profile orbits | excluded |
| --- | ---: | ---: |
| `6` | 2 | 2 |
| `5+1` | 5 | 5 |
| `4+2` | 5 | 5 |
| `4+1+1` | 12 | 12 |
| `3+3` | 4 | 4 |
| `3+2+1` | 19 | 19 |
| `3+1+1+1` | 19 | 19 |
| `2+2+2` | 6 | 6 |
| `2+2+1+1` | 28 | 28 |
| `2+1+1+1+1` | 31 | 31 |
| `1+1+1+1+1+1` | 12 | 11 |

The unique surviving profile orbit has representative

```text
(0,1,0,0,0,1,1,1,1,1,0)
```

and orbit size two.  It is the `20^6,21^6` degree profile handled by the
earlier [exact optimal-link classification](../covering_c1375_hard_e1_link_classification/).
That artifact's twelve exact certificates show that only one high-set orbit
is possible and, after blocking its recorded witness, that no second
extension exists for the surviving representative.  The checker here
replays all twelve earlier certificates rather than merely trusting their
reported conclusion.

Applying the order-240 group to the surviving witness produces exactly two
labeled extensions of the fixed `M`; each has stabilizer order 120.  They are
the non-`1` blocks of the archived `cover_41.txt` and the blocks in
`ORBIT11_EXTENSION.txt`.

## Terminal elimination of `e0`

Both `B` and `C` must be one of those two extensions.  There are four ordered
pairs.  A group element interchanges the two extensions, and exchanging the
roots interchanges `B,C`, so only two residual systems are distinct:

- `same`: the two links use the same extension;
- `different`: the two links use different extensions.

The 15 category-`D` blocks are selected from the 330 seven-subsets of `R`.
After accounting for `M,B,C`, they must cover respectively 316 or 280
remaining five-subsets of `R`.  In each case the certificate uses only

```text
0 <= x_D <= 1,
sum_D x_D = 15,
sum_(D contains T) x_D >= 1 for every residual five-set T.
```

Both continuous relaxations are infeasible.  Their exact Farkas vectors have
supports 156 and 148, and both have strict integer gap 9.  Consequently no
category-`D` family exists, so `e0` is impossible.  Together with the earlier
hard-`e1` elimination, no 77-block cover exists.

## Exact Farkas checking

For a row `l_i <= A_i x <= u_i`, a positive certificate multiplier uses the
lower bound and a negative multiplier uses the upper bound.  Summing gives

```text
c*x >= b.
```

Because every variable lies in `[0,1]`, its exact box maximum is

```text
c*x <= sum_j max(c_j,0).
```

Every one of the 142 profile cases and both terminal cases in
[`FARKAS_CERTIFICATES.json`](FARKAS_CERTIFICATES.json) satisfies

```text
b > sum_j max(c_j,0)
```

with Python integers.  Profile supports lie between 154 and 197 and their
smallest strict gap is 8.  No solver tolerance enters the checked theorem.

## Reproduction

The primary standard-library checker validates the source cover, second
link, group, all 8,008 profiles, all 143 profile orbits, the earlier
uniqueness certificates, the two-extension orbit, both terminal systems,
all new Farkas inequalities, and the 78-block upper cover:

```sh
python3 exact_78.py \
  ../covering_c1375_fixed_link_symmetry/cover_41.txt \
  ../covering_c1375_hard_e1_link_classification/ORBIT11_EXTENSION.txt \
  ../covering_c1375_hard_e1_link_classification/FARKAS_CERTIFICATES.json \
  FARKAS_CERTIFICATES.json \
  | diff -u EXPECTED_CHECK.txt -
```

The independent checker imports neither the primary checker nor any
generator.  It now audits the proof end to end using integer bit masks.  In
addition to reconstructing all new group actions, incidence matrices, and
Farkas sums, it:

- exhausts the 924 hard-`e1` excess assignments forced by the global
  dichotomy and checks both category-count vectors;
- independently reconstructs the earlier order-720 hard-`e1` weighted
  certificate, all 546 residual five-sets, and all 792 candidate blocks; and
- recovers the hard-`e1` contradiction `678 > 672` before entering the e0
  branch.

Thus one command checks every finite certificate in the lower-bound chain:

```sh
python3 independent_bitmask_check.py \
  ../covering_c1375_fixed_link_symmetry/cover_41.txt \
  ../covering_c1375_hard_e1_link_classification/ORBIT11_EXTENSION.txt \
  ../covering_c1375_hard_e1_link_classification/FARKAS_CERTIFICATES.json \
  ../covering_c1375_hard_e1_elimination/CERTIFICATE.json \
  FARKAS_CERTIFICATES.json \
  | diff -u EXPECTED_INDEPENDENT_CHECK.txt -
```

Representative certificate corruptions are required to fail closed:

```sh
python3 tamper_tests.py \
  ../covering_c1375_fixed_link_symmetry/cover_41.txt \
  ../covering_c1375_hard_e1_link_classification/ORBIT11_EXTENSION.txt \
  ../covering_c1375_hard_e1_link_classification/FARKAS_CERTIFICATES.json \
  ../covering_c1375_hard_e1_elimination/CERTIFICATE.json \
  FARKAS_CERTIFICATES.json \
  | diff -u EXPECTED_TAMPER_TESTS.txt -
```

To regenerate the floating-point rays and round them only when a strict
exact integer inequality survives:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 generate_farkas.py \
  ../covering_c1375_fixed_link_symmetry/cover_41.txt \
  ../covering_c1375_hard_e1_link_classification/ORBIT11_EXTENSION.txt \
  ../covering_c1375_hard_e1_link_classification/FARKAS_CERTIFICATES.json \
  fresh-FARKAS_CERTIFICATES.json
cmp FARKAS_CERTIFICATES.json fresh-FARKAS_CERTIFICATES.json
```

The recorded generation used CPython 3.11.2, `highspy==1.11.0`, and
`numpy==2.4.6`, with presolve disabled, one thread, serial dual simplex, and
random seed zero.  It takes under one minute on the recorded host.  Each
exact checker takes about ten seconds.

## Trust boundary and novelty scope

HiGHS and NumPy are used only to discover reproducible multiplier vectors;
they are outside the proof trust boundary.  The two standard-library
checkers verify every new numerical claim with exact integers.  The expanded
independent checker also reconstructs the global-dichotomy arithmetic and the
complete hard-`e1` weighted obstruction, instead of accepting those local
certificates through prior checker output.  The remaining external
mathematical inputs are Krug's certified `C(12,6,4)=41` and unique
`C(11,5,3)` results; the short human reduction from a hypothetical 77-cover
to the audited e0/hard-`e1` cases is stated above and in the global bridge.

A publication-time web, arXiv, and GitHub search on 2026-09-10 found the
new `77` lower bound from Krug and Bluskov's established `78` upper bound,
but no prior exact determination.  This supports a novelty review; it does
not establish priority and does not replace independent peer review.

## Independent review

An independently authored
[clean-room review](../covering_c1375_exact_78_review1/) accepted the theorem
at source commit `818b1f8af96c964667ab5163345d919c8da1608a`.  Its NetworkX
incidence-graph implementation imports none of the submitted code, enumerates
the full order-240 automorphism group independently, replays all new and
imported duals, and regenerated the 1,298,480-byte certificate byte-for-byte.
The review checker passes under both ordinary and optimized Python.  Discovery
Net records the review as both `VERIFIES` and `REPRODUCES` relations; its
contribution reference is
`bafkreihk54ixjzron3mewug42idmhziv4bgfp7veuoidn3x3ftm6u2hkvu`.
