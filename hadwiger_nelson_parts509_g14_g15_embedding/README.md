# Exact G14/G15 embeddings in the Parts-509 completion geometry

## Result and scope

This directory independently reconstructs the recently published three-distance
graphs `G14` and `G15`, then identifies exact copies in the geometry surrounding
Jaan Parts's 509-vertex unit-distance graph `G`.

Let

\[
D=\{1,1/\sqrt3,2\}.
\]

Two points are adjacent in a `D`-distance graph when their Euclidean distance is
in `D`.  Exact arithmetic and a solver-free exhaustive coloring computation
verify the source invariants

```text
       vertices  D-edges (1, 1/sqrt3, 2)  chi  alpha
G14          14             (18, 27, 5)      6      3
G15          15             (22, 30, 4)      6      3
```

The new structural observations are:

1. `G15` is realized on the following zero-based Parts vertex indices, in the
   canonical source order:

   ```text
   0, 157, 165, 149, 168, 152, 160, 66, 63, 60, 57, 54, 69, 204, 216
   ```

   All 105 squared distances agree exactly with the canonical carrier.

2. Each of the two exact isometries of that carrier onto this Parts subset
   extends the canonical `G14` carrier into the certified completion geometry
   `V(G) union Q3`.  Each image uses ten Parts vertices and four of the 1,158
   external points with at least three unit neighbors in `V(G)`:

   ```text
   image A: V={0,54,57,60,63,66,69,157,160,207}
            Q3={470,523,619,653}

   image B: V={0,54,57,60,63,66,69,165,168,213}
            Q3={411,417,454,750}
   ```

   The complete 91-pair distance matrix is checked for each image.  Seven of
   the eight external points have four Parts neighbors; `Q3[750]` has three.

3. Consequently every proper 5-coloring of the Parts unit-distance graph has,
   among the fifteen displayed vertices, a monochromatic pair at distance
   `1/sqrt(3)` or `2`.  Indeed, the restriction already respects the 22 unit
   pairs.  If it also separated every one of the 30 distance-`1/sqrt(3)` pairs
   and four distance-2 pairs, it would be a proper 5-coloring of `G15`, contrary
   to `chi(G15)=6`.

This is a structural bridge between a small few-distance obstruction and the
current 509-vertex unit-distance record geometry.  It does **not** produce a
smaller 5-chromatic unit-distance graph and does not improve
`5 <= chi(R^2) <= 7`.  The `G14` and `G15` objects themselves are prior work;
only their exact occurrence in the Parts/completion geometry is presented as a
new finding.  Targeted literature, repository, and committed-graph searches
through 2026-09-01 found no explicit statement of these embeddings, but no
priority claim is made.

## Exact verification

Use CPython 3.11 or newer.  Keep the environment under `/scratch`:

```bash
python3 -m venv /scratch/parts-g14-g15-venv
/scratch/parts-g14-g15-venv/bin/pip install -r requirements.txt
/scratch/parts-g14-g15-venv/bin/python verify_embedding.py
/scratch/parts-g14-g15-venv/bin/python independent_sympy_check.py
```

The primary checker uses rational coefficient vectors in
`Q(sqrt(3),sqrt(5),sqrt(11))` after the already-audited Parts coordinate parser.
It:

- reconstructs all `G14`/`G15` edges in `Q(sqrt(3))`;
- computes the exact chromatic number without a SAT solver, by dynamic
  programming over every independent vertex subset (at most `2^15` masks);
- checks each complete distance matrix against its claimed image;
- reparses the completion-point coefficient vectors and rescans every cited
  point against all 509 Parts vertices.

Expected leading and final fields are:

```text
"all_checks": true
G14: vertices=14, edges=50, chromatic_number=6, independence_number=3
G15: vertices=15, edges=56, chromatic_number=6, independence_number=3
"g15_forcing": "every proper 5-coloring ..."
```

The independent checker imports none of the primary checker or either sibling
field implementation.  It denests the published coordinates into SymPy's
`AlgebraicField(QQ, sqrt(3), sqrt(5), sqrt(11))`, rebuilds the eight completion
points from their rational radical coefficients, checks 105 + 2*91 complete
distance equalities, and independently rescans all eight neighborhoods.  It
must report:

```text
"independent_sympy_check": true
"g15_complete_distance_checks": 210
"g14_complete_distance_checks": 182
"completion_point_rescans": 8
```

## Provenance

The canonical `G14`/`G15` coordinates and the claims `chi=6`, `alpha=3` are
from the MIT-licensed source:

<https://github.com/HeliCorgi/fourteen-points-six-colors>

The certificate records source commit
`4c84e4d67522e644faef704694cd5ba7fc273abc` and the SHA-256 hashes of the two
exact coordinate files.  `SOURCE_LICENSE.txt` preserves its license.  This
directory stores the same coordinates more compactly as four rational
coefficients per point.

The Parts construction and its exact coordinates are from:

- Jaan Parts, *Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane*, Geombinatorics 29(4) (2020), 137--166,
  <https://arxiv.org/abs/2010.12665>.
- The sibling `../hadwiger_nelson_parts509_criticality` independently certifies
  the strict 2,442-edge graph and its 5-vertex-criticality.
- The sibling `../hadwiger_nelson_parts509_swap_closure` exactly enumerates the
  1,158 external completion points used here.

## Trust boundary

- The small-graph reconstruction and chromatic-number calculation trust
  CPython integer/rational arithmetic and the compact coordinate input.  No SAT
  solver or proof log is used.
- The primary embedding checker trusts the sibling Parts parser (including
  SymPy 1.14.0 for denesting the four apparent nested radicals), its small
  rational multiquadratic-field implementation, and the published coordinate
  input.  Every equality after parsing is a rational-coefficient comparison.
- The independent geometry checker replaces that arithmetic by SymPy's
  `AlgebraicField`; it shares only the input files, certificate schema, and
  theorem statement.
- The statement that the completion list is exhaustive is inherited from the
  separately certified swap-closure contribution.  This directory independently
  verifies only the coordinates and full Parts neighborhoods of the eight cited
  entries.
- Neither checker is a proof-assistant formalization.  Source publication and
  two software implementations are not a substitute for formal verification.
