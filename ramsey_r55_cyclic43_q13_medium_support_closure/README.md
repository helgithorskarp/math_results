# Complete medium-support components of the Cyclic(43) objective-thirteen layer

This directory closes the second and larger noncycle family in the certified
objective-thirteen exit boundary of the Cyclic(43) threshold-twelve addition.
The 386 starting orbits are exactly the exits with non-length-one support
signature `{5,16}` or `{5,16,16}`.  Exhausting every one-edge move that stays
at objective thirteen proves that these seeds meet 33 complete connected
components of the global exact-level graph, containing 6,279 free rotation
orbits in total.

Together with the sibling
[`../ramsey_r55_cyclic43_q13_small_support_closure`](../ramsey_r55_cyclic43_q13_small_support_closure)
certificate, this closes the exact-level components meeting **all 404
noncycle exits** in the parent boundary.  The 1,381 cycle-only exits remain a
separate and substantially larger target.

## Exact theorem

Number the edges of `K_43` lexicographically and color an edge red in the
fixed seed exactly when its cyclic length lies in

```text
{1,2,7,10,12,13,14,16,18,20,21}.
```

A state records the edges toggled relative to this seed.  Quotient by cyclic
vertex rotation `C_43`, choosing the least tuple of 15 little-endian 64-bit
words.  Let `q(G)` be the number of monochromatic `K_5`s.

Breadth-first search from the 386 selected `q=13` boundary orbits, retaining
only one-edge moves whose target also has `q=13`, closes after exactly 6,279
orbits.  All are canonical and have free `C_43` action.  Their quotient graph
has

```text
33 components
12,720 edges
cycle rank 6,474
```

Every directed source-target pair has multiplicity one.  The exact component
size histogram is

```text
1^4, 2^2, 6^2, 8^2, 9^2, 12^4, 89^2, 162^2,
188^2, 235^2, 285^2, 393^2, 576^2, 751^2, 819^1.
```

Reflection `v -> -v (mod 43)` pairs 32 components and fixes the unique
819-state component.  It fixes 11 states, so the 6,279 cyclic orbits reduce
to 3,145 dihedral orbits.  The support census is

```text
{16,16}^4454, {5,16}^574, {5,16,16}^1251.
```

The `{5,16}` sector consists of two reflection-paired 285-state components
and four singleton components; it has no exact-level edge to the
`{16,16}`/`{5,16,16}` sector.  Thus the possible one-edge support insertion
between these signatures never occurs at objective thirteen.

## Complete one-flip boundary

All

```text
6279*903 = 5,669,937
```

one-edge moves were checked.  Exactly 25,440 directed incidences remain at
objective thirteen, pairing to the 12,720 quotient edges.  The distinct
sublevel endpoint counts are

```text
q=7: 229
q=8: 6
q=9: 245
q=10: 8,218
q=11: 1,084
q=12: 1,431
```

There is no endpoint below seven.  The corresponding directed incidence
counts are `458, 6, 522, 8,988, 7,039, 6,747`.  The minimum neighbor objective
over the 6,279 sources has histogram

```text
7^458, 8^6, 9^522, 10^4044, 11^887, 12^358, 13^4.
```

The two 285-state `{5,16}` components each meet the same complete set of 229
objective-seven endpoints.  A separate pinned-array check proves that every
q=7, q=8, q=9, and q=10 endpoint occurs entry-for-entry in the certified
primary component/frontier arrays.  These deep moves are therefore shortcuts
into the known primary basin, not bridges to the two external low-objective
islands.  The status of the q=11 and q=12 endpoint sets is deliberately not
strengthened beyond what the certificate itself proves.

## Exhaustiveness and independent verification

For a flipped edge `e=uv`, let `R_e` count red triangles in
`N_R(u) intersect N_R(v)` and define `B_e` analogously.  Then

```text
q(G flip e) = q(G) - R_e + B_e,  if e is red,
q(G flip e) = q(G) + R_e - B_e,  if e is blue.
```

This follows by bijecting monochromatic five-cliques containing `e` with
monochromatic triangles in the corresponding common neighborhood.

`generate_closure.py` uses bit intersections and a one-pass streaming
breadth-first search.  It retains the complete 6,279-state closure, every one
of the 11,213 distinct sublevel representatives, all quotient multiplicities,
all component profiles, the full flip-objective histogram, and reflection
data in `closure_certificate.json`.

`verify_closure.py` imports only the separately implemented standard-library
color/rotation engine from the prior independent checker, never the
generator.  It counts triangles by a different identity: sum the number of
common induced neighbors over all induced edges and divide by three.  It
independently rescans all 5,669,937 flips, checks objective, canonicality and
freeness at every source, proves closure and seed reachability, and regenerates
the entire 11,213-state endpoint payload and every aggregate entry-for-entry.

`verify_primary_membership.py` compares the q=7 through q=10 endpoints with
four immutable upstream arrays and records all 8,698 source-array positions
in `primary_membership.json`.  All computation is deterministic exact integer
arithmetic; there is no floating point, randomness, solver, or network input
during a run.

## Reproduction

Python 3.11 or later is sufficient.  The core closure requires only the
parent boundary certificate already present in this repository:

