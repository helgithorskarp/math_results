# Gaussian contacts near full-rank isometries

This packet proves an explicit positive **actual concentration-profile**
margin for bounded, nondegenerate inputs whose contractions are uniformly
close after orthogonal Procrustes alignment. It uses an inward first
variation and absorbs its Taylor error by pair-distance loss. The bound
excludes nontrivial ordered contacts, including critical levels, throughout
a specified positive-time and bounded-volume range. A separate core-versus-
tail inequality gives a sufficient exclusion test for unbounded inputs.

The unrestricted dimension-three Gaussian-majorisation conjecture remains
open. This is complete author mathematics awaiting independent review,
not an accepted solution or a new Kneser--Poulsen theorem.

- [Full proof, constants and scope](PROOF.md).
- [Attribution and R5/R8 handoff](SOURCES.md).
- [Exact algebra and nonvacuity audit](audit.py), with [expected output](EXPECTED.json).

From this directory, using CPython 3.11 or later and only its standard library:

```sh
python3 audit.py --check
python3 -O audit.py --check
sha256sum -c SHA256SUMS
```

Expected status: `CONTACT_NEAR_ISOMETRY_EXACT_CONTROLS_PASS`.
The deterministic audit checks weighted double-centering and Gram identities,
the pair-strain covariance identity, six rational contraction fixtures, an
unaligned-rotation negative control, and the rational inequalities in the
Gaussian-core example. It runs in well under one second. It does not certify
the analytic proof, approximate any unknown Gaussian gap, or imply independent
review. No external data, numerical libraries or omitted outputs are needed.

The practical handoff is Theorem 1 and equations (29)--(30) of the proof.
R5's reference-set mechanism and R8's common-set stability keep their own
quantifiers; this estimate uses the source's actual optimizing set and needs
a covariance floor and small aligned displacement.
