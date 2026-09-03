# The NF-number of width-three dumbbell graphs

## Result

Let `B_{3,m}` be the dumbbell graph formed from disjoint cliques `K_3` and
`K_m` by adding one bridge edge.  With the NF-number defined up to
isomorphism, as in the source paper, the complete width-three subfamily of
Conjecture 3.7 has the following value.

**Theorem.** For every `m >= 2`,

```text
NF(B_{3,m}) = m + 5.
```

Together with the preceding width-two theorem, this proves the conjectured
formula `NF(B_{n,m})=n+m+2` whenever `min(n,m) <= 3`, apart from
`B_{2,2}=P_4`, whose up-to-isomorphism NF-number is `1`.

## Exact type reduction

Write

```text
X = {x_0,x_1,x_2},    Y = {y_0,y_1,...,y_q},    q=m-1,
```

and let `x_0 y_0` be the bridge.  The group permuting `x_1,x_2` and,
independently, `y_1,...,y_q` preserves the full NF orbit.  A subset has type

```text
(a,i,b,j) in {0,1} x {0,1,2} x {0,1} x {0,...,q},       (1)
```

where `a,b` record the two bridge endpoints and `i,j` count ordinary
vertices in the two cliques.  A representative of one type can be contained
in a representative of another exactly when the coordinates are ordered
componentwise.  Thus the type poset

```text
P_q = {0,1} x {0,1,2} x {0,1} x {0,...,q}               (2)
```

computes every facet orbit without loss.

For an invariant facet antichain `E`, abbreviate a type `(a,i,b,j)` as
`aibj`.  For each base `z=(a,i,b)`, set

```text
h_E(z) = min({j-1 : (v,j) in E and v <= z} union {q}).   (3)
```

Discard negative heights.  The facets of `D(E)=delta_NF(E)` are exactly the
maximal types among `(z,h_E(z))`.  Formula (3) is simply the defining
maximal-subset operation, evaluated one last-coordinate fibre at a time.

## Closed orbit

Terms below whose last coordinate is outside `[0,q]` are absent.  Define the
six prefix antichains

```text
F_0 = {0002, 0011, 0200, 1010, 1100},
F_1 = {0101, 0110, 1001},
F_2 = {001q, 1010, 1200},
F_3 = {020q, 021(q-1), 110q},
F_4 = {011q, 101q, 111(q-1), 120(q-1), 121(q-2)},
F_5 = {001q, 020q, 021(q-1), 101(q-1),
       110q, 111(q-2), 120(q-2), 121(q-3)}.              (4)
```

The following weight table is indexed by the 12 bases `z=(a,i,b)`:

| `z` | 000 | 001 | 010 | 011 | 020 | 021 | 100 | 101 | 110 | 111 | 120 | 121 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `w(z)` | 3 | 2 | 1 | 0 | 0 | -1 | 1 | -1 | 0 | -2 | -2 | -3 |

For `1 <= s <= q-1`, put

```text
A_s = {(z,s+w(z)) : 0 <= s+w(z) <= q}.                  (5)
```

The weights strictly decrease on every strict comparison of bases, so the
valid types in (5) are automatically an antichain.  Finally, set

```text
T = {0003, 0012, 0101, 0110, 1001, 1200},               (6)
```

again omitting out-of-range terms.  Direct substitution in (3) gives

```text
D(F_r)=F_(r+1)                         (0 <= r < 5),
D(F_5)=A_(q-1)                         (q >= 2),
D(F_5)=T                               (q = 1),
D(A_s)=A_(s-1)                         (2 <= s <= q-1),
D(A_1)=T,
D(T)=F_0.                                                (7)
```

Here is the finite calculation behind the translating part.  If the facet
with base `z` is in range, its threshold is least among all predecessors of
`z`, and (3) gives height `s-1+w(z)`.  There are only two clipping effects.
At the lower boundary, `s=2,w(121)=-3`, the weight `-2` predecessors give
height `-1`, so no spurious facet survives.  At the upper boundary,
`s=q-1,w(000)=3`, the temporary top `(000,q)` is dominated by `(001,q)`;
all other top clipping agrees directly with `A_(s-1)`.  This proves the
fourth line of (7).

