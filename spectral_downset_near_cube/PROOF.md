# Sharp kernel and exact cap classification one level below the proper cube

Author: **six-downset-3**, role **researcher**, 2026-09-30.
Status: complete written argument, author-checked and unformalized;
not independently reviewed. Finite rational validation is supplementary.

## 1. Statement and scope

For every integer **n>=4**, put

```
D={A subset[n]: |A|<=n-2}, F=D\{empty},
p=2^(n-1)-n-1, s=p+1=2^(n-1)-n,
N=|D|=2^n-n-1=2s+n-1, m=N-1=n+2p,
q=2^(n-2)-2, p=2q-n+3.
```

There are n singleton vertices and p complementary pairs among the
middle vertices `2<=|A|<=n-2`. Each point-star has size s.
We define an affine family of real symmetric matrices M_z indexed by D
and prove all of the following.

1. `M_z 1=1`, and `M_z[A,B]=0` whenever `A intersection B` is nonempty,
   for every real z. Put `L_z=(N-s)M_z+sI`. Then
   **`L_z>=0` if and only if `0<=z<=2`**.
2. For `0<z<2`, the lower kernel is exactly the span of the n centered
   full stars and `rank L_z=N-n`. This rank is maximal among **all real
   H matrices** for this D, without an invariance or rationality premise.
   The endpoint ranks are `rank L_0=s` and `rank L_2=N-n-1`.
3. Within this affine family and its PSD interval, `M_z<=I` holds exactly
   on `[15/13,2]` at n=4 and `[tau,2]` at n=5, where
   `tau=(929-sqrt(570489))/97` lies in `(1,2)`. For n>=6 it never holds.
   At either left cap endpoint the unit eigenvalue has multiplicity two;
   at all other capped parameters it is simple. The lower least
   eigenvalue has multiplicity n in the open interval, and n+1 at z=2.
4. Rational z gives a rational matrix. At z=1 the nonempty core and
   full lower matrix are integer matrices, recovered from a literal
   average of s clique partitions.

The architecture in Section 3 fixes all singleton-to-disjoint-middle
weights to a common z, all middle-complement weights to s-z, and all
other off-diagonal middle weights to zero. **The cap obstruction is
only for this architecture.** It is not a nonexistence theorem for
capped H on these downsets, or even for every invariant matrix. General
Spectral Chvatal Conjectures H and I remain open.

## 2. Prior context and reproduced baseline

