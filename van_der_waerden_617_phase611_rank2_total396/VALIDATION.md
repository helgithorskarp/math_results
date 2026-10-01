# Actual validation

Author: **six-vdw-3**, researcher. These are same-author independent
implementation checks, not external review or formalization.

Frozen standard-library reproduction passed with CPython3.11.2 in5.835s,
optimized CPython3.11.2 in6.229s, and CPython3.12.14 in5.727s. Exact result files
were identical in all three runs. The optimized run's mathematical control
subprocess also actually ran with optimization enabled. No substantive check
depends on Python assertions.

Each run rejected29 mathematical corruptions and11 malformed logical tuples.
The controls exercise wrong dependency hashes, hidden branches, weaker caps,
noninteger/bool data, out-of-range APs, duplicate rows, full-domain overload,
invalid triple intersection, unsupported budget deductions, poles, missing
contradictions, trial freshness, nested assumptions and unknown tuple tags.
The generic covering/defect checks exhaust255 empty-intersection three-edge
families on four vertices,1529 weighted hitting models,3337 defect-budget
models and4566 strict-screen cases. Their exact integer checks support the
written argument; they are not an enumeration of3704-point words.

The frozen premise has one failed literal,13 actual unit implications and53
budget deductions. It proves3159 unchanged under e_0<=197, with e_1 uncapped.
Together with82 original packing screens, the inherited state has83 positions.
The new weighted certificate checks897 single APs and135 AP occurrences in45
distinct triples, then every capacity on the complete1766-point original0
remaining domain. W=196317912,D=1000000 gives defect budget682088.

The frozen scoped exclusion checks881 global units,188 global budget facts,
139 failed literals,16983 trial units and6896 trial budget facts. Its final
two forced original0 edits consume804868 packing-defect units, strictly exceeding
682088 by122780. No other-class forced edit is needed in this retained terminal.
The proof still uses the explicit other-class cap198 in its scoped implications.

A fresh CPython3.12.14 source-only run regenerated the one-position premise
from the selected old coefficients. It reused only the public integer packing,
then generated and checked five new serial proposal windows. Fresh logical
generation and pruning took79.343s, in addition to the preceding5.727s frozen
checks. Every configured proposal loop was eight seconds with at most400 probes;
serialization and checking add wall time. Parent peak RSS125984KiB, child peak
RSS118204KiB. The fresh pruned proof has132 failed literals and ends in the actual
monochromatic AP(11,22), independently checked on its seven interval positions.
It is a distinct valid contradiction and is not claimed byte-identical to the
frozen packing-defect proof. Full raw fresh traces remain outside Git.

The numerical proposal originally used a checked431-position experimental
domain. Three successive augmentation solves raised its floating guide from
196.012876 to196.318389; all native solves were optimal and under0.6s, with the
unchanged15-second limit and one thread. Up to104 triple rows were selected;
45 have positive coefficients in the published exact packing. These numerical
values neither prove optimality nor exclude the cap. The final independent
packing check instead replays the smaller83-position premise and checks the
FULL1766-point remaining domain. The experimental431-position proof is not an
input. Selection-limit exhaustion, no violated floating guide row, timeout,
UNKNOWN or no witness found establishes no mathematical exclusion.

Read-only graph refresh attempts hit the existing45-second guard. Splitting
searches and omitting unneeded nested source fields recovered complete bounded
reads at8288, with complementary bodies read at8290. No limit was increased.
All research jobs were serial; solver/BLAS/OpenMP threads were one. The previous
timed-out transversal MIP was not retried and supplied no proof evidence.

The compact publication includes plain JSON logical certificates rather than
large exploratory corpora, binary archives, known-state dumps or environments.
`manifest.json` pins every mathematical input and separates compact-file hashes
from canonical decoded logical-record hashes. Actual check summaries and
resources are recorded in `validation.json`.
