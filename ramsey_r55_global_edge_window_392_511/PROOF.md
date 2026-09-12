# Every good graph on 43 vertices has between 392 and 511 edges

A graph is **good** if it has neither a clique nor an independent set of
order five.  We prove that no good graph on 43 vertices has 391 edges.
Complementation also excludes 512 edges.  Together with the accepted parent
window `391 <= e(G) <= 512`, this gives

```text
392 <= e(G) <= 511.
```

No automorphism, carrier, partition, or structured graph family is assumed.

## 1. The global excess join

Assume that `Y` is good and `e(Y)=391`.  The classical degree window is
`18 <= d_Y(v) <= 24`.  Put

```text
delta(v) = d_Y(v)-18,       sum_v delta(v)=8,
Z = {v: delta(v)>0},        F = V(Y)-Z.
```

For `v in F`, define

```text
s_v = sum_(w in N_Y(v)) delta(w).
```

Let `a=e(Y[N_Y(v)])`, and let `b` be the number of complement edges on the
24 nonneighbors of `v`.  The cross-edge identity is

```text
a+b = 213+s_v-8/2 = 209+s_v.
```

The imported exact local extremum `a<=85` therefore gives `b>=124+s_v`.
Call `v` qualifying if `s_v>=3`; its 24-vertex neighborhood in
`X=complement(Y)` is a `(4,5;24)` graph with at least 127 edges.

There are at least five qualifying vertices.  Indeed, if the positive
excesses are `delta_1,...,delta_z`, weighted double counting gives

```text
S := sum_(v in F) s_v
   = sum_(w in Z) delta(w)(18+delta(w)-d_(Y[Z])(w)).          (1)
```

Using only `d_(Y[Z])(w)<=z-1`,

```text
S >= 8(19-z) + sum_i delta_i^2.
```

If at most four vertices qualify, every other `s_v` is at most two and
every qualifying `s_v` is at most eight, so

```text
S <= 2(43-z)+24.
```

The lower bound exceeds this upper bound by

```text
42-6z+sum_i delta_i^2 >= 42-6z+8 >= 2,
```

because `z<=8` and every positive integral excess satisfies
`delta_i^2>=delta_i`.  Thus at least five vertices qualify.

## 2. Endpoint overlap theorem

The finite computation proves the following unrestricted local statement.

**Endpoint overlap theorem.**  Let `X` be a good graph on 43 vertices with
512 edges.  There do not exist adjacent degree-24 vertices `u,v` such that
both neighborhood graphs `X[N_X(u)]` and `X[N_X(v)]` have at least 127
edges and

```text
sum_(w in N_X(u) intersect N_X(v)) (24-d_X(w)) <= 5.         (2)
```

Here is the complete finite proof of that theorem.

For an edge `uv`, put

```text
C=N_X(u) intersect N_X(v), c=|C|,
T=V(X)-(N_X(u) union N_X(v)), t=|T|=c-5.
```

The common graph `X[C]` is triangle-free.  Write `d_w=d_C(w)`, `e=e(C)`,
and, for `i` equal to `u` or `v`, let `D_i(w)` be the degree of `w` in the
rooted neighborhood graph `H_i=X[N_X(i)]`.  Define

```text
P_i = sum_(w in C) D_i(w),
Q_i = sum_(w in C) d_w D_i(w)
      - sum_(wz in E(C)) codeg_(H_i)(w,z).
```

With `epsilon(w)=24-d_X(w)` and `r_w=|N_X(w) intersect T|`, exact degree
counting gives

```text
r_w = 24-epsilon(w)-D_u(w)-D_v(w)+d_w.
```

Summing `r_w<=t` and summing the pair-intersection bound on every edge of
`C` give the necessary inequalities

```text
P_u+P_v+sum_C epsilon(w) >= c(29-c)+2e,                    (3)

Q_u+Q_v+sum_C d_w epsilon(w)
    >= sum_C d_w^2+(40-c)e.                                (4)
```

