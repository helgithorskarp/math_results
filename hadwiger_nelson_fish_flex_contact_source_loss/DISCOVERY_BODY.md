Exact computer-assisted construction lemma.  The flexible 23-vertex
Hochberg--O'Donnell fish has an exact plane realization at which the nonedge
`(10,21)` becomes a unit contact.  The 23 physical points are distinct and the
complete strict unit-distance graph has exactly 43 edges: the 42 named fish
edges and `(10,21)`, with no other contacts.

This event strictly reduces the set of complete source colourings, not merely
a projected terminal product.  The full assignment
`01110021022330110210021` is proper on all 42 fish edges but gives 10 and 21
the same colour, so it does not lift to the complete physical graph.  The full
assignment `01110021022330110210012` is proper on all 43 physical edges, so the
loss is nonvacuous.  An exhaustive deterministic three-colour decision on the
fish source returns UNSAT after 541 calls.  Hence both the source and complete
physical graph have ordinary chromatic number exactly four.

The exact support is the unique zero in a rational box of a square system of
42 squared-unit equations after fixing vertices 0 and 1 at `(0,0)` and
`(1,0)`.  A standard-library verifier uses a rational approximate inverse to
prove that `x-AF(x)` is a contraction mapping the box strictly into itself.
It then checks rational enclosures for all 253 pairs, excluding every
unlisted collision and unit contact, and directly checks both colour words.
Normal and assertion-disabled outputs agree.  A pinned `mpmath==1.3.0`
regeneration is byte-identical.  Eight mathematical corruptions are rejected
without relying on hashes.  This is author-side evidence, not independent
review or formalization.

Public source, proof and reproduction commands:
https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_fish_flex_contact_source_loss

Standard-library verifier:
https://github.com/helgithorskarp/math_results/blob/main/hadwiger_nelson_fish_flex_contact_source_loss/verify.py

From a complete checkout with Python 3.11 or later:

```text
python3 -B hadwiger_nelson_fish_flex_contact_source_loss/verify.py
python3 -O -B hadwiger_nelson_fish_flex_contact_source_loss/verify.py
python3 -B hadwiger_nelson_fish_flex_contact_source_loss/controls.py
```

Verified mathematical-package commit:
`4e900a233cd6de3ced408cfb81bd9b25844afc2b`.  Geometry-certificate SHA-256:
`e079c2d86f0b3574e6e24d9fc18a9abc2d8b7d7fe111ba011d5978875d5fc732`.
Complete edge-stream SHA-256:
`aa1c195c64beef1e6f14c57eeec13b5c9a88bfe3633051807ef5a6ee4c3aff13`.

This is a positive plane-native complete-input forcing event but not a
five-chromatic graph, a sub-509 candidate, a record advance, or a claim about
all fish flexes.  It supplies no host or cap-feasible route from this single
lost edge to five-chromaticity.  Other self-contacts and flex parameters were
not exactified or classified, and this result does not license an adjacent
sweep.  Parts's 509-point/2,442-edge construction remains the supported
unrestricted record comparison: https://arxiv.org/abs/2010.12665 .
