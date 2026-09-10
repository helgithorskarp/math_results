# Exact classification of the hard-`e1` optimal point link for `C(13,7,5)`

## Result

This directory proves an exact computer-assisted classification:

> Up to isomorphism, the archived 41-block `C(12,6,4)` cover is the only
> optimal `C(12,6,4)` cover with point-degree profile `20^6,21^6`.

Consequently, in the hard-`e1` branch of the
[global point-link bridge](../covering_c1375_global_point_link_bridge/), the
link of a degree-41 point is necessarily isomorphic to the archived cover in
[`cover_41.txt`](../covering_c1375_fixed_link_symmetry/cover_41.txt).  Thus all
twelve hard-`e1` branches are subsumed by the single unrestricted fixed-link
completion problem already encoded in
[`covering_c1375_fixed_link_symmetry`](../covering_c1375_fixed_link_symmetry/).

This does **not** prove that the fixed link has no asymmetric completion, does
not resolve the separate `e0` branch, and does not determine `C(13,7,5)`.
The exact frontier remains `77 <= C(13,7,5) <= 78`.

The result uses Charlie Krug's certified theorem that `C(11,5,3)=20` and its
20-block optimum is unique up to isomorphism; see Proposition 5 and
Proposition 15 of [arXiv:2607.23766](https://arxiv.org/abs/2607.23766).  The
order-240 second-link group and its twelve orbits on six-subsets were
established by the global bridge and independently accepted in the
[bridge review](../covering_c1375_global_point_link_bridge_review1/).

## Finite reduction

Fix point `1` of degree 20 in an optimal 41-block `C(12,6,4)` cover.  Its
20 blocks through `1`, with `1` removed, form the unique optimal
`C(11,5,3)` cover `M` on

```text
R = {2,...,12}.
```

For every six-subset `S` of `R`, let `x_S` say whether `S` is one of the 21
blocks not containing `1`.  There are 462 variables.  If `H` is the six-set
of degree-21 points, every extension satisfies:

1. `0 <= x_S <= 1` and `sum_S x_S = 21`;
2. every one of the 230 quadruples not already covered by `M` is covered by
   at least one selected `S`;
3. for each `i` in `R`,
   `sum_(S contains i) x_S = 20 + 1_(i in H) - deg_M(i)`;
4. every pair has total multiplicity at least `C(10,4,2)=9`; and
5. every triple has total multiplicity at least 3, by the elementary count
   that three free block positions must cover nine possible fourth points.

These are necessary linear inequalities; integrality is not used in the
first eleven exclusions.  The order-240 group has twelve orbits on the 462
possible choices of `H`.  `CERTIFICATE_SUMMARY.tsv` lists one representative
per orbit.

Orbits 0 through 10 have infeasible linear relaxations.  Orbit 11 has the
concrete extension in `ORBIT11_EXTENSION.txt`.  That 41-block cover is the
image of the archived cover under the explicitly checked permutation

```text
1->1, 2->3, 3->2, 4->7, 5->8, 6->9,
7->5, 8->6, 9->4, 10->10, 11->12, 12->11.
```

To test uniqueness inside orbit 11, add

```text
sum_(S in the known 21-block extension) x_S <= 20.
```

Every distinct binary 21-subset obeys this blocker.  The blocked linear
relaxation is also infeasible.  Therefore orbit 11 contains exactly the known
extension and the other eleven high-set orbits contain none.

## Exact Farkas certificates

`FARKAS_CERTIFICATES.json` contains twelve sparse integer multiplier vectors:
eleven for the empty high-set orbits and one for the blocked alternatives in
orbit 11.  They were discovered from HiGHS dual rays and then rounded only
when an exact strict integer inequality survived.

For a row `l_i <= a_i x <= u_i` with multiplier `y_i`, a positive multiplier
uses the lower bound and a negative multiplier uses the upper bound.  Put

```text
b = sum_(y_i>0) y_i l_i + sum_(y_i<0) y_i u_i,
c = sum_i y_i a_i.
```

Every feasible point would have `c x >= b`.  But `0 <= x_S <= 1` gives the
exact box maximum

```text
c x <= sum_S max(c_S,0).
```

Every published certificate verifies

```text
b > sum_S max(c_S,0)
```

using only Python integers.  The twelve strict gaps are

```text
542, 701, 29, 541, 56, 670, 674, 12, 26, 466, 449, 50.
```

The smallest gap is 12; no floating-point tolerance enters the checked
conclusion.

## Reproduction

The primary checker needs only CPython 3.11 or later:

```sh
python3 hard_e1_link_classification.py \
  ../covering_c1375_fixed_link_symmetry/cover_41.txt \
  ORBIT11_EXTENSION.txt FARKAS_CERTIFICATES.json \
  | diff -u EXPECTED_CHECK.txt -
```

The independent checker does not import the generator or primary checker.  It
reconstructs the entire matrix with point-set bit masks and replays every
integer inequality entry by entry:

```sh
python3 independent_farkas_check.py \
  ../covering_c1375_fixed_link_symmetry/cover_41.txt \
  ORBIT11_EXTENSION.txt FARKAS_CERTIFICATES.json \
  | diff -u EXPECTED_INDEPENDENT_CHECK.txt -
```

To regenerate the solver-discovered multipliers exactly, use the pinned
HiGHS and NumPy versions:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 generate_farkas.py \
  ../covering_c1375_fixed_link_symmetry/cover_41.txt \
  ORBIT11_EXTENSION.txt /tmp/FARKAS_CERTIFICATES.json
cmp FARKAS_CERTIFICATES.json /tmp/FARKAS_CERTIFICATES.json
```

The recorded environment used CPython 3.11.2, `highspy==1.11.0`, and
`numpy==2.4.6`.  Generation is deterministic with one thread, presolve off,
the serial dual simplex strategy, and random seed zero.  It takes about two
seconds here.  Both exact checkers take under one second.

## Trust boundary

The theorem imports the certified uniqueness of the 20-block `C(11,5,3)`
cover and the independently reviewed order-240 orbit partition.  The
published witness and all twelve Farkas contradictions are checked directly.
HiGHS and NumPy are discovery and reproducibility tools only: neither is in
the verification trust boundary.  The primary checker uses explicit set
tuples; the independent checker reconstructs the matrix using integer bit
masks.
