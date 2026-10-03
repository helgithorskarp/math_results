# Degree-nine first power on the marked three-fifths disk

Actual **six-sendov-1**, **researcher**. Every degree-nine complex polynomial
with all nine original zeros in the closed unit disk has
sum over all eight critical multiplicities |a-zeta|^-1>8 at every marked
zero |a|<=3/5. A zero denominator means infinity. This complete ordinary
analytic author proof has exact finite sufficient inequalities;
**unformalized and independently unreviewed**. The lower marked region
|a|<=11/20 explicitly depends on the author's committed lemma10101.
See [PROOF.md](PROOF.md) and [LITERATURE.md](LITERATURE.md).

The new standalone channel on CLOSED[11/20,3/5] needs only finite nonzero
complex q8, r>=5/8,F<=8,|J|>=1. It proves F>186/25,E<17/4,
Re(mean q)>1063/1600,|mean q|<=1,|O|>257/256. A separate reusable origin
lemma assumes only F<=8,E<=17/4,Re(mean q)>=1063/1600 and allows zeros.
No conjugacy, balance, equal radius, separation, individual critical-disk
condition or second-moment premise is imposed.

The key improvement is a sharp radial product bound proved with a
quadratic Hermite majorant. Its application replaces the previous coarse
radial loss and pays for a compatible energy threshold. Classical centered
coordinate, Newton and Cauchy–Schwarz/Maclaurin bounds retain their credit.

From this directory, use **CPython3.12.14**, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O verify.py
python3 -I -B validate.py
```

Replay checks all63 closed polar cells and272 closed origin leaves. Every
full polynomial is compared under two exact algebraic derivations; every
integral is evaluated in two ways. All19 polar coefficients, every origin
order2..8, both rounding directions, all seven centered recurrence minima,
and the entire closed cover topology are checked. The default is read-only.
Expected stdout reports PASS,63 polar cells,272 origin leaves and the
full checked-record SHA256 in [EXPECTED.json](EXPECTED.json).

[COVER.json](COVER.json) is the full271-split binary plan, with exact
midpoints and both closed children. No runtime adaptive search, sampled
profile, imported solver result or hidden numerical input is needed.
Polar convolution is compared against binomial/kernel-basis expansion,
with a separate beta integral. Origin convolution is compared against
multinomial counting and a separate multinomial integral. These are
same-author cross-checks, not independent review.

EXPECTED.json is a compact extrema/fingerprint record. Individual exact
case checks precede the fingerprint comparison. An optional full regenerated
record can be written with `--record /tmp/sendov-three-fifths-record.json`,
outside this directory; verbose pilot corpora remain private. All defining
inputs/formulas/cases are public, so those corpora are not an omitted premise.

[validate.py](validate.py) performs serial normal/optimized local/cold
replays, meaningful mathematical damage controls, malformed external
compact-record rejections and source-byte damage. Children have unchanged
45-second guards, all six native thread variables1, and1CPU/2GiB scope.
A timeout or incomplete cover fails without a nonexistence inference.
Observed timings and all rejection labels are in [VALIDATION.json](VALIDATION.json).

[MANIFEST.json](MANIFEST.json) pins the defining source and compact inputs.
Explicit author `verify.py --emit` and `validate.py --seal` regenerate
expected evidence and seals. Pins detect changed bytes, not joint source
and evidence replacement or correctness of ordinary analytic bridges.
The unrestricted conjecture, optimal radius/constants and a uniform extra
first-power margin remain unproved. Prior lower-region verdicts do not
supply an independent verdict for this new upper region.
