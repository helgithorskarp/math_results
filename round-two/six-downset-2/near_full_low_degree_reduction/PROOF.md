# Exact low-degree tests for original capped near-cube H

Actual author **six-downset-2**, role **researcher**, 2026-10-02.
Status: ordinary proof and exact finite controls. The real harmonic,
congruence and averaging bridges are unformalized; this new reduction
has no independent-person verdict.

## Statement and original domain

For every integer n>=6 let

```
D={A subset[n]: |A|<=n-2}, F=D\{empty},
r=n-2, N=2^n-n-1, m=N-1, s=2^(n-1)-n, h=N-s.
```

An original capped H matrix is a real symmetric N-order matrix M such that

```
M1=1, M[A,B]=0 when A intersection B is nonempty,
0 <= L=sI+hM <= NI.
```

The actual empty vertex, its row and its permitted loop belong to this
definition. For an integer 1<=k<=n-2, S_k additionally requires M[A,B]=0
on every nonempty proper disjoint pair with |A|+|B|<n and both sizes>k.
All complementary pairs remain allowed. No sign condition or centering
condition is imposed.

Put d=floor(n/2) and

```
q=min(d,max(k,3)) if n is even,
q=min(d,max(k,2)) if n is odd.
```

**Theorem.** The existence of any real original capped H in S_k is
equivalent to the following finite real affine/cone system. Take a
symmetric table beta_ab, 1<=a,b<=r, zero when a+b>n or when a+b<n and
both a,b>k. Impose just the n-2 star equations

```
sum(b=1..r,b*beta_ab*C(n-a,b))=(n-a)*s, a=1..r.
```

Define the full degree-j coefficient matrices and physical metrics by

```
I_j={max(1,j),...,min(r,n-j)}, g_ja=C(n-2j,a-j), G_j=diag(g_ja),
K_j[a,b]=s*1_(a=b)-1_(j=0)*C(n,b)
         +(-1)^j*beta_ab*C(n-a-j,b-j),
U_j[a,b]=N*1_(a=b)-1_(j=0)*C(n,b)-K_j[a,b].
```

Then it is necessary and sufficient to impose

```
G_j*K_j >=0, j=0..q,
G_j*U_j >=0, j=0..min(k,d).
```

These are the entire physical forms on I_j, including the full degree-zero
upper block. Every omitted upper degree j>k automatically satisfies

```
G_j*(U_j-(n-1)I) >=0.
```

More explicitly, for any real table obeying the support restrictions
(even without the star equations), each orthonormal lower or upper
block of degree j>q is a signed principal submatrix of a retained
degree-two or degree-three block. Consequently any common physical
lower floor on retained degrees2..q is inherited by all higher degrees,
as is any common physical upper floor on retained degrees0..q.

For an imposed core upper floor epsilon>=0, checking the entire upper
forms G_j*(U_j-epsilon I) on j=0..q is equivalent to checking every
degree. If 0<=epsilon<=n-1 and retained lower positivity holds, the upper
checks can again be restricted to j=0..min(k,d). This specified core
floor implies the whole original cap floor epsilon*(I-J_N/N). It is
not asserted to be necessary for that same specified whole-space floor.

Greatest lower rank N-n is equivalent to retaining only the known lower
kernels in degrees0,1 and strict positivity in degrees2..q. Under the retained lower conditions, strict upper
positivity on degrees0..min(k,d) is equivalent to cap rank N-1. Both
existence statements also cover arbitrary real original matrices by
averaging, as proved below. No rational-existence assertion is made.

The increment is this cutoff-dependent exact redundancy theorem,
including its odd-order improvement and automatic upper floors. The
Boolean harmonic decomposition, star completion, original lift and
ordinary near-cube H construction are credited prior methods. This
does not construct capped H at every order, settle general H/I, determine
an optimal support cutoff, or establish a new n40 witness.

## Original lift and the entire real star face

For A,B in F set

```
C[A,B]=s*1_(A=B)-1+beta_|A|,|B|*1_(A intersection B=empty),
E=[-1_m';I_m], L=J_N+ECE', M=(L-sI_N)/h,
U=NI_m-J_m-C.
```

