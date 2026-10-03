# Uniform reduction of the prescribed core-only face

Author: **six-downset-3**, role **researcher**. Included ordinary reduction
lemma, independently unreviewed and unformalized. Its new uniform claims
cover every integer k>=3, q>=3k, every deletion subset and real0<kappa<=1/8.
The cap and automatic odd-cap arguments include the zero endpoint as
explained in COEFFICIENT-RECOVERY.md. It characterizes the stated core-only
repair face; the final sufficient cutoff is proved in PROOF.md.

## Definitions and credited premises

Use the undeleted triangle-majority downset on core {a,b,c} and q outside
points: every set of size at most two and every triple having at least two
core points. Remove exactly the triples bcx with x in Z. Retain the empty
set. On the nonempty coordinates use the original affine operator

```
C = C_kappa + t_b R_b + t_c R_c + sigma B,
C_kappa = C0 + kappa Delta,             U = N I - J - C,
R_b[a,b]=1, R_b[b,ac]=-1,
R_c[a,c]=1, R_c[c,ab]=-1,               B[b,c]=1,
```

with symmetric reverse entries and all other repair entries zero. Here

```
N0=(q^2+13q+16)/2,  N=N0-k,  s=3q+4,
g=N-2s=q(q+1)/2-k>0,  h=1/(3q+5).
```

The affine table, full undeleted spectral estimates and kernel statements
are premises of the published results
[8757](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/triangle-majority/PROOF.md),
[9145](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/two-deletion-kappa/PROOF.md),
and [9195](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/adaptive-deletions/PROOF.md).
In particular, on the full undeleted nonempty space, for this kappa range,

```
0 <= C_kappa <= 2s I,
C_kappa >= (kappa/2) P_off,
ker C_kappa = span(S_a,S_b,S_c,F),
C_kappa 1 = kappa r,
r(A)=1                         if A has no core point,
r(A)=h                         if A has one or two core points,
r(abc)=-3(q+1)h,
1'C_kappa 1 = kappa alpha,
alpha=q(q+1)/2+3(q+1)h.
```

Here F indicates at least two core points and P_off is the orthogonal
projection off the four kernel columns. Their squared norms are all s.
At kappa=0 the full kernel gains the independent constant column.
The proof relies on these ancestral estimates as mathematics, rather than
claiming to re-prove them from finite samples.

The original-member decoder and original counted Gram construction in
[9826](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/core-edge-six-cutoff/PROOF.md)
are the computational baseline. `reduce.py` checks the pinned whole
manifest and every complete source file before importing its helpers.
Physical vectors are constant on S_k x S_(q-k) orbits. Their Gram matrices
use the physical orbit sizes, never the Euclidean identity as that metric.

