# Exact capped restrictions by pair deletion

Authoring agent: **six-downset-1**, role **researcher**, 2026-09-30.
This extends the uniform projection in [PROOF.md, section 9](PROOF.md).
The infinite statements below have ordinary written proofs. Exact rational
computations validate specified examples; they do not supply the infinite
quantifiers. No independent review, formalization, or priority claim is made.

## 1. Statement and scope

Let n>=3, let D_n be the downset of all subsets of [n] of size at most two,
and set

```
N_0 = 1+n+binom(n,2),       kappa = n(n-1)/(n-2).
```

Choose a set T of k pairs to delete, retaining every singleton and the empty
set. Assume **some coordinate is incident to no pair of T**. Equivalently,
the remaining pair graph has a universal vertex. The resulting downset
D_{n,T} has

```
N = N_0-k,                 s = n.
```

Let C be the uniform core in PROOF.md, section 9, and C' its principal
submatrix on the retained nonempty sets. Define E=[-1^T; I] and

```
Q = E C' E^T,        M = (Q+J_N-n I_N)/(N-n).               (1)
```

Every such M satisfies H: symmetry, disjointness support, M1=1, and
(N-n)M+nI>=0. The following results decide or guarantee its extra bound
M<=I. They concern the specified inherited matrix, not all possible
certificates for the downset.

**Exact regular-deletion theorem.** For k>=1, suppose the line graph of T
is d-regular: each deleted pair meets exactly d other deleted pairs. Put

```
g = n-1-d + 2(k-1-d)/(n-2).
```

Then g>=0 and

```
lambda_max(Q) = kappa+(k-1)g,
M<=I  iff  kappa+(k-1)g <= N_0-k.                         (2)
```

In particular, (1) is capped for every partial-star deletion with
1<=k<=n-2, and for every matching deletion with 1<=k and 2k<n.
All one-pair deletions are included. Arbitrary products of these factors,
uniform rank-two downsets, and any other already capped factors satisfy H
by PROOF.md, section 5. The tensor construction retains the upper cap.

**Exact arbitrary-deletion test.** For n>=4 let G be the k by k matrix

```
G[i,i]=n-1;
G[i,j]=-1 if deleted pairs i,j meet;
G[i,j]=2/(n-2) otherwise, for i!=j.
```

Set delta=N-kappa>0. Then

```
M<=I iff 1_k^T G(delta I_k+G)^(-1)1_k <= 1.               (3)
```

This is a rational linear-system test, even when the line graph is
irregular. The empty deletion has value zero. The only eligible n=3
nonempty deletion has k=1, delta=0, and is capped by the one-deletion proof.

## 2. The coalesced empty vector and frame identity

The original C is PSD, C1=0, and C^2=kappa C. Its rank is
r=binom(n,2)-1. Choose Gram vectors u_A in R^r for its nonempty indices:

```
<u_A,u_B>=C[A,B],
sum_A u_A=0,             sum_A u_A u_A^T = kappa I_r.     (4)
```

These facts follow from a square root on the range of C. The first sum
vanishes since its squared norm is 1^T C1=0. The second is the tight-frame
form of the scaled-projection identity. A real square root is used only in
the proof: the actual matrices (1) and (3) are rational.

Let W have as columns the k deleted vectors, and let t=W1_k. The empty
vector in the lifted retained core is exactly t, because minus the sum
of the retained vectors equals the sum of the deleted vectors. Thus Q is
the Gram matrix of t and the retained u_A. Its frame operator is

```
F = kappa I_r - W W^T + t t^T
  = kappa I_r + W(J_k-I_k)W^T.                           (5)
```

F and Q have the same nonzero eigenvalues, including multiplicities.
Moreover their vector sum is zero, so Q1=0. The principal-core proof in
PROOF.md, sections 2-3, supplies the remaining H requirements.

On 1_N perpendicular, M=(Q-nI)/(N-n); on 1_N, M has eigenvalue one.
Consequently the extra upper bound is precisely Q<=NI, or F<=NI.
This also follows from the exact identity
(N-n)(I-M)=NI-J-Q.

The untouched-coordinate hypothesis implies
k<=binom(n-1,2)<r, because r-k>=n-2. Hence the orthogonal complement of
the columns of W is nonzero; on it F acts as kappa I. This prevents a
negative perturbation from eliminating the original top baseline entirely.

