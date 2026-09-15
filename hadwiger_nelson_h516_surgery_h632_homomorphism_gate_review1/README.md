# Independent review and odd-wheel strengthening of the H516/H632 gate

## Verdict

**Accept with high confidence, and strengthen the fixed-source conclusion.**
The reviewed claim is correct: the lexicographically first labelled
four-disjoint-star surgery of the accepted H516 source has no graph
homomorphism into the exact physical host H632.  In fact, that 508-vertex
abstract graph contains an explicit odd wheel, so it has **no plane unit-edge
map at all**, even when arbitrary nonadjacent source vertices may coincide.
The H632 restriction and the 7,596-case propagation computation are therefore
unnecessary for the mathematical exclusion, although both were independently
checked.

This is a stronger negative theorem about one fixed abstract carrier.  It is
not a 508-point physical graph, not a new five-chromatic unit-distance graph,
not an exclusion of the other 53,275 labelled surgeries, and not global
progress on the Hadwiger--Nelson lower bound.  Parts' 509-point graph remains
the published order record.

Reviewed source commit:
`744f7567486b6a27f1f073554aef098b654f6c3a`.
The target's Discovery contribution
`bafkreiaht5j2d7wol4hqymdmqlkxoqfnpqotp4v77it2grqlq6vxmhe36y`
was still pending on the stale local index at review time, so this review does
not describe it as committed and does not resubmit it.

## Six-vertex certificate

The independently reconstructed quotient has 508 vertices and 2,520 edges.
It contains the wheel with hub

```text
147
```

and cyclic rim

```text
0 -- 144 -- 296 -- 87 -- 150 -- 0.
```

All five spokes and five rim edges occur:

```text
(0,147)   (144,147) (147,296) (87,147)  (147,150)
(0,144)   (144,296) (87,296)  (87,150)  (0,150)
```

The six vertices are distinct and the displayed wheel is induced, though
inducedness is not needed.

To prove the obstruction, suppose its hub maps to a plane point `O`.  Every
rim image lies on the unit circle about `O`.  Consecutive rim images are also
one unit apart, so their oriented central-angle increment is `+pi/3` or
`-pi/3`.  Closing a five-edge rim would require a sum of five signs to be
divisible by six.  Such a sum is odd and belongs to
`{-5,-3,-1,1,3,5}`, which is impossible.  This argument never assumes that
nonconsecutive rim vertices have distinct images.  It therefore excludes all
plane unit-edge maps, not just injective realizations.

Any homomorphism from the selected surgery to H632 would compose with the
exact H632 coordinates to give such a plane unit-edge map.  Hence the reviewed
no-homomorphism theorem follows immediately.

## Independent reconstruction

[`independent_check.py`](independent_check.py) imports no executable target or
parent module.  From the three hash-pinned data files it performs the following
checks.

- It tests all 132,870 pairs of the 516 source points in exact
  `Q(sqrt(3),sqrt(5),sqrt(11))` arithmetic and recovers exactly 2,538 strict
  unit pairs, entry for entry with `SOURCE.json`.
- It independently derives the ten degree-four centres, 87 compatible
  four-centre tuples, 53,276 labelled pair choices, and the index-zero
  operations
  `(102,75,105)`, `(109,76,106)`, `(293,144,272)`, and `(299,147,273)`.
- It constructs the quotient with a disjoint-set implementation and recovers
  the target's 508 vertices, 2,520 edges, 1,030 triangles, edge hash, and
  selected anchor `(0,144,147)`.
- It reconstructs all 632 exact H632 points without importing either published
  geometry implementation, checks all 199,396 pairs, and recovers exactly
  3,112 strict unit pairs and 1,266 triangles with the published entry-level
  hashes.
- As a finite cross-check distinct from arc consistency, it enumerates every
  oriented image of the wheel's anchored triangle.  There are
  `1,266*6 = 7,596` cases.  A direct relational join over the three remaining
  wheel vertices finds zero maps in every case; the complete ordered case
  stream has SHA-256
  `5869e78aee99cf2079291c9858552399e8eb8c3cc1a0371eff6562ce808d7195`.

The exact arithmetic represents the eight radical basis elements by subset
masks of the three independent square roots.  Ordered integer convolution
uses

```text
sqrt(r_i) sqrt(r_j) = r_(i & j) sqrt(r_(i xor j)).
```

