# A rigorous boundary for combining the positive classes

The existing 24-site proper-screw contraction is outside the closure of
all finite compositions of anchored norm-preserving contractions and
contractions admitting a continuous motion in R5. Factor counts, frames
and auxiliary labels are unrestricted. The [author proof](PROOF.md)
classifies its entire R3 distance interval as two states and gives an
exact certificate excluding every anchor pair. Independent review pending.

This is a counterexample to a proposed factorization of arbitrary
contractions. **It is not a Gaussian-majorisation counterexample.** Its
purpose is to keep the newly proved norm-preserving class from being
mistaken for a complete route through composition. The actual finite-
variance hinge on the screw family is still open.

The construction, the R5 halfway obstruction and the finite-interval
compactness method are credited prior team work. The new result combines
them with the complete R3 interval and an anchor obstruction that remains
valid under perturbation. It does not introduce another screw template.
For distinct positive priors it also excludes exact alternative atom
matchings through such deterministic chains. Details and the remaining
positive obligation are in [HANDOFF.md](HANDOFF.md).

From this directory, with CPython3.11 or later and the standard library:

```sh
python3 -B verify.py
python3 -B -O verify.py
sha256sum -c SHA256SUMS
```

Both Python modes reproduce [EXPECTED.json](EXPECTED.json), with status
`SCREW_COMPOSITION_OBSTRUCTION_EXACT_PASS`. The checker reconstructs the
fixture and uses exact fractions throughout. There is no omitted search
corpus. Universal rigidity and compactness remain written mathematics;
code success is not independent review. [SOURCES.md](SOURCES.md) records
the essential dependencies and claim boundaries.
