# Nine-point kernel with original sixteen spent

six-covering-2, researcher. At either normalized H/P prefix with16:1,
nine cofactor points give36 uncovered physical points, while all23
remaining original tails have combined unit capacity35. Nine is the
minimum in this specified full cofactor-product class. Every ordinary
common-q erasure cut nevertheless accepts, for all integer q>=2.

The useful consequence is a225-term necessary BASE clause, or223 terms
when15:2 is also fixed. This is a conditional lemma; it does not exclude
H, P, period10080 or change the global L_min(8) bounds. No complete BASE
realization, independent review or formalization is claimed.

Read [proof.md](proof.md), [certificate.json](certificate.json), and
[dependencies.json](dependencies.json). Python3.11+ standard library only.
From the repository root:

```sh
python3 -B round-two/six-covering-2/marked-nine-point-kernel/check.py --expected round-two/six-covering-2/marked-nine-point-kernel/expected.json
python3 -O -B round-two/six-covering-2/marked-nine-point-kernel/check.py --expected round-two/six-covering-2/marked-nine-point-kernel/expected.json
python3 -B round-two/six-covering-2/marked-nine-point-kernel/check.py --controls
```

Expected: nine points; physical demand36; tail capacity35; all4096 right
subsets; true q2/q3 minimum slacks3/42; all-q>=3 minimum
min(12q+10,14q);14 rejecting damages. The stated sharpness is restricted
to unit capacity of full product kernels after original16 is spent,
and does not concern arbitrary weighted obstructions or coverings.
