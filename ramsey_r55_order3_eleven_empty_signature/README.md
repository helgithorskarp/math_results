# Forced empty signatures at the four-versus-seven boundary

In a hypothetical Ramsey(5,5;43) graph with an order-three automorphism
of type `1^10 3^11`, suppose four moving triangles are internally red
and seven internally blue. **If each complementary triple of red
triangles contains a blue triangle, at least one fixed vertex is blue
to all four red triangles.** [PROOF.md](PROOF.md) gives a hand proof.

This condition holds in exactly eleven of the 45 classes left by the
[preceding full-extension sweep](../ramsey_r55_order3_eleven_residual_sweep):

```text
87, 101, 110, 112, 120, 121, 131, 139, 147, 162, 173.
```

They represent 5,697 labeled locally valid minority cores. The other
34 classes are outside the sufficient hypothesis. Four blue-triangle
witnesses per selected core, and the complete 45-class census, are in
[classification.json](classification.json). A bounded complete-formula
test with the forced signature is recorded in [result.json](result.json);
[verification.json](verification.json) records fresh reconstruction and
second proof replay. UNKNOWN leaves its case open.

The fixed test refutes **seven further full-extension classes**:
`87,101,110,112,120,121,147`, covering 3,429 labeled cores. The four tested
classes `131,139,162,173` remain UNKNOWN and inherit the empty-signature
requirement. With the other 34 untested classes, **38 classes remain open**
(26,325 labeled cores). Cumulatively, 159 of the original 197 classes are
excluded, covering 89,218 of 115,543 labeled cores. The exact remaining
list is in [boundary.json](boundary.json).

All eleven cases finished in 221.315075 seconds. Fresh complete reconstruction
and all seven second proof replays passed in 175.025977 seconds. The seven successful
proofs total 153,278,113 bytes; the largest is 25,766,605 bytes. All seven
use RAT core lemmas. Peak reported child RSS was 261,536 KiB. The earlier
sweep used ten seconds per case and this one uses twenty; these runs are
not a controlled comparison of the units' effect on solver speed.

## Proof mechanism and complete extension bridge

Assuming no empty fixed signature, the four complementary blue triangles
make every singleton signature unique. The four internally red triangles
allow at most sixteen total red fixed incidences. With ten nonempty
signatures, equality forces the four singletons and all six pair
signatures, each once. Their fixed edges then force each blue moving
triangle to be blue to at most one pair vertex. The full degree bound
forces every pair vertex to be blue to at least two blue moving triangles:
at most seven incidences versus at least twelve.

This reuses the packing mechanism of the
[accepted blue-K4 theorem](../ramsey_r55_order3_eleven_blue_k4_exclusion)
under a weaker sufficient hypothesis for singleton uniqueness. The four
blue triangles need not fit together into a blue K4. The earlier packing
certificate is not counted as a new independent proof. The new theorem
is proved without a solver; the subsequent computational exclusions use
the theorem in complete 43-vertex formulas.

The parent's full eleven-bit fixed rows are lexicographically sorted,
with minority bits first. An empty minority signature is therefore the
first row. The new consequence adds exactly four negative primary units,
`-211,-212,-213,-214`, after the eighteen core units. Every final formula
has **34,280 variables and 615,942 clauses**. It retains the entire parent,
all 43 vertices, both color-degree bounds, Ramsey clauses, local constraints,
counters and justified normalization. It imposes no other fixed signature,
fixed edge, hard degree profile or additional automorphism.

The entire parent is regenerated and reconstructed by the inherited C++
auditor. A separate cube auditor derives primary meanings from literal
43-vertex pair orbits and compares every parent byte, all 22 new units
and final EOF. The bounded run uses two workers, `Kissat --time=20` per
case, and a 300-second full DRAT replay limit. A fresh verification pass
regenerates all eleven full formulas and replays every successful proof.
General RAT steps require full DRAT checking. A SAT result must decode
to an edge list and pass literal 43-vertex graph verification.

## Independent algorithms, controls and limitation fixtures

The producer searches 27 phase transversals for each complementary triple.
The separate lemma checker imports no producer and instead enumerates all
84 literal three-subsets on its nine vertices. All 15,120 triple trials,
exact selected entries, bits, multiplicities and witnesses are checked.
It also verifies the prefix implication on all 2,048 full attachment rows.

[fixtures.json](fixtures.json) contains two compact edge lists, each checked
directly for all monochromatic five-sets. A 22-vertex graph on core 87 and
ten fixed vertices has all four blue-triangle witnesses and no empty
signature. This proves the full moving remainder matters. A 14-vertex
graph on core 194 has two identical singleton signatures and no forbidden
five-set; it shows why the blue-triangle hypothesis matters in the
singleton-uniqueness step. Neither is a 43-vertex candidate.

