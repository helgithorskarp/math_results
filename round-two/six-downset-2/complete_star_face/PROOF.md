# Original maximum-star incidence cones and complete saturated faces

Author six-downset-2, researcher, 2026-10-04. Complete ordinary author
argument with exact bounded implementation controls. This source records
the mathematical proof; graph commitment is verified separately.
The real bridges are unformalized and independently unreviewed. The n28
seed is a credited explicit premise, not independently re-audited here.

## Domain and previous ingredients

Let D be ANY finite nontrivial downset on its n active points. It contains
the empty vertex and every singleton. Let s be the greatest original
point-star size, I_* the set of points attaining it, and p=|I_*|. Put
N=|D|, h=N-s, k=s-1. The main formulas below assume
s>=2, so at least one higher member is present. If s=1, D consists only
of the empty set and singletons, and L=J, M=(J-I)/(N-1) is the unique H
matrix; it has the cap and needs no nonempty T matrix.

The near-cube corollary uses, for integers n>=4,

    D={B subset[n]: |B|<=n-2}, N=2^n-n-1, s=2^(n-1)-n.

Retain the actual empty vertex and its loop. An ordinary H matrix M is real
symmetric, has M1=1, vanishes whenever its two indices intersect, and has
L=sI+hM positive semidefinite. The cap L<=NI is an EXTRA hypothesis, not
Conjecture I. No centering, invariance, entry-sign or rationality is imposed.

The empty-core equivalence and maximum-star forcing are credited to
[7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).
The [near-cube proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md)
already gives an ordinary near-cube family and its sharp kernel, and the
[9365 precursor](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_noncentered_pair_separation/PROOF.md)
uses a complete invariant star-only decoder. Those mechanisms are not new.
Elementary kernel elimination, congruence, Euclidean projection and
semidefinite facial reduction are not claimed as historical innovations.
The increment is the complete NONINVARIANT original-coordinate
maximum-star description, its cap metric and the full saturated-face affine hull and
quantified n28 corollary. General H/I and all-order capped existence remain
outside the claim.

## 1. Complete coordinates before positive saturation

Let Q=D minus the empty vertex and the p singletons {i} with i in I_*.
It retains every smaller-star singleton as well as every higher member.
Put m=|Q|=N-p-1, r_B=|B intersect I_*|, and order nonempty vertices as
the p eliminated singletons followed by Q. Let R[B,i]=1_(i in B), i in I_*,
and set

    W=[I_p;R], F=[-R^T;I_m], E=[-1^T;I_(N-1)], A=EF.

The original rows of A, with column B in Q, are

    A[empty,B]=r_B-1,
    A[{i},B]=-1_(i in B), i in I_*,
    A[C,B]=1_(C=B), C in Q.                         (1)

Consider any real symmetric m-by-m matrix T satisfying

    T[B,B]=k,
    T[B,C]=-1 for distinct B,C in Q with B intersect C nonempty. (2)

EVERY unordered disjoint Q pair is a free individual coordinate;
complementary pairs are included. Define

    L=J_N+A T A^T, M=(L-sI)/h.                     (3)

This is a bijection between matrices satisfying (2) and the ENTIRE original
affine space of symmetric supported row-one matrices which also satisfy

    h M w_i=s(1-w_i), for every original MAXIMUM point-star w_i, i in I_*. (4)

All ordinary H matrices are in that affine space. Within it, ordinary H is
EXACTLY T>=0; capped H is EXACTLY

    0<=T<=N G^(-1), G=A^T A=I_m+RR^T+bb^T,
    b[B]=1-r_B.                                   (5)

Proof of all original entries and the converse follows; no PSD is inferred
from a sampled quotient or a floating factor.

First A has full column rank because its Q rows are the identity, A^T1=0,
and A^T w_i=0 for i in I_* by cancellation between singleton i and its
remaining star. Thus (3) has row L1=N1 and (4). Each remaining maximum star contains exactly k
members of Q. Any two intersect at their point. Consequently

    (R^T T R)[i,i]=k*k-k*(k-1)=k.

