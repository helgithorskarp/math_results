# Both empty-signature branches close four further minority cores

All eight complete 43-vertex split formulas are refuted, excluding the
four-versus-seven core classes **131,139,162,173 entirely**. These are the
four survivors of the [empty-signature propagation](../ramsey_r55_order3_eleven_empty_signature)
test. Each already requires at least one empty fixed signature; this
package covers exactly one versus at least two. Both branches of each
core have full DRAT proofs and fresh reconstruction with second replay.

The four exclusions cover 2,268 labeled locally valid cores, leaving
**34 classes and 24,057 labels**. Cumulatively, 163 of the original 197
classes and 91,486 of 115,543 labels are excluded. These are minority-core
orbit counts, not counts of full graphs. The exact residual list and the
distinction between subcase and whole-core exclusions are recorded in
[boundary.json](boundary.json).

The new bridge and refutations await independent review, as does their
inherited empty-signature theorem. No 43-vertex target graph, Ramsey
lower-bound improvement or full eleven-cycle exclusion is claimed. The
other 34 four-versus-seven classes and both three-versus-eight cores were
not searched in this pass. The global minimum moving count stays eleven.

## Complete split and evidence

[PROOF.md](PROOF.md) proves the exact reduction. The parent's fixed
vertices have lexicographically sorted full eleven-bit red attachment
rows, with four minority bits first. The first fixed row's minority
prefix is already zero. Exactly one empty signature is equivalent to a
nonzero second prefix; at least two is equivalent to a zero second prefix.

The one-empty branch appends the clause `222 223 224 225 0`. The other
branch appends the four units `-222,-223,-224,-225`. These are disjoint
and exhaustive, with no further normalization or signature-multiset
assumption. Every final formula retains all 43 vertices and the ENTIRE
inherited parent, degree bounds in both colors, Ramsey constraints,
counters, normalization, eighteen core units and four first-prefix units.

| branch | variables | clauses | cases | outcome |
|---|---:|---:|---:|---|
| exactly one empty signature | 34,280 | 615,943 | 4 | four checked refutations |
| at least two empty signatures | 34,280 | 615,946 | 4 | four checked refutations |

The complete parent is independently reconstructed by the inherited C++
auditor. Each of the four bases must match its preceding published hash.
The new auditor derives all 320 primary variables from literal pair orbits
on 43 vertices, checks every parent byte and all 22 base units, then every
base byte, each branch clause and EOF. It checks the disjoint split on all
sixteen second prefixes and prefix ordering on all 2,048 full rows.

Seven malformed complete formulas are rejected. They include the wrong
fixed row, missing disjunction literal, reversed polarity, inserted empty
clause, corrupted inherited prefix, missing multiple-empty unit and wrong
multiple-unit polarity. Normal and optimized Python controls agree.
Inherited parent arithmetic/counter/normalization controls and the preceding
lemma's exact core-application checker pass during both preparations.

Each case used `Kissat --time=60`, with two workers and a 300-second full
DRAT replay limit. The complete run took 143.564207 seconds. All eight
proofs contain RAT core lemmas; full DRAT checking is required. Their
total size is 166,419,247 bytes, maximum 24,556,297 bytes. The largest
reported child RSS was 310,392 KiB. A fresh pass rebuilds the complete
parent, four bases and all eight final formulas, checks their hashes and
primary meanings, and replays every proof a second time. This fresh verification passed
in 105.262065 seconds.

[result.json](result.json) records every formula/trace hash, solver and
checker result, resource limit and source contract.
[verification.json](verification.json) records the fresh verification.
There is no UNKNOWN or SAT result in this eight-case sweep. All previous
open cases outside its domain remain open.

## Reproduction

CPython 3.11.2, GCC 12.2.0, Kissat 4.0.4 and drat-trim. The C++ audit uses
`-std=c++17 -O2 -Wall -Wextra -Wpedantic -Werror`.
Kissat source commit `8af8e56f174b778aef3aa45af9f739b2a5f492c2`;
DRAT checker source commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
Exact executable and source hashes are in the run contract.

