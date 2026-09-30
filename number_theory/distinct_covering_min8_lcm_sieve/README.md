# A finite LCM sieve for distinct coverings of exact minimum eight

**six-covering-2 — researcher.** Every such covering with actual LCM below
30240 has LCM in

    10080,12600,15120,15840,18480,20160,22680,23760,25200,27720,28080.

These are necessary possibilities. The source establishes no covering at
any listed value. With the new 20160 construction, the only remaining
candidates for L_min(8) are **10080,12600,15120,15840,18480,20160**.
For support contained in {2,3,5}, the resulting rigorous lower bound is
**43200**, without ordering the exponents. The prior global lower bound,
three exponent barriers and upper construction are explicit inputs; all
44 new finite exclusions are reproduced here. See [proof.md](proof.md).

Python **3.10 or newer**, standard library only. From the repository root:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B number_theory/distinct_covering_min8_lcm_sieve/check.py
python3 -B number_theory/distinct_covering_min8_lcm_sieve/audit.py
```

The 170717-byte `certificate.json` contains 4252 explicit weight boxes and
complete continuation records. `expected.json` gives every case manifest,
all completion counts and the ordered event hashes. The checker fails on
an uncut branch, missing child, unused record, invalid support or nonstrict
capacity inequality. The alternate audit uses different phase
normalization, full-period counts, box decoding and progression unions.
It is by the same author; external review is not asserted.
Observed CPython 3.11.2 runtimes were about24seconds for the main replay and
181seconds for the full alternate replay with controls; main peak RSS was
below47MiB, within the existing scope.

All private solver work used one thread under the standing CPU1/RAM2GiB
limits. No solver, floating-point decision or large search corpus is
required for the published replay. The unrestricted numerical interval
is **10080 <= L_min(8) <= 20160**.
