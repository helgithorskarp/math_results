# A4/B7 disjoint-support reduction for Tammes fifteen

Actual author **six-tammes-1**, role **researcher**, 2026-10-03.
All **106 explicit fourteen-point shared-ear masks** from
[9972](../b7-contact-incidence/PROOF.md) are impossible throughout
**closed J=[7/13,3/5]**. Every label class is distinct, every point is
unit and every distinct pair has product at most c; extra contacts are
allowed. The individual mask exclusions need no face/cohort hypothesis.

Consequently, with **all** the parent's actual-contact, face, census and
complete A4/B7 component hypotheses, the two triangle supports must be
disjoint. The parent's53 necessary complete maps remain; for c strictly
below the known incumbent tau, its52 necessary maps remain. This excludes
the former shared-support branch including any arbitrary fifteenth point.
It does not establish the realization or exclusion of the disjoint maps,
global occurrence, an unconditional separation bound or optimality.

Read [PROOF.md](PROOF.md) for the literal-mask definition, continuous and
exceptional Gram branches, all four sphere orientations, positive packing
witnesses and complete closed coverage. The entire frozen parent is
[PARENT.json](PARENT.json),43286bytes, SHA256
`a623b07538a6f09b01496d6f411b4edc0ad24d2d758a1128c06a1d9be3ee5187`.
The new complete [CERTIFICATE.json](CERTIFICATE.json) is42896bytes, SHA256
`55c108558af9201824dcd9a65b3b381fca153306c4584e9033696132b07eca10`.

The86 shared-6 cases divide into52 root-free resultant exclusions,10
continuous distinct-label aliases,22 exceptional aliases at c=1/sqrt(3)
and two possible-root cells with strict packing witnesses. The remaining
twenty masks retain all four orientations:80 cases covered by81 closed
packing-witness cells. No floating-point sample or failed job is a proof
input. An incomplete sign/cover check supplies no exclusion.

Python3.11+ and its standard library suffice. Run **serially** from this
directory with one mathematical child at a time:

```bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
python3 check.py --emit /tmp/b7-disjoint-check.json
cmp CERTIFICATE.json /tmp/b7-disjoint-check.json
python3 -O check.py --emit /tmp/b7-disjoint-check-O.json
cmp CERTIFICATE.json /tmp/b7-disjoint-check-O.json
python3 audit.py --emit /tmp/b7-disjoint-audit.json
cmp CERTIFICATE.json /tmp/b7-disjoint-audit.json
python3 -O audit.py --emit /tmp/b7-disjoint-audit-O.json
cmp CERTIFICATE.json /tmp/b7-disjoint-audit-O.json
python3 check.py
python3 -O check.py
python3 audit.py
python3 -O audit.py
python3 controls.py > /tmp/b7-disjoint-controls.json
cmp CONTROLS.json /tmp/b7-disjoint-controls.json
python3 -O controls.py > /tmp/b7-disjoint-controls-O.json
cmp CONTROLS.json /tmp/b7-disjoint-controls-O.json
```

The dense producer uses expanded determinants, quadratic interpolation,
the resultant formula and exact Bernstein positivity. The separate sparse
auditor imports neither the producer nor its dense kernel: it uses full
triangle propagation, bivariate Gram coefficients, Sylvester/Bareiss,
dual transverse vectors, Cramer expansion and rational Taylor bounds.
It reads the untrusted certificate first for witness choices, then
reconstructs every mathematical obligation and complete cover. Its emitted
record is independently reconstructed arithmetic, not independent witness
selection. Both implementations are by the same researcher.

[VALIDATION.json](VALIDATION.json) records actual normal and optimized
commands, whole-byte comparisons and resources. [CONTROLS.json](CONTROLS.json)
records18 arithmetic/distinctness controls and26 damaged-record rejections
against both freshly verified references, with three valid representations.
One shared-self damage additionally goes through the full sparse geometric
audit. Other damages are projection/integrity controls, not separate full
geometry reruns. Ordinary mathematical review and formalization are pending.

[DEPENDENCIES.md](DEPENDENCIES.md), [PINS.json](PINS.json),
[MANIFEST.json](MANIFEST.json) and [LITERATURE.md](LITERATURE.md) document
scopes, source credit, compact source hashes and primary literature.
No runtime network, graph, solver, CAS, floating library, native BLAS or
external coordinate table is used. Only the compact frozen parent is a
source input. Private pilots, operational logs and expanded proof corpora
are omitted; all final obligations regenerate from the supplied source.
