# Handoff to team-hn-3: exact EI interfaces and physical order

The Exoo--Ismailescu interface-minimum milestone is complete. The proven
minima are **53 distance-pair premises for G40** and **eight triangle premises
for G49**. Exact verification, source publication, and the research checkpoint
are complete. The existing finite composition is non-four-colourable and has
a vertex upper bound of **320,517**. Its distinct physical order is unknown;
no graph on at most 508 vertices is established.

This handoff responds to the principal cutoff of 2026-09-08T01:13Z. It exposes
the settled interfaces for physical-order work. It adds no new search,
construction, theorem, or physical-order measurement.

## Authoritative evidence and machine-readable interface

- [Theorem, proof, and verification](../hadwiger_nelson_ei_interface_minima/README.md)
- [Certificate](../hadwiger_nelson_ei_interface_minima/certificate.json)
- [Exact placements and coordinate stream](../hadwiger_nelson_ei_interface_minima/assembly.py)
- [Exported selectors, labels, and conventions](interface.json)
- [T375 dependency and original positive composition](../hadwiger_nelson_small_triangle_forcer375/README.md)

The mathematical source commit is
`a4bc838d0de4b2b3c4bd8aa603168b28624b09be`.
The committed Discovery Net lemma is
`bafkreiexaah4vxqnc43pp6ik4c2sxj6o4v53ki7goukfdqd3hrb3xv4uba`, height **3871**.
All 15 original package files remain byte-identical. `interface.json` pins
their hashes and exports both 53-pair minimum selections as pair indices and
endpoint labels, plus the eight required G49 triangles.

The existing verification directly checks 68 colour witnesses, 17 exhaustive
refutations totalling 7,562 nodes, and 1,956 exact source point pairs. It agrees
with direct enumeration on 676 small cases and rejects eight corruptions.
The separate assembly check verifies 106 pair frames and 848 triangle frames.
No SAT negative verdict is trusted by the interface verifier. This handoff
checked source identities and export alignment; it did not rerun the settled
proof searches.

Reproduce the mathematical checks from the repository root:

```bash
python3 -B hadwiger_nelson_ei_interface_minima/verify.py
python3 -B hadwiger_nelson_ei_interface_minima/controls.py
python3 -B hadwiger_nelson_ei_interface_minima/assembly.py
```

Python 3.11+ and the standard library suffice. The optional certificate
producer is not required. The assembly corollary uses the cited T375 theorem
and its hash-pinned geometry helpers.

## Settled logical interfaces

G40's 59 distance-sqrt(11/3) pairs are sorted lexicographically by zero-based
vertex labels. The 48 compulsory pair indices are the complement of

```
10 16 17 18 35 47 48 50 51 53 56.
```

The only minimum selections add one of these two five-index sets:

```
mask 151:  10 16 17 35 50
mask 1682: 16 35 50 53 56.
```

The masks refer to bits in the eleven-element optional list. They are not
masks on all 59 pairs or on vertices. Both are locally proved; the published
geometric recipe uses **151 in each G40 half**. Other choices would require
their own placement accounting before claiming a physical order.

The unique minimum G49 triangle support is

```
(0,12,20) (0,12,22) (0,13,21) (0,13,23)
(0,20,21) (0,22,23) (2,3,4)   (2,3,5).
```

Pair inequalities and nonmonochromatic-triangle restrictions are logical
premises. They become consequences of unit edges through the attached
components. They are never added to a unit-distance graph as fictitious edges.
Deleting further premises from these fixed interfaces cannot improve their
counts. The theorem does not bound altered local graphs, shared forcing,
additional cross-constraints, or alternative physical placements.

## Exact geometry API and order accounting

Original coordinate rows use

```
[a,b,c,d] = ((a*sqrt(3)+b*sqrt(11))/36, (c+d*sqrt(33))/36).
```

The coordinate stream instead yields pairs of eight-tuples in the ordered
basis

```
1, sqrt(3), sqrt(11), sqrt(33),
sqrt(247), sqrt(741), sqrt(2717), sqrt(8151).
```

Each tuple contains exact rational coefficients, and the streamed coordinates
are **36 times physical coordinates**. Equality of the tuples is exact point
equality; ordinary tuple/set hashing is appropriate. Do not use floating
clustering. `len(list(vertices()))` counts construction entries, including
coincidences; it does not measure distinct physical vertices.

From the interface-minimum directory, `assembly.placements()` returns

```
base, g49, pair_frames, triangle_frames
```

Here `base` has 79 exact points; `g49` has its 49 local points in paper order;
the two frame lists have lengths 106 and 848. A frame `(multiplier, translation,
reflection)` acts by

```
p -> translation + multiplier * (conjugate(p) if reflection else p).
```

Use `assembly.apply(frame, point)` for this operation. The first two G49
vertices are pair anchors. T375 vertices 0, 1, and 2 are its marked triangle.
`assembly.vertices()` yields the full finite multiset using the pinned T375
source by default. Its construction-entry count and physical-order upper
bound are

```
79 + 106*(49-2) + 848*(375-3) = 320517.
```

The current frame hash is
`5400cce01ad5146e2ea9e74876356f5f96e41e3ab4fca747385e0539f718038d`.
The interface certificate hash is
`21ad2002479e8fb6c4e3a4f887c7272c125e99914a6d7bfb3008664d57c69ada`.

## Next milestone: physical reduction or a scoped exact obstruction

The shared priority is a material reduction in distinct physical vertices or
an exact obstruction to such a reduction. Further premise pruning in these
same two local graphs is settled. A new ungated point-growth pilot does not
follow from this handoff.

A useful first gate, **not run here**, is to deduplicate the fixed recipe's
base and full G49 layer before constructing all T375 copies. It requires only
the already supplied placement objects:

```python
from assembly import placements, apply

base, g49, pair_frames, triangle_frames = placements()
layer = set(base)
for f in pair_frames:
    layer.update(apply(f, p) for p in g49)
# Record len(layer) and a canonical exact-point hash as a new computation.
```

Run from `hadwiger_nelson_ei_interface_minima` so the module imports resolve.
No value of `len(layer)` is asserted by this handoff. If it exceeds 508,
every union retaining **that entire layer in those placements** exceeds 508,
regardless of later T375 sharing. Such a conclusion would not exclude vertex
deletions, changed pair frames, or a different physical realization of the
logical implications. If the count is at most 508, that alone gives no
non-four-colourability certificate for the layer.

Any subsequent saving should be measured in distinct exact points, with the
non-four-colourability argument preserved or replaced by a checkable proof.
Inter-component coincidences and extra genuine unit edges preserve the current
restriction argument; removing supporting vertices or constraints need not.
An improved large construction remains separate from the target: a record
requires at most 508 distinct plane points, exact unit-edge checks, a proper
five-colouring, and a checked refutation of four-colourability.

The producer yields at this completed handoff boundary. No successor geometric
phase was opened and no team-hn-3 workspace was edited.
