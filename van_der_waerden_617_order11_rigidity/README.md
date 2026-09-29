# Excluding the order-11 multiplicative construction at 617

**Exact computer-assisted lemma.** A coloring
`c : F_617^* -> {0,1}` that avoids every monochromatic progression
`a, a+d, ..., a+6d` with `d != 0` and all seven terms nonzero, and is
invariant under a multiplicative subgroup of order **at least 11**, is
the quadratic-residue coloring up to global color exchange.

Consequently, a different progression-free nonzero pattern at this
modulus has multiplicative stabilizer of order **at most 8**. This
strengthens the previous order-at-least-14 threshold by closing index
56, the order-11 construction family. It does not establish existence
at order 8, an interval upper bound, or a new lower bound for `W(2,7)`.
Throughout, `W(2,7)` means two colors and seven terms.

Author and role: **six-vdw-1, researcher**, 2026-09-29. Approach:
construction/counterexample. SAT explored possible constructions; the
published proof uses exact exhaustive computation without a SAT library
or imported solver proof. Validation is by the same author and is not
independent peer review.

## Finite reduction and exact proof

The field has prime order 617, and its nonzero group is cyclic of order
`616=2^3*7*11`, with primitive root 3. For `m | 616`, invariance under
`H_m=<3^m>` means `c(3^e)=y[e mod m]` for a binary cyclic word of length
`m`. A progression imposes a not-all-equal constraint on its set of
coset indices, including any repeated indices.

`orbit_exact.cpp` enumerates **every one of the 617*616=380072 pairs
(a,d)**, with `d != 0`, to build these index sets. It removes every set
involving zero's separate index before solving. Thus the proved
classification concerns the punctured field and is valid irrespective
of any color assigned to zero.

Normalize `y[0]=0` using global complementation. For an even index, every
nonalternating word has a unique first deviation `j=1,...,m-1` from
`y[v]=v mod 2`. Fix that prefix, propagate not-all-equal constraints,
then branch on both colors of a remaining variable. A constraint with
both assigned colors is already satisfied; an unsatisfied constraint
with no free vertex is contradictory; one with one free vertex forces
the opposite of its assigned color. An unassigned singleton is also
contradictory. Simultaneous opposing forced colors cause a contradiction.
All other choices are handled by exhaustive binary branching. Therefore
closing every first-deviation case excludes every nonalternating word.
The alternating word itself satisfies all retained constraints.

| Index | Subgroup order | Full edge sets | Punctured edge sets | Exhaustive nodes |
| --- | --- | --- | --- | --- |
| 44 | 14 | 13112 | 12936 | 1895 |
| 56 | 11 | 16828 | 16632 | 18845 |

At index 56 the 55 cases yield 9450 contradictions and 127365 propagated
variables in total. Case `j=1` alone has 8023 nodes; all cases closed
below the explicit budgets. Exact per-case counts and edge-set hashes
are in `expected.json`.

Every possible original index for a subgroup of order at least 11 is
in `{1,2,4,7,8,11,14,22,28,44,56}`. Each divides either 44 or 56. If
`m | M`, an `H_m`-invariant coloring is also `H_M`-invariant, so the two
classification computations cover all such subgroups. For an odd
original index, the alternating coloring would have that odd period,
which is impossible. The two quadratic color orientations remain for
every compatible even index. This proves the lemma and, since subgroup
orders divide 616, the stabilizer bound at most 8.

## Reproduce and check

From this directory, with one CPU/thread:

```sh
mkdir -p build
g++ -std=c++17 -O2 -Wall -Wextra -Wconversion -Wshadow \
  orbit_exact.cpp -o build/orbit-exact
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 validate.py --checker build/orbit-exact
```

Used versions: GCC 12.2.0 and Python 3.11.2; no external library is
required. The final validation output reports `verified=true`, subgroup
threshold 11, and nonquadratic stabilizer bound 8. To run the new
exhaustive case alone:

```sh
build/orbit-exact --m 56 --nodes 1000000 --seconds 120
```

Its final status is `RIGIDITY_CERTIFIED`, with 18845 nodes. The measured
release run took 4.29 seconds and 11384 KiB peak RSS in the shared scope;
timing depends on the environment. Node and time budgets terminate with
`INCOMPLETE_*`, exit code 2, and no classification. The `--first` and
`--last` options allow individual cases to be resumed, but a proper
subrange gets only `CASE_RANGE_CERTIFIED`.

Validation compares the entire native constraint sets against explicit
Python coset multiplication and against a separate spacing-one/scaling
enumeration. The latter is exact because multiplying a field progression
by a nonzero scalar cyclically shifts its coset indices. Native Boolean
search is compared against exhaustive enumeration on 1000 deterministic
small instances. All 256 index-eight words are also enumerated, leaving
only masks 85 and 170. Three fail-closed controls cover exhausted node
budget, exhausted time budget, and a partial case range. The index-56
proof and small controls also passed address/undefined-behavior sanitizer
checks.

All masks are unsigned 64-bit integers; the accepted indices are at most
62, so the largest shift is below 64. Field-coordinate products are
below 4320. Recursion assigns a new variable each branch. The trust
boundary is the source, compiler/runtime and elementary proof bridge.
No bulky enumeration, binary, solver log or external input is needed.

## Construction frontier and provenance

[The preceding threshold](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_multiplicative_rigidity)
closed indices 8, 28 and 44. Its verified source commit was
`3f094bee56fe0984d0848b202e16d99d522558e2`; Discovery Net lemma
`bafkreigz4vflgi4o334f7kdm5extw6klor64pthtafrl4izdoqwubz4sje`.
This directory supplies a self-contained recomputation of index 44 and
the new index-56 proof.

The next symmetry orders are 8 and 7, with indices 77 and 88. Bounded
SAT probes at 100000 conflicts returned **UNKNOWN** for both; neither
family is excluded. A useful exact search normalization is to fix
`y[0]=y[1]=0`: every nonalternating cyclic word has an equal adjacent pair,
and coset shift plus color complement moves that pair to these values.
For an odd cyclic word, such a pair always exists. This reduction does
not depend on the inconclusive solver probes.

The incumbent and notation were rechecked against
[Monroe, JCMCC 128, Tables 1 and 2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/),
which give `>3703` and modulus 617 for two colors/seven terms, using
`W(length,colors)`. Multiplicative prepartitioning is an established
method in [Heule, Section 4.3](https://www.cs.utexas.edu/~marijn/publications/JOC_08_03_A01.pdf).
[Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
give the unzipped 617 construction. The new claim is the quantified
order-11 obstruction, not novelty of multiplicative orbit methods; it
was not found in the inspected primary sources, without a priority claim.

Complementary work studies
[affine QR617 seams](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_phase_rigidity)
and [the 29-edit necessity for interval extensions](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_repair_distance).
Those claims and this field-template classification have different scopes.
No coloring on `[1,3704]` was found in this pass; the target remains open.
