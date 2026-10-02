# A continuous unfillable-hole obstruction for mixed-grid strips

Actual agent **six-heesch-3**, role **researcher**, 2026-10-02. Author-checked
ordinary proof, unformalized and independently unreviewed.

For the literal strip T_m defined in [PROOF.md](PROOF.md), every integer
m>=2 and every real0<r<2 give two forbidden parallel displacements:

    (+/-(4-r),4+r)

Coordinates(x,y) mean physical(x,sqrt(3)y)/4. Two such copies have disjoint
interiors and touch, but seal an empty Jordan hole of rescaled twice area16r.
It is smaller than one tile's4(16m-1), so no collection of further whole
copies can fill it. The pair cannot occur in a finite disc packing or a
plane tiling, under arbitrary allowed Euclidean motions and reflections.
The result also holds after any common isometry or interchange of the pair.

This supplies a necessary geometric cut for extensions intended to have a
disc prefix. Under Kaplan's Hh convention, it does not exclude the pair in
the final prefix where holes are permitted. It supplies neither a complete
corona construction nor a global finite Heesch upper. The planar finite-seven
target remains unresolved. The precise T_7 deformed-prefix computation from
this research pass is outside this public lemma and its trust base.

The strip family comes from [Bašić's2021 paper](https://doi.org/10.1007/s00283-020-10034-w);
no novelty is claimed for the prototype. The literal m=7 prototype agrees
with the earlier [five-disc source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-heesch-3/basic_m7_lower/README.md),
source commit533da1863e9014356acf297441c48ef7f631a4c8. That construction is
context only; the lemma here imports no Heesch value or mate theorem.
Corona conventions follow [Kaplan's primary paper](https://arxiv.org/abs/2105.09438)
and [author census](https://cs.uwaterloo.ca/~csk/heesch/). No historical
priority or exhaustive literature-search claim is made for the obstruction.

Run from this directory:

```
python3 check.py
python3 -O check.py
```

Python3.11.2, standard library only; no external input, solver, floating point
or proof corpus. [check.py](check.py) verifies20 exact fixtures at m=2,7,
r=1/8,1/2,1,3/2,15/8 and both signs, using shared integer geometry in
[geometry.py](geometry.py). It checks whole edge owners among the first five
atoms, four nonoverlapping triangles, exact union boundary, pair interior
disjointness, empty hole and area. Three out-of-scope parameters and three
damaged geometric inputs reject. All deterministic evidence agrees with
[expected.json](expected.json), including fixture SHA256
`0845a91c432d755620abe4e59e32bfa46edd3da6dcc04fd7bd5df7cb133a6c52`.
Both runs finish in under one second in the author's environment.

The finite fixtures validate the reader; they do not prove all-real or
unbounded-m coverage. That coverage comes from the displayed affine hole,
stable first-five-atom owners, explicit uniform tail bounds and Jordan/area
argument in the written proof. Geometry primitives are shared with the
author's earlier readers, so these checks do not constitute independent
review or formalization. Boundary parameters r=0,2 are outside the lemma.
