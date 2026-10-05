# Structural component: the universal maximizing-parent budget

Author: Atlas, agent ID `studio-researcher-1`, researcher; 2026-10-05,
version 1. The [proof](PROOF.md) establishes a weighted-tree lemma: for
every nonstar tree and every parent p of globally maximum-potential
leaves,

```text
(d-1)(1-2^(1-H)) <= (5/4)(n-1-d-H),
```

where d counts graph-leaf neighbors and H is eccentricity to a graph
leaf. With h = H-1 the core eccentricity, this implies

```text
n >= h+1+(9/5)d-(4/5)d*2^(-h).
```

The latter also holds for stars. The source explicitly proves the
full-tree degree normalization, keeps all tied maximizing parents,
separates K2, and states the inherited stacking-classification interface.
It does not establish the full multiplicity asymptotic by itself.

Run from this directory with CPython 3.11.2 or compatible Python 3.11+:

```bash
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
  python3 check_structural.py --output /tmp/atlas-structural-result.json
python3 -c 'import json; a=json.load(open("EXPECTED.json")); b=json.load(open("/tmp/atlas-structural-result.json")); assert a == b'
```

Only the Python standard library is needed. All mathematical comparisons
use integers or `fractions.Fraction`, including powers with negative
exponents. No random sampling, solver, external data, inherited source
module, or reachability oracle is imported.

The controls compare direct BFS potentials, recursively reconstructed
deficits, edge-end weights, the chosen-path complement, and explicit
disjoint bottom-edge pairings. They cover all labeled trees of orders
three through five, small boundary fixtures, and a bounded grid of
branched brooms. Negative controls retain the known order-22 failure of
the older height bound, reject applying maximality at a nonmaximizing
parent, and reject the nonstar-only stronger budget at a star. Invalid
graph inputs are rejected. The output records exact scope/counts and
compact witness values; finite controls corroborate the universal proof
without replacing it. See `RUN.md` for the measured local run and
`MANIFEST.json` for frozen source hashes.

This is an author component awaiting a new exact-version internal check
by another researcher. An earlier feasibility check concerns its earlier
note, rather than automatically accepting this version or the final
assembled theorem. Source publication is coordinated with the other
checked components; private campaign state is outside this directory.
