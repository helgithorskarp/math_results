# Order-seven local phase extension

For H=<3^88> in F617*, every phase assignment on any seven or fewer
J=H union(-H) cosets extends to an H-invariant partial coloring with no
monochromatic seven-term field AP entirely inside those cosets.
[PROOF.md](PROOF.md) gives the quantified union reduction and scope.

This family supplies a barrier for phase constraints derived solely from
small local AP systems. It does not construct a full field template or a
3704-point interval coloring. Earlier global phase restrictions remain valid.

Author **six-vdw-2**, role **researcher**. Python standard library only;
Python 3.11 is supported. No solver, BLAS library, network service, or key is
needed for reproduction. The source must retain its sibling
`../order7-geometric-cut/encode.py`; its exact bytes are checked before import
using [SOURCE_PINS.json](SOURCE_PINS.json). The independent literal checker
does not use that helper or import the new generator.

From the repository root, use a fresh scratch directory:

```sh
python3 round-two/six-vdw-2/order7-local-phase-extension/run.py \
  --work /tmp/h7-local-extension-proof
python3 round-two/six-vdw-2/order7-local-phase-extension/controls.py \
  --certificate /tmp/h7-local-extension-proof/certificate.json \
  --work /tmp/h7-local-extension-controls
```

The first command generates the positive certificate and audits its full
coverage and every witness in normal and optimized Python modes. The second
runs twelve adversarial controls. Existing output directories are rejected.
Jobs run serially with numeric-library thread variables set to one.

Expected: 375760 literal APs; 26488 signed AP supports; 12936 projected
supports; 464 union-cover records; 51696 positive phase witnesses; all
683 eligible union checks and 61888 small rotation controls pass. The exact
semantic output and certificate SHA256 are in [expected.json](expected.json).
Generated witnesses, logs, and caches stay outside public source. They are
not needed as repository inputs.

Primary family context: Monroe's
[Table 1 and Table 2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
report >3703 for two colors/seven terms and prime617; that source writes
the length argument first. Here W(2,7) has two colors and seven terms, so
an AP-free coloring of [1,3704] would establish W(2,7)>=3705. The present
partial-coloring theorem establishes no such bound. The primary
[Herwig et al. paper](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
provides the multiplicative-prepartitioning background (617 is in Table3).
No universal latest-record or historical-priority assertion is made.
