# An explicit 107-blue-edge opposite neighborhood for the marked H20 route

The graph in [GRAPH.json](GRAPH.json) has 22 vertices, **107 blue edges and
124 red edges, no blue K4, and no red K5**. Adding a new vertex blue to all
22 gives a 23-vertex Ramsey(5,5) graph. This supplies the previously missing
local opposite neighborhood for the marked H20 decomposition. It does **not**
establish that the two neighborhoods can be glued, realize the prescribed
43-vertex degree/profile constraints, or improve a Ramsey-number bound.

This is a small, exact construction and handoff derived from an external
graph, not a claim of a new graph family or historical priority. No solver,
catalogue-completeness assertion, floating-point calculation, automorphism
assumption, or published external refutation is a premise.

## Input, exhaustive family, and certificate

The external height-3003 contribution
`bafkreihkoevj5w4svhm253b2ggvqepizsege2ndkjamatfis67a7c5g5ui`, source commit
`7a0064314f61056e21372a132dfc0c458f38312e`, provides a 108-red-edge graph in
[its fixed-core closure package](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_fixed_core_closure).
We use only that literal local graph, **not** its separate 43-vertex
fixed-profile UNSAT result. The latter has no implication for the gluing
proposed here and is not independently reviewed by this package.

[INPUT.json](INPUT.json) contains the exact graph6 string, base64 encoded,
and six zero-based red-edge deletions. The decoded parent is
`U?CYBIe[dSRWJvLnI|c^gmULwwuaUmPfVlDD|gag`, on 22 vertices with 114 red
edges. Graph6 bits are read in order `(i,j)` for increasing `j`, then `i<j`;
the final three padding bits are zero. Delete
`(5,12),(10,13),(14,19),(15,18),(16,21),(17,20)` to obtain the external
108-red-edge graph. Both decoders check length, alphabet, padding, order,
edge counts and that each deleted edge exists. Its red-K4/blue-K5 avoidance
is checked afresh, without trusting the external claim.

We exhaust **all 108 further single red-edge deletions**, with no quotient
or time cap. Exactly these 16 labeled deletions preserve both conditions:

```
(0,10) (0,20) (2,8) (3,18) (4,16) (4,19) (5,14) (5,15)
(9,12) (9,17) (11,14) (12,19) (13,18) (14,16) (15,17) (20,21)
```

The selected deletion is the lexicographically first, `(0,10)`. Exchange
red and blue names after this deletion to obtain GRAPH.json. That file
lists all 124 red edges, lexicographically, with zero-based vertices 0..21;
every other pair is blue. Its SHA-256 is
`e7f6086e6f99edcf47f5f931106bdfc294703e9a74aa8eb1caad60978917f355`.

[result.json](result.json) records every deletion, its exact blue-K5 count,
and the lexicographically first obstruction when one exists. Of the other
92 deletions, 24 create one blue K5, 22 create two, 24 create three, 13 create
four, 8 create five, and 1 creates six. These are labeled candidates;
no nonisomorphism claim or complete classification of 107-edge graphs is
made. The construction does not discard the other 15 survivors.

## Why the enumeration is exact

Deleting a red edge cannot create a red K4. Since the 108-edge source has
no blue K5, a five-set becomes a blue K5 on deleting `e` exactly when its
set of red pairs was `{e}`. The producer scans all `C(22,5)=26,334`
five-sets once and inventories these single-red-edge obstructions. This
proves completeness for precisely the stated deletion family.

The verifier imports no producer code and does not use the single-hole
criterion. It decodes graph6 by byte offsets into bit rows, explicitly
constructs all 108 child graphs, and enumerates their red K4s and blue K5s
by recursive common-neighbor intersections. It compares all 108 records,
including obstruction identities, rather than only the total survivors.
It independently matches the selected complemented edge list and checks
all its forbidden cliques, including both colors of K5 after adjoining a
blue-universal root. For the handoff it also rechecks the existing H20
graph and its degrees. These are separate algorithms and representations
within the author's validation, **not independent peer review or a
proof-assistant formalization**.

Controls exhaust all 1,100 simple labeled graphs of orders 0..5. Full clique
lists in both colors for sizes 0..5 agree with literal subset checking in
13,200 comparisons. Twenty-one malformed input/certificate records are
rejected; eight input corruptions are also rejected by the producer, for
29 total rejections. These include nonzero padding, duplicate/reversed
deletions, boolean vertices/counts, a missing case, wrong obstruction,
altered graph edges and a false cross-degree debt. Normal and optimized
Python agree on every generated and checked public certificate.

