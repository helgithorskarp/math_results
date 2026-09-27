# Independent acceptance and replay boundary

As of 27 September 2026, this certificate has **independent correctness
acceptance in its stated scope**. Historical novelty remains uncertain.
The full bounded-law dimension-three Gaussian-majorisation problem remains
open.

The accepting [review](../gaussian_deep_flap_cell_review_frontier/REVIEW.md)
is Discovery Net contribution6358,
`bafkreih4knvvl5grkggcsm26sa33esepgwus6zqcwwi2hzm5ie7w32ipcm`,
with a committed VERIFIES relation to original6341,
`bafkreidewnncabhfdz4rugy7wqmrcl6hnuyqyj6d2vbehj7vdji3mkdt7m`.
The verified review publication is
`660c395774692d339baba960d89c612ba2702e62`.

## Accepted statement

At Gaussian covariance I_3, every member of the sixteen-label coordinate
box in [CELL.json](CELL.json), with equal masses1/16, satisfies all Gaussian
hinge inequalities. With the adverse sign H from [PROOF.md](PROOF.md),

    H(u)<=0                         for all u>=0,
    H(u)<=-C u/2                    for 0<u<=1/512,
    H(u)<-1/128                     for 1/512<=u<=9/32.

The source peak is below9/32. The box has96 independent endpoint coordinate
parameters; its separately anchored slice has90. Every labeled pair has
squared-distance loss at least1/32. The rational slice belongs to R^c_2,
and the reference paired configuration has rank six.

This acceptance concerns a fixed-variance, fixed-prior positive cell.
It does not establish an all-variance flap theorem, unrestricted majorisation,
nonliftability of the damped cell, or a Kneser--Poulsen volume consequence.

## What was independently checked

The review's [checker](../gaussian_deep_flap_cell_review_frontier/independent_check.py)
imports none of this packet's code. It reconstructs the geometry and the
complete finite radial cover using binomial exponential bounds instead of
the author's alternating Taylor bounds. It verifies all194,280 radial
endpoints on504 adjoining windows, a separately reconstructed far-tail
mean-support enclosure, and deliberate corruption rejections. Its
[expected record](../gaussian_deep_flap_cell_review_frontier/EXPECTED.json)
contains the exact independent margins.

The review accepts the middle and high ranges through code inspection,
normal and optimized target replays, small entry-level controls, and the
previously reviewed quadrature theorem. It does **not** independently
reimplement the entire13.9-million-site middle histogram. Layer cake,
star-shapedness, symmetry, perturbation transfer, and the infinite-tail
argument remain reviewed written mathematics. There is no proof-assistant
formalization or claim that every component has a second implementation.

## Preserve the reviewed source while recording its later status

The mathematical source commit is
`9a3465863e32c53d9594f202a0bcc28fb58578f8`; the completed graph-cited source
is `8ee386da005a59786fbbab26eb673856e7200346`.
The later source-status commit
`c35bfcc212f282e2ac0f3c5c9f2b78055e11017c` only updated SOURCES.md and its
digest. The independent checker pins nine exact target files, including
the historical README, PROOF and SOURCES files.

Those nine files retain their reviewed bytes, including the earlier dated
"pending" wording. This notice records the subsequent acceptance without
invalidating the independent replay's pins. The target SHA256SUMS also
covers this notice. The author's EXPECTED.json retains SHA256
`f00fd3bd6b973ab64a141275927e8222199f130c619d7d3955490f04fca69c41`.

From the repository root, with standard-library Python3.11 or later:

```sh
python3 -B probability/gaussian_deep_flap_cell/verify.py
python3 -B probability/gaussian_deep_flap_cell_review_frontier/independent_check.py
```

The respective expected markers are `GAP_FREE_DEEP_FLAP_CELL_PASS` and
`DEEP_FLAP_CELL_INDEPENDENT_ACCEPT`. Each complete run takes about two
minutes on one CPU; optimized Python is also supported. Both directories
provide SHA256SUMS. No private dataset, large omitted certificate, or
reviewer workspace is required. Recording this acceptance needs only the
source-pin and manifest checks, not another complete replay.
