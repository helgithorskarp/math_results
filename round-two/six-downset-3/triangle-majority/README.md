# An unbounded capped H family with a nonstar maximum

six-downset-3, researcher, 2026-10-01.

For three core points and every integer number \(q\geq2\) of outside points,
include all sets of size at most two and all triples with at least two core
points. The rational matrices here certify tight weighted Hoffman H,
attain the universally maximal lower rank \(N-4\), and have a simple unit
endpoint. The three core stars and the core triangle plus every admitted
triple are exactly the four maximum families. All finite mixed products
have exactly four maximum cylinders per factor with smallest \(q\).

Here \(N=(q^2+13q+16)/2\) and \(s=3q+4\). Read the fully quantified theorem,
elementary sector completeness proof, cap criterion and tensor argument
in [PROOF.md](PROOF.md). This is an author-checked ordinary proof with
exact certificates; the analytic/completeness bridge is not formalized
and no independent-review verdict is claimed. General H and I remain
open as stated in the [primary problem source](https://arxiv.org/html/2609.28404v1#S4).

Run from this directory, or substitute its path from the repository root:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O verify.py
sha256sum -c SHA256SUMS
```

Python 3.10 or later and its standard library suffice. There are no external
imports, numerical solvers, CAS dependencies or downloaded proof corpora.
The replay takes about three seconds and below 25 MiB on the author's
single-thread run. It regenerates 33 infinite sign certificates (357
coefficients), checks full rational matrices at \(q=2,3,4\), verifies all
41 literal sector-action columns at \(q=4\), rejects 26 damaged or inexact
inputs, and tests four positive matrix controls. Both modes reproduce the
same deterministic records hash:

`96e033843bd8c31faf2bd3518d292bec5137a5580bc96f1fea5579f40cdad383`.

Files:

- [model.py](model.py): explicit generic weights and exact sector forms;
- [poly.py](poly.py), [signs.py](signs.py), [SIGNS.json](SIGNS.json): exact
  rational functions, regenerating code and unbounded sign certificates;
- [BOUNDARIES.json](BOUNDARIES.json), [matrices.py](matrices.py),
  [exact.py](exact.py): two boundary tables, whole-domain reconstruction
  and exact Schur/characteristic checks;
- [literal_action.py](literal_action.py): separate literal spanning/action
  algorithm using ordinary rational row reduction;
- [verify.py](verify.py), [RESULTS.json](RESULTS.json): full replay,
  corruption controls and deterministic mathematical records;
- [PROOF.md](PROOF.md), [SHA256SUMS](SHA256SUMS): mathematical bridges,
  credits and compact source integrity manifest.

To construct a particular matrix from this directory:

```python
from fractions import Fraction
from matrices import build
from exact import lift
members, s, families, C = build(5)
N = len(members)
L = lift(C)
M = [[Fraction(L[i][j] - s*(i == j), N-s)
      for j in range(N)] for i in range(N)]
```

Full matrices are reconstructed locally rather than stored. The infinite
proof is the elementary complete sector decomposition plus positive
coefficient polynomials at \(q=4+u\), \(u\geq0\). The finite literal checks
validate the implementation and separately prove the two boundary tables.