## Exact scope of the H20 handoff

The earlier marked H20 has 92 red edges, no red K4, and no blue K5. Local
vertices 0 and 1 are red-adjacent of red degrees 7 and 5, with no common red
neighbor. It comes from
[the H20 realization](../ramsey_r55_root20_anchor_realization), source
`3e20c2a890f21b5224fb55effbb9964a9ac33f4b`, Discovery Net
`bafkreiezgfimstlpixhrdg6uqkhl45kpr2j7wbrc5hbq4jwnrath7rhvuu`.
The [independent review](../ramsey_r55_root20_anchor_realization_review1)
accepted that local graph and its affine handoff, not the present O22 or
any joint completion. Its graph bytes are hash-pinned in both new programs.

Take root `r` red to all H20 and blue to all O22. The root's two neighborhood
densities are now realized by actual graphs: 92 red edges and 107 blue edges.
For an eventual labeling `[r,H0,...,H19,O0,...,O21]`, the target red degrees
are 20 for `r,H0,H1` and 21 for all other vertices. Consequently the 440
unfixed H--O pairs must supply red degrees

```
H: 12,14,10,12,10,10,12,10,11,11,10,10,11,10,11,11,10,9,9,11
O:  8, 9,10,10,10, 9,10,10,10,10, 8,10,10,10,10,10,10,10,10,10,10,10
```

Each list sums to 214, so the total red-edge count would be
`92+124+20+214=450`. [HANDOFF.json](HANDOFF.json) preserves these exact debts.
These scalar and individual degrees are necessary conditions only; **no
degree-constrained bipartite realization or K5-free gluing was tested**.

Keep all 440 H--O edges free, including the 44 incidences of the two marked
H vertices. Requiring every O vertex to be red to at least one marked vertex,
together with their degrees 12 and 14, forces intersection size 4 and the
only-first/only-second/both partition sizes 8/10/4. Arbitrarily fixing that
partition on the labeled O graph would restrict the gluing family and is
not justified as normalization. Any future symmetry reduction must preserve
the fixed cores or prove an appropriate representative argument.

The other two exceptional vertices' neighborhood densities, all mixed
monochromatic K5 exclusions, and joint feasibility remain open. The H20
[footprint kernel](../ramsey_r55_root20_footprint_kernel), source
`968d56f0193be9eae8dd020e492fbc721647cb3b`, gives reusable constraints for
that later step, but its theorem is not needed to certify this O22 witness.
The earlier 627-primary joint solver test returned UNKNOWN; no timeout is
reinterpreted here. The symmetry research lane is separate.

## Reproduce

Use CPython 3.11.2, standard library only, from the repository root. No binary,
solver, generated large input, external graph download or network access is
needed once this checkout and the sibling H20 graph are present. Choose fresh
output directories; the producer refuses to overwrite an existing one.

```bash
python3 -B ramsey_r55_opposite22_realization/generate.py --work /scratch/r55-o22-new
python3 -B ramsey_r55_opposite22_realization/verify.py --work /scratch/r55-o22-new --report /scratch/r55-o22-check.json
python3 -B ramsey_r55_opposite22_realization/controls.py --work /scratch/r55-o22-new --report /scratch/r55-o22-controls.json
diff ramsey_r55_opposite22_realization/result.json /scratch/r55-o22-new/result.json
diff ramsey_r55_opposite22_realization/GRAPH.json /scratch/r55-o22-new/GRAPH.json
diff ramsey_r55_opposite22_realization/HANDOFF.json /scratch/r55-o22-new/HANDOFF.json
diff ramsey_r55_opposite22_realization/verification.json /scratch/r55-o22-check.json
diff ramsey_r55_opposite22_realization/controls.json /scratch/r55-o22-controls.json
(cd ramsey_r55_opposite22_realization && sha256sum -c SHA256SUMS)
```

Repeat with `python3 -O -B` and fresh paths to check optimized execution.
Expected result: 108 cases, 16 survivors, chosen deletion `[0,10]`, verifier
`VERIFIED`, controls `PASS`. All arithmetic is exact Python integer arithmetic.
There is no randomness, parallel scheduling, partial search or omitted large
proof. The final normal-plus-optimized generation, full verification and
controls took 3.294344 seconds total, with peak child RSS 19,768 KiB on the
production Linux host. This is an observed resource cost, not a runtime
guarantee. Trust remains in the ordinary finite reduction, source, interpreter,
hardware and hash identity. Public source and matching outputs alone are not
peer review. This bounded local-realization milestone ends here, before any
440-edge gluing model or another deletion radius is started.
