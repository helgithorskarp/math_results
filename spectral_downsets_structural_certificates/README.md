# Exact structural certificates for spectral downsets

**Agent:** six-downset-1. **Role:** researcher. **Date:** 2026-09-30.

[PROOF.md](PROOF.md) derives exact rational Hoffman certificates and
transport rules for Conjecture H. It proves the infinite rank-two subclass,
and product closure when factor certificates also have maximum eigenvalue
at most one. Balanced certificates establish this extra condition for
matching downsets, yielding arbitrary products of matching downsets and
Boolean cubes. Disjoint-support unions and restrictions retaining the
largest-star size have explicit certificate lifts. A valid seven-vertex
certificate with eigenvalue 8/5 demonstrates why unrestricted tensoring of
H certificates can fail.

The finite evidence covers **208 nontrivial rank-two downsets on at most
six active coordinates**, with certificate dimensions at most 22. This is
a specified cohort, not an exhaustive classification of all downsets on
six coordinates. The unrestricted Conjecture H remains open.

## Reproduce

Python **3.11.2**, standard library only; no solver or numerical package.
Run from this directory:

```bash
python3 certificates.py
python3 verify.py
```

The first command deterministically regenerates
[rank_two_certificates.json](rank_two_certificates.json), a 14 KB compact
fixture of graph encodings and partitions. The second prints
[expected.json](expected.json). It checks support, row sums, symmetry,
largest-star sizes, and positive semidefiniteness using exact rational LDL
elimination. It independently partitions all labeled graphs through order
five into isomorphism orbits and compares individual representatives.
Order six coverage uses unrestricted vertex extension and the induction in
the proof. The analytic proofs of the infinite classes do not depend on
the finite enumeration.

Fixture SHA-256:

```
97189bdb1f948e15bda3abeab288ade0bad30d932a72af54daf16239b051cc4f
```

Expected key outputs: class counts `[1,2,4,11,34,156]`; total `208`; six
cube baselines; 24 bounded matching checks; product parameters `(49,14)`,
`(35,14)`, `(15,6)`; the naive tensor quadratic form `-168`.
Generation took 0.65 seconds and verification 2.62 seconds on the research
worker, with verification peak RSS about 18 MiB. Each command runs one
process and uses no thread pool. No bulky artifacts are required or omitted.

The infinite rank-two consequence uses established Vizing edge coloring.
The lift and closures are explicit applications of standard matrix and
theta/Hoffman machinery. These artifacts make no literature priority claim
and have not undergone an independent review or formalization.

## Primary sources and current status

- Ellis, Filmus, Friedgut, [*Chvátal's conjecture: a proof from The Book*,
  Section 4](https://arxiv.org/html/2609.28404v1#S4), submitted 2026-09-23.
  The [current arXiv record](https://arxiv.org/abs/2609.28404) had v1 only
  when checked on 2026-09-30. Section 4 leaves H and I unresolved. Its
  projection-packing argument is distinct from an H matrix certificate.
- Misra and Gries, [*A Constructive Proof of Vizing's Theorem*, author's
  manuscript](https://www.cs.utexas.edu/~misra/psp.dir/vizing.pdf), and
  [published article](https://doi.org/10.1016/0020-0190(92)90041-S),
  *Information Processing Letters* 41 (1992), 131-133. This supplies the
  established maximum-degree-plus-one edge-coloring theorem.
- Stephen and Yusun, [*Counting inequivalent monotone Boolean functions*,
  Table 3](https://arxiv.org/pdf/1209.4623), for the wider counts of 210 and
  16,353 ambient-coordinate downset classes, including trivial families.
  Those counts are context, not an imported input or a coverage claim here.

Targeted searches located no separate primary statement of this exact
certificate package. That bounded search does not establish novelty.
