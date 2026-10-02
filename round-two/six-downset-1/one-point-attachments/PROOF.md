# Star-bounded one-point attachments to a Boolean cube

Actual author: **six-downset-1**, role **researcher**, 2026-10-02.
Complete author-checked ordinary proof, unformalized. Exact checks below
validate the implementation; independent review of this result is pending.

## Quantified closure and rank statement

Let X be an n-element set, n>=2, and q=2^(n-1). For each member j of a
nonempty finite index set, choose a mark x_j in X and a nontrivial downset
E_j on a private support Y_j. The Y_j are pairwise disjoint and disjoint
from X. Each E_j contains its actual empty set. Suppose E_j has an
ordinary H certificate, with largest-star size t_j<=q. Define

```text
F = 2^X union union_j {T, {x_j} union T : T in E_j},
d_j=|E_j|-1, d_i=sum_(j:x_j=i) d_j, m=sum_j d_j,
D=max_(i in X) d_i, k=|{i in X:d_i=D}|,
N=|F|=2q+2m, s=q+D.
```

There is an explicit ordinary H certificate on F. It is rational whenever
the private certificates are rational. No upper spectral cap is assumed
on the inputs or asserted for this output.

If **every t_j<q**, this certificate has

```text
rank((N-s)M+sI)=N-k,
ker((N-s)M+sI)=span{1_(i-star)-(s/N)1 : d_i=D}.
```

The lower rank is greatest among **all real H certificates** on F.
Exactly the k heavy old stars are maximum intersecting families.
There is no bound on the number of attachments, their sizes or their
coordinate counts beyond the stated private-star bound and certificate
hypothesis. Several private families may attach at the same old mark;
marks without an attachment remain part of the cube.

At the weak boundary t_j=q, existence still holds. If nu_j is the nullity
of the supplied private nonempty H core, the displayed construction has

```text
rank((N-s)M+sI)=N-k-sum_(j:t_j=q) nu_j.              (1)
```

We make no greatest-rank or maximum-family classification claim at that
boundary. In particular, the strict hypothesis is retained in both claims.

For Boolean private inputs E_j=2^(Y_j), their complement certificates give
t_j=2^(|Y_j|-1). Thus **arbitrarily many Boolean facets of sizes at most n**
may attach at arbitrary old marks with the greatest-rank and exact
maximum-family conclusions. Facets of size n+1 are also allowed for
ordinary existence and the supplied boundary rank (1).

## Context and credit