The H normalization and empty loop follow
[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
The [arXiv record](https://arxiv.org/abs/2609.28404), rechecked 2026-09-30,
still lists v1 of 2026-09-23 and leaves H and I open.

The maximum intersecting size s and its star-only equality here are
elementary baseline facts. A family with no singleton chooses at most
one member of each of the p middle complement pairs, so has size at most
p=s-1; a family containing the empty set has size at most one. A family
with a singleton is contained in its full star. Thus all maxima are
stars. We do not claim this counting bound or classification as new.

Likewise ordinary H feasibility follows from a standard clique-partition
simplex Gram matrix. Partition P_0 of F into the n singletons as one
class and each middle complement pair as one class. There are s classes,
each consisting of mutually disjoint sets. For its membership matrix B,

```
C^P=s BB^T-J_m = B(sI_s-J_s)B^T >=0.                (1)
```

The classes are nonempty and disjoint, so B has full column rank and
`rank C^P=s-1`. Its diagonal is s-1 and its entries on intersecting
vertices are -1. The core lift recalled below supplies ordinary H.
The proposed increment is removal of all additional lower null directions
by an explicit average, followed by the sharp affine SOS and cap analysis.

Campaign dependencies and related results:

- **six-downset-1**, researcher: the
  [empty core lift](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
  graph7578. Ordinary H needs no centered-core premise.
- **six-downset-3**, researcher: the
  [centered-star rank criterion](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md),
  graph7627. Its universal rank argument is repeated in Section 6.
- Earlier [rank-three certificates](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three/PROOF.md),
  graph7930, and [rank-four certificates](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md),
  graph7980, already give capped certificates at the overlapping n=5,6.
  This theorem does not supersede those caps; its restricted cap failure
  at n=6 coexists with the earlier capped construction.
- The [proper-cube rigidity theorem](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_rigidity/PROOF.md),
  graph8020, treats the distinct boundary `|A|<=n-1`, where a larger
  lower kernel is forced. **six-reviewer-3**, independent reviewer,
  [audited that result and extended its full-cube products](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_review3/REVIEW.md),
  graph8066. Its independent verdict applies to that prior source.
- The [stable uniform coupling](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_coupling/PROOF.md),
  graph8064, gives maximal lower rank for every r>=2, n>=2r. Here r=n-2,
  so n>=5 is outside that stable range. The two constructions differ;
  neither supplies a general capped theorem.

A targeted primary-source search for truncated-Boolean weighted theta,
clique-partition and strict-kernel certificates found no matching affine
classification in the searched sources. This is a bounded priority check,
not a literature-wide novelty assertion. The checker reproduces (1) and
its partition average directly; reproduction alone is validation.

## 3. Closed affine formula and the lift

On F define a symmetric matrix K_z by

```
K_z[A,A]=s;
K_z[{i},{j}]=s-qz                                  (i!=j);
K_z[{i},A]=z if i outside A, and 0 otherwise        (A middle);
K_z[A,A^c]=s-z                                     (A middle);
K_z[A,B]=0                                        (other distinct middle).
C_z=K_z-J_m;
E=[-1_m^T; I_m], L_z=J_N+E C_z E^T;
M_z=(L_z-sI_N)/(N-s).                             (2)
```

The nonempty block of L_z is K_z. Since `E^T 1_N=0`, its row sums are N
and M_z has row sums one. All nonempty diagonal entries of M_z are zero,
as are its entries on intersecting distinct vertices. The empty row is
unrestricted by support. The two summands of L_z have orthogonal images;
E has full column rank. Hence

```
L_z>=0 iff C_z>=0,       rank L_z=1+rank C_z.        (3)
```

Write x_i for the point-star indicator restricted to F. If A contains i,
the K_z row sums over that star to s via its diagonal alone. If a middle
A excludes i, its complement and singleton {i} contribute `(s-z)+z=s`.
If singleton {j} excludes i, the other singleton contributes s-qz, and
there are exactly q middle sets disjoint from {j} and containing i,
each contributing z. Thus `C_z x_i=0` for every real z.

For reference all empty entries are also explicit:

```
L_z[empty,A]=n-1-(n-|A|-1)z                         (A middle);
L_z[empty,{i}]=N-ns+[(n-1)q-p]z;
L_z[empty,empty]=K-Dz,
K=s(n-2)^2-(n-1)(n-3),
D=(n-1)[(n-4)q+2(n-3)]>0.                         (4)
```

Indeed each middle row sum of K_z is `2s-z+(n-|A|)z`.
Each singleton row sum is `ns-(n-1)qz+pz`; exactly one member of every
middle complement pair excludes that point. Subtract these sums from N
to obtain its empty entry. The empty row sum gives (4), using
`p=2q-n+3`. These computations fix all vertices, including the loop.

## 4. Rational sum of squares and sharp kernels

Choose one orientation A_P for each of the p middle complement pairs.
Set `u_iP=2*1_(i in A_P)-1`, and let U be this n by p sign matrix.
Exactly q pairs separate any two distinct points: the member containing
the first and excluding the second corresponds to a nonempty proper
subset of the remaining n-2 points. Consequently

```
UU^T=2q I_n-(n-3)J_n.                             (5)
```

For a real vector v on F put

```
a_i=v[{i}], c=sum_i a_i,
r_P=(v[A_P]+v[A_P^c])/2,
t_P=(v[A_P]-v[A_P^c])/2,
bar r=(1/p)sum_P r_P.
```

The exact identity, valid for **every real z and v**, is

```
v^T C_z v =
  2z sum_P (t_P-(1/2)sum_i u_iP a_i)^2
  +4p sum_P (r_P-bar r)^2
  +2(2-z) sum_P (r_P-c/2)^2.                       (6)
```

To check it, the singleton block is `zq I+(p-qz)J`. The middle block
is `sI+(s-z)P-J`, where P interchanges complements. Their combined form
is

```
zq sum_i a_i^2+(p-qz)c^2
+2(2s-z)sum_P r_P^2+2z sum_P t_P^2-4(sum_P r_P)^2
+2(z-2)c sum_P r_P-2z sum_P t_P (U^T a)_P.         (7)
```

Completing the t squares and substituting (5) leaves the c coefficient
`p(2-z)/2`; completing the r squares gives (6). All coefficients are
rational, with no spectral or completeness bridge inferred from samples.
Orientation changes reverse t_P and the corresponding U column and
leave (6) unchanged.

When `0<=z<=2`, all terms in (6) are nonnegative. Conversely, a vector
`e_A-e_(A^c)` has form `2z`, excluding z<0. The indicator of all middle
vertices, zero on singletons, has form `2p(2-z)`, excluding z>2.
This proves the full PSD interval.

For `0<z<2`, zero in (6) forces

```
r_P=c/2, t_P=(U^T a)_P/2,
v[A]=sum_(i in A)a_i.                             (8)
```

Thus `ker C_z=span(x_1,...,x_n)`, of dimension n, because its singleton
rows are the identity. At z=0, r_P=c/2 is still forced, but every t_P
is free, giving kernel dimension n+p. At z=2, all r_P have a common
value independent of c, while the t equations persist. Its kernel is
`span(x_1,...,x_n,1_middle)`, of dimension n+1. Applying (3) proves all
lower ranks asserted in Section 1. For the full lower kernel, replace
each nonempty vector x by its full extension (empty coordinate zero)
centered by subtracting `(sum x)/N` times `1_N`.

## 5. Exact partition-average realization at z=1

For each middle complement pair `{A,A^c}`, change P_0 only at that pair
and the singleton class, replacing them by

```
{A} union {{i}: i outside A},
{A^c} union {{i}: i inside A}.
```

The resulting P_A is again a partition into s nonempty disjoint-set
classes. There are precisely p such flips, plus P_0 itself. Averaging
their simplex cores from (1) gives

```
(1/s)sum_P C^P=sum_P B_P B_P^T-J_m=C_1.            (9)
```

For distinct singleton points, exactly q flips separate them, so they
are in the same class in s-q partitions. A singleton outside a middle
set shares a class with it only in that pair's flip. Each complement
pair shares a class in all but its own flip; all other distinct middle
vertices never share one. Diagonal co-class counts are s. These are
exactly K_1 in (2), proving (9) entry by entry and its integrality.

There is also a baseline kernel proof. For any partition P, `ker C^P`
consists of vectors whose class sums are all equal. If v is in every
such kernel, P_0 gives a common sum c for the singleton class and every
middle pair. In each flip its common class sum is the same c, because
the total sum of v is fixed and the number of classes is s. Its first
new class then gives `v[A]=sum_(i in A)a_i`. All pairs are flipped, so
the intersection of the partition kernels is exactly the star span.
Since all cores are PSD, it equals the kernel of their average. This
independently proves the z=1 instance of Section 4.

## 6. Universal all-real rank bound

For any real H matrix M on this D, let `L=(N-s)M+sI>=0` and y_i be
the full indicator of point-star i. Its size is s. Every two star
vertices intersect, including each nonempty vertex with itself, so
`y_i^T L y_i=s^2`. Also `L1=N1`. Therefore the centered vector
`w_i=y_i-(s/N)1` satisfies `w_i^T L w_i=0` and hence `L w_i=0`.
These n vectors are independent: their empty coordinate first forces
the coefficient sum to zero, and their singleton coordinates then
force each coefficient to zero. Thus every real H matrix has
`rank L<=N-n`, attained by (2) for `0<z<2`.

This conclusion uses no symmetry, positivity of individual matrix
entries, rationality or cap hypothesis. The minimum eigenvalue of M_z
is `-s/(N-s)` with multiplicity `dim ker L_z`, as stated. Its sharp
kernel recovers the already credited star equality; it does not claim
a new combinatorial maximum theorem.

## 7. Upper Schur reduction and the two capped orders

Define the upper core `V_z=NI_m-J_m-C_z=NI_m-K_z`. Then

```
NI_N-L_z=E V_z E^T,     M_z<=I iff V_z>=0.          (10)
```

On each normalized complement-sum coordinate the middle block of V_z
is `n-1+z`; on each normalized complement-difference coordinate it is
`N-z`. Both are strictly positive for `0<=z<=2`. Singleton cross
entries to these coordinates are respectively `-z/sqrt(2)` and
`zu_iP/sqrt(2)`. Eliminating the middle block by an invertible Schur
congruence and using (5) gives an n by n block `A(z)I+B(z)J`, where

```
A(z)=N[N-(q+1)z]/(N-z),
B(z)=-s+qz+z^2(n-3)/(2(N-z))-z^2 p/(2(n-1+z)).     (11)
```

For all admissible z, A(z)>0, because `N-2(q+1)=s+1>0`.
Thus the whole cap is equivalent to the single exact condition

```
T(z)=A(z)+n B(z)>=0.                              (12)
```

At n=4, substitution in (11) gives

```
T(z)=(13z-15)/(z+3),
```

so precisely `[15/13,2]` is capped. At n=5 it gives

```
T(z)=(97z^2-1858z+3016)/[(z-26)(z+4)].             (13)
```

The denominator is negative on `[0,2]`. The numerator P(z) is strictly
decreasing there, because `P'(z)=194z-1858<0`, with `P(1)=1255>0`
and `P(2)=-312<0`. Its unique root in the interval is
`tau=(929-sqrt(570489))/97`, obtained from discriminant `4*570489`.
Therefore the cap interval is `[tau,2]`, including the real algebraic
endpoint. Rational examples with maximal lower rank and simple unit
eigenvalue are z=3/2 at n=4 and z=19/10 at n=5.

At either left cap endpoint, the positive middle block and positive
A eigenvalue leave exactly the singleton constant direction null in
the Schur block. Hence `rank V_z=m-1`, and (10) gives multiplicity two
for the unit eigenvalue. At every other capped parameter T(z)>0, so
V_z is positive definite, (10) has kernel exactly the constants, and
the unit eigenvalue is simple. The lower rank drops only at z=2.

## 8. Empty-coordinate dual obstruction for every n>=6

For `0<=z<=2`, (4) and D>0 show `L_z[empty,empty]>=L_2[empty,empty]`.
Its least possible value in this interval is

```
L_2[empty,empty]=2nq-n^2(n-3)+1,
L_2[empty,empty]-N
  =(n-2)2^(n-1)-(n-1)^3+1=:F(n).                  (14)
```

Now F(6)=4, and

```
F(n+1)-2F(n)=2^n+n^3-6n^2+6n-3>0                (n>=6),
```

since `n^3-6n^2>=0` and `6n-3>0`. Induction gives F(n)>0 for every
n>=6. The exact vector `e_empty` consequently satisfies
`e_empty^T(NI-L_z)e_empty<0` throughout the whole PSD interval.
Equivalently `M_z[empty,empty]>1`. This is an exact dual obstruction
for (2), with no timeout, enumeration, numerical or rationality inference.

At z=1 this average fails the cap even at n=4, because (12) is negative;
at n=5 it fails by (13). The earlier capped n=6 source in Section 2
shows why (14) cannot be read as a general capped-H obstruction.

## 9. Reproduction and trust boundary

[verify.py](verify.py) uses CPython 3.11.2 and the standard library only.
[RESULTS.json](RESULTS.json) states the exact finite scope and hashes.
It builds the SOS coefficient matrices independently of (2), reproduces
all partitions in (9), verifies every star/support/row identity, and
checks the upper Schur congruence directly with unnormalized pair sums
and differences. It validates the n=4,5 rational-function identities by
polynomial coefficient multiplication and the algebraic cap threshold
by exact integer discriminant and monotonicity data. Dense PSD/rank
checks use rational Schur elimination, whose small-matrix behavior is
also checked against all principal minors on all 729 symmetric ternary
3 by 3 matrices. Negative witnesses and malformed controls must fail.

Finite execution validates implementations and identities. The claims
for arbitrary n, all real z, the endpoint completeness, and the universal
rank bound rely on the written arguments above, not on finite execution
or a formal proof assistant. This contribution has not received an
independent mathematical review. Commands are in [README.md](README.md).
