# Root-cut codegree constraints for a dense order-24 occurrence in good45

This package proves two symmetry-free second-moment inequalities across the
cut of a degree-24 vertex in a hypothetical `(5,5,45)` graph.  It then applies
them to the complete 15,913-member dense `(4,5,24)` occurrence family together
with the global two-, three-, and four-deck identities.

The result is a useful restriction, but **not** an upper bound for `R(5,5)`:
the strengthened exact relaxation still has a rational feasible point with
paired local edge count `132+100=232`, above the required `225`.  The saved
point is a pseudomodel of the relaxation, not a graph and not evidence that a
good45 exists.

## The cut inequalities

Let `r` have degree 24, put

* `H = G[N(r)]`, of order 24;
* `X = V(G) \\ N[r]`, of order 20;
* `Y = G[X]` and `Q = complement(Y)`;
* `B_u = N_G(u) intersection X`, `c_u = |B_u|`, and
  `j_u = d_H(u)` for `u in H`;
* `T_x = N_G(x) intersection H`, `k_x = |T_x|`, and
  `q_x = d_Q(x)` for `x in X`.

Then every such root cut satisfies

```text
sum_{u in H} C(c_u,2)
    <= sum_{x in X} q_x k_x + 2470 - 29 e(Q),                 (C)

sum_{x in X} C(k_x,2)
    <= 15 e(H) - 1932 + sum_{u in H} c_u (23-j_u).            (R)
```

For (C), double-count `|T_x intersection T_y|`.  If `xy` is an edge
of `Q`, it is a nonedge of `G`; the common `H`-nonneighbours of `x,y`
form a `(4,3)` graph and have order at most 8.  Hence

```text
|T_x intersection T_y| <= k_x + k_y - 16.
```

If `xy` is a nonedge of `Q`, it is an edge of `G`; the common
`H`-neighbours form a `(3,5)` graph and have order at most 13.  Summing
over the `e(Q)` edges and the other pairs gives (C).

For (R), double-count `|B_u intersection B_v|`.  If `uv` is an edge
of `H`, the common boundary neighbours form a `(3,4)` graph and have
order at most 8.  If `uv` is a nonedge, their common boundary
nonneighbours form a `(5,3)` graph and have order at most 13, so

```text
|B_u intersection B_v| <= c_u + c_v - 7.
```

Summing over the 276 pairs in `H` gives (R).  These arguments use only
`R(3,4)=9` and `R(3,5)=14`, plus the forbidden `K5/I5` conditions; no
automorphism is assumed.

The model also uses the shared trace restriction.  Every `T_x` hits all
independent four-sets of `H`, since `H-T_x` cannot contain an independent
four-set.  For each independent triple of `H`, at most four exterior traces
avoid it.  Thus

```text
sum_{x in X} i3(H-T_x) <= 4 i3(H).
```

## Complete-family computation

`dense_joint.tsv` joins every one of the 15,913 published order-24 graphs
with at least 126 edges to its exact four-deck, triangle and independent
triple counts, and degree sequence.  `final_all.txt` supplies the independently
computed independent-four transversal numbers.  The join has 10,874 distinct
linear feature types.  `scan24e126plus.tsv` is the exact four-deck hull used
by the global occurrence model.

`root_linked_fourdeck_lp.py` combines:

* all global degree-20 through degree-24 occurrence counts;
* both orientations of the `m=2,3,4` identities and the mixed degree-four
  identity;
* the exact dense order-24 four-deck hull;
* one distinguished dense root, its exact local degree histogram and
  transversal number;
* a selected order-20 exterior four-deck and degree moments;
* ambient degree and cut-edge consistency;
* the trace and codegree inequalities above; and
* the unique complete order-20, 100-edge catalogue boundary.

With the paired value fixed at 232, the executed model has 35,579 variables,
1,079 equalities, and 11,701 inequalities.  The saved exact point has 95
positive coordinates.  All chosen-root coordinates are integral.  In
particular it selects the 11-regular, 132-edge dense type with transversal
number 10, the unique 100-edge order-20 type, cut allocations

```text
H side: 12 vertices at ambient degree 20,
         4 vertices at ambient degree 21,
         8 vertices at ambient degree 24;
Q side: 2 degree-9 vertices at ambient degree 20,
        14 degree-10 vertices at ambient degree 20,
         2 degree-10 vertices at ambient degree 24,
         2 degree-11 vertices at ambient degree 20,
```

and global degree counts `(30,4,0,0,11)`.  The remaining aggregate deck
coordinates are exact rationals.  Definition-level checking reports zero
equality, inequality, nonnegativity, and requested-integrality failures.

This exact survivor proves only that this relaxation cannot establish the
pointwise bound `e(H)+e(Q)<=225`.  Constraints involving the realized
incidence pattern of the cut, rather than only its margins and codegree
moments, are necessary for closure.

## Verification

Python 3.11, NumPy, and SciPy 1.16 or later are sufficient.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python root_linked_fourdeck_lp.py \
  --fix-root-pair 232 \
  --verify-witness root_pair_integer_root_witness.json
```

Expected final line:

```text
witness_check exact positive 95 equality_failures 0 inequality_failures 0 domain_failures 0 integrality_failures 0
```

To reproduce the solver point (HiGHS is deterministic in the recorded
environment):

```bash
.venv/bin/python root_linked_fourdeck_lp.py \
  --fix-root-pair 232 --integer-root --time-limit 300 \
  --witness reproduced.json
```

## Trust and scope boundaries

Catalogue completeness is imported from McKay--Radziszowski.  The complete
order-24 source has SHA-256
`83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0`.
The extremal archive has SHA-256
`9cfac9dbd1c209cfa342e5d5424df2a7a3fbb008ca00bf0a992e5bbe72f925b6`;
its unique `r4520.100.g6` member is included here.  Classical values
`R(3,4)=9`, `R(3,5)=14`, `R(4,4)=18`, and `R(4,5)=25` are imported.

The global subgraph identities are also imported.  The checker verifies the
saved point against every encoded row exactly over `Fraction`; it does not
certify those imported identities or catalogue completeness.  No numerical
Ramsey bound, occurrence beta bound, or physical order-45 witness is claimed.
