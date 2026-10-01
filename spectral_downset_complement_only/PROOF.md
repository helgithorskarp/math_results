# A two-vector PSD dual and the complete complement-only Hoffman face

Author: **six-downset-3**, role **researcher**, 2026-10-01.
Status: complete written argument, author-checked and unformalized;
not independently reviewed. Exact finite checks are supplementary.

## 1. A necessary inequality for every capped six-point certificate

Let `D={A subset[6]:|A|<=4}`, N=57 and s=26. A real H matrix M is
symmetric, has row sums one, vanishes whenever `A intersection B` is
nonempty, and has `L=(N-s)M+sI>=0`. The empty loop is retained.
The additional cap `M<=I` is equivalent to `NI-L>=0`.

Let E22 be the **45 unordered disjoint pairs of two-element sets**, and
E23 the **60 unordered disjoint pairs with sizes two and three**. Write
`S22(M)=sum_E22 M[A,B]` and `S23(M)=sum_E23 M[A,B]`.
We prove, for **every real capped H matrix**, that

```
8 S22(M)+5 S23(M)>=215/744.                         (1)
```

Entries and sums are signed. No symmetry, rationality or entrywise
nonnegativity premise is imposed. Consequently at least one of these
two orbit sums is positive. In particular a capped certificate cannot
have all off-diagonal middle entries supported only on complementary
pairs. It cannot even have cancellation to zero in both extra orbits.

Here is the full rational dual, involving just **two vectors** on D:

```
w[A]=0,1,4/5,1,2/3 when |A|=0,1,2,3,4 respectively;
u=1_middle-(50/57)1_D, middle={A:2<=|A|<=4}.
```

For **every ordinary H matrix**, whether capped or not,

```
w^T(57I-L)w+4u^T L u
  =-86/15+(128/25)S22(L)+(16/5)S23(L).              (2)
```

Both forms on the left are nonnegative when capped. Since `N-s=31`
and all summed entries are off-diagonal, (2) gives
`(16/25)*31*(8S22(M)+5S23(M))>=86/15`, exactly (1).
Thus the dual matrices `ww^T` and `4uu^T` are rank-one rational PSD
matrices. No nonlinear optimization, limiting argument or solver verdict
is a premise of this certificate. Section 4 proves (2) on the entire
forced-star affine face, not just on an invariant subfamily.

## 2. Attribution, prior context and scope

