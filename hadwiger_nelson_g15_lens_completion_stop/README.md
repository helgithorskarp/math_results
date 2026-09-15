# Complete unit-lens closure of the three-distance G15 is four-chromatic

Start from the exact fifteen-point graph `G15` whose forbidden distances are

```text
D = {1, 1/sqrt(3), 2}.
```

The `D`-distance graph has 56 edges, chromatic number six, and independence
number three.  For every one of its 30 pairs at distance `1/sqrt(3)`, adjoin
**both** common unit neighbours.  For every one of its four pairs at distance
two, adjoin the unique common unit neighbour.  Collision-merge the resulting
points and include every strict unit-distance edge.

The complete physical support has **75 distinct points and 304 unit edges**.
It has chromatic number exactly **four**.  Hence this natural attempt to turn
the small carrier's genuine global three-distance obstruction into an ordinary
unit-distance obstruction fails, and it does not improve the 509-point record.

This is a forcing-coupled whole-support test, not a terminal-only relation
census.  Every nonunit `G15` edge participates in the operation, and all
incidental contacts among all lens points are reconstructed before colouring.
The result retires this one complete-lens operation on `G15`.  It does not
classify partial lens choices, different carriers, additional shells, or
arbitrary plane unit-distance graphs; none of those variants is proposed here.

## Exact geometry

Write a source point as `(x,y)` with `x,y` in `Q(sqrt(3))`.  If source points
`p,q` have squared distance `1/3`, their two common unit neighbours are

```text
(p+q)/2 +/- i*(q-p)*sqrt(11)/2.
```

If their squared distance is four, their unique common unit neighbour is the
midpoint.  Thus the whole support lies in `Q(sqrt(3),sqrt(11))^2` and is
represented exactly in the basis `1,sqrt(3),sqrt(11),sqrt(33)`.

There are 79 formal addresses.  Exact collision merging gives 75 points.  The
only non-singleton address classes are

```text
S0  = L4:1:4 = L4:2:5 = L4:3:6,
S11 = L4:13:14.
```

The verifier tests all `C(75,2)=2,775` physical pairs.  In particular the 304
edges are the complete strict unit graph, rather than just the intended lens
spokes.  The point and edge streams have SHA-256 hashes

```text
points 9a0b2c2d3751703f7e36249562a5bc468e33a06077224340c1f22d1c1bd98b39
edges  79ee66296587b0453a16267acb3c48b43625799cf08abbdd9daa4854f0f36e83
```

## Colour decision

The stored 75-digit word is checked directly on every reconstructed edge and
uses four colours.  A deterministic DSATUR-style exhaustive search rejects
three colours after 64 search nodes.  At each node it chooses an uncoloured
vertex of maximum saturation, then maximum degree, and tries every colour not
already used by a coloured neighbour.  Each branch colours another vertex;
there is no solver, omitted proof trace, or heuristic cutoff.  This proves
`chi=4`.

The verifier separately reconstructs the source `D` graph and computes its
chromatic number six by dynamic programming over every one of the `2^15`
vertex subsets and all independent subsets.  This rechecks that the selected
input carried the advertised global obstruction even though its lens closure
does not preserve it.

## Reproduction

Python 3.11 or later and the standard library suffice.  From the repository
root run

```bash
python3 -B hadwiger_nelson_g15_lens_completion_stop/verify.py
python3 -O -B hadwiger_nelson_g15_lens_completion_stop/verify.py
python3 -B hadwiger_nelson_g15_lens_completion_stop/audit.py
python3 -B hadwiger_nelson_g15_lens_completion_stop/controls.py
sha256sum -c hadwiger_nelson_g15_lens_completion_stop/SHA256SUMS
```

`audit.py` imports none of the submitted geometry code.  It instead represents
the field as the nested extension `Q(sqrt(3))(sqrt(11))`, reconstructs the
support and all physical edges, compares both canonical hashes, and rechecks
the positive word.  `controls.py` rejects four damaged certificates.

The fifteen exact source coordinates are hash-pinned from the sibling
[`G14/G15 embedding package`](../hadwiger_nelson_parts509_g14_g15_embedding/README.md),
which records their MIT-licensed upstream provenance and independently proves
the source invariants.  This package rederives the invariants from the points;
it does not use the Parts-509 embedding or any positive-parent argument.

The trust boundary is the displayed elementary lens formula, exact rational
arithmetic, radical-basis independence, exhaustive finite loops, CPython, and
ordinary hardware.  The two implementations are author-side checks, not an
independent external review.

Parts's [509-point construction](https://arxiv.org/abs/2010.12665) remains the
supported unrestricted record comparison.  Haugland's [August 2026
revision](https://arxiv.org/html/2608.04542v4) also states that record; its
2,131-point construction concerns the spindle-free restricted family.
