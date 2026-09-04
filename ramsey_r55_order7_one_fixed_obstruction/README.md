# An order-seven, one-fixed-vertex obstruction for Ramsey(5,5,43)

No red/blue coloring of `K_43` without a monochromatic `K_5` admits a
color-preserving automorphism with vertex-cycle type

```text
1^1 7^6.
```

This is an exact computer-assisted theorem.  It excludes one structured
symmetry family; it does **not** construct a 43-vertex Ramsey graph and does
not improve a bound on `R(5,5)`.

## The invariant SAT formula

All permutations with cycle type `1^1 7^6` are conjugate.  We use the
permutation fixing vertex zero and sending

```text
1 + 7*c + r  ->  1 + 7*c + ((r+1) mod 7),   0 <= c < 6.
```

Its action on the 903 unordered edges has exactly 129 orbits, all of size
seven.  A Boolean variable records each orbit's color, with true meaning red.
For every five-set `A`, let `M(A)` be the distinct orbit variables on its ten
edges.  The two clauses

```text
OR_{x in M(A)} x          OR_{x in M(A)} not x
```

exclude an all-blue and an all-red five-set, respectively.  Enumerating all
`C(43,5) = 962,598` five-sets and deduplicating produces 273,696 clauses from
136,848 distinct projected masks.

Every vertex in a `(5,5;43)` graph has degree between 18 and 24.  Indeed, a
degree at least 25 contradicts `R(4,5)=25` inside its neighborhood, and the
color-complementary argument gives the lower bound.  The fixed vertex sees
each seven-cycle uniformly, so its red degree is a multiple of seven and
therefore is exactly 21.  Thirty clauses say that exactly three of its six
incident orbit variables are red.

Two complete symmetry breaks reduce search without removing an isomorphism
class:

- The centralizer can permute the six seven-cycles.  Sort their intrinsic
  four-bit profiles: the fixed-vertex edge color followed by the colors at
  the three internal cyclic distances.  The 600 adjacent-order clauses are
  complete because every list of six profiles can be sorted.
- After choosing cycle zero as phase anchor, the centralizer can rotate every
  other cycle independently.  Make each seven-bit cross-edge word between
  cycle zero and that cycle lexicographically least among its rotations.  The
  five necklace constraints contribute 540 clauses and are complete because
  these five phase choices are independent.  Phase changes preserve the
  intrinsic profiles, so the two symmetry breaks are compatible.

The final direct formula has 129 variables and 274,866 distinct clauses.  Its
deterministic DIMACS serialization has SHA-256

```text
a8186032c02f54eb0fd204f4ca12e3dbc8f06f733b904c92ba1bf08247158c04
```

`generate_formula.py` constructs it from the definitions.  The independently
implemented `verify_formula.cpp` instead builds edge orbits with a disjoint-set
union, reconstructs the mathematical clause set, parses the generated DIMACS,
and requires exact set equality.  It obtains the clause-length histogram

```text
3:12  4:42  7:5790  8:3960  9:55440  10:209622.
```

## Exact UNSAT certificate

Kissat 4.0.4 was run on a complete adaptive cube partition.  The four levels
contain 14, 14, 9, and 28 retained leaves, respectively, for 65 leaves total.
The twelve possible split variables are

```text
7 8 9 127 | 10 17 24 | 11 18 25 | 12 19.
```

`proof_tree.py` describes the tree without solver-dependent data and checks
all `2^12 = 4,096` assignments, requiring each to extend exactly one retained
leaf.  Each leaf CNF is the root formula plus its path's unit clauses.

All 65 leaf runs returned UNSAT and emitted binary DRAT proofs.  Each proof
was independently replayed by drat-trim; all returned `s VERIFIED`.  Before
replay, all CNF and proof byte counts and SHA-256 values were checked against
`result.json`.  Interrupted superseded parent runs are not present in that
manifest and play no role in the conclusion.

