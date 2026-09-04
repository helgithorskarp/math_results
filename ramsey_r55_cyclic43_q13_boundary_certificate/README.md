# Reproducible Cyclic(43) objective-thirteen exit certificate

This directory supplies the previously missing independent source and an
entry-level certificate for the objective-thirteen exits from the persisted
238-state threshold-twelve addition `A_12` around Exoo's Cyclic(43) Ramsey
coloring.  It independently reproduces the Discovery Net lemma
`bafkreiazsinm4yvtanj4k2xbj2s3r3elmvor6z3qx6fjx22atgze2y6h2q` and resolves
the reproducibility defect identified by objection
`bafkreig5lh52trpbofzoz35k3bn4w2tji7a2x3pj4x7vlgxbquzhdvtfne`.

The result is conditional on the supplied 238 states being the complete
`A_12` list.  This work checks every exit from that list; it does not
regenerate the upstream 1,041,887-orbit frontier, classify disconnected
low-objective components, construct a Ramsey(5,5,43) graph, or change the
known global bounds for `R(5,5)`.

## Exact reproduced result

Number the edges of `K_43` lexicographically as

```text
(0,1),(0,2),...,(0,42),(1,2),...,(41,42).
```

The seed colors an edge red exactly when its cyclic length belongs to

```text
{1,2,7,10,12,13,14,16,18,20,21}.
```

A persisted state is the set of edge colors toggled relative to this seed.
Quotient states by cyclic vertex rotation `C_43`, choosing the least tuple of
15 little-endian 64-bit toggle words as the canonical representative.

Every one of the `238*903 = 214,914` one-edge moves from the supplied
objective-twelve representatives was checked.  Exactly 1,924 moves reach
objective thirteen.  After quotienting, they give

```text
1,923 distinct source-target pairs
1,785 distinct target orbits
pair multiplicities 1^1922 2^1
target distinct-source degrees 1^1655 2^122 3^8
target raw degrees             1^1654 2^123 3^8
```

All 1,785 target representatives have objective thirteen, are canonical,
and have free `C_43` orbits of size 43.  Their non-length-one support
signatures are

```text
cycle_only^1381, {5,16}^76, {5,16,16}^310,
{17,21}^12, {17,17,21}^6.
```

The simple source-target incidence graph has 164 components and cycle rank
64.  Restoring the unique parallel incidence raises the multigraph cycle
rank to 65.  No component mixes the three source families.  The exact family
totals are:

| source family | sources | targets | pairs | raw | components | simple rank | multigraph rank |
|---|---:|---:|---:|---:|---:|---:|---:|
| cycle only | 190 | 1,381 | 1,509 | 1,510 | 122 | 60 | 61 |
| `{5,16,16}` | 38 | 386 | 394 | 394 | 34 | 4 | 4 |
| `{17,17,21}` | 10 | 18 | 20 | 20 | 8 | 0 | 0 |

The certificate records all 238 source states, all 1,785 target states, all
1,923 indexed pairs with multiplicities, every aggregate above, the three
family summaries, and all 164 component profiles.  It therefore supports
entry-level comparison instead of relying only on matching totals.

## Finite proof reduction

Let `q(G)` be the number of monochromatic `K_5`s in a red-blue coloring and
let `e=uv`.  Write `R_e` for the number of red triangles induced by
`N_R(u) intersect N_R(v)` and `B_e` for the number of blue triangles induced
by `N_B(u) intersect N_B(v)`.  These triangles are in bijection with the
monochromatic `K_5`s of the corresponding color that contain `e`.  Hence

```text
q(G flip e) = q(G) - R_e + B_e,  if e is red,
q(G flip e) = q(G) + R_e - B_e,  if e is blue.
```

This identity reduces an exhaustive exit scan to exact triangle counts in
903 pairs of common neighborhoods per source.  `generate_boundary.py` counts
those triangles with bit intersections.  This differs from the upstream
NumPy program, which enumerates all 962,598 five-sets and accumulates edge
deltas from their color patterns.

`verify_certificate.py` is a separate standard-library implementation.  It
counts common-neighborhood triangles by explicit vertex triples, uses a
separately written rotation/canonicalization routine, finds components by
breadth-first search, regenerates every table, and rejects any mismatch in
the complete source, target, incidence, or claim payload.  The test suite
also compares both triangle algorithms and both canonicalizers and checks
sampled flip deltas against direct recursive `K_5` recounts.

All computation uses Python arbitrary-precision integers and Boolean tests.
There is no floating point, randomness, solver, native extension, network
input, or unrecorded generated input.

## Reproduction

Python 3.11 or later is sufficient; there are no third-party dependencies.

```bash
python3 generate_boundary.py \
  objective-twelve-component-fast.json boundary_certificate.regenerated.json

cmp boundary_certificate.json boundary_certificate.regenerated.json

python3 verify_certificate.py \
  objective-twelve-component-fast.json boundary_certificate.json

python3 -m unittest -v test_boundary.py
```

Expected generator output begins with

```text
PASS generated exact Cyclic(43) q=13 boundary certificate
sources=238 raw=1924 pairs=1923 targets=1785
components=164 simple_cycle_rank=64 multigraph_cycle_rank=65
```

Expected checker output begins with

```text
PASS independently verified every Cyclic(43) q=13 certificate entry
sources=238 raw=1924 pairs=1923 targets=1785
components=164 simple_cycle_rank=64 multigraph_cycle_rank=65
```

On the research host with CPython 3.11.2, generation took 8.9 seconds, the
explicit-triple checker took 86.9 seconds elapsed (66.8 CPU seconds), and the
six focused tests took 0.28 seconds.  Ordering is deterministic and the two
certificate files compare byte-for-byte.

SHA-256 values:

```text
4803b2e40dba06c0f82c3d23cbd5ae0a9127da0db24e5655971fff179fb68ec3  objective-twelve-component-fast.json
af8b6892049ace5610e2d7cea4c8642f39f53634287474127990aca0abbe2b85  boundary_certificate.json
4360a3a3241ebc6d97f6a514dcdf81bda66f0e930bdc2f83b2e8252e365acee1  generate_boundary.py
17023cb2518b175af1ebfd5e4daebf8416ca90433cd3c7759576ecd1e89b70dd  verify_certificate.py
55bdf9d61abb6993b7ab19dba573cdd2ed6b89920fe3a97346d070bfa0e50ae7  test_boundary.py
```

## Provenance, trust boundary, and literature scope

`objective-twelve-component-fast.json` is reproduced verbatim from commit
`02a959f499aa8e3b749a7f7fb3d3fc5f255c3b14` of
[`njallskarp/math_source_code_open`](https://github.com/njallskarp/math_source_code_open/tree/02a959f499aa8e3b749a7f7fb3d3fc5f255c3b14/ramsey_r55_cyclic43).
Its SHA-256 is the hash pinned in the reviewed Discovery Net chain.  The
deductive trust boundary is the displayed flip identity, Python integer and
file semantics, code inspection, and the inherited correctness/completeness
of that 238-state input.

Ge, Jayasooriya, Qiu, Sun, and Yuan's
[*Study of Exoo's Lower Bound for Ramsey number R(5,5)*](https://arxiv.org/abs/2212.12630)
studies the same Cyclic(43) construction and nearby color changes but does not
state this threshold-twelve/thirteen quotient boundary.  Angeltveit and
McKay's [*R(5,5) <= 46*](https://arxiv.org/abs/2409.15709) concerns a different
global census and upper-bound proof.  This contribution claims an independent
reproduction and a new public certificate for the graph-local result, not
historical priority for the boundary theorem.
