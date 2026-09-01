# Exact edge-criticality certificate for the 2,259-edge Parts-509 subgraph

## Result and scope

Let `H` be the graph in `reduced_edges.json`: it has the 509 points of Jaan
Parts's record construction as vertices and 2,259 of their unit-distance pairs
as edges.  The evidence in this directory, together with the separately checked
non-4-colorability certificate described below, establishes

\[
\chi(H)=5
\quad\text{and}\quad
\chi(H-e)=4\quad\text{for every }e\in E(H).
\]

Thus `H` is **5-edge-critical**.  `certificate.json` contains an explicit proper
4-coloring of each of the 2,259 graphs `H-e`.  In every witness, the two endpoints
of the deleted edge receive the same color.  Two solver-free checkers replay all

\[
2259\cdot2258=5{,}100{,}822
\]

retained-edge inequalities and all 2,259 deleted-endpoint equalities.

This independently certifies the edge-criticality assertion in Mohammed Amer's
2026 data release.  It does **not** improve the 509-vertex record, does not improve
the 2,259-edge bound from that release, and does not determine the chromatic
number of the plane.  No novelty or priority claim is made for the abstract
edge-criticality statement.

## Structural corollaries

The earlier certificate in `../hadwiger_nelson_parts509_criticality` gives a
proper 4-coloring of the strict 2,442-edge graph after every vertex deletion.
Restricting those colorings to `H-v` proves

\[
\chi(H-v)=4\quad\text{for every }v\in V(H).
\]

Consequently `H` is both 5-vertex-critical and 5-edge-critical.

There is also an edge-contraction corollary.  For `e=uv`, each committed
coloring of `H-e` has `c(u)=c(v)`, so it descends to a proper 4-coloring of the
contraction `H/e`.  Conversely, a 3-coloring of `H/e` would lift to a 3-coloring
of `H-e`; recoloring one of `u,v` with a fourth color would then 4-color `H`, a
contradiction.  Hence

\[
\chi(H/e)=4\quad\text{for every }e\in E(H).
\]

In summary, every single vertex deletion, edge deletion, and edge contraction
lowers this graph's chromatic number from 5 to exactly 4.  The contraction
statement is an elementary consequence of the checked edge witnesses, not a
claim about preservation of a unit-distance embedding after contraction.

## Fast, solver-free verification

CPython 3.11 or newer is sufficient; verification has no third-party Python
dependency.

```bash
python3 edge_criticality.py verify reduced_edges.json certificate.json
python3 independent_check.py reduced_edges.json certificate.json
```

Both commands should report

```text
all_checks=true
edge_deletion_colorings_verified=2259
endpoint_equality_checks=2259
retained_edge_inequality_checks=5100822
```

The second checker does not import the generator or primary verifier.  It parses
and decodes the certificate independently and confirms that the unique
monochromatic edge in row `i` is exactly edge `i`, the edge deleted in that row.

The certificate uses one 128-byte row per edge.  Each vertex color occupies two
bits; the last byte's six unused bits are required to be zero.  The 289,152-byte
binary payload is base64-encoded in JSON.

## Regenerating witnesses

Generation uses PySAT only to find witnesses.  Keep the environment, progress
files, and any solver output under `/scratch`.

```bash
python3 -m venv /scratch/parts509-edge-venv
/scratch/parts509-edge-venv/bin/pip install -r requirements.txt

/scratch/parts509-edge-venv/bin/python edge_criticality.py generate \
  reduced_edges.json \
  /scratch/parts509-edge-certificate-new.json \
  --progress /scratch/parts509-edge-progress.partial \
  --solver cadical195 \
  --vertex-deletion-certificate \
  ../hadwiger_nelson_parts509_criticality/certificate.json
```

The generator supports checkpointed `generate-segment` runs and a `merge`
command for disjoint ranges.  SAT solvers can return different valid colorings,
so a regenerated payload need not have the committed hash.  It must pass both
solver-free verifiers.

The search encoding deliberately omits at-most-one-color clauses.  At least one
color is selected at each vertex, and same-color selections are excluded across
every retained edge.  Therefore the selected-color sets at adjacent vertices
are disjoint, and choosing the least selected color at every vertex gives an
ordinary proper coloring.  The deleted endpoints are both pinned to color zero.
Verified colorings of `H-u` and `H-v` are used as phase hints or direct extension
witnesses; they do not enter the verification trust boundary.

