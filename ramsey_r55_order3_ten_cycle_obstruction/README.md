# Ten moving triangles must split four versus six

In a hypothetical Ramsey `(5,5;43)` graph, an order-three automorphism
with ten moving 3-cycles must have **four moving triangles of one internal
color and six of the other**. Five of the six internal-color counts up
to complementation are excluded by audited formulas and checked DRAT
proofs. See the [complete argument](PROOF.md).

The four-versus-six case remains open. The minimum number of moving
3-cycles stays at ten, and the fixed-point bound stays at thirteen.
This is neither a complete exclusion of `1^13 3^10` nor a 43-vertex
construction or improved Ramsey lower bound.

## What the computation establishes

| red moving triangles | variables | complete clauses | status |
|---:|---:|---:|:---|
| 0 | 28,878 | 922,248 | DRAT verified |
| 1 | 28,905 | 924,030 | DRAT verified |
| 2 | 28,926 | 925,416 | DRAT verified |
| 3 | 28,941 | 926,406 | DRAT verified |
| 4 | 28,950 | 927,000 | unresolved |
| 5 | 28,953 | 927,198 | DRAT verified |

All six formulas retain every one of the 962,598 five-sets. The Python
generator uses modular edge differences; a separate C++ checker builds
the actual permutation orbits of all 903 pairs and reconstructs **every
primary and auxiliary clause**. It compares the complete canonical DIMACS
stream. The five exclusion claims additionally require verified traces.

The moving-triangle deficit bound rises to six. Its common-neighborhood
cap must still be retained: there are 10,679 feasible local arithmetic
profiles among 3,670,016 possibilities, while the deficit bound alone
admits 1,380 impossible cross-weight vectors. These are necessary local
conditions, not graph realizations.

The strengthened encoding explicitly imposes the established degree
interval 18 through 24 at the thirteen fixed vertices. Each fixed vertex
has twelve fixed-edge variables and ten moving-incidence variables of
weight three. Independent reconstruction uses all 42 actual incident
edges, checking the multiplicities directly. No fixed degree profile,
graph catalog or hard-deficiency assumption is used.

The [30-vertex fixture](moving30.edges), with 219 red edges and five
triangles of each internal color, passes a literal check of all 142,506
five-sets and all moving-triangle conditions. It is a positive control
for the moving relaxation, not a target witness.

## Reproduce

Requirements: Python 3.11+, C++17, POSIX shell, `sha256sum`, Kissat 4.0.4,
and drat-trim. Tested with CPython 3.11.2 and GCC 12.2.0 on Linux.

```sh
sh verify.sh --work /tmp/r55-order3-k10 \
  --kissat /path/to/kissat/build/kissat \
  --drat-trim /path/to/drat-trim/drat-trim
```

The command audits the arithmetic, normalizations, counters and fixtures;
regenerates and completely reconstructs all six formulas; and produces
and verifies the five claimed proof traces. For `r=4` it records that the
formula was audited and that no exclusion was established. It ends with:

```text
PASS: ten-cycle red counts 0,1,2,3,5 excluded; r=4 remains open
```

The solver limit is 180 seconds per certified case and the proof replay
limit is 240 seconds. A timeout, incomplete proof or failed reconstruction
exits with failure and is never counted as an exclusion. `complete=true`
in the generated report means the stated checks completed;
`all_cases_excluded` remains false.

Keep generated state outside Git. The roughly 36 MB formulas, general
DRAT proofs and logs are **not committed**. Source, a compact fixture,
anchor profiles, exact counts, byte sizes and hashes are committed.
`result.json` records each complete formula and each certified reference
trace. Hashes alone are not certificates: verification requires generating
and successfully replaying the traces. Different compiler builds may
produce different proof hashes; the script records this and still requires
successful replay against the identical audited formula.

These proofs use general DRAT, with possible RAT steps and deletions.
Do not treat them as addition-only RUP proofs. The solver produces evidence;
the external checker verifies unsatisfiability. No third-party Python
package or external Ramsey dataset is required.

## Pinned tools

The tested sources are [Kissat](https://github.com/arminbiere/kissat),
commit `8af8e56f174b778aef3aa45af9f739b2a5f492c2`, and
[drat-trim](https://github.com/marijnheule/drat-trim), commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Binary hashes are in
`result.json`. A possible local setup is:

```sh
git clone https://github.com/arminbiere/kissat.git /tmp/r55-kissat
git -C /tmp/r55-kissat checkout 8af8e56f174b778aef3aa45af9f739b2a5f492c2
(cd /tmp/r55-kissat && ./configure && make)
git clone https://github.com/marijnheule/drat-trim.git /tmp/r55-drat-trim
git -C /tmp/r55-drat-trim checkout 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
make -C /tmp/r55-drat-trim drat-trim
```

## A bounded next frontier

An additional valid normalization orders the nonanchor triangles of each
internal color by their phase-normalized anchor-word weight. In the
remaining four-versus-six case, the red anchor then has an increasing
triple of weights in `{0,1,2}` toward red triangles and an increasing
sextuple in `{0,1,2,3}` toward blue triangles. At most one weight is three,
and the total deficit is at most six.

Exactly **98** vectors meet these necessary conditions. The compact list
is [anchor_r4.json](anchor_r4.json); two enumerations compare its entries
exactly in `audit.py`. These are potential anchor profiles, not graph
realizations or excluded cases. The six production solver formulas do
not impose this additional order. A separate bounded pilot with it also
timed out for `r=4`; no exhaustion of the 98 profiles has been started.

## Scope and provenance

The direct theorem imports
[McKay--Radziszowski, R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
The inherited minimum-ten conclusion uses the
[previous nine-cycle exclusion](../ramsey_r55_order3_nine_cycle_obstruction),
whose dependency chain has an
[accepted independent review](../ramsey_r55_order3_nine_cycle_review1).
This new result is independent of the order-five exclusion and the
teammate's asymmetric structural work.

The reduction, counter argument and symmetry normalizations are ordinary
unformalized mathematics. Exact execution trusts the checking programs,
runtime, compiler, hardware and external DRAT checker. Separate internal
implementations and sanitizer checks do not constitute independent peer
review of the new result. The searched graph and primary-source reports,
including the external [q7 report](https://github.com/wustep/maths/tree/main/problems/ramsey-r55/compute/q7),
did not contain this restriction; no universal priority claim is made.
