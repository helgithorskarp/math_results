# Proof certificate and logical scope

Write `B` for the labelled 516-vertex source and `Q=H632-H560`, so `|Q|=72`.
For each `q` in `Q`, define

```text
C(q) = {v in B : B-v+q is four-colourable}.
```

The checker establishes the following finite statement solely through
explicit proper colourings:

```text
for every q in Q, |C(q)| >= 508.
```

It also establishes that `B-v` is four-colourable for every `v in B`.

Let `J` be any subgraph of the strict geometric graph on `B+q`, with
`|V(J)|<=508`. If `q` is absent, then at least one `v in B` is absent and the
colouring of `B-v` restricts to `J`. If `q` is present, at least
`516-507=9` base vertices are absent. The complement `B-C(q)` has size at most
eight, so some absent `v` belongs to `C(q)`. The colouring of `B-v+q` then
restricts to `J`. Thus every such `J` is four-colourable.

This is a positive-witness proof. Solver completeness, an UNSAT answer, the
five-chromaticity of `B`, and the vertex-criticality of `B` are not logical
premises. The last two facts explain why the family is target-bearing.

For `q in H560-B`, the previously published full H560 closure gives the same
conclusion immediately. Hence the new 72-point theorem and that imported
44-point case decide all `q in H632-B`.

## Certificate layout

`base_vertices` and `outside_points` use H632 labels. For a deletion row with
label `v`, unpack the two-bit colour stream against `sorted(B-{v})`. Multiple
rows may have the same deleted label. For a direct row `(q,v)`, unpack against
`sorted((B-{v}) union {q})`.

Every stream is canonical Base64 with zero high padding bits. The checker
validates all domains, every induced unit edge, row uniqueness, source hashes,
and exact support identities before using a colouring for coverage.