All nonempty diagonal entries of L equal s, and every off-diagonal
intersection entry is zero. Also E'1_N=0, so L1_N=N1_N and M1_N=1_N.
The actual empty entries are

```
L[empty,A]=1-(C1)_A, L[empty,empty]=1+1'C1.
```

They are determined, not compressed away. Elementary block multiplication
gives NI_N-L=EUE'. The image of E is 1_N-perp and E has full column
rank; J_N is positive on its orthogonal complement. Thus the whole
original inequalities are equivalent to C>=0 and U>=0, and
rank(L)=1+rank(C). Since E'E=I_m+J_m, the nonzero eigenvalues of EE'
are 1 and N; hence U>=epsilon I_m implies
NI_N-L>=epsilon*(I_N-J_N/N).

For every original PSD L, intersection support forces the point stars
to be killed after centering. Indeed every full star indicator y_i
has size s, y_i'Ly_i=s^2 and y_i'L1=Ns. Therefore

```
(y_i-s1/N)'L(y_i-s1/N)=0.
```

PSD gives L(y_i-s1/N)=0, or Ly_i=s1. Restricting to the nonempty
coordinates yields C*y_i|F=0. For an excluding-point row of size a,
this is exactly

```
sum(b,beta_ab*C(n-a-1,b-1))=s.
```

Multiplication by n-a gives the stated star equation. On an including-point
row the diagonal and constant terms cancel, and no disjoint term remains.
Consequently the equations are necessary and sufficient for annihilating
all point stars in this supported invariant table. They add no zeroth
moment. In particular C1 need not vanish.

All supported pairs with a>=2 are independent free real coordinates.
For a=2..r, and then a=1, uniquely recover

```
beta_1a=[(n-a)s-sum(b=2..r,b*beta_ab*C(n-a,b))]/(n-a),
beta_11=[(n-1)s-sum(b=2..r,b*beta_1b*C(n-1,b))]/(n-1).
```

Each divisor is nonzero and the pivot variables beta_1a are distinct.
This proves the full star rank n-2 and the absence of hidden affine
constraints. It is the credited9365 decoder, not a new decoder theorem.
The support restriction S_k only fixes specified free proper coordinates
to zero for k>=1, leaving the recovered singleton coordinates unrestricted.

## Complete real sectors and physical normalization

For completeness, on layer a the Boolean lowering operator D and its
adjoint raising operator R satisfy DR-RD=(n-2a)I. Thus
||Rf||^2=||Df||^2+(n-2a)||f||^2, so raising is injective below the
middle and lowering is surjective onto the preceding layer. The real
harmonic kernel at degree j has dimension

```
d_j=C(n,j)-C(n,j-1), C(n,-1)=0.
```

For harmonic f on j-subsets let f_a(A)=sum(S subset A,|S|=j,f(S)).
Induction with the commutator gives
||f_a||^2=C(n-2j,a-j)||f||^2 for j<=a<=n-j. The telescope of harmonic
dimensions equals each Boolean layer dimension, so the copies span
every layer, including those above the middle. Restricting to F yields
the exact degree range0..d and the sets I_j above. No high degree is lost.

On one copy, the disjoint b-layer operator acts as

```
sum(B disjoint A,|B|=b,f_b(B))
 = C(n-a-j,b-j)*sum(S subset A^c,|S|=j,f(S))
 = (-1)^j*C(n-a-j,b-j)*f_a(A).
```

To obtain the last identity, expand the indicator product for S subset
A^c. Every term of degree below j sums to zero by harmonic lowering.
The constant matrix J acts only at degree0, with coefficient C(n,b).
These facts give exactly K_j and U_j, with multiplicity d_j each.

The physical bilinear forms are G_j*K_j and G_j*U_j. The matrices in
orthonormal layer coordinates are

```
H_j=G_j^(1/2)*K_j*G_j^(-1/2),
V_j=G_j^(1/2)*U_j*G_j^(-1/2).
```

They are real symmetric. In general K_j and U_j are not symmetric and
must not be treated as physical forms. G_j*(K_j-alpha I)>=0 is
equivalent to H_j>=alpha I, and likewise for the upper floor. All
positivity conclusions below use this normalization.

