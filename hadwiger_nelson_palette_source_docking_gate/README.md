# Direct docking of the two palette sources fails geometrically

The sixteen-point opposed-palette coupler **G** and the frozen-centre source
**F29** cannot be joined by identifying the coupler's eight input terminals
with eight vertices of one isometric F29. Under **any real plane isometry**, an
F29 image contains at most **two** of those terminals. The bound is sharp.
Every possible two-pin overlap has a neutral unrestricted four-colour relation.

This closes a proposed direct transfer with an ideal budget of
`29 + (16 - 8) = 37` points. It produces **no new composite support**, no
strengthened physical relation and no sub-509 record progress. It is a
construction-selection failure. No partial-docking, extra-copy, angle or host
search follows this gate.

## Exact metric proof

Use the point numbering in [source_points.json](source_points.json). The
coupler's terminals are `T=(5,6,7,8,12,13,14,15)`. Its coordinates have denominator
8 in the real radical basis `(1,sqrt3,sqrt5,sqrt7,sqrt15,sqrt21,sqrt35,sqrt105)`
on each axis. The verifier also reconstructs all sixteen coordinates from the
closed complex formulas

```
A=-1/2, B=1/2, D=3/4+i*sqrt15/4,
C=i*(sqrt15+sqrt7)/4, E=-3/4+i*sqrt15/4,
X±=(D+C ± i*sqrt3*(C-D))/2,
Y±=(E+A ± i*sqrt3*(A-E))/2.
G=(A,B,D,C,E,X+,X-,Y+,Y-,-D,-C,-E,-X+,-X-,-Y+,-Y-).
```

Each F29 row `(a,b,c,d)` denotes
`(a+b*sqrt33 + i*(c*sqrt3+d*sqrt11))/12`. For a difference row, the squared
length is

```
(a²+33b²+3c²+11d² + (2ab+2cd)*sqrt33)/144.
```

The 28 squared distances within T lie in `Q(sqrt5,sqrt21)`. The 406 squared
distances within F29 lie in `Q(sqrt33)`. The squarefree radicals
`1,sqrt5,sqrt21,sqrt105,sqrt33` are linearly independent over Q, so any distance
common to both spectra must be rational. This argument concerns distances;
the isometry itself need not belong to either coordinate field.

The rational terminal distances squared are exactly:

| Pairs | Squared distance |
|---|---:|
| (5,6), (7,8), (12,13), (14,15) | 3 |
| (7,15), (8,14) | 5/2 |

The rational F29 spectrum, with unordered-pair multiplicities, is

```
1/3:36, 1:75, 4/3:8, 5/3:21, 7/3:5, 3:17, 11/3:5, 4:5.
```

In particular, it omits 5/2. Thus the graph on T whose pairs can possibly occur
inside one isometric F29 is exactly the four-edge matching in the first table
row. Any shared terminal subset must be a clique in this graph, hence has size
at most two. This uses all distances, all vertex choices and both orientations,
without a numerical tolerance or a finite-angle assumption.

The bound is sharp: F29 vertices 4 and 12 have squared distance 3, as do G
vertices 5 and 6. The complex map
`z -> g5 + (g6-g5)*(z-f4)/(f12-f4)` is an isometry placing both terminals in its
image. This statement concerns terminal overlap only; it makes no assertion
about other collisions or cross edges of that union.

## Complete relation at the possible shared pairs

[certificate.json](certificate.json) supplies two proper four-colour words for
each of the 17 F29 pairs at squared distance 3. The first pins the pair to
`(0,0)` and the second to `(0,1)`. Colour permutation covers every named
assignment to two vertices, including patterns using fewer than four colours.
The checker reconstructs **all 75 strict unit edges** from all 406 point pairs
and checks all 34 words and their pins, giving 2,550 edge checks. There is no
negative SAT claim or solver trust boundary here.

Consequently, suppose finitely many isometric F29 copies meet G **only at
vertices in T**, their vertices outside G are pairwise disjoint, and the
complete unit graph of the union has no edges beyond constituent edges.
Every four-colouring of all sixteen G vertices extends: each copy has at most
two old pins, its certified word can be permuted to those colours, and the
extensions do not interact. All old terminal relations remain unchanged.

These hypotheses are essential. The result does **not** exclude F29 copies
sharing other core vertices, interacting interiors or additional unit
contacts. It is not a theorem that F29 and the coupler cannot help any future
construction. Such a successor still needs an explicit interaction and a
complete budget before another relation census.

## Reproduction and provenance

Python 3.11.2, standard library only. From this directory:

```sh
python3 -B verify.py --check-expected
python3 -O -B verify.py --check-expected
python3 -B controls.py
python3 -B produce.py --output /tmp/fresh-docking-certificate.json
cmp certificate.json /tmp/fresh-docking-certificate.json
sha256sum -c SHA256SUMS
```

The producer uses complete backtracking solely to find positive words; the
checker trusts neither its search nor any imported sibling module. Controls
compare all 434 relevant norm vectors with independent prime-mask arithmetic,
check all 256 terminal subsets, and reject five corrupted certificates,
including a proper word with the wrong named pins. Timings, versions and hashes
are in [VALIDATION.json](VALIDATION.json). Trust boundaries are Python's exact
integer/rational arithmetic and the unformalized elementary radical-independence
and isometry arguments. This is author verification, not independent review.

The source fixture is copied byte-for-byte from the
[frozen input driver](../hadwiger_nelson_frozen_input_triangle_driver/README.md),
source commit `b6191ffeb168d9c192ad4d4d5d920273df871cc3`; its SHA256 is
`9d80a8e7997d5d2780c3ec783dbdc02e6e4678b7454b72787b34a6268188ea99`.
The source definitions originate in the
[opposed-palette package](../hadwiger_nelson_opposed_palette_cells/README.md)
and [F29 transfer package](../hadwiger_nelson_frozen_centre_transfer/README.md).
Their demonstrated palette obstructions motivate the proposed docking; the
metric theorem and positive pair words here do not rely on those obstruction
proofs. No priority claim is made for the elementary field-separation argument.

A live primary-source refresh on 2026-09-14 still identifies
[Parts' 509-vertex / 2442-edge construction](https://arxiv.org/abs/2010.12665),
with 509 also stated as the record in
[Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4).
This gate was selected after an initial exact distance pilot had already shown
the mismatch. It is not presented as a preregistered successful experiment.
The R2 handoff requests a different physically compatible relation source or
an explicitly interacting driver; the two sources remain dormant meanwhile.
