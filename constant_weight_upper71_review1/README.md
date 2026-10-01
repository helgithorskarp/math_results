# Independent upper-bound-71 review and two-graph proof

Actual author **six-reviewer-1**, independent mathematical reviewer.
The [complete assessment and proof](REVIEW.md) confirms
\(69\le A(18,6,5)\le71\). Attainment of 70 or 71 remains unproved here.

The new independent route uses two compatibility graphs, on 95 and 96
quadruples, and a **36,056-byte** certificate containing **4,672** proof nodes.
It also reproves the classical \(A(17,6,4)=20\) bound and proves the sharper
local statement: a seventeen-point quadruple pair packing with two
replication-five points whose pair is uncovered has at most nineteen blocks.
Both anchor forms attain nineteen.

From the repository root, CPython 3.11.2 standard library only:

```sh
python3 -B constant_weight_upper71_review1/verify.py --certificate constant_weight_upper71_review1/certificate.json --baseline constant_weight_upper71_review1/baseline69.txt --controls --expected constant_weight_upper71_review1/expected.json
python3 -B -O constant_weight_upper71_review1/verify.py --certificate constant_weight_upper71_review1/certificate.json --baseline constant_weight_upper71_review1/baseline69.txt --controls --expected constant_weight_upper71_review1/expected.json
python3 -B constant_weight_upper71_review1/produce.py --certificate constant_weight_upper71_review1/certificate.json
```

The first two commands have identical complete output. The third independently
regenerates every certificate byte; add `-O` to check its optimized execution.
The producer writes only when `--write` is explicitly supplied.

The verifier uses literal quadruples, pair sets and actual proper colorings;
it imports no producer, campaign code, solver or original research certificate.
The separate producer uses row injections, pair bit masks and integer graph
coloring. Ten malformed controls, two valid small-graph controls, seven
twenty-block affine controls and two nineteen-block sharpness witnesses pass.
All checks use exceptions and stay active under optimized Python.

[baseline69.txt](baseline69.txt) is the unchanged small
[primary Aw--Chee--Ling code](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69),
credited in [their paper](https://ymchee66.github.io/home/PDF/6cwc.pdf).
The verifier checks all 69 words and every pair independently; the lower
bound is established prior work, not a new construction.

One process, native numerical-library threads one, no external dependencies.
The full verification takes about one second in the reviewed environment.
The finite normalization, certificate-soundness induction and global counting
bridges are written proofs, not proof-assistant formalizations. Provenance,
versions, input hashes and validation timings are in [provenance.json](provenance.json).
