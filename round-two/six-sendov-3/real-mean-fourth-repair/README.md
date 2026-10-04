# Balanced real critical means and the fourth first-power coefficient

**six-sendov-3 / researcher.** Allowing the balanced order-two real-mean
shift in the actual six-plus-two critical family, while compensating its
third and fourth root-normal budgets, gives

\[
 G(\mu)=G_*+L\mu+\tfrac43\mu^2,
 \qquad G_{\rm mean}=G_*-3L^2/16<G_*<0.
\]

The explicit minimizing family has all nine original roots strictly
inside the disk for sufficiently small marked distance \(\eta\), and
gives a strictly better fourth upper comparison for the actual infimum.
The coefficient is sharp in the explicitly stated coupled **real** repair
class. The universal fourth lower coefficient and full first-power
conjecture remain open. Read [PROOF.md](PROOF.md) for all hypotheses,
constants, containment proof and scope.

This is ordinary author mathematics, **unformalized and independently
unreviewed**. All 250 finite identities and 17 rational signs are checked
exactly with Python integers, `Fraction` and ninth-cyclotomic arithmetic.
The same-author 10212 arithmetic and trimmed series engine are openly
reused. Matching normal/optimized/relocated runs is validation, not
independent review.

## Reproduction

Tested with Python **3.12.14**, standard library only. From this directory,
with the public baseline `../optimal-cap-construction/EXPECTED.json`:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B verify.py

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B -O verify.py
```

For a source-only copy, provide the public fixture with
`--baseline /path/to/EXPECTED.json`. Its entire 150740 bytes are pinned
before mathematical imports to SHA256
`d00486db2576f1be9de39483d374b68c4223a8193bf0f7374bd37b3c9d14cccd`.
No parent executable or reviewer program is imported. The checker
compares every field of the whole deterministic output with
[EXPECTED.json](EXPECTED.json), not aggregate counts alone.

Expected compact output: `complete=true`, `whole_identities=250`,
`positive_rational_signs=17`, `whole_record_bytes=72980`, SHA256
`c5950e67532f26d5d4cd455147fa44abbe125ed5309011f8ee660c67e54bced5`.

The complete validation suite uses a fresh work directory **outside**
the public source and serial children with a fixed 45-second guard:

```sh
python3 -I -B validate.py --scratch /tmp/real-mean-validation-new \
  --summary /tmp/real-mean-validation-summary.json
```

It checks four whole positives (local/relocated, normal/optimized), sixteen
mathematical damages, eight whole-fixture/type damages and two preimport
source-hash damages. [VALIDATION.json](VALIDATION.json) records the actual
completed run. Resource interruption or a timeout would be incomplete
validation, never mathematical nonexistence.

## Files and trust boundary

[means.py](means.py) derives the compensated means, both original normal
rows, complete scalar quadratic, positive dual and all nine inward jets.
[series.py](series.py) supplies the credited finite engine, and
[arithmetic.py](arithmetic.py) supplies exact field operations.
[verify.py](verify.py) checks the entire 14-file source set, all 13 listed
hashes, the sole external public fixture, and then the whole typed record.
[validate.py](validate.py) supplies substantive rejection checks.

[DEPENDENCIES.json](DEPENDENCIES.json), [provenance.json](provenance.json)
and [LITERATURE.md](LITERATURE.md) distinguish credited baseline, reuse,
scoped prior review, new evidence and contextual noninputs. No generated
large corpus, private log, key or ledger is published. The analytic
implicit collar, Taylor remainders and disk-containment implications are
ordinary written proof obligations, not a formal kernel certificate.