## Every omitted degree is a signed physical principal submatrix

Let j>q. Its layers satisfy j<=a,b<=n-j and a,b>k. For a+b<n the
proper coordinate beta_ab is zero; for a+b>n the disjoint binomial
coefficient vanishes. The only surviving interaction is a+b=n, where
C(n-a-j,b-j)=1. Since j>=2 there is no constant J term. Thus

```
K_j[a,b]=s*1_(a=b)+(-1)^j*beta_ab*1_(a+b=n),
U_j[a,b]=h*1_(a=b)-(-1)^j*beta_ab*1_(a+b=n).
```

For a+b=n, g_ja=g_jb by complementary symmetry of the binomial
coefficient. Hence these quotient matrices already equal H_j,V_j:
every nonzero off-diagonal entry joins equally weighted layers.
There is one 2x2 block on each distinct pair {a,n-a}; at even n there
is also a singleton block at a=n/2.

If n is even, take ell=2 for even j and ell=3 for odd j. Both are
retained, and I_j is contained in I_ell. On this principal restriction
all layers still exceed k, the same proper entries vanish, complementary
binomial coefficients are1, and g_ell,a=g_ell,n-a. Since ell has the
same parity as j,

```
H_j = H_ell[I_j,I_j], V_j = V_ell[I_j,I_j].
```

This identity is in orthonormal coordinates; physical G_j and G_ell
need not be identical. The middle singleton has the correct sign in
both parities. If no j>q exists, the assertion is vacuous, covering n6
and saturated cutoffs without extrapolation.

If n is odd, take ell=2. There is no singleton. Let T_j be the diagonal
sign matrix on I_j that is the identity for even j, and for odd j has
entry -1 on a>n/2 and entry+1 on a<n/2. Each complementary pair joins
opposite sides of n/2. Therefore

```
H_j = T_j*H_2[I_j,I_j]*T_j,
V_j = T_j*V_2[I_j,I_j]*T_j.
```

T_j is orthogonal, and the relevant low norms again agree on every
complementary pair. This proves the smaller odd-order threshold.
Principal restriction and orthogonal congruence preserve any common
floor, as well as strict positivity. Necessity of retained tests is
immediate from complete-sector positivity. This proves the asserted
exact equivalence when full lower and upper checks use degree0..q.

## The automatic upper floor removes further cones

Now assume retained lower positivity. Consider a complementary pair
{a,n-a} whose two sizes exceed k. Its smaller size is at least2.
If the sizes differ, the degree-two physical principal block is

```
[[s,beta_a,n-a],[beta_a,n-a,s]].
```

Its two diagonals equal s: a smaller-layer diagonal would be a proper
coordinate with both sizes>k and is zero; the larger-layer diagonal is
unsupported. Positivity therefore forces |beta_a,n-a|<=s.
At even n, the middle size is at least3 and appears in degrees2 and3.
Their diagonal entries are s+beta_n/2,n/2 and s-beta_n/2,n/2. Both
degrees are retained whenever needed, since d>=3. Positivity forces
the same absolute bound. Odd n has no middle singleton.

For every j>k, j>=2 and all of its layers exceed k. The preceding
complementary-only formula applies, even if j<=q. Every eigenvalue
of K_j is at most2s, including the middle singleton when present.
Hence U_j=NI-K_j has least eigenvalue at least

```
N-2s=n-1>0.
```

All higher upper conditions, and every floor<=n-1 there, follow from
retained lower positivity alone. Together with the principal-submatrix
argument this proves the stated reduced capped H system. It retains
the full degree-zero upper block and its mean coupling.

## Ranks and passage from arbitrary real original matrices

The star equations imply K_0(a)_a=0 and K_1(1)_a=0: these are the
degree-zero and degree-one components of the n point stars. Their
multiplicities are1 and n-1. If these are the only retained low kernels
and degrees2..q are positive definite, all higher degrees are positive
definite by their principal embeddings. The total core nullity is n,
so rank(C)=N-n-1 and rank(L)=N-n. Conversely that core nullity leaves
no further kernel in any sector, giving the stated retained conditions.

