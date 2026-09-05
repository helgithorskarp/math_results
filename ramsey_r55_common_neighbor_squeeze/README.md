# Common-root capacities leave one double-degree-19 cell pattern

The hard-branch profile `19^2 20^3 21^38` now has just **one normalized
central cell-size pattern**, instead of seven:

```text
|U|=2, |W|=8,
(|A_2|,|A_3|,|A_4|)=(4,2,8),
(|B_2|,|B_3|,|B_4|)=(4,8,2).
```

Moreover U is a red edge, and each of its endpoints has exactly 8, 8,
and 2 red neighbors in P, Q, and W respectively. The two induced graphs
`P union {4}` and `Q union {3}` must each be **eight-regular `(4,4)`
graphs on 15 vertices**. These are necessary structures, not constructed
graphs or assertions that such structures can be glued together.

The new proof is an elementary common-root degree bound. It applies to
both remaining W types, not just the eleven-edge type that motivated the
experiment. Combined with the preceding ten-edge exclusion, the number
of normalized pattern/W-type templates drops from **14 to 2**. No whole
degree profile, anchored split, or target graph is resolved. The inherited
global counts remain **67 profiles / 273 anchored splits**.

## 1. A common-neighbor lemma and strengthened paired bound

Let G have no red or blue K5. Choose distinct roots z,w and a set C
disjoint from them, and partition C as

```text
J=N_R(z) intersect C,       K=N_R(w) intersect C,
P=J\K,   Q=K\J,   U=J intersect K,   W=C\(J union K).
```

No color is assumed for zw. For every `u in U`,

```text
d_P(u)<=8,                d_Q(u)<=8.                     (1)
```

Indeed `N_R(u) intersect P` is red to both endpoints of the red edge zu
and blue to w. It has no red triangle (which would extend zu to a red K5)
and no blue four-clique (which would extend w to a blue K5). It therefore
has at most eight vertices by `R(3,4)<=9`. Interchanging z,w proves the
other bound. This argument does not require u to belong to the pool P;
it is precisely the additional root missing from the earlier cell-only
degree constraints.

For completeness, the elementary bound `R(3,3)<=6` follows by considering
three same-color neighbors of any vertex. If a triangle-free graph on nine
vertices had no independent four-set, every red neighborhood would have
size at most three. Every blue neighborhood would have neither a triangle
nor an independent triple, so would have size at most five. Every red
degree would consequently equal three, contradicting the odd degree sum
27. This proves the bound used in (1) without a catalog.

Writing `c=|U|`, (1) implies the useful leakage inequality

```text
d_W(u) >= d_(G[C])(u)-16-(c-1).                          (2)
```

It also strengthens the preceding paired-neighborhood bound. Choose
`F_z subset N_R(z) intersect N_B(w)` and
`F_w subset N_R(w) intersect N_B(z)`, both outside C and excluding the
roots, and put

```text
D=e_R(P,F_z)+e_R(Q,F_w).
```

Then

```text
2e_R(J)+2e_R(K)
 <= 8(|P|+|Q|)-D+32c+2c(c-1).                           (3)
```

To prove it, `P union F_z` and `Q union F_w` each have no red or blue
four-clique. Their red degrees are at most eight, giving

```text
2e_R(P)+2e_R(Q)<=8(|P|+|Q|)-D.
```

Now use the exact decomposition

```text
e_R(J)+e_R(K)=e_R(P)+e_R(Q)+e_R(U,P)+e_R(U,Q)+2e_R(U),
```

together with `e_R(U,P),e_R(U,Q)<=8c` from (1), and
`e_R(U)<=c(c-1)/2`. This proves (3). The old degree-budget bound and
(3) are complementary bounds, not an assertion that one dominates the
other for every graph. The cap eight in (1) is attained by a literal
11-vertex Ramsey fixture in the verifier; (3) is not claimed sharp.

## 2. Apply the squeeze to the seven inherited patterns

