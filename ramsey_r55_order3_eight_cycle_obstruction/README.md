# At least nine moving 3-cycles in a Ramsey (5,5;43) graph

Every order-three automorphism of a hypothetical 43-vertex graph avoiding
a clique and an independent set of order five has **at least nine moving
3-cycles**. The new exclusion is `1^19 3^8`; the earlier work excludes one
through seven. This gives at most 16 fixed vertices for an order-three
element.

This is a structural restriction, not a 43-vertex construction or an
improvement to the Ramsey lower bound. The [complete proof](PROOF.md)
derives a new local deficit constraint, covers all five internal color
splits, and supplies compact certificates.

## Mechanism

At eight moving triangles, the previous degree equality becomes a deficit
budget of two. If a cross block supplies `w` neighbors in the triangle's
own color, its deficit is `2-w+3*[w=3]`, taking values `2,1,0,2`.
The sum of the seven deficits is at most two. The common-neighborhood cap
and degree bound leave exactly 52 local fixed-count/cross-weight profiles.

Color reversal and cycle permutation reduce internal colors to zero
through four red triangles. Independent phase changes normalize seven
anchor words; fixed vertices can then be sorted by their eight-bit
incidence signatures. Each case has a full 43-vertex formula projecting
all 962,598 five-sets. No graph catalog or hard-deficiency assumption is used.

The fixed vertices are essential: the committed [24-vertex red edge
list](moving24.edges) has no monochromatic five-set and satisfies the
moving-vertex deficit bound. Its literal verifier checks all 42,504
five-sets. It is a partial test graph, not a target witness.

## Compact evidence

| red moving triangles | full variables | full clauses | core clauses | RUP additions |
|---:|---:|---:|---:|---:|
| 0 | 7,611 | 585,876 | 460 | 395 |
| 1 | 7,632 | 589,383 | 1,406 | 2,057 |
| 2 | 7,647 | 591,888 | 270 | 302 |
| 3 | 7,656 | 593,391 | 465 | 1,216 |
| 4 | 7,659 | 593,892 | 360 | 118 |

All **4,088 RUP additions** are committed: five proof files total
**171,954 bytes**, and their five clause subsets total **97,473 bytes**.
No large or omitted trace is needed to verify the result.

The C++ checker independently forms the permutation orbits on actual
unordered pairs and reconstructs every clause of each complete formula.
The Python certificate checker verifies every core clause's membership
in that formula, then proves every stored addition by ordinary unit
propagation through the empty clause. It uses no RAT steps or deletions.

## Reproduce

Requirements: Python 3.11+, a C++17 compiler, a POSIX shell and
`sha256sum`. Tested with CPython 3.11.2 and GCC 12.2.0 on Linux.
No solver, third-party Python package, network access or external dataset
is needed.

```sh
sh verify.sh
```

To preserve regenerated formulas and the compiled checker outside Git:

```sh
sh verify.sh --work /tmp/r55-order3-k8
```

The five generated formulas are about 24.4–24.9 MB each. By default they
live in a temporary directory that is removed at completion. The complete
run takes a few minutes on the tested host and ends with:

```text
PASS: order-three type 1^19 3^8 is excluded; minimum moving 3-cycles is 9
```

A single case can be checked with:

```sh
python3 generate.py --red-cycles 1 --output /tmp/r55-k8-r1.cnf
g++ -std=c++17 -O2 -Wall -Wextra -Werror check_formula.cpp -o /tmp/r55-k8-check
/tmp/r55-k8-check 1 /tmp/r55-k8-r1.cnf
python3 check_certificate.py --full /tmp/r55-k8-r1.cnf \
  --core core_r1.cnf --proof proof_r1.rup
```

An optional external check of each compact pair is:

```sh
drat-trim core_r1.cnf proof_r1.rup -U
```

The final five pairs all pass this check. Full reproduction also checks
the local profiles, relabelings, signed/repeated-input counters, elementary
propagation examples and moving fixture. The full-clause checker rejects
missing-clause and changed-literal mutations; core membership rejects an
invented input clause. Optimized and ASan/UBSan builds agree on representative
uniform and mixed internal-color cases.

## Provenance and trust

Discovery used Kissat 4.0.4, commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, and drat-trim, commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Full formulas were solved with
the default seed except case `r=1`, whose selected initial run used
`--seed=1`. After verified core extraction, solving those cores with
`kissat --plain` and trimming with `drat-trim -U -c ... -l ...` produced
the final smaller cores and RUP traces. Deletion lines were removed and
the resulting addition-only traces replayed against the final cores.
These discovery tools are unnecessary for checking the committed evidence.

The imported graph-theoretic input is
[McKay–Radziszowski, R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
The minimum-nine corollary also imports the
[seven-cycle theorem](../ramsey_r55_order3_seven_cycle_obstruction) and its
sparse predecessor. The new eight-cycle exclusion itself is independent
of the order-five theorem and of the team's asymmetric branch.

The analytic bridge remains ordinary unformalized mathematics. Finite
verification trusts the small Python/C++ checking programs and their
runtimes. Separate implementations by the same researcher do not constitute
independent peer review. The proof does not trust a solver's verdict.

The refreshed Discovery Net graph and searched primary sources, including
the external [q6](https://github.com/wustep/maths/tree/main/problems/ramsey-r55/compute/q6)
and [q7](https://github.com/wustep/maths/tree/main/problems/ramsey-r55/compute/q7)
reports, did not contain this eight-cycle exclusion. No universal priority
claim is made.

Remaining order-three types have nine through fourteen moving cycles.
Their larger deficit budgets require a new analysis; they are outside
this pass. The [cumulative symmetry handoff](../ramsey_r55_automorphism_exclusion_handoff)
records the current screening rules.
