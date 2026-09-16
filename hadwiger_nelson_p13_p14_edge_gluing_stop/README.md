# Exact `P13`--`P14` edge-gluing stop

This directory certifies one frozen heterogeneous cyclotomic-cloud trial for
the Hadwiger--Nelson sub-509 campaign. It is a **scoped negative result**, not
a record candidate.

Let

```text
P_n = {zeta_n^i - zeta_n^j : 0 <= i,j < n}.
```

The construction uses the canonical first nonbipartite distance shell of each
full cloud from the all-scale source package. Normalize `P13` by the oriented
edge `(0,0)--(0,1)` and normalize `P14` by `(0,0)--(0,2)`, then identify those
oriented unit edges pointwise. Before any colour query, declare the completion
to add both equilateral apices of every private cross-cloud unit edge.

Exact reconstruction in `Q(zeta_546)` gives:

- 157 and 99 formal cloud points;
- 253 collision-merged physical points, with exactly three shared points;
- 492 complete unit edges;
- 312 source edges from `P13` and 182 from `P14`, with two shared edges;
- **zero private cross-cloud unit edges**, hence zero declared completion
  points;
- component orders `197, 28, 28`;
- no 4-core;
- chromatic number exactly **3**, witnessed by a checked ternary word and a
  checked 13-cycle.

Thus this one placement fails before the intended globally coupled gate. The
result does not exclude other relative placements, scales, polygon orders, or
other completions. In accordance with the one-architecture allocation, none
of those variants is tested here.

## Reproduction

Python 3.11 or later, standard library only:

```sh
python3 verify.py
python3 -O verify.py
python3 controls.py
sha256sum -c SHA256SUMS
```

`verify.py` independently generates `Phi_546`, reconstructs both normalized
clouds as exact projective cyclotomic coordinates, collision-merges them,
tests every physical pair for unit distance, verifies the colouring and odd
cycle, and recomputes the graph structure. The literal colouring is only a
positive witness; solver soundness is not a proof premise.

The input all-scale cloud theorem is in
[`hadwiger_nelson_polygon_difference_spectra`](../hadwiger_nelson_polygon_difference_spectra/README.md)
at source commit `883ef03fd8550d5ee4f34ef26a7ea1539048aa97`.