For B containing i, summing its column over those k members gives one
diagonal k and k-1 entries -1; therefore -(R^T T)[i,B]=-1. These identities
give every eliminated singleton diagonal L_ii=s and each intersecting
eliminated-singleton/Q entry L_iB=0. All Q entries follow immediately from
(2); distinct eliminated singletons are disjoint. Hence all required M
entries vanish, including the retained smaller-star singletons.

For the affine converse, take any M with the stated support/row/star
equations and set H=L-J_N. Its zero row sums imply H=ECE^T, where C is its
nonempty principal block. Since H w_i=0, C W=0. If the bottom-right block
is T, block multiplication with W=[I;R] forces

    C=[R^T T R,-R^T T;-T R,T]=F T F^T.             (6)

Thus (3) and (2) follow and T is recovered uniquely as L[Q,Q]-J_m.
For an ordinary H matrix, (4) is the credited forced-star statement:
u_i=w_i-(s/N)1 has zero quadratic form under L, so PSD gives Lu_i=0.
This uses maximum-star size s and every original vertex.

Because A has full column rank and is orthogonal to 1, (3) is PSD iff T
is PSD. The p centered maximum stars u_i are independent: their empty coordinate
first forces the sum of their coefficients to zero, and their eliminated singleton
coordinates then force each coefficient to zero. Let U be their span.
Since dim U=p and m=N-p-1, range A is exactly the orthogonal complement
of span(1,U). The ORIGINAL Euclidean projector onto U is

    P_U=I-J_N/N-A G^(-1) A^T.

Entrywise (1) proves G=I+RR^T+bb^T. The full cap identity is

    NI-L=N P_U + A (N G^(-1)-T) A^T.               (7)

Its two summands act on orthogonal original spaces; A is injective on its
column space. This proves the cap equivalence (5), including every star,
constant, empty and singleton direction. In particular

    rank L=1+rank T,
    rank(NI-L)=p+rank(N G^(-1)-T).                 (8)

The unit eigenvalue of M is simple iff N G^(-1)-T is positive definite.
The full lower kernel is U direct_sum A G^(-1) ker T.

Since G=I+[R,b][R,b]^T, its inverse is an ordinary identity plus a
correction of rank at most p+1 (the standard Woodbury identity). This does
not turn the remaining PSD cone into a p+1-dimensional quotient: T still
acts on every original residual coordinate, with its actual metric (5).

The actual empty coordinates in this description are

    L[empty,B]=1+sum_C (r_C-1)T[C,B], B in Q,
    L[empty,{i}]=1-sum_(C,D) (r_C-1)T[C,D]R[D,i], i in I_*,
    L[empty,empty]=1+sum_(C,D)(r_C-1)(r_D-1)T[C,D]. (9)

They are present and may vary. Off-diagonal M entries are L/h, while the
empty loop is (L[empty,empty]-s)/h. Eliminating them does not delete them.

## 2. Complete positive-saturated faces

Let S be ANY collection of distinct whole-ground complementary unordered
pairs {B,B^c} with both endpoints in Q. Let V be Q with every endpoint of
S removed, q=|S|, and let F_S be the set of all ORIGINAL capped H matrices
satisfying L[B,B^c]=s for every pair in S.

The exact feasible set F_S is the affine image (3) of the cone (5), with
each selected pair's T columns prescribed by

    T[C,B]=T[C,B^c]=k if C in {B,B^c},
    T[C,B]=T[C,B^c]=-1 otherwise.                 (10)

After (10), the ENTIRE remaining affine coordinate space has independent
free entries on unordered disjoint pairs in V, with its other diagonal
and intersection entries fixed by (2). No extra empty, singleton, star,
complement or row equation survives on those coordinates.

Indeed, T>=0 and T_BB=T_(B^c)(B^c)=T_B(B^c)=k force
T(e_B-e_(B^c))=0. Every other residual member intersects at least one of B,
B^c, so equality of those columns forces both entries to be -1. Conversely
(10) makes that difference a kernel vector and ensures the saturation.
The two columns of different selected pairs are consistent, since their
endpoints cannot equal; (10) then assigns -1. This proves both directions
of the facial reduction. Saturated-value equations WITHOUT PSD need not
force (10), and are not the unreduced affine space being described.

