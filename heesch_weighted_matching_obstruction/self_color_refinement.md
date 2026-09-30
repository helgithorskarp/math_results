# Canonical color refinement and a five-corona dead end

Author: **six-heesch-3**, role: researcher.

This is a structural pruning rule for [quintic_realization.md](quintic_realization.md),
checked on one specified patch. Connected-component constraints and forced
grouping are standard ideas; no historical priority is claimed.

## Canonical refinement of a fixed rotational patch

Fix a valid rotations-only grid patch. Its port graph has one vertex per
original boundary unit edge and an edge `ij` whenever ports `i,j` meet
along a shared unit edge in the patch. Include self-loops. The matching
table requires equal colors and opposite states in `{-1,0,+1}`.

Every compatible color assignment is constant on each connected component.
Assigning a different color to each component gives the strongest
compatible self-color table: every other compatible color assignment
coarsens that partition. If the strongest color-only marking tiles the
plane, every compatible coarser color-only marking also tiles by relabeling.

The state equations are `s_i+s_j=0`. An odd closed walk takes a state to
its negative, so all states on a nonbipartite component are zero. On a
bipartite component they are a common `t` on one side and `-t` on the
other, with `t` in `{-1,0,+1}`. This is the earlier elementary port-graph
calculation, but balanced components may now impose directions without
providing nonzero additive charge. Thus a color-only tiling certificate
does not generally eliminate directed refinements: also prove that every
component is nonbipartite.

This reduces color-only refinement of one fixed patch to one canonical
instance. Multiple components alone do not prove finiteness.

## Specified baseline and reinterpretation

Use [signed_hex4_depth5.witness.json](signed_hex4_depth5.witness.json), with
SHA256 `d857774a28daa5e8f28e45a4ce711cc45ebc11cb759904fa98309122892aed0a`.
Its base is the straight four-cell polyhex `[(0,0),(1,0),(2,0),(3,0)]`.
Its layer counts are `1,5,11,23,39,52`, and all prefixes are discs. Its
original complementary-signed marking with reflections is the previously
documented Heesch-five reproduction.

For this mirror-symmetric base only, reinterpret every reflected geometric
copy as an unreflected copy with the same turn and normalized translation.
First check that each of the 57 changed records has exactly the same cell
footprint. Then erase the old signs and directly check the resulting
unmarked five-corona patch. Cell sets, corona completeness, contacts and
prefix topology are unchanged. The old signed marking is not preserved;
this is not a conversion of its finite Heesch-five result.

The reinterpreted port graph has **51 distinct pairs** and two components:
ports `0,...,16`, with self-loops at `5,15,16`, and port `17`, with its own
self-loop. Port zero is directly adjacent to every port `1,...,16`, so the
first component is connected. Both components are nonbipartite. Every
compatible directed state is therefore zero. Every compatible color is
constant on ports `0,...,16`; only port `17` may have a different color.
The strongest assignment is `[1,...,1,2]`, with seventeen entries of one.

## The strongest refinement tiles periodically

Port `17` is the interface between cell centers `(3,0)` and `(4,0)`. It is
the unique color-two port, so its mate in a fully covered tile must be
that same port on another copy. Equal-handed matching forces a half-turn
about the interface midpoint, namely `p -> (7,0)-p` on axial cell indices.
The two copies form the eight-cell strip `[(0,0),...,(7,0)]`, with no
overlap. Their private-color ports pair internally; every remaining
boundary port has color one.

Repeat the motif with periods `(8,0)` and `(0,1)`, using these copies:

```
turns 0, normalized translation (0,0);
turns 3, normalized translation (4,0).
```

There are no reflections. The period determinant is eight and the motif
represents each of the eight cell classes exactly once. A separate
inverse-motion checker examines all 36 boundary-port incidences, including
interfaces crossing a period boundary. All colors match; precisely two
incidences form the internal private-color pair. This tiles the marked
grid, and the quintic network deformation gives a plane tiling of the
unmarked curved shape.

Every coarser color assignment also tiles by the motif; every compatible
directed state was already forced to zero. Consequently **every** marking
of the stated color/state type compatible with this fixed uniform
five-corona patch tiles the plane. None yields a finite Heesch record. A
different patch is necessary for this route.

## Reproduction and limits

```
python3 heesch_weighted_matching_obstruction/self_color_refinement.py
```

Compare the output with [self_color_expected.json](self_color_expected.json).
The standard-library checker reads the hash-pinned witness, checks all
changed footprints and prefix conditions, reconstructs the graph, verifies
its components and loops, and checks the periodic motif by inverse cell
ownership. No solver, large certificate or external data is needed. The
geometric realization and global deformation remain written proofs.

This excludes refinements only of the specified reinterpreted patch. Other
five-corona patches and the original mixed-handed quartic model remain
unclassified by this statement. No new record is established.
