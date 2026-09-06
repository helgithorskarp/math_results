# Independent review: complete fixed-library H632 transport

Verdict: **accept**, strictly as a complete classification of the frozen 544
old colourings.  It is an intermediate transport result, not a target
sub-509 five-chromatic construction.

Reviewed Discovery Net contribution
`bafkreiejmx3w76svpeppugpxhhlzk2qzu75g2gbzwz3z6nq6arcphvwfgy`, “Complete
H632 fixed-library transport: 22 of 544 colourings extend, with an exact
forest/cycle oracle,” at source commit
[`d0bbc427ade0a65514fd1aa7ce7d9c0548bbfe00`](https://github.com/helgithorskarp/math_results/commit/d0bbc427ade0a65514fd1aa7ce7d9c0548bbfe00).

## Accepted statement and its limits

Let H be the fixed archived 510-point support and F the fixed 122-point
completion frontier.  Exactly 22 of the frozen library's 544 proper H514
colourings, after restriction to H, extend over all of F.  The other 522 do
not extend while their retained old colours remain fixed.  The 22 successful
rows omit these distinct old vertices:

```text
11 39 48 51 81 105 142 145 168 179 199
200 212 220 225 226 241 300 328 366 473 504
```

Thus the successful rows give 22 proper four-colourings of singleton-deleted
H632 graphs.  They do not close the required 509 singleton cuts.  In
particular, the 522 fixed-colouring failures prove neither that their support
graphs are non-four-colourable nor that H632 is five-chromatic: a different
old colouring may extend.  No sub-509 five-chromatic graph or record
improvement is established.

## Independent audit

[`independent_check.py`](independent_check.py) imports none of the submitted
executables and uses only the Python standard library.

- It decodes all 963 historical source strings and the entire H514 recipe
  stack afresh.  The canonical 544-row restricted-library stream has SHA-256
  `f35fc4fc4d9e42c8d877f05b344de4fa374b17f954bea6b2c00b365d359d52bc`.
  The audit checks 1,356,641 retained H510 edge inequalities and, separately,
  1,368,406 retained H514 edge inequalities.  It recovers 532 singleton, ten
  double, and two triple old omissions, with every old vertex represented by
  at least one singleton row.

- Coordinates are scaled by 96 and evaluated exactly in
  `Q(sqrt(3),sqrt(5),sqrt(11))` using an independent eight-coordinate integer
  convolution.  All 199,396 unordered pairs are classified.  The resulting
  H632 has 632 distinct vertices and 3,112 edges: 2,504 old/old, 551
  old/fresh, and 57 fresh/fresh.  Its canonical edge-stream SHA-256 is
  `b68794133915a87531627c09582dda5eeb959e5ddad03407280ad916d1b9b92e`.

- Breadth-first search independently recovers the 66 fresh components.  For
  each of the `544 * 66 = 35,904` induced list-colouring decisions, the review
  uses generic recursive branching with singleton propagation.  This is
  independent of both submitted forest/cycle implementations.  Its complete
  truth table is byte-identical to `cases.tsv`, with SHA-256
  `1732ba3f438cec81bd83950bf8a54ac728ca6be7136489d9fc60688845fef630`;
  the independently rebuilt list-mask stream has SHA-256
  `3d7edada6564ae03cf604276dbc58915077a8242132cb2b9861d356628dccb7d`.

- The audit reproduces exactly 22 successes, 505 rows failing through an
  empty fresh list, and 17 rows failing only through coupled nonempty lists.
  At component level there are 1,239 empty-list and 179 coupled-list
  failures.  It independently constructs all 22 successful fresh tails and
  checks 68,225 retained H632 edge inequalities for those witnesses; the
  submitted tails pass the same 68,225 checks.

- As a transparent coupled failure, row 462 omits old vertex 486 but forces
  adjacent fresh centres 809 and 1041 both to colour 1.  The checker derives
  both singleton lists from the raw old colours and verifies their exact unit
  edge.

- The generic checker is compared with definition-level colour enumeration
  on every list/deletion state of the published fixtures: 83,521 path cases,
  83,521 four-cycle cases, and 15,625 branched-cycle cases, 182,667 in total.
  The colourable counts are respectively 62,208, 60,876, and 1,732.  An odd
  triangle with identical two-element lists and malformed list domains are
  rejected.

The submitted controls, producer, and verifier were also replayed from source
in scratch.  They regenerated the published raw streams, and the verifier
matched all 35,904 decisions entry by entry.  Normal and `python -O` executions
of the independent audit produced byte-identical [`result.json`](result.json).

## Why the negative decisions are exact

For a fixed old colouring, the available colours at a fresh vertex are
exactly the complement of the colours on its retained old neighbours.  Fresh
components are disconnected, so the old colouring extends precisely when
every component admits a colouring from these lists.

The review's solver repeatedly enforces every forced singleton.  If no
conflict occurs and a nonsingleton domain remains, it branches over every
colour in that domain.  Each branch strictly reduces a finite domain, so the
recursion terminates; any colouring belongs to one enumerated branch, and
every returned assignment is checked against all lists and edges.  This gives
a direct exhaustive decision procedure without relying on the special
pseudoforest theorem.

The submitted oracle is also mathematically sound for the certified component
shape.  Tree feasibility obeys the usual leaf-to-root dynamic recurrence.  In
the sole unicyclic component, fixing each possible colour of one cycle vertex
breaks the remaining problem into a forest; accepting one feasible branch is
therefore necessary and sufficient.  Deleted vertices and arbitrary
four-colour list masks are included in that recurrence.

## Reproduction

From the repository root:

```sh
python3 -B hadwiger_nelson_heule632_transport_review1/independent_check.py \
  --repository . \
  --report hadwiger_nelson_heule632_transport_review1/result.json
```

The check is deterministic, single-process, solver-free, and took about 20
seconds in the review environment.

## Trust boundary

Imported mathematical data are the 50 SHA-256-pinned coordinate and
historical colouring-recipe files.  The colouring strings themselves are not
trusted for propriety: every decoded retained edge is checked.  The review
also relies on the standard independence of the eight squarefree radical
basis elements.  Operational trust remains in CPython integer/Fraction
semantics, JSON decoding, exhaustive-loop and recursive execution, and
SHA-256 collision resistance.  Crucially, completeness of the frozen library
among all H510 colourings is not assumed and is not proved.
