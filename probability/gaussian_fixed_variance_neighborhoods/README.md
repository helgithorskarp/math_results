# Full Gaussian majorisation in a fixed-variance neighborhood

At any specified Gaussian variance, a strict homothety of a bounded,
full-covariance law has a nonzero neighborhood in which **every threshold**
has the majorisation sign. Both endpoint laws may be independently moved
and reweighted; arbitrary diffuse clouds are allowed.

More generally, put an already certified Gaussian comparison after the
homothety, and also require the reference target's moment-generating
function to be bounded by that of the contracted source. An exact
martingale coupling supplies the latter condition. The same explicit
neighborhood transfer then applies. [PROOF.md](PROOF.md) gives the uniform
parameter theorem, an all-threshold join and a positive mean-loss floor.

This changes the reference shape and allows targets comparable in size
to their sources. It does not only enlarge the radius in the earlier
[small-target theorem](../gaussian_uniform_small_target/PROOF.md).
R2's reviewed balanced-loss geometry supplies a nontrivial reference;
R3's verified support covers and relative cell-mass bounds supply the
perturbation inputs. Section 6 is the concise dependency handoff.

**Status:** complete author proof, independent review pending. The
unrestricted dimension-three question remains open. The perturbation
radius depends on the specified variance; one fixed positive neighborhood
is not proved to work at every variance. No new Kneser--Poulsen consequence
or historical priority is asserted.

The explicit constants are conservative. For the supplied eight-site
reference, the error budget is `2^-12859466`. We store that exponent,
not a denominator with millions of digits. The result is a uniform
positive-neighborhood theorem, not a claim of a practical coarse cover
of the remaining unrestricted frontier.

The [checker](verify.py) uses exact rational arithmetic for a nontrivial
R2 reference and its martingale witness. It also checks a 64-site cloud
calibration with paired rank six, 224 preserved pairs and 1,792 strict
pairs. Its exact anchor obstruction and zero minimum loss exclude the
norm-preserving and all-pairs balanced-loss guards on that actual
configuration. The example itself has a contracting straight motion;
it is a calibration, not claimed new geometric coverage. The theorem
applies to all admitted perturbations, not just that finite example.

Reproduce with CPython 3.11, standard library only:

```sh
python3 -B verify.py > /tmp/fixed-variance-neighborhood.json
cmp /tmp/fixed-variance-neighborhood.json EXPECTED.json
python3 -B -O verify.py > /tmp/fixed-variance-neighborhood-opt.json
cmp /tmp/fixed-variance-neighborhood-opt.json EXPECTED.json
python3 -B verify.py --input INPUT.json > /tmp/fixed-variance-input.json
cmp /tmp/fixed-variance-input.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `FIXED_VARIANCE_NEIGHBORHOOD_CONTROLS_PASS`.
Record SHA-256:
`5d96843b7c280e775370b2e346f2de73d385d5c7b8731082e4f9ac8e981dd263`.

The compact [input](INPUT.json) parametrizes the structured control; it is
not a general-purpose verifier for arbitrary laws or point lists. The
checker rejects invalid inputs and damaged witnesses, checks 36 integer
schedules and 13 negative controls, and verifies six dependency content
pins. It constructs no Gaussian quadrature and no huge dyadic denominator.
Normal and optimized CPython 3.11.2 runs each took under half a second on
the development host, with child-process peak RSS below 22 MiB.
The continuum theorem is a conventional analytic proof, not inferred
from those finite tests or formally verified. [SOURCES.md](SOURCES.md)
records attribution and mathematical dependencies.
