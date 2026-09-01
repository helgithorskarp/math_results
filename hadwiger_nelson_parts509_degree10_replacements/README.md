# Four exact degree-10 completion points do not yield a 508-vertex graph

## Exact result

Let `G` be the strict unit-distance graph on the 509 algebraic points in the
Parts construction: every pair of listed points at Euclidean distance exactly
one is an edge.  Define four further points

\[
q_{\epsilon,\delta}
=\left(\frac{\epsilon}{6},
       \frac{\delta\sqrt3+2\sqrt{11}}6\right),
\qquad \epsilon,\delta\in\{-1,1\}.
\]

Exact arithmetic in `Q(sqrt(3),sqrt(5),sqrt(11))` shows that the four points
are distinct from the 509 Parts points and that each has exactly ten unit
neighbors in `G`.  For every one of the four choices of `q` and every
two-element subset `D` of the Parts vertices, the strict unit-distance graph on

\[
(V(G)\setminus D)\cup\{q\}
\]

is 4-colorable.  Thus none of these four two-delete/one-add augmentations gives
a 5-chromatic unit-distance graph on 508 vertices.

This closes exactly

\[
4\binom{509}{2}=517{,}144
\]

candidate graphs.  It is a negative local search, not a proof that the
509-vertex record is globally minimal.  In particular, it says nothing about
other added points, adding several points at once, changing several coordinates,
or using a different ambient construction.

## Certificate structure

The previously published vertex-criticality certificate in
`../hadwiger_nelson_parts509_criticality` contains a proper 4-coloring of
`G-v` for every vertex `v`.  Restricting one of those rows by one further
deletion and coloring `q` with a missing neighbor color directly settles
503,154 of the 517,144 cases.

The remaining 13,990 instances occur on 12,578 distinct deleted pairs.
`certificate.bin` contains 13,473 proper coloring witnesses; a single witness
can sometimes cover more than one of the four added points.  The format has a
16-byte header followed by fixed 132-byte records:

- two little-endian 16-bit deleted vertex indices;
- 510 two-bit colors packed into 128 bytes, including the added point as
  vertex 509.

The primary solver-free verifier reconstructs the 2,442 base edges and all four
candidate neighborhoods exactly, rechecks the earlier 509 deletion colorings,
checks 32,624,299 retained-edge inequalities in the new witnesses, and confirms
that every instance is covered.  A second checker imports none of the primary
code; it independently decodes and replays the same coverage argument against
the committed edge and neighborhood manifests.

## Solver-free verification

Use CPython 3.11 or newer.  Keep the environment under `/scratch`:

```bash
python3 -m venv /scratch/parts509-replacement-venv
/scratch/parts509-replacement-venv/bin/pip install -r requirements.txt

/scratch/parts509-replacement-venv/bin/python \
  pair_replacement.py verify certificate.bin
python3 independent_check.py certificate.bin
```

Both commands should report `all_checks: true`, together with:

```text
two_deletion_instances = 517144
instances_covered_by_prior_deletion_rows = 503154
residual_instances = 13990
certificate_records = 13473
retained_edge_inequality_checks = 32624299
```

## Regenerating the witnesses

Generation uses MiniSat 2.2 through PySAT only to find colorings.  Models are
decoded and checked before being written.  The generated certificate may have
different valid colorings and therefore a different hash.

```bash
/scratch/parts509-replacement-venv/bin/python \
  pair_replacement.py generate \
  /scratch/parts509-degree10-certificate-new.bin \
  --solver minisat22 \
  > /scratch/parts509-degree10-generation.log
```

The generator uses a standard four-color CNF without redundant at-most-one
clauses.  Each vertex selects at least one color and adjacent selected-color
sets are disjoint, so choosing one selected color at each vertex gives an
ordinary proper coloring.  A fixed triangle receives deletion-conditional
color pins.  Candidate edges are activated by selector literals.  None of
these encoding details enters the solver-free witness replay.

## Hashes

```text
certificate.bin
  f2608be542d4455ba1719a6273321b69fd0aea1459e42c7118ba5387326cba42
base 2442-edge canonical list (lines "u v\n")
  5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c
base coordinate file (in sibling contribution)
  770a585a6c1e1222355322707479cb826e9ada560279da904ef89c15c99ff0b5
base packed vertex-deletion witnesses (in sibling contribution)
  be5c4c0d333552334ae6d343d000f84456be50f8ef9e7f95d64ca92779390d36
```

## Status and trust boundary

This is an exact computer-assisted negative sub-search and a structural fact
about four explicit high-incidence completion points.  It is not a smaller
5-chromatic graph and does not improve the bounds
`5 <= chi(R^2) <= 7`.  No novelty or priority claim is made; a targeted search
found no previously published certificate for these four points, but the
result may be implicit in earlier minimization experiments.

The exact geometry layer trusts the Parts coordinate input, CPython
`fractions.Fraction`, SymPy 1.14.0 parsing/denesting, and the small
multiquadratic-field implementation in the sibling contribution.  The new
4-colorability conclusion does not trust MiniSat: all returned colors are
stored and replayed directly.  The primary checker depends on the previously
certified Parts deletion rows; the independent checker separately parses and
checks those rows but trusts the committed edge and candidate-neighbor
manifests.  Neither checker is a proof-assistant formalization.

## Context

- Jaan Parts, *Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane*, Geombinatorics 29(4) (2020), 137--166,
  <https://arxiv.org/abs/2010.12665>.
- Marijn J. H. Heule, *Computing Small Unit-Distance Graphs with Chromatic
  Number 5*, Geombinatorics 28(1) (2018), 32--50,
  <https://arxiv.org/abs/1805.12181>.
- The exact base reconstruction and complete one-vertex deletion certificate
  are in `../hadwiger_nelson_parts509_criticality`.

Parts explicitly distinguishes graph *minimization* (which may add vertices)
from deletion-only reduction.  The present search probes one small, exact
augmentation--replacement neighborhood of that frontier.
