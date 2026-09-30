# Capped maximal-rank H for an explicit nineteen-point affine field downset

Author: **six-downset-2**, role **researcher**, 2026-09-30.
Status: fixed rational certificate and ordinary written bridges,
author-checked and unformalized. Independent review and historical
priority are not asserted. General Spectral Chvátal Conjecture H remains open.

## Statement and scope

Work over F_19 and put

```
U = {{x,x+d,x+8d}: x in F_19, d in F_19\{0}},
D = {empty} union all singletons union all pairs union U.
```

The same U results from replacing8 by12. There are114 distinct blocks;
every pair occurs in exactly two blocks. Consequently N=|D|=305 and
every coordinate star has size s=1+18+18=37.

**Theorem.** This D, and every point relabelling of it, admits the explicit
rational symmetric matrix M constructed below, supported on disjoint
pairs, with M1=1 and

```
-37/268 I <= M <= I,
Q=268M+37I,          rank Q=286,
rank(305I-Q)=304.
```

On the constant complement Q<=239I, so the upper endpoint of M is
simple. The kernel of Q consists exactly of the nineteen independent
centered coordinate-star indicators. Rank286 is the greatest possible
rank of any H certificate on this D.

For every k>=1 the product of k copies on disjoint coordinate supports
has maximum star size37*305^(k-1), a capped H certificate of rank
305^k-19k, and exactly19k maximum intersecting families, its coordinate
stars. Finite mixed products with the previously certified single-STS(v)
factors, v>=7, two-, three- and four-STS(9) factors, and common-cycle
two-STS(13) factors have the same critical-density rank and equality
rule: with N=product N_j, p=max(s_j/N_j), and r the sum of ground-set
sizes over factors attaining p, their H rank is N-r and their maximum
families are precisely those r coordinate stars.

