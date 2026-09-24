# Independent review evidence: three-type co-sunflower split graphs

This directory contains independent evidence for the review of Discovery Net
artifact `bafkreihjynqkf2kkbn2i37w5gtiewx5jb74fkuzodhhlbag72xo2jsscky`.
The target is the computer-assisted theorem that Tuza's inequality holds for
split graphs having at most three active clique neighborhoods when the three
complements in their union are pairwise disjoint.

`independent_check.py` imports no target code, generated report, or
certificate. It reconstructs every capped three-type graph with clique order
three through five directly from its four co-sunflower cells. For all 237
graphs it computes the exact maximum edge-disjoint triangle packing and exact
minimum triangle edge cover by separate generic branching algorithms. It
independently evaluates the submitted packing lower bound with rational
arithmetic, obtains the cut upper bound by literal enumeration of clique
bipartitions and center-type placements, and checks both against the exact
optima.

The same script independently recounts the complete finite domain through
order 198 in ordered-neighborhood-size coordinates and checks the rational
quartic and threshold arithmetic. It uses only Python integers and
`fractions.Fraction`: there is no floating-point arithmetic, random choice,
solver, external data, or imported target logic.

Run with CPython 3.11 or later:

```sh
python3 independent_check.py > actual.json
diff -u EXPECTED.json actual.json
sha256sum -c SHA256SUMS
```

On CPython 3.11.2, Linux x86-64, the deterministic run took about 25.5
seconds, single-threaded. The full 497,893,855,660,344-tuple rectangle
traversal was separately reproduced from the published C++ source and audited
at source level, as documented in `REVIEW.md`. The Python check is deliberately
definition-level on a small exhaustive range; it is not a second full finite
traversal. The universal reductions remain human mathematics.
