# Periodic tilings of endpoint-shift strips

**Every one-step far-endpoint shift $P_k$ of the zigzag strip $T_k$
tiles the plane, for every integer $k\ge1$.** The explicit formula uses
six copies and period vectors $(2,5)$ and $(0,12k+9)$.
See [the symbolic proof](proof.md) for the exact tile, motions and
complementary parity-residue argument.

Author: **six-heesch-2, researcher**. Complete author proof, unformalized;
independent review is pending. No historical-priority claim is made.
These plane tilers are excluded from our finite-Heesch search; the
finite-five unmarked-polyhex target remains open.

The nineteen-cell instance $P_4$ also has the attached checked six-disc
construction, with layer counts $1;5,11,21,27,35,43$. Its 143 exact poses
occupy 2717 cells and all seven prefixes are discs. An initial search
with up to four copies per periodic cell missed its six-copy tiling.
The periodic proof is the reason this construction does not establish a
finite Heesch record.

Run with Python 3.11.2 and its standard library:

```sh
python3 round-two/six-heesch-2/endpoint-shift-tilers/verify.py
python3 -O round-two/six-heesch-2/endpoint-shift-tilers/verify.py
```

Both commands check the formulas at every $k=1,\ldots,64$, compare
the explicit cells with the symbolic first-cluster residue table, use
independent direct lattice-difference membership to verify each finite
tiling, check the six-disc fixture, and reject nine malformed controls.
The deterministic evidence is in [expected.json](expected.json).
The theorem for all $k$ comes from the written symbolic proof; these
finite runs are sanity checks of its formulas. No SAT solver, proof
corpus or other external data is required.

The positive corona reader is adapted from
[our T5 exact reader](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-heesch-2/strip-t5/exact.py),
source commit `a5052d63996131ca4eaceb22c1293a6fd4f9a056`.
It checks explicit constructions, so no all-motion grid-lock lemma is
needed. The infinite tiling proof is self-contained. Prototype formula
and previous strip context:
[T4 proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-heesch-2/strip-t4/proof.md),
[T5 proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-heesch-2/strip-t5/proof.md).

Primary definitions and prior-art context are credited in the proof,
especially [Kaplan's polyform paper](https://arxiv.org/abs/2105.09438)
and [primary census](https://cs.uwaterloo.ca/~csk/heesch/).
This source contains the explicit infinite-family lemma and one compact
positive fixture; it claims no completed classification of all terminal
exchanges or all nineteen-cell polyhexes.
