# Bounded full-extension sweep of the 79 residual minority cores

This package tests every remaining four-versus-seven core with the
complete 43-vertex Ramsey formula, using ten seconds of solver time
per core. Exact excluded and open lists are recorded in `result.json`;
fresh formula reconstruction and second proof replays are recorded
in `verification.json`. A bounded UNKNOWN outcome leaves its case open.

The fixed sweep excludes **34 additional core classes** (21,942 labeled
cores) and leaves **45 classes** (29,754 labeled cores) open. Together
with the preceding 118-class theorem, **152 of 197 classes** are now
excluded, covering 85,789 of the 115,543 locally valid labeled cores.
These counts describe marked-action core orbits, not counts of full
43-vertex graphs. No SAT candidate was obtained.

The first run completed all 79 cases in 545.101 seconds with two workers.
Fresh reconstruction and all 34 second proof replays completed successfully
in 211.684 seconds. Its 34 successful DRAT traces total 583,276,093 bytes; the largest is
21,622,803 bytes. Thirty-three traces use RAT core lemmas, so a RUP-only
check is insufficient. Peak reported child RSS was 261,504 KiB. These
measurements describe this run, not portable resource guarantees.

The preceding [blue-K4 exclusion](../ramsey_r55_order3_eleven_blue_k4_exclusion)
and the underlying 197-class cover now have an
[accepted independent review](../ramsey_r55_order3_eleven_blue_k4_exclusion_review1).
That review includes the complete marked-action cover and its
full-parent normalization. The new sweep tests exactly the resulting
79 residual entries. It introduces no fixed-signature or degree-profile
restriction beyond the complete parent and the selected core bits.

## What is checked

Each formula retains the entire reviewed r=4 parent: all 43 vertices,
all Ramsey clauses, both color-degree bounds, local constraints,
counters and normalization. Eighteen primary units specify the core.
Every final instance has **34,280 variables and 615,938 clauses**.
[PROOF.md](PROOF.md) gives the coverage argument and exact unit meanings.

The full parent is regenerated and independently reconstructed by the
inherited C++ checker. A separate cube auditor reconstructs primary
edge meanings from the full 43-vertex action and checks the complete
parent prefix, every appended unit, and EOF for each case.

Kissat UNSAT results require a successful full DRAT replay. A fresh
verification pass regenerates all 79 formulas and replays every
successful proof again. General RAT steps are accepted by the full
checker; a RUP-only substitute would be insufficient when RAT steps
occur. Any SAT result must decode to a 43-vertex edge list and pass
literal graph verification before being called a target.

Five malformed full formulas are rejected, and normal/optimized
Python cube-control reports agree. The parent also reruns its inherited
arithmetic, counter and normalization controls. No 118-core blue-K4
case or three-versus-eight case is included in this sweep. In particular,
four-versus-seven catalog indices 11 and 13 are distinct from the open
three-versus-eight cores carrying the same indices in a different catalog.

## Reproduction

CPython 3.11.2, GCC 12.2.0, Kissat 4.0.4 and drat-trim. The inherited
C++ auditor builds with
`-std=c++17 -O2 -Wall -Wextra -Wpedantic -Werror`.
Kissat source commit: `8af8e56f174b778aef3aa45af9f739b2a5f492c2`.
DRAT checker source commit: `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
Exact source and executable hashes are in the run contract in `result.json`.

From this directory, choose work directories outside Git:

```sh
sha256sum -c SHA256SUMS
python3 -B sweep.py --work /scratch/new-r55-r4-residual/full \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim \
  --solve-seconds 10 --replay-seconds 300
python3 -B verify.py --source-work /scratch/new-r55-r4-residual/full \
  --work /scratch/new-r55-r4-residual/verification \
  --drat-trim /path/to/drat-trim --replay-seconds 300
python3 -B -O controls.py --parent /scratch/new-r55-r4-residual/full/parent.cnf \
  --work /scratch/new-r55-r4-residual/controls-O
cmp /scratch/new-r55-r4-residual/full/cube_controls/controls.json \
  /scratch/new-r55-r4-residual/controls-O/controls.json
```

Formula hashes are deterministic. Timing fields and timeout outcomes
can vary between machines. A regenerated proof must pass the exact
checker against its audited formula; matching an outcome count or a
hash alone is not a refutation. The default run uses two workers.

The runner saves each completed case atomically and fixes all source,
input, solver/checker binary hashes and resource limits in its contract.
A `STOP` file in the full work directory prevents new cases while
active cases finish. `--resume` requires the identical contract and
retains completed UNKNOWN cases at their original limit. It does not
silently lengthen their searches. Incomplete/error runs are explicitly
distinguished from completed bounded sweeps.

Full CNFs, proof traces, partial UNKNOWN traces, binaries and operational
logs remain outside Git. Published source regenerates them. Compact
outcome/verification manifests identify the exact checked evidence;
their hashes alone do not replace the omitted proof traces. Partial
UNKNOWN traces are neither certificates nor resumable solver states.

## Dependencies and shared checkpoint

The accepted cover/blue-K4 review has source commit
`820b71722dea416cdbf85a89bcb5b53adb22405c` and Discovery Net reference
`bafkreic2gyirwl4zcop47nmswxtgldwpq67aoxwl7iranbiyneehcywcyi`
(height 2893). The relevant prepublication graph refresh through height
2898 found no contrary feedback or duplicate sweep.

The teammate's separate
[visible-obstruction cover](../ramsey_r55_visible_obstruction_cover),
source commit `2b81cba46c279870292fe579e80cf8515b06bcc8`, proves an exact
34-visible-edit optimum for its retained cover relaxation and a total-edit
lower bound of 52. Its witness creates new K5s. That non-symmetric repair
result is neither a proof input nor a search domain in this package.
The two lanes remain separate; no target or full hard-profile closure is
inferred from either milestone.

## Scope and trust

The cover, blue-K4 exclusion and parent reduction are independently
reviewed. The new full-case refutations have internal replay and fresh
reconstruction; they await independent review. The external R(4,5)=25
theorem and the parent's unformalized normalization/counter bridge are
imported. Other trust boundaries are the exact source code, Python,
C++ compiler/runtime/hardware, SHA256 and the external DRAT checker.
There is no proof-assistant formalization or historical-priority claim.

No target graph or Ramsey lower-bound improvement is claimed. The
three-versus-eight branch is unchanged. This milestone ends after
the fixed 79-case sweep and verification, before a larger timeout,
additional subdivision, or a different proof/construction phase.
