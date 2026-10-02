# Five-hub pair total 35 at 71 words

Actual author **six-code-1, researcher**. [PROOF.md](PROOF.md) establishes
the conditional lemma: a 71-word weight-five packing on 18 points with
exactly five unsaturated points has hub-pair total **P>=35**. A correction
for eight actual five-hub row markings extends the prior capacity cut.
At P=34, the exact necessary row inventory would force a nonempty closed
cubic graph on six vertices with no triangles or four-cycles, impossible.

The explicit dependencies are the reviewed upper71/universal star theorem
8323, reviewed generic23-star coverage8933, and local three-point9249
independently confirmed by9293. [DEPENDENCIES.json](DEPENDENCIES.json)
records the exact scopes, graph references and source commits. The new
capacity/extension/girth transfer is author checked, unformalized and
independently unreviewed. Independent9355 confirms the earlier P34 bound,
with no verdict on this new P35 proof. The unrestricted campaign interval69..71 stays
open. No historical priority, sharpness or whole-profile exclusion is claimed.

Use CPython3.11+ and its standard library. Author validation uses3.11.2.
From the repository root, write generated evidence to a separate scratch
directory. The checker itself writes only the requested output file.

```sh
mkdir -p scratch/five-hub35
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 round-two/six-code-1/five_hub_pair_total35/verify.py \
  --output scratch/five-hub35/normal.json

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -O round-two/six-code-1/five_hub_pair_total35/verify.py \
  --output scratch/five-hub35/optimized.json
```

Both complete mathematical outputs must equal the result frozen in
[EXPECTED.json](EXPECTED.json), byte for byte after the documented
sorted-key, two-space-indented JSON serialization plus a terminal newline.
The checker compares the entire decoded expected object, not only hashes.
[VALIDATION.json](VALIDATION.json) records the cold runs, timings, output
hash and unchanged mathematical source/input hashes.

The exact checks cover every one of426 physical marked rows, including
the eight five-high-hub exceptions; all necessary categories and every
count vector in both P34 branches; all5005 nine-edge sets on six vertices;
the positive abstract Petersen graph; all2346 pairs of the credited
69-word baseline;22 semantic damage/scope/nonempty controls; and1278
marked rows under actual point permutations. The full corrected row hash is
`4832875a52850041bc33b5fc8d99ab96de0a35019b0b2dad68830701cb0d5034`.
The boundary patterns are empty for Q=0 and uniquely[6,1,6,0] for Q=1,
in the explicitly included category order. They are necessary statistics,
not realizations of packings.

[fixtures.json](fixtures.json) is the unchanged compact credited23-star
input. Its supplied groups are unused. The checker reconstructs owners
from intersections of physical block-index columns and imports no author,
reviewer, solver or earlier program. The written complete23-star coverage,
incidence, extension and physical graph bridges are mathematical inputs;
an output digest or abstract graph enumeration does not prove those bridges.
Executing the published9313 programs in this pass is baseline validation,
not an independent review of this new lemma.

Only compact source/input/expected evidence is published. Complete row
arrays, peer replay records and operational state stay in scratch. One
serial mathematical job, native numeric threads1, unchanged1CPU2GiB.
Fixed100000-state/10-second category guards fail loudly if incomplete;
author cold subprocess guard10seconds. No timeout or resource kill is
used as mathematical nonexistence.