The [paired-neighborhood artifact](../ramsey_r55_paired_neighborhood_budget/README.md)
reduces the specified hard-branch profile to the exceptional core E on
`0,...,4` with red edges

```text
01,02,04,12,13,23,24.
```

The central set C consists of the 38 degree-21 vertices. Let z=0,w=1,
`F_z={4}`, `F_w={3}`. The central cells are

```text
U: red to {0,1}, size 2;
W: red to {2,3,4}, size 8;
A_i: red to {0,i}; B_i: red to {1,i}, i=2,3,4.
P=A_2 union A_3 union A_4; Q=B_2 union B_3 union B_4.
```

These are exact signatures on E; all unlisted E incidences are blue.
In particular `|P|=|Q|=14`, and every U vertex has degree 19 in C.
The inherited seven possibilities are

```text
A=(a,b,14-a-b), B=(8-a,10-b,a+b-4),
3<=a<=5, 2<=b<=4, 6<=a+b<=8.
```

Here `D=|A_4|+|B_3|=24-a-2b`. The two exact exceptional local red
edge counts, each 85, give

```text
e_R(J)+e_R(K)=154-D.                                    (4)
```

This is also checked by the full parent replay. Combining (3) and (4),

```text
308-2D <= 8*28-D+32*2+2*2*(2-1)=292-D,
so D>=16.                                              (5)
```

Of the seven patterns, only `(a,b)=(4,2)` has `D>=16`, and it has D=16.
An equivalent derivation preserves the leakage interpretation. Set

```text
S_P=112-|A_4|-2e_R(P)>=0,
S_Q=112-|B_3|-2e_R(Q)>=0.
```

The U degree sum and (4) give the exact slack identity

```text
S_P+S_Q+2e_R(U,W)=D-8.                                  (6)
```

By (2), each U vertex needs at least two red neighbors in W, so
`e_R(U,W)>=4`. Equation (6) again gives D>=16. The finite comparison is:

| A sizes | D | Previous upper bound on `e_R(U,W)` | New lower bound | Survives |
|---|---:|---:|---:|---|
| 3,3,8 | 15 | 3 | 4 | no |
| 3,4,7 | 13 | 2 | 4 | no |
| 4,2,8 | 16 | 4 | 4 | yes |
| 4,3,7 | 14 | 3 | 4 | no |
| 4,4,6 | 12 | 2 | 4 | no |
| 5,2,7 | 15 | 3 | 4 | no |
| 5,3,6 | 13 | 2 | 4 | no |

This is a unique pattern in the normalized core labeling. It is not a
claim that G has the core's relabeling symmetry or any automorphism.

## 3. Equality forces two regular rooted sides

For D=16, equality holds in (3). All its slack terms are nonnegative,
so all vanish. Consequently

```text
e_R(U)=1,
d_P(u)=d_Q(u)=8 and d_W(u)=2 for each u in U,
e_R(P)=e_R(Q)=52,
d_(P union {4})(v)=8 for every v in P,
d_(Q union {3})(v)=8 for every v in Q.
```

Vertex 4 is red to the eight vertices of A_4 in P, and vertex 3 is red
to the eight vertices of B_3 in Q. Thus the two rooted sides really are
eight-regular on 15 vertices, with 60 red edges each. Their `(4,4)`
property follows from their uniform opposite-colored joins to roots 0,1.
In terms of the original sides alone, A_4 and B_3 vertices have side
degree seven, and all other P/Q vertices have side degree eight.
Also `{0,1} union U` is a red K4.

The [ten-edge-cell obstruction](../ramsey_r55_ten_edge_cell_obstruction/README.md)
still applies. W must have 11 or 12 red edges. If `k=e_R(W)`, the central
degree sums now fix several further aggregate counts:

```text
e_R(U,P)=e_R(U,Q)=16, e_R(U,W)=4,
e_R(P,W)=e_R(Q,W)=70-k,
e_R(P,Q)=76+k.
```