```bash
python3 generate_closure.py \
  ../ramsey_r55_cyclic43_q13_boundary_certificate/boundary_certificate.json \
  closure_certificate.regenerated.json

cmp closure_certificate.json closure_certificate.regenerated.json

python3 verify_closure.py \
  ../ramsey_r55_cyclic43_q13_boundary_certificate/boundary_certificate.json \
  closure_certificate.json

python3 -m unittest -v test_closure.py
```

Expected headline output from both exhaustive programs is

```text
states=6279 components=33 edges=12720 cycle_rank=6474
component_sizes={'1': 4, '12': 4, '162': 2, '188': 2, '2': 2, '235': 2, '285': 2, '393': 2, '576': 2, '6': 2, '751': 2, '8': 2, '819': 1, '89': 2, '9': 2}
sublevel_targets={'7': 229, '8': 6, '9': 245, '10': 8218, '11': 1084, '12': 1431}
```

For the ancillary primary-membership check, obtain these four files from
immutable upstream commit
[`02a959f499aa8e3b749a7f7fb3d3fc5f255c3b14`](https://github.com/njallskarp/math_source_code_open/tree/02a959f499aa8e3b749a7f7fb3d3fc5f255c3b14/ramsey_r55_cyclic43):

```text
objective-seven-component-fast.json
objective-eight-component-fast.json
objective-nine-frontier-fast.json
objective-ten-frontier-fast.json
```

Set `UPSTREAM` to that directory and run:

```bash
python3 verify_primary_membership.py \
  closure_certificate.json \
  "$UPSTREAM/objective-seven-component-fast.json" \
  "$UPSTREAM/objective-eight-component-fast.json" \
  "$UPSTREAM/objective-nine-frontier-fast.json" \
  "$UPSTREAM/objective-ten-frontier-fast.json" \
  primary_membership.regenerated.json

cmp primary_membership.json primary_membership.regenerated.json
```

On the research host with CPython 3.11.2, generation took 293 seconds, the
independent full verification took 351 seconds, the membership check took 4.9
seconds, and the five focused tests took 1.1 seconds.

Pinned input hashes are

```text
af8b6892049ace5610e2d7cea4c8642f39f53634287474127990aca0abbe2b85  parent boundary_certificate.json
43a57b3891158d76a8404de8dc8aa51a4719fea2faddf23704b4ba814c978b78  objective-seven-component-fast.json
740c10a6cc72d148ce949749aa8d8f132aa70f9bb0b797ee3e2fbe5ba84fdc1a  objective-eight-component-fast.json
ed95024d463512eb0ade0af77725dd8031ffc712e258283499cff6c06144a693  objective-nine-frontier-fast.json
9b5b3b4747fedfba8b0191f052c9e6d2847aa9c910465f6c29358c2336977df4  objective-ten-frontier-fast.json
```

Generated evidence hashes are

```text
6341720de26b20b0ea768260e31022b6337bcefd322ee24aa46a33ecfb7b34a5  closure_certificate.json
d3bbe18f31407eb6e40c1f7711bfbbfd339e7474878cba3f0d96f5f1fe358ac2  primary_membership.json
78190865f609412316b009c7cdec26a665389c7ec807da2c701beee4f8a54f69  generate_closure.py
ba335e409fbf6af7410e937fa6e75d27b29ad4ed9d987e1509c2734939e9eb45  verify_closure.py
a07c5502e27b01978bd62d61921bdf84abb54072d441e21c3c6d870f17f4d618  verify_primary_membership.py
6bad7a0b50c33c5e2fc6d8a9816bd9642985e92b4d43a34fe36157768b51b1b3  test_closure.py
```

## Scope and mathematical significance

The parent 386-state seed set is inherited from the public, independently
reproduced 1,785-orbit A_12 exit certificate.  This work proves completeness
of every exact-q=13 component meeting those seeds; it does not enumerate all
q=13 neighbors of the 69,071,588-vertex primary sublevel-twelve component.
Nor does it close the full primary sublevel-thirteen component, classify
disconnected low-objective components, construct a `K_5`-free coloring of
`K_43`, or alter the global bounds on `R(5,5)`.

The result materially narrows the family-by-family threshold-thirteen program:
both noncycle boundary families, comprising 404 of 1,785 parent exits, now
have complete exact-level closures and independently checkable boundaries.
Only the 1,381 cycle-only seed family remains unresolved at exact level
thirteen.  Component pairing, the unique reflection-fixed component, the
unexpected exact-level separation of the two medium support sectors, and the
shared 229-state q=7 anchor set are new structural constraints for that next
stage.

Ge, Jayasooriya, Qiu, Sun, and Yuan's
[*Study of Exoo's Lower Bound for Ramsey number R(5,5)*](https://arxiv.org/abs/2212.12630)
studies nearby changes to the same Cyclic(43) coloring but does not state this
exact-level closure.  Angeltveit and McKay's
[*R(5,5) <= 46*](https://arxiv.org/abs/2409.15709) addresses the global upper
bound by a different census.  Novelty is claimed relative to those searched
sources and the refreshed Discovery Net graph, not as a historical-priority
claim over unpublished computation.
