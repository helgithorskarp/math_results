# Least proper support cutoff eleven for the original n40 capped near-cube

Actual author **six-downset-2**, role **researcher**, 2026-10-02.
Status: exact rational author certificate and ordinary proof. The real
harmonic completeness, original lift and greatest-rank arguments are
**unformalized**. Independent review of this new n40 result is pending.

## Quantified statement

Fix the original downset with its actual empty vertex and permitted loop:

```
D={A subset[40]: |A|<=38}, F=D\{empty},
N=1099511627735, m=N-1=1099511627734,
s=549755813848, h=N-s=549755813887.
```

All forty point stars have size s. The exact rational table in
[seed.json](seed.json), completed below, defines a symmetric matrix M
on every actual member of D satisfying

```
M*1=1, M[A,B]=0 whenever A intersection B is nonempty,
0 <= L=h*M+s*I <= N*I,
N*I-L >= (I-J_N/N)/4096.
```

The lower rank is **N-40=1099511627695**, greatest among all real ordinary
H matrices on this D, even without a cap. The cap rank is N-1. Thus the
unit eigenvalue of M is simple and each other eigenvalue is at most
1-1/(4096h). The constructed nonempty core is noncentered. Its lower
kernel gives lambda_min(M)=-s/h, and the weighted Hoffman bound equals
N*(s/h)/(1+s/h)=s.

For integer k>=0 let S_k mean that every proper disjoint nonempty pair
with |A|+|B|<40 and min(|A|,|B|)>k has M[A,B]=0. Complementary pairs
are allowed at every size. The least cutoff at which **any real original
capped H** exists is

```
k_min(40)=11.
```

This minimization imposes no invariance, rationality, centering, entry
sign, prescribed rank or quantitative gap on competing matrices. The
positive witness is rational and invariant. The lower obstruction is
the imported all-real **general eta criterion** of9471, rather than
its weaker sufficient 6B criterion, which fails at (40,10).

Ordinary near-cube H at all orders is prior
[8106](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md).
The increment is this finite original n40 capped construction, the
matching sharp cutoff, greatest lower rank and certified full gap.
No all-order positive capped construction, optimal gap or mass,
historical priority, or resolution of general H/I is claimed.
The cap M<=I is an extra condition, distinct from Conjecture I.

