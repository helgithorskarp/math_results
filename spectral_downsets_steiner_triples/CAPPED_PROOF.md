# Capped certificates for every Steiner triple downset

Author: **six-downset-2**, role **researcher**, 2026-09-30.
This is a written mathematical proof, with exact rational checks of examples;
it is not a proof-assistant formalization or an independent review.
[The separate review by six-reviewer-1](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_steiner_triples_review1/REVIEW.md)
confirms this single-system theorem and gives additional exact uniform evidence.
The order convention below is explicit as suggested there.

## 1. The theorem and the formula

Let T be any Steiner triple system on v>=3 points: every pair occurs in exactly
one triple. Its generated downset D contains the empty set, all singletons,
all pairs and the triples of T. Put

```
r=(v-1)/2, b=v(v-1)/6, e=3b,
s=v+r=(3v-1)/2,
N=1+v+e+b=(2v^2+v+3)/3.
```

**Theorem.** Every such downset has a rational symmetric matrix M satisfying

```
M 1=1,   M[A,B]=0 when A intersects B,
-s/(N-s) I <= M <= I.
```

For v>=7 the construction below has rank((N-s)M+sI)=4b, and the eigenvalue
1 of M is simple. The lower endpoint has multiplicity v+1. The case v=3 is
the full Boolean cube, with the complement-permutation certificate.

For v>=7, define

```
h=(v+3)/(v-3),
w=1+(v+3)/((v-3)(v-2)),
beta=-5/(v-2)=w-h.
```

Construct Q as follows. All nonempty diagonal entries equal s; all distinct
intersecting entries are zero. Every entry involving the empty set equals 1,
including its diagonal. On distinct disjoint nonempty sets use:

| Sizes of A,B | Q[A,B] |
|---|---:|
| 1,1 | 0 |
| 1,2 with A union B in T | beta |
| 1,2 with A union B not in T | w |
| 2,2 | w |
| 1,3 or 2,3 | h |
| 3,3 | 1 |

Then M=(Q-sI)/(N-s). Signed entries are permitted by Conjecture H. In
particular the negative singleton/pair weight beta causes no support issue.
The proof is independent of the system's automorphisms or isomorphism type.

## 2. Incidence identities and the core

Let P be the e by v pair/point incidence matrix, B the b by v triple/point
incidence matrix, and R the e by b pair/triple containment matrix. Let T_0
be the e by v matrix recording the unique completing point of each pair.
Counting inside each triple gives

```
P^T P=(v-2)I+J,      B^T B=(r-1)I+J,
R^T R=3I,           P^T R=2B^T,
T_0=RB-P,           T_0^T P=J-I.
```

For example, for two distinct points i,j there is exactly one pair containing
j whose completing point is i, which proves the last identity. Also
P1=2*1, B1=3*1, P^T1=2r*1, B^T1=r*1, R1=1 and R^T1=3*1.

Order the nonempty vertices by points, pairs, triples. The matrix
C=Q_nonempty-J has the following blocks; every J has the indicated dimensions:

```
C11=sI-J,
C12=(w-1)J-wP^T-hT_0^T,
C13=(h-1)J-hB^T,
C22=(s+w)I-wPP^T+(w-1)J,
C23=(h-1)J-hPB^T+hR,
C33=(s+2)I-BB^T.
```

The pair/triple disjointness indicator is J-PB^T+R: an intersecting pair
has intersection size one or two, and R corrects exactly the latter case.
The triple disjointness indicator is J+2I-BB^T. These facts verify the
displayed blocks directly from the entry table.

The two scalar identities

```
s=w(v-2)+h(r-2),       h(v-3)=v+3
```

and the incidence identities give

```
C [ I_v ; P ; B ]=0.                                  (1)
```

One can check (1) without a PSD assumption: C12 P+C13 B=-C11,
C22 P+C23 B=-C21 and C32 P+C33 B=-C31. Thus, with K the pair/triple
principal block of C,

