# Independent degree20/18 absent-pair review

Author: **six-reviewer-2, independent mathematical reviewer**, 2026-09-30.
Read [REVIEW.md](REVIEW.md) for the exact theorem scope, historical
attribution, dependency audit and trust boundaries.

This compact source independently checks the sharp restricted maximum
62, its degree20/19 multiplicity-one upper57 input, and the conditional
six-triple upper68 transfer. It regenerates all finite domains and all
color certificates, with no import or execution of target-author code.
The only external data read is the original public `witness62.json`.
[INPUT.json](INPUT.json) pins its bytes and all inspected target sources.

From the repository root, use Python 3.11 or later and a C++17 compiler.
Validated versions: CPython 3.11.2 and g++ 12.2.0. Standard libraries only.
Run these commands sequentially:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
review_dir=constant_weight_twenty_eighteen_review2
mkdir -p "$review_dir/build"
g++ -std=c++17 -O2 -Wall -Wextra -Wconversion -pedantic "$review_dir/partition.cpp" -o "$review_dir/build/partition"
g++ -std=c++17 -O1 -g -Wall -Wextra -Wconversion -pedantic -fsanitize=address,undefined -fno-omit-frame-pointer "$review_dir/partition.cpp" -o "$review_dir/build/partition-sanitized"
python3 -B "$review_dir/reproduce.py" --engine "$review_dir/build/partition" --sanitized-engine "$review_dir/build/partition-sanitized" --work "$review_dir/work/full"
python3 -O -B "$review_dir/reproduce.py" --engine "$review_dir/build/partition" --sanitized-engine "$review_dir/build/partition-sanitized" --work "$review_dir/work/full"
```

The first command regenerates geometry and runs the complete native census
when the work directory is fresh. Approximately six minutes sufficed on
the unchanged 1CPU/2GiB scope. A repeat validates the same fingerprinted
completed batches and regenerates all mathematical checks and certificates;
it is not a second native census. Remove the work directory or choose a
new one to run another fresh full census. Changed native-binary bytes
require a new directory. Do not increase the hard search guards.

Expected final output:

```json
{"cases":45100,"covers":{"0":839,"1":1927,"2":0},"expected_sha256":"644c94f2d564cf3ffb27cf590c2c5de191b85601ef1d004e82574231a13077fc","marked_star_pairs":1093,"status":"COMPLETE computer-assisted independent review"}
```

`0` is the collinear-triangle branch, `1` the orthogoval-completion branch,
and `2` the other leaves. The complete canonical [expected.json](expected.json)
also records 235,922,791 recursion states, maximum 14,780 per case,
all 1,277 marked certificate checks, literal controls, transfer cases and
the independently reconstructed 56-word completion of the 62-word fixture.
Default execution compares every stable entry, excluding runtime, RSS and
binary fingerprint. `--record` explicitly generates a new baseline and
must not be substituted for this comparison in a verification report.

The complete workflow is `domain.py` (root-edge degrees and geometric
orbits), `partition.cpp` (point-neighbor partitions and residual pair
covers), `audit.py` (all branches and direct colors), `marked.py` (the
alternative complete upper57 proof), and `validate.py` (Python reference,
sanitizers, different triple-based candidate encoding, corruption controls,
and the literal five-case transfer). `exact.py`, `degrees.py` and
`reference.py` reuse this reviewer's prior exact kernels with attribution.

Generated domain, native inputs/outputs, operational batch metadata and
full certificate lists stay in the ignored `work/` directory. Binaries
stay in ignored `build/`. They are deliberately omitted from publication.
The small expected record is a reproducibility target, not a stand-alone
UNSAT proof. All reductions are written in the review and not formalized.

The literal transfer is conditional at the reviewed height7928 source.
The newer height7996 general upper68 theorem is downstream context, not
an independently reproduced target of these commands. Dow's historical
completion theorem is an alternate cited proof input; this computation
does not audit its original proof.
