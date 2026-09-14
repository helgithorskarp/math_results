# Exact closure of a non-Parts paired-kernel star family

## Result

Let `K` be the exact 39-point paired-circle kernel from the earlier
[two-variable realization](../hadwiger_nelson_paired_circle_obstruction_realizability/README.md).
Its four marked centres form two disjoint unit edges and have a common unit
neighbour.  Consequently their unrestricted four-colour interface permits
exactly the following equality types, up to a permutation of the colours:

```text
0101  0102  0120  0110  0112  0121
```

The seventh edge-compatible type `0123` is impossible because the common
neighbour would see all four colours.  The certificate supplies a proper
colouring for each of the six positive types, so this is an exact interface
statement about the physical 39-point graph, not the older orbit-phase or
owner-list obstruction.

This contribution closes a natural exact composition representation.  Take a
fixed copy of `K`.  An allowed attachment maps either marked centre edge of a
second copy to an oriented unit edge of the fixed copy, using either planar
chirality.  There are

```text
2 source edges * 102 target edges * 2 orientations * 2 chiralities = 816
```

raw attachments and 326 distinct two-copy point supports.  The union of the
fixed copy and **all** attached images is a strict plane unit-distance graph
`H` on 587 distinct points and 2,426 edges.  All collisions are merged and
all 171,991 unordered point-pair distances are checked exactly.

The central theorem is stronger than an enumeration of small compositions:

> Every graph obtained from the fixed kernel and an arbitrary subset of the
> 816 allowed attached copies is exactly three-chromatic and has the same
> six-pattern four-colour interface on the fixed centres as `K`.

Indeed every such graph `G` is the induced unit-distance graph on an
intermediate point set, so `K` is a subgraph of `G` and `G` is an induced
subgraph of `H`.  The certificate gives all six terminal colourings of `H`.
Thus, writing `R_X` for the extendible terminal patterns,

```text
R_H subset R_G subset R_K,    R_H = R_K,
```

which proves equality throughout.  Moreover the whole host has the explicit
three-colouring

```text
colour((a+b sqrt(3)) + i(c+d sqrt(3))) = a+c (mod 3).
```

Every coefficient denominator in `H` is 1 or 2, hence is invertible modulo
three.  The 2,426 unit edges have six coefficient-difference residues, and the
displayed linear form is nonzero on all six.  Since `K` contains a unit
triangle, every intermediate graph has chromatic number exactly three.

This is a restricted-family exclusion and a construction pivot, not global
Hadwiger--Nelson progress.  In particular the 587-point aggregate host is
above the record threshold, while every member of this family on at most 508
points is three-colourable.  No five-chromatic plane unit-distance graph is
claimed.  Parts's [509-vertex construction](https://arxiv.org/abs/2010.12665)
remains the campaign baseline.

## Exact construction

Coordinates lie in `Q(sqrt(3),i)`.  The producer writes

```text
z = (a+b sqrt(3)) + i(c+d sqrt(3))
```

as two quadratic-field pairs.  Put

```text
omega = (1+i sqrt(3))/2,    U = {1,omega,...,omega^5}.
```

The base centres are

```text
a0 = 0,
a1 = (sqrt(3)-i)/2,
b0 = omega-i,
b1 = 1-i.
```

The kernel construction takes the complete cross-circle intersections,
closes every owner-relative direction under `U`, translates the two direction
sets by their two owners, merges equal points, and reconstructs every unit
edge.  This yields the previously certified 39 points and 102 edges, with
canonical hashes

```text
points 866e7f8c58acb891be61935663f8d77fb02818835272d0532c90d845bbf14912
edges  797b1e2d848a30cf2467b4b22b6772ed13ee0d13bf11aefb7efa0d2fb92b8ec3
```

For a source centre edge `(s0,s1)` and oriented target unit edge `(t0,t1)`,
an orientation-preserving attachment is

```text
T(z) = t0 + alpha (z-s0),
alpha = (t1-t0) conjugate(s1-s0).
```

For the reflected attachment, replace `z-s0` by its conjugate and use
`alpha=(t1-t0)(s1-s0)`.  Both source and target vectors are unit, so these are
exact isometries.  The exhaustive loops implement precisely the 816 choices
in the displayed product; no approximate placement or abstract graph is used.

The aggregate host hashes are

```text
points 5c3ad1512fcd1369446536d46be2ace1e651b7ba6a1c661436a324e822b6251c
edges  07ae8be266e812c7e926df39336a5dda36ea94c0a3716e4ef9f87bbc64b6910e
```

## Reproduction and trust boundary

The producer requires CPython 3.11 or later and `python-sat==1.8.dev17`:

```sh
python3 -m venv /tmp/hn-sqrt3-star-env
/tmp/hn-sqrt3-star-env/bin/pip install -r requirements.txt
/tmp/hn-sqrt3-star-env/bin/python -B build.py --out /tmp/hn-sqrt3-star.json
cmp certificate.json /tmp/hn-sqrt3-star.json
```

The independent checker requires only the Python standard library:

```sh
python3 -B verify.py --check-expected
python3 -O -B verify.py --check-expected
sha256sum -c SHA256SUMS
```

`build.py` uses complex pairs over `Q(sqrt(3))` and CaDiCaL to discover one
host colouring for each terminal type.  `verify.py` imports neither the
producer nor the earlier package.  It instead uses the tensor basis
`1,sqrt(3),i,i*sqrt(3)`, independently reconstructs the base, all 816 exact
isometries, the 326 support hashes, all 587 points, and all 2,426 edges.  It
checks the six supplied colour words directly, derives the modular
three-colouring, and rejects nine malformed controls.  SAT soundness and
solver model ordering are therefore not proof dependencies.

The remaining trust is in Python's exact rational arithmetic, the elementary
linear independence of the displayed field basis, ordinary hardware, and the
written completeness/sandwich argument above.  This is author-side exact
verification, not external review or proof-assistant formalization.  The
5,187-byte certificate has SHA-256

```text
38b016dd646eb088f17fe9f5cdd6aa68c4fc86b0c8db5558df65a3fe6cfe76a1
```

## Construction decision

The selected non-Parts core met the physical interface milestone at 39 points:
its exact graph forbids `0123` while realizing all six other terminal types.
The star representation is now closed much more strongly than the planned
three-copy gate, because its entire finite attachment host preserves that
interface and is three-colourable.  Further star attachments to edges of the
fixed base are therefore a proven dead end.  This does not close attachments
to newly created edges, other realizations of the paired-circle obstruction,
or non-star compositions; those require a new representation rather than more
sampling inside this host.
