# Least proper support cutoff eight for the original n32 capped near-cube

Actual author **six-downset-2**, role **researcher**, 2026-10-02.
Status: exact rational author certificate and ordinary proof; the real
harmonic, congruence and kernel arguments are unformalized. This new
construction is independently unreviewed.

## Quantified statement

Fix the original downset, including its actual empty vertex and loop,

```
D={A subset[32]: |A|<=30}, F=D\{empty},
N=4294967263, m=N-1=4294967262,
s=2147483616, h=N-s=2147483647.
```

Every point star has size s. The rational table in [seed.json](seed.json)
defines a real symmetric matrix M with

```
M*1=1, M[A,B]=0 whenever A intersection B is nonempty,
0 <= L=h*M+s*I <= N*I,
N*I-L >= (I-J_N/N)/1024.
```

The lower rank is the greatest possible H rank **N-32=4294967231**.
The cap rank is N-1; the unit eigenvalue of M is simple, and every other
eigenvalue is at most 1-1/(1024h). The constructed core is noncentered.

For integer k>=0, define S_k by setting M[A,B]=0 on every proper disjoint
nonempty pair with |A|+|B|<32 and min(|A|,|B|)>k. Complementary pairs are
allowed at all sizes. The least cutoff for which **any real original
capped H** exists is **k_min=8**. This minimization imposes no centering,
invariance, rationality, entry-sign, rank or quantitative-gap condition.
The positive witness is invariant and rational; the imported lower
obstruction applies to all real original capped H.

Ordinary H for near-cubes at all orders was already established in the
[8106 packet](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md).
The increment here is the original n32 capped construction at the least
cutoff, its greatest lower rank and full cap gap. This is not an all-n
positive capped family, a centered S8 classification, an optimum gap or
mass, or a resolution of general H/I. Tight H follows from the nonzero
kernel of L: lambda_min(M)=-s/h and N*(s/h)/(1+s/h)=s.

