# Exact finite circle-centre synthesis: completed negative pilot

The graph specified by `seed.json` and `construction.json` has **1,024 distinct
vertices and 6,317 unit edges**. The independently checked colouring in
`certificate.json` is proper and makes vertices 0, 1 and 2 monochromatic. Those
vertices form a triangle of side `1/sqrt(3)`. Thus this finite graph does not
have the intended triangle-forcing property, and the finite construction gate
was **not reached**. No at-most-508 five-chromatic graph was found.

This is a bounded negative experiment using actual Euclidean vertices and every
unit edge among them. It is not a theorem excluding the infinite centre closure,
other selection orders, or the construction method. Its contribution is the
reproducible finite boundary and surviving colouring, with compact witnesses
showing where the geometric additions eliminated encountered colourings.

The [support handoff](SUPPORT_HANDOFF.md) consolidates and retires the completed
paired-circle, parallel-line and rational-height programs. Their earlier proofs
and certificates are unchanged. This experiment uses finite point synthesis;
it does not extend those support exclusions or HN-2's fixed-support certification.

## Seed, construction and intended gate

The seed is the 51-vertex, 180-edge graph G51 in Section 4 of
[Exoo and Ismailescu, arXiv:1805.00157v1](https://arxiv.org/abs/1805.00157v1).
The coordinate table is on PDF page 7. Each row `[a,b,c,d]` means

```
x = (a sqrt(3) + b sqrt(11))/36,
y = (c + d sqrt(33))/36.
```

The authors' G627 is a triangle-forcing gadget: no proper four-colouring makes
its marked small triangle monochromatic. That statement is conditional and
does not say that G627 itself is five-chromatic. Their G79/G49 construction
explains how such a gadget feeds a finite five-chromatic construction. This
pilot sought that same explicit forcing property with another finite sequence
of added centres; it did not achieve it. No novelty is claimed for the
circle-centre method, and no successful composition or improved size bound is
asserted here.

The discovery calculation writes `X=36x/sqrt(3)` and `Y=36y`, both in
`K=Q(sqrt(33))`. A unit edge is exactly

```
3 (X1-X2)^2 + (Y1-Y2)^2 = 1296.
```

For each pair of existing points, the generator enumerates its common unit
centres when their scaled coordinates lie in K. It keeps candidates having
neighbours in at least three colours of the current proper four-colouring with
the first three vertices pinned to colour 0. It prefers four represented
colours, then larger neighbour count, then smaller coefficient bit complexity,
then lexicographic coordinates. Every insertion adds a real point and all its
actual unit edges. SAT enforces exactly one of four colours at each vertex and
unequal colours at every edge. Fixing the three terminal colours to 0 loses no
monochromatic-terminal colouring, since colour names may be permuted.

The cap was fixed at 1,024 total vertices before the run. All 973 additions have
at least three prior unit neighbours. At 18 additions the new point had all four
neighbour colours in the current model, so that model could not extend. Each of
these 18 claims has its own proper earlier colouring in the certificate. The
final graph still has the required monochromatic-terminal colouring. The
discovery run took 44.934 seconds and left 4,740 unused candidates. These last
runtime and pool figures are run provenance, not independently certified
completeness claims. No second seed or subsequent construction phase was run.

## Exact finite certificate

`construction.json` contains 973 triples of earlier vertex indices. Each triple
has a unique circumcentre at distance one from all three parents; that centre
is the next vertex. The initial 51 vertices are in `seed.json`. This records the
entire graph without a large coordinate or edge dump. The final scaled
coefficient rows `[a,b,c,d]` mean `X=a+b sqrt(33), Y=c+d sqrt(33)`; this differs
from the paper's seed convention by a factor of three in its second entry.

`build.py` reconstructs each point by exact pair-circle intersections in K.
`verify.py` imports neither that producer nor its geometry code. It works in
the independent basis `1,sqrt(3),sqrt(11),sqrt(33)` and finds each centre from two
linear perpendicular-bisector equations. It checks the nonzero determinant,
all three unit distances, and distinctness. It then expands squared distances
for **every one of the 523,776 unordered vertex pairs**, checks the complete
edge and point hashes, the final proper colouring, the terminal side lengths,
and all 18 blocking witnesses. Thirteen malformed controls must be rejected.
The checks stay active with Python optimization enabled.

The finite four-colourability claim depends only on exact rational arithmetic,
these small input files and the checker, not on SAT soundness, a heuristic's
exhaustiveness, or floating-point tolerances. The seed transcription is also
relevant to identifying the experiment with the paper's G51; the certificate
defines and verifies its graph even independently of that identification.
No external-author review or proof-assistant formalization is claimed.

## Reproduction

Python 3.11 or later and its standard library suffice to reconstruct and check
the published object. Run inside this directory:

```sh
python3 build.py
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

Both checker runs should print the exact JSON in `expected.json`: 1,024
vertices, 6,317 edges, 973 additions, 18 blocking witnesses, 13 rejected controls,
a proper four-colouring with monochromatic terminals, and both success flags
false. Canonical hashes use compact JSON (`sort_keys=True`, separators `,` and
`:`), scaled integer coefficient rows, and all edges `[i,j]` ordered with
`i<j` lexicographically:

```
points 428c5f26afc20f8ef0343d544cc73bd402d88072a2c64d01ae6f20caac7b77fc
edges  895e145427aadbf8254e2b6a7ed97d2a709524ce5147328d6e0b3d0b99ca5b2b
```

`search.py` preserves the optional discovery procedure; it additionally needs
`python-sat==1.9.dev15` (the recorded run used Python 3.12.14 and bundled
Glucose3). It writes its uncommitted raw history below `out/`. For the
mathematical certificate, replay above is sufficient and independent of native
solver model ordering. Different native builds can choose different colourings
and therefore different subsequent vertices.

```sh
python3 -m pip install python-sat==1.9.dev15
python3 search.py
```

The completed pilot is parked at its declared boundary. A finite forcing gadget
or an unconditionally non-four-colourable candidate is still needed. This
package makes no new record claim; the standing comparison remains the
[509-vertex Parts construction](https://arxiv.org/abs/2010.12665).
