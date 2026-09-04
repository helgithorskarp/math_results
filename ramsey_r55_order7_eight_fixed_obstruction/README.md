# An order-seven, eight-fixed-point obstruction for Ramsey(5,5,43)

No red/blue coloring of `K_43` without a monochromatic `K_5` admits a
color-preserving automorphism with vertex-cycle type

```text
1^8 7^5.
```

This exact computer-assisted theorem excludes one symmetry family; it does
not construct a 43-vertex Ramsey graph or improve a bound on `R(5,5)`.
Together with the sibling [`1^1 7^6` obstruction](../ramsey_r55_order7_one_fixed_obstruction),
it implies that an order-seven automorphism of a hypothetical target would
have to fix at least 15 vertices.

## Exact invariant formula

All permutations with cycle type `1^8 7^5` are conjugate.  Label the eight
fixed vertices `0,...,7`; on each remaining block let the generator add one
modulo seven.  The 903 unordered edges split as follows:

```text
fixed--fixed:       C(8,2)       =  28 singleton orbits
fixed--cycle:       8*5          =  40 seven-edge orbits
within cycles:      5*3          =  15 seven-edge orbits
between cycles:     C(5,2)*7     =  70 seven-edge orbits
                                  ----
                                   153 variables
```

One Boolean variable records the color of each edge orbit.  For every
five-set `A`, let `M(A)` be the distinct variables on its ten edges.  The two
clauses

```text
OR_{x in M(A)} x          OR_{x in M(A)} not x
```

require both colors on `A`.  Directly enumerating all
`C(43,5) = 962,598` five-sets and deduplicating their projections gives
273,664 Ramsey clauses.

The centralizer of the order-seven action supplies three sequential,
compatible normalizations:

1. Permute the five seven-cycles to sort their phase-invariant three-bit
   internal-distance profiles.  Adjacent inversion blocking gives
   `4*C(8,2) = 112` clauses.
2. With that cycle order fixed, permute the eight fixed vertices to sort
   their five-bit incidence words to the cycles.  This gives
   `7*C(32,2) = 3,472` clauses.  It does not change the cycle profiles.
3. Choose cycle zero as phase anchor and rotate each other cycle independently
   so its seven-bit cross-edge word with the anchor is lexicographically least
   in its necklace.  There are 20 binary necklaces of prime length seven, so
   this gives `4*(128-20) = 432` clauses.  Phase shifts preserve both preceding
   profile families.

Every list can be sorted and every word can be rotated to a least necklace
representative, so each step retains at least one representative of every
centralizer orbit.  No color-fixing clause, degree assumption, auxiliary
variable, heuristic constraint, or random choice is used.

The resulting CNF has 153 variables and 277,680 clauses.  Its deterministic
DIMACS serialization has SHA-256

```text
fdbd24c09d0163d1f524cbd0d35a6e55ee2308cc43409a419aa336b3dbab645a
```

`generate_formula.py` constructs the formula by least-image edge orbits.
`verify_formula.cpp` is an independent implementation: it obtains the orbits
with disjoint-set union, reconstructs the mathematical clause set, parses the
DIMACS, and requires exact set equality.  Its clause-length histogram is

```text
3:10  4:80  5:840  6:392  7:14432
8:35560  9:89880  10:136486.
```

## Standalone UNSAT certificate

Kissat 4.0.4 at commit `8af8e56` returned UNSAT after 71,792 conflicts and
110,194 decisions, using 61 MiB maximum resident memory and 10.28 process
seconds.  Its 5,962,352-byte binary DRAT proof was checked and reduced twice
by drat-trim's verified-core extraction.  The retained binary proof is
2,146,217 bytes; xz compression reduces the checked-in file to 580,180 bytes.

The final proof has SHA-256

```text
e00f323cca6a56e21f705299a0d5cad883a8772ccb90f4e6427de082d0b310ed
```

after decompression, while `proof.drat.xz` has SHA-256

```text
42844fc6534671a55617bf6851c36df9d134729a43788d6d83c9bd4bfc98a0b0.
```

drat-trim independently replayed the retained proof against the regenerated
formula, used 588,548 resolution steps, and returned `s VERIFIED` in 8.74
seconds.  The proof is streamed from xz during reproduction, so no large
temporary proof file is needed.

## Reproduction

Requirements are Python 3.11 or later, a C++20 compiler, xz, and
[drat-trim commit `2e3b2dc`](https://github.com/marijnheule/drat-trim/commit/2e3b2dc0ecf938addbd779d42877b6ed69d9a985).
From this directory run

```bash
DRAT_TRIM=/path/to/drat-trim ./verify.sh
```

The script checks all published hashes, regenerates and hashes the 10.6 MB
formula, builds and runs the independent C++ checker, tests the xz stream, and
replays the binary proof.  Its final line must be `s VERIFIED`.  Focused
standard-library tests can also be run with

```bash
python3 -m unittest -v test_exact.py
```

Proof regeneration, if desired, uses
[Kissat commit `8af8e56`](https://github.com/arminbiere/kissat/commit/8af8e56f174b778aef3aa45af9f739b2a5f492c2):

```bash
python3 generate_formula.py formula.cnf
/path/to/kissat formula.cnf proof.regenerated.drat
```

The recorded Kissat binary has SHA-256 `2d185e...26b45`; the drat-trim binary
has SHA-256 `9c09fe...412a`.  These identify the research-host builds, while
the checked proof—not the solver's exit code—establishes UNSAT.  The complete
C++ verifier also passed AddressSanitizer and UndefinedBehaviorSanitizer with
GCC 12.2.0.

## Scope and trust boundary

The mathematical trust inputs are the orbit reduction and completeness of
the three centralizer normalizations.  The computational boundary comprises
the two independent formula reconstructions, the checked-in compressed proof,
xz decompression, drat-trim, and ordinary Python/C++ execution semantics.
Kissat is not trusted for the final conclusion because its proof is replayed.

Exoo's [*A lower bound for R(5,5)*](https://doi.org/10.1002/jgt.3190130113)
and Ge, Jayasooriya, Qiu, Sun, and Yuan's
[*Study of Exoo's lower bound for Ramsey number R(5,5)*](https://arxiv.org/abs/2212.12630)
provide the structured-coloring context.  Angeltveit and McKay's
[*R(5,5) <= 46*](https://arxiv.org/abs/2409.15709) gives the upper-bound
context.  The inspected sources and refreshed Discovery Net graph did not
state this cycle-type obstruction.  Novelty is claimed only relative to those
inspected sources, not as a universal priority claim.