```
F=[ -P^T  -B^T ; I_e  0 ; 0  I_b ],
C=F K F^T.                                           (2)
```

The bottom rows of F form an identity matrix, so PSD and rank of K transfer
to C, with equal ranks. This avoids any inverse of a singular core.

## 3. An orthogonal decomposition, with fixed-size blocks

Let U be the centered point space 1_v-perpendicular. Put p=v-2 and t=r-1.
The pair space decomposes orthogonally into:

```
the constant vector;
P U and V U, where V=RB-(2t/p)P;
R ker(B^T);
W=ker(P^T) intersect ker(R^T).
```

Here P^T V=0 and V^T V=(tv/p)I on U. Also
dim ker(B^T)=b-v and dim W=2b-v+1. Indeed P and B have full column rank,
the incidence identities prove orthogonality, and the dimensions add to e.
The triple space is the orthogonal sum of its constants, B U and ker(B^T).
All these spaces, coupled as below, are invariant for C and K.

**Constant levels.** In normalized constant directions, C is

```
[ r           -2 sqrt(r)    sqrt(3r) ]
[ -2 sqrt(r)   4            -2 sqrt(3)]
[ sqrt(3r)    -2 sqrt(3)     3        ]
= (sqrt(r),-2,sqrt(3)) (sqrt(r),-2,sqrt(3))^T.
```

It is PSD of rank one, with eigenvalue r+7. The vector of level sizes is
annihilated, since sqrt(rv)-2sqrt(e)+sqrt(3b)=0. Consequently C1=0.
The constant-level block of K is [[4,-2sqrt(3)],[-2sqrt(3),3]], also
PSD of rank one.

**Centered point directions.** Choose any orthonormal basis of U. For each
basis vector u, use the normalized pair directions Pu/sqrt(p),
Vu/sqrt(tv/p), and triple direction Bu/sqrt(t). The block of K is

```
[ alpha   0       -h(v-4)sqrt(t/p) ]
[ 0       delta    h sqrt(v/p)     ]
[ -h(v-4)sqrt(t/p)  h sqrt(v/p)    v+3 ]
```

where

```
alpha=s-w(v-3)=(v^2+v-16)/(2(v-2)),
delta=s+w.
```

For v>=7, alpha>=4 and delta>=10. Its final Schur complement equals

```
v+3 - (v+3)^2(v-4)^2/((v-3)(v^2+v-16))
    - h^2 v/((v-2)delta).                            (3)
```

The first subtracted term is

```
v - 4(v^2+6v-36)/((v-3)(v^2+v-16)) < v.
```

The second is at most (25/4)*(7/5)/10=7/8, since h<=5/2 and
v/(v-2)<=7/5. Thus (3)>17/8>0. Each of these v-1 blocks is positive
definite. Through (2), the full centered block of C has rank three on
four level directions, the missing direction being the star vector.

**Centered triple kernel.** For z in ker(B^T), use Rz/sqrt(3) and z.
The block of C and K is

```
[ delta     sqrt(3)h ]
[ sqrt(3)h  s+2     ].
```

It is positive definite: delta(s+2)>=120 while 3h^2<=75/4.
There are b-v such blocks (zero of them for v=7).

**Remaining pair directions.** On W, C and K equal delta I, strictly
positive. There are 2b-v+1 such directions.

This proves C>=0 and

```
rank C=1+3(v-1)+2(b-v)+(2b-v+1)=4b-1.                (4)
```

## 4. The upper bound and the empty vertex

We prove C<N I on its positive eigenspaces using the same decomposition.
The constant eigenvalue is r+7=(v+13)/2<N. The remaining-pair eigenvalue
delta<= (3v+2)/2<N. The triple-kernel block has trace
2s+w+2<=3v+5/2<N, hence both of its eigenvalues are below N.
These inequalities follow immediately from N=(2v^2+v+3)/3 and v>=7.

The full centered-point block of C is PSD, so its largest eigenvalue is
bounded by its trace

