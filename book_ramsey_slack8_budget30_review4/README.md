# Book budget30: independent review by six-reviewer-4

[REVIEW.md](REVIEW.md) confirms the complete two-histogram exclusion behind
graph lemma8164 and proves a stronger rational-root trace obstruction in its
last square exception. This is not a resolution of the Ramsey22-versus23 gap.

CPython3.11.2, standard library, exact integers. From the repository root:

~~~bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B -O book_ramsey_slack8_budget30_review4/audit.py \
    --check book_ramsey_slack8_budget30_review4/expected.json
python3 -B -O book_ramsey_slack8_budget30_review4/controls.py
(cd book_ramsey_slack8_budget30_review4 && sha256sum -c SHA256SUMS)
~~~

The proof reconstructs768+343 weighted-defect forms from mathematical
parameters; no original research certificate selects the domain. Five proved
prime-field determinants per matrix uniquely reconstruct the integer
determinant under a Hadamard bound. All1108 nonsquares also have small-prime
nonresidue witnesses. Two33-eigenspaces have exact norm obstructions; the
last matrix has rational-root traces only in residues4/6modulo10, excluding
the host trace22. The expected output includes all three compact exception
certificates, profile/orbit counts and exact stream hashes.

The independent generator and prime-field arithmetic extend this reviewer's
credited [first-slack source](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_first_slack_review4/audit.py).
The stronger centralizer-field trace argument is written in the review.
Ordinary reductions and proof soundness are unformalized; hashes are
provenance, not proofs of coverage.

Optional comparison with the original author source can be performed after
the standalone computation:

~~~bash
python3 -B -O book_ramsey_4_7_degree_reductions/slack8_remaining_check.py \
  --matrices /tmp/book-slack8-full.json
python3 -B -O book_ramsey_slack8_budget30_review4/audit.py \
  --check book_ramsey_slack8_budget30_review4/expected.json \
  --compare-author book_ramsey_4_7_degree_reductions/slack8_remaining_expected.json \
  --compare-matrices /tmp/book-slack8-full.json
~~~

This verifies every original orbit, determinant, floor square root and F/H
fingerprint, and compares1075448 literal matrix entries. The generated
matrix corpus is optional diagnostic data; it is not published or required
by the independent proof. Use the original source commit recorded in
[PROVENANCE.json](PROVENANCE.json) when reproducing the frozen comparison.

[controls.py](controls.py) checks essential hypothesis boundaries and positive
small-field-root examples. [baseline21.rows](baseline21.rows) is the credited
known21-point construction, freshly matched to the primary public source,
not a new witness. All checks are explicit exceptions active under-O.

[VALIDATION.json](VALIDATION.json) records final timings, memory, output hashes,
source comparison and original-checker replay. The published expected file
contains the standalone output; optional comparisons add diagnostic fields.
Run one mathematical job at a time, with one numerical thread.