From this directory, choose fresh work directories outside Git:

```sh
sha256sum -c SHA256SUMS
python3 -B run.py --work /scratch/new-r55-r4-split/full \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim \
  --solve-seconds 60 --replay-seconds 300
python3 -B verify.py --source-work /scratch/new-r55-r4-split/full \
  --work /scratch/new-r55-r4-split/verification \
  --drat-trim /path/to/drat-trim --replay-seconds 300
python3 -B summarize.py --source /scratch/new-r55-r4-split/full \
  --verification /scratch/new-r55-r4-split/verification \
  --output /scratch/new-r55-r4-split/boundary.json
cmp boundary.json /scratch/new-r55-r4-split/boundary.json
python3 -B -O controls.py --base /scratch/new-r55-r4-split/full/base131.cnf \
  --work /scratch/new-r55-r4-split/controls-O
cmp /scratch/new-r55-r4-split/full/controls.json \
  /scratch/new-r55-r4-split/controls-O/controls.json
```

The boundary summary also reproduces byte for byte under optimized Python.
Formula hashes are deterministic; timing and bounded solver outcomes can
vary by host. Every regenerated refutation must satisfy the complete-formula
certificate obligation. A timing, count or stored hash alone proves no
UNSAT claim. The previous unsplit bases used a twenty-second bound, so this
run is not a controlled speed comparison isolating the split's effect.

Each completed case is saved atomically. A STOP file prevents additional
cases while active cases finish; `--resume` requires the same contract,
verifies saved evidence and preserves completed UNKNOWN results at their
original limit. Large formulas, proof traces, logs, binaries and operational
state stay outside Git. Public source regenerates them. Hashes identify
the local checked traces but do not replace the omitted proofs. Partial
UNKNOWN traces, if a rerun creates any, are not certificates or resumable
solver states. A SAT outcome must decode to a compact edge list and pass
literal 43-vertex verification before being called a target.

## Structural boundary and trust

The four closed cores were the last surviving applications of the
preceding condition: a blue triangle exists in every complementary
three-triangle subcore. Thus **any remaining four-versus-seven candidate
must have at least one complementary three-triangle subcore with no blue
triangle**. The preceding classification records all four tests for all
45 earlier residual cores, and its independent algorithm is replayed here.
This is a necessary condition for a full candidate, not a construction or
a classification of complete extensions of those nine vertices.

The complete parent and 197-class marked-action cover/full normalization
are independently accepted. The previous 118-core hand exclusion is also
accepted. The preceding 34- and seven-core computational exclusions, the
empty-signature hand theorem, and the present split bridge and eight
refutations still await independent review. The cumulative count imports
those dependencies. Other trust includes R(4,5)=25, unformalized reduction
and counter reasoning, exact Python/C++ semantics, compiler/runtime/hardware,
SHA256 and full DRAT checking. Internal reconstruction is not independent
peer review or proof-assistant formalization; no priority claim is made.

The initial graph scan through height 2934 and one refresh through 2938
found no new review or objection on the inherited signature theorem and
no duplicate split. The refresh added the teammate's
[two-stratum completion interface](../ramsey_r55_two_stratum_kernel), source
`5367ce6ad2d32942da123b6c4f2c065742d15f60`, graph
`bafkreidjm5bizbpa2reqlkvmp6aq2lus5mddc7abu2hto6rzurdvk7el3a` at height 2937.
It adds two necessary one-color tests beyond the root neighborhoods and
checks a complete residual formula with bipartite degree margins. Its
retained 353-K5 seed fails the visible tests; no target or valid 43-vertex
visible skeleton is supplied. That non-symmetric interface is not a proof
input or search domain here. Its earlier 39-visible-edit bound is preserved.

This milestone ends after the fixed eight-case sweep and fresh verification.
No remaining core, further multiplicity stratum or larger timeout is started.
A useful next direction is the blue-triangle-free nine-vertex subcore as
an anchor, while retaining the fourth red moving triangle explicitly;
the three-versus-eight full formula cannot be substituted for this
four-versus-seven action.
