# Independent uniform near-cube audit — six-reviewer-2

Read [REVIEW.md](REVIEW.md) for the exact all-real, centered, n>=16 scope and
the independent quantitative cap-excess corollary. General H/I remain open.

From the repository root, with CPython3.11.2 (stdlib only):

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-reviewer-2/near-cube-uniform-audit/verify.py
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B -O round-two/six-reviewer-2/near-cube-uniform-audit/verify.py
```

Both commands compare the entire regenerated result against [expected.json](expected.json).
Expected PASS, canonical complete-record SHA256
`bbfec9ae8c81c596b06a81843b5bfbff2803e16f2848aab434d22dccb48d5f17`,
42 positive universal shift coefficients,100 independent complement-direction
controls, literal orders57/120, seven rejected damages, the exact negative
boundary16 and cap-excess fraction reported in REVIEW.md.
`--record` prints the full regenerated record without changing any file.

[polynomial.py](polynomial.py) implements independent sparse coefficient
arithmetic over Q[n,x,T,a]. [verify.py](verify.py) solves row-count equations,
counts original-set actions, uses unordered even-multiplicity moment partitions,
and derives the bound numerator before comparing its P/Q coefficients.
No author executable, external certificate, CAS or solver is imported.
Profiles/formulas are mathematical input credited to the original source.

Finite controls check encoding; written affine/cancellation/moment arguments and
universal coefficient identities justify the unbounded theorem. Ordinary
mathematical bridges and Python remain trusted; no formalization is claimed.
Own final runs take under6seconds and23MiB; all mathematical jobs were serial
with six thread limits1 and fixed90second guards. See provenance.json and
SHA256SUMS for exact source/evidence metadata. No large matrix or private ledger
is part of this public packet.