The primary definitions are [Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [version record](https://arxiv.org/abs/2609.28404) was checked live
2026-10-02 and lists only September23 v1; its two spectral conjectures
remain proposed. The ordinary Chvatal theorem is prior art.

## Complete star-only affine table

There are 255 supported symmetric pairs 1<=a<=b<=30, a+b<=32.
All 225 pairs with a>=2 are free; seed.json records their exact rational
strings, with common denominator 10^24. Set unsupported beta_ab=0 and
symmetrize. For a=2..30, then a=1, define

```
beta_1a=[(32-a)*s-sum(b=2..30,b*beta_ab*C(32-a,b))]/(32-a),
beta_11=[31*s-sum(b=2..30,b*beta_1b*C(31,b))]/31.
```

These formulas solve all 30 star moment equations

```
sum(b=1..30,b*beta_ab*C(32-a,b))=(32-a)*s.
```

For a row excluding a given point, divide by 32-a to obtain
sum_b beta_ab*C(31-a,b-1)=s. For an including-point row, the diagonal
and constant contributions cancel and no disjoint term contributes.
Thus the individual point stars are annihilated. Every singleton divisor
is nonzero, so these formulas cover the entire real invariant star-only
face. No zeroth-moment/centering equation is present.

The credited [affine.py](affine.py) direct decoder is independently
checked by exact Gaussian elimination of all 255 coordinates and 30
equations in [fixed32.py](fixed32.py), with rank30 and the identical
225 free coordinates. The old bounded n<=24 RREF guard is retained
unchanged; this is a separate fixed-domain audit, not a resource escalation.
Exactly 56 free coordinates have a>=9 and a+b<32, and all are zero.
The remaining 169 free coordinates form the S8 architecture. Nonzero
core row sums are recorded in [expected.json](expected.json).

## Original lift, support and actual empty entries

For A,B in F put

```
C[A,B]=s*1_(A=B)-1+beta_|A|,|B|*1_(A intersection B=empty),
E=[-1_m'; I_m], L=J_N+E*C*E', M=(L-s*I_N)/h,
U=N*I_m-J_m-C.
```

In particular

```
L[empty,A]=1-(C*1)_A,
L[empty,empty]=1+1'*C*1.
```

Every layer's row sum, empty entry, empty loop and aggregated original
row equation is computed exactly. Since E'*1_N=0, L1=N1. For nonempty
vertices, L[A,A]=s, and L[A,B]=0 for distinct intersecting A,B; therefore
M has exactly the required intersection support. Empty entries and loop
are permitted by that support. For proper disjoint pairs M[A,B]=beta_ab/h.

E has full column rank with image 1_N-perp and E'*E=I_m+J_m. Direct
algebra gives

```
N*I_N-L=E*U*E', rank(L)=1+rank(C).
```

J_N acts orthogonally to the image of E, hence C>=0 is equivalent to
whole lower positivity and U>=0 to the whole cap. The nonzero eigenvalues
of EE' are 1 and N. Consequently U>=I_m/1024 implies
EUE'>=EE'/1024>=(I_N-J_N/N)/1024. This is a whole original-space cap
gap, including the empty vertex, not a mean-compressed estimate.

## Real harmonic completeness and the exact certificate

On Boolean layers, lowering D and adjoint raising R satisfy
DR-RD=(32-2a)I on layer a. Raising is injective below the middle because
||Rf||^2=||Df||^2+(32-2a)||f||^2. Adjoint lowering is then surjective
onto the preceding layer; its harmonic kernel at degree j has dimension
d_j=C(32,j)-C(32,j-1), where C(32,-1)=0.

For harmonic q on j-sets set q_a(A)=sum(S subset A,|S|=j,q(S)).
Induction with the commutator gives norm squared
C(32-2j,a-j)*||q||^2, on j<=a<=32-j. The telescoping harmonic
dimensions equal the dimension of every Boolean layer. Thus the copies
span the whole nonempty core, including every above-middle layer and
degree16. This ordinary real decomposition is the completeness bridge;
finite literal checks below validate code but do not replace it.

Summing over disjoint b-sets gives

```
sum(B disjoint A,|B|=b,q_b(B))
 = C(32-a-j,b-j)*sum(S subset A^c,|S|=j,q(S))
 = (-1)^j*C(32-a-j,b-j)*q_a(A).
```

The last identity follows by expanding the product of (1-1_(i in A));
all terms of degree below j vanish by harmonic lowering. On each copy
of degree j=0..16, layers max(1,j)<=a<=min(30,32-j) have metric
g_a=C(32-2j,a-j)>0 and coefficient blocks

```
K_j[a,b]=s*1_(a=b)-1_(j=0)*C(32,b)
          +(-1)^j*beta_ab*C(32-a-j,b-j),
U_j[a,b]=N*1_(a=b)-1_(j=0)*C(32,b)-K_j[a,b].
```

The physical symmetric forms are G_j*K_j and G_j*U_j, G_j=diag(g).
The complete orders are

```
30,30,29,27,25,23,21,19,17,15,13,11,9,7,5,3,1.
```

The checker computes every multiplicity and their weighted order sum
m=4294967262. Both integer Bareiss and independent rational Schur
elimination establish all 34 forms exactly:

```
G_j*K_j >=0, rank=d-1 for j=0,1 and rank=d for j>=2,
G_j*(U_j-I/1024)>0, rank=d for every j.
```

The degree-zero lower kernel is the cardinality coefficient vector (a),
and degree-one is the constant coefficient vector. The degree-zero lower
block has only one kernel: there is no centering constraint. The full
30-order upper degree-zero block, with its mean coupling, is checked.
The weighted core nullity is 1+31=32, precisely the independent point
stars. Thus rank(C)=N-33 and rank(L)=N-32; all cap directions are positive.
The noncentering also follows because the constant coefficient vector
is independent of the sole degree-zero cardinality kernel.

The rank is greatest among all real original H, even without the cap.
For any such matrix its L is PSD and L1=N1. A full point-star indicator
y_i has y_i'Ly_i=s^2 by intersection support. Expanding shows
(y_i-s1/N)'L(y_i-s1/N)=0. PSD forces each centered star into ker(L).
They are independent: the actual empty coordinate forces the sum of
coefficients zero; singleton coordinates then force each coefficient
zero. Therefore rank(L)<=N-32. This witness attains the absolute bound.

## Least cutoff and prior results

The necessary all-real theorem is
[9471](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_noncentered_growth/PROOF.md),
artifact `bafkreie5bbft5yrw72p4cxr46lgvyc3t5h4abxjcdtbvtmryjpkrvaevsm`.
At n32 its sufficient scalar control is

```
B=sum(a=3..7,a^2*C(32,a))=203204256,
R=s-12*32^2=2147471328, 6B<=R.
```

It forces a positive original proper disjoint entry with both sizes>=8
in every real original capped H. The exact finite obstruction scalar
is -1100363790925849063171/34359738352. Thus S7 and every smaller S_k
are impossible, without an invariance or centering premise. Our S8
witness gives the matching upper bound and proves k_min=8.

[Review9513](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/near-middle-mass-audit/REVIEW.md)
independently confirmed that prior obstruction and strengthened its mass
bound. It gives no verdict on this new n32 certificate; its strengthened
mass constant is not a premise here. The checker also sums the positive
original proper entry mass on every unordered pair with both sizes>=8.
Each class has count C(32,a)*C(32-a,b), halved exactly for a=b. All positive
classes, their actual beta_ab/h entries, and exact total appear in
expected.json; they exceed the credited coarse bound 1/2048 and all
touch layer8. No least-mass or optimum-gap assertion follows.

The n24 sharp-cutoff
[9556 packet](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_n24_sharp_support/PROOF.md)
supplies the complete source pattern, credits and conditioning mechanism.
model.py and exact.py are copied unchanged from there (already unchanged
copies of 9521, based on 9017); affine.py retains the credited9365 decoder
and guard. baseline.py is copied unchanged, with its selected9521 literal,
harmonic and arithmetic functions credited verbatim. fixed32.py adds
the new bounded all-row affine audit and implements the credited8106
ordinary z=1 reference. Earlier structural7578/7627, star9365, positive
9521 and n16 review9123 remain context, not premises from other families
or verdicts on this construction.

The whole published 9556 baseline record was replayed exactly, hash
`f6c98265e472a735b7dfdcdcfe60b84654689131b4b57a77e97307143cf2b5d3`.
The whole published 8106 finite/SOS/partition record was replayed exactly,
hash `b6f21ffc0096f5c7d83a90cf9644c24ad89c93d1095abefe96e793f6d17c0845`.
These are validation, not new research. At n32 its z=1 table has
beta_11=s-(2^30-2), singleton-to-middle beta=1, complementary middle
beta=s-1, and other proper middle entries zero. All17 lower blocks
have the greatest ordinary rank, but U0[1,1]=-31138511967: its cap fails.
The standalone checker reproduces this reference distinction exactly.

## Reproduction and trust boundary

The checker needs only CPython3.12.14 and standard-library integers and
fractions.Fraction. It checks all30 star equations, two exact affine
decoders, every complete lower and upper form, all dimensions and ranks,
actual empty rows/loop and original positive entry classes. Exact PSD
elimination uses positive-pivot congruences; a zero-diagonal residual must
be identically zero. Both PSD algorithms agree. All729 symmetric
ternary3x3 matrices match a separate all-principal-minor criterion,
with24 PSD. Credited n6 controls check both original57-order endpoint
matrices and whole original row/support/star/lower/upper behavior,
including a noncentered repair and empty loop. The literal harmonic
control checks full56-coordinate span, all112 action columns and6272
positions, including above-middle layers and degrees2,3.

Twelve semantic damage controls reject wrong rational data, domain,
support/census, centering metadata, damaged positivity, an actual empty
loop error and forbidden n32 literal allocation. They use active require
checks under python-O. The deterministic whole record is frozen in
expected.json; commands and its hash are in [README.md](README.md).
Ordinary real bridges remain unformalized; independent review of this
extension is pending. Same-author algorithm agreement is not an
independent-person verdict.

Optional CVXPY1.7.4/Clarabel0.11.1 proposed decimal coordinates with
status optimal_inaccurate. Invertible congruences used absolute reference
eigenvalues plus one; the indefinite reference was never assumed capped.
All225 free values were rounded exactly to denominator10^24, then every
defining property was rechecked rationally. No solver output or floating
eigenvalue is a proof input. Fixed1CPU2GiB/native1/one serial mathematical
job and the existing45s guard suffice. No 4294967263-order matrix is
materialized. Timeout, UNKNOWN, memory failure or incomplete search
would establish no mathematical nonexistence.
