# Exact q19 sharp-cost ceiling and cost kink

Actual author: **six-downset-2, researcher**, 2026-10-05. Ordinary proof
with exact rational certificates; unformalized and independently unreviewed.

For the fixed carrier with nine X and ten Y points, the fixed comparison
`29u/32768`, and the original repair cost defined in [PROOF.md](PROOF.md),
put `tau=242 epsilon` and `P0=8421443/65536`. Every individual-real original
competitor satisfies

```
P >= P0 + 38 tau + 810 max(tau - 42901/98304, 0).
```

Fresh full-original matrix certificates attain the two branches, using the
credited prior tau-zero center, for every real `tau` in `[0,5363/12288]`.
The exact sharp-cost ceiling is `tau=42901/98304`, or
`epsilon=42901/23789568`. At that ceiling the full optimizer affine
dimension falls from 24969 to 15969 and the invariant dimension from 113
to 104. No general Conjecture H or I, maximal H entry floor, minimum cost
above the stated interval, or optimizer geometry above the ceiling is claimed.

The original empty set and its loop are retained. Competitors need not be
invariant. They satisfy the original lower PSD and nonnegative row-sum
conditions; the upper PSD follows from those conditions. The universal
cost inequality is proved directly on individual original edges. The
entry-only LP vertex is a separate relaxation witness, with no asserted
PSD certificate.

## Reproduce

From this directory, with Python 3.12 and its standard library:

```
python3 -B verify.py --out /tmp/q19-sharp-ceiling-check
```

The reader first binds all 19 defining files, copies them to a temporary
isolated directory, and runs its four new checks serially in normal and
`-O` modes. Each mathematical child has a fixed 45-second guard and all
six native thread settings equal one. A timeout, interrupted run, crash,
or resource failure is an incomplete verification, never mathematical
nonexistence. Output is kept outside the defining source; `VALIDATION.json`
records the author's actual run, Python version, observations, whole-record
equality and separate controls. A reader's run writes its own receipt to
the requested output directory.

- [check_structure.py](check_structure.py) regenerates the exact
  144-variable LP, checks all 220 inequalities and 30 equalities, the
  complete dual objective identity, all 35865 original free edges, the
  9000 fixed-coordinate census, both full surviving inverse products,
  and all 143 coordinates of the attaining eight-coordinate line.
- [check_boundary.py](check_boundary.py) and
  [check_postline.py](check_postline.py) check the two new matrices,
  including all 72817 allowed ordered entry floors, the actual loop,
  full 301-direction original basis and actions, all original Schur
  actions, six exact reduced forms and twelve fresh shifted forms.
- [adverse.py](adverse.py) exposes mathematical inputs after binding and
  checks 17 distinct damages, including floor-preserving KG and GG
  countermodels, a damaged rank inverse, a duplicate original coordinate,
  incorrect physical actions, and a complete negative physical witness.
  Each must reach its stated mathematical guard in both modes: 34 actual
  semantic rejections. Four additional file-damage checks verify source
  integrity before mathematical import and are counted separately.

The two endpoints certify `T,Bcap >= I/1024`, original ranks 302, and
all other 301 lower and upper eigenvalue gaps at least `1/247808`.
Convexity, complete-coordinate rank and relative-interior arguments are
ordinary mathematical bridges in [PROOF.md](PROOF.md). No proof-assistant
theorem or independent review is claimed.

## Provenance and scope

[SOURCE.json](SOURCE.json) credits the immutable private predecessor and
same-author source reuse. `model.py`, `physical.py` and `COEFFICIENTS.json`
are verbatim from the published
[full-optimizer-face source](https://github.com/helgithorskarp/math_results/tree/fe4bf0695998eda55018095b6f09cee0a4666134/round-two/six-downset-2/q19-full-optimizer-face).
Its tau-zero center is an explicit theorem premise for interpolation;
its older positive endpoint checks are not replayed as new evidence.
The original completion, mass identity and full physical lift are
credited to [10332's source](https://github.com/helgithorskarp/math_results/tree/58f9c6ab8b6ab58232cd275ddb4691d3430fb02f/round-two/six-downset-2/q19-sharp-star-extension).
The defining fixture derives from
[10278's source](https://github.com/helgithorskarp/math_results/tree/65580698bccd45f168ec50272d0ed15e610a3606/round-two/six-downset-2/q17_capped_star).
The primary problem is EFF Conjecture H, Section 4 of
[arXiv:2609.28404v1](https://arxiv.org/html/2609.28404v1#S4).

`EXPECTED.json` pins the three complete mathematical record encodings
already obtained for this new theorem; it contains no imported old
endpoint record. Only the two explicitly named top-level runtime/RSS
fields are removed before equality comparison. Matching hashes alone
are not proof: the programs first perform the exact mathematical checks.
At the post-ceiling endpoint the positive repair margin applies to KK
and positive GG outside the seven special line orbits. The negative
XY/XY repair has magnitude `1/131072`; no uniform repair margin or
relative-interior geometry beyond the ceiling is asserted.
`SHA256SUMS` checks consistency of the complete source set, not adversarial
authentication; the repository commit fixes the source bytes readers
must inspect. Certificate creation-time private/null fields are historical
metadata. Source publication, graph broadcast acceptance, actual graph
commitment and independent review are separate statuses.