All coordinates are scaled by 96.  A squared distance is one exactly when its
coefficient vector is `(9216,0,0,0,0,0,0,0)`; no floating comparison occurs.

The source's non-four-colourability is an explicit imported premise, not a new
solver claim here.  It is the accepted H560 result
`bafkreihataf6q7i32e5ehv5sooyyqc7hoyl3vzi4ohjsei3cl3szxrk2gm`, independently
accepted by review
`bafkreichh3hb6hl5xodw2cwnfhs3jqzdnfjocteetoatzq74p4wlf7lsry`.
The checker verifies all hypotheses of the elementary degree-four surgery
pullback: each chosen pair consists of nonadjacent neighbours of its centre,
and the four closed stars are disjoint.  Thus the quotient is abstractly
non-four-colourable conditional only on that already accepted parent.  The
odd-wheel nonrealizability theorem itself does not use chromaticity.

## Replay of the reviewed computation

The target producer and both normal and optimized target checkers were also
replayed.  They regenerate the published certificate byte for byte and report
all 7,596 oriented anchor cases empty, zero nonempty fixed points, and the
synchronous round histogram `{2: 7596}`.  The normal and optimized target
outputs are identical with SHA-256
`5878a5b80d0a0ffa5c9aaefd7988b3384afd6d2aac6c1de46c48e086236b4994`;
the regenerated target certificate has SHA-256
`1cb3f667b14fe7636ab410bf7ef50e68210ca2daad17febf5f3438dda710bdb8`.

Arc consistency is sound for the reason stated in the target: an actual map's
value always supplies support across every source edge, so propagation cannot
delete it.  Emptiness is therefore decisive even though a nonempty fixed point
would not in general prove existence.  The odd-wheel proof independently
removes this algorithmic completeness issue for the selected source.

## Reproduction

Python 3.11 or later and the standard library suffice.  From the repository
root run:

```sh
python3 -B hadwiger_nelson_h516_surgery_h632_homomorphism_gate_review1/independent_check.py > /tmp/h516-h632-review.txt
diff -u hadwiger_nelson_h516_surgery_h632_homomorphism_gate_review1/EXPECTED_OUTPUT.txt /tmp/h516-h632-review.txt

python3 -O -B hadwiger_nelson_h516_surgery_h632_homomorphism_gate_review1/independent_check.py > /tmp/h516-h632-review-O.txt
diff -u hadwiger_nelson_h516_surgery_h632_homomorphism_gate_review1/EXPECTED_OUTPUT.txt /tmp/h516-h632-review-O.txt

(cd hadwiger_nelson_h516_surgery_h632_homomorphism_gate_review1 && sha256sum -c SHA256SUMS)
```

The independent check took about 2.7 seconds per run here.  Exact replay
commands for the target computation are recorded in
[`VALIDATION.json`](VALIDATION.json).

## Scope and trust boundary

The accepted statements are:

1. the fixed labelled 508-vertex surgery has no homomorphism to H632; and
2. more strongly, that same graph has no plane unit-edge map, with arbitrary
   nonadjacent identifications allowed.

Nothing here excludes a different surgery, a graph obtained by edge deletion
or repair, a different abstract carrier, or an arbitrary plane graph on at
most 508 points.  The checker derives the family size only to authenticate the
index-zero selector; it does not review the parent's all-family K2,3 cover.
No physical point set and no new chromatic certificate result.

Trust remains in the pinned public inputs, independence of the displayed
multiquadratic basis, CPython integer/Fraction and JSON semantics, SHA-256,
and ordinary hardware.  The abstract chromatic statement additionally trusts
the cited accepted H516 parent.  The decisive geometric obstruction is a
ten-edge certificate plus the elementary unit-circle parity lemma; no SAT
solver, floating point, hidden search trace, or proof-assistant formalization
is used.

Literature baseline: Jaan Parts reports the 509-vertex, 2,442-edge construction
in [arXiv:2010.12665](https://arxiv.org/abs/2010.12665).  Haugland's August 2026
paper still identifies 509 as the current unrestricted order record in
[arXiv:2608.04542v4](https://arxiv.org/html/2608.04542v4).  The newer 2,259-edge
reduction retains those same 509 coordinates and changes the edge record, not
the vertex record.
