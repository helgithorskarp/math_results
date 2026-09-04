# No order-five automorphism in a Ramsey (5,5;43) graph

A hypothetical 43-vertex graph with neither a clique nor an independent
set of order five **cannot have an automorphism of order five**. This
package closes the last cycle type, `1^3 5^8`, by refuting both incidence
patterns left by the analytic fixed-incidence theorem.

Consequently `5` does not divide the automorphism-group order. Combined
with the earlier prime-order exclusions, the automorphism group has order
`2^a 3^b`. No 43-vertex witness or Ramsey bound improvement is claimed.

## New finite certificates

The fixed vertices are `x,y,z`, with `xy` red and `xz,yz` blue. The eight
moving cycles have red fixed-neighbor masks as follows, with bit weights
`x=1,y=2,z=4`:

| case | incidence columns | variables | Ramsey clauses | normalization clauses | result |
|---|---|---:|---:|---:|---|
| `h=0` | `0,1,2,3,5,5,6,6` | 148 | 248,630 | 0 | UNSAT, DRAT verified |
| `h=1` | `0,1,2,3,4,5,6,7` | 148 | 248,610 | 169 | UNSAT, DRAT verified |

The variables are eight internal `C_5` orientations and 140 cross-cycle
edge-orbit colors. Every one of the 962,598 five-sets supplies the two
Ramsey clauses before exact simplification. For `h=1` only, a global
coordinate multiplier chooses the first internal orientation, and seven
independent cycle shifts minimize their words to an anchor cycle.
The [complete proof](PROOF.md) justifies every restriction and substitution.

There are no degree-counter clauses, hard-branch assumptions, catalog
restrictions, or additional automorphisms in these formulas.

## Reproduce

Requirements: Python 3.11+, a C++17 compiler, Kissat 4.0.4 and `drat-trim`.
The tested interpreter is CPython 3.11.2 and compiler is GCC 12.2.0.
The solver/checker source revisions are:

```text
kissat:    8af8e56f174b778aef3aa45af9f739b2a5f492c2
drat-trim: 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
```

Build those revisions from the primary repositories
[arminbiere/kissat](https://github.com/arminbiere/kissat) and
[marijnheule/drat-trim](https://github.com/marijnheule/drat-trim), using
`./configure` then `make` for Kissat and `make` for drat-trim. Keep the
checkouts and build products outside this research repository. Tested
binary hashes and reference certificate hashes are in [result.json](result.json).

From this directory, with the two built executable paths:

```sh
python3 reproduce.py --work /tmp/r55-no-order5 \
  --kissat /path/to/kissat/build/kissat \
  --drat-trim /path/to/drat-trim/drat-trim
```

The runner regenerates both formulas, independently reconstructs and
compares every clause, rejects two malformed formulas per case, obtains
fresh proofs, and replays them. Its default solver limit is 120 seconds
per case; `--seconds` changes that limit. A timeout or failed replay is
an error, never an exclusion. Successful output ends with:

```text
PASS: both residual order-five incidence patterns are certified UNSAT
```

The reference run's summary is in `EXPECTED_OUTPUT.txt`; detailed compact
timings and hashes are in `REPRODUCTION_RESULT.json`. Fresh solves took
0.36 and 4.73 seconds, and proof replays took 0.62 and 6.48 seconds on the
research host. Proof hashes may
depend on the solver build; the runner records whether they match and
requires an actual successful replay regardless. Formula hashes must match.
Generated formulas, proofs, checker executable, logs, and `reproduction.json`
stay under `--work`.

For reconstruction alone, after generating a case's formula:

```sh
g++ -std=c++17 -O2 -Wall -Wextra -Werror independent_formula.cpp \
  -o /tmp/r55-independent-formula
/tmp/r55-independent-formula 0 0 /tmp/r55-no-order5/h0.cnf
/tmp/r55-independent-formula 1 1 /tmp/r55-no-order5/h1.cnf
```

The middle argument specifies whether the normalization is included. The
checker requires `0` for `h=0`, and `1` for `h=1`.

## Evidence and trust boundary

The Python generator uses modular edge differences and set projection.
The independent C++ checker constructs actual permutation orbits by
union/find and compares the complete clause multiset. Both cases passed
ASan/UBSan. A separate explicit-graph normalization audit covers all 256
internal orientation profiles with seeded cross words and checks all 903
edges. These are same-researcher audits, not an independent peer review or
proof-assistant formalization of this new exclusion.

Both binary DRAT traces were replayed on the research host. The reference
traces are 257,320 and 4,415,625 bytes, and the formulas are about 9.6 MB
each. These generated artifacts are **not committed**. This source package
recreates and checks them; hashes alone do not certify UNSAT. The DRAT
checker implementation and the documented mathematical reduction remain
explicit trust boundaries.

The cycle type `1^3 5^8` itself imposes no hard-branch condition. In
particular this proof covers both the low-deficiency and hard branches
used elsewhere in the team's degree-profile work.

## Prior results completing the order-five theorem

| moving 5-cycles | fixed vertices | durable exclusion |
|---:|---:|---|
| 1 | 38 | [analytic fixed-38 obstruction](../ramsey_r55_order5_f38_analytic_obstruction) |
| 2 | 33 | [degree-strengthened fixed-33 certificate](../ramsey_r55_order5_f33_degree_obstruction) |
| 3,4,5,6 | 28,23,18,13 | [four middle-type certificates](../ramsey_r55_order5_middle_obstruction) |
| 7 | 8 | [independent reproduction of external q4 certificate](../ramsey_r55_order5_f8_external_reproduction) |
| 8 | 3 | this package, using the [two-pattern incidence theorem](../ramsey_r55_order5_f3_incidence) |

The incidence theorem also has an
[independent review](../ramsey_r55_order5_f3_incidence_review3). Its earlier
two-cycle local feasibility checks are compatible with this result: full
extension couples forbidden sets across more cycles, whereas those local
checks treat each pair separately.

During this pass, the teammate also published a
[hard-branch specialization](../ramsey_r55_order5_hard_branch) reducing
that branch to one degree profile and three marked incidence cases.
The present unrestricted exclusion covers those three cases as well as
the low-deficiency branch. It does not use the additional hard-branch
equations, and the earlier necessary-condition theorem remains valid.

The external [wustep/maths q4 source](https://github.com/wustep/maths/tree/main/problems/ramsey-r55/compute/q4)
records the maximal order-five type as unresolved. The present computation
uses the later two-pattern incidence reduction. The searched literature
and refreshed committed graph did not contain this complete order-five
closure; no universal priority claim is made. The cumulative consequences
are recorded in the [automorphism handoff](../ramsey_r55_automorphism_exclusion_handoff).