The target is Ellis, Filmus and Friedgut,
[arXiv:2609.28404](https://arxiv.org/abs/2609.28404),
[Section 4](https://arxiv.org/html/2609.28404v1#S4), live checked 2026-10-02:
the listed version is v1 of 2026-09-23, and H and I remain open. The
matrix upper cap used in other packets is an additional property of a
construction, and is not part of H or equivalent to I.

The empty lift, forced-star argument, ordinary disjoint-support union,
complement baseline and private uniform rank-two input are credited to
LEMMA7578,
[structural certificates](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).
The old loaded-cube Gram block and marked-row residual are credited to
the pendant line, including LEMMA9153,
[two-load types](../two-load-types/PROOF.md), LEMMA9229,
[three distinct loads](../three-distinct-loads/PROOF.md), and LEMMA9305,
[arbitrary pendant profiles](../arbitrary-pendant-loads/PROOF.md).
The new private-row projection and scaled private-core shift below use
these mechanisms to give a conditional attachment closure for general
private downsets. This ordinary result does not extend the pendant
line's upper-cap guarantee.

LEMMA8579's [two-facet result](../UNEQUAL_FACETS.md) and LEMMA8700's
[all Boolean sunflowers](../ALL_PETALS.md) cover one attached Boolean facet
and common-core configurations. They do not directly cover facets meeting
the old cube at different old singleton marks. Their covered cases and
finite small-family coverage are prior art. We claim this explicit closure
and rank argument, without a historical priority claim for ordinary H on
any overlapping finite instance. No review of a predecessor transfers to it.

The newly committed REVIEW9349,
[independent arbitrary-profile audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/arbitrary-profile-audit/REVIEW.md),
independently confirms9305's new analytic pendant branch and strengthens its
normalized balanced mean budget to greater than1/5, retaining the earlier
branches as premises for its all-profile corollary. This is scoped predecessor
context, not a proof input or review of the new attachment closure.

## The actual empty lift

For a downset of size N and parameter s, a nonempty core C with

```text
C>=0, C[A,A]=s-1,
C[A,B]=-1 when A!=B and A intersects B
```

gives the actual N-by-N matrix, including the empty row and loop,

```text
E=[-1'; I_(N-1)], Q=ECE',
L=J_N+Q, M=(L-sI)/(N-s).                            (2)
```

The constant vector has L-eigenvalue N, E'1=0, and M1=1. Prescribed
intersecting entries of M, including all nonempty diagonals, vanish.
L>=0 and rank(L)=1+rank(C). Conversely every real H matrix supplies such
a core: its L has constant eigenvalue N, so Q=L-J_N>=0, has zero row
sums, and equals ECE'. This credited equivalence does not need C to be
invertible. The empty Gram vector is minus the sum of **all** nonempty
Gram vectors; it is never discarded.

## Exact old-cube identities

Index the old nonempty vertices by A in 2^X minus {empty}. Let P be
proper complementation: P[A,B]=1 when A and B are complements in X,
and zero otherwise. Its row at the full set X is zero. Define

```text
A_D=(q+D)I+(q-D)P-J.                               (3)
```

This matrix is positive definite for every D>0. On proper pair-constant
contrasts its eigenvalue is 2q, multiplicity q-2; on proper pair-antisymmetric
vectors it is 2D, multiplicity q-1. The remaining two-dimensional space is
spanned by the proper constant and the full-set unit. In an orthonormal
basis its matrix is

```text
[[2, -sqrt(2q-2)], [-sqrt(2q-2), q+D-1]],
```

with positive diagonal and determinant 2D>0. These spaces have total
dimension 2q-1. At q=2 the first contrast space is empty; the same
two-dimensional determinant proof applies. The square root describes
an ordinary spectral decomposition; all constructed matrix entries are
rational.

Take independent old Gram vectors g_A with Gram A_D. Put

```text
H_i=-sum_(A:i in A) g_A, G=sum_A g_A, w=q+D-1.
H_i*g_A=D(1-2[i in A]), H_i*H_l=qD[i=l],
G*H_i=-D, G*G=w.                                  (4)
```

For the first identity, if i is in A, the sum over the i-star in the
A-column of (3) is (q+D)-q=D. If i is not in A, proper complementation
contributes q-D and the star contributes -q, giving -D. For i!=l exactly
half of the l-star contains i, proving orthogonality of H_i,H_l. The
diagonal and constant identities follow by the same counts. In particular,
the old/private cross entries have **both signs**; they are not indicator
matrices.

## Marked rows and private rows

For each old mark i with d_i>0 choose vectors Z_(j,T), over all its d_i
private nonempty members, with Gram

```text
(q+D)(I_(d_i)-J_(d_i)/D).                          (5)
```

They are perpendicular to the old span and to every other marked residual
space. Since 0<d_i<=D, (5) is PSD. Its rank is d_i if d_i<D and d_i-1
if d_i=D. In the latter case its sum vector is zero. Define the new marked
vectors, corresponding to {x_j} union T, by

```text
V_(j,T)=H_(x_j)/D+Z_(j,T).                         (6)
```

For each private input let C_j be its nonempty H core. In a new residual
space perpendicular to every old and marked residual space, take W_(j,T)
with Gram

```text
R_j=(1+D/q)[C_j+(q-t_j)I].                         (7)
```

Residual spaces for distinct j are perpendicular. The shift in (7) is
nonnegative, so R_j>=0. If t_j<q it is positive definite. Its diagonal is
(1+D/q)(q-1). Define the private rows by

```text
U_(j,T)=-H_(x_j)/q+W_(j,T).                        (8)
```

All norms are w: (6) has old part q/D and residual s(1-1/D), while (8)
has old part D/q and residual (1+D/q)(q-1). Their sum in each case is w.

All required off-diagonal Gram products equal -1. An old A intersects a
marked row precisely when x_j is in A, where (4) and (6) give -1. Marked
rows with the same old mark have product q/D-s/D=-1. Different-mark
marked rows are disjoint and have product zero. A private row and a marked
row with its own mark have product -1 regardless of their private members;
this imposes some additional -1 entries at disjoint pairs, which H permits.
Different marks give product zero. Within one private input, intersecting
distinct T,T' give

```text
U_(j,T)*U_(j,T')=D/q+(1+D/q)(-1)=-1.
```

Private rows are disjoint from all old sets and from private rows of other
inputs, so their other products are free. These cases exhaust every
intersection in F. Equations (3),(5),(7) are PSD Gram data, proving the
complete nonempty core is PSD. Formula (2) gives H.

For a literal implementation the complete closed entry table is

```text
old A, V_(j,T): 1-2[x_j in A];
old A, U_(j,T): (D/q)(2[x_j in A]-1);
V_(j,T), V_(l,S): s[(j,T)=(l,S)]-1 if x_j=x_l, else 0;
U_(j,T), V_(l,S): -[x_j=x_l];
U_(j,T), U_(l,S): (D/q)[x_j=x_l]+[j=l]R_j[T,S].    (9)
```

Use (3) for old/old entries and symmetry for the reversed cases.
Diagonal positions in (9) have their actual distinct vertex labels.

## Family size, stars and exact ranks

Every nonempty private member adds exactly two vertices, while empty and
the marked singleton already belong to the old cube. Thus N=2q+2m.
An old i-star has size q+d_i. A private coordinate has star at most 2t_j.
Deleting a coordinate from its star is an injection into the other half
of a downset, so d_j=|E_j|-1>=2t_j-1. Hence

```text
q+D>=q+d_j>=q+2t_j-1>2t_j,
```

as q>=2. The largest stars are exactly the k maximum-load old marks, of
size s=q+D. Since D<=m, s<=N/2. The lift denominator is positive.

The old vectors span dimension 2q-1. Subtracting their projections from
(6) leaves all marked residuals, spanning m-k dimensions. Subtracting
the old projection from (8) leaves all independent private residuals,
spanning

```text
sum_j rank(R_j)=m-sum_(j:t_j=q) nu_j.
```

These three spaces are mutually orthogonal. All their spanning vectors
are obtained from the actual nonempty rows. Thus their sum is the exact
core rank, proving (1), not merely a rank upper bound.

In the strict case the core kernel has dimension k. Each heavy star is
in this kernel: its old vectors sum to -H_i and its marked vectors sum
to (d_i/D)H_i=H_i, with zero residual sum. The k star indicators are
independent, since each heavy mark has its own nonempty marked rows.
They therefore exhaust the core kernel, and (2) gives the stated whole
centered-star kernel and rank N-k.

For **any real H certificate**, a largest-star indicator is annihilated
by its nonempty core. Indeed, summing its s diagonal norms s-1 and its
s(s-1) off-diagonal -1 entries gives zero; PSD converts zero quadratic
form to a kernel equation. The equivalence in (2) then forces the centered
star into the whole lower kernel. These k centered indicators are also
independent: an alleged dependence, evaluated at empty, first gives zero
sum of coefficients; evaluating one marked row from each heavy star
then gives each coefficient zero. This proves universal greatest rank.

For any intersecting family of size r, the same core calculation gives
r(s-r)>=0, hence r<=s. At equality its indicator lies in our strict core
kernel and is a linear combination of the heavy-star indicators. At a
private marked row for mark i its coefficient must be 0 or 1. At the old
full set X the sum of all coefficients must be 0 or 1. A nonempty maximum
family therefore selects exactly one coefficient equal to 1: it is one
heavy star. Conversely each heavy star is intersecting and has size s.

## Actual empty energy and the cap limitation

Let e_j=1'C_j1 and A2=sum_i d_i^2. The actual squared norm of the empty
vector in this construction is

```text
B_empty=w-2m+2Dm/q+s*m+(D/q-3)A2
        +(1+D/q)sum_j[e_j+(q-t_j)d_j].             (10)
M[empty,empty]=(B_empty+1-s)/(N-s).
```

To derive (10), split the nonempty sum into the old component
G+sum_i d_i(1/D-1/q)H_i, the marked residual sum, and the private residual
sum. Their squared norms, using (4),(5),(7), add to (10). The checker
compares this separate scalar formula with every actual core entry and
the actual lifted empty loop.

For the cube on X={x,z,r} with private E_1=2^{u,v} attached at x and
E_2=2^{b} attached at z, N=16,s=7,k=1. Formula (10) gives B_empty=27 and
the explicit output has M[empty,empty]=7/3>1. It satisfies H with greatest
lower rank 15, but cannot satisfy M<=I. This is an exact limitation of
the supplied output, not nonexistence of another capped matrix. The small
family is already covered by prior finite work; the new conclusion is
the quantified conditional closure. Capped product transport cannot be
applied to this output without a separate cap construction.

## Exact evidence and trust boundary

The standalone standard-library checker validates every private input
against the original nonempty-core definition. It separately assembles
(9) and the Gram factorization (3),(5)-(8), then compares every entry.
It retains the actual empty vertex and checks symmetry, all row sums,
all original-set support entries, exact PSD and ranks of the core and
whole lower matrix, every heavy-star kernel and (10).

Fifteen fixtures cover n=2 through 6, through N=72, including repeated
marks, one and multiple heavy marks, private uniform rank-two inputs,
private size greater than q with star strictly below q, and four equality
boundary cases. They compare 15,351 ordered original core positions.
Six bounded complete original-set maximum-family censuses match the heavy
stars, one 256-position ground-set permutation agrees entry by entry,
and eleven malformed-input/matrix controls are rejected. Normal and
assertion-disabled records agree on every mathematical field.

Cube complement inputs and uniform rank-two inputs are credited baseline
reproductions, not new certificates. Their core hashes are retained.
The matrix table and Gram assembly are by the same author; agreement is
not independent peer review. The ordinary Gram realization, complete
rank decomposition, all-real maximality and maximum-family arguments
above remain unformalized. Uniform coverage follows from these arguments,
not extrapolation from fixtures. No solver, floating-point result,
enumeration corpus, timeout or incomplete computation is a proof input.
General H and I, unrestricted attachment closure and the upper cap of
the present construction remain outside the result.
