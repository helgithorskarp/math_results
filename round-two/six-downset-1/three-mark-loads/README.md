# Capped H for three marked pendant groups with loads(D,t,t)

Actual agent **six-downset-1**, role **researcher**. Author-checked,
unformalized ordinary proof and exact source; independent review pending.

[PROOF.md](PROOF.md) covers every Boolean cube order n>=3, three distinct
old marks and integers D>t>=1. Attach D fresh pendant leaf/spoke pairs
at the heavy mark and t at each lighter mark. With q=2^(n-1),m=D+2t,
N=2q+2m and s=q+D, the rational H matrix has universally greatest
lower rankN-1,upper rankN-1,simple endpoints and full scaled cap gap1/2.
The heavy marked star is the unique maximum intersecting family.

The new light-swap decomposition accounts for symmetric6,antisymmetric3,
all internal spaces,untouched cube eigenspaces,and the actual empty vector.
The light-leaf variance includes the extra difference energy. Ten exact
rational signs are reconstructed by coefficient arithmetic in
q=Q+4,t=T+1,D=t+B+1,Q,T,B>=0. The antisymmetric cap also follows directly
from the light internal inequality, so it adds no harder cap requirement.
General H/I and arbitrary three different positive loads remain open.
The equal profile is credited to the existing equal-load results.

Run from the repository root with CPython3.11+ and a POSIX host:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B round-two/six-downset-1/three-mark-loads/verify_signs.py --expected round-two/six-downset-1/three-mark-loads/RESULTS.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B round-two/six-downset-1/three-mark-loads/verify_full.py --expected round-two/six-downset-1/three-mark-loads/RESULTS.json
```

Repeat with `-O` for the optimization-mode regression. Expected: ten strictly
positive rational functions with8251 reconstructed nonzero coefficient
terms,complete signed1/2/6/24 determinant sums,and18 exact multiplication
controls; five original-index fixtures through N72 check3437 complete
changed-frame entries,all untouched actions,S2 symmetry,support,rows,PSD,
seed/raw/mixed ranks,unit/half-unit gaps,and10 deliberate corruption rejections.

Only the Python standard library is required. The checker imports the
credited [9005 polynomial engine](../two-unequal-loads/verify_signs.py),
[full-matrix helpers](../two-unequal-loads/verify_full.py),
[definition checker](../verify.py),and [Gram helpers](../verify_two_marks.py).
Their hashes are included in [SHA256SUMS](SHA256SUMS).
[RESULTS.json](RESULTS.json) records compact coefficient fingerprints and
full matrix hashes. The infinite quantifier is the written frame/Schur
proof and coefficient positivity; finite replay validates the construction.
No CAS,solver,network input,private polynomial corpus or credential is required.
One mathematical job at a time; thread counts1,existing60s stage/30000-term
and N80 literal guards unchanged.
