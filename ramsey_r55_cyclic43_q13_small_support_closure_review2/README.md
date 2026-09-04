# Independent review of the Cyclic(43) small-support `q=13` closure

**Verdict: accept with high confidence, within the stated finite-basin
scope.**  This review independently verifies the exact computational claim
in
[`ramsey_r55_cyclic43_q13_small_support_closure`](../ramsey_r55_cyclic43_q13_small_support_closure/README.md)
at immutable commit
[`414c28de80207a4ac8d4806e8b3e339b61f7c34e`](https://github.com/helgithorskarp/math_results/tree/414c28de80207a4ac8d4806e8b3e339b61f7c34e/ramsey_r55_cyclic43_q13_small_support_closure).

The 18 selected boundary orbits meet exactly six complete connected
components of the exact-objective-13 graph in the `C_43` rotation quotient.
The verified component sizes are `59,59,10,10,6,6`, with 228 quotient edges
and cycle rank 84.  This does not close the full objective-13 landscape and
does not alter the known bounds on `R(5,5)`.

## Definition-first independent method

The target generator obtains flip deltas from common-neighbour triangle
counts, and its internal verifier enumerates triples in those common
neighbourhoods.  The new
[`verify_direct_k5.cpp`](verify_direct_k5.cpp) uses neither method.  It
precomputes all

```text
C(43,5) = 962,598
```

five-vertex subsets and scans their ten edge colours directly.  If a
five-set has `r` red edges, its contribution to the monochromatic-`K5`
objective and to one-edge flip deltas is completely determined:

| `r` | current contribution | relevant flip effect |
|---:|---:|---|
| 0 | 1 blue `K5` | flipping any of its ten edges destroys it |
| 1 | 0 | flipping its unique red edge creates a blue `K5` |
| 9 | 0 | flipping its unique blue edge creates a red `K5` |
| 10 | 1 red `K5` | flipping any of its ten edges destroys it |

All other colour counts contribute zero to every one-edge delta.  This
gives the objective and all 903 neighbouring objectives in one direct pass,
without invoking the common-neighbour identity used by the reviewed code.

For every one of the 150 certificate states, the checker:

- directly obtains objective 13 from the five-sets;
- independently implements the lexicographically least 15-word rotation
  representative and proves the `C_43` orbit is free;
- scans all 903 flips and requires every objective-13 neighbour to occur in
  the certificate;
- rebuilds reachability from the 18 seeds, all six components, edge count,
  cycle rank, support census, and reflection pairing; and
- reconstructs the full distinct sublevel endpoint sets and directly
  recounts the objective of all 274 endpoints in a second five-set pass.

The seed set is independently selected from the hash-pinned parent boundary
by its `{17,21}` and `{17,17,21}` support signatures.  The eight objective-6
and 16 objective-8 endpoints are also checked for membership in the pinned
primary representative arrays.

The resulting exact statistics are

```text
q13 states:                    150
all flips checked:             135,450
internal directed incidences:  456
undirected quotient edges:     228
components:                    6
cycle rank:                    84
dihedral orbits:               75
reflection-fixed states:       0
support census:                {17,17,21}:8, {17,21}:118, {21}:24
distinct endpoints:            q6:8, q8:16, q10:20, q11:52, q12:178
```

In addition, I ran the target generator and obtained a byte-for-byte copy of
its 107,192-byte certificate, then ran its separately written explicit-
triple verifier and all five tests.  Every check passed.

## Reproduction

Requirements: a C++20 compiler with OpenMP support.  I used GCC 12.2.0.
The input files are:

- the parent boundary at
  [`ramsey_r55_cyclic43_q13_boundary_certificate/boundary_certificate.json`](../ramsey_r55_cyclic43_q13_boundary_certificate/boundary_certificate.json);
- the reviewed closure certificate at
  [`ramsey_r55_cyclic43_q13_small_support_closure/closure_certificate.json`](../ramsey_r55_cyclic43_q13_small_support_closure/closure_certificate.json);
- `objective-six-component-representatives.json`; and
- `objective-eight-component-fast.json`.

Obtain the last two files from immutable external source commit
[`02a959f499aa8e3b749a7f7fb3d3fc5f255c3b14`](https://github.com/njallskarp/math_source_code_open/tree/02a959f499aa8e3b749a7f7fb3d3fc5f255c3b14/ramsey_r55_cyclic43).
Their expected SHA-256 values are recorded below.

From this review directory, with `UPSTREAM` pointing to that external
`ramsey_r55_cyclic43` directory, run:

```sh
g++ -O3 -std=c++20 -Wall -Wextra -Wpedantic -fopenmp \
  verify_direct_k5.cpp -o verify_direct_k5

OMP_NUM_THREADS=16 ./verify_direct_k5 \
  ../ramsey_r55_cyclic43_q13_boundary_certificate/boundary_certificate.json \
  "$UPSTREAM/objective-six-component-representatives.json" \
  "$UPSTREAM/objective-eight-component-fast.json" \
  ../ramsey_r55_cyclic43_q13_small_support_closure/closure_certificate.json
```

The output must match [`EXPECTED_OUTPUT.txt`](EXPECTED_OUTPUT.txt).  The
parallel loops write disjoint per-state records, so thread count changes
runtime but not the result.

Input hashes:

```text
af8b6892049ace5610e2d7cea4c8642f39f53634287474127990aca0abbe2b85  boundary_certificate.json
aea99967a1a3cc41c640c73c471a73b015259186619495ffa5223968cb48d320  objective-six-component-representatives.json
740c10a6cc72d148ce949749aa8d8f132aa70f9bb0b797ee3e2fbe5ba84fdc1a  objective-eight-component-fast.json
85e271af8ebbd55c8bf8e6ad033122911f750a13dc95f638d74681f8c03e4d1e  closure_certificate.json
```

## Why the completeness conclusion follows

Let `S` be the 150 listed quotient states.  The direct five-set computation
proves that every state of `S` has objective 13.  For every `x` in `S`, all
903 single-edge flips are examined, and each objective-13 rotation orbit
reached from `x` is again in `S`.  Conversely, graph search from the 18
specified seeds reaches every element of `S`.  Therefore `S` is exactly the
union of the exact-level connected components meeting those seeds: closure
gives one inclusion and reachability gives the other.  The independently
rebuilt adjacency graph then proves the six-component statistics.

Rotation quotienting loses no move here.  The seed colouring is
rotation-invariant, each listed toggle orbit is checked to have all 43
members, and canonicalization is applied after every flip.  Reflection maps
the closed set to itself and pairs the six components without fixing a state
or a component.

## Trust boundary and uncertainty

The new checker is a complete proof computation for the closure **from the
18 supplied seeds**.  It trusts standard C++ integer and container semantics,
the compact key-specific JSON parser, the compiler, and the four hash-pinned
input files.  It uses no floating point, randomness, solver, native library,
network input during execution, or generated uncommitted certificate.

The claim that these are exactly the desired small-support exits imports the
parent 1,785-orbit boundary certificate.  That boundary has both an earlier
independent review and a public clean-room reproduction.  Membership of the
deep objective-6 and objective-8 endpoints imports the two pinned primary
arrays.  This review does not regenerate the much larger primary
sublevel-12 component.

Residual uncertainty is therefore about the inherited upstream basin, not
the six-component exact-level closure.  The reviewed statement correctly
limits its mathematical significance: it neither classifies disconnected
low-objective colourings nor produces a `K5`-free colouring of `K43`.

## Strengthening and improvement opportunities

1. Publish a compact canonical adjacency list, not only the state and
   aggregate payloads, so component structure can be checked without a full
   rescan while retaining the rescan as the completeness certificate.
2. Vendor or mirror the two small primary-anchor inputs beside the closure,
   subject to repository-size policy, to make the reproduction command
   entirely commit-local.
3. State consistently that the six components live in the rotation
   **quotient** exact-level graph; the current source does this, but the
   shorter graph title can be misread as a statement about labelled states.
4. Extend the same closure computation to the `{5,16}`, `{5,16,16}`, and
   cycle-only boundary strata, prioritizing strata whose endpoint minima
   suggest a connection back to the primary basin.
5. Preserve the current novelty qualification.  These exact finite
   components are useful search geometry, not by themselves progress on the
   numerical bounds for `R(5,5)`.

## Literature scope

- Ge, Jayasooriya, Qiu, Sun, and Yuan,
  [*Study of Exoo's Lower Bound for Ramsey number R(5,5)*](https://arxiv.org/abs/2212.12630),
  studies the underlying Cyclic(43) construction but not this quotient
  closure.
- Angeltveit and McKay,
  [*R(5,5) <= 46*](https://arxiv.org/abs/2409.15709), concerns the global
  upper bound rather than this local exact-objective basin.