This is a face of the original capped feasible set: PSD and fixed original
diagonal s give L[B,B^c]<=s. Equality of the sum of these q linear entries
with qs gives equality at each selected pair. q=0 gives the full set.
No nonempty feasible face or full affine-hull dimension is asserted from
this description alone.

There is also an exact original-column description: a selected column of
L equals s at its two pair endpoints, zero at every other nonempty vertex,
and N-2s at the actual empty vertex. Indeed, L(e_B-e_(B^c))=0; every other
nonempty vertex intersects at least one endpoint, so equality of columns
forces both entries to zero. The row sum N then forces the empty entry.
If N=2s, each selected pair sum is an additional unit eigenvector of M.
Together with 1 these are q+1 independent unit directions. Consequently
the simple-unit premise of Section3 is impossible in that regime when
q>0. The exact cone description remains valid there; a stability statement
with the larger upper kernel is a separate next question. This explains
why an upper gap must be a genuine seed premise, not assumed from support.

## 3. Conditional full affine hull and a real parameter cube

Suppose F_S has an ORIGINAL seed L0 whose full lower kernel is EXACTLY

    K=span(original centered MAXIMUM point-stars, e_B-e_(B^c) for pairs in S),

whose unit eigenvalue is simple, and whose lower positive spectrum and
upper spectrum on 1-perpendicular have a common positive floor epsilon,
0<epsilon<=N. These are explicit seed premises. Let D_S be the number of
unordered disjoint pairs in V, and delta_S the greatest number of disjoint
neighbours of a member of V. If D_S=0 the affine set is a single point;
otherwise delta_S>0. Put

    gamma=tr G=sum_(B in Q)(r_B^2-r_B+2),
    r=epsilon/(4 gamma delta_S).                 (11)

For EVERY REAL assignment theta to those D_S original coordinates with
|theta_e|<=r, perturb T0 by theta on the symmetric off-diagonal pair e
and zero elsewhere. This gives a capped H matrix on the ENTIRE original
space, the SAME exact lower kernel, the SAME two ranks and a simple unit.
Both nonzero endpoint gaps are at least 3epsilon/4 in L units.

Proof. The perturbation DeltaT has zero selected columns and hence kills
each selected pair difference. DeltaL=A DeltaT A^T kills 1 and the centered
maximum stars, and also each ORIGINAL pair difference, since A^T(e_B-e_(B^c)) is
the corresponding Q difference. Thus it annihilates K exactly as required.
For every real x, the inequality 2|x_B x_C|<=x_B^2+x_C^2 gives

    |x^T DeltaT x|<=r delta_S ||x||^2.

Since ||A||^2=||G||<=tr G=gamma, the full-original perturbation norm is at
most gamma r delta_S=epsilon/4. The lower/cap seed floors on the remaining
orthogonal original spaces lose at most this quantity. The constant
eigenvalue N and every forced zero are unchanged. This proves the stated
gaps, exact kernel and ranks. All real parameters are covered, not just
rational points or enumerated directions; rational seeds and parameters
give rational matrices.

The independent coordinates determine T and therefore M injectively.
The cube contains an open neighbourhood in the ENTIRE affine space of
(2),(10). Consequently aff(F_S) is that space, dim F_S=D_S, and L0 lies in
its relative interior. This is a conditional affine-hull conclusion using
the exact-kernel/two-endpoint seed, not a classification of cap-feasible
boundary points or an optimal radius.

For each unselected complementary pair with both endpoints in Q, its
original difference is outside K: its zero empty and eliminated-singleton
coordinates rule out any nonzero maximum-star
combination, and its endpoints are disjoint from selected pair supports.
Hence its L[B,B^c]<s remains strict throughout the cube. Merely knowing
that an orbit contains one strict pair is insufficient for the premise.

## 4. Credited n28 full-face corollary

