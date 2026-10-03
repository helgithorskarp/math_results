# Original n26 rank-nine PSD cut

Actual author six-downset-2, researcher. [PROOF.md](PROOF.md) proves an
exact necessary inequality depending only on the thirty proper entries
of the declared n26 invariant star face. It excludes **every real choice
of six independent deficits** at the fixed normalized n24 transport.
The full36-coordinate face and general Conjecture H remain open.
Ordinary proof unformalized; independent review of this new result pending.

The compact [certificate](CERTIFICATE.json) specifies two integer
signed-layer vectors, the actual empty indicator and six sparse original
complement-difference vectors with positive integer weights. Their PSD
outer-product sum has original rank9 and exact constant pairing

    -274356636025866281341291/98175000000

at the transported proper coefficients. No upper cap or harmonic
completeness is used. The complete proper-only cut is also recorded.

## Reproduce

Use CPython3.10+ (author3.12.14), standard library only. In a repository
checkout, retain this directory and the three already public neighboring
files listed in [CREDITS.json](CREDITS.json):

    ../minimal_complement_classes_n24/CERTIFICATE.json
    ../minimal_complement_classes_n24/model.py
    ../minimal_complement_classes_n24/credited/matrices.py

These dependencies are pinned to their entire byte hashes in verify.py;
all are available in the published n24 source. They are defining data,
a separate credited face decoder and a literal n8 control. No discovery
program or numerical package is needed. From this directory, run serially:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1
sha256sum -c SHA256SUMS
python3 -I -B verify.py --audit --check expected.json --output /tmp/n26-cut-normal-record.json
python3 -I -O -B verify.py --audit --check expected.json --output /tmp/n26-cut-optimized-record.json
cmp /tmp/n26-cut-normal-record.json /tmp/n26-cut-optimized-record.json
```

Both modes regenerate the full mathematics before consulting the expected
record. Expected: original dual rank9,37 complete original affine-basis
probes,23125 whole table comparisons, all original rows/stars/support and
actual empty entries, eight semantic damaged-certificate rejections and
the exact negative constant above. The entire6690-byte record SHA256 is

    bc01de1d6ffb247aeb0d87ebf4515525fef7b851f6331d5f36a41a11393c648d

[VALIDATION.json](VALIDATION.json) records the actual isolated flags,
native thread values and fixed45-second guarded author runs. The literal
n8 control compares all61009 original entries and exact vector energies.
These replays check arithmetic and interpretation; they do not constitute
formalization or person-independent review.

Floating optimization supplied a proposal only. Its inaccurate negative
floor is not a proof; acceptance here uses literal original counts and
an explicit PSD dual. Numerical proposals, generated streams, virtual
environments and operational state are kept outside the public source.

The next mathematical step must change some proper coefficient. Any
positive n26 cap still needs all original cones, actual empty equations
and rank checks; this obstruction does not provide that witness.
