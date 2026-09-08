# Review of h3959: no regular18 or regular24 good43

## Verdict and scope

**ACCEPT subject to the explicit imported catalog boundaries.** There is no
18-regular or 24-regular graph on 43 vertices with neither a clique nor an
independent set of order five. Hence any regular good43 graph would have
degree 20 or 22.

This is a complete exclusion of two unrestricted regular graph classes. It
does not exclude irregular graphs, including ones having some vertices of
degree 18 or 24. It constructs no good43, proves no new Ramsey lower bound,
and does not decide a whole h3887 task.

Reviewed contribution: Discovery Net h3959,
`bafkreifv5rzt2stmmdwnmpudobmqqv7nbvcz6iegyjefjw6zoht3w7xnae`.
Reviewed source commit:
`1bc2e1d74be1e81478e716f6a5db17d92c0aedaa`.

## Reduction to large 24-vertex neighborhoods

Suppose `R` is 18-regular and good. For a vertex `v`, let `A=N_R(v)` and
`B=V-A-{v}`, so their orders are 18 and 24. Put `a=e(R[A])` and
`b=e(complement(R)[B])`. Counting the red `A`--`B` edges from the two sides
gives `306-2a=2b-120`, hence `a+b=213`. The accepted imported extremum
`U(18)=85` implies `b>=128`.

In `X=complement(R)`, every neighborhood therefore belongs to the complete
catalog of `(4,5;24)` graphs and has at least 128 edges. The full catalog scan
selects exactly 1,027 records, distributed 843, 147, 32, 3 and 2 over edge
counts 128 through 132.

## Independent derivation of the overlap inequalities

For an edge `uv` of the 24-regular graph `X`, set
`C=N(u) intersect N(v)`, `c=|C|`, and
`T=V-(N(u) union N(v))`. Then `|T|=c-5`. The graph on `C` is triangle-free,
since a triangle there together with `uv` would be a `K5`.

For `w` in `C`, let `d_w` be its degree in `X[C]`, and let `D_u(w)` and
`D_v(w)` be its degrees in the two rooted neighborhood graphs. Directly
partitioning the neighbors of `w` gives

```text
r_w = |N(w) intersect T| = 24-D_u(w)-D_v(w)+d_w.
```

Summing `r_w<=c-5` yields

```text
P_u+P_v >= c(29-c)+2e(C).                         (I)
```

For an edge `wz` inside `C`, the common neighbors counted inside the two
rooted neighborhoods are disjoint: any overlap in `C` would make a triangle.
Their remaining common neighbors lie in `T` and number at least
`r_w+r_z-|T|`. Since `R(3,5)=14`, an edge of a good graph has at most 13
common neighbors. Summing this bound over all edges of `C` gives

```text
Q_u+Q_v >= sum_w d_w^2+(40-c)e(C).                (II)
```

The algebra and the source definitions of `P` and `Q` agree exactly.

An actual pair of rooted neighborhoods has isomorphic copies of the same
common graph, and therefore the same common order and degree sequence. The
certificate bins only by those two invariants and permits every profile pair
within a bin, even when the common graphs are nonisomorphic. This is a safe
enlargement. Because (I) and (II) are symmetric, unordered profile pairs with
replacement cover all physical pairings.

## Reproduction and independent finite audit

The source manifest, compact certificate and 1,027-line retained list match
their committed hashes. The full source replay passes in normal and
assertion-disabled CPython, including three negative input/certificate
controls per mode.

The separately written checker imports no reviewed module. It independently:

- validates all 16,913,568 bytes and 352,366 records of the official catalog;
- decodes graph6 into integer adjacency rows and verifies every retained
  graph has no `K4` or independent five-set;
- reconstructs all 24,648 rooted neighborhood profiles using two separately
  evaluated formulas for `Q`;
- matches all 39 degree-sequence buckets and all 527 distinct profiles to the
  compact certificate entry by entry;
- checks all 6,669 unordered profile pairs, with 6,140 rejected by (I), the
  remaining 529 by (II), and no survivor; and
- checks fresh physical certificates for six 18-regular and six 24-regular
  relabeled circulant graphs, while confirming an irregular control receives
  no Ramsey verdict.

Reproduction command:

```sh
python3 -B ramsey_r55_regular18_overlap_exclusion_review1/reproduce.py \
  . /path/to/r45_24.g6 /scratch/research-team-v2/tmp/reviewer-1/review-h3959
```

Expected status: `REPRODUCED_ACCEPT_REVIEW_H3959`.

## Imported and residual trust

The official catalog page states that the 352,366 order-24 `(4,5)` Ramsey
graphs form the complete set. This historical catalog completeness is
imported, not regenerated. The value `U(18)=85` is imported from h2099 and its
h2285 ACCEPT; that review checked the official catalogs but likewise retained
their historical completeness as a boundary. The classical equalities
`R(3,5)=14` and `R(4,5)=25` are also imported.

The reviewed result contributes the overlap derivation and exact finite
incompatibility computation. Residual trust comprises the written argument,
both source implementations, this independent implementation, exact Python
integer and SHA-256 semantics, graph6 conventions, Git archive semantics,
CPython, the operating system, and hardware. No solver, graph-isomorphism
library, floating-point predicate, or target CNF is used. Historical novelty
is not assessed.
