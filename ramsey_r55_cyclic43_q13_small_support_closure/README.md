# Six complete small-support components of the Cyclic(43) objective-thirteen layer

This directory closes the smallest unresolved family in the certified
objective-thirteen boundary of the primary Cyclic(43) Ramsey landscape.  The
18 starting orbits are exactly the boundary states whose non-length-one
support signatures are `{17,21}` or `{17,17,21}`.  Exhausting all one-edge
moves that remain at objective thirteen proves that these seeds meet exactly
six complete connected components of the global **exact-level** graph.

The statement depends on the independently reproduced parent boundary in
[`../ramsey_r55_cyclic43_q13_boundary_certificate`](../ramsey_r55_cyclic43_q13_boundary_certificate).
It does not claim to close the complete objective-thirteen frontier of the
69,071,588-vertex primary sublevel-twelve component.

## Exact closure theorem

Use the lexicographic edge order

```text
(0,1),(0,2),...,(0,42),(1,2),...,(41,42)
```

and color an edge red in the seed precisely when its cyclic length belongs to

```text
{1,2,7,10,12,13,14,16,18,20,21}.
```

A state lists the edges toggled from this seed.  We quotient by cyclic vertex
rotation and select the least tuple of 15 little-endian 64-bit toggle words.
Let `q` denote the number of monochromatic `K_5`s.

The 18 selected `q=13` boundary seeds have a complete exact-level closure of
150 free `C_43` orbits.  Its quotient graph has

```text
6 connected components
228 edges
cycle rank 84
component sizes 59^2, 10^2, 6^2
```

The component pairs are exchanged by vertex reflection `v -> -v (mod 43)`.
No state and no component is fixed by this reflection, so the 150 cyclic
orbits form 75 dihedral orbits.  The support-signature census is

```text
{17,17,21}^8, {17,21}^118, {21}^24.
```

The paired component profiles are:

| size | copies | seeds per copy | edges per copy | rank per copy | distinct sublevel endpoints per copy |
|---:|---:|---:|---:|---:|---|
| 59 | 2 | 1 | 96 | 38 | `q6:4, q8:8, q10:10, q11:24, q12:72` |
| 10 | 2 | 4 | 13 | 4 | `q11:2, q12:10` |
| 6 | 2 | 4 | 5 | 0 | `q12:11` |

Some `q=12` endpoints are shared between components, so the global distinct
endpoint counts are

```text
q=6: 8, q=8: 16, q=10: 20, q=11: 52, q=12: 178.
```

There are no `q=7` or `q=9` moves.  Among all `150*903 = 135,450` flips,
456 directed incidences stay at `q=13`; all have multiplicity one and pair to
the 228 undirected quotient edges.  The low boundary incidence counts are

```text
q=6: 8, q=8: 16, q=10: 20, q=11: 124, q=12: 238.
```

The minimum neighbor objective across the 150 sources has histogram

```text
6^8, 8^16, 10^20, 11^36, 12^68, 13^2.
```

All eight objective-six endpoints and all 16 objective-eight endpoints occur
entry-for-entry in the previously certified primary sublevel-six and
sublevel-eight representative arrays.  This is a striking shortcut back into
the primary basin, not a merger with a disconnected lower island.  The
certificate records the exact upstream array indices and hashes.

## Why the enumeration is exhaustive

For an edge `e=uv`, let `R_e` be the number of red triangles in
`N_R(u) intersect N_R(v)` and define `B_e` analogously.  The monochromatic
five-cliques containing `e` are in bijection with these triangles, hence

```text
q(G flip e) = q(G) - R_e + B_e,  when e is red,
q(G flip e) = q(G) + R_e - B_e,  when e is blue.
```

`generate_closure.py` uses bit intersections to count the triangles and
performs breadth-first search from all 18 seeds.  It scans all 903 flips of
every newly found state.  A listed set is therefore a complete union of
exact-level components precisely when every `q=13` target is already listed;
the generated certificate records that closed set, its complete sublevel
boundary, and every aggregate above.

