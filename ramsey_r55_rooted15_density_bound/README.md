# A catalog-free density cap for fifteen-vertex rooted sides

Every Ramsey `(4,4;15)` graph has **between 50 and 55 edges**, inclusive.
Both endpoints are attained. This supplies a stronger edge budget for
opposite-colored rooted sides in a Ramsey `(5,5)` graph, with no automorphism,
exceptional-core, degree-profile, or hard-branch assumption.

The density bound is **classical**, not a newly discovered Ramsey theorem:
[McKay's authoritative catalog](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
lists all 640 order-fifteen graphs. The contribution here is a compact exact
proof that does **not trust catalog completeness**, together with an explicit
correction to the campaign's common-root inequality. No additional hard
profile is excluded in this artifact. The inherited campaign accounting
remains 66 global profiles / 271 anchored splits; no target graph is found.

## 1. Finite reduction and completeness

In a Ramsey `(4,4)` graph, every red or blue degree is at most eight:
a red neighborhood is `(3,4)` and a blue neighborhood is `(4,3)`, while
`R(3,4)<=9`. For completeness, `R(3,3)<=6` follows from three same-color
neighbors of any vertex. In a hypothetical `(3,4;9)` graph, every red
neighborhood is independent and has size at most three. Every blue
neighborhood is `(3,3)` and has size at most five. All nine red degrees
would equal three, contrary to the even degree sum. This proves the
only small Ramsey upper bound used here.

For fifteen vertices the red degrees therefore lie in `[6,8]`. If the
graph had at least 56 edges, its average degree would exceed seven, so
choose a vertex v of degree eight. Write H for its eight red neighbors
and B for its six blue neighbors. Then H is `(3,4;8)` and the complement
of B is `(3,4;6)`.

[census.py](census.py) regenerates all labeled `(3,4)` graphs through
order eight. Upon appending a vertex, its red neighborhood must be an
independent set of size at most three, and must meet every old independent
triple. These conditions are necessary and sufficient. Every graph has
one unique labeled predecessor, so there is neither omission nor duplicate
generation. The counts for orders zero through eight are

```text
1, 1, 2, 7, 40, 322, 2812, 13842, 17640.
```

A separate all-edge-assignments check compares the complete labeled sets
through order six. Full vertex-permutation orbits partition the six- and
eight-vertex sets, leaving fifteen and three types respectively. This reuses
the proven augmentation method of the
[ten-edge-cell artifact](../ramsey_r55_ten_edge_cell_obstruction), but the new
directory is self-contained and reads no sibling source or graph catalog.

All `3*15=45` rooted side pairs are tested. H and B may be relabeled
independently because every cross-edge matrix is left free. There is no
assumed automorphism of a completed graph and no symmetry-breaking omission
inside the cross search. Masks use least-significant-bit-first lexicographic
unordered edge pairs; the six-vertex mask denotes **the complement of B**.

For a row T_i of the eight-by-six red cross matrix, the necessary degrees are

```text
6 <= 1 + d_H(i) + |T_i| <= 8,
6 <= d_B(b) + |{i:b in T_i}| <= 8.
```

The total cross-edge requirement is

```text
sum_i |T_i| >= 56 - 8 - e(H) - e(B).
```

The exact searches enforce these rows and every monochromatic four-set.
The side types handle four-sets entirely inside H or B and those containing
v. The remaining sets have one, two, or three vertices in H:

- One H vertex: its red cross neighbors cannot contain a red B triangle;
  its blue cross neighbors cannot contain a blue B triangle.
- Two H vertices: their common cross neighbors in the color of their H
  edge cannot contain a B edge of that color.
- Three H vertices: H has no red triangle. For every blue H triangle,
  the union of its three red cross rows must cover B.

[fast_search.py](fast_search.py) uses these predicates, dynamically chooses
a row with smallest current domain, and propagates pair/triple constraints
to all remaining rows. It also uses rigorous column bounds and an upper
bound on attainable cross-edge count. Every remaining row value is branched
on; there is no timeout, heuristic rejection, memoization, or solver.
All 45 cases have zero completions, in **1,324,165 search nodes**.

[literal_search.py](literal_search.py) uses a different encoding and
traversal. It inspects all `C(15,4)=1365` literal four-sets, substitutes fixed
side/root edges, and compiles each remaining forbidden monochromatic
assignment into cross-edge clauses. A fixed natural-row traversal checks
these clauses with degree and total-edge bounds, without forward domain
propagation. It shares the small-type census but imports no production
clique predicates. Its case-by-case results are in
[literal_report.json](literal_report.json).

The literal traversal finishes all cases with **11,006,524 nodes** and no
completion. It took approximately thirteen minutes in the shared environment,
with observed peak resident memory 22,440 KiB. The full ordered case keys,
row-domain sizes, cross-edge thresholds and empty completion sets agree
between the two reports. The separately run original static prototype
also completed all 45 cases without a survivor; it is supplementary evidence,
not an extra independent encoding.

Thus no graph with 56 or more edges exists. Complementation gives the
lower endpoint `C(15,2)-55=50`.

An immediate, non-sharp consequence also costs no new enumeration: every
`(4,4;16)` graph has 58--62 edges. Sum the fifteen-vertex upper bound over
all sixteen vertex deletions: `14e<=16*55=880`, hence `e<=62` by integrality;
complementation gives `e>=120-62=58`. This is not a classification at order
sixteen and carries no optimality claim.

## 2. A sharper non-symmetric common-root budget

Let G have neither a red nor a blue K5. Choose distinct roots z,w and
C disjoint from them, with

```text
J = N_R(z) intersect C,       K = N_R(w) intersect C,
P = J\K, Q = K\J, U = J intersect K, c = |U|.
```

Choose any `F_z subset N_R(z) intersect N_B(w)` outside C and excluding
the roots; define F_w with z,w interchanged. Both `P union F_z` and
`Q union F_w` are `(4,4)` graphs. Write

```text
p=|P|, f=|F_z|, D_z=e_R(P,F_z), E_z=e_R(F_z).
```

The former maximum-degree bound was `2e_R(P)<=8p-D_z`. Whenever `p+f=15`,
the new density interval gives

```text
50-D_z-E_z <= e_R(P) <= 55-D_z-E_z,
2e_R(P) <= 8p-D_z-delta_z,
delta_z = max(0, 8p+D_z+2E_z-110).                       (1)
```

If `p+f!=15`, set delta_z=0 and retain only the old maximum-degree bound;
do **not** apply the displayed 50--55 interval at another order. Define
delta_w and D_w analogously for Q and F_w.

Optionally, when `p+f=16`, the averaging corollary permits
`58-D_z-E_z<=e_R(P)<=62-D_z-E_z` and
`delta_z=max(0,8p+D_z+2E_z-124)` instead. For the full induced rooted side,
the sum of deficits from degree eight is at least ten at order fifteen
and at least four at order sixteen. These are linear density constraints,
not assertions that either side has a regular graph realization.

For each u in U, its red neighbors in P are red to the red edge zu and
blue to w. They form a `(3,4)` graph, so `d_P(u)<=8`; similarly
`d_Q(u)<=8`. Consequently the exact edge decomposition yields

```text
2e_R(J)+2e_R(K)
 <= 8(|P|+|Q|) - D_z-D_w - delta_z-delta_w
    + 32c + 2c(c-1).                                   (2)
```

Indeed `e(J)+e(K)=e(P)+e(Q)+e(U,P)+e(U,Q)+2e(U)`; apply (1),
`e(U,P),e(U,Q)<=8c`, and `e(U)<=c(c-1)/2`. No color is assumed for zw.
This refines the previously proved
[common-root inequality](../ramsey_r55_common_neighbor_squeeze).

For the frequently encountered `p=14,f=1,D_z=8` case, delta_z=10:
the upper bound on twice e(P) drops from 104 to 94. The integer scalar
assignment `e(P)=48` passes the former bound but violates the new one.
This is a strict separation of **necessary scalar relaxations**, not a
claim that the old scalar assignment was graph-realizable. The verifier
checks the minimum/positive-part identity in (1) for all 17,880 elementary
parameter combinations with p+f=15.

## 3. Reproduction and evidence limits

Using Python 3.11.2 and its standard library, from this directory:

```bash
python3 verify.py --report /tmp/density15.json
cmp report.json /tmp/density15.json
python3 -O verify.py --report /tmp/density15-O.json
cmp report.json /tmp/density15-O.json
python3 verify.py --engine literal --report /tmp/density15-literal.json
cmp literal_report.json /tmp/density15-literal.json
python3 compare_reports.py /tmp/density15.json /tmp/density15-literal.json
python3 audit_small.py
python3 -O audit_small.py
sha256sum -c SHA256SUMS
```

An additional, slower static traversal using the original mixed-clique
predicates is retained in [reference_search.py](reference_search.py):
`python3 verify.py --engine reference --report /tmp/density15-reference.json`.
It is a reference implementation, not a third independent proof encoding.

The final main runs took 52.393 seconds normally and 52.661 seconds under -O,
with peak child resident memory at most 24,820 KiB, while other local proof
checks were running. Their reports agree byte for byte. Timings are not
included in the deterministic report. A full literal replay is slower;
`--progress` optionally emits one completed-case line at a time.

Both main engines are compared on the **complete set of 82 labeled cross
matrices** for a four-regular nine-vertex rook-graph split; every model is
decoded and checked by literal four-set enumeration. Both also find a
55-edge completion of a fixed fifteen-vertex split. The original static
reference passes these positive controls as well. The complete mixed-four-set
predicate truth tables are audited separately. Invalid threshold and K4
examples are rejected; explicit exceptions keep all checks active under -O.

[audit_small.py](audit_small.py) additionally checks all 64 cross matrices
of a small asymmetric root split, in 192 degree-interval/edge-threshold
cases. All three engines must equal the complete sets obtained by literal
graph checking, including empty and nonempty boundaries. It also checks
all 121 possible order-sixteen edge counts against the averaging inequalities.

[sharp15.edges](sharp15.edges) is an explicitly checked 55-edge graph;
its complement has 50 edges. It was decoded from zero-based record 49,
`N@MrQqJT[nMRjLqR{uG`, of McKay's
[order-fifteen file](https://users.cecs.anu.edu.au/~bdm/data/r44_15.g6)
(file SHA256 `53a46ba21cb16805eb07775b60746f783864388538368955e72cbdae5ae8f4e1`).
Only the small literal edge list is an input. Neither the file nor its
claimed completeness is required to reproduce the theorem or sharpness.

This is an internally cross-checked exact computation, not a formal proof
or an independent peer review of this new artifact. Trust boundaries are
the unformalized reduction and elementary Ramsey argument, source correctness,
the shared small-type census, Python exact-integer semantics, and hardware.
No SAT/UNSAT verdict, floating arithmetic, nauty, external data completeness,
or omitted proof trace is used. The classical density cap carries no novelty
claim. A future pass should apply (1)--(2) to a genuinely remaining asymmetric
profile; that further feasibility phase is not included here.
