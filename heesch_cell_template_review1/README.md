# Independent template review and core-removal certificate

Actual agent **six-reviewer-1**, independent mathematical reviewer.
Read [REVIEW.md](REVIEW.md) for the complete theorem, checked original proof,
and stronger result: every **nonempty** prototype in the 104-cell halo pool
realizing the fixed 19-copy two-corona template automatically retains the
25-cell core and tiles periodically.

From the repository root, Python 3.11.2 standard library only:

~~~sh
python3 -B heesch_cell_template_review1/check.py heesch_polyomino_cell_template_tiling/certificate.json --strengthening heesch_cell_template_review1/strengthening.json --controls --expected heesch_cell_template_review1/expected.json
python3 -B -O heesch_cell_template_review1/check.py heesch_polyomino_cell_template_tiling/certificate.json --strengthening heesch_cell_template_review1/strengthening.json --controls --expected heesch_cell_template_review1/expected.json
~~~

The checker requires the original certificate's exact pinned SHA 256, then
independently reconstructs its mathematical meaning. It imports no campaign
source, SAT solver or external geometry code. Both commands have identical
output. The original 202-step refutation, geometric 128-step core-removal prefix
and strengthened 330-step refutation are all checked.

The input certificate is already published in the adjacent original directory;
it is not duplicated here. Its seven source/input files and reviewed commit
are pinned in [provenance.json](provenance.json).
The small new proof prefix is in [strengthening.json](strengthening.json).

All runtime checks use explicit exceptions and remain active with optimized
Python. Nine malformed controls, two period-translation controls and an
essential nonemptiness check are included. One CPU, numeric/solver threads one;
full runs with controls take under ten seconds in the reviewed environment.
The written geometry and logical entailment bridges remain unformalized.
No conclusion outside the specified pool and copy template is asserted.
