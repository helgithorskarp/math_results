# Three exact fixed-weight composition gates

No five-chromatic plane unit-distance graph is produced here. Three frozen
bottom-up constructions below the 509-vertex record were collision-merged,
their complete strict unit graphs were reconstructed exactly, and explicit
proper colourings were checked on every edge.

| Construction | Formal addresses | Physical points | Unit edges | Checked upper bound |
|---|---:|---:|---:|---:|
| five-subsets of 11 consecutive regular 12-gon rays | 462 | 206 | 725 | 3 |
| four-subsets of 12 consecutive regular 18-gon rays | 495 | 375 | 1,383 | 3 |
| weight-five sum of ten mixed negative-trace directions | 252 | 246 | 574 | 4 |

The two regular cases contain a unit triangle, so their chromatic numbers are
exactly three. The mixed case is asserted only to be four-colourable; no lower
bound beyond its displayed physical substructures is claimed.

## Exact definitions

For the first row let `zeta=exp(pi*i/6)`, take
`D={zeta^j:0<=j<=10}`, and sum each five-element subset of `D`.
Coordinates are checked in `Q(sqrt(3))`.

For the second row let `zeta=exp(pi*i/9)`, take
`D={zeta^j:0<=j<=11}`, and sum each four-element subset. Arithmetic uses the
power basis of `Q(zeta)` with `zeta^6-zeta^3+1=0`; conjugation sends `zeta` to
`zeta^-1`.

For the mixed row put `E=Q(sqrt(-3),sqrt(-11))`, let `b0,...,b12` be the
canonical ordered union of the unoriented unit directions occurring in the
exact Moser and Golomb graphs, and set

```text
u=(7+i sqrt(15))/8,  v=(5+i sqrt(39))/8.
```

The ten generators are

```text
b1,b5,b6,b7, u*b1,u*b6,u*b7,u*b10, v*b10,v*b12.
```

The physical support is the set of all five-generator sums. Its exact field
is `E(sqrt(5),sqrt(13))`. The final `v`-pair was selected from the finite 78
pair geometry census by maximum complete-edge count before its colouring was
queried.

All three supports identify equal coordinates before graph construction. No
abstract inherited edge set is used: the verifier tests every unordered pair
of distinct physical points for squared distance one.

## Reproduction

CPython 3.11 or later and its standard library suffice. From the repository
root run:

```bash
python3 -B hadwiger_nelson_fixed_weight_composition_gates/verify.py --check-expected
python3 -O -B hadwiger_nelson_fixed_weight_composition_gates/verify.py --check-expected
python3 -B hadwiger_nelson_fixed_weight_composition_gates/controls.py
```

The saved words originated in exploratory SAT calls, but solver soundness is
not a premise: `verify.py` directly checks every character against every exact
unit edge. `controls.py` checks that monochromatic and malformed words are
rejected. Coordinate and edge stream hashes in `EXPECTED.json` pin the three
physical graphs.

## Scope

This is a restricted construction checkpoint, not record progress or a global
exclusion. It says nothing about other direction selections, fixed weights,
regular polygons, continuous phases, added points, or arbitrary plane
unit-distance graphs. The mixed field is deliberately beyond the previously
published base-field four-colouring theorem, but the one frozen graph still
has the checked positive word supplied here.

The current unrestricted comparison remains Parts's 509-vertex construction.
The newly committed 530-point construction and the 119-image obstruction for
the abstract five-chromatic `G_11` were refreshed before publication; neither
is a mathematical premise here, and neither is an at-most-508 record graph.
