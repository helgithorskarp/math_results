# At least ten moving 3-cycles in a Ramsey (5,5;43) graph

Every order-three automorphism of a hypothetical 43-vertex graph avoiding
a clique and an independent set of order five has **at least ten moving
3-cycles**, and therefore at most 13 fixed vertices.

The new excluded cycle type is `1^16 3^9`. The earlier packages exclude
one through eight moving cycles. This is a structural restriction, not
a 43-vertex construction or an improved Ramsey lower bound. See the
[complete proof](PROOF.md).

## What changes at nine cycles

The local deficit budget rises from two to four. For a moving triangle,
let `w_j` count neighbors in another triangle in its own color and
`m` count complete blocks. The common-neighborhood and degree bounds imply

```text
a + 3m <= 4,
D = sum_j (2-w_j+3*[w_j=3]) <= 4.
```

The common-neighborhood condition remains essential. There are 28 weight
vectors that meet the deficit budget but have two complete blocks and
cannot have any feasible fixed count. Retaining both conditions leaves
987 local arithmetic profiles among 1,114,112 possibilities. These are
local necessary conditions, not graph realizations.

Color reversal and cycle permutation leave five internal-color cases:
zero through four red moving triangles. Eight independent anchor phases
and a lexicographic ordering of the sixteen fixed signatures give proved
normalizations. The full formulas retain all 962,598 five-sets and use
no graph catalog, hard-deficiency branch or extra group assumption.

The [27-vertex partial graph](moving27.edges) satisfies the moving-vertex
conditions with four red and five blue triangles. Its independent literal
audit checks all 80,730 five-sets. The fixed vertices are needed to close
the full case; this partial graph is not a target witness.

## Exact evidence

| red moving triangles | variables | complete clauses | result |
|---:|---:|---:|:---|
| 0 | 8,490 | 609,409 | DRAT verified |
| 1 | 8,514 | 612,097 | DRAT verified |
| 2 | 8,532 | 614,113 | DRAT verified |
| 3 | 8,544 | 615,457 | DRAT verified |
| 4 | 8,550 | 616,129 | DRAT verified |

The Python generator uses modular differences. The separate C++ checker
constructs the actual permutation orbits of all 903 vertex pairs and
rebuilds **every primary and auxiliary clause**, comparing complete
canonical DIMACS streams. All five cases pass this reconstruction.

A fresh reproduction regenerated all five formulas and proofs, matched
every reference proof hash, and independently replayed each trace with
`drat-trim`. Fresh solver times were 3.4–9.8 seconds per case and replay
times 4.5–9.7 seconds, in addition to formula generation and auditing.
Optimized and ASan/UBSan checks agree on representative uniform and mixed
cases; changed-literal and missing-clause mutations are rejected.

## Reproduce

Requirements: Python 3.11+, C++17, a POSIX shell, `sha256sum`, Kissat 4.0.4,
and drat-trim. Tested with CPython 3.11.2 and GCC 12.2.0 on Linux.
No third-party Python package or Ramsey dataset is needed.

```sh
sh verify.sh --work /tmp/r55-order3-k9 \
  --kissat /path/to/kissat/build/kissat \
  --drat-trim /path/to/drat-trim/drat-trim
```

The complete command regenerates the formulas, reconstructs their clauses,
produces proof traces, and replays every trace. It ends with:

```text
PASS: order-three type 1^16 3^9 is excluded; minimum moving 3-cycles is 10
```

Keep the work directory outside the repository. The five formulas total
124,396,054 bytes and the reference binary DRAT traces total 81,986,115 bytes.
These large generated files and logs are **not committed**. The source,
fixture, counts, hashes and exact recipe are committed. Hashes alone are
not certificates; verification requires regeneration and successful replay.

The solver limit is 60 seconds per case and the replay limit is 120 seconds.
An incomplete or timed-out case exits with failure and is never counted
as an exclusion. Different compiler builds may produce different valid
traces: the script records whether each matches the reference, and always
requires proof verification against the identical audited formula.

To inspect a retained case directly:

```sh
/tmp/r55-order3-k9/check_formula 4 /tmp/r55-order3-k9/full_r4.cnf
/path/to/drat-trim/drat-trim /tmp/r55-order3-k9/full_r4.cnf \
  /tmp/r55-order3-k9/full_r4.drat
```

These are general DRAT traces, potentially with RAT steps and deletions.
Do not replay them as though they were addition-only RUP proofs.

## Pinned tool sources

The tested sources are [Kissat](https://github.com/arminbiere/kissat),
commit `8af8e56f174b778aef3aa45af9f739b2a5f492c2`, and
[drat-trim](https://github.com/marijnheule/drat-trim), commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Binary and artifact hashes
are recorded in `result.json`. A possible local setup is:

```sh
git clone https://github.com/arminbiere/kissat.git /tmp/r55-kissat
git -C /tmp/r55-kissat checkout 8af8e56f174b778aef3aa45af9f739b2a5f492c2
(cd /tmp/r55-kissat && ./configure && make)
git clone https://github.com/marijnheule/drat-trim.git /tmp/r55-drat-trim
git -C /tmp/r55-drat-trim checkout 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
make -C /tmp/r55-drat-trim drat-trim
```

The first solver is used only to discover a trace. The independent proof
checker, not the solver's verdict, establishes unsatisfiability.

## Scope and provenance

The graph-theoretic input is
[McKay–Radziszowski, R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
The minimum-ten corollary additionally imports the
[eight-cycle theorem](../ramsey_r55_order3_eight_cycle_obstruction), whose
complete dependency chain now has an
[accepted independent review](../ramsey_r55_order3_eight_cycle_review1).
This new nine-cycle exclusion is independent of the order-five theorem
and of the teammate's asymmetric structural work.

The reduction, counter extension and normalizations remain unformalized
mathematics. Exact execution trusts the small checking programs, runtime,
compiler, hardware and the external DRAT checker. The new internal audits
are not independent peer review. The proof does not depend on a catalog
or an unreplayed UNSAT claim.

The refreshed Discovery Net graph and searched primary sources, including
the external [q7 report](https://github.com/wustep/maths/tree/main/problems/ramsey-r55/compute/q7),
did not contain this nine-cycle closure. No universal priority claim is made.
The [cumulative symmetry handoff](../ramsey_r55_automorphism_exclusion_handoff)
records the current restrictions. Ten through fourteen moving cycles remain
outside this package; no next stratum is started here.