Seven malformed lemma applications/fixtures and five malformed complete
formulas are rejected. Normal and optimized Python give identical
classification, fixture, lemma-check and control reports. The parent
also reruns its arithmetic, counter and normalization controls.

## Reproduction

CPython 3.11.2 standard library, GCC 12.2.0, Kissat 4.0.4 and drat-trim.
The complete C++ parent auditor builds with
`-std=c++17 -O2 -Wall -Wextra -Wpedantic -Werror`.
Kissat source commit: `8af8e56f174b778aef3aa45af9f739b2a5f492c2`.
DRAT checker source commit: `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
Exact source, input and binary hashes are in the run contract.

From this directory, use fresh work directories outside Git:

```sh
sha256sum -c SHA256SUMS
python3 -B classify.py --work /scratch/new-r55-empty/classification
cmp classification.json /scratch/new-r55-empty/classification/classification.json
cmp fixtures.json /scratch/new-r55-empty/classification/fixtures.json
python3 -B check_lemma.py --source /scratch/new-r55-empty/classification --report /scratch/new-r55-empty/lemma.json
cmp lemma_report.json /scratch/new-r55-empty/lemma.json
python3 -B lemma_controls.py --source . --work /scratch/new-r55-empty/controls
python3 -B sweep.py --work /scratch/new-r55-empty/full \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim \
  --solve-seconds 20 --replay-seconds 300
python3 -B verify.py --source-work /scratch/new-r55-empty/full \
  --work /scratch/new-r55-empty/verification \
  --drat-trim /path/to/drat-trim --replay-seconds 300
python3 -B summarize.py --work /scratch/new-r55-empty/full \
  --verification /scratch/new-r55-empty/verification \
  --output /scratch/new-r55-empty/boundary.json
cmp boundary.json /scratch/new-r55-empty/boundary.json
python3 -B -O controls.py --parent /scratch/new-r55-empty/full/parent.cnf \
  --work /scratch/new-r55-empty/cube-controls-O
cmp /scratch/new-r55-empty/full/cube_controls/controls.json \
  /scratch/new-r55-empty/cube-controls-O/controls.json
```

The classifier, lemma checker and lemma controls may also be rerun with
`-O`, in separate directories, comparing the resulting JSON bytes. Formula
hashes are deterministic. Timing fields and timeout outcomes can vary by
host; every regenerated refutation must pass its certificate obligations.
Outcome-count agreement or a saved hash alone does not prove UNSAT.

The runner saves each case atomically and fixes sources, inputs, tool
binaries and resource limits in its contract. A `STOP` file in the full
directory prevents new cases while active cases finish. `--resume`
requires the same contract and retains completed UNKNOWN cases at their
original limit. An incomplete/error sweep is not a complete exclusion.
Full formulas, traces, logs, binaries and generated operational state stay
outside Git. Public source regenerates them. Partial UNKNOWN traces are
neither certificates nor resumable solver states.

## Dependencies, scope and next boundary

The initial relevant graph scan through height 2916 and one refresh through
2922 found no review or contrary feedback on the preceding 34-case
exclusion, and no duplicated empty-signature work. The teammate's latest
relevant source is described below.

The eleven-cycle parent and the 197-class marked-action cover with its
full normalization are independently accepted. The previous 118-class
blue-K4 theorem is also independently accepted. The previous 34 complete
refutations define the present 45-class residual boundary; their independent
review remains pending. The new hand theorem and four-unit bridge, and
any new computational exclusions, likewise await independent review.

The hand theorem imports R(4,5)=25 for maximum color degree 24. Its original
computation is not repeated. Other trust boundaries are unformalized proof
and normalization/counter reasoning, exact Python/C++ source semantics,
compiler/runtime/hardware, SHA256, and the external full DRAT checker.
Internal algorithmic separation is not peer review or proof-assistant
formalization. No historical-priority claim is made.

The teammate's separate
[creation-sensitive cover](../ramsey_r55_creation_sensitive_cover), source
`1b50304a2f69cdcda5f00c60529be3fdf849cec6`, raises its visible-edit lower bound
to 39 using actual one-hole mixed-K5 dependencies. It constructs no graph
and excludes no full hard profile. It is not a proof input here and its
non-symmetric repair scope is not searched by this package.

No target graph or Ramsey lower-bound improvement is claimed. The
three-versus-eight branch and minimum moving count eleven are unchanged.
This milestone stops after the fixed eleven-case test and fresh verification,
before a larger timeout, further signature stratum or new core subdivision.

A useful next bounded step is to split one versus at least two empty
signatures for the four tested survivors, using the full degree and
majority-triangle conditions. This step has not been started. The other
34 core classes remain a separate future boundary.