For k=1, the two terms W W^T and t t^T cancel. More concretely, Q is just
the original C with the removed pair relabelled as the empty vertex.
Its top eigenvalue remains kappa. Here N>=2n, and

```
2n-kappa = n(n-3)/(n-2) >= 0.
```

Therefore every eligible one-pair deletion is capped, including n=3 with
equality.

## 3. The arbitrary-deletion test

G=W^T W is the deleted principal block of C, so G is PSD and has the
entries displayed in section 1. For n>=4, N>=2n gives
delta=N-kappa>=n(n-3)/(n-2)>0. From (5),

```
NI-F = delta I_r+W W^T-t t^T.
```

For any positive-definite A, A-tt^T is PSD exactly when t^T A^(-1)t<=1:
congruence by A^(-1/2) reduces it to I-vv^T. Take A=delta I_r+W W^T.
The identity

```
(delta I_r+W W^T)W = W(delta I_k+G)
```

and invertibility on both sides give

```
t^T A^(-1)t = 1_k^T G(delta I_k+G)^(-1)1_k.
```

This proves (3), including singular G. The coefficient matrix is strictly
positive definite, so an exact rational solve suffices. This criterion
does not establish that every deletion passes, nor obstruct alternative
matrices if a deletion fails.

## 4. Regular line graphs and exact top eigenvalues

If the line graph is d-regular, every row of G sums to g. PSD implies g>=0.
With B=W(J-I)W^T, its distinguished vector satisfies

```
B t=(k-1)g t,          ||t||^2=k g.
```

For any x perpendicular to t,

```
x^T Bx = (x^T t)^2-||W^T x||^2 = -||W^T x||^2 <= 0.
```

If g>0, t is nonzero and the top eigenvalue of B is (k-1)g. If g=0,
t=0 and B=-WW^T; because k<r, B still has a zero eigenvalue. Its top is
again (k-1)g=0. Adding kappa I proves (2). For delta>0, the scalar
test also reduces to kg/(delta+g)<=1, or (k-1)g<=delta.

If g>0, a rational top eigenvector of Q is available without Gram square
roots:

```
z[0]=kg,
z[A]=sum_{e in T} C[A,e]  for each retained nonempty A.    (6)
```

Indeed z consists of inner products of t with the new frame vectors.
It satisfies Qz=[kappa+(k-1)g]z, z^T1=0, and
||z||^2=[kappa+(k-1)g]kg. Formula (6) is useful for exact failures of
the additional cap.

## 5. Two infinite deletion classes

For a star of k deleted edges, d=k-1 and g=n-k. The condition k<=n-2
leaves a coordinate outside its k+1 vertices. Direct completion of the
square gives

```
N_0-k-kappa-(k-1)(n-k)
 = [k-(n+2)/2]^2 + n^2(n-4)/[4(n-2)].                    (7)
```

For n>=4 this is nonnegative. For n=3 the only allowed k is one and
the expression is zero. This proves the cap for all partial stars,
without any finite enumeration.

For a matching of k deleted edges, d=0 and
g=n-1+2(k-1)/(n-2). Write the cap margin as

```
h(k)=n(n+3)/2-kappa-nk-2(k-1)^2/(n-2).
```

For real k>=1 it is decreasing: for b>a>=1 both nk and (k-1)^2
increase strictly or weakly. Since k< n/2 implies k<=(n-1)/2,

```
h(k)>=h((n-1)/2)=(n^2-9)/[2(n-2)]>=0.                   (8)
```

The last inequality holds for n>=3. This proves every claimed matching
case. Stars and matchings refer to the graph of **deleted** pairs;
the retained downsets are generally dense nonuniform rank-two families.

## 6. Clique deletion and an exact restriction obstruction

For T consisting of all pairs on t coordinates with 2<=t<n,
k=t(t-1)/2, d=2(t-2), and the row sum simplifies to

```
g=(n-t)(n-t+1)/(n-2).
```

Thus (2) is an exact rational criterion for the inherited certificate of
every complete graph with one clique of pairs deleted. At t=n-1 the
retained pair graph is a star, N=2n, and the top eigenvalue is exactly 2n;
the cap holds with equality. Intermediate values need not pass.

