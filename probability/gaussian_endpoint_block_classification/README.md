# Gaussian comparison from an exact endpoint-block classification

The [author proof](PROOF.md) signs every contraction moving at most three
points while fixing an arbitrary bounded background, for all probability
weights, Gaussian variances and hinges. It also gives both union and
intersection Kneser--Poulsen inequalities for arbitrary individual radii.

For a general finite contraction, mixed source/target distances determine
a directed graph. Its strongly connected components are exactly the groups
that must switch together in any contracting chain using only the original
endpoint positions. The smallest possible maximum batch size equals the
largest component size. If that size is at most three, the full Gaussian
and ball comparisons follow. A stronger exact criterion also accepts larger
components with a displacement plane or a common norm anchor.

This is a finite classification and positive certificate, using the accepted
norm-preserving theorem and classical displacement-plane lifting. It does
not introduce a new R5 barrier or another motion family.

Two consequences change the shared finite frontier:

- Every seven-label contraction preserving a nondegenerate tetrahedron
  satisfies full Gaussian majorisation. An adverse rooted indecomposable
  witness needs at least eight labels and four movers, with a strongly
  connected graph and an inconsistent four-row anchor minor.
- Any adverse finite input has a single unresolved component retaining at
  least its hinge deficit divided by ordered mean distance loss. The
  extraction uses only the original endpoint coordinates and keeps weights,
  variance and threshold unchanged. It need not preserve strictness of
  every pair contraction.

An asymmetric example has any prescribed number of three-point components,
with different anchors. The ten-label [input](INPUT.json) needs two such
components; its whole map has full paired rank six and no norm anchor.
These are controls for the two specified tests, not claims of separation
from every existing positive class.

**Status:** complete author proof awaiting independent review. The analytic
inputs have their stated prior attribution. Historical novelty of the ball
consequences is unverified. The unrestricted R3 theorem remains open.

## Reproduction

Use standard-library CPython3.11 or later, from this directory:

```sh
python3 -B certificate.py INPUT.json > /tmp/endpoint-block-certificate.json
cmp /tmp/endpoint-block-certificate.json CERTIFICATE.json
python3 -B check_certificate.py INPUT.json CERTIFICATE.json
python3 -B verify.py
python3 -B -O verify.py
sha256sum -c SHA256SUMS
```

Expected audit status: `ENDPOINT_BLOCK_CLASSIFICATION_CONTROLS_PASS`.
The audit compares all4096 directed graphs on four labels with all75 weak
orders, then checks180 actual geometric orders, exact anchors and minors,
the ordered-loss telescope, frame/label changes, collisions, and10 rejection
controls. [EXPECTED.json](EXPECTED.json) gives every compact record. The
direct [certificate checker](check_certificate.py) imports no producer code
and verifies every pair at every supplied stage. No Gaussian quadrature,
solver, old motion checker or large external artifact is used.
Normal and optimized audits on CPython3.11.2 took0.36 and0.50 seconds and
produced identical records, SHA256
`3e0c61298c2dce0307ea73b3fc4ac8fe1c0b881af6a995339bdcd1ff9dfbca30`.

Input is two equally sized lists of rational3-vectors, with distinct source
points and pairwise contractive targets. Weights and variances are absent
because the conclusion holds for all of them. `NOT_COVERED` means this
specific certificate fails; a known positive four-point similarity is a
deliberate rejection control. The classifier does not search independently
chosen endpoint frames. See [FORMAT.md](FORMAT.md), [SOURCES.md](SOURCES.md),
and the [finite-frontier handoff](HANDOFF.md).