```
L=s+alpha+delta+(v+3)
 =(11v+3)/2-(v-4)w.
```

At v=7, L=71/2<36=N. For every integer v>=8,

```
N-(11v+3)/2=(4v^2-31v-3)/6>0,
```

so L<N there as well. Therefore every eigenvalue of C lies in [0,N).

Extend C to D by a zero empty row and column, obtaining C_bar. Since
C1=0, the claimed matrix is exactly Q=J_N+C_bar, with Q1=N1. Its constant
direction has eigenvalue N. On the centered space, Q equals C_bar. Thus

```
0<=Q<=N I,      rank Q=rank C+1=4b,
rank(N I-Q)=N-1.
```

The entry table gives all support conditions. Normalizing Q proves the
theorem, including the endpoint multiplicities. No numerical eigenvalue,
finite-system classification, or completeness inference enters this proof.

## 5. Products and a separation from partition certificates

Take any finite collection of Steiner triple downsets on disjoint supports,
including order three if desired. Tensor their normalized matrices. Symmetry,
row sums and disjointness support are preserved. Write p_j=s_j/N_j and
rho_j=p_j/(1-p_j). Since p_j<=1/2, every factor spectrum lies in
[-rho_j,1], with rho_j<=1. A negative product eigenvalue has magnitude at
most max_j rho_j. The product downset has

```
N_product=product_j N_j,
s_product=N_product * max_j p_j.
```

Thus the tensor certificate satisfies H and M<=I. This conditional tensor
mechanism is also documented by **six-downset-1**, researcher, in
[its structural proof, Section 5](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).
The substantive input here is the required upper bound for every STS factor.
For k copies of any STS(v) with v>=7, the PSD matrix has rank
N^k-k(v+1): precisely one negative endpoint factor and k-1 factors at their
simple eigenvalue 1 can attain the lower endpoint. Two or more negative factors have
strictly smaller magnitude because 0<rho<1.

This construction goes beyond the usual single-partition certificate for
every STS(v) with v>=7. That certificate starts with s classes of disjoint
nonempty sets and C[A,B]=s*[same class]-1. Its nonempty principal Q-block
is s*[same class]. If N mod s is neither zero nor one, the largest class
has size at least ceil((N-1)/s)>N/s, forcing a principal eigenvalue above N.

For an STS downset, direct substitution gives

```
27N=8s^2+14s+32.
```

If N=0 modulo s, then s divides 32. If N=1 modulo s, then s divides 5.
But v>=7 implies s>=10, and the necessary STS congruence v=1 or 3 modulo
6 implies s=1 or 4 modulo 9. Neither possible divisor 16 or 32 of 32
has that residue; no divisor of 5 is large enough. Hence every such STS
downset excludes the upper bound for this partition formula, while our
explicit matrix satisfies it. This excludes a certificate template only;
it makes no assertion about ordinary disjoint-class partitions, convex
combinations of partition matrices, or failure of H.

## 6. Scope and validation

The open target and normalizations follow
[Ellis–Filmus–Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4),
whose current arXiv record was checked 2026-09-30 (only version 1).
The point/block incidence spectra are standard; see also
[Adriaensen et al., Section 1](https://arxiv.org/html/2609.26607#S1).
We claim this explicit construction and proof, without a historical priority
claim. The unrestricted conjecture and capped certificates for unions of
multiple block-disjoint systems remain outside this single-system theorem.
The separate exact finite result in [TWO_STS9_PROOF.md](TWO_STS9_PROOF.md)
now supplies the cap for every union of two block-disjoint STS(9).

The standard-library verifier constructs the entry-table matrix independently
of the decomposition, checks both PSD inequalities by rational Schur
elimination for STS(7), affine STS(9), and cyclic STS(13), and checks the
incidence identities against the entry formula. The infinite claim rests
on the written decomposition and inequalities, rather than extrapolation
from those examples. Floating-point searches used to discover a nine-point
certificate are outside the proof boundary.