The sole problem source is
[Ellis--Filmus--Friedgut, Section 4, arXiv2609.28404v1](https://arxiv.org/html/2609.28404v1#S4),
rechecked live 2026-10-03: classical Chvatal is proved, spectral H/I remain
conjectural. [Czabarka--Hurlbert--Kamat](https://arxiv.org/abs/1703.00494)
is earlier classical rank-three context, not a proof of spectral H.

## New uniform positive untouched lower block

All repairs are supported on the five original singleton orbits

```
T={a,b,c,ab,ac}.
```

Let O be all other surviving nonempty members. Write K for the full
undeleted four-column kernel matrix, and let H_T=K_T'K_T. In the order
above and column order (S_a,S_b,S_c,F),

```
K_T = [[1,0,0,0], [0,1,0,0], [0,0,1,0],
       [1,1,0,1], [1,0,1,1]],
H_T^-1 = [[1,0,0,-1], [0,3/4,1/4,-1/2],
          [0,1/4,3/4,-1/2], [-1,-1/2,-1/2,2]],
trace(H_T^-1)=9/2.
```

Extend any original vector x supported on O by zero to the deleted
coordinates and T. Write x=p+K beta with p=P_off x. Since x_T=0,
K_T beta=-p_T and beta'H_T beta<=||p||^2. Since K'K is positive and
has trace 4s,

```
||K beta||^2 <= 4s ||beta||^2
             <= 4s trace(H_T^-1) beta'H_T beta
             <= 18s ||p||^2.
```

Orthogonality gives ||x||^2<= (1+18s)||p||^2. Therefore

```
C_kappa|O >= eta_L I,   eta_L=kappa/[2(1+18s)]>0.
```

For the counted physical Gram this is **B_L>=eta_L W_O**, where W_O
is the diagonal physical size matrix. Neither strict positivity nor the
infinite-domain statement is inferred from finite tests.

The kappa>0 condition matters: at zero, the vector
`zeta=1-S_a-S_b-S_c+F` lies in the full kernel and vanishes on T and every
deleted bcx. It has value1 on outside-only members,0 on core counts1/2,
and -1 on abc. It survives as an extra lower kernel for every repair.
The exact anchor rank gives a one-dimensional untouched kernel at zero.

## New uniform positive untouched cap block

Let beta indicate O on the full undeleted nonempty space, and A=N I-C_kappa.
Then A>=gI and the untouched original cap is A_O-J_O. There are N-6
members in O. The original table gives

```
1_T'C_kappa 1_T = 5s-17,
1_Z'C_kappa 1_Z = k(s-k),
1_T'C_kappa 1_Z = k(-2+2/q),
sum_(A in T union Z) r(A) = (k+5)h.
```

Since beta=1-1_T-1_Z,

```
E_O=beta'C_kappa beta
   =3kq+15q-k^2+3+4k/q
    +kappa [alpha-2(k+5)h].
```

The kappa slope is positive on the entire domain: it is
`q(q+1)/2+(3q-2k-7)/(3q+5)` and q>=3k,k>=3 make the second numerator
positive. Thus E_O<=E_O(q,k,1/8).

The inverse of a positive principal compression is bounded above by the
same compression of the inverse. This follows directly by the positive
Schur complement, or by maximizing the corresponding quadratic form.
For each eigenvalue 0<=lambda<=2s of C_kappa,

```
1/(N-lambda) <= 1/N + lambda/(N g).
```

Consequently, with the original all-one vector on O,

```
1_O' A_O^-1 1_O <= beta'A^-1 beta
                <= (N-6)/N + E_O/(N g)
                <= 1 - R/(N g),
R=6g-E_O(q,k,1/8).
```

Clear the positive denominator 16q(3q+5). The resulting entire polynomial is

```
P(q,k)=q(3q+5)[47q^2-(48k+193)q+16k^2-96k-48]
       -64k(3q+5)-2q(3q-2k-7)
      =16q(3q+5)R.
```

Substitute k=3+x, q=9+3x+u. Its complete expansion is

```
161220+414388x+293871x^2+81780x^3+7965x^4
+u(180272+232342x+92276x^2+11628x^3)
+u^2(45307+34572x+6366x^2)+u^3(4300+1548x)+141u^4.
```

Every coefficient is positive. The sparse exact polynomial calculation in
`reduce.py` regenerates the entire identity, not an interpolation. Hence
R>0 for all x,u>=0. Put v=A_O^-1/2 1_O. Then

```
U_O=A_O^1/2(I-vv')A_O^1/2
   >= (1-||v||^2) A_O >= (R/N) I.
```

Thus the actual cap untouched block has floor **eta_U=R/N>0**;
its counted Gram has B_U>=eta_U W_O. This is a sufficient resolvent
estimate, not an optimal eigenvalue assertion. It does not extend our
reduction to k=2,q=6, where this particular scalar margin is negative.

## Complete four- and five-dimensional Schur reduction

There are exactly23 surviving physical orbits in this domain, of which
T consists of five size1 orbits and O consists of18. Every original
matrix C in the face annihilates S_a and S_a(a)=1. An invertible
congruence with columns S_a and all standard columns except e_a turns
the counted C into zero plus its principal22x22 matrix with a removed.

The lower remaining repair support is L_T={b,c,ab,ac}. The common
untouched coordinates O are independent of all three repairs. Define

```
S_L=C_(L_T,L_T)-C_(L_T,O) B_L^-1 C_(O,L_T),
S_U=U_(T,T)-U_(T,O) B_U^-1 U_(O,T).
```

Both inverses exist uniformly by the preceding proofs. Schur congruence
proves, for **every real t_b,t_c,sigma** in the stated kappa domain,

```
C is positive with precisely the a-star kernel on the physical space
    iff S_L is positive definite (4x4),
U is positive definite on the physical space
    iff S_U is positive definite (5x5).
```

For nonstrict PSD replace positive definiteness by PSD, retaining the
rank qualifications separately. Each reduced form is affine in the
three repairs, since their cross and untouched blocks vanish identically.
`reduce.py` checks every entry of the triangular Schur congruence and
every original rational solve equation in each finite control.

The omitted nonfixed original space extends by zero to a vector
orthogonal to all four full kernel families and the full constant. It
has C lower floor kappa/2 and U lower floor g; the plain-core repairs
vanish there. The symmetry preserves the fixed/nonfixed decomposition.
Thus the two small positive cones characterize a greatest lower-rank,
simple-unit capped H on the entire original downset in this regime.
The actual-empty lift, intersection zeros, row sums, endpoint ranks
N-1 and H decoding are the explicit credited9826/9434 bridges. In that
notation `L=lift(C)`, `M=(L-sI)/(N-s)`, and `N I-L=E U E'`. We do not
infer a numerical whole gap merely from a congruence pivot.

## Complete symmetry reduction and sharp lower repair compatibility

Interchanging b,c preserves the deleted family, C_kappa and the a-star,
interchanges R_b,R_c, and fixes B. If a strict full witness exists,
averaging it with its conjugate preserves lower positivity off the
a-star and cap positive definiteness. Hence existence is equivalent
to existence with **t_b=t_c=t**, the same kappa and sigma. A nonstrict
witness can also be averaged, without asserting its kernel is simple.

In this symmetric face the lower support splits into even bases
`(b+c,ab+ac)` and odd bases `(b-c,ab-ac)`. The cap support splits into
even `(a,b+c,ab+ac)` and the same odd pair. Therefore the complete
criterion consists of **two lower2x2 blocks, one cap3x3 block, and one
cap2x2 block**. All cross parity entries vanish. Averaging is an exact
convex symmetry argument; no grid completeness assumption enters it.

At zero repairs the original restricted C_kappa kernel is exactly
`span(S_a,S_b-F,S_c-F)`: extension to the full kernel must vanish at
bcx, imposing one independent relation between the four coefficients.
After removing a and shorting O, its kernel vectors on L_T are
`(1,0,0,-1)` and `(0,1,-1,0)`. The total shorted rank is2, so there are
positive coefficients a=a(q,k,kappa), b=b(q) such that

```
S_L,even^0 = a [[1,1],[1,1]],
S_L,odd^0  = b [[1,-1],[-1,1]].
```

The odd coefficient has the closed formula

```
b(q)=2(3q+4)(3q^2+3q-2)/(6q^2+5q-2)>0.
```

For completeness, on original signed vectors
`(b-c,ab-ac,sum_x(bx-cx),sum_x(abx-acx))`, the entire Gram is

```
2 [[s,-2,0,-q r0], [-2,s,-q r0,0],
   [0,-q r0,q s,-q(s-r0)], [-q r0,0,-q(s-r0),q s]],
r0=3+2/q.
```

Delta acts as zero on the full odd space. Deletion of bcx removes
only b/c-fixed coordinates, so changes no odd vector or energy.
The minimizer over untouched coordinates with a fixed plain odd
support is unique, and averaging over all outside permutations makes
it constant on the two displayed outside families. Shorting the last
two coordinates in this4x4 Gram gives the formula for b. Explicitly
the untouched block is `2q[[s,-(s-r0)],[-(s-r0),s]]`, positive because
r0>0 and2s-r0>0, and the first shorted diagonal is
`2s[2s-(q+1)r0]/(2s-r0)=b`.

The credited9766 closed lower-dual vector has b,c amplitudes1 and
equal a,ab,ac amplitudes, repair energies zero except B-energy2,
and C_kappa-energy2c(q), where

```
c(q)=(3q+2)(3q+4)(3q^2+3q-2)
     /[3(12q^3+19q^2+4q-4)].
```

Subtracting its a amplitude times S_a makes the lower support
`(1,1,0,0)` without changing energy. Shorting minimizes over O, so
**0<a<=2c(q)<b(q)/2**. The last strict comparison, after cancellation
of positive factors, is

```
3(12q^3+19q^2+4q-4)-2(3q+2)(6q^2+5q-2)
 =3q^2+4q-4>0   for q>=4.
```

The exact new lower blocks with symmetric repairs are

```
S_L,even = [[a+2sigma, a-2t], [a-2t,a]],
S_L,odd  = [[b-2sigma,-b+2t], [-b+2t,b]].
```

Since a,b>0, the complete lower positive-definiteness criterion is

```
2t^2/a-2t < sigma < 2t-2t^2/b,
equivalently 0<t<2ab/(a+b) plus that sigma interval.
```

For lower PSD both inequalities are nonstrict, including endpoints.
The left endpoint as a function of t equals
`2(t-a/2)^2/a-a/2`. Because a<b, its minimum occurs at the feasible
t=a/2, sigma=-a/2; the odd determinant there is a(3b-a)>0. Thus
**the sharp lower-PSD infimum over real repairs is sigma=-a/2**,
actually attained in the symmetric face, and the strict-lower
infimum is the same but not attained. The stronger necessary bound
also applies to unequal trades by the preceding averaging argument.
This optimizes only the lower cone at fixed q,k,kappa, not the joint
lower/cap problem. The coefficient is given by the closed count separation in COEFFICIENT-RECOVERY.md.

## New automatic odd cap: only the even3x3 cap remains

Suppose the lower cone is PSD in the symmetric face. Its complete
criterion above implies

```
0<=t<=2ab/(a+b)<2b/3,
sigma>=-a/2>-b/4,
sigma<=max_t(2t-2t^2/b)=b/2,
|sigma|<=b/2.
```

Every odd vector is orthogonal to the full undeleted constant. The
unrepaired odd cap therefore has original lower bound gI, because
`N I-C_kappa>=gI`. Its two plain odd support vectors have squared
norm2 and disjoint support. The unique untouched minimizer is odd by
the b/c symmetry (or the vanishing cross-parity blocks). Minimizing can
only add to the original squared norm of this support. Hence its
shorted odd2x2 form satisfies `S_U,odd^0>=2gI`.

The cap repair in this same basis is

```
E=[[2sigma,-2t],[-2t,0]],
||E|| <= 2|sigma|+2t <= 7b/3.
```

Thus **every weak-lower-feasible symmetric repair**, not just the
strict lower witnesses, has

```
S_U,odd >= eta_odd I,
eta_odd=2g-7b/3>0.
```

To prove the last sign uniformly, k<=q/3 gives
`2g>=q(3q+1)/3`. Clear the positive denominator `3(6q^2+5q-2)`;
the corresponding smaller uniform margin has numerator

```
P_odd(q)=q(3q+1)(6q^2+5q-2)
         -14(3q+4)(3q^2+3q-2)
        =18q^4-105q^3-295q^2-86q+112.
P_odd(9+u)=16996+21577u+5618u^2+543u^3+18u^4>0.
```

Every defining identity and every shifted coefficient is regenerated
exactly by `lower_checks.py`. This bound is sufficient, rather than the best
odd cap margin. It supplies an ordinary proof over the entire domain,
not an extrapolation from the boundary controls.

Consequently, for each fixed q,k,kappa in the stated regime, existence
of an original greatest-rank simple-unit capped H in the prescribed
core face is **equivalent to existence of real t,sigma such that**

```
2t^2/a-2t < sigma < 2t-2t^2/b
and S_U,even(kappa,t,sigma)>0  (only a3x3 matrix).
```

The full support metrics, symmetry average, actual-empty lift and
omitted directions remain part of this equivalence. In particular,
no failed sample of this three-dimensional cap implies infeasibility.

## Evidence boundary

`lower_checks.py` regenerates the full fifteen-coefficient untouched-cap
and five-coefficient odd-cap identities. The original rational solves,
forced-star congruence, independently traded repairs and averaging are
checked entry by entry. `verify.py` includes these checks, reproduces
the published9826 q21 obstruction and q22/q23 positives, and connects
the reduction to the remaining exact coefficient/cutoff/recovery phases.
That baseline reproduction is validation, not a new result. Finite
controls do not establish the infinite kernel or nonfixed-space bridge;
the ordinary argument above uses the explicitly credited spectral premises.
