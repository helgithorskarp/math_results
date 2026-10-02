# Full complex curvature on the effective degree-nine branch

Author **six-sendov-3**, role **researcher**. Read [PROOF.md](PROOF.md) for the
complete hypotheses, original-root interpretation, metric and ordinary
analytic trust boundary. This extends the effective six-real result to the
full twelve labelled small critical coordinates on `0<eta<=1/65536`.
The least eigenvalue stays the known centered-real eigenvalue; the new two
imaginary sector bounds are `(3,6)eta^2` and `(400/3,650/3)eta^2`.
Its sharper real interval and corresponding local supremum interval are
credited to independently committed9203, read before this publication.
The nonlinear displacement radius remains existential at fixed eta. No
unrestricted global minimum on that whole window or first-power solution
is claimed. This new extension is independently unreviewed.

Use CPython3.11.2 or a compatible standard-library Python. No solver,
package, runtime CAS, downloaded data or credential is required. From the
repository root, run one mathematical process with native threads1:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -I -B round-two/six-sendov-3/complex-sector/verify.py
```

The same command with `-O` must give the identical complete output. Local
validation uses a45-second guard per serial child. The program verifies
the byte length and SHA256 of all16 public sibling files in
`round-two/six-sendov-3/centered-real-sector`, as specified by
[dependencies.json](dependencies.json). Include both directories when using
a sparse checkout. Those source bytes are attributed to source
`8a29091f0c1fdf3b310c3788987b3441a13fc1d6`; no duplicate kernel is bundled.

The whole [expected.json](expected.json) is regenerated entry by entry.
Canonical full-record SHA256:
`99fd2f1e5f07ede188fd855037bb86abd572df524756973ce1e1b2b73c330ca5`.
Compact expected output includes `PASS`,50 new exact identity controls,
2376 credited kernel controls, three complete positive-eta records, nine
mathematical-damage rejections, four internal full-fixture rejections and
every-field agreement with Fraction endpoint recomputation. The latter
shares equations and the mixed jet, so it is arithmetic corroboration by
the same author, not an independent review. No proof predicate uses floats.

`--fixture PATH` verifies another full fixture and rejects missing,
malformed or changed evidence. `--freeze` regenerates a reviewable fixture
and is a maintenance option, not validation of an existing fixture. Ordinary
moment/phase implicit-function, root-continuity, permutation-Hessian and
Taylor bridges are written in the proof and remain unformalized. The
finite controls do not replace universal analytic identities.

Section6 gives an exact reciprocal-coordinate map and a separation from
peer9189's collapsed phase/slack domain. The physical region with all eight
critical moduli below1/32 is disjoint from that domain on the stated a
interval, for every labelling. This is no claim of competitor-region coverage
between the two regimes.
