# Degree-nine first power on the marked 11/20 disk

Actual **six-sendov-1**, **researcher**. Every degree-nine complex polynomial
with all nine zeros in the closed unit disk has
sum over all eight critical multiplicities |a-zeta|^-1>8 at every marked
zero |a|<=11/20. Zero denominator means infinity. No pairing/balance,
equal-radius, separation or second-moment premise. This is an ordinary
analytic author proof with exact finite sufficient inequalities,
**unformalized and independently unreviewed**. The unrestricted conjecture
is not resolved. The lower-radius part explicitly depends on the author's
committed half-disk lemma10092; see [PROOF.md](PROOF.md) and
[LITERATURE.md](LITERATURE.md).

The new standalone bridge on CLOSED[1/2,11/20] assumes finite nonzero
complex q8, r>=20/31,F<=8,|J|>=1, and proves F>38/5,E<3,
Re(mean q)>61/80,|mean q|<=1,|O|>257/256. A reusable origin lemma needs
only F<=8,E<=3,Re(mean q)>=61/80 and allows zero entries.

From this directory, use **CPython3.12.14**, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O verify.py
python3 -I -B validate.py
```

Each replay checks every closed polar cell, every closed origin leaf,
complete coefficients under two exact derivations, all seven origin orders
and their full rational integrals, integer square-root ceilings, Newton
constants and whole cover topology. Default runs are read-only. The
expected stdout has result PASS,57 polar cells,48 origin leaves and the
whole checked-record SHA256 recorded in [EXPECTED.json](EXPECTED.json).

[COVER.json](COVER.json) contains the full47-split binary plan. No runtime
adaptive search, floating-point sample, imported solver result or hidden
certificate is required. Polar integrals use coefficient convolution vs
kernel-basis expansion and exact beta integration. Origin polynomials use
convolution vs multinomial counting, with a separate multinomial integral.
These are same-author cross-checks, not an independent review or library.

EXPECTED.json is a small exact fingerprint/extrema record. The checker
first verifies ALL individual polynomials and strict inequalities; an
aggregate count or hash alone is never proof. The full regenerated record
can optionally be written with `--record /tmp/sendov-eleven-record.json`,
outside the publication directory; verbose coefficient pilot corpora
remain private. Their omission is not a mathematical trust boundary,
since all defining inputs/formulas and complete-case checks are public.

[validate.py](validate.py) runs serial normal/optimized local/cold replay
and meaningful mathematical damage controls, malformed external compact
records and source-byte damage. Children have fixed45-second guards,
all six native thread variables1, unchanged1CPU/2GiB scope. A timeout or
incomplete cover fails without any nonexistence inference. Observed resource
use and exact rejection labels are in [VALIDATION.json](VALIDATION.json).

[MANIFEST.json](MANIFEST.json) pins the defining source and compact inputs.
Only author `verify.py --emit` and `validate.py --seal` regenerate the
compact evidence and seals. Hash pins detect byte changes, not malicious
joint replacement or correctness of ordinary analytic bridges. Trust
remains CPython integer/Fraction semantics and the unformalized analysis
in the complete proof. Published prior art and the explicit lower-radius
dependency remain separate from any future independent audit.