The retained leaf proofs total 1,304,530,053 bytes, so they are deliberately
not checked into this repository.  `result.json` is the compact evidence: it
records every leaf assignment, CNF hash, proof hash, byte count, solver time,
and checker time.  Full regeneration with the pinned deterministic solver
recreates the omitted payload; the second command below first confirms all
published CNF hashes even when no solver is supplied.

## Reproduction

Lightweight formula and partition audit requires Python 3.11 or later and a
C++20 compiler, with no third-party libraries:

```bash
python3 generate_formula.py formula.cnf
sha256sum formula.cnf

g++ -O3 -std=c++20 -Wall -Wextra -Wpedantic \
  verify_formula.cpp -o verify_formula
./verify_formula formula.cnf

python3 -m unittest -v test_exact.py
python3 proof_tree.py formula.cnf work --jobs 4 | tail -1
```

The last command creates about 673 MB of regenerable cube CNFs and should end
with

```text
{"all_cnf_hashes_match": true, "leaf_count": 65, "partition_assignments_checked": 4096}
```

For full proof regeneration and replay, build
[Kissat commit `8af8e56`](https://github.com/arminbiere/kissat/commit/8af8e56f174b778aef3aa45af9f739b2a5f492c2)
and [drat-trim commit `2e3b2dc`](https://github.com/marijnheule/drat-trim/commit/2e3b2dc0ecf938addbd779d42877b6ed69d9a985),
then run

```bash
python3 proof_tree.py formula.cnf work \
  --solver /path/to/kissat --jobs 4

python3 proof_tree.py formula.cnf work \
  --checker /path/to/drat-trim --jobs 4
```

The first full command must report `all_unsat` and
`all_proof_hashes_match` as true.  The second must additionally report
`all_verified` as true.  The recorded solver binary was Kissat 4.0.4 with
SHA-256 `2d185e...26b45`; the checker binary had SHA-256
`9c09fe...412a`.  These binary hashes are identifying metadata, not a claim
that another conforming build is invalid.

On the research host, retained leaf solver times summed to 5,838.179 seconds.
Checker times summed to 5,381.509 seconds; the final eight-worker audit took
890.507 seconds elapsed.  Formula generation and independent formula
verification each take tens of seconds.  Runs are deterministic, use no
random inputs or floating point, and each leaf is a separate single-threaded
process.  The independent C++ verifier also completed under AddressSanitizer
and UndefinedBehaviorSanitizer with GCC 12.2.0.

## Scope and trust boundary

The implication from an invariant coloring to the SAT assignment and both
symmetry-breaking completeness arguments are mathematical inputs.  The exact
degree restriction imports McKay and Radziszowski's theorem `R(4,5)=25`.
The computational trust boundary consists of the two independently written
formula constructions, ordinary Python/C++ semantics, the regenerated leaf
files, and drat-trim's proof checker.  Kissat's UNSAT answers are not trusted
without proof replay.  Because the bulky proofs are omitted, a checkout by
itself permits complete formula/partition verification but requires proof
regeneration (or byte-identical files matching the manifest) for a fresh UNSAT
replay.

McKay and Radziszowski's
[*R(4,5)=25*](https://doi.org/10.1002/jgt.3190190304) supplies the exact local
degree input.  Exoo's [*A lower bound for R(5,5)*](https://doi.org/10.1002/jgt.3190130113)
and Ge, Jayasooriya, Qiu, Sun, and Yuan's
[*Study of Exoo's lower bound for Ramsey number R(5,5)*](https://arxiv.org/abs/2212.12630)
give the structured-construction context; Angeltveit and McKay's
[*R(5,5) <= 46*](https://arxiv.org/abs/2409.15709) gives the upper-bound
context.  The inspected primary sources and refreshed Discovery Net graph did
not state this cycle-type obstruction.  Novelty is claimed only relative to
those inspected sources, not as a universal priority claim.
