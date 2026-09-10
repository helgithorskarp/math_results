# Exact `e0` degree-profile exclusions for `C(13,7,5)`

## Result

Every hypothetical 77-block `C(13,7,5)` cover is now known to lie in the
global `e0` branch.  This directory gives the first exhaustive pruning of that
sole remaining branch:

> Of the 143 second-link symmetry orbits of integral point-degree excess
> profiles in `e0`, 20 orbits (representing 536 of the 8,008 labeled profiles)
> have infeasible linear relaxations.  In particular every profile of type
> `6` or `5+1` is impossible, so every point has degree at most 45.

The precise orbit exclusions by integer partition are:

| point-excess partition | all profile orbits | excluded here | unresolved |
| --- | ---: | ---: | ---: |
| `6` | 2 | 2 | 0 |
| `5+1` | 5 | 5 | 0 |
| `4+2` | 5 | 4 | 1 |
| `4+1+1` | 12 | 6 | 6 |
| `3+3` | 4 | 3 | 1 |
| `3+2+1` | 19 | 0 | 19 |
| `3+1+1+1` | 19 | 0 | 19 |
| `2+2+2` | 6 | 0 | 6 |
| `2+2+1+1` | 28 | 0 | 28 |
| `2+1+1+1+1` | 31 | 0 | 31 |
| `1+1+1+1+1+1` | 12 | 0 | 12 |
| **total** | **143** | **20** | **123** |

This result does not exclude the remaining 123 profile orbits and does not
determine whether `C(13,7,5)` is 77 or 78.

The global starting point is the independently reviewed
[hard-`e1` elimination](../covering_c1375_hard_e1_elimination/), which proves
that every hypothetical 77-block cover contains two degree-41 points of pair
multiplicity 20.  The canonical second link comes from Charlie Krug's exact
value and uniqueness theorem for `C(11,5,3)=20`; see Proposition 15 of
[arXiv:2607.23766](https://arxiv.org/abs/2607.23766).

## Exact `e0` reduction

Label the degree-41 pair `{0,1}`.  The 20 blocks through both points, with the
pair deleted, form the unique optimal `C(11,5,3)` cover `M` on

```text
R = {2,...,12}.
```

After fixing the canonical `M` extracted from the archived
[`cover_41.txt`](../covering_c1375_fixed_link_symmetry/cover_41.txt), the other
57 blocks split exhaustively into:

| family | form | candidates | selected |
| --- | --- | ---: | ---: |
| `B` | `{0}` plus a six-subset of `R` | 462 | 21 |
| `C` | `{1}` plus a six-subset of `R` | 462 | 21 |
| `D` | a seven-subset of `R` | 330 | 15 |

Let the full degrees on `R` be `41+a_p`.  Since the roots have degree 41 and
`77*7-13*41=6`, the vector

```text
a = (a_2,...,a_12)
```

is a nonnegative integral weak composition of six.  There are
`C(16,10)=8,008` labeled vectors.  Two explicitly checked automorphisms of
`M` generate a group of order 240.  Its action partitions these vectors into
143 exact orbits; the checker enumerates the complete partition rather than
assuming it.

For one fixed profile `a`, introduce one variable `x_Q` for each of the 1,254
candidate blocks and relax it to `0 <= x_Q <= 1`.  Every completion satisfies:

1. all 902 five-sets not covered by the fixed 20 blocks have coverage at
   least one;
2. the three category sums are exactly `21,21,15`;
3. every point `p` in `R` has exact total degree `41+a_p`; and
4. every one-, two-, and three-subset has total multiplicity at least
   `41,20,9`, respectively.

The triple bound is `C(10,4,2)=9`: blocks through a fixed triple, with that
triple deleted, must cover all pairs of the remaining ten points.  The final
matrix has 1,270 rows and 101,850 nonzero unit entries.  No quadruple-shadow
constraint is needed for any published exclusion.

## Exact Farkas certificates

`FARKAS_CERTIFICATES.json` contains one sparse integer multiplier vector for
each of the twenty excluded profile orbits.  HiGHS supplied floating-point
dual rays only as discovery data.  Each ray was normalized and rounded only
after an exact strict inequality survived.

For rows `l_i <= A_i x <= u_i` and integer multipliers `y_i`, a positive
multiplier selects `l_i` and a negative multiplier selects `u_i`.  Put

```text
b = sum_(y_i>0) y_i l_i + sum_(y_i<0) y_i u_i,
c = sum_i y_i A_i.
```

Every feasible point would satisfy `c*x >= b`, while the exact box maximum is

```text
c*x <= sum_Q max(c_Q,0).
```

Every certificate verifies with Python integers that

```text
b - sum_Q max(c_Q,0) > 0.
```

The twenty strict gaps are

```text
1842,1150,5594,982,184,14128,4649,408,2062,757,
200,1056,226,530,1403,4607,78,439,884,648.
```

Thus no floating-point tolerance or solver verdict remains in the theorem's
local verification boundary.  `CERTIFICATE_SUMMARY.tsv` lists every orbit,
representative, support, scale, and exact arithmetic value.

## Reproduction

The primary checker requires only CPython 3.11 or later:

```sh
python3 e0_degree_profile_exclusion.py \
  ../covering_c1375_fixed_link_symmetry/cover_41.txt \
  FARKAS_CERTIFICATES.json \
  | diff -u EXPECTED_CHECK.txt -
```

The independent checker imports neither the generator nor the primary
checker.  It reconstructs the entire formula with integer bit masks, generates
the profile orbits independently, and replays every multiplier entry:

```sh
python3 independent_bitmask_check.py \
  ../covering_c1375_fixed_link_symmetry/cover_41.txt \
  FARKAS_CERTIFICATES.json \
  | diff -u EXPECTED_INDEPENDENT_CHECK.txt -
```

To regenerate the solver-discovered rays byte-for-byte, use the pinned
versions:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 generate_farkas.py \
  ../covering_c1375_fixed_link_symmetry/cover_41.txt \
  /tmp/FARKAS_CERTIFICATES.json
cmp FARKAS_CERTIFICATES.json /tmp/FARKAS_CERTIFICATES.json
```

The recorded environment used CPython 3.11.2, `highspy==1.11.0`, and
`numpy==2.4.6`.  Generation uses one thread, presolve off, the serial dual
simplex strategy, and random seed zero.  Both exact checkers use only the
standard library.

## Trust boundary

The local profile orbit partition, finite reduction, and all twenty Farkas
contradictions are reconstructed exactly.  HiGHS and NumPy are regeneration
tools only.  The global degree-45 corollary additionally imports the reviewed
global `e0` reduction and Krug's certified uniqueness of the 20-block
`C(11,5,3)` cover.  The 123 profiles without a published contradiction remain
open and are not claimed feasible.
