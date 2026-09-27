# A permanent geometric guard for the indecomposable Gaussian frontier

The [author proof](PROOF.md) reduces the full R3 Gaussian-majorisation
question to finite indecomposable contractions fixing one prescribed regular
tetrahedron. Its four vertices each carry mass at least1/8, both supports
lie in the unit ball, and covariance is at least I/162.

These bounds hold throughout every intervening contraction chain. The
fixed anchor distances imply pointwise nonincrease of the norm; the fixed
anchor masses give the covariance floor. Thus the geometry needed by the
accepted loss-relative localization survives selection of an indecomposable
step. A conditional adverse gap divided by mean distance loss is retained
without dividing by the number of chain links.

The finite source construction adds four fixed atoms to an arbitrary
contraction. Its separated-component estimate is credited to R5's fixed-atom
argument and R7's related symmetry construction. The new feature is the
simultaneous, quantitative preservation of root shape, root mass, radius
and covariance through the full indecomposable reduction.

**Status:** complete author proof, independent review pending. No Gaussian
counterexample or new positive comparison class is supplied. The full
question remains open. Variance can approach zero and mesh size is unbounded;
this is not a completed finite cover or a Kneser--Poulsen sign theorem.
See [HANDOFF.md](HANDOFF.md) for exact consumer guards and limits.

## Reproduction

From this directory, use standard-library CPython3.11 or later:

```sh
python3 -B transplant.py INPUT.json > /tmp/guarded-transplant.json
cmp /tmp/guarded-transplant.json TRANSPLANT.json
python3 -B verify.py INPUT.json TRANSPLANT.json
python3 -B verify.py
python3 -B -O verify.py
sha256sum -c SHA256SUMS
```

The audit returns `GUARDED_INDECOMPOSABLE_FRONTIER_CONTROLS_PASS` and
reproduces [EXPECTED.json](EXPECTED.json), SHA256
`493ac75dbdcb405235dcfbf5ea70fe2c8801208319f7da5576d92961bbd4cf88`.
The normal and optimized audits took0.16s and0.31s on CPython3.11.2;
the supplied-record check took0.10s. The supplied-record mode does
not call or import the producer. It checks all91 pairs of the fourteen-label
transplant, an intermediate placement, covariance identities and all seven
principal minors at each of three stages, and the ordered-loss telescope.
The full audit adds125 exact scalar hinge cases,14 damaged-input controls,
the byte-for-byte producer check and a five-label known-positive reflection
whose full distance interval has exactly two states.

The [input](INPUT.json) uses a previous known-positive ten-label map as a
geometry fixture. No Gaussian sign is evaluated for its transplanted output.
`budget_bits` is a conditional error budget, not evidence of an adverse
Gaussian margin. The [transplant](TRANSPLANT.json) explicitly sets both
`adverse_input_verified` and `indecomposability_verified` to false.

The scripts construct no Brehm mesh and replay no old checker. The universal
analytic and geometric proof is written mathematics, not an independent
review or formalization. No solver, quadrature, external dataset, large
certificate or additional package is needed. Input semantics and provenance
are in [FORMAT.md](FORMAT.md) and [SOURCES.md](SOURCES.md).
