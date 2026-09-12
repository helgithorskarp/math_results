# Every good43 has between 391 and 512 edges

A graph is **good** if it has neither a clique nor an independent set of
order five.  We prove that every good graph `Y` on 43 vertices satisfies

```text
391 <= e(Y) <= 512.
```

The proof imports the classical degree window `18 <= d(v) <= 24` and the
accepted global edge window `390 <= e(Y) <= 513`.  It decides both remaining
boundary classes.  No symmetry, carrier normalization, or fixed graph family
is assumed.

## 1. The overlap inequalities with deficit three

Let `X` be good, put `delta(w)=24-d_X(w)`, and let `uv` be an `X`-edge whose
endpoints both have degree 24.  Suppose the two rooted neighborhood graphs

```text
H_u = X[N_X(u)],   H_v = X[N_X(v)]
```

each have at least 128 edges.  Put

```text
C = N_X(u) intersect N_X(v),  c=|C|,
T = V(X) - (N_X(u) union N_X(v)),  |T|=c-5.
```

Write `d_w=d_C(w)` and `e=e(C)`.  For `i` equal to `u` or `v`, let
`D_i(w)` be the degree of `w` in `H_i`, and define the rooted quantities

```text
P_i = sum_(w in C) D_i(w),
Q_i = sum_(w in C) d_w D_i(w)
      - sum_(wz in E(C)) codeg_(H_i)(w,z).
```

The accepted parent proof derives

```text
P_u + P_v + sum_C delta(w) >= c(29-c)+2e,                    (1)

Q_u + Q_v + sum_C d_w delta(w)
    >= sum_C d_w^2 + (40-c)e.                               (2)
```

The two neighborhood graphs are members of the complete order-24 `(4,5)`
catalog.  Grouping all 24,648 dense rooted occurrences by `c`, the degree
sequence of `C`, and `(P,Q)` gives 6,669 unordered profile pairs.  If
`sum_C delta <= 3`, (1) rejects 5,354 pairs and (2), using
`sum_C d_w delta(w) <= 3 max_C d_w`, rejects another 1,314.

There is exactly one coarse survivor:

```text
c = 11,
degree sequence of C = (3,3,3,3,4,4,4,4,4,4,4),
(P_u,Q_u) = (P_v,Q_v) = (120,358).
```

This survivor is an artifact of grouping nonidentical physical roots by
aggregate data.  There are exactly six rooted occurrences with these data
in the hash-pinned retained catalog.  Their common graphs are mutually
isomorphic and asymmetric, so every ordered pair has one possible common-
graph identification, for 36 physical gluings in all.

For such an identification, define the undepleted required number of
`C`-to-`T` neighbors at `w` by

```text
r_0(w) = 24 - D_u(w) - D_v(w) + d_w.
```

In a physical gluing,

```text
r(w) = |N_X(w) intersect T| = r_0(w)-delta(w) <= |T|=6.
```

Consequently

```text
sum_C delta(w) >= sum_C max(0,r_0(w)-6).
```

The exact 6-by-6 table in `CERTIFICATE.json` has entries only 4 or 5.
Thus every physical realization of the unique coarse survivor requires
common deficit at least four.  This proves:

**Deficit-three overlap lemma.**  If `u,v` are adjacent degree-24 vertices
of a good43 graph, both 24-vertex neighborhood graphs have at least 128
edges, and `sum_(w in N(u) intersect N(v)) delta(w) <= 3`, then a
contradiction follows.

The finite catalog is used only to prove this lemma.  The six occurrences,
all common-graph isomorphisms, and all 36 physical degree requirements are
reconstructed by both supplied implementations.

## 2. Total degree excess six forces five dense normal vertices

Assume for contradiction that `Y` is good and `e(Y)=390`.  Define

```text
delta(v)=d_Y(v)-18,       D=sum_v delta(v)=2*390-43*18=6,
Z={v:delta(v)>0},         F=V(Y)-Z.
```

For `v in F`, put

