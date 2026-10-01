# Reproduction and trust boundary

Author: **six-vdw-2**, role **researcher**. Same-author independent
implementation audit; no independent peer review or formalization claimed.

The generator and checker use different constructions. Generation reuses
the pinned logarithm-based field support helper, bit rotations, a union queue,
and bit-mask color tests. The checker imports neither helper nor generator:
it constructs signed H-cosets by literal multiplication, enumerates every
field AP, uses coordinate translations for rotations, verifies union closure,
and checks actual dictionary colors against every internal AP support.

Complete normal and optimized audits verify all 2520 cover representatives,
all 7432 eligible union tests, and all 578032 positive phase witnesses. The
certificate SHA256 is
`7d28652b4e096ac3dea2efd7393746c2e500a7ad7bf77483755bd25a94317584`.
Both literal quadratic-residue colorings pass the full AP census. Another
61888 exhaustive tiny controls check signed-coset wrapping, phase rotation,
and global color exchange. Every coverage guard uses explicit exceptions
and remains active under `python3 -O`.

The runner uses serial mathematical subprocesses, numeric-library threads
one, and a fixed 55-second deadline for each generation or audit stage.
Deadline failure proves no mathematical statement. Python 3.11.2 was used
for a fresh release-source reproduction:

| Stage | Seconds |
| --- | ---: |
| Positive certificate generation | 4.912 |
| Independent normal audit | 26.598 |
| Independent optimized audit | 23.251 |
| Complete runner | 55.300 |

Peak child memory was 49292 KiB and parent memory 16020 KiB. The generator
scanned 3652094 normalized orientation words before obtaining all positive
witnesses. The output result records the exact timings and memory values.

The adversarial controls make five isolated corruptions of the checked
certificate: wrong field, missing phase witness, boolean masquerading as
an integer word, constant coloring with the correct phase, and omission
of a nonbasis support union. All are rejected by their mathematical guards
in normal and optimized modes. A sixth control changes an isolated helper
copy and is rejected before import in both modes. No published helper is
modified. The controls report the exact omitted union mask and twelve
successful rejection checks. All twelve passed for the fresh checked
certificate; the omitted nonbasis union mask was 33603905.

The mathematical trust boundary consists of Python integer/set semantics,
the independent literal checker, the explicit rotation/union reduction in
PROOF.md, and the checked positive colorings. No solver, proof converter,
floating-point computation, UNKNOWN, or incomplete negative search is a
premise. This proof establishes local flexibility, not full-field extension
or a global van der Waerden bound.
