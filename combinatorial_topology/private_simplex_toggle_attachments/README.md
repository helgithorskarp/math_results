# Optimal toggle words survive private simplex attachments

Suppose an augmented simplicial face lattice has a winning toggle word
using each face H exactly |mu(H,top)| times. Attach simplices along
arbitrary old faces F_i, using nonempty pairwise disjoint sets of new
vertices. The resulting complex again has such a word.

If a_H attachments use H as their old intersection, the exact new
minimum length is

    number_of_attachments + sum_H |mu_old(H)+a_H|.

The compiler replaces suitable old additions with new simplex moves,
then appends a remove/add pair for each remaining simplex. It handles
coefficients that become zero or change sign, and its output is optimal
for every nonnegative assignment of move costs.

The theorem needs a certified optimal input word; it does not assert
that arbitrary nonpure shellable complexes are optimal. The private
vertices and the separately adjoined top are essential conventions.
The construction can be iterated using newly created attachment faces.

[PROOF.md](PROOF.md) proves the universal statement, exact length update,
and a nonpure cancellation family resolving the earlier four-facet
control. [REFERENCES.md](REFERENCES.md) credits the game, lower bound,
prior shelling theorem, review, and existing acyclic-family methods.

## Reproduce

From the repository root:

    python3 combinatorial_topology/private_simplex_toggle_attachments/verify.py

From this directory:

    python3 verify.py
    python3 -O verify.py
    sha256sum -c MANIFEST.sha256

Python 3.10+, tested with CPython 3.11.2; standard library only.
No downloaded input, solver, random sampling or numerical approximation.
Use --emit to print compact evidence without reading expected.json.

Expected: PASS, 20 fixtures, 14 BFS optima, 14 weighted Dijkstra optima,
354 output moves replayed, and six invalid controls rejected.
The verifier recomputes upper Möbius values by recurrence and replays
literal monochromatic-ideal moves. Shortest paths use the full legal
state graph, not the construction or its predicted bound. Tests include
zero costs, coefficients of magnitude three, reversed input words,
repeated/nested/empty attachment bases, nonshellable output, and the
shared-new-vertex failure of the coefficient formula.

These finite checks corroborate the written proof; they are not its
logical basis or independent peer review. Historical priority is not
asserted, and the general NCI conjecture has already been refuted.
The minimum size of an unwinnable lattice is not determined here.

MANIFEST.sha256 covers the other five files.
