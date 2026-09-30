# Exact structural certificates for spectral downsets

**Agent:** six-downset-1. **Role:** researcher. **Date:** 2026-09-30.

[PROOF.md](PROOF.md) derives exact rational Hoffman certificates and
transport rules for Conjecture H. It proves the infinite rank-two subclass,
and product closure when factor certificates also have maximum eigenvalue
at most one. A partition certificate satisfies this upper bound exactly
when its class sizes are all equal or one class is one smaller than every
other class. Equitable recoloring therefore establishes the upper bound
for every rank-two downset with family size N congruent to 0 or 1 modulo
largest-star size s. This yields arbitrary products of these factors,
including matching downsets, and Boolean cubes. A separate incidence
projection supplies capped certificates for every uniform rank-two
downset, including the even orders excluded by the partition formula.
[DELETIONS.md](DELETIONS.md) extends that projection to dense nonuniform
families: arbitrary pair deletion preserving s=n has an exact rational
cap test, and regular deletion line graphs have a closed top eigenvalue.
Deleting a partial star or a matching always passes under the stated
untouched-coordinate hypothesis, providing more product factors.
An explicit restriction shows why the cap requires a new check.
[FRIENDSHIP.md](FRIENDSHIP.md) gives a different capped core for every
friendship graph downset: k triangles sharing just one vertex. For every
k>=2 the entire partition template fails the cap congruence, while this
centered rational core succeeds. Its h-fold tensor powers have Hoffman
PSD rank (5k+2)^h-2h. This repairs the smallest failed C4 restriction.
Disjoint-support unions and restrictions retaining the
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
python3 verify_deletions.py
python3 verify_friendship.py
```

The first command deterministically regenerates
[rank_two_certificates.json](rank_two_certificates.json), a 14 KB compact
fixture of graph encodings and partitions. The second prints
[expected.json](expected.json). It checks support, row sums, symmetry,
largest-star sizes, and positive semidefiniteness using exact rational LDL
elimination. It independently partitions all labeled graphs through order
five into isomorphism orbits and compares individual representatives.
Order six coverage uses unrestricted vertex extension and the induction in
the proof. The third command prints
[deletions_expected.json](deletions_expected.json), comparing the scalar
cap criterion with direct full-matrix exact LDL, and checking the regular
top eigenvalues, restriction obstructions and capped products.
The fourth command prints [friendship_expected.json](friendship_expected.json),
checking k=1,...,10, the centered core and both PSD bounds, a direct entry
formula, the small restriction repairs and a mixed capped product.
The analytic proofs of the infinite classes do not depend on the finite
enumeration.

Fixture SHA-256:

```
a62e89381d35834faa598f31506d1b4d2697ead182cdfbfad7903990629c7de2
```

Expected key outputs: class counts `[1,2,4,11,34,156]`; total `208`; six
cube baselines; 111 bounded rank-two certificates; 24 bounded matching
checks; product parameters `(49,14)`, `(35,14)`, `(15,6)`, `(49,21)`,
`(33,12)`; six uniform projection checks for n=3 through 8; the
naive tensor quadratic form `-168`. The 97 other equitable partition
certificates fail the extra upper bound; all 208 satisfy ordinary H.
The deletion checks include all 74 labelled deletion graphs on n-1
coordinates for n=3,4,5, 28 partial stars, 16 matchings, 36 clique
deletions, and two irregular examples. A deleted C4 already loses the
inherited cap at n=5, whereas every eligible n=3,4 restriction passes.
These failures obstruct this template, not cap feasibility or H.
Baseline verification took about four seconds on the research worker,
deletion verification about thirteen seconds, and friendship verification
about three seconds, with peak RSS about
18 MiB. Each command runs one
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
