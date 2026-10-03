# Independent review of coupled cubic coercivity

Actual **six-reviewer-3**, **independent mathematical reviewer**, 2026-10-03.
Audit of LEMMA9894/0, actual author six-sendov-3. Written formulas and our earlier
work were exposed. Fresh ordinary proof/arithmetic were sealed before native
code and fixtures were accessed; this is not blind or formally checked.

The standalone lemma is proved for every zero-sum complex n-tuple, n>=2,
and all real |A|<=|beta|. On the actual degree-nine boundary band eta<=1/16000,
the new leaf deductions are checked relative to explicit9857 local inputs.
Both target230 objective and247 physical costs are reproduced, and rational
459/2 objective and987/4 physical refinements are proved with all the same
moment/all-nine stability estimates and BOTH cuts. See [PROOF.md](PROOF.md)
and [REVIEW.md](REVIEW.md) for exact hypotheses, adoption boundary and verdict.

Python3.12 standard library only; keep one native thread in all six libraries.
From this directory:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python audit.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python -O audit.py
python validate.py
```

`SUMMARY.json` freezes the entire compact output; `audit.py --record /tmp/cubic-record.json`
regenerates the entire canonical coefficient/budget/control record. Do not
publish that larger generated record. `validate.py` executes serial normal/O
baselines plus eight meaningful damages under the unchanged45-second child
guard. All checks use explicit exceptions and survive optimization.
`SEAL.json` pins the pre-native core, proof and receipts. Native comparison is
post-seal replay/adoption evidence; it does not replace the independent proof.

An initial naive helper run hit45seconds while constructing an unused final
polynomial square. That child was stopped; the unused work was removed without
changing resource limits. A proposed smaller physical lambda failed the exact
determinant and was discarded. Neither failure was a mathematical exclusion or
a defect in the target. The final core runs in about two seconds. No solver,
additional worker, purchased resource, formal proof kernel or hidden dataset.
