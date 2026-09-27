# Eventual Gaussian majorisation for signed radial product laws

**Complete author proof; independent review pending.** Let X=A U in R3,
where 0<=A<=R and the unit direction U is independent of A, with arbitrary
angular law. Every odd scalar contraction h gives Y=h(A)U. Assume

```text
|h(R)| <= (1-epsilon)R,                    0<epsilon<=1,
P(A<=epsilon R/8) >= 2^-m,
P(A>=(1-epsilon/8)R) >= 2^-m,              integer m>=1.
```

Put N=ceil(32(m+1)/epsilon) and E=2m+4N. The [proof](PROOF.md) establishes
**every Gaussian hinge comparison simultaneously**, for every variance

```text
s >= (2112/epsilon) 2^E R^2.
```

The bound is uniform over the laws and profiles with those parameters.
Radial mass between the two clouds is arbitrary. No atoms, covariance floor,
angular density bound, or Lipschitz constant strictly below one are needed.
It includes folds that fix an inner ball and reverse outer directions.

Consequently, if 0 and the outer radius R belong to the support of A, every
odd scalar contraction gives eventual full Gaussian majorisation. When
|h(R)|=R the map on the input support is an isometry and every variance works.

The previous [signed-radial result](../gaussian_signed_radial_tail_exclusion/PROOF.md)
only signed the spherical-tail test. A new six-vertex exponential envelope
from aggregate radial clouds supplies a margin uniform in the whole tail
parameter. The [accepted Gaussian endpoint](../gaussian_majorisation_eventual_endpoint/PROOF.md)
then signs the entire hinge curve. This rules out actual large-variance
counterexamples in the class, including diffuse input laws.

The cutoff is extremely conservative. For A uniform on [0,4] and the odd
fold h(r)=r for r<=1, h(r)=2-r for r>=1, one may take epsilon=1/2, m=4,
giving s/R^2>=4224*2^1288. No smaller-variance sign or new Kneser--Poulsen
consequence follows. The unrestricted dimension-three problem remains open.

The publication refresh found R1's new
[universal spherical comparison](../gaussian_spherical_sinc_comparison/PROOF.md),
an author proof of eventual comparison for every finite contraction and every
uniformly strict bounded contraction. The present additional scope is the
uniform diffuse family at Lipschitz constant one. Its finite control is not
a new finite eventual class, and the proof does not require R1's new result.

## Reproduction

Use CPython3.11 or later, standard library only, from this directory:

```sh
python3 -B verify.py
python3 -B -O verify.py
python3 -B verify.py --schedule 4 1/2
sha256sum -c SHA256SUMS
```

The first two commands reproduce [EXPECTED.json](EXPECTED.json), with marker
`SIGNED_RADIAL_CLOUD_EVENTUAL_EXACT_CONTROLS_PASS`. Seven polynomial identities
are checked coefficient by coefficient; finite controls check360 hexagon
vertex barycentres,30 exact schedules (including very large exponents), a
16-site rank-six input, and10 malformed records. The schedule command keeps
the cutoff compressed instead of allocating its enormous power of two.
`--emit` prints a fresh expected record without reading the stored one.

These checks audit exact algebra and constants. Jensen inequalities,
independence, spherical integration and the imported Gaussian endpoint remain
written mathematics, not computer-assisted integration or formal proof.
No other lane's finite-atomic certifier is used or reimplemented.
[SOURCES.md](SOURCES.md) records attribution and source pins;
[HANDOFF.md](HANDOFF.md) states the precise remaining search boundary.
