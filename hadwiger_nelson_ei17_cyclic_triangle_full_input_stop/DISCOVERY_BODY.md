Exact computer-assisted stopping lemma for one bottom-up whole-support
construction.  Fix the certified 17-point, 31-edge, triangle-free,
four-chromatic EI17 realization from the dependency below.  Normalize any of
its 31 unit edges, in either endpoint order and either orientation, to one side
AB of a unit equilateral triangle ABC.  Take three congruent copies cyclically
on AB, BC and CA.  This enumerates all 124 labelled frames of the declared
architecture.

Exact rational interval arithmetic collision-merges every frame to 48 distinct
physical points, with exactly the three prescribed anchor identifications.  It
reconstructs a conservative complete-contact upper graph for every frame: 116
have exactly the 93 inherited edges, and eight have those edges plus three
possible cross contacts.  Every actual strict physical unit graph is a
subgraph of its checked upper graph.  The 93-edge inherited union has no
articulation vertex and no bridge in every frame.

The source has exactly 85,088 proper four-colourings modulo global colour
permutation.  Every one extends through every frame.  For the 116 contact-free
frames this follows from an explicit cyclic colour-permutation formula.  For
the eight contactful upper graphs, the checker finds and directly checks all
680,704 source/frame witnesses; a separate algorithm re-solves all 27- or
39-state reduced domain censuses.  Since each union contains the certified
four-chromatic source, every actual complete physical graph has chromatic
number exactly four.  Thus the full projection onto all 17 vertices of the
first source is unchanged: the cyclic incidence operation produces no
complete-input forcing loss despite being nonseparable.

Public exact source and proof:
https://github.com/helgithorskarp/math_results/tree/abadf3d5f33005152f588fe0a2e2a52cf0d204eb/hadwiger_nelson_ei17_cyclic_triangle_full_input_stop

Standard-library verifier:
https://github.com/helgithorskarp/math_results/blob/abadf3d5f33005152f588fe0a2e2a52cf0d204eb/hadwiger_nelson_ei17_cyclic_triangle_full_input_stop/verify.py

Reproduce from a complete checkout with Python 3.11 or later:

```text
python3 -B hadwiger_nelson_ei17_cyclic_triangle_full_input_stop/verify.py --check-expected
python3 -O -B hadwiger_nelson_ei17_cyclic_triangle_full_input_stop/verify.py --check-expected
python3 -B hadwiger_nelson_ei17_cyclic_triangle_full_input_stop/controls.py
python3 -O -B hadwiger_nelson_ei17_cyclic_triangle_full_input_stop/controls.py
```

Mathematical-package commit:
abadf3d5f33005152f588fe0a2e2a52cf0d204eb.  Geometry-stream SHA-256 is
6bb50a2375d31f15ab407fa24e5cb87ed003999eb0ee486d05c1b1e757abe913;
the plain-frame witness-stream SHA-256 is
4241349c724f01fb7af0b0e6ef45670b29920765126011df344b71eccd380df0.

This is author-side exact evidence, not independent review, a five-chromatic
graph, a record candidate, or a global EI17-gluing exclusion.  It closes only
this cyclic three-copy equilateral architecture for this one exact EI17
realization.  No adjacent copy-count, polygon, phase, or alternate-source sweep
is implied.  Parts's 509-point construction remains the supported unrestricted
record comparison: https://arxiv.org/abs/2010.12665 .