## Lower-bound and exact-geometry audit

The edge-deletion witnesses prove `chi(H-e) <= 4`; edge-criticality additionally
needs `chi(H) > 4`.  That lower bound is kept as a separate trust boundary.

The exact checker in the sibling contribution reconstructs all 2,442 unit pairs
among the 509 algebraic coordinates in
`Q(sqrt(3),sqrt(5),sqrt(11))`.  It verifies that every one of the 2,259 edges in
`reduced_edges.json` is a unit pair.  It also audits the external DIMACS file as
exactly the standard four-coloring encoding for these edges plus three sound
triangle pins:

```bash
python3 ../hadwiger_nelson_parts509_criticality/parts509.py audit-cnf \
  ../hadwiger_nelson_parts509_criticality/parts509.vtx \
  reduced_edges.json \
  /scratch/hadwiger-nelson-e5/FINAL2.cnf
```

A fresh run returned 2,442 exact unit pairs, 2,259 audited reduced edges, 2,036
variables, 9,548 clauses, and pins assigning distinct colors to the triangle
`(0,149,152)`.  No floating-point comparison is used.

The 46 MiB proof log is intentionally not committed.  With the external data
under `/scratch`, replay it using `drat-trim`:

```bash
/scratch/drat-trim/drat-trim \
  /scratch/hadwiger-nelson-e5/FINAL2.cnf \
  /scratch/hadwiger-nelson-e5/FINAL2_proof.drat \
  > /scratch/parts509-edge-drat.log 2>&1
```

The fresh replay checked 92,649 core lemmas and 5,813,255 resolution steps and
returned `s VERIFIED`.  A proper 5-coloring of the strict graph, already checked
in the sibling contribution, restricts to `H`; hence `chi(H)=5`.

## Hashes

```text
reduced_edges.json
  99b8ca39503a33c692bed66e45afcc7e8b67bec0870253c53b097836fbbbe3b2
canonical 2,259-edge list (lines "u v\n")
  93f5ff096936613b61fcbdba3bca27addd5d59868c10561385c4ada7606d2305
certificate.json
  8b7290cb4d97cb383fbdc2cba4311db44417a9a7170e54016480a3b89469c0b0
packed edge-deletion witnesses before base64
  61be99f8154b98093080349970f5d3420e71f3003729ce15440d34c515509abc
external FINAL2.cnf
  9bcea2812e5c95e3ccdc9a4e3a2b6c96234cd86dacdecdc9ac2e0c26b05a65db
external FINAL2_proof.drat (kept under /scratch)
  2c64344e3137c95db53f23ff9e9490034a210d214e3ce7805eafbf1d53c25930
```

## Trust boundary

- The two committed witness checkers use only CPython's JSON, base64, and hash
  implementations.  They do not invoke or trust a SAT solver.
- Non-4-colorability of `H` trusts the audited external CNF and proof bytes and
  the C implementation of `drat-trim`.  The proof log remains under `/scratch`.
- The unit-distance embedding trusts the coordinate input, SymPy parsing and
  denesting, and the sibling checker's exact rational multiquadratic arithmetic.
- The reduced graph is non-strict: 183 other pairs on these points are also at
  unit distance but are deliberately omitted as graph edges.  This is valid for
  a unit-distance graph in the ordinary, non-faithful sense.
- The claim that every vertex deletion is 4-colorable depends on the separately
  committed and independently reviewed vertex-deletion certificate.
- PySAT, CaDiCaL, Minisat, phase seeding, symmetry breaking, and segmented search
  were used only to generate witnesses and are outside the verification trust
  boundary.

## Provenance

- Mohammed Amer, data and independent lower-bound verification for a
  509-vertex, 2,259-edge graph (2026):
  <https://github.com/md-amer/hadwiger-nelson-e5>.
- Jaan Parts, *Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane*, *Geombinatorics* 29(4) (2020), 137–166:
  <https://arxiv.org/abs/2010.12665>.
- Aubrey D. N. J. de Grey and Jaan Parts, *On lower bounds of the order of
  k-chromatic unit distance graphs*, *Geombinatorics* 32(2) (2022), 72–74:
  <https://arxiv.org/abs/2303.14714>.

The upstream edge list and license are reproduced unchanged.  The exact source
commit and public links are recorded in the Discovery Net contribution after a
fresh URL and commit verification.
