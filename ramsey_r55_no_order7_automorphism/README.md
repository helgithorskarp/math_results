# No order-seven automorphism in a Ramsey(5,5,43) coloring

Let `G` be a graph on 43 vertices with neither a clique nor an independent
set of order five.  Then `Aut(G)` contains no element of order seven.

This is an exact computer-assisted structural theorem.  It does not construct
a 43-vertex Ramsey graph and does not improve a bound on `R(5,5)`.

## Exhaustion of cycle types

An order-seven permutation has only fixed points and seven-cycles.  If `f` is
its number of fixed points and `k>0` its number of seven-cycles, then

```text
f + 7*k = 43,
```

so the only possibilities are

```text
1^1 7^6,  1^8 7^5,  1^15 7^4,
1^22 7^3,  1^29 7^2,  1^36 7^1.
```

The first two were independently certified in the sibling
[`1^1 7^6`](../ramsey_r55_order7_one_fixed_obstruction) and
[`1^8 7^5`](../ramsey_r55_order7_eight_fixed_obstruction) artifacts.  This
directory gives standalone compressed proofs for each of the remaining four
types.

## Exact invariant formulas

Fix the canonical action on vertices `0,...,42`: the first `f` vertices are
fixed, and the remaining vertices lie in consecutive seven-blocks on which
the generator adds one modulo seven.  Its edge orbits comprise

```text
C(f,2)                 fixed--fixed singleton orbits,
f*k                    fixed--cycle seven-edge orbits,
3*k                    within-cycle seven-edge orbits,
7*C(k,2)               between-cycle seven-edge orbits.
```

One Boolean variable records each edge orbit's color.  For every one of the
`C(43,5) = 962,598` five-sets, project its ten edges to distinct orbit
variables and add the two clauses requiring both colors.  Duplicate projected
clauses are removed.

The centralizer of the action gives three compatible normalizations:

1. Sort the `k` cycles by their three phase-invariant internal-distance bits.
2. In that cycle order, sort the `f` fixed vertices by their `k` incidence
   bits to the cycles.  This does not change the first profiles.
3. Choose cycle zero as phase anchor and independently rotate each other cycle
   until its seven-bit cross word with the anchor is lexicographically least
   among its rotations.  This preserves both prior profile families.

Every list can be sorted and every binary word can be rotated to a least
necklace representative, so these steps retain a representative of every
centralizer orbit.  The 15-, 22-, and 29-fixed-point formulas use no other
constraint: no color unit, degree assumption, auxiliary variable, heuristic,
or random choice.

For `1^36 7^1`, the symmetry-only formula did not resolve in a bounded
600-second Kissat probe.  Here one small exact degree consequence closes the
case.  `R(4,5)=25` forces every target degree into `[18,24]`.  Sorting the 36
fixed-to-cycle incidence bits makes them a threshold word.  If `T` is their
number of ones and `S` the number of red internal distances of the moving
seven-cycle, each moving vertex has degree

```text
T + 2*S.
```

For each of the eight internal patterns, two boundary literals enforce
`18 <= T+2*S <= 24`.  Thus 16 transparent four-literal clauses replace a
20,451-variable exploratory BDD encoding.  Two coincide with existing Ramsey
clauses, so they add 14 distinct clauses.  `test_exact.py` exhausts all
`37*8 = 296` threshold/internal cases and checks equivalence to the degree
interval.

The resulting exact instances are:

| cycle type | variables | Ramsey clauses | extra distinct clauses | total clauses |
|---|---:|---:|---:|---:|
| `1^15 7^4` | 219 | 278,336 | 2,088 symmetry | 280,424 |
| `1^22 7^3` | 327 | 317,994 | 860 symmetry | 318,854 |
| `1^29 7^2` | 477 | 476,428 | 304 symmetry | 476,732 |
| `1^36 7^1` | 669 | 919,748 | 35 symmetry + 14 degree | 919,797 |

`generate_formula.py` constructs every formula using least-image edge
representatives.  The independently implemented `verify_formula.cpp` instead
builds the edge orbits with disjoint-set union, reconstructs all mathematical
clauses, parses each DIMACS file, and requires exact set equality.  It also
checks that the orbit-size histogram is