`verify_closure.py` shares no project code with the generator.  It rebuilds
the coloring, counts common-neighborhood triangles by explicit vertex
triples, separately implements rotations and reflection, rescans all 135,450
moves, checks reachability and closure, regenerates the complete 274-state
sublevel endpoint payload, and verifies the pinned primary-component array
positions.  All arithmetic is exact integer arithmetic; there is no floating
point, randomness, solver, native extension, or network input during a run.

## Reproduction

Python 3.11 or later is sufficient.  First obtain two upstream primary-layer
certificates at immutable commit
[`02a959f499aa8e3b749a7f7fb3d3fc5f255c3b14`](https://github.com/njallskarp/math_source_code_open/tree/02a959f499aa8e3b749a7f7fb3d3fc5f255c3b14/ramsey_r55_cyclic43):

```text
objective-six-component-representatives.json
objective-eight-component-fast.json
```

From this directory, set `UPSTREAM` to that downloaded directory and run:

```bash
python3 generate_closure.py \
  ../ramsey_r55_cyclic43_q13_boundary_certificate/boundary_certificate.json \
  "$UPSTREAM/objective-six-component-representatives.json" \
  "$UPSTREAM/objective-eight-component-fast.json" \
  closure_certificate.regenerated.json

cmp closure_certificate.json closure_certificate.regenerated.json

python3 verify_closure.py \
  ../ramsey_r55_cyclic43_q13_boundary_certificate/boundary_certificate.json \
  "$UPSTREAM/objective-six-component-representatives.json" \
  "$UPSTREAM/objective-eight-component-fast.json" \
  closure_certificate.json

python3 -m unittest -v test_closure.py
```

Expected headline output from both enumerator and verifier is

```text
states=150 components=6 edges=228 cycle_rank=84
component_sizes={'10': 2, '59': 2, '6': 2}
sublevel_targets={'6': 8, '8': 16, '10': 20, '11': 52, '12': 178}
```

On the research host with CPython 3.11.2, generation took 7.5 seconds, the
independent explicit-triple verification took 33.8 seconds, and the five
focused tests took 6.2 seconds.  The generated JSON is deterministic.

Input hashes are

```text
af8b6892049ace5610e2d7cea4c8642f39f53634287474127990aca0abbe2b85  boundary_certificate.json
aea99967a1a3cc41c640c73c471a73b015259186619495ffa5223968cb48d320  objective-six-component-representatives.json
740c10a6cc72d148ce949749aa8d8f132aa70f9bb0b797ee3e2fbe5ba84fdc1a  objective-eight-component-fast.json
```

Output and source hashes are recorded after the final verification below:

```text
85e271af8ebbd55c8bf8e6ad033122911f750a13dc95f638d74681f8c03e4d1e  closure_certificate.json
aca964695d8422cb3f4de0a066d013fe30e87919451889002f7810109cd5afa8  generate_closure.py
b1d6824d954c6e157b9f2ee01de6710fe030a5c29040224b67d599ceb5bff1ce  verify_closure.py
94cf039238a0010fbd4066ee8ef08431feaf80cbeb1952792431cfb92876688c  test_closure.py
```

## Scope, provenance, and significance

The parent 18-state seed set comes from the complete small-support portion of
the public 1,785-orbit exit certificate.  Completeness of that parent input
is inherited; completeness of the six exact-level components and their
one-flip boundaries is established here independently.  The lower-layer
membership comparison inherits the correctness and completeness of the two
pinned upstream representative arrays.

The result converts a sparse unexplored corner of the first `q=13` boundary
into six fully classified exact-level components and exposes an exact
reflection pairing plus unusually deep one-flip descents.  It may guide
which support strata to close next, but it neither closes the primary
sublevel-thirteen component nor classifies disconnected colorings, constructs
a `K_5`-free coloring of `K_43`, or changes the global bounds on `R(5,5)`.

Ge, Jayasooriya, Qiu, Sun, and Yuan's
[*Study of Exoo's Lower Bound for Ramsey number R(5,5)*](https://arxiv.org/abs/2212.12630)
studies the same Cyclic(43) construction, while Angeltveit and McKay's
[*R(5,5) <= 46*](https://arxiv.org/abs/2409.15709) concerns the global upper
bound.  Neither paper states this exact-level quotient closure.  Novelty is
claimed only relative to the searched public sources and Discovery Net, not
as an exhaustive historical priority claim.
