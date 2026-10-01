# Degree-nine first power with reflected lights and a complex center tube

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.

For a disk-root degree-nine polynomial with critical multiset H^6,L1,L2,
the [proof](PROOF.md) establishes first-power Tang--Zhang at every
marked root for which the light points mutually reflect in the line
through zero and that root. The heavy point has any complex direction
and either distance order. A second sector permits equal-distance
nonreflected lights whose short unit reciprocal center has chord at
most(1-|a|)/80000 from that line's positive direction. Both sectors
have strict interior inequality and only the binomial boundary equality.

The new abstract reflected origin norm obeys
|I|^2>=r^12s^4+(1-b) at real mean at least b, on the entire normalized
radius range. The direct mean-loss parameterization replaces a heavy
phase cone and opening monotonicity. The unrestricted degree-nine
first-power problem and general complex6+1+1 are still open here.

From the repository root, CPython3.10+ standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -I -B sendov_degree9_reflected_light_mean_first_power/verify.py
```

Repeat with `-O` to verify that proof checks remain active under Python
optimization. Each run regenerates the complete coefficient tensors
and full identities; a successful compact JSON has result=PASS,
new_certified_sign_coefficients=30294, positive_coefficients=30186,
zero_coefficients=108 and rejected_corruptions=13. The exact expected
record is [expected.json](expected.json). The check uses one CPU and
typically takes tens of seconds with less than100MiB; no external
solver, numeric package, generated corpus or network is required.

[kernel.py](kernel.py) constructs the new moments, direct norm,
independent Chebyshev coefficient cross-products and both cleared
loss/radius charts. [verify.py](verify.py) checks every sign, zero
support and inverse Bernstein identity, exact original/cube/center
controls, actual polynomial examples and communication identities.
[algebra.py](algebra.py) and [certificate.py](certificate.py) retain
the generic arithmetic provenance listed in [LITERATURE.md](LITERATURE.md).

This is a complete ordinary author proof with exact finite evidence,
not a formal proof or an independent review. The sole imported campaign
premise is the arbitrary-phase complex6+1+1 polar mean lemma8148,
independently confirmed8184 in its stated hypotheses. Classical
Gauss--Lucas, logarithmic derivative, product identities and Rouche
remain written analytic inputs. The previously unreviewed6+2 origin
minimum and the new exploratory Schur sign are not premises. Source
publication or graph commitment alone does not constitute acceptance.
Compact source and hashes regenerate the tensors; private diagnostic
probes, checkpoints and ledgers are excluded.

Illustrative correction2026-10-01: the original rotated-antipodal
example had zero unit sum and no short center. The examples now use
a non-antipodal pair, verify the original nonzero center, and rebuild
their compact records; the origin proof and sector theorem are
unchanged. The subsequent
[square-root center theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_square_root_center_first_power/PROOF.md)
also enlarges the linear center tube proved here.
