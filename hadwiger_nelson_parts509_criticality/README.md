# Exact vertex-criticality certificate for the Parts 509 graph

## Result and scope

Let `G` have the 509 distinct points in `parts509.vtx` as vertices, with an
edge for **every** pair at Euclidean distance exactly one.  The checks in this
directory certify

\[
|V(G)|=509,\qquad |E(G)|=2442,\qquad \chi(G)=5,
\]

and, for every vertex `v`,

\[
\chi(G-v)=4.
\]

Thus the published 509-vertex unit-distance graph of Jaan Parts is
5-vertex-critical: every vertex is individually indispensable to
non-4-colorability.  This closes all 509 one-vertex deletions of the current
vertex-record construction.  It does **not** produce a graph on fewer than 509
vertices, and no novelty or priority claim is made for the abstract
vertex-criticality fact.  The contribution is an independently rerunnable
structural certification of the known construction.

The inference `chi(G-v) = 4`, rather than merely `chi(G-v) <= 4`, is elementary:
adding one vertex raises chromatic number by at most one, while `chi(G) = 5`.

## What is certified

`parts509.py` performs four separate checks.

1. It parses the algebraic coordinates and reconstructs all unit pairs.  The
   apparently nested radicals denest via

   \[
   \frac18\sqrt{\frac{35\mathbin{\pm}5\sqrt{33}}2}
   =\frac{\sqrt{55}\mathbin{\pm}\sqrt{15}}{16}.
   \]

   Consequently every coordinate lies in
   `Q(sqrt(3), sqrt(5), sqrt(11))`.  After parsing, squared distances are
   compared as eight-tuples of exact rational coefficients; no floating-point
   tolerance or numerical root comparison is used.
2. `certificate.json` contains an explicit proper 5-coloring of `G` and 509
   explicit proper 4-colorings, one for each `G-v`.  The deletion witnesses are
   packed four 2-bit colors per byte and base64 encoded.  Verification decodes
   them and checks every retained edge directly, without invoking or trusting a
   SAT solver.
3. For every deletion witness, the neighbors of the deleted vertex use all
   four colors.  This is a useful local consistency condition and is also forced
   by non-4-colorability of the full graph.
4. Non-4-colorability is independently bridged to a checked DRAT refutation.
   The audited 2,259-edge graph is a subgraph of the 2,442-edge strict graph.
   Its CNF consists exactly of the standard at-least-one vertex clauses, binary
   same-color edge exclusions, and three sound color-symmetry pins on the
   triangle `(0,149,152)`.  `drat-trim` reports `s VERIFIED`, so that subgraph,
   and hence `G`, is not 4-colorable.

The exact graph has minimum degree 4, maximum degree 36, and degree histogram

```text
4:6, 5:42, 6:56, 7:62, 8:45, 9:40, 10:69, 11:50,
12:61, 13:28, 14:15, 15:14, 16:6, 17:4, 18:4, 22:6, 36:1.
```

## Fast verification from committed compact evidence

Use CPython 3.11 or newer.  All environments and regenerated outputs should
remain under `/scratch`.

```bash
python3 -m venv /scratch/parts509-venv
/scratch/parts509-venv/bin/pip install -r requirements.txt
/scratch/parts509-venv/bin/python parts509.py verify \
  parts509.vtx certificate.json
```

Expected mathematical summary:

```text
all_checks=true
exact_unit_distance_pairs=2442
five_coloring_verified=true
deletion_colorings_verified=509
neighbor_color_surjectivity_checks=509
```

Regenerate the coloring witnesses with CaDiCaL 1.9.5 through PySAT:

```bash
/scratch/parts509-venv/bin/python parts509.py generate \
  parts509.vtx /scratch/parts509-certificate-new.json \
  --solver cadical195
```

SAT solvers may choose different valid colorings, so a regenerated certificate
need not have the same byte hash.  Its verification result must agree.

## Independent UNSAT-proof audit

