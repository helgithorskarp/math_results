# Small Hall witnesses at the order-15 strong-Seymour frontier

For a vertex `x` of a tournament, put

```text
A = N+(x),  B = N-(x),
Gamma_x(S) = {b in B : s -> b for some s in S}  (S subset A).
```

A vertex is **strong Seymour** when the bipartite directed link from `A` to
`B` has a matching saturating `A`.  It is **ordinary Seymour** when
`|N++(x)| >= |N+(x)|`.

## Theorem

Suppose that a tournament `T` on 15 vertices has no strong Seymour vertex.
If `x` is an ordinary Seymour vertex and `S` is an inclusion-minimal deficient
Hall set at `x`, then

```text
d+(x) = 7  and  4 <= |S| <= 6.
```

The degree assertion is the previously certified order-15 frontier theorem.
The new assertion is the exclusion of `|S|=1,2,3`.

## Local reduction

The earlier frontier theorem gives `delta+(T)=6`, says that `T` is
nonregular, and excludes ordinary Seymour vertices of out-degree six.  Hence
`d+(x)=7`.  Write `A=N+(x)` and `B=N-(x)`.  Since `x` is ordinary and both
shores have size seven,

```text
N++(x) = B.                                      (1)
```

Let `s=|S|` and `R=Gamma_x(S)`.  Inclusion-minimality gives
`|R|=s-1`, and every vertex of `R` has at least two in-arcs from `S`.  Put

```text
C = A \ S,       D = B \ R.
```

Thus `|C|=7-s`, `|D|=8-s`, and every arc between `D` and `S` points from
`D` to `S`.  For `v in S`, define

```text
p(v) = d+_{T[S]}(v),       q(v) = |N+(v) intersect R|.
```

The only possible out-neighbors of `v` lie in `(S\{v}) union R union C`.
The minimum-degree bound therefore gives

```text
p(v) + q(v) >= s-1.                              (2)
```

If equality holds in (2), then `v` dominates all of `C` and has out-degree
exactly six.  By (1), every member of `D` has an in-neighbor in `C` (no
member of `S` sends an arc to `D`).  Consequently

```text
D subset N++(v).                                 (3)
```

This immediately excludes the first two sizes.

- If `s=1`, equality holds and (3) supplies seven second out-neighbors.
- If `s=2`, choose the sink `v` of `T[S]`.  The unique vertex of `R` is
  reached by both members of `S`, so `p(v)=0`, `q(v)=1`, and equality holds.
  The six vertices of `D`, together with `x` reached through `R`, give seven
  second out-neighbors.

In both cases `v` would be an ordinary degree-six vertex, contrary to the
frontier theorem.

Now let `s=3`.  If equality holds in (2) for some `v`, then (3) gives five
second out-neighbors.  If `q(v)>0`, the path through `R` to `x` supplies a
sixth.  If `q(v)=0`, then `p(v)=2`; `v` dominates the other two vertices of
`S`, and double coverage forces both of them to dominate both vertices of
`R`.  Hence both vertices of `R` are second out-neighbors of `v`.  Again `v`
is an ordinary degree-six vertex, a contradiction.

Therefore `p(v)+q(v)>=3` for all three `v in S`.  But

```text
sum_{v in S} p(v) = 3,       sum_{v in S} q(v) <= 6.
```

All inequalities are equalities.  Thus `T[S]` is a directed 3-cycle and
every arc from `S` to `R` points toward `R`.  Up to relabeling, this is one
rigid residue.

## Certified rigid residue

`generate_reduced_cnf.py` imports the exact no-strong-tournament encoding
from `strong_seymour_order15/generate_cnf.py`, selects its normalized
`d7-s3` branch, and adds only:

1. the five clauses expressing (1) on `D`;
2. the directed 3-cycle and all six arcs from `S` to `R`; and
3. three harmless representative arcs under permutations within `C`, `R`,
   and `D`.

The resulting formula has 20,666 variables and 47,347 clauses.  CaDiCaL
3.0.1 proves it UNSAT, and `drat-trim` verifies the 2,527,866-byte binary DRAT
trace.  Exact hashes are recorded in `README.md`.  This excludes the rigid
residue and hence `|S|=3`.

Finally `|S|<=6`, because `S=A` would have `Gamma_x(S)=N++(x)=B` by (1) and
would not be deficient.  Therefore `4<=|S|<=6`, as claimed.

## Scope

This does not prove that every order-15 tournament has a strong Seymour
vertex.  It reduces the unresolved nonregular branch to minimal Hall-witness
sizes four, five, and six at any ordinary root.  The finite step trusts the
inspected base generator, PySAT's cardinality encodings, CaDiCaL, and
`drat-trim`; the checked trace proves UNSAT only for the exact hashed CNF.