For example take n=7, T=all ten pairs on the first five coordinates.
Then N=19, s=7, kappa=42/5, g=6/5, and

```
lambda_max(Q)=96/5>19,
lambda_max(M)=(96/5-7)/12=61/60>1.                       (9)
```

Multiplying (6) by five gives an integer eigenvector x with entries:
empty 60; singleton -8 on the first five coordinates and 20 on the other
two; retained cross-pair -8; pair on the other two coordinates 20.
Then x^T1=0, ||x||^2=5760, and

```
x^T [19I-J-Q]x = -1152,
x^T (I-M)x = -96.                                      (10)
```

The original uniform certificate is capped and the restriction preserves
s. Hence this explicitly shows that the **principal-core restriction
construction** need not preserve the cap. It refutes that transport rule,
not H, cap feasibility for this downset, or a different transport method.
The restricted matrix still satisfies H exactly.

The construction already fails the cap at n=5: delete a four-cycle on
the first four coordinates. Then k=4, d=2, g=8/3, N=12, s=5,
lambda_max(Q)=44/3 and lambda_max(M)=29/21>1. Formula (6), multiplied
by nine, gives a centered integer eigenvector of norm squared 12672 and
quadratic form -33792 against 12I-J-Q. At n=3,4 every eligible deletion
passes: after placing an untouched coordinate last, a deletion graph on
at most three coordinates is empty, one edge, a two-edge star, or a
triangle. These are covered above. Thus five is the least coordinate
order where this particular projection restriction can lose the cap.
This minimality statement concerns the transport construction only.

These two five-coordinate failure templates have other capped matrices.
The C4 deletion retains the friendship graph F_2, whose different centered
core is proved in [FRIENDSHIP.md](FRIENDSHIP.md). Deleting K4 minus an edge
gives N=11,s=5, already covered by the equitable partition criterion
N=1 modulo s. Neither failed inherited matrix obstructs cap feasibility.

## 7. Validation, dependencies, and next frontier

[deletions.py](deletions.py) constructs (1), the rational criterion (3),
and the exact eigenvector (6). [verify_deletions.py](verify_deletions.py)
checks definition-level H and the upper bound using exact LDL from
[verify.py](verify.py), independently of the scalar criterion. For the
stated small deletion cohort it compares the scalar decision with direct
PSD entry by entry, and checks each nonempty regular-case top eigenvalue
with both its exact eigenvector and a PSD upper shift. Empty deletions use
the original projection baseline.

The run includes all 74 labelled deletion graphs on the first n-1
coordinates for n=3,4,5, with 65 capped and nine uncapped inherited
matrices; 28 partial stars and 16 matchings for n=3,...,9;
36 regular clique deletions for n=3,...,10, of which 28 pass and eight
fail; two irregular seven-coordinate examples; both explicit restriction
obstructions; and two capped products of dimensions 54 and 84.
It is validation of the
proved mechanisms, not a census of all downsets or proof that every
possible certificate was tried. Precise counts, bounds and compact outputs
are in [deletions_expected.json](deletions_expected.json).

Reproduce with CPython 3.11.2, standard library, one process:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 verify_deletions.py
```

Primary problem context remains Ellis--Filmus--Friedgut,
[*Chvátal's conjecture: a proof from The Book*, section 4](https://arxiv.org/html/2609.28404v1#S4).
The [current arXiv record](https://arxiv.org/abs/2609.28404) was refreshed on
2026-09-30 and still listed only v1. H and I remain conjectures in that
paper. A bounded targeted search did not locate these precise formulas;
that does not establish priority. The proofs here depend on the uniform
incidence identity and elementary symmetric linear algebra. No Vizing,
solver, floating-point inference, imported census, or missing completeness
bridge is needed for the deletion theorems. The proofs are unformalized.

The next mathematical question is whether different capped cores cover
further split-graph families whose inherited projection fails (3),
starting with the 19-vertex example. Its pair graph is K2 joined to five
independent leaves. The two smallest failure templates are repaired as
described above.
Formula (3) diagnoses this inherited template;
it is not a universal nonexistence test. General H and unrestricted capped
rank-two feasibility remain unresolved by this source.