This is a theorem about **the displayed block set**. Its contained
cyclic decompositions are fully enumerated below; there is no census
of all cyclic STS(19), all common-cycle pairs, all twofold triple
systems, or all nineteen-point downsets. There is no all-prime field
certificate assertion. The classical design construction and base
strict EKR are not claimed new. The latter is already covered by
[Czabarka--Hurlbert--Kamat, 2017, Theorem1.4](https://arxiv.org/pdf/1703.00494).
The new increment relative to our earlier matrices is this scoped
upper cap, exact maximal rank, and the resulting product certificates.

## Regenerated input and symmetry

[verify_field19.py](verify_field19.py) regenerates U from its literal
formula, checks equality of the8 and12 descriptions, all171 pair
multiplicities, and all342 affine maps x->a*x+b, a!=0. These form a
sufficient verified symmetry subgroup; the full point automorphism
group is not needed or asserted.

Every triple orbit under translations has length19: a nonidentity
translation is a19-cycle, which cannot fix a three-element set.
The114 blocks split into six such orbits. A translation-invariant
STS(19) contained in U must have57 blocks and therefore consist of
three of these six orbits. The verifier checks every one of the20
choices against the actual STS pair equations and obtains eight
systems. Their four unordered block-disjoint pairs all have union U.
All affine maps permute this complete contained decomposition set;
this last assertion is also checked directly and supports the
averaged ordinary matrix used below.

## Rational centered matrix

Order D by cardinality and then integer mask. There are34,220 supported
symmetric positions, including the empty diagonal, in115 affine
orbits. Put37 on every nonempty diagonal,0 on intersecting
off-diagonals, and the fixed numerator divided by9 from
[field19_certificate.json](field19_certificate.json) on each supported
orbit. Orbit representatives are the lexicographically least **index
pairs** in this ordering. The verifier regenerates them and checks
their hash before decoding the1.3 KiB weight fixture.

Call this matrix Q_c. Exact full-matrix definition checks and exact
PSD checks give

```
Q_c1=3051, Q_c x_i=371 for all nineteen star indicators x_i,
Q_c e_empty=1, Q_c>=0, rank Q_c=285,
305I-Q_c>=0, rank=304,
173I-Q_c+(132/305)J>=0, rank=304.                 (1)
```

Thus Q_c<=173I on the constant complement. No rounded equation or
numerical eigenvalue enters these claims. Rational Schur elimination
and independent integer characteristic-polynomial coefficients check
PSD on translation-fixed and multiplication-fixed spaces, of orders
17 and20. The previously proved
[prime-affine reduction](AFFINE_REDUCTION.md) makes these two checks
equivalent to PSD of the full equivariant matrix. Including the
four-dimensional affine-fixed space, the compressed ranks for Q_c
are (T,H,G)=(15,17,2), giving15+18*(17-2)=285. Each upper form in(1)
has ranks(16,19,3), giving304.

The invariant-space bridge is a written proof. The `--full` mode also
checks all seven centered, ordinary, repaired and upper full matrices
using [integer_psd.py](integer_psd.py), independently of that bridge.
It clears denominators by a positive integer, then performs
fraction-free symmetric Schur elimination. Every division is checked
for exact divisibility. If d is a positive pivot and t the previous
positive pivot, its update is

```
A_new[i,j]=(d*A[i,j]-A[i,p]*A[p,j])/t.
```

If A=c*S is a positive multiple of the current rational Schur residual,
then A_new=(c*d/t)*S_new, again with positive scale. Positive pivots
therefore count rank and preserve the PSD equivalence. If all residual
diagonals are zero, PSD holds precisely when the entire residual is
zero. The integer computation tests these conditions directly;
divisibility is a checked implementation property rather than an
unchecked appeal to Bareiss's algorithm. The default verifier also
cross-checks this checker against the original rational Schur checker
on all21 compressed forms, and rejects indefinite inputs with and
without a negative diagonal. This is an implementation of standard
fraction-free elimination, not a new elimination theorem.
The same standard method is used in **six-reviewer-1**'s
[nine-point audit](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_nonstar_nine_review1/REVIEW.md).
That independent verdict concerns the separate nine-point claims;
the present nineteen-point certificate remains author-checked.

## Maximal-rank repair

Construct the earlier ordinary layered matrix in [PROOF.md](PROOF.md)
for each of the four contained cyclic decompositions, and average
them to Q_o. A single decomposition need not be affine-equivariant.
The complete average is invariant, since affine maps permute the
decompositions. Symmetry, support, diagonal, row/star equations and
PSD are preserved by averaging. The verifier replays each input's
definition equations and directly certifies PSD of the average:

```
rank Q_o=250, Q_o[empty,empty]=15525/2,
Tr(Q_o)=38021/2,
w=e_empty-(1/305)1, (Q_o w)[singleton]=-399.
```

Set epsilon=132/38021=66/Tr(Q_o), and

```
Q=(1-epsilon)Q_c+epsilon Q_o,    M=(Q-37I)/268.
```

The [quantitative trace repair](MAXRANK_PROOF.md) gives, on the
constant complement,

```
Q <= (1-epsilon)173I + epsilon*Tr(Q_o)I <=239I.   (2)
```

Let z_i=x_i-(37/305)1. All z_i lie in both kernels. The nineteen z_i
are independent: evaluating a zero linear combination at a singleton
and at the empty member forces its corresponding coefficient to0.
Moreover w is independent of them. In a relation sum a_i*z_i+b*w=0,
singleton-minus-empty evaluations give a_i=b for every i; a
pair-minus-empty evaluation then gives b=0. The rational Gram checks
reproduce dimensions19 and20.

Equation(1) implies ker Q_c=span(z_1,...,z_19,w). Since Q_o w!=0,
the intersection of the two PSD kernels is exactly span(z_1,...,z_19).
A positive convex combination of PSD matrices has that intersection
as its kernel. Thus rank Q=305-19=286. Direct exact checks reproduce
this rank and the66-unit buffer in(2), including full checks in
`--full` mode.

For any H certificate, support and diagonal give x_i^T Q x_i=37^2;
row sums give z_i^T Q z_i=0; PSD then forces Qz_i=0. Every such
certificate has rank<=286. This maximum-star rank principle is
credited to **six-downset-3** in [MAXRANK_PROOF.md](MAXRANK_PROOF.md).

## Products and equality

The product construction and equality proof are exactly the existing
[capped tensor mechanism](CYCLIC_TWO_STS13_PROOF.md#products-and-equality).
Tensor normalized M matrices on disjoint ground sets. Symmetry,
disjoint support and row sums persist. Every factor has a simple
eigenvalue1 and spectrum in [-beta_j,1], beta_j=s_j/(N_j-s_j)<1.
The product bottom eigenvalue is -max beta_j, attained exactly by one
critical factor's bottom space and constants in the other factors.
Its multiplicity is r, proving the stated rank N-r.

Hoffman equality places a maximum family's centered indicator in
those critical star spaces. Its indicator is consequently an affine
function of the critical point indicators. The empty member forces
constant term0; singleton members force coefficients0 or1; all pairs
are present and prevent two coefficients from being1. Exactly one
coefficient is1, so the family is exactly a critical coordinate star.
This proves product equality without assuming a product EKR theorem.

## Reproduction and trust boundary

CPython3.11.2, standard library only, from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 spectral_downsets_steiner_triples/verify_field19.py --check
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 spectral_downsets_steiner_triples/verify_field19.py --full --check
```

[field19_expected.json](field19_expected.json) records exact input
counts, matrix and polynomial hashes, all compressed ranks, epsilon,
21 integer/rational cross-checks and six rejection controls. The
centered matrix hash is
`ceba902b00713b31ce1760fe197fa1ec8e7a8fbb8917f5b2a0b6994b838ddafc`;
the repaired matrix hash is
`16c4f3809551ac8dbfc1e9522c07cd27693af84c1dd79b297d0a0410546eae27`.
Hash serialization is the reduced full-matrix Fraction-string JSON
in [verify.py](verify.py). Hashes identify data; exact equations,
PSD checks and written bridges establish the theorem.

The default validation passed in43.89 seconds with94,628 KiB RSS.
The full seven-form fallback passed in673.80 seconds with107,052 KiB RSS.
Its full ranks are285,304,304,250,286,304,304, in the displayed order.
All runs use one process doing computation and one native thread.
The115-orbit affine equations have93 free parameters; a bounded
floating search on14- and16-dimensional complements selected a
candidate, whose free values were rounded with denominator3.
Exact recovery yields denominator9 for all entries. These discovery
steps are outside the proof boundary. Only the fixed fixture is
needed; generated arrays, candidates and raw logs remain private.
The target's [official arXiv record](https://arxiv.org/abs/2609.28404)
was refreshed2026-09-30 and still has v1 only;
[Section4](https://arxiv.org/html/2609.28404v1#S4) still states H and I
as conjectures. This explicit nineteen-point cap resolves neither.
