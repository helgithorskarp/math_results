# Three possible minority cores at eleven moving cycles

For a hypothetical Ramsey `(5,5;43)` graph with an order-three automorphism
and **three internally red moving triangles, eight internally blue moving
triangles and ten fixed vertices**, the nine minority vertices must induce
one of three explicit cores. The complete fourteen-class cover has eleven
excluded extensions with replayed full DRAT proofs. Classes 8,11,13 remain
**open**, with UNKNOWN outcomes at 60 seconds.

| class | red words on 01,02,12 | red weight multiset | distinguished phase sum |
|---:|---|---|---|
| 8 | 100,100,100 | 1,1,1 | zero |
| 11 | 100,110,110 | 1,2,2 | zero |
| 13 | 110,110,101 | 2,2,2 | nonzero |

Thus no minority block is empty or complete, and weights 1,1,2 cannot occur.
The full nine-vertex domain has 343 labeled cores; the three remaining
normalizer classes contain 54 labeled cores. A fixed vertex may be red to
all three minority triangles only in class 8. These are necessary structural
conditions, **not 43-vertex constructions or a lower-bound improvement**.
The four-versus-seven eleven-cycle split and moving counts 12..14 remain
open. The minimum moving count remains eleven.

[PROOF.md](PROOF.md) gives the algebraic invariant, complete normalization,
formula bridge and trust boundaries. [cover.json](cover.json) gives all
343 orbit members and fourteen representatives. The parent
[eleven-cycle formula](../ramsey_r55_order3_eleven_cycle_obstruction)
has now received an [accepted independent review](../ramsey_r55_order3_eleven_cycle_obstruction_review1).
The present fourteen-class result has internal checks and awaits independent
review.

## Exact computation

The symmetry group permutes the three red cycles, rotates them independently,
and may simultaneously invert **all eleven** moving cycles. Its 324 maps give
14 classes, determined by the unordered red weights and, when all are
nonzero, the zero/nonzero value of an oriented phase sum modulo three.
An independent literal adjacency audit checks all 512 nine-bit inputs and
all 111132 transports of valid cores. The core normalization is compatible
with the parent's anchor words, blue-cycle weight sorting and final fixed
signature ordering.

The parent formula has 34268 variables and 615572 clauses. Each cube appends
exactly nine primary units, giving 615581 clauses. The entire parent is
freshly generated and independently reconstructed from actual pair orbits;
every cube prefix and unit tail is checked. No degree profile, catalog,
extra automorphism, or chosen fixed graph is imposed. Both degree bounds
and the common-neighborhood cap are retained.

| class | representative | labeled cores | phase invariant | outcome | solve seconds |
|---:|---|---:|---|---|---:|
| 0 | 000000000 | 1 | none | excluded | 1.068 |
| 1 | 000000001 | 9 | none | excluded | 10.448 |
| 2 | 000000011 | 9 | none | excluded | 7.539 |
| 3 | 000100001 | 27 | none | excluded | 19.126 |
| 4 | 000100011 | 54 | none | excluded | 16.467 |
| 5 | 000110011 | 27 | none | excluded | 58.654 |
| 6 | 100100001 | 18 | nonzero | excluded | 45.456 |
| 7 | 100100011 | 27 | zero | excluded | 31.821 |
| 8 | 100100100 | 9 | zero | open | 60.062 |
| 9 | 100100101 | 54 | nonzero | excluded | 45.965 |
| 10 | 100110011 | 54 | nonzero | excluded | 58.254 |
| 11 | 100110110 | 27 | zero | open | 60.059 |
| 12 | 110110011 | 9 | zero | excluded | 53.533 |
| 13 | 110110101 | 18 | nonzero | open | 60.109 |

The complete run took 508.260191 seconds with two workers, 60-second solver
limits and 300-second replay limits. Largest child peak RSS was 259504 KiB.
Successful full traces total 399325866 bytes. Ten of the eleven proofs use
RAT steps; only class 0 has zero RAT core lemmas. Full trace replay, rather
than a solver verdict or hash comparison, establishes each exclusion.
Fresh regeneration, complete cube audits, eleven full replays and four
malformed-cube rejections took 238.133569 seconds. The report is
[verification_result.json](verification_result.json).

## Reproduction

Python 3.11.2 standard library and GCC 12.2.0 were used. The inherited C++
checker builds with `-std=c++17 -O2 -Wall -Wextra -Wpedantic -Werror`.
Kissat 4.0.4 source was `8af8e56f174b778aef3aa45af9f739b2a5f492c2`;
drat-trim source was `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
Tool and source hashes are pinned in `result.json`. The inherited parent
source is commit `15a3657bb030419fc7c5738cbb7eb5d8055c4b08`.

From this directory, choosing fresh work paths outside the repository:

```sh
python3 controls.py --work /scratch/r55-k11-core/controls
python3 run.py --work /scratch/r55-k11-core/full \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim \
  --workers 2 --solve-seconds 60 --replay-seconds 300
python3 verify.py --source-work /scratch/r55-k11-core/full \
  --work /scratch/r55-k11-core/verification \
  --drat-trim /path/to/drat-trim --replay-seconds 300
sha256sum -c SHA256SUMS
```

Expected: fourteen complete cube reconstructions, eleven proof replays,
`excluded=[0,1,2,3,4,5,6,7,9,10,12]`, `open=[8,11,13]`, four rejected cube
mutations, four rejected cover mutations, and matching normal/optimized
cover and literal-audit reports. Complete manifests contain all formula and
trace hashes. Different machines may time out on different cases; a changed
trace is acceptable only with successful replay of the exact audited formula.
An UNKNOWN trace is neither a refutation nor a resumable solver state.

`run.py` writes atomic per-case checkpoints. A `STOP` file in the work directory
prevents further cases starting, while active cases finish. `--resume` requires
an unchanged computation contract, reconstructs the formulae, retains OPEN
cases at their original bounds and replays saved exclusions. Verification
always requires a new work directory. This milestone does not start another
core refinement, anchor sweep, or moving-cycle stratum.

## Evidence boundaries

The direct external theorem is
[McKay and Radziszowski's R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
The normalizer and counter extension arguments are ordinary mathematical
proofs, without proof-assistant formalization. Exact source, runtime,
compiler/hardware, SHA-256 and drat-trim remain trust boundaries. Internal
reconstruction and repeated replay do not constitute independent peer review.

Only substantive source and compact reports are committed. Full CNFs,
399325866 successful proof bytes, partial UNKNOWN traces and logs remain
outside Git; the commands regenerate them. Reports and hashes alone are not
standalone certificates. Existing traces can be replayed without invoking a
SAT solver, but regenerating omitted traces requires one.
