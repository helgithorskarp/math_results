# Independent review: fixed 122-centre incidence and two-choosability

Verdict: **accept**, with the claim restricted to the fixed archived table of
122 completion centres.

Reviewed Discovery Net contribution
`bafkreiapqhphqnrryhl72riy4crzdtfh2dzzcft53i6iraa4xoaqdjnouu`, “The fixed
122 Heule completion centres are two-choosable: 65 trees and one four-cycle
component,” at source commit
[`ac6553bd4ede54bea77c6ef4bd66c02638d8f297`](https://github.com/helgithorskarp/math_results/commit/ac6553bd4ede54bea77c6ef4bd66c02638d8f297).

## Accepted statement and limits

Let H be the archived 510-point Heule support and F the 122 explicit points in
`hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json`. The
strict unit-distance graph induced by F has 57 edges and 66 components: 65
trees and one 37-vertex unicyclic component whose unique cycle is

```text
1239 -- 1370 -- 1522 -- 1371 -- 1239.
```

Consequently F and every subgraph of F are two-choosable. If a proper
four-colouring of any retained subset of H gives at most two distinct colours
to the retained old neighbours of each selected fresh vertex, it extends over
those fresh vertices. The stated tree dynamic program, with at most four
forest tests for the cyclic component, also decides extension for arbitrary
four-colour lists.

This establishes neither four-colourability nor non-four-colourability of the
full 632-point H∪F support. It produces no sub-509 five-chromatic graph and no
record improvement. It treats the fixed table as the definition of F and does
not re-establish the historical 21,978,620-triple search that found it.

## Independent exact audit

[`independent_check.py`](independent_check.py) imports no submitted executable
code and uses only the Python standard library.

- Coordinates are scaled by 96 and evaluated exactly in
  `Q(sqrt(3),sqrt(5),sqrt(11))` through an eight-vector integer coefficient
  convolution. All 7,381 fresh pairs and 62,220 fresh/old pairs are checked.
  The audit finds 632 distinct points, 57 fresh edges and 551 old attachments.
  Its 69,601-vector norm stream has SHA-256
  `f319dfe814bb9a2259a914b74c79adde9272422e4e761d57dc308fc750a638f7`;
  the canonical fresh-edge stream has SHA-256
  `76bb5adb53ddc6cb7def884a6a999cf3d570af5ed27bbb3a199be6eba3e012d4`.

- Components are rebuilt by breadth-first search. Instead of either submitted
  cycle algorithm, the review removes each of the 57 edges in turn and tests
  endpoint connectivity. Exactly 53 edges are bridges; the other four are
  precisely the displayed cycle. The component-order histogram is
  `1:55, 2:7, 4:1, 6:2, 37:1`, and the complete edge/component certificate
  matches entry by entry.

- The independently recovered old-attachment classes are 43 L-only, 75
  S-only and four mixed centres `170,436,1239,1527`. Each mixed centre has
  old L-neighbour set `{0}`. Fresh edge types are `LL:1, MM:3, MS:7, SS:46`,
  with no L-to-M or L-to-S edge. The 37-vertex component contains the four
  mixed and 33 S-only centres and meets 100 distinct old S vertices.

- For the four-colour application, all `6^4 = 1,296` assignments of
  two-element lists to the certified C4 are tested by direct colouring
  enumeration. For every case, the checker constructs a complete list
  colouring of all 122 vertices by extending outward through the attached
  trees. The identical two-list assignment on an odd triangle is correctly
  rejected as a parity control.

The author verifier was also replayed separately and returned the same exact
incidence, cycle and 1,296-list totals. The machine-readable independent audit
is [`result.json`](result.json).

## Combinatorial derivation

Every tree is two-choosable: pick a root colour and move outward, where only
the parent colour is forbidden. For an even cycle with two-element lists, use
alternation when all lists agree. Otherwise choose adjacent vertices `u,v`
with different lists, colour `u` from its list outside the list of `v`, and
greedily traverse the cycle so that `v` is last. The closing edge is safe
because the colour of `u` is unavailable at `v`. Attached trees then extend
greedily. Lists of size greater than two reduce to arbitrary two-element
sublists, so this proof is not limited to a four-colour universe.

For the extension corollary, give each selected fresh vertex the complement in
`{0,1,2,3}` of the colours used on its retained old neighbours. The hypothesis
makes every list have size at least two; a list-colouring of F then satisfies
all old/fresh and fresh/fresh edges.

For arbitrary lists, the feasible colours at a tree vertex are exactly those
for which every child subtree has a feasible colour different from the parent
choice. This follows inductively from the leaves. If the C4 remains, fixing a
colour of one cycle vertex and deleting that colour from all its neighbours
leaves a forest. Trying its at most four colours is therefore both necessary
and sufficient.

## Reproduction

From the repository root:

```sh
python3 -B hadwiger_nelson_heule_fresh122_incidence_review1/independent_check.py \
  --repository . \
  --report hadwiger_nelson_heule_fresh122_incidence_review1/result.json
```

The check is deterministic, single-process and solver-free, and took about six
seconds in the review environment.

## Trust boundary

The remaining imported mathematical data are the two SHA-256-pinned coordinate
tables and the standard degree-eight independence of the squarefree radical
basis. Operational trust remains in CPython integer/Fraction arithmetic,
faithful JSON decoding, exhaustive-loop execution and SHA-256 collision
resistance. The two-choosability and extension conclusions also use the
elementary tree/even-cycle arguments above. No previous colouring library,
solver result, original centre-enumeration completeness claim, H514 closure or
other support theorem is a premise.