The DRAT proof is deliberately not committed here: it is a 46 MiB proof log,
and repository policy requires proof logs and solver traces to stay under
`/scratch`.  The compact CNF, reduced edge list, coordinate source, and proof
are currently mirrored by Mohammed Amer at commit
`6d5ac08491f7cadbebd7d5b79e3f825d08eedf7b`:

<https://github.com/md-amer/hadwiger-nelson-e5>

One exact replay is:

```bash
git clone https://github.com/md-amer/hadwiger-nelson-e5.git \
  /scratch/hadwiger-nelson-e5

/scratch/parts509-venv/bin/python parts509.py audit-cnf \
  parts509.vtx \
  /scratch/hadwiger-nelson-e5/FINAL_reduced.json \
  /scratch/hadwiger-nelson-e5/FINAL2.cnf

git clone https://github.com/marijnheule/drat-trim.git /scratch/drat-trim
make -C /scratch/drat-trim
/scratch/drat-trim/drat-trim \
  /scratch/hadwiger-nelson-e5/FINAL2.cnf \
  /scratch/hadwiger-nelson-e5/FINAL2_proof.drat
```

The fresh audit used `drat-trim` commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` and returned:

```text
c parsing input formula with 2036 variables and 9548 clauses
c 8644 of 9548 clauses in core
c 92649 of 228706 lemmas in core using 5813255 resolution steps
c 0 RAT lemmas in core; 88474 redundant literals in core lemmas
s VERIFIED
```

The CNF audit independently recovered 2,259 reduced edges, verified every one
as an edge of the exact 2,442-edge graph, and checked all 9,545 non-pin clauses
plus the three triangle pins.

## Hashes from the certified run

```text
parts509.vtx
  770a585a6c1e1222355322707479cb826e9ada560279da904ef89c15c99ff0b5
exact 2442-edge list (canonical lines "u v\n")
  5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c
certificate.json
  d354f9629c41639168b80fc1aa6feb6e4187dd37dee7efcb83b4ef6ebe68d16c
packed 509 deletion witnesses before base64
  be5c4c0d333552334ae6d343d000f84456be50f8ef9e7f95d64ca92779390d36
external reduced 2259-edge list (canonical lines "u v\n")
  93f5ff096936613b61fcbdba3bca27addd5d59868c10561385c4ada7606d2305
external FINAL2.cnf
  9bcea2812e5c95e3ccdc9a4e3a2b6c96234cd86dacdecdc9ac2e0c26b05a65db
external FINAL2_proof.drat (kept under /scratch)
  2c64344e3137c95db53f23ff9e9490034a210d214e3ce7805eafbf1d53c25930
```

## Trust boundary

- Exact geometry trusts CPython's `fractions.Fraction`, the small field
  implementation in `parts509.py`, SymPy 1.14.0's parsing/denesting, and the
  coordinate input.  Equality decisions after parsing use rational arithmetic
  only.
- The 5-coloring and all deletion colorings are proof witnesses checked directly
  by the committed verifier; their generation solver is outside the verification
  trust boundary.
- Full-graph non-4-colorability trusts the audited CNF bridge, the external DRAT
  bytes with the recorded hash, and `drat-trim`'s proof checking.  The proof log
  is externally mirrored and was present under `/scratch` for the reported run.
- The proof pertains to the ordinary unit-distance-graph convention, and in fact
  the reconstructed 2,442-edge graph is strict: every unit pair among the 509
  coordinates is included.

## Provenance and prior work

- Jaan Parts, *Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane*, Geombinatorics 29(4) (2020), 137--166,
  <https://arxiv.org/abs/2010.12665>.
- The coordinate list was obtained from the exact-data mirror above, where it is
  identified as the unaltered Parts 509-vertex input.  Coordinate expressions
  are unchanged here; only CRLF line endings were normalized to LF.  The
  accompanying MIT notice is preserved in `SOURCE_LICENSE.txt`.
- The same mirror's 2026 edge-minimization work concerns the number of edges on
  these 509 vertices, not a smaller vertex construction.