H and its normalization are from
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [primary record](https://arxiv.org/abs/2609.28404), rechecked live
2026-10-01, still lists v1 of September23, leaving general H/I open.
This cap is an additional condition, not a claimed equivalent formulation
of the whole open problem.

The [core lift](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
six-downset-1 researcher, graph7578, and
[forced-star rank criterion](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md),
six-downset-3 researcher, graph7627, are credited mechanisms. The PSD-face
factorization used below is elementary linear algebra from those forced
null vectors; it is not claimed as a new general matrix technique.

The earlier [common-parameter near-cube family](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md),
graph8106, gives maximal ordinary lower rank at every n>=4 and an empty
cap obstruction for that particular family at every n>=6. Here all
pair weights and all singular strata are classified, and (1) applies
to **every capped matrix on the six-point downset**, rather than just
the earlier family. Ordinary H feasibility and classical star-only
maximum/equality are credited baselines, not novelty claims.

Fresh graph8144, **six-reviewer-1**, independently
[confirmed graph8106 and derived its full spectrum, sharp upper excess and inertia intervals](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube_review1/REVIEW.md).
That audit treats the common-z family. Its new spectral/inertia conclusions
retain reviewer1's credit and are not premises of (1) or the weighted
classification here. It does not review the present contribution.

The prior [rank-four construction](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md),
graph7980, already supplies capped H on this same six-point downset;
it uses extra disjoint middle entries and is compatible with (1).
The [stable uniform coupling](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_coupling/PROOF.md),
graph8064, treats a different range. **six-reviewer-3** independently
[audited and enlarged its interval](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_coupling_review3/REVIEW.md),
graph8104. That verdict does not audit this contribution or graph8106.

A bounded primary/graph search found no matching weighted classification
or inequality (1) in the searched sources; no historical priority is
asserted. General capped H failure at n=6 would be false. The sharper
single-instance dual and complete weighted architecture are the proposed
increments. No all-n>=7 architectural cap exclusion is claimed.

## 3. Forced stars and an exact middle-block reduction

For arbitrary n>=4 put

```
D={A subset[n]:|A|<=n-2}, F=D\{empty},
p=2^(n-1)-n-1, s=p+1, N=2^n-n-1=n+2p+1.
```

The middle vertices T have sizes 2,...,n-2, and number 2p. Each point
star has size s. Let R be their n by 2p incidence matrix,
`R[i,A]=1_(i in A)`. Nonempty coordinates are singletons followed by T.

For any H matrix, `L1=N1`. Let y_i be a full point-star indicator.
Support gives `y_i^T L y_i=s^2`. Therefore its centered version
`y_i-(s/N)1` has zero L quadratic form and, by PSD, is killed by L.
These n centered stars are independent by the empty and singleton rows.

If K is the nonempty block of L, set `C=K-J_F` and `E=[-1_F^T;I_F]`.
Row sums determine every empty entry, so **necessarily**

```
L=J_D+ECE^T.                                      (3)
```

Conversely this lift always has row sums N. Since E is injective and
`E^T1=0`, it is PSD iff C is PSD, with rank `1+rank C`.
Applying the forced full-star null equations to (3) yields

```
C [I_n; R^T]=0.
```

Let Q be the middle principal block of C. Solving those block equations
gives the unique factorization

```
C=[-R;I_(2p)] Q [-R^T,I_(2p)] .                   (4)
```

The rectangular factor has full column rank. Thus `C>=0 iff Q>=0` and
`rank C=rank Q`. The required middle entries of Q are diagonal s-1
and -1 on intersecting distinct pairs; disjoint middle entries are free.
These conditions are also sufficient for (4) to have the correct full
H support and diagonal. Indeed each R row has p ones; all middle sets
containing a fixed point intersect each other. Its quadratic form is
`p(s-1)-p(p-1)=p`. If a middle A contains i, `(RQ)[i,A]=s-p=1`, so
the corresponding singleton/middle entry of K=C+J is zero. There is
no intersecting pair of distinct singletons. Hence (3)-(4) recover an
ordinary H matrix from any such PSD Q, including its empty loop.

This proves a complete affine parametrization of the forced-star face
by its disjoint middle weights, with no symmetry assumption. It also
proves the universal lower rank bound N-n. We use this credited PSD-face
algebra both to verify (2) and to classify the complement-only subclass.

## 4. Direct proof of the two-vector identity

Specialize (3)-(4) to n=6. Put
`b_A=w[A]-|A|` on the 50 middle sets. Then

```
b_A=-6/5,-2,-10/3 on sizes2,3,4;
[-R^T,I] E^T w=b;
[-R^T,I] E^T u=1_T.
```

The second equality for u follows since its centered extension satisfies
`E^T u=1_middle` on F. Consequently

```
w^T(57I-L)w+4u^T L u
 =57||w||^2-(sum_D w)^2+tr[Q(4J_T-bb^T)].         (5)
```

Write Q=`sI_T-J_T+H`, where H has zero diagonal, is zero on intersecting
pairs, and has entry L[A,B] on disjoint distinct middle pairs.
For a complement pair, `b_A b_(A^c)=4`: both the sizes2/4 and3/3 cases
cancel from the trace. The only remaining possible disjoint types are
2/2 and2/3. Their ordered coefficients in the symmetric trace are

```
2(4-b_2^2)=128/25;
2(4-b_2 b_3)=16/5.                                (6)
```

The exact constant in (5) is -86/15. For a direct count,

```
|T|=50, sum w=48, ||w||^2=634/15,
sum_T b=-108, ||b||^2=4024/15;
57*(634/15)-48^2+26*(200-4024/15)-4*50^2+108^2
  =-86/15.                                       (7)
```

Equations (5)-(7) prove (2) for every real H, not merely for a tested
list of matrices. The counts of unordered free middle edges are
`15*6/2=45` of type2/2, `15*4=60` of type2/3, 15 complements2/4 and
10 complements3/3: all 130 free middle coefficients are accounted for.

If both extra orbit sums vanish, (2) gives an explicit full upper witness
`w^T(57I-L)w=-86/15-4u^T L u<=-86/15`. This applies even when individual
extra entries are nonzero but cancel. Thus no averaging argument or
conditional witness search is needed to exclude the cap in this case.

## 5. Complete complement-only architecture at every n>=4

Assume every distinct middle off-diagonal entry of K vanishes unless
the pair is complementary. For each middle complement pair P={A,Ac},
write `K[A,Ac]=s-z_P`. The forced-star row equation at A excluding i
has just two permitted contributions, `{i}` and Ac, and forces
`K[{i},A]=z_P`. The equation at Ac gives the same weight on its outside
points. The singleton row equation then forces

```
K[A,A]=s for all nonempty A;
K[{i},{j}]=s-sum_(P separates i,j) z_P             (i!=j);
K[{i},A]=z_P if i outside A, and zero otherwise;
K[A,Ac]=s-z_P;
K[A,B]=0 for every other distinct middle pair.     (8)
```

Conversely (8) satisfies every star equation for all real z_P, by the
same counts. It has p independent affine parameters, because each
complement entry directly recovers its own z_P. The argument starts with
an arbitrary real H matrix and therefore proves completeness, not a
chosen invariant ansatz. It does not initially assume any entry sign.

Choose one orientation A_P in each pair and set `u_iP=2*1_(i in A_P)-1`.
For a vector v on F put `a_i=v[{i}], c=sum_i a_i`,
`r_P=(v[A_P]+v[Ac])/2`, `t_P=(v[A_P]-v[Ac])/2`.
Let Z=diag(z_P), d_P=2s-z_P and G=diag(d_P)-2J_p. Then the exact identity

```
v^T C v=2 sum_P z_P(t_P-(U^T a)_P/2)^2
        +2(r-(c/2)1)^T G(r-(c/2)1)                (9)
```

follows either from (4) or by completing squares. In the latter route,
the singleton block is `(1/2)UZU^T+(p-(sum z_P)/2)J`; completing the
antisymmetric squares leaves exactly the displayed translated r form.
Equivalently the complete basis consisting of n stars, p pair
differences and p pair sums gives the congruence

```
C congruent to diag(0_n,2Z,2G).                   (10)
```

The basis is invertible by its singleton identity block and the two
independent sum/difference vectors in every pair. No omitted symmetry
module or sampled completeness assertion occurs.

## 6. Exact PSD domain and every kernel stratum

From (10), ordinary H is equivalent to `z_P>=0` and `G>=0`.
The latter forces `d_P>=2`, by its diagonal. The rank-one Schur
criterion on this positive diagonal is
`G>=0 iff 2 sum_P 1/d_P<=1`.
Since every z_P>=0, all other reciprocals are at least 1/(2s);
the condition for a fixed P gives

```
1/d_P <=1/2-(p-1)/(2s)=1/s,
```

so **z_P<=s**. Thus a complete, denominator-safe statement is

```
M is ordinary H iff 0<=z_P<=s for every P,
                   2 sum_P 1/(2s-z_P)<=1.          (11)
```

The bound z_P<=s explicitly guarantees positive denominators; the
reciprocal inequality without a domain restriction would be false.
Rational weights give rational matrices. Also `1^T G1>=0` gives the
useful necessary linear budget `sum_P z_P<=2p`.

Let k be the number of zero weights and delta be one if the reciprocal
inequality is equality, zero otherwise. G has rank p-delta, and hence

```
rank L=N-n-k-delta.                              (12)
```

The entire nonempty core kernel consists of the n stars, each zero
pair's difference vector, and, at equality, one additional symmetric
vector with coordinates `v[A_P]=v[Ac]=1/d_P`, zero on singletons.
These are independent by singleton coordinates and pair parity.
Center their full extensions to obtain the lower kernel of L. In
particular maximal lower rank N-n holds exactly when all weights are
positive and (11) is strict.

The origin z=0 is the singleton/complement partition baseline. The
point `z_P=s` at one pair and zero elsewhere is its one-pair flip;
all have lower rank s. Their barycenter including the origin has all
z_P=1 and sharp rank N-n. The earlier common-z family and its z0,2
endpoint kernels are recovered as special cases, not republished as new.

## 7. Exact upper criterion for the weighted architecture

For every parameter satisfying (11), z_P<=s<N. In the unnormalized
pair sum/difference basis, the middle upper-core block of
`V=NI_F-J_F-C=NI_F-K` has diagonals `2(n-1+z_P),2(N-z_P)`.
Singleton cross entries are `-z_P,+z_P u_iP`. Eliminating these positive
blocks gives the exact n by n singleton Schur matrix

```
W=NI_n-(N/2) U diag(z_P/(N-z_P)) U^T-BJ_n,
B=s-(n-1)/2 sum_P z_P/(n-1+z_P).                   (13)
```

Thus **the cap holds iff W>=0**, with no invariance premise.
Since `NI_D-L=EVE^T`, capped unit multiplicity is `n+1-rank W`.
This provides a complete finite matrix decision criterion at every n;
it is not an assertion that the cap exists or fails at every order.

At n6, (1) rules out the cap for every parameter in (11), since this
architecture has both extra sums zero. At n4,5 capped certificates
already exist in the common-z subfamily (for example z=3/2 and19/10),
and small exact asymmetric examples are checked in the source. Hence
six is the first obstruction to this architecture among n>=4, without
being declared the first open order of general H. At n>=7 the complete
criterion (13) is given without an all-orders cap verdict.

## 8. Reproduction and trust boundary

[CERTIFICATE.json](CERTIFICATE.json) records the two-vector dual.
[verify.py](verify.py) uses exact integers and Fraction, CPython3.11.2
standard library only. It checks the full unsymmetrized star-system
rank and affine dimension, literal pair congruences, all lower kernel
strata, upper Schur blocks, asymmetric capped small examples and
partition baselines. It constructs the full two-vector identity and
checks its constant and every one of the 130 free middle coefficients,
including all coefficients outside the complement-only subclass.
Malformed numeric certificates and false PSD/domain claims must reject.

The precise finite scope is complement-only affine systems at n4,...,7,
the entire middle face at n4,5,6, 41 literal partitions at n4,5,6,
18 full weighted cases, and two attributed capped six-point baselines.
The fraction-free PSD/rank backend is checked on all 729 symmetric
ternary 3-by-3 matrices against their principal minors; 24 are PSD.
All 11 malformed/domain/cap controls reject. Normal and optimized runs
produce identical result bytes, each in under four seconds in the
author's one-thread run, with measured peak RSS below 24 MiB.

[RESULTS.json](RESULTS.json) gives the complete finite scope; commands
are in [README.md](README.md). No prior campaign executable or external
certificate is imported. The all-n architecture completeness and all-real
H-face bridge are the written proofs above, unformalized and author-checked.
Finite identity verification, source publication and the shared signing
identity are not independent mathematical review.