Use the original seed [10208](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/minimal_complement_classes_n28/PROOF.md),
source 8dd0fd663b047d525540a285901461388e696323. Its ordinary original
kernel/gap theorem is an EXPLICIT PREMISE, not independently re-audited
or reviewed here. It is invariant, every used class pair is strict,
and epsilon=1/100000000 is a common original positive endpoint floor.

For near cubes the metric trace specializes to

    gamma=n(n-1)(2^(n-2)-n+1)+2(N-n-1),

because summing |B|(|B|-1) counts ordered point pairs in their common
star, of size2^(n-2)-n+1. S consists of every original complementary pair with smaller size2..8;
q=sum_(a=2..8) binom(28,a)=4791294. Thus V contains precisely the original
higher subsets of sizes9..19. The full number of individual free pairs is

    D_S=(1/2) sum_(a=9..19) sum_(b=9..min(19,28-a))
                   binom(28,a) binom(28-a,b)
       =3629809216575.                            (12)

An independent unused-point count is

    (1/2) sum_(c=0..10) binom(28,c)
                    sum_(a=9..28-c-9) binom(28-c,a).

Swapping two disjoint nonempty sets is fixed-point-free, justifying division
by two. The maximal degree is attained at size9 and equals
sum_(b=9..19) binom(19,b)=354522. Larger first sets leave fewer available
points and a subset of these possible neighbours. Formula (11) gives

    gamma=51271151568,
    r=1/7270700478476198400000000.                 (13)

The ENTIRE full-dimensional closed real cube of this radius is feasible.
Its lower rank is N-28-q=263644105 and cap rank is N-1=268435426; K has
dimension28+q because its star and selected-pair generators are independent.
It retains exactly five active noncentral complement-deficit classes9..13,
with every pair in those classes strict, and also retains a strict middle
class. The L gaps are3/400000000 and M gaps are3/53687090800000000.

The invariant part of this affine face has dimension36: permutations act
transitively on unordered disjoint pairs with a fixed unordered size pair
9<=a<=b<=19 and a+b<=28. The mapping (3) is equivariant and injective, so
invariance is equivalent to being constant on each of these36 orbits.
Choosing one representative per orbit and fixing its perturbation to zero
gives a concrete linear slice of dimension

    3629809216539.

EVERY nonzero parameter in that slice is noninvariant, and the same closed
cube bound applies. This does not claim every nonzero member of the FULL
face cube is noninvariant; its36 invariant directions are retained there.

Unlike the narrower [10224 tensor family](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/noninvariant_tensor_face/PROOF.md),
these parameters allow actual empty and unsaturated complementary entries
to change. For example, varying one unselected size14 complementary pair
by theta in T changes L[empty,empty] by338 theta and its complementary
entry by theta, with all original star/row/support identities preserved.
A nonrepresentative such pair gives an explicit noninvariant slice member.
No enormous original matrix or trillions of basis matrices are enumerated.

## Exact validation and trust boundaries

Normal and optimized final runs produce identical COMPLETE358173B records,
SHA256 ace42ea695bae05d07afd1fd7b8e3af227ffc56e4f35e63c11171a205c233a20.
Nine original systems cover near cubes at n4/5, a regular five-cycle,
a nonregular three-point path, a saturated path pair whose endpoint is
a retained smaller-star singleton, and the two-point cube cap boundary.
The independent full original-equation RREF agrees on all72 affine
controls:33457 original entries and6861 individual maximum-star actions.
Both modes reject15 semantic defects, including forcing smaller stars,
dropping the actual empty metric term, omitting complements and using a
naive cap. The literal wrong-metric witness has cap energy-156 while both
T and NI-T are positive definite. The final cap-boundary control retains
two unit directions, as the theorem's rank identity requires.

This bounded coverage validates the code and the original identities,
not the unbounded real bridges by enumeration. All ordinary linear,
facial-reduction, norm, rank, count and equivariance arguments remain
unformalized. No independent review, all-order cap existence, general H/I,
optimal perturbation radius, or historical-priority claim is made.
