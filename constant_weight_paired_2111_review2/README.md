# Independent paired-star audit and upper bound65

Reviewer: **six-reviewer-2**, independent mathematical reviewer, 2026-10-01.

For a family of five-subsets of eighteen points intersecting pairwise in at
most two points, suppose two points each occur in twenty words, both positive
pair-deficit rows are `(2,1,1,1)`, and their mutual pair occurs three times.
Then the code has **at most65 words**. This improves the reviewed author's
conditional upper66. Sharpness is unknown. This review does not establish a global bound; the
maintained primary table records69–72. A newly committed campaign proof
attempt claims upper71 and is explicitly not reviewed here; see REVIEW.md.

The [review](REVIEW.md) explains the complete reduction and trust boundaries.
The independent census tests **418,037,760 full labelings**, bypassing the
author's tail double-coset reduction, and recovers2,296 compatible maps and128
ordered-center classes. A separate incidence classification gives70 classes
with the centers unordered. An explicit center exchange transports an
existing28-class partition to the sole29-class case, proving upper65.

The [source inputs](INPUT.json) pin the author's eight literal representatives
and128 untrusted partitions from
[the original artifact](https://github.com/helgithorskarp/math_results/tree/main/coding_theory/a18_6_5_no_2111_at_72).
No author executable code is imported or run. The complete eight-class theorem
is an imported premise, already independently audited by this reviewer. The
ordinary corollary for72 words additionally imports Brouwer's historical point
cap and the previously reviewed minimum-pair/no221 lemmas.

From the repository root, using fresh output directories outside the source:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B constant_weight_paired_2111_review2/audit.py \
  --target coding_theory/a18_6_5_no_2111_at_72 --work /tmp/paired2111-audit
python3 -B constant_weight_paired_2111_review2/strengthen.py \
  --target coding_theory/a18_6_5_no_2111_at_72 --work /tmp/paired2111-audit
python3 -B constant_weight_paired_2111_review2/controls.py \
  --work /tmp/paired2111-controls
python3 -B -O constant_weight_paired_2111_review2/verify.py \
  --record /tmp/paired2111-audit/audit.json \
  --control-record /tmp/paired2111-controls/controls.json \
  --strengthening-record /tmp/paired2111-audit/strengthening.json
```

CPython3.11.2 standard library, g++12.2.0, C++17; no solver or numerical library.
The normal build uses `-O2 -Wall -Wextra -Wpedantic -Werror`; controls build an
additional `-O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer` executable.
Run the commands sequentially with one intensive process. Guards remain
200,000 states and ten seconds per5040-labeling fiber or incidence problem;
the full native job also has a300-second wall guard. Failure or INCOMPLETE
supplies no mathematical verdict.

Expected: baseline COMPLETE418,037,760 assignments,2,296 maps,128 ordered
classes,70 unordered classes, original partitions upper66; then PROVED upper65.
[expected.json](expected.json) freezes the deterministic census and control
hashes. [improvement.json](improvement.json) contains the explicit18-point
transport, complete118-point candidate-index bijection, and28-class replacement
partition. [VALIDATION.md](VALIDATION.md) records the measured checks.

`verify.py` checks saved result provenance only. `audit.py --raw-input FILE`
rechecks a saved complete raw census and is not a fresh enumeration. The full
command above regenerates that census. Large joint-class tables, mapping
streams, binaries and operational records are generated privately and are not
published.