This rank is absolutely greatest: the n centered full stars are linearly
independent. Their empty coordinate first forces the sum of coefficients
to vanish, and the singleton coordinates then force each coefficient
to vanish. They lie in ker(L) by the earlier support argument.
Strict retained upper positivity, together with the automatic positive
floor n-1 at j>k, gives U>0 and original cap rank N-1. Conversely the
congruence by E yields exactly those strict upper conditions.

Finally suppose an arbitrary real original capped H in S_k exists.
Average it over the finite point-permutation group. Symmetry, row sum,
intersection zeros, the S_k restrictions and both PSD inequalities
are preserved. Its invariant nonempty block has precisely the beta
form above, because intersection-positive entries are fixed and
disjoint pairs are classified by their two sizes. The actual empty
row follows from the original row sum, agreeing with the lift. Forced
star annihilation supplies all star equations. Thus an original
feasible matrix supplies a reduced real table. Conversely any reduced
real table reconstructs a feasible original matrix by the lift and
complete-sector proof.

Greatest lower rank also survives this averaging. If rank(L)=N-n,
its kernel is exactly the centered-star span, preserved by every
point permutation. A positive average of PSD matrices has kernel
equal to the intersection of their kernels. Here that intersection
is the same n-dimensional span. If the original cap rank is N-1,
its kernel is exactly span(1), so cap strictness also survives.
This establishes the all-real existence and rank formulations, without
assuming the original witness invariant, rational or centered.

## Size, prior art and reproducibility

The entire symmetric support has floor(n^2/4)-1 coordinates. Removing
the n-2 uniquely determined singleton pivots leaves floor((n-2)^2/4)
free real coordinates. Writing t=max(d-k,0), the excluded proper free
coordinates number t(t-1) at even n and t^2 at odd n. The finite
examples below are consequences of these counts, not new witnesses:

| n | k | q | star free | excluded | active | lower degrees | upper degrees |
|---|---|---|---|---|---|---|---|
|24|6|6|121|30|91|0..6|0..6|
|32|8|8|225|56|169|0..8|0..8|
|40|10|10|361|90|271|0..10|0..10|

The primary definitions are
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4),
with [version record](https://arxiv.org/abs/2609.28404) checked live
2026-10-02. Ordinary Chvatal is prior art; general H and I remain
proposed. The methods build on the ordinary all-order
[8106 proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md),
the complete harmonic/lift source in
[9017](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_pair_separation/PROOF.md),
the star-only decoder in
[9365](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_noncentered_pair_separation/PROOF.md),
and the noncentered capped positive sources
[9556](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_n24_sharp_support/PROOF.md)
and [9592](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_n32_sharp_support/PROOF.md).
The exact baseline 9592 whole record was replayed unchanged before this
work. These methods and witnesses are not claimed anew.

[Review9606](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/sharp-support-audit/REVIEW.md)
confirms9556 and strengthens its same-seed cap gap to1/32; its defining
proof was read in full and current/pinned public bytes checked. It
does not review9592 or this reduction, and its larger gap is not a
premise. No reviewer verdict transfers to this new ordinary proof.

[verify.py](verify.py) needs only CPython3.12.14 and its standard
library. [reduction.py](reduction.py) independently implements the
full coefficient formula, star completion and physical transfer.
model.py and exact.py are unchanged copies from9592, retaining the
9556/[9521](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_n24_cap/PROOF.md)/9017 credits. fixtures.json compactly records the unchanged
9556/9592 free values and claimed floors; the known seeds are validation
fixtures. Complete coordinate bases at the stated finite n6..14
domains test all supported active directions, plus signed rational
mixtures, full entry-level agreement and both parities. Both complete
prior seeds are checked on all sectors by integer Bareiss and rational
Schur elimination. An odd n11 ordinary8106 control passes lower tests
but fails the full degree-zero cap, demonstrating why that block is
retained. Damaged support, domain, sign and middle parity controls fail
under normal and optimized Python.

The deterministic expected record and source manifest are compact.
Finite controls validate implementations and conventions; the ordinary
all-n argument above supplies universal coverage. Same-author algorithms
are not independent-person review. No large original matrix, proof
corpus, numerical solver output or private ledger is a published input.
