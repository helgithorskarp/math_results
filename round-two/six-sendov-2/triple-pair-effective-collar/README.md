# Explicit32111 angular stability collar

Actual author **six-sendov-2**, role **researcher**. See [PROOF.md](PROOF.md).
Ordinary author proof plus exact finite checks; independently unreviewed.

For normalized sign/permutations of

```
(-5^3,(3+X-U)^2,3+X+U+epsilon,3+X+U-epsilon,3-4X)
```

with X in[5/4,13/10], the explicit domain is the union of
U in[0,1/4],|epsilon|<=1/4 and U in[-1/16,0],|epsilon|<=1/16.
It includes all collisions and a genuine32111 collar of the known431 orbit,
retaining its threefold block and splitting its fourfold block into2+1+1.
The other32111 coalescence chart, splitting both original blocks, is outside
this explicit domain; no effective full-sphere ball is claimed.
The exact conclusions are C<=C0(X)-2(4U²+2epsilon²) and
C<=c3-300dist(theta,O3)², in the balanced unit-sphere Euclidean metric.
The earlier full-sphere local theorem and sharper asymptotic coefficient
are credited; here the smaller300 has an explicit restricted domain.

The full fourth-moment kernel and Schur correction are regenerated.
A literal genuine32111 point has actualC<c3<R3, proving that the proposed
three-moment-only global certificate cannot work. This is not a target
counterexample. Full32111,22211,6..8-level and first-power targets remain open.

From repository root, CPython3.11.2, standard library only:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
 timeout 50s python3 -I -B round-two/six-sendov-2/triple-pair-effective-collar/verify.py
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
 timeout 50s python3 -I -B -O round-two/six-sendov-2/triple-pair-effective-collar/verify.py
```

Expected PASS:34 records,eight full8 commutant controls,6498 collar
Bernstein coefficients(6270positive,228structural zeros),four whole basis
reconstructions,four mathematical damage controls. Additional13 curvature
and5 denominator coefficients are all positive. Record SHA256:

```
7fd83897a3785ba01bcfcaa8dc0bcd8ad8fe40c3142f5f56ce938f16526c80e4
```

`--expected PATH` compares a complete external fixture; missing, malformed,
altered or extra entries fail normally and under optimization. `--emit PATH`
regenerates the small full record without treating it as proof input. The
checker derives polynomial identities and every coefficient sign before
comparing the expected record. Hashes corroborate full reconstructions.

Sparse rational arithmetic and full8 commutant code adapt the credited own
fourfold checker; the final script has no runtime campaign imports. Discovery
used a separate SymPy1.14.0 substitution; it is not a runtime dependency.
The spectral interpretation, interlacing, calculus and geometric transfer
remain the ordinary mathematical proof in PROOF.md.
