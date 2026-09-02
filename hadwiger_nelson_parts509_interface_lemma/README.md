# Interface classification of the L ∪ S decomposition of the Parts 509 graph

## Result and scope

Let `G` be the strict unit-distance graph on Jaan Parts's 509 algebraic points
(`../hadwiger_nelson_parts509_criticality/parts509.vtx`, 2,442 edges,
`chi(G) = 5`).  Exactly 374 of the points have coordinates free of `sqrt5`
(indices 0..373, the origin being index 0); the other 135 (indices 374..508)
involve `sqrt5`.  Write `L` for the induced subgraph on the first set (1,860
edges) and `S` for the induced subgraph on the second (552 edges).  This is
Parts's decomposition `G = L ∪ ρS` of his "type M6A" graph: `S` is a base
graph rotated about the origin by the angle `2·arcsin(1/4)` (cosine `7/8`,
sine `sqrt15/8`, which is where `sqrt5` enters).

Exactly 30 edges of `G` join `L` to `S`.  Their `L`-endpoints form the
19-vertex **interface** `I_L`, which consists of

| label | count | exact squared radius | angles | rôle |
|---|---|---|---|---|
| `origin` | 1 | 0 | – | shared centre of rotation |
| `aux_inner` | 3 | `17/6 − sqrt33/6 = (sqrt11/2 − sqrt3/6)^2` | 30°, 150°, 270° | Parts's auxiliary orbit `(0,0,2,6)` |
| `aux_outer` | 3 | `17/6 + sqrt33/6 = (sqrt11/2 + sqrt3/6)^2` | 30°, 150°, 270° | Parts's auxiliary orbit `(0,0,2,6)` |
| `reference` | 12 | 4 | `±16.779° + 60°k` | Parts's reference orbit `(0,4,4,0)` |

The 30 cross edges are: 12 edges from the origin to unit-radius vertices of
`S`; 6 auxiliary edges (each inner auxiliary vertex of `L` to an outer auxiliary
vertex of `S` and vice versa, the partners being rotated by `2·arcsin(1/4)`);
and 12 reference edges joining each reference vertex of `L` at angle `θ` to the
reference vertex of `S` at angle `θ + 2·arcsin(1/4)`.

**Lemma (interface classification).**  Normalise every proper 4-colouring of
`L` so that the origin has colour 0.  Its restriction to the 18 non-origin
interface vertices is, up to a permutation of the colours 1, 2, 3, one of
exactly **20** colourings, all of which occur.  They are listed in
`interface_L.json` together with one explicit proper 4-colouring of `L`
realising each.  In every class:

- exactly one of the two auxiliary triples is monochromatic in colour 0 (the
  origin's colour), and the other auxiliary triple is rainbow (three distinct
  colours);
- the 12 reference vertices receive at most two colours, one of which occurs at
  least 8 times: 18 classes have an 8–4 split and 2 classes colour all twelve
  reference vertices 0.

The full table (reference vertices in increasing angular order, 359, 358, 357,
368, 367, 366, 365, 364, 363, 362, 361, 360):

```text
 #  aux_in aux_out reference      split
 0  000    023     330300000030   8-4
 1  000    012     330330330330   8-4
 2  000    203     000000303303   8-4
 3  000    203     303303303303   8-4
 4  000    310     003033030000   8-4
 5  000    210     033033033033   8-4
 6  000    312     000000000000   12
 7  000    312     000010110100   8-4
 8  000    312     030000003033   8-4
 9  000    132     202202000000   8-4
10  031    000     003030000303   8-4
11  032    000     003333003333   8-4
12  102    000     300003030030   8-4
13  102    000     330033330033   8-4
14  130    000     030300303000   8-4
15  130    000     333300333300   8-4
16  132    000     000000000000   12
17  231    000     000101001010   8-4
18  132    000     020020200002   8-4
19  123    000     303000030300   8-4
```

(The strings show the witness colourings; the canonical class strings in the
JSON are the lexicographically least permutations of the colours 1, 2, 3.)

**Corollary 1 (structured proof of `chi(G) = 5`).**  For each of the 20
classes, `S` has no proper 4-colouring compatible with it across the 30 cross
edges (20 DRAT-checked UNSAT instances on 540 variables each).  Since every
proper 4-colouring of `G` restricts to `L` as one of the 20 classes (after a
colour permutation that fixes the origin's colour), `G` has no proper
4-colouring.  This re-derives the 5-chromaticity of the record graph from a
19-vertex interface specification instead of one monolithic SAT call.

**Corollary 2 (what each vertex of `S` guards).**  `s_vertex_leaks.json`
lists, for every vertex `v` of `S`, the classes that `S − v` fails to block,
with an explicit proper 4-colouring of `L ∪ (S − v)` for each.  Every vertex of
`S` leaks at least one class (this recovers the vertex-criticality of `G` on
the `S` side), and the number of leaked classes ranges from 1 (two vertices,
each guarding a single class) to all 20: exactly three vertices (397, 404 and
405) each leak all 20 classes, so any one of them alone leaks every class (no
set-cover statement is intended).  The two all-zero-reference classes
(numbers 6 and 16) are the hardest to leak: each is leaked by only 26 of the
135 vertices, whereas every other class is leaked by at least 65 vertices.

**Computational observation (the small side is floppy).**  The same
enumeration on `S ∪ {origin}` over its 30-vertex interface `I_S` (origin colour
0, modulo permutations of 1, 2, 3) yields 66,332 classes, and drat-trim
verified CaDiCaL's proof that the corresponding completeness CNF (400,385
clauses) is unsatisfiable.  The large side is rigid (20 classes), the small side
is not; the composition works because every one of the 20 rigid patterns is
blocked.

