# Upper coatoms of the matching and Lagrange orders

## Theorem

Let `a>b>=2` be coprime and let `D(a,b)` be the rational Dyck paths from
`(0,0)` to `(a,b)`.  Put

```text
H = R^a U^b,
A = R^(a-1) U^(b-1) R U,
B = R^(a-1) U R U^(b-1).
```

In the strict orders pulled back from the matching score `M` and Lagrange
score `L`:

* `A` is the unique path immediately below `H` in the matching order;
* `A` and `B` are exactly the paths immediately below `H` in the Lagrange
  order;
* `L(A)=L(B)`, and `A=B` precisely when `b=2`.

Thus `A` is a common upper coatom, while for `b>2` the path `B` is an
additional Lagrange coatom which is not a matching coatom.  This is an
explicit partial solution of the cover-classification problem for every
coprime endpoint, rather than a bounded enumeration.

The full proof is in [PROOF.md](PROOF.md).  It is symbolic.  Computation is
used only as an independent finite check of definitions, boundary cases, and
the equality classification.

## Exact corroboration

Requirements: CPython 3.11 or later; no third-party packages.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -I verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -I test_verify.py
sha256sum -c SHA256SUMS
```

`verify.py` exhausts every coprime endpoint `2 <= b < a <= 12`.  It computes
matching scores by integer continued-fraction matrices and Lagrange scores as
reduced rational squares, groups all paths into exact levels, and checks the
claimed maximum and coatom sets.  The expected final markers are

```text
EXACT COATOM ENUMERATION VERIFIED
INDEPENDENT CONTINUANT CHECKS PASSED
```

The compact expected summary is stored in `expected.json`.  The score-table
digest hashes every enumerated path together with its exact matching score and
reduced Lagrange square; no bulk score table is committed.

## Prior work and novelty scope

Apruzzese and Cong, [On Two Orderings of Lattice
Paths](https://arxiv.org/abs/2310.16963), prove that `H` is the common unique
maximum.  Their block-merger lemma and its exact Fibonacci difference formula
are used in the matching half of the proof.

Li, [Lagrange Collisions and Cover Relations for Rational Dyck
Paths](https://github.com/crabsatellite/lattice-path-orders/blob/main/paper/Li_Lattice_Path_Orders_2026.pdf)
(2026), gives a global exact prefix-certificate characterization for all
covers, as well as endpoint parity, local matching formulas, and the first
(lowest) matching levels in `D(n,n-1)`.  It does not state the upper-coatom
classification proved here.

Targeted arXiv, Crossref, GitHub-source, and Discovery Net searches on
2026-09-03 found no earlier explicit classification of the matching or
Lagrange coatoms.  The result is therefore described only as apparently new
to the searched sources, not as a priority claim.

## Trust boundary

The theorem depends on the displayed elementary reductions, the standard
alternating comparison rule for simple continued fractions, and the cited
Apruzzese--Cong block-merger identity.  The finite checker trusts CPython
integer arithmetic, `fractions.Fraction`, SHA-256, the operating system, and
hardware.  `test_verify.py` independently recomputes continuants without the
production matrix routine.  Neither finite search is needed for the uniform
theorem.
