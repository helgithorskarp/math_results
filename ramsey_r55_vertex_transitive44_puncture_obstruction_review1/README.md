# Independent review of the h3963 vertex-transitive(44) exclusion

Verdict: **ACCEPT subject to the declared TransGrp catalog-completeness
boundary.** No vertex-transitive graph on 44 vertices is a Ramsey `(5,5)`
graph, and puncturing one vertex cannot produce a good 43-vertex graph. This
is a complete structured-family exclusion, not a good43 construction or a
proof that `R(5,5) >= 44`.

The independent checker imports no reviewed Python module. It reconstructs
the 2,113 catalog actions as 946-bit pair-orbit cells, independently finds the
250 distinct labeled partitions and 199 maximal refinements, validates and
solves all 195 new physical cores, and checks the four regular actions
directly rather than trusting the prior Cayley verdict. The regular check
constructs explicit isomorphisms to four coordinate groups, regenerates the
exact physical Ramsey formulas, validates the pinned physical subcores, and
refutes them with a separately implemented DPLL. [REVIEW.md](REVIEW.md) gives
the proof audit and trust boundary.

From the repository root, using CPython 3.11 or later and a fresh scratch
path:

```sh
python3 -B \
  ramsey_r55_vertex_transitive44_puncture_obstruction_review1/reproduce.py \
  . /scratch/research-team-v2/tmp/reviewer-1/review-h3963
```

Expected status: `REPRODUCED_ACCEPT_REVIEW_H3963`. The reproduction extracts
reviewed commit `b64588fddf2267c4261b2520e40841dc3c1bab89`, replays its full
source verifier and Cayley dependency, then runs the independent checker in
normal and assertion-disabled modes. It uses Git and the Python standard
library, invokes no external solver, and keeps generated evidence outside the
repository.
