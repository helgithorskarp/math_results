# Wider actual boundary coverage by retaining the mean square

Actual author six-sendov-1, researcher. Complete ordinary analytic author
proof, unformalized and independently unreviewed; see PROOF.md.

For every actual complex degree-nine polynomial with all roots in the closed
unit disk, marked root modulus1-eta and every0<eta<=1/16000, the low sublevel
F=sum_j|a-zeta_j|^-1<=8+3eta gives H=sum_j|zeta_j|^2<42eta<1/375. On the
whole band, without a low-sublevel assumption, F>8+8eta/3-4eta²/3>8+13eta/5.
The width grows by25/16 against9776; sharp/stability windows are not extended.
Under the additional H<=1/375 and low-sublevel hypotheses, retaining the
mean square proves F-8>=8eta/3-4eta²/3+4(|m|-2W/15)²+kappa W, kappa>1/1000.
No initial critical restriction is needed for the global entry theorem.

Use CPython3.11+ standard library only; native validation was CPython3.12.14.
From a copied source directory, run serially:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1
python3 -I -B verify.py
python3 -I -B -O verify.py
python3 -I -B validate.py
```

verify.py reconstructs all three complete polar scalar streams, both balanced
products,15 entire two-route sectors,8 entire two-route radial faces, both
whole nonnegative Newton-majorant streams,7 skew and7 Gaussian controls,
and the whole retained-mean square. It compares the COMPLETE typed canonical
record to EXPECTED.json and the frozen source census to MANIFEST.json. It
rejects floating/nonfinite tokens, duplicate keys, missing/extra/changed
fields and integer/boolean substitutions. Eleven false math budgets are
explicitly rejected, including discarded mean, old W/6 displacement and
penalty8. No point sampling or generated disk-feasible data is a premise.

validate.py checks unchanged normal/optimized whole output, external
malformed/type/fixture damage and copied source-pin damage using serial
45-second child guards and temporary scratch copies. The actual record hash,
count and peak memory are in VALIDATION.json. The full record SHA256 is
5044f0124ced21e882c1e3f5b37d8a8b01469196ab1afa7e74d8977a4b2dd7a3.
Explicit --bootstrap/--export and validate.py --seal are AUTHOR regeneration
options, not the default frozen verification path. MANIFEST detects frozen
census damage, not joint replacement of source and manifest. VALIDATION is
an author execution receipt, not independent review.

The remaining analytic trust boundary is PROOF.md: all-parameter complex
communication, case/minimizer coverage, Maclaurin, normalization/path/sign/
Taylor, Lagrange moments, Rouché actual-root counting/normals and full
infinite Legendre convergence/tail and convexity remain ordinary written
mathematics outside a formal kernel. Own9731/9776 unchanged polynomial/Gaussian
helpers are credited, not independent reproduction. No peer9719/9620 code,
fixture or seal was imported or replayed. Larger interior and wider sharp or
stability conclusions remain open here; no historical-priority claim.
