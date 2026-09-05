# Eleven moving triangles split three-versus-eight or four-versus-seven

In a Ramsey `(5,5;43)` graph, an order-three automorphism of type
`1^10 3^11` must have either **three moving triangles of one internal
color and eight of the other, or four and seven**. Four of the six
internal-color counts up to complementation are excluded by complete,
independently reconstructed formulas and checked DRAT proofs.

The two displayed splits remain OPEN. Their solver timeouts are neither
exclusions nor feasible graphs. The minimum moving-cycle count remains eleven;
this does not exclude the whole eleven-cycle type, produce a 43-vertex
coloring, or improve the Ramsey lower bound.

The [full proof](PROOF.md) gives the local arithmetic, coverage of all six
counts, centralizer normalizations, primary/auxiliary encoding, and proof
checking boundary. No fixed degree profile, automorphism beyond the given
order-three action, or graph catalog is imposed.

## Complete bounded result

| red triangles after complementation | variables | clauses | status |
|---:|---:|---:|---|
| 0 | 34196 | 613,487 | DRAT verified |
| 1 | 34226 | 614,357 | DRAT verified |
| 2 | 34250 | 615,050 | DRAT verified |
| 3 | 34268 | 615,572 | OPEN (UNKNOWN) |
| 4 | 34280 | 615,920 | OPEN (UNKNOWN) |
| 5 | 34286 | 616,094 | DRAT verified |

All six formulas use 320 nonconstant edge-orbit variables, all 962,598
five-sets in both colors, exact degree/common-neighborhood/deficit counters,
anchor-phase and same-color anchor-weight order, and fixed-signature order.
There are 331 pair orbits in total, including eleven internally constant
triangles. The generator and independent C++ DSU verifier agree on all
3,690,480 canonical clauses across the six formulas.

The sweep used two workers, 180 seconds per solve and 300 seconds per
proof replay. It completed in 616.752262 seconds, with largest child peak
RSS 263,480 KiB. Four solver exits were 20 and their full DRAT replays
returned zero with `s VERIFIED`. Counts three and four returned explicit
UNKNOWN at their limits. Runtime and time-limited outcomes depend on the
host; a later timeout must never be counted as an exclusion.

The four completed proof traces total 223,356,924 bytes. They have respectively
59, 420, 932 and 1,558 RAT core lemmas for r=0,1,2,5; general DRAT is
required. Full CNF/proof hashes, solver/checker binary hashes and frozen source
hashes are in [result.json](result.json). Large CNFs, proof traces and logs
are omitted from Git, with reproducible source and compact reports retained.
Hashes and reports alone are not standalone refutations.

## Local reduction and active upper-degree bound

For a moving triangle in its internal color, let a be the number of fixed
neighbors, w_j its ten cross-block weights, m the number of complete
blocks, and `D=sum(2-w_j+3*[w_j=3])`. Its common own-color neighborhood
has size at most four. Its own-color degree is `22+a+3m-D`, between
18 and 24 by the published theorem `R(4,5)=25`. Thus

```
max(0,D-4-3m) <= a <= min(10,4-3m,D+2-3m).
```

A fixed count exists exactly when D<=8 and m<=1. Exact ordered enumeration
and independent multinomial counting agree on 80,726 local arithmetic
profiles. These are necessary local data, not graph realizations. The
budget alone admits 23,565 further weight vectors with too many complete
blocks. Omitting the upper-degree term admits twelve additional profiles
with degree 25 or 26. Every production formula enforces that upper bound.

The older ten-cycle local cap automatically gave the degree upper bound;
the eleven-cycle cap does not. The new moving upper counter therefore bounds
the forty outside-triangle own-color incidences by **22**, accounting for
the two internal neighbors. Their negations have bound 24 to impose degree
at least 18. Deficit counters replace a potential 1,847,560 explicit
nine-token clauses without changing the allowable primary assignments.

## Reproduction

Requirements: CPython 3.11.2 (standard library only), GCC 12.2.0, C++17,
Kissat 4.0.4 and drat-trim. Tested tool source commits:

- Kissat: `8af8e56f174b778aef3aa45af9f739b2a5f492c2`.
- drat-trim: `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.

From this directory, with a fresh work directory outside Git:

```sh
python3 run.py --work /scratch/r55-k11/full \
  --kissat /path/to/kissat/build/kissat --drat-trim /path/to/drat-trim \
  --workers 2 --solve-seconds 180 --replay-seconds 300
python3 verify.py --source-work /scratch/r55-k11/full \
  --work /scratch/r55-k11/verification --drat-trim /path/to/drat-trim
python3 -O controls.py --report /scratch/r55-k11/controls_optimized.json
cmp controls_result.json /scratch/r55-k11/controls_optimized.json
sha256sum -c SHA256SUMS
```

Expected: `excluded_counts=[0,1,2,5]`, `open_counts=[3,4]`; six full formula
reconstructions, four successful full-proof replays and four rejected formula
mutations. Time and memory fields need not reproduce byte for byte. Formula
hashes and control reports are deterministic. A different valid proof trace
is accepted only by replay against the exact audited formula.

`run.py` writes atomic per-case records and an aggregate result after each
completion. A `STOP` file prevents another case from starting, while active
bounded cases finish. `--resume` requires an unchanged contract, reconstructs
all formulas, replays saved exclusions, and retains OPEN statuses without
extending their search time. Partial timeout traces are not solver restart
states. SAT results are decoded to literal edge lists and exhaustively checked
for both kinds of five-set before any target claim.

## Validation and trust

`verify.py` freshly regenerates all six complete formulas, checks every clause
with the independent C++ program and replays every claimed full proof against
the fresh CNF. Its compact report is [verification_result.json](verification_result.json).
The fresh pass completed in 426.266287 seconds. Four deliberate mutations are rejected: missing clause, wrong polarity,
unsupported empty axiom, and wrong moving upper-counter overflow unit.
No extracted-core package is used in this milestone.

The controls exhaust all 1,048,576 weight vectors with eleven fixed counts,
all 2,048 internal-color profiles for literal normalization checks, 1,734
signed/repeated counter assignments, and 96 seven-vertex orbit assignments.
Normal and optimized Python reports match. Complete formulas r=0 and r=5
pass address/undefined-behavior sanitizers, with flags and outputs in
[sanitizers_result.json](sanitizers_result.json). Their independently generated
pilot and frozen-run CNFs also match byte for byte. The frozen production
sources remained unchanged throughout the run.

The only external graph-theoretic theorem needed for the direct exclusions is
[McKay--Radziszowski, R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
The current minimum-eleven conclusion additionally uses the independently
reviewed ten-cycle chain. The C3-square exclusions and the teammate's
non-symmetric filters are not assumptions of this new result.
Remaining trust lies in the unformalized reduction and normalization proof,
source/runtime/compiler/hardware, SHA256 and the external drat-trim checker.
The generator's modular-difference construction and the checker's literal
pair-DSU reconstruction provide internal independence; this is not an external
peer-review verdict or a proof-assistant formalization.

## Completed boundary and handoff

Research-host work is preserved under `/scratch/team-r55-1-order3-k11`:
`full/` contains the six formulas and original traces, `verification/` the
fresh reconstruction and proof replay, and `pilot/` the two early full
formula controls. No twelve-cycle or anchor-subdivision search is included.
The next structured step should address the two remaining eleven-cycle
splits after fresh coordination, rather than repeat the six-count sweep.
The teammate's non-symmetric M=216 signature-obstruction work stays separate.
