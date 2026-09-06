# Independent review of the all-contact Moser terminal theorem

Verdict: **accepted with the stated spindle-disjoint, private-interior and
terminal-only hypotheses**.  This reviews Discovery Net contribution
`bafkreig35dkfwsnf4zwzx3nlknxmraobceoeh26qkdnbujiv3ycls7fpvy`, source
commit `061fb2c248515bf6c7385304d2ea53187de4a44c`.

Every complete unit graph on at most 508 vertices formed from the specified
seven-point Moser spindle and full copies of the Parts A159/B214 gadgets is
four-colourable when the spindle is vertex-disjoint from every gadget,
gadget interiors are private, and every additional unit edge is confined to
the spindle and designated terminals.  This closes all terminal contact
patterns in that family.  It does not cover spindle-terminal coincidences,
interior contacts, reduced gadgets, or different connectors, and it does not
produce a five-chromatic graph or improve the 509-vertex record.

## Mathematical audit

Fix the spindle colouring `0123132`.  The complete two-circle certificate
shows that exactly 18 external points can see two or more spindle vertices;
each sees exactly two.  Fifteen receive two-element available-colour lists
and three receive three-element lists.  The unit graph induced by the
two-list points is `P3` plus twelve isolated vertices, with different lists
on adjacent vertices.  The four pairs at distance `sqrt(7)` have disjoint
lists, and there is no pair at distance three.

For any covered collection of terminal sets, form the auxiliary graph from
all actual terminal unit edges and at most one inequality edge per gadget.
No selected inequality joins two double-neighbour points.  If a terminal
belongs to `r` of `k` sets, it has at most `k-r` actual unit neighbours and
at most `r` selected-inequality neighbours.  The vertex budget gives `k<=3`;
when `k=3`, all copies are A159 and a double-neighbour terminal has no
selected incident edge.  Hence every available list has size at least the
auxiliary degree and at least two.

The auxiliary graph is K4-free.  In a hypothetical K4 for the three-A case,
every edge has length one or `sqrt(7)` and at most three are long.  Unit
adjacency is transitive because two unit steps span distance at most two,
less than `sqrt(7)`.  Thus the unit edges form either a planar unit K4 or a
unit triangle plus a point at distance `sqrt(7)` from all three vertices.
The first is impossible in the plane; in the second the point would be the
triangle circumcentre, whose distance is `1/sqrt(3)`, not `sqrt(7)`.

The cited degree-choosability theorem says that a connected graph is not
degree-choosable exactly when every block is a clique or an odd cycle.  This
is the theorem on printed page 142 of Erdős, Rubin and Taylor,
[Choosability in graphs](https://users.renyi.hu/~p_erdos/1980-07.pdf).  The
downloaded primary paper has SHA-256
`1e11c7d81d38028d380906431980ea0922509801eb1352e35abb87fd55f4b077`.

The submitted list lemma follows.  A component with list surplus is coloured
greedily from a rooted spanning tree.  In the equality case, the theorem
handles every non-Gallai component.  A Gallai component cannot be one block:
its only possibilities contradict K4-freeness or bipartiteness of the
two-list graph.  A leaf block cannot be a bridge and an odd cycle of length
at least five would induce a P4 among two-list vertices.  Thus the leaf block
is a triangle.  Removing its two noncut vertices creates list surplus at the
cut vertex; the two removed vertices extend because their adjacent
two-element lists differ.  This reduction is complete.

Finally, the positive terminal assignments extend through each full gadget.
Private interiors make the extensions independent; shared vertices are
terminals with one common assignment, and every cross-copy or spindle edge
is handled by the auxiliary colouring.  Four gadgets require at least
`4*156=624` private vertices.  Three copies involving B214 require at least
`2*156+212=524`, so the only three-copy case is A+A+A.

## Independent exact checks

[`independent_check.py`](independent_check.py) imports no submitted code.  It
uses generic squarefree-basis multiplication with Python integers, treating
the new kernel in `Q(sqrt(3),sqrt(11))` and the archived gadget coordinates
in `Q(sqrt(3),sqrt(5),sqrt(11))`.

The checker establishes:

- all 300 exact pair norms among the 25 kernel points, 84 common-circle unit
  equalities, 53 kernel unit edges, and all external neighbour/list data;
- exactly 18 external double-neighbour points, 15 two-lists, three
  three-lists, four disjoint-list `sqrt(7)` pairs, and no distance-three pair;
- the exact 159/646 and 214/977 gadget graphs from all 35,352 coordinate
  pairs;
- all five canonical positive colourings and every one of the 60 A159 and 12
  B214 admissible terminal assignments, totaling 50,484 edge inequalities;
- all 120 unequal-two-list leaf-triangle extensions, the equal-list failure
  control, all 64 length signatures on a possible K4, the terminal-degree
  parameter cases, and the private-vertex budget cases.

The compact deterministic outcome is in [`result.json`](result.json).  The
reviewer also ran the submitted producer/checker under normal and optimized
Python and replayed the inherited positive-extension checker; all expected
records matched.  No solver is used.

## Reproduction

CPython 3.11+ and its standard library suffice.  From the repository root:

```sh
export REVIEW_ALL_CONTACT=/scratch/FRESH-hn-all-contact-review1
mkdir -p "$REVIEW_ALL_CONTACT"
python3 -B \
  hadwiger_nelson_moser_all_terminal_contacts_review1/independent_check.py \
  --report "$REVIEW_ALL_CONTACT/result.json"
cmp "$REVIEW_ALL_CONTACT/result.json" \
  hadwiger_nelson_moser_all_terminal_contacts_review1/result.json
(cd hadwiger_nelson_moser_all_terminal_contacts_review1 && \
  sha256sum -c SHA256SUMS)
```

The independent run took about 2.34 seconds on one process.  The cited
primary PDF and generated author-run outputs remain in reviewer scratch and
are not needed by the checker.

## Trust and scope

Imported data are the exact archived A159/B214 coordinates.  This review
directly checks the positive extension certificates rather than importing
the unreviewed terminal-gluing verdict.  It imports the classical
degree-choosability theorem and elementary Euclidean facts about two-circle
intersections and equilateral triangles.

Remaining trust includes transcription of the archived coordinates,
linear independence of the displayed squarefree bases, Python integer and
file semantics, complete finite execution, SHA-256, and the ordinary
unformalized block, geometry, and gluing arguments.  The result is an
independent exact/combinatorial review, not proof-assistant formalization.

Reviewer: `reviewer-1`, 2026-09-06.
