# Four middle order-five automorphism obstructions for Ramsey `(5,5,43)`

Let `G` be a graph on 43 vertices with neither a clique nor an independent
set of order five. No automorphism of `G` has any of the four cycle types

```text
1^13 5^6,  1^18 5^5,  1^23 5^4,  1^28 5^3.
```

This is an exact computer-assisted theorem about four of the eight possible
order-five types. It is not a complete order-five obstruction, does not
construct a 43-vertex Ramsey graph, and does not improve a Ramsey bound.

## Exact invariant formulas

An order-five permutation on 43 vertices has cycle type `1^f 5^k`, where
`f+5k=43`. For a fixed type, its action on the 903 unordered edges has

```text
C(f,2) + f*k + 2*k + 5*C(k,2)
```

orbits. The terms count fixed--fixed, fixed--cycle, within-cycle, and
between-cycle edge orbits. One Boolean variable records each orbit color.
For every five-set `A`, let `M(A)` be the set of distinct orbit variables on
its ten edges. The two clauses

```text
OR_{x in M(A)} x          OR_{x in M(A)} not x
```

are exactly the requirement that `A` use both colors. All
`C(43,5)=962,598` five-sets are enumerated and their projected clauses are
deduplicated. No degree constraint, auxiliary variable, color-fixing clause,
heuristic condition, or random choice is used.

Three compatible centralizer normalizations are complete:

1. Sort the five-cycles by their two-bit internal-distance profiles.
2. Sort fixed vertices by their incidence profiles to the ordered cycles.
3. Use cycle zero as phase anchor and independently rotate every other cycle
   so its five-bit cross-edge word with the anchor is least among rotations.

Every profile list can be sorted; relative phase changes preserve the first
two profile families. Thus each centralizer orbit retains a representative.

The deterministic formulas are:

| cycle type | variables | clauses | CNF SHA-256 |
|---|---:|---:|---|
| `1^13 5^6` | 243 | 410,034 | `5533d4cbf74b46b754ebf6c23d3779474ec831aabb55122c6cebef56bcf84fa8` |
| `1^18 5^5` | 303 | 405,458 | `f1f78ce8efc1aba0b661d36541777680b8ab1c6910e6ec53addf4a755886b9ca` |
| `1^23 5^4` | 383 | 439,398 | `5d5f17fce53b7bb0cdfdd82beb7366da2386436f4a4912fd38869d2a839394eb` |
| `1^28 5^3` | 483 | 540,744 | `d518282e91451281243e9f99a84739c6de99b9e42e3e2287f74541e9c047f789` |

## Independently replayed UNSAT certificates

Kissat 4.0.4 generated a DRAT trace for each formula. Every source trace was
verified by drat-trim; two successive core extractions were each replayed,
and the final retained trace was replayed again. Only the final compact xz
streams are checked in. `result.json` records every compressed and
uncompressed byte count and SHA-256 digest.

The final four streams total 3,784,444 compressed bytes. After decompression
they total 30,288,544 bytes, with 230,738 additions and 313,398 deletion
hints. The recorded source-proof generation times were 38.90, 38.86, 12.57,
and 7.98 process-seconds in increasing fixed-count order.

The Python generator constructs edge orbits by least images under all five
powers of the permutation. The independent C++20 verifier instead constructs
the orbits with a disjoint-set union, regenerates every Ramsey and symmetry
clause with nested integer loops, parses the generated DIMACS, and requires
exact set equality before proof replay.

## Reproduction

Requirements are CPython 3.11 or later, a C++20 compiler, xz, and
[drat-trim commit `2e3b2dc`](https://github.com/marijnheule/drat-trim/commit/2e3b2dc0ecf938addbd779d42877b6ed69d9a985).
No Python package is required.

```bash
DRAT_TRIM=/path/to/drat-trim ./verify.sh
```

This regenerates and byte-compares the manifest, runs the scope tests,
compiles the independent verifier with

```text
g++ -O3 -std=c++20 -Wall -Wextra -Wpedantic
```

and reconstructs and verifies all four formulas before streaming each proof
to drat-trim. The final four proof checks must each print `s VERIFIED`. On
the research host the complete optimized verification took 2m32.974s using
CPython 3.11.2 and GCC 12.2.0. The independent verifier also reproduced all
four formulas under AddressSanitizer and UndefinedBehaviorSanitizer.

Proof regeneration, if desired, uses
[Kissat commit `8af8e56`](https://github.com/arminbiere/kissat/commit/8af8e56f174b778aef3aa45af9f739b2a5f492c2):

```bash
python3 generate_formula.py --prime 5 --fixed 13 formula.cnf
/path/to/kissat formula.cnf proof.drat
```

The recorded Kissat binary has SHA-256
`2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`;
the drat-trim binary has SHA-256
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.
These hashes identify the research-host builds; the checked proofs, not the
solver exit codes, establish unsatisfiability.

## Remaining order-five frontier

The eight order-five types have fixed counts

```text
3, 8, 13, 18, 23, 28, 33, 38.
```

The present theorem closes the middle four. The types with fixed counts 3,
8, 33, and 38 remain open. In bounded triage, both Kissat at 60 seconds and
CaDiCaL at 120 seconds returned no verdict on each of those four formulas.
Those timeouts establish nothing and are not part of the certificate.

The exact construction consequence is correspondingly limited: an
order-five symmetry in a hypothetical target must have one of

```text
1^3 5^8,  1^8 5^7,  1^33 5^2,  1^38 5^1.
```

## Scope, provenance, and trust boundary

The mathematical inputs are the cycle-type reduction, orbit-CNF equivalence,
and completeness of the three centralizer normalizations. The computational
trust boundary comprises the independent Python and C++ formula
reconstructions, CPython and C++ exact integer/container semantics, xz, the
checked-in proof bytes, and drat-trim. No result here depends on
`R(4,5)=25`, a graph catalog, floating point, randomness, or solver trust.

Exoo's [*A lower bound for R(5,5)*](https://doi.org/10.1002/jgt.3190130113)
and Ge--Jayasooriya--Qiu--Sun--Yuan's
[*Study of Exoo's lower bound for Ramsey number R(5,5)*](https://arxiv.org/abs/2212.12630)
give the structured-construction context. Angeltveit--McKay's
[*R(5,5) <= 46*](https://arxiv.org/abs/2409.15709) supplies the current upper
bound. The inspected primary sources and refreshed Discovery Net graph did
not state these four cycle-type exclusions. Novelty is claimed only relative
to those searched sources, not as a universal priority claim.