```text
s_v = sum_(w in N_Y(v)) delta(w).
```

Let `a` be the number of `Y`-edges in the 18-vertex `Y`-neighborhood of
`v`, and let `b` be the number of complement edges in its 24 nonneighbors.
The accepted cross-edge identity gives

```text
a+b = 213+s_v-D/2 = 210+s_v.
```

The imported local extremum `a<=85` therefore gives `b>=125+s_v`.
Call `v` **qualifying** when `s_v>=3`; its complement neighborhood has at
least 128 edges.

Let `H` be the qualifying set.  If `u,v in H` were adjacent in the
complement `X`, both would have `X`-degree 24 and

```text
sum_(w in N_X(u) intersect N_X(v)) delta(w)
    <= D-s_u <= 3.
```

The deficit-three overlap lemma forbids this.  Hence `H` is a clique in
`Y`.

It remains to show `|H|>=5`.  If the positive excesses on `Z` are
`(delta_1,...,delta_z)`, weighted double counting gives the exact identity

```text
S := sum_(v in F) s_v
   = sum_(w in Z) delta(w)(18+delta(w)-d_(Y[Z])(w)).          (3)
```

Because `Y[Z]` is `K5`-free, minimizing (3) over its possible edge sets
gives the following exhaustive table.  The last column is the gap between
the lower bound for `S` and the largest possible upper bound if `|H|<=4`.

| positive excesses | `z` | lower bound for `S` | gap |
|---|---:|---:|---:|
| 1,1,1,1,1,1 | 6 | 88 | 2 |
| 1,1,1,1,2 | 5 | 94 | 6 |
| 1,1,1,3 | 4 | 102 | 12 |
| 1,1,2,2 | 4 | 100 | 10 |
| 1,1,4 | 3 | 114 | 22 |
| 1,2,3 | 3 | 110 | 18 |
| 1,5 | 2 | 128 | 34 |
| 2,2,2 | 3 | 108 | 16 |
| 2,4 | 2 | 122 | 28 |
| 3,3 | 2 | 120 | 26 |
| 6 | 1 | 144 | 48 |

For clarity, the upper bound used in that comparison is elementary.  If
`h=|H|<=3`, nonqualifying vertices contribute at most two and qualifying
vertices at most `D=6`, so

```text
S <= 2(|F|-h)+6h.
```

If `h=4`, then `H` is a `K4`.  No exceptional vertex can be adjacent in
`Y` to all four vertices of `H`, so the weighted contribution from edges
between `H` and `Z` is at most `3D=18`.  Hence

```text
S <= 2(|F|-4)+18.
```

The minimum positive gap in the table is two, so `h<=4` is impossible.
Thus `H` contains at least five vertices, but it is a clique in `Y`, the
final contradiction.

There is no good43 with 390 edges.  Applying the same result to the
complement excludes 513 edges and proves `391 <= e(Y) <= 512`.

## 3. Exact role of computation and trust boundary

`produce.py` uses Boolean adjacency sets and degree-partition permutation
isomorphisms.  `verify.py` imports no producer code; it uses integer bitsets,
a recursive colored-graph isomorphism search, and a different enumeration
of the eleven excess histograms.  Both check all 6,669 coarse pairs, locate
all six physical roots, prove uniqueness of all 36 common-graph
identifications, and verify the excess-six incidence table.  The producer
also enumerates all 33,951 internal exceptional graphs; the verifier
repeats this independently.

The prior accepted edge-window result, the classical degree window,
`R(3,5)<=14`, `R(4,5)<=25`, `U(18)=85`, and completeness of the official
352,366-record order-24 `(4,5)` catalog are imported.  In particular, this
package verifies the hash-pinned 1,027-record dense retained stream but does
not independently regenerate it from the external full catalog.  Catalog
completeness is an explicit finite-data trust boundary.

No solver status, floating-point calculation, automorphism assumption, or
candidate graph is used.  This theorem narrows a universal necessary edge
window; it does not construct a good43 or change the certified Ramsey-number
interval.
