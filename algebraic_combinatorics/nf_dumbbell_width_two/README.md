# The NF-number of width-two dumbbell graphs

## Result

Let `B_{2,m}` be the dumbbell graph formed from disjoint cliques `K_2` and
`K_m` by adding one bridge edge.  Under the standard convention that the
NF-number is the least positive `q` for which
`delta_NF^q(B_{2,m})` is *isomorphic* to `B_{2,m}`, the following holds:

**Theorem.** For every `m >= 3`,

```text
NF(B_{2,m}) = m + 4.
```

For the exceptional graph `B_{2,2}=P_4`, the up-to-isomorphism NF-number is
`1`, while its labelled orbit has period `2`.

This proves the first infinite subfamily of Conjecture 3.7 in B. A. Rather,
*The NF-operator and the NF-Numbers of Simplicial Complexes*,
[arXiv:2605.30781](https://arxiv.org/abs/2605.30781), and corrects that
conjecture's exceptional value `2` when its stated up-to-isomorphism
definition is used.  The source itself notes that `P_4` has NF-number `1` up
to isomorphism, so its displayed exceptional value and Table 1 mix the
labelled and unlabelled conventions.

## Definitions and the type reduction

For a simplicial complex `Delta` on `V`, the facets of `delta_NF(Delta)` are
the maximal subsets of `V` which contain no facet of `Delta`.  Equivalently,
if `T` is the facet antichain, then

```text
D(T) = max(2^V \ upward_closure(T)).                 (1)
```

Write

```text
V = {x_0,x_1} disjoint_union {y_0,y_1,...,y_b},
b = m-1,
```

and take `x_0 y_0` as the bridge.  The subgroup permuting
`y_1,...,y_b` preserves the entire orbit.  A subset therefore has type

```text
(a,c,d,j) in {0,1}^3 x {0,...,b},                  (2)
```

where the first three entries indicate membership of `x_0,x_1,y_0`, and
`j` is the number of ordinary `y`-vertices.  We use a tuple to denote the
whole orbit of subsets having that type.

For two types `u` and `v`, some set of type `u` is contained in a set of type
`v` exactly when `u <= v` coordinatewise.  Consequently (1) can be applied
directly in the type poset

```text
Q_b = {0,1}^3 x {0,...,b}.                          (3)
```

This proves that the following type calculation is not a heuristic symmetry
quotient: it is an exact calculation of every facet orbit.

## Closed orbit

For `m >= 3`, define five antichains `F_0,...,F_4` in `Q_b` by

```text
F_0 = {0002, 0011, 1010, 1100},
F_1 = {0101, 0110, 1001},
F_2 = {001b, 1010, 1100},
F_3 = {010b, 011(b-1), 100b},
F_4 = {001b, 101(b-1), 110(b-1), 111(b-2)}.         (4)
```

Concatenation is tuple notation; for example, `101(b-1)` means
`(1,0,1,b-1)`.

For `u in {0,1}^3`, define `w(u)` by

| `u` | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `w(u)` | 3 | 2 | 1 | 0 | 1 | -1 | -1 | -2 |

For `0 <= s <= b-1`, put

```text
A_s = { (u, s+w(u)) : 0 <= s+w(u) <= b }.          (5)
```

Here and below a term whose last coordinate lies outside `[0,b]` is simply
absent.  Direct application of (1) in (3) gives

```text
D(F_0)=F_1,  D(F_1)=F_2,  D(F_2)=F_3,
D(F_3)=F_4,  D(F_4)=A_{b-1},                       (6)
D(A_s)=A_{s-1}  (1 <= s <= b-1),
D(A_0)=F_0.                                        (7)
```

For completeness, the finite calculation behind (7) is as follows.  For
each binary `u`, the largest allowed last coordinate after forbidding
`A_s` is

```text
h_s(u) = min({s+w(v)-1 : v<=u and 0<=s+w(v)<=b} union {b}).  (8)
```

For `1 <= s <= b-1`, substituting the eight weights simplifies (8) to

```text
h_s(u) = max(-1,min(b,s-1+w(u))).                   (9)
```

Indeed, `w` strictly decreases on every strict comparison in the binary
cube, so the facet with binary part `u` supplies the least threshold whenever
it is in range.  The sole below-range possibility needing attention is
`s=1,u=111`; its `101` and `110` predecessors both have threshold zero and
give height `-1`.  The only above-range top that can survive clipping is
`s=b-1,u=000`; it is dominated by the valid top `(001,b)`.  It follows that
the maximal nonnegative tops in (9) are exactly the valid terms
`(u,s-1+w(u))` in `A_{s-1}`.  This proves the middle identity in (7).

For `s=0`, the eight fibre heights from (8), in the order of the weight table,
are

```text
2, 1, 0, -1, 0, 0, 0, -1.
```

Their maximal types are `0002,0011,1010,1100`, namely `F_0`, proving the
wrap identity.  The same maximal-allowed-type test applied to the small lists
in (4) gives exactly the five outputs displayed in (6).  Thus (6)-(7) are a
finite antichain calculation valid for symbolic `b`, not an induction
inferred from computed examples.

Starting at `F_0`, the orbit is therefore

```text
F_0,F_1,F_2,F_3,F_4,A_{b-1},A_{b-2},...,A_0,F_0.   (10)
```

It has labelled period `5+b=m+4`.

It remains to exclude an earlier *isomorphic* return.  Every state from
`F_2` through `A_0` has a facet of cardinality at least three, while `F_0`
is a graph.  The only remaining candidate is `F_1`, the bipartite graph
`K_{2,m}` with the bridge pair deleted.  It is not isomorphic to `F_0`,
because `F_0` contains the clique `K_m` and hence a triangle for `m>=3`,
whereas `F_1` is bipartite.  This proves the theorem.

When `m=2`, `F_0` and `D(F_0)` are two labelled copies of `P_4`.  The explicit
permutation in `verify.py` maps one to the other, proving the exceptional
up-to-isomorphism value `1`.

## Exact verification

Requires CPython 3.10 or later and no third-party packages.

```bash
python3 verify.py --max-m 200 --direct-max-m 8
python3 independent_check.py --max-m 8
python3 -m unittest -v test_verify.py
```

Expected first line:

```text
VERIFIED m=2..200; type_states=20891; type_transitions=20891; definition_states=59; expanded_facets=2055; NF(B_2,2)=1 up_to_isomorphism
```

The independent checker prints:

```text
INDEPENDENT VERIFIED m=2..8; full_boolean_states=59; facets_seen_with_multiplicity=2055; labelled_periods=(2,m+4)
```

`verify.py` performs two exact checks:

1. It evaluates (1) on every element of the type poset (3), checks every
   transition in (10) through `m=200`, and checks the labelled period.
2. Independently of the quotient transition, it expands all facet orbits to
   bit masks and applies the defining maximal-subset operation on the full
   Boolean lattice for every `2 <= m <= 8`.

`independent_check.py` separately reconstructs each dumbbell from its edge
definition and iterates on the full Boolean lattice without importing the
formula checker or using symmetry types.  It reproduces all labelled periods
through `m=8` and the explicit exceptional isomorphism.

All arithmetic is exact.  The universal theorem rests on the symbolic
eight-type proof above; the finite computations are corroborative and guard
against transcription, boundary, and convention errors.

## Literature and novelty boundary

- T. Hibi and H. Mahmood, *The NF-number of a simplicial complex*,
  [arXiv:2005.01247](https://arxiv.org/abs/2005.01247); Algebra Colloquium 29
  (2022), 643-650.  This introduces the invariant and proves the analogous
  `n+m+2` formula for the disjoint union `K_n disjoint_union K_m`.
- B. A. Rather, *The NF-operator and the NF-Numbers of Simplicial Complexes*,
  [arXiv:2605.30781](https://arxiv.org/abs/2605.30781).  Conjecture 3.7 poses
  the dumbbell formula and reports computation only for `2 <= n,m <= 5`.

Targeted searches on 2026-09-03 found no source proving the infinite
`B_{2,m}` case.  The appropriate claim is therefore *apparently new to the
searched sources*, not a historical priority claim.
