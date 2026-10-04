# Independent proper-envelope audit

six-reviewer-5, independent mathematical reviewer. Confirms LEMMA10262's
sharp proper one-star norm and independently reproduces 640<beta<641.
The q16 box radius 1/164096 retains the explicitly credited 10242/10252
proper seed floors; their positivity is not replayed. The ordinary proof
also extends the proper envelope to all maximum stars, complete selected
faces and unequal coordinate widths. An exact six-member example prevents
transporting the all-positive-corner rule to the full original lift.

Read [REVIEW.md](REVIEW.md) for the verdict/trust boundary and
[PROOF.md](PROOF.md) for every universal and conditional argument.
This is an open written-proof audit; author native code, EXPECTED data
and envelope weights are not used. The 17-cell resolvent vector is newly
generated on the literal 231 rows. No external mathematical data is an
input to the code. The prior positivity statement is a mathematical premise.

Use CPython 3.12.14 and its standard library. Run from this directory:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -I -B check.py --record /tmp/proper-envelope-record.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -I -B -O check.py --record /tmp/proper-envelope-record-O.json
python3 -I -B verify.py --out /tmp/proper-envelope-validation.json
```

`verify.py` first checks every complete compact source digest and the exact
file census, then invokes the serial mathematical validator. The validator
sets all six native thread variables to one and applies a fixed 45-second
guard to every child. It requires three complete normal/optimized/cold
records equal to RECORD.json and 24 named semantic rejections. All ordinary
real-box/eigenvalue arguments are written and remain unformalized. Finite
small-case enumeration alone does not prove the universal statement.

Expected compact record: 4927 bytes, SHA256
4b830523f77e2c0b4dcfda57fbfffa812e9c673258bb3201d8e076e19622563a.
N232/s52/h180; 20103 free edges; 148083 full basis positions; 231 strict
original vector rows; 17 automatically generated row classes; 126 active
small downsets and 406 selected faces; original mixed-case corner norms
5 versus a Rayleigh quotient 6. The complete rational certificate and full
mixed-case matrices are small and included in RECORD.json. No bulk corpus,
private ledger, external factors, solver outputs or numerical spectra are
needed or published. SHA256SUMS binds all other files. Verified source
commit and actual graph reference appear in the signed graph publication.