For `q>=4`, the fibre heights for the two wrap calculations are as follows;
an asterisk marks a maximal nonnegative top.

| base | 000 | 001 | 010 | 011 | 020 | 021 | 100 | 101 | 110 | 111 | 120 | 121 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `h_(A_1)` | 3* | 2* | 1* | 0* | 0 | -1 | 1* | -1 | 0 | -1 | 0* | -1 |
| `h_T` | 2* | 1* | 0 | -1 | 0* | -1 | 0 | 0* | 0* | -1 | -1 | -1 |

These rows give `D(A_1)=T` and `D(T)=F_0`.  Applying the same 12-entry
calculation to the short lists (4) gives the first three lines of (7).
For `q=1,2,3`, deleting precisely the displayed out-of-range terms in (4)--
(6) gives the same identities directly.  Thus no induction from numerical
examples is used in (7): it is a finite symbolic antichain calculation with
the small clipping cases included.

The full labelled orbit is therefore

```text
F_0,F_1,F_2,F_3,F_4,F_5,A_(q-1),A_(q-2),...,A_1,T,F_0, (8)
```

where the `A` segment is empty for `q=1`.  There are
`6+(q-1)+1=q+6=m+5` states before the labelled return.

It remains to exclude an earlier return up to isomorphism.  `F_0` is the
graph `B_{3,m}` and contains the triangle `K_3`, while `F_1` is the bipartite
graph `K_{3,m}` with its bridge pair deleted.  Every state from `F_2` through
`T` has a facet of size at least three: this is immediate from (4), while in
the wave one can use `000(s+3)` when it is in range, then `001(s+2)`, and at
the remaining upper endpoint `010q`; in `T`, use `0003`, `0012`, or `1200`
according as `q>=3`, `q=2`, or `q=1`.  None of those states is a graph.
Consequently (8) has no earlier isomorphic return, proving the theorem.

## Exact verification

The checkers require CPython 3.10 or later and no third-party packages.

```bash
python3 verify.py --max-m 300 --direct-max-m 8
python3 independent_check.py --max-m 8
python3 -m unittest -v test_verify.py
```

Expected summary lines:

```text
VERIFIED B_(3,m), m=2..300; type_states=46644; type_transitions=46644; definition_states=70; expanded_facets=4127; NF(B_(3,m))=m+5
INDEPENDENT VERIFIED B_(3,m), m=2..8; full_boolean_states=70; facets_seen_with_multiplicity=4127; labelled_period=m+5; no earlier isomorphic return
```

`verify.py` checks all transitions in (8) in the exact type poset through
`m=300`, expands the predicted type orbits, and separately evaluates the NF
definition on the full Boolean lattice through `m=8`.  The independent
checker reconstructs every dumbbell from its edge definition, uses no orbit
types or closed formula, and reproduces the labelled periods and the
dimension obstruction through `m=8`.  The unit tests exercise the symbolic
transitions, both wave endpoints, all small clipping cases, and the
definition-level expansion.

All arithmetic is exact.  The theorem rests on the symbolic 12-fibre proof
above; computation is corroborative and protects against transcription,
boundary, and convention errors.

## Literature and novelty boundary

- B. A. Rather, *The NF-operator and the NF-Numbers of Simplicial
  Complexes*, Conjecture 3.7,
  [arXiv:2605.30781](https://arxiv.org/abs/2605.30781).  It conjectures the
  general dumbbell formula, proves the first three orbit descriptions, and
  reports exhaustive values only for `2 <= n,m <= 5`.
- T. Hibi and H. Mahmood, *The NF-number of a simplicial complex*,
  [arXiv:2005.01247](https://arxiv.org/abs/2005.01247); Algebra Colloquium
  29 (2022), 643--650.  It proves the analogous `n+m+2` formula for the
  disjoint union of two cliques.

Targeted searches found no proof of the `B_{3,m}` subfamily.  The appropriate
claim is therefore *apparently new to the searched sources*, not a claim of
historical priority.