For example the W degree sum is
`144=2k+4+e_R(P,W)+e_R(Q,W)`. The equal P/Q degree sums force equal
W incidences, and `266=104+16+e_R(P,Q)+e_R(P,W)` finishes the calculation.

## 4. Exact positive boundary and verification

[EDGE_WITNESSES.json](EDGE_WITNESSES.json) gives two integer vectors, one
with k=11 and one with k=12. Variables are the 36 unordered cell pairs,
including diagonals, in lexicographic combinations-with-replacement order
on cell masks `(3,5,6,9,10,17,18,28)`. All parent boxes and **153 two-sided
rows** are checked, together with **11 new equality rows**: six saturated
P/Q cell degree sums, the U edge, U--P/Q/W totals, and the specified W
edge count. Thus both scalar k alternatives survive this strengthened
aggregate relaxation.

These vectors are **not** individual-edge assignments, actual critical-W
realizations, actual eight-regular rooted-side graphs, full core-signature
primals, or solutions of central triangle-count constraints. In particular
the individual endpoint incidences `8/8/2` and 15-vertex regularity are
proved necessary above but only their stated aggregate consequences enter
the witness system. No feasibility claim goes beyond that system.

[verify.py](verify.py) uses the standard library and explicit exceptions.
It replays the complete pinned paired and ten-edge parents, including the
critical-W classification, then audits the new identities and witnesses.
It also tests the common-root lemma and strengthened bound on every root
pair and remaining-set choice of every Ramsey graph on five labeled
vertices, and 5,814 partitions of a directly checked 19-vertex Ramsey
fixture. A separate 11-vertex fixture attains the root cap eight. Four
negative tests reject cap seven, omission of the Ramsey hypothesis,
erasure of the forced U edge, and the old weaker retained-pattern witness.
These finite tests support implementation correctness; the universal
theorem is proved in sections 1--3, not inferred from those tests.

Numerical one-vertex extension LPs suggested (1); their separators reduced
to the two elementary mixed-root inequalities. No numerical infeasibility
status, branch sweep, or opaque solver proof is used in the theorem.
Optional [find_witnesses.py](find_witnesses.py) uses NumPy 2.2.6 and SciPy
1.15.3's bundled HiGHS, with 20 seconds per MILP, solely to discover the
two primals. Its rounded outputs are accepted only after exact integer
checking. Discovery can produce other valid vectors; uniqueness is not
asserted. The checked vectors, not solver termination, establish the
positive aggregate boundary.

From this directory, with Python 3.11.2:

```bash
python3 verify.py --report /tmp/r55_common_root.json
cmp report.json /tmp/r55_common_root.json
python3 -O verify.py --report /tmp/r55_common_root_optimized.json
cmp report.json /tmp/r55_common_root_optimized.json
sha256sum -c SHA256SUMS
```

Compare stdout with [EXPECTED_OUTPUT.txt](EXPECTED_OUTPUT.txt).
The full normal replay took 10.444 seconds and 26,168 KiB peak child RSS
on the research host; optimized-mode output and the complete report match.
The source hashes of both immediate parent verifiers are pinned in code;
their own checks carry the earlier certificate dependencies. No new
external dataset is needed. The general lemma uses only elementary Ramsey
bounds. The campaign corollary imports the parent core/profile reduction,
exact exceptional local counts, and reviewed local-extremal inputs.
The parent reductions and this new result are unformalized; no independent
peer review of this contribution is claimed. Exact Python execution,
the imported proof/certificate chain, and hardware remain trust boundaries.
No novelty claim is made for the elementary rooted Ramsey argument.

## Checkpoint and next direction

This pass ends at the one-pattern reduction. No background search is left
running. The best next structural frontier is compatibility of the two
forced eight-regular 15-vertex `(4,4)` sides, the adjacent U vertices, and
the two remaining critical-W types. Their actual realizations have not
been enumerated or excluded here. This is separate from the teammate's
automorphism/structured-construction lane and the parked catalog-radius
lane. The M=214 whole-stratum formulation concerns another degree profile
and is neither rerun nor strengthened by this result.