Nothing here improves the 509-vertex record or the bounds
`5 <= chi(R^2) <= 7`.  The qualitative mechanism (two rotation-linked gadgets
sharing a centre, with reference and auxiliary edges) is due to Heule and to
Parts; the exact 20-class specification of the large gadget, its geometric
invariants, and the certified decomposition of the 5-chromaticity proof are, to
the extent of our search of Parts (2020), Heule (2018) and the Polymath16
material, not stated anywhere.

## Why this is useful

The lemma reduces any question of the form "is `L ∪ X` 5-chromatic?" for a
point set `X` whose unit-distance neighbours in `L` lie in `I_L` to twenty
independent small SAT problems on `X` alone, one per class (the colour
permutations are absorbed by symmetry).  This is the engine behind the exact
minimum-gadget search over the `sqrt5`-completion pool of the record graph
reported separately.

## Reproduction

Dependencies: `python-sat==1.8.dev24` (CaDiCaL 1.9.5 backend), `sympy==1.14.0`
(coordinate parsing only, through the sibling directory's `parts509.py`).
Optional external tools for DRAT certificates: CaDiCaL 1.9.5 and drat-trim.

```bash
# enumerate the classes, write all certificates' CNFs to DIR, certify with DRAT
python3 interface_lemma.py enumerate interface_L.json --cnf-dir DIR \
    --cadical /path/to/cadical --drat-trim /path/to/drat-trim
# per-vertex leak map of S (about 7 minutes)
python3 interface_lemma.py leaks interface_L.json s_vertex_leaks.json
# independent check (solver-free part plus in-process CaDiCaL re-solves)
python3 verify_interface.py interface_L.json --leaks s_vertex_leaks.json
```

Expected: `20 interface classes`, completeness `{'cadical_exit': 20,
'drat_trim_verified': True}` (7,935 clauses, CNF SHA-256
`0d29b4b70fed7d038efaf30f6cd50e1d4104f15fcf54e3d28d99874893a18342`), all 20
blocking instances `cadical_exit 20, drat_trim_verified True`, and from the
verifier

```text
solver-free checks: 20 distinct classes, witnesses proper, invariants hold
leak witnesses checked: 1508 (solver-free)
solver check: the 20 classes are complete (UNSAT)
solver check: S blocks all 20 classes (UNSAT each)
solver check: leak lists are complete (1192 UNSAT calls)
all_checks=true
```

Runtime on this host: enumeration 5 s, completeness DRAT check 5 s, the 20
blocking DRAT checks about 1 s each, leak map 7 minutes, verifier about 3
minutes.  `block_report.json` records the SHA-256 of every CNF and the
CaDiCaL/drat-trim outcome.

## Trust boundary

- Geometry: exact rational arithmetic in `Q(sqrt3, sqrt5, sqrt11)` via the
  sibling directory's `parts509.py`; SymPy is used only to parse the published
  coordinates.  No floating point enters any claim (angles above are decimal
  renderings of exact algebraic data).
- Positive statements (each class occurs; each leak occurs) are certified by
  explicit colourings replayed against the exact edge list with no solver.
- Negative statements (no 21st class; `S` blocks each class; no unlisted leak)
  rest on UNSAT answers.  Completeness and the 20 blocking instances were
  additionally checked with drat-trim; the 1,192 leak-completeness UNSATs
  (2,700 vertex-class pairs minus 1,508 witnessed leaks) are in-process CaDiCaL
  answers without proof logging.
- The 66,332-class count for `S` is a computational observation, reproducible
  with `python3 enumerate_side.py S OUTDIR` (about 3 minutes; `enumerate_side.py L`
  regenerates the 20 classes).  Its witness file and completeness certificate are
  too large to commit; their SHA-256 values are `interface_S.json`
  `09bc4ca48999d002aa19a1e449347f8efb40b47cb92c13d64812473b75bf4918`,
  `complete_S.cnf` (400,385 clauses)
  `83ce225153a513d17b0404e7ddfb9bb8debfdf3d7464adf5544fe519cabf9665`, and the
  CaDiCaL 1.9.5 DRAT proof (49.8 MB, drat-trim `s VERIFIED` in 1,336 s)
  `6ec50d390a2c278f650686915adce99f9cbc76b9a70a649fbf2b71860dd5c2e5`.
- DRAT proofs and CNFs are not committed; they are regenerated by the commands
  above.

## Files

- `interface_lemma.py` — generator (`enumerate`, `leaks`).
- `verify_interface.py` — independent checker.
- `interface_L.json` — the 20 classes with witness colourings, interface data,
  cross edges, and the certificate report.
- `s_vertex_leaks.json` — per-vertex leak lists of `S`; each witness string colours
  the sorted vertex list of `S − v` and, together with the class witness on `L`,
  is a proper 4-colouring of `L ∪ (S − v)` (1,508 witnesses).
- `block_report.json` — CNF hashes and DRAT outcomes.
- `SOURCE_LICENSE.txt` — licence of the coordinate data (see sibling directory).
