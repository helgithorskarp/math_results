# Independent review of the sixteen-point support condition

Reviewer: **six-reviewer-5**, independent mathematical reviewer, 2026-09-30.
Researcher: **six-code-1**. The shared signing identity is not evidence of
distinct authorship; these explicit identities and the independent methods
are the attribution record.

The reviewed theorem says that a hypothetical 72-word binary code of length
18, weight five and minimum distance six has at least sixteen points of
degree at least three in the pair-deficit support graph. Its definition is
\(t_{xy}=5-d_{xy}\), with a support edge exactly when \(t_{xy}>0\).
The review confirms this necessary condition. It does not rule out 72 words.
The global interval remains \(69\le A(18,6,5)\le72\).

[REVIEW.md](REVIEW.md) records the full scope, predecessor audit, exact
normalization, literature qualifications and improvement opportunities.
[provenance.json](provenance.json) identifies reviewed source commit
`51a6b2dbf5b3a0156f7614a58e5aaeee759bc70d`, every checked file, original
fixture attribution, entry-level candidate comparison and local resources.

From the repository root, Python 3.11.2, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B constant_weight_18_6_5_support16_review5/audit_support16.py --baseline constant_weight_18_6_5_support16_review5/baseline69.txt --expected constant_weight_18_6_5_support16_review5/support16_expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B constant_weight_18_6_5_support16_review5/audit_rgdd26.py --expected constant_weight_18_6_5_support16_review5/rgdd26_expected.json
```

The first audit constructs the order-four plane from determinant
collinearity and generates every candidate using forbidden triples. It
checks all 30 inverse point splits and all 36 distinguished fixed-axis
frames. Two leave cases have fixed-block conflicts. The other four have
449,450,443,449 candidates and respectively 435,540,288,435 complete stars
at the point labeled 14. All 1,698 stars fail residual pair partition.

The second audit independently replays the **classical**, not newly
discovered, nonexistence of a resolvable triple group-divisible design of
type \(2^6\), used in a predecessor proof. It constructs all 160 legal
triples and all 4,960 parallel classes; the first-class cubic incidence
multigraph gives three complete equivalence classes. None extends to a
five-class resolution. Positive partial resolutions are checked directly.

Both audits have finite node and wall limits and raise `INCOMPLETE` if a
limit is reached; that event establishes no exclusion. No limit was reached.
Normal and optimized Python runs have identical output, so checks remain
active under `-O`. The JSONs and hashes are compact replay evidence; the
programs recompute all cases. No numerical solver, large certificate,
private catalog or researcher module is a proof input.

`baseline69.txt` is the small, attributed public incumbent code from
Aw, Chee and Ling (2003), as distributed in Brouwer's maintained table.
Its validity is directly checked and its saturated point-zero link serves
only as a positive control. It is not a new construction by this reviewer.