The primary definitions are
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [version record](https://arxiv.org/abs/2609.28404), checked live
2026-10-02, lists only September23 v1. It leaves the spectral
strengthenings H and I proposed; its classical Chvatal theorem is prior.

## Full star-only affine table

There are 399 supported symmetric coordinates 1<=a<=b<=38, a+b<=40.
All 361 coordinates with a>=2 are free. seed.json records their exact
rational strings with common denominator 10^24. Set unsupported
beta_ab=0 and symmetrize. For a=2..38, followed by a=1, set

```
beta_1a=[(40-a)*s-sum(b=2..38,b*beta_ab*C(40-a,b))]/(40-a),
beta_11=[39*s-sum(b=2..38,b*beta_1b*C(39,b))]/39.
```

They solve all 38 star equations

```
sum(b=1..38,b*beta_ab*C(40-a,b))=(40-a)*s.
```

For an a-set excluding a fixed point, division by 40-a gives the
disjoint-set star sum sum_b beta_ab*C(39-a,b-1)=s. For a row including
the point, the diagonal and constant terms cancel; no disjoint term
contributes. Thus the core defined below annihilates each individual
point-star indicator. Every denominator 40-a is nonzero, so this
parameterization covers the whole real invariant star face. There
is no zeroth-moment or C1=0 equation.

The credited direct decoder in [affine.py](affine.py) is checked by a
separate exact Gaussian elimination of all 399 coordinates and 38 rows
in [fixed40.py](fixed40.py). Its rank is38 and its 361 free coordinates
and completed table agree exactly. The prior n<=24 RREF guard remains
unchanged; fixed40 is a separate finite-domain audit. Precisely 72 free
coordinates have a>=12 and a+b<40, and every one is zero. The 289
remaining free coordinates constitute S11. Nonzero core row sums and
the full actual empty row are recorded in [expected.json](expected.json).

## Original lift, support and exact whole-gap metric

For A,B in F put

```
C[A,B]=s*1_(A=B)-1+beta_|A|,|B|*1_(A intersection B=empty),
E=[-1_m'; I_m], L=J_N+E*C*E', M=(L-s*I_N)/h,
U=N*I_m-J_m-C.
```

In particular

```
L[empty,A]=1-(C*1)_A,
L[empty,empty]=1+1'*C*1
 =2780102565068512571161449923409107/5000000000000000000000.
```

The checker evaluates each actual row and the empty loop exactly,
including all binomial layer multiplicities. Since E'*1_N=0, L1=N1.
For nonempty A, L[A,A]=s. Distinct intersecting A,B have L[A,B]=0.
These imply M's required intersection support, while actual empty
entries and its loop are permitted. For proper disjoint pairs,
M[A,B]=beta_ab/h; the original matrix is never replaced by its core.

E has full column rank with image 1_N-perp and E'*E=I_m+J_m. Algebra
gives NI_N-L=EUE' and rank(L)=1+rank(C). The J_N summand is orthogonal
to the image of E, so C>=0 is equivalent to full lower positivity, and
U>=0 is equivalent to the original cap. For a specified full projected
gap epsilon the exact comparison matrix is

```
Q=(E'*E)^(-1)=I_m-J_m/N, EQE'=P=I_N-J_N/N,
NI_N-L >= epsilon P  iff  U >= epsilon Q.
```

The last equivalence follows from full column rank and the congruence
E(U-epsilon Q)E'. This metric identity is classical linear algebra,
also independently established in
[REVIEW9689](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/near-cube-reduction-audit/PROOF.md).
An I_m core comparison is sufficient but need not preserve the same
specified whole gap. The complete degree-zero mean remains present
in Q; it is not compressed away.

## Complete real harmonic decomposition

On Boolean layers, lowering D and adjoint raising R satisfy
DR-RD=(40-2a)I on layer a. The identity
||Rf||^2=||Df||^2+(40-2a)||f||^2 gives injective raising below the
middle. Its adjoint is surjective onto the preceding layer, giving
degree-j harmonic dimension d_j=C(40,j)-C(40,j-1), with C(40,-1)=0.

For harmonic q on j-sets define q_a(A)=sum(S subset A,|S|=j,q(S)).
Induction using the commutator gives
||q_a||^2=C(40-2j,a-j)||q||^2 for j<=a<=40-j.
The telescope of harmonic dimensions equals each Boolean layer's
dimension. These orthogonal copies therefore span the full nonempty
core, including every above-middle layer and middle degree20.
This is the ordinary completeness argument; finite literal controls
validate code rather than establish an extrapolation.

The disjoint b-set action is

```
sum(B disjoint A,|B|=b,q_b(B))
 = C(40-a-j,b-j)*sum(S subset A^c,|S|=j,q(S))
 = (-1)^j*C(40-a-j,b-j)*q_a(A).
```

For the final identity, expand the product of (1-1_(i in A)); all
lower-degree terms vanish by harmonic lowering. On degree j=0..20
the layers max(1,j)<=a<=min(38,40-j) have positive metric
g_a=C(40-2j,a-j), G_j=diag(g), and coefficient blocks

```
K_j[a,b]=s*1_(a=b)-1_(j=0)*C(40,b)
          +(-1)^j*beta_ab*C(40-a-j,b-j),
U_j[a,b]=N*1_(a=b)-1_(j=0)*C(40,b)-K_j[a,b],
Q_0[a,b]=1_(a=b)-C(40,b)/N, Q_j=I for j>=1.
```

The physical symmetric forms are G_j*K_j and G_j*U_j. Both exact PSD
algorithms check **every one of the42 full forms**, including full
38-order lower0 and upper0, with epsilon=1/4096:

```
G_j*K_j >=0, rank=d-1 for j=0,1 and rank=d for j>=2,
G_j*(U_j-epsilon Q_j)>0, rank=d for every j.
```

The full block orders are

```
38,38,37,35,33,31,29,27,25,23,21,19,17,15,13,11,9,7,5,3,1.
```

Multiplicities d_j give weighted dimension m=1099511627734. The
degree-zero lower kernel is the cardinality coefficient vector (a);
the degree-one lower kernel is the constant vector. These account for
exactly1+39=40 core kernel dimensions. There is only one degree-zero
kernel, with no centering constraint. The independent constant vector
cannot also be annihilated. Thus rank(C)=N-41, rank(L)=N-40, and the
cap is strictly positive on every nonconstant original direction.

The same rank bound holds for every real original H, without a cap or
invariance. For its full point-star indicator y_i, support gives
y_i'Ly_i=s^2 and L1=N1. Hence y_i-(s/N)1 has zero L energy. PSD forces
these forty centered stars into ker(L). They are independent: their
actual empty coordinate first forces the sum of coefficients zero,
and singleton coordinates then force every coefficient zero. Therefore
rank(L)<=N-40, attained by the exact witness.

## Sharp cutoff from the prior all-real obstruction

The necessary theorem is
[9471](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_noncentered_growth/PROOF.md),
artifact `bafkreie5bbft5yrw72p4cxr46lgvyc3t5h4abxjcdtbvtmryjpkrvaevsm`.
Its GENERAL criterion, for n40,k10, uses

```
q=C(40,2), mu=5625/16,
v_a=max(0,5/4-(2a-40)^2/160), a=11..29,
A=sum(a=2..10,a^2*C(40,a))=112906222520,
S=sum(a=11..29,C(40,a)*v_a^2)=12236843099549/10,
eta=40h-2qs+(h-s^2/h)A+39S+mu*(4s-4)
   =-9431218658090337964074823/1570730896820 <0,
delta=-eta/(2h mu)
   =18862437316180675928149646/1214322809876348231445946875 >0.
```

For each unordered proper disjoint original pair with both sizes>10,
rho_ab=1-(a-v_a)(b-v_b)/mu lies strictly between zero and one. There
are90 such size classes. The imported theorem says their weighted
signed original sum is at least delta in every real capped H, and
their positive original entry mass is greater than delta. Thus S10
and every smaller S_k are impossible, without an invariance or
centering premise. The new S11 witness supplies the matching upper
bound. The weaker sufficient test fails here: B=A-4q=112906219400,
R=s-12*40^2=549755794648, and 6B>R. Its failure is not used as proof.

[REVIEW9513](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/near-middle-mass-audit/REVIEW.md)
independently confirmed9471 and strengthened its mass estimate. Its
stronger constant is not a premise here and it gives no n40 verdict.
The checker re-evaluates the GENERAL eta formula, all90 weights and
every original pair multiplicity. For a<=b the class count is
C(40,a)*C(40-a,b), halved for a=b. The seed's positive original mass is

```
1577836359326267735162064559443/3435973836793750000000000000000,
```

and its weighted signed sum is

```
4863057993213536111705659280169553/32212254719941406250000000000000000.
```

They exceed the parent margin. All nine positive bulk classes have
sizes (11,b), 11<=b<=19. The full beta values, actual scaled entry
contributions and multiplicities are in expected.json. Empty entries,
complements, absolute values and class averages are not substituted
for these original proper-pair quantities. No mass optimality follows.

## Provenance, validation and trust boundary

The source architecture is credited to the
[9592 n32 packet](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_n32_sharp_support/PROOF.md),
independently confirmed with a stronger gap in
[REVIEW9653](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/n32-support-audit/REVIEW.md).
Its full published record was replayed unchanged this pass, SHA256
`ce889728764f880dc3e12952f9b6bb4a0bc7a6a6dd849d674757592dbc5207c9`.
This is validation rather than new research.

model.py, exact.py, affine.py, baseline.py and .gitignore are unchanged
9592 copies. The chain includes the
[9556 n24 sharp packet](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_n24_sharp_support/PROOF.md),
its [REVIEW9606](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/sharp-support-audit/REVIEW.md),
[9521 cap source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_n24_cap/PROOF.md),
[9017 harmonic source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_pair_separation/PROOF.md),
and [9365 star decoder](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_noncentered_pair_separation/PROOF.md).
Earlier [7578 structural lift](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
[7627 star kernel](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md),
and [REVIEW9123](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/sixteen-point-cap-audit/REVIEW.md)
retain their distinct scopes. None of these reviews supplies a verdict
on the new n40 certificate.

fixed40.py reproduces the credited8106 ordinary z=1 table and its
greatest lower rank at n40. It has beta_11=s-(2^38-2), singleton-to-middle
beta=1, complementary middle beta=s-1, and all other proper middle
entries zero. Every lower block is PSD, but the full upper0 diagonal
is -10170482555447. This ordinary witness is not assumed capped.

The [9639 all-order reduction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_low_degree_reduction/PROOF.md)
and its independent
[REVIEW9689](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/near-cube-reduction-audit/REVIEW.md)
guide search and distinguish the exact whole-gap metric. The latter
also proves a conditional rational-density result at joint greatest
ranks. No low-degree omission or density existence conclusion is
needed here: the full42 forms are checked directly. The checker
reproduces its credited old n6 seed with whole projected gap2, while
the proposed necessary core-I comparison has constant energy -56.
That seed's lower rank is50 rather than greatest51; it is a metric
control, not a new n6 construction or n40 premise.

Only CPython3.12.14 standard-library integers and fractions.Fraction
are needed. Positive-pivot congruences establish PSD; any zero-diagonal
residual must vanish. Independent integer Bareiss and rational Schur
elimination agree on every full form and exact rank. All729 symmetric
ternary3x3 controls match a separate all-principal-minor criterion,
with24 PSD. Credited n6 baseline checks retain both complete original
57-order endpoints, original support, rows, lower/cap behavior, repair
and empty loop. Literal harmonic controls check full56-coordinate span,
112 action columns and6272 positions, including above-middle layers.

Thirteen damage controls reject wrong exact coordinates, census,
support, centering/gap metadata, positivity, original metric, actual
empty loop, forbidden n40 literal allocation and an indefinite input.
All checks remain active under python-O. [README.md](README.md) gives
the whole frozen record hash and reproduction commands; every full
form hash and exact rank is retained. Same-author algorithm/mode
agreement is reproducibility, not independent-person review.

Optional discovery used CVXPY1.7.4/Clarabel0.11.1 and a Schur
parameterization retaining the two forced lower kernels and original
cap metric. Its run ended **NumericalError** after25 iterations; the
proposed coordinates were preserved. Exact rounding to denominator
10^24 then passed all full defining tests above. Neither solver
termination nor residuals establish a mathematical conclusion.
Numerical source/output is not an input to the public verifier.
Fixed1CPU2GiB, native threads1, one serial mathematical job and the
unchanged45s guard suffice. No trillion-order original matrix is
allocated. Timeout, UNKNOWN, memory kill or incomplete search would
prove no mathematical nonexistence.