For (4), an edge in a good graph has at most 13 common neighbors, by
`R(3,5)=14`, and two subsets of `T` of sizes `r_w,r_z` intersect in at
least `r_w+r_z-t` elements.

The complete published `(4,5;24)` catalogue has 352,366 graphs.  Its pinned
SHA256 is

```text
83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0.
```

Exactly 4,428 catalogue graphs have at least 127 edges, giving 106,272
rooted occurrences.  Grouping by `c`, the degree sequence of `C`, and
`(P,Q)` produces 20,388 unordered profile pairs.  Equations (3) and (4),
using total deficit at most five, reject 20,187 and leave 201 coarse pairs.

The physical layer reconstructs every relevant rooted graph and every
actual common-graph isomorphism.  The 4,330 relevant roots form 28 exact
common-graph isomorphism classes.  Across 112,640 unordered rooted pairs,
86,040 have isomorphic common graphs, with 698,368 physical isomorphisms.
For each isomorphism the program enumerates all nonnegative deficit vectors
of total at most five (at most 6,188 vectors), checks `0<=r_w<=t`, (3), (4),
and every individual `R(3,5)` pair-intersection cap.  Exactly 330 physical
maps survive; 698,038 are rejected.

Direct two-color unit propagation on all forbidden five-sets among the 37
vertices fixed by the two rooted neighborhoods contradicts 298 of the 330
maps, independently of the deficit vector and of all edges meeting `T`.
The other 32 maps admit exactly 52 deficit vectors.  Explicit `C`-to-`T`
row witnesses verify that no necessary branch was lost at this join.

For each of the 52 remaining branches, a physical Boolean formula has one
variable for every edge of the 43-vertex graph and asserts:

* the two literal rooted neighborhood graphs and their common identification;
* every exact degree `24-epsilon(w)` for `w in C`;
* degree 18 through 24 for every other vertex;
* exactly 512 edges; and
* both forbidden-five clauses for every five-subset.

Every formula is UNSAT.  CaDiCaL 1.9.5 emitted a DRAT proof for each branch.
DRAT-trim reduced these to 52 cores containing 1,597 input clauses in total
and 1,413 trimmed proof lines.  The largest core has 147 clauses.  The
checker regenerates each full formula, confirms that every core clause is a
literal input clause, and independently verifies every trimmed proof against
its core.  Therefore all 330 maps are impossible, proving the endpoint
overlap theorem.

## 3. Finishing the global contradiction

Let `u,v` be qualifying vertices.  They have degree 24 in `X`.  If they
were adjacent in `X`, both neighborhood graphs would have at least 127
edges.  Moreover `C=N_X(u) intersect N_X(v)` is disjoint from `N_Y(u)`, so

```text
sum_(w in C) (24-d_X(w))
 = sum_(w in C) delta(w) <= 8-s_u <= 5.
```

The endpoint overlap theorem forbids this.  Thus all qualifying vertices
form a clique in `Y`.  Section 1 supplies at least five of them, contradicting
that `Y` is good.  Hence 391 edges are impossible.  Complementation excludes
512 edges and proves the stated window.

## Trust boundary and scope

Imported results are the prior certified window `391<=e(G)<=512`, the
classical degree window, `R(3,5)=14`, `R(4,5)=25`, the exact local extremum
`U(18)=85`, and completeness of the published 352,366-record `(4,5;24)`
catalogue.  The source catalogue is hash-pinned but not redistributed here.

The new work is a complete physical overlap enumeration and 52 checked SAT
certificates.  NetworkX is used for exact graph isomorphism enumeration,
NumPy only for Boolean filtering of an explicitly generated integer table,
and PySAT only to generate deterministic cardinality encodings.  The final
UNSAT claims do not trust solver status: their stored DRAT proofs are checked.
Residual trust includes the written covering argument, catalogue provenance,
the supplied programs and proof checker, Python/C implementations, the OS,
and hardware.  No good43 is constructed and the exact value of `R(5,5)` is
not determined.