```text
C(f,2) orbits of size 1, and (903-C(f,2))/7 orbits of size 7.
```

All four complete verifier runs passed optimized and AddressSanitizer plus
UndefinedBehaviorSanitizer builds with GCC 12.2.0.

## Standalone DRAT certificates

Kissat 4.0.4 generated one binary DRAT proof per case.  drat-trim verified
each source trace, extracted its used proof core, verified that core, extracted
again, and verified the final retained proof.  The retained proofs are xz
compressed in this directory but stream directly into drat-trim.

| fixed points | Kissat seconds | source proof | retained proof | xz proof | final replay |
|---:|---:|---:|---:|---:|---:|
| 15 | 10.27 | 4,405,594 B | 1,688,368 B | 413,536 B | 9.17 s |
| 22 | 1.54 | 1,168,112 B | 468,079 B | 125,268 B | 3.11 s |
| 29 | 0.58 | 119,333 B | 42,999 B | 13,952 B | 1.66 s |
| 36 | 1.60 | 86,213 B | 1,724 B | 752 B | 3.18 s |

Every full formula hash, source/retained/compressed proof hash, solver count,
and replay count is recorded in `result.json`.  None of the 600-second UNKNOWN
output for the weaker final formula is used.

## Reproduction

Requirements are Python 3.11 or later, a C++20 compiler, xz, and
[drat-trim commit `2e3b2dc`](https://github.com/marijnheule/drat-trim/commit/2e3b2dc0ecf938addbd779d42877b6ed69d9a985).
From this directory run

```bash
DRAT_TRIM=/path/to/drat-trim ./verify.sh
```

The script checks every published hash, runs the focused exact tests, builds
the independent C++ verifier, regenerates and checks all four formulas, tests
each xz stream, and replays every proof.  It must end with four occurrences of
`s VERIFIED`.

Proof regeneration, if desired, uses
[Kissat commit `8af8e56`](https://github.com/arminbiere/kissat/commit/8af8e56f174b778aef3aa45af9f739b2a5f492c2):

```bash
python3 generate_formula.py --fixed 15 f15.cnf
/path/to/kissat f15.cnf f15.drat
```

and analogously for fixed counts 22, 29, and 36.  The recorded Kissat binary
has SHA-256 `2d185e...26b45`; the drat-trim binary has SHA-256
`9c09fe...412a`.  These identify the research-host builds.  Solver exit codes
are not trusted for the theorem because every retained proof is independently
replayed.

## Combined trust boundary and scope

For the four new cases, the trust boundary consists of the orbit reduction,
the three centralizer normalization arguments, the `R(4,5)=25` degree input
used only for the last case, the two independent formula constructions, the
checked-in compressed proofs, xz, drat-trim, and ordinary Python/C++ semantics.
The complete no-order-seven corollary additionally depends on the sibling
certificates for fixed counts one and eight.  The eight-fixed proof is
standalone.  The one-fixed computation's 1.304 GB checked proof tree is omitted
under the compact-artifact policy, but all 65 leaves were hash-gated and
replayed on the research host and its complete assignments/hashes remain in
that artifact's `result.json`.

Exoo's [*A lower bound for R(5,5)*](https://doi.org/10.1002/jgt.3190130113)
and Ge, Jayasooriya, Qiu, Sun, and Yuan's
[*Study of Exoo's lower bound for Ramsey number R(5,5)*](https://arxiv.org/abs/2212.12630)
provide the structured-coloring context.  McKay and Radziszowski's
[*R(4,5)=25*](https://doi.org/10.1002/jgt.3190190304) supplies the sole imported
degree theorem.  Angeltveit and McKay's
[*R(5,5) <= 46*](https://arxiv.org/abs/2409.15709) gives the upper-bound
context.  The inspected sources and refreshed Discovery Net graph did not
state the complete order-seven obstruction.  Novelty is claimed only relative
to those inspected sources, not as a universal priority claim.
