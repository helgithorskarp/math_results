# A proper screw can require six dimensions

The [author proof](PROOF.md) gives 24 rational sites in two rigid groups.
The fixed group has 16 sites; the moving group has eight and undergoes a
quarter-turn plus axial translation. All endpoint distances contract, but
no continuous contraction in R5 exists. An explicit R6 contraction does.

This is a negative checkpoint for extending the
[positive tangential motion](../gaussian_tangential_screw_lift/PROOF.md)
to arbitrary endpoint-contractive two-group maps. It is **not** a Gaussian
counterexample, a new positive Kneser--Poulsen class, or a minimal-size
claim. Independent review and historical priority remain pending.

R6 handoff: endpoint contractivity and proper relative orientation cannot
replace the sign hypotheses of the earlier motion. Eight exact contacts
and eight nearby probes force an impossible halfway state; the proof gives
a rational gap of 1/96. The witness is intended as an adversarial control
for universal tangential-lift proposals. This route is closed; no nearby
family catalogue is needed. The unrestricted Gaussian sign is still open.

`WITNESS.json` lists the prescribed labels and both endpoints.
`check.py` independently rebuilds those endpoints with exact fractions,
checks every pair, and checks the algebraic certificate. The first-time
crossing argument and the reduction of a preserved rigid group to an
affine isometry are the handwritten trust boundary.

Validated with CPython 3.11.2, standard library only:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 check.py > /tmp/screw-check.json
diff -u EXPECTED.json /tmp/screw-check.json
PYTHONDONTWRITEBYTECODE=1 python3 -O check.py > /tmp/screw-check-opt.json
diff -u EXPECTED.json /tmp/screw-check-opt.json
sha256sum -c SHA256SUMS
```

The checker exits nonzero on a mismatch. `--write-fixture` is only a
deterministic fixture-generation command, not needed for reproduction.
There is no solver, floating point, external dataset, or omitted large
certificate. The point/motion checks do not by themselves prove
nonexistence; Sections 2--5 of the proof do.

Current team context at the start of this checkpoint: R3's moving
small-loss estimate and R5's averaged replica gap had accepting reviews;
R5 had completed beta rows through eleven; R8 had an arbitrary-radius
covariance-boundary theorem; R1's reflection-group alignment source was
published; R7's latest certified contact was positive. The publication
refresh also included R2's damped all-threshold martingale family and
R6's [meridian theorem](../gaussian_meridian_contractions/PROOF.md), whose
azimuth-preserving hypothesis excludes the present prescribed screw.
These are not
premises of the obstruction. It does not reopen closed cap/flap/parity
work or replace any of those positive results.
