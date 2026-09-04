# No order-15 automorphism in Ramsey `(5,5;43)`

Let `G` be a graph on 43 vertices with neither a clique nor an independent
set of order five. Then `Aut(G)` has no element of order 15.

This is an exact computer-assisted structural theorem, not a 43-vertex
construction or an improvement to the Ramsey bound. It does not claim that
15 cannot divide the automorphism-group order: a group divisible by 15 need
not contain an element of order 15.

## Complete power filter

Write the cycle counts of an order-15 permutation as

```text
(a,b,c,f) = (#15-cycles, #5-cycles, #3-cycles, #fixed points).
```

The cube has order five and `3a+b` five-cycles. The certified order-five
classification permits only seven or eight such cycles. The fifth power has
order three and `5a+c` 3-cycles; the sparse-motion theorem requires at least
seven. Exhausting

```text
15a + 5b + 3c + f = 43
```

leaves exactly six types:

| `(a,b,c,f)` | cube 5-cycles | fifth-power 3-cycles | orbit variables | clauses | CNF SHA-256 |
|---|---:|---:|---:|---:|---|
| `(1,4,2,2)` | 7 | 7 | 99 | 120,666 | `7bc3cd5254f45248274c3767c5dd822e510d9ceb07caa5acfbd2f93dd5e2921a` |
| `(2,1,0,8)` | 7 | 10 | 93 | 121,030 | `527f12749c74e49eb2efe961610a4a4ad5afb218e1db37967212be9bb3abb7ed` |
| `(2,1,1,5)` | 7 | 11 | 79 | 119,598 | `0892d64707c95c11c74f92688eea708a92232adcb91cc1061ee89cde57b46e97` |
| `(2,1,2,2)` | 7 | 12 | 71 | 118,788 | `673bce285ad3d5b5cfc9ff9b8747ebb04d6d9325664a6f19d184c3c185c3911e` |
| `(2,2,0,3)` | 8 | 10 | 73 | 120,846 | `4aa4041d0d9a2e708e6450615d35a57d15c6d693c2b78eaac16cdc7bb166f164` |
| `(2,2,1,0)` | 8 | 11 | 67 | 119,446 | `68efaa8fc89e69959c25ad08a9601af8ca889f5aef19f09f3a7e68f3aa6bfd7e` |

`verify_cycle_types.py` independently enumerates all nonnegative cycle
counts, computes the permutation order and both power types, and reproduces
this list.

## Direct orbit formulas and certificates

For each type, label each cycle consecutively and let the order-15
permutation advance every cycle by one. A Boolean variable records each
orbit of unordered vertex pairs. For every one of the
`C(43,5)=962,598` five-sets, two clauses over its distinct pair-orbit
variables require both colors. Duplicate clauses are removed. No symmetry
breaking or degree lemma is used in these six formulas.

Kissat 4.0.4 returned UNSAT for every case in 1.25--3.12 process-seconds.
drat-trim verified all six source traces, two successive retained cores, and
each final checked-in proof. The final proofs total 549,601 uncompressed
bytes and 98,044 xz-compressed bytes. Their exact per-case hashes, line
counts, additions, and deletion hints are in `result.json`.

The Python generator constructs edge-orbits by least images under all 15
powers. The independent C++20 verifier constructs the permutation from its
cycle counts, builds edge-orbits with disjoint-set unions, reconstructs every
Ramsey clause with nested loops, and requires exact equality with the parsed
DIMACS clause set.

## Reproduction

Requirements are CPython 3.11 or later, a C++20 compiler, xz, and
[drat-trim commit `2e3b2dc`](https://github.com/marijnheule/drat-trim/commit/2e3b2dc0ecf938addbd779d42877b6ed69d9a985).
No Python package is required.

```bash
DRAT_TRIM=/path/to/drat-trim ./verify.sh
```

The script byte-compares a regenerated manifest, rechecks the cycle-type
filter, regenerates all formulas, independently reconstructs their clause
sets, and streams every proof to drat-trim. Every proof verdict must be
`s VERIFIED`. The C++ verifier is also tested under AddressSanitizer and
UndefinedBehaviorSanitizer.

Proof regeneration used
[Kissat commit `8af8e56`](https://github.com/arminbiere/kissat/commit/8af8e56f174b778aef3aa45af9f739b2a5f492c2).
The recorded Kissat binary SHA-256 is
`2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`;
the drat-trim binary SHA-256 is
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

## Scope, provenance, and trust boundary

The power filter depends on the three order-five artifacts and the sparse
order-three theorem. The direct formulas close all six remaining types. The
mathematical inputs are the power-cycle calculation and orbit-CNF
equivalence. The computational trust boundary comprises the independent
Python/C++ reconstructions, exact runtime/compiler semantics, xz, the
checked-in proof bytes, and pinned drat-trim. Kissat's exit code is not
trusted without proof replay.

The inspected structured-construction literature and refreshed Discovery
Net graph did not state this complete order-15 obstruction. Novelty is
claimed only relative to those searched sources, not as a universal
priority claim.
