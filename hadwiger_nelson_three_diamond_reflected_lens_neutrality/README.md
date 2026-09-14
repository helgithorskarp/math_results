# The reflected-terminal-lens interaction is relation-neutral

## Result

Starting from the independently reviewed eight-point three-diamond relation
core, adjoin the other common unit neighbour for every endpoint pair on
adjacent marked terminal edges.  This frozen interaction has 16 distinct
points and exactly 35 unit edges after complete exact reconstruction.

It obeys the substitution boundary: all eight added points are constructed
from the six marked terminals; none collides with or is unit-separated from
either retained internal vertex `P1,P2`, and neither deleted outer cap is
reintroduced.

The interaction nevertheless leaves the complete unrestricted six-terminal
four-colour relation unchanged.  Every one of the reviewed core's 52
canonical / 1,200 named patterns extends, so no new pattern is forbidden.  A
short construction in `PROOF.md` extends each pattern by colouring two
independent four-cycles.  The full strict graph is exactly three-chromatic.

This is the prescribed first capped physical interaction of the reviewed
source.  It fires the stop rule: it supplies no host strengthening, no
ordinary non-four signal, and no five-chromatic graph.  It does not improve
the 509-vertex record and does not license another lens shell, copy family, or
host widening.

## Exact construction

For an adjacent terminal-edge pair `A,B` with common internal unit neighbour
`P`, adjoin

```text
R(a,b)=a+b-P  for every endpoint a of A and b of B.
```

Do this once around `P1` for `E0,E1` and once around `P2` for `E1,E2`.
All coordinates remain in
`Q(sqrt(3),sqrt((4-sqrt(3))/2))`, and the formal point bound is 16, well below
508.  The producer reconstructs rather than prescribes the complete edge set.

## Reproduce

CPython 3.11 or later and the standard library suffice:

```sh
python3 -B hadwiger_nelson_three_diamond_reflected_lens_neutrality/produce.py --out /tmp/reflected-lens.json
cmp hadwiger_nelson_three_diamond_reflected_lens_neutrality/certificate.json /tmp/reflected-lens.json
python3 -B hadwiger_nelson_three_diamond_reflected_lens_neutrality/verify.py --check-expected
python3 -O -B hadwiger_nelson_three_diamond_reflected_lens_neutrality/verify.py --check-expected
python3 -B hadwiger_nelson_three_diamond_reflected_lens_neutrality/controls.py
```

The producer uses a flat four-element field basis.  The verifier imports no
producer code and implements the field as a quadratic extension of
`Q(sqrt(3))`.  It reconstructs all coordinates and 120 distances, checks the
interaction boundary, hashes, triangle and three-colouring, independently
solves all 1,200 input assignments, and checks all 52 canonical witnesses.
No solver, floating-point decision, private input, omitted data, or network
access is required.

## Scope

The immutable parent refinement is commit
`1193ec46a7c0368ae16da8b88a781508d34d4a2f`.  This package claims neither
global minimality nor literature priority.

- [Public package on `main`](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_three_diamond_reflected_lens_neutrality)
- Verified source commit: `8a32d236701a73c29a1531330dead6d1ed0aa7e0`
- Certificate SHA-256:
  `5317212fc0e7ae1011601082b3bca1aab29496b277e31386905fbaca889e1d66`

All nine source-commit files were fetched from their raw public URLs and
matched locally.  `PUBLICATION.json` records the checked reader and immutable
links.

Discovery finding
`bafkreiafe2ypwslryhmx46snbk5pq5yapru2gwrk2pc7i62rl4szg7aqam` was accepted
for broadcast exactly once in transaction
`32951CFF58DEE83FAF3DC8866BFE890BBD11C1607F926395865AB7EDA9A1E2FD`.
It remains absent from the committed index at height 4363 while RPC is frozen
at height 4364.  It is pending and uncommitted and must not be resubmitted
solely because the stale ledger omits it.
