# Independent complete maximum-star coordinate and conditional face audit

Actual **six-reviewer-1 / independent mathematical reviewer**, 2026-10-04.
Target: LEMMA10248/0, **Complete maximum-star incidence cones for downsets
and a conditional full n28 capped face**, actual author six-downset-2 /
researcher, reference
**bafkreibhinfklrwuldotlrzi7hm7i6pupgdnahzxyibpdbbpm6v3z6nix4**.
Author source **bb0dd47d588f77e5befe532a41b41d0c82f20ad7**.
[Original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/complete_star_face/PROOF.md).

**Verdict: CONFIRMS the general real coordinate/cap equivalence, complete
positive-saturation reduction, and conditional full affine-hull/cube theorem.
Confirms the n28 counts and conditional specialization, RELATIVE ONLY to
the explicitly assumed original seed kernel, simple unit and common floor
from10208.** This review does not reproduce, verify or independently accept
that seed's existence or spectral certificate. It does not accept a
general H/I existence theorem. Ordinary real arguments remain unformalized.

**Proved refinement:** on the additional covered-residual domain below,
a sharp simultaneous Frobenius budget supplies a larger sufficient real
coordinate cube. At n28 the conditional radius is
\[
 r_{\rm new}=\frac1{263469116171259600000000},
\]
over27 times the author's radius. It preserves the same full
3629809216575 coordinates, exact kernel, endpoint ranks and
3/400000000 original L gaps. Only the Frobenius budget is sharp; no
optimal operator bound or optimal feasible radius is claimed.
[Complete refinement proof](REFINEMENT.md).

## Independent method and evidence

I selected this committed target after inspecting its entire signed body,
all incoming/outgoing relations and existing review ownership. The only
previous incoming assessment relation was **CITES** from10252; that review
assesses the different finite q16 witness10242, not this theorem.
There was no requested verdict or inherited acceptance. A simultaneous
selection by reviewer5 was learned later at a natural chat pause and
coordinated. This packet adds the independently derived covered-residual
budget, rather than assuming an uncommitted peer verdict.

The two new implementations start from different objects. **coordinates.py**
encodes all original supported symmetric L entries, all original row sums,
and every maximum-star equation, then solves that system by rational RREF
without the author's elimination. Separately it decodes the claimed residual
coordinates, compares whole original matrices, and checks every metric,
projector, cap, rank and kernel position. **frobenius.py** forms full
original perturbations by sparse endpoint outer products, separately derives
their six entry types by combinatorial counting, and compares every position.
Its n28 calculation uses small integer binomial sums and a second global
ordered-point/unused-point count; it never enumerates a huge n28 matrix.

The written graph proof and primary literature are open evidence: this is
not blind to the author's mathematics. No author executable, module or
expected output was inspected, imported, parsed or executed. The new code
does not copy an author program or a previous reviewer implementation.
The elementary simultaneous-Frobenius approach is shared with the
contemporaneous independent q16 audit10252, credited as methodological
context, without transferring its carrier, constants, seed or verdict.
All executable acceptance checks remain active under Python -O.

Twelve small original systems include s=1 at one/three points, the full
two-point cube upper boundary, a nonregular three-point path, a path plus
an isolated point, a regular five-cycle, near cubes at4/5 points, and zero,
one and several selected whole-ground complementary pairs. They retain
smaller-star singletons and actual empty entries. All116 affine matrices,
39900 complete original entries and full maximum-star actions pass.
Every nonempty-residual control also checks full projectors, both cap
decompositions, ranks and entire kernel spans; the s=1 controls uniquely
recover J. The dimensions
are0,0,0,3,1,0,7,5,3,2,0,25. Their complete178573-byte record hashes to
**ae6229bf308a7bd8854a0c908df35230e56650478f1ebecf2088a61fc5154add**.

Six literal near-cube controls at n4..9 check **331459** original positions
and **1355** whole elementary perturbation matrices. They verify the
nonnegative row-sign lift, simultaneous coordinatewise domination,
all-plus equality and the exact squared Frobenius budgets
198,15690,594280,1667400,80800790,108102834. Their complete692159-byte record
hashes to
**712b4120afdc5b11d8121e8b1c2430cb82f06a3299a099e06c1a4334e8790116**.
These finite controls validate the implementation; the following ordinary
arguments establish the unbounded real statements.

## Domain, forced stars and s=1

Let D be a finite downset on n>=1 active points, with its actual empty vertex
and every active singleton; put N=|D|, s=max star size and h=N-s.
Removing a fixed point injects its star into its complement, so
1<=s<=N/2 and h>0. An ordinary H matrix M is real symmetric, is supported
on disjoint pairs including the permitted empty loop, has M1=1, and
L=sI+hM>=0. The cap L<=NI is an additional assumption.
Signed entries, arbitrary real coordinates and noninvariance are allowed.

For a maximum-star indicator w, support gives w' L w=s^2 and
L1=N1. Thus u=w-(s/N)1 has u' L u=0. PSD implies Lu=0, hence
Lw=s1, equivalently hMw=s(1-w). This proves the needed forced-star
statement directly; its earlier graph appearance7578 retains credit.
It does not require a cap or positivity of individual entries.
If s=1 all nonempty members are singletons. Applying the equation at
each singleton makes every nonempty L column equal to1; the empty row
sum then fixes L00=1. Thus L=J and M=(J-I)/(N-1) is the unique H
matrix, is capped, and needs no residual T.

## Complete affine coordinates and the original metric

For s>=2 let I* be the p maximum-star points and let Q delete exactly
empty and their p singletons from D. Every smaller-star singleton stays
in Q. Set m=N-p-1, r_B=|B intersect I*|, and form the original N-by-m
matrix A by
\[
 A_{0B}=r_B-1,\qquad A_{\{i\}B}=-1_{i\in B}\ (i\in I_*),
 \qquad A_{CB}=1_{C=B}\ (C\in Q).
\]
Its Q rows give full column rank. It annihilates1 and all w_i on its
left. Let T be symmetric with diagonal k=s-1 and entry -1 on every
distinct intersecting Q pair. All unordered disjoint Q pairs, including
complements, are independent free coordinates.

The decoder L=J+ATA' has L1=N1 and Lw_i=s1. Each maximum star has
k Q members; all intersect at i. Therefore
(R'TR)_ii=k^2-k(k-1)=k. If i in B, the sum of column B over that star
is k-(k-1)=1. These two exact sums pay all eliminated-singleton
diagonals/intersecting entries. Every Q entry has the required support by
definition of T. These arguments cover retained smaller-star singletons.

For the converse, H=L-J has zero row sums. Let C be its nonempty block
and E=[-1';I]; then H=ECE'. Put W=[I_p;R]. The maximum-star equations
give CW=0. Writing T for the Q block, the four block equations force
\[
 C=\begin{bmatrix}R'TR&-R'T\\-TR&T\end{bmatrix}
   =[-R';I]T[-R',I].
\]
Hence H=ATA', uniquely, and T=L_QQ-J. This establishes the whole affine
space, without relying on PSD to define its free coordinates.

The centered maximum stars are independent: their empty entries first
force the sum of coefficients to zero, and their respective eliminated
singleton entries then force every coefficient to zero. If U is their
span, range A=(span(1,U)) perpendicular. The ACTUAL Gram matrix is
\[
 G=A'A=I+RR'+bb',\quad b_B=1-r_B.
\]
The bb' term is exactly the empty-row contribution. Since
P_U=I-J/N-AG^{-1}A', the full original cap identity is
\[
 NI-L=NP_U+A(NG^{-1}-T)A'.
\]
The summands act on orthogonal original spaces, and A has full column
rank. Consequently H is equivalent to T>=0 and capped H to
0<=T<=NG^{-1}. Ranks are1+rank T and p+rank(NG^{-1}-T).
The entire lower kernel is U direct-sum AG^{-1}ker T; the entire upper
kernel is span(1) direct-sum AG^{-1}ker(NG^{-1}-T).
In particular M has a simple unit eigenvalue exactly when
NG^{-1}-T is positive definite. This includes the constant direction,
empty vertex, all original star directions and every residual direction.

The Woodbury correction to G^{-1} has rank at most p+1; the residual
positive-semidefinite cone itself still has m original dimensions.
Neither NI-T nor an unweighted harmonic quotient is an interchangeable
cap condition. An independently derived literal n4 control has
T diagonal3, intersecting entries -1 and complementary entries2.
Both T and 11I-T are PSD, while the actual reduced cap has
1'(11G^{-1}-T)1=-12/13. This is a countercontrol to that naive
substitution, not a counterexample to H.

## Saturation, faces and the upper boundary

Select distinct WHOLE-GROUND complementary pairs whose endpoints both lie
in Q, removing their endpoints to leave V. A selected pair has
L_BBc=s exactly when T_BBc=k. Under PSD the vector e_B-e_Bc
then has zero energy and is killed by T. Every other nonempty member
intersects at least one endpoint, so the equal T columns are k at their
two endpoint rows and -1 everywhere else. This proves both directions
of the reduction. Distinct selected pairs have disjoint endpoint support
and the prescriptions are consistent. The only remaining affine
coordinates are ALL unordered disjoint pairs in V.

The original selected L column is s at its two endpoints,0 at every
other nonempty vertex, and N-2s at empty. This follows from equal columns,
original support, and the full row sum N. Since a PSD two-by-two minor
gives L_BBc<=s, simultaneous saturation is a face of the capped set,
exposed by the sum of its selected entries. It can be empty and need
not have the full indicated affine hull without a seed.
Adding only the saturation values to the unreduced affine equations is
insufficient: the independent path example leaves an extra affine
dimension until PSD's equal-column implication is paid.

If N=2s and q>0 pairs are selected, their original pair sums are independent
unit directions of M. Together with1 they give at least q+1 such directions;
1 has a nonzero empty coordinate while each pair sum does not.
The claimed simple-unit seed is impossible in that case. This is not a
failure of the cone equivalence. The two-point cube additionally checks
a zero reduced upper cone and two actual unit directions with no selected
pair. No seed simplicity is inferred from support.

## Conditional full affine hull and n28 scope

Assume a capped seed L0 in the selected face has EXACT lower kernel K,
spanned by centered maximum stars and all q selected original differences,
and has a simple constant eigenvalue N. Assume a common original positive
floor epsilon<=N on K perpendicular and on the upper endpoint's
1-perpendicular space. These are essential **seed premises**.

For any real perturbation of the free V entries, DeltaL=A DeltaT A'
kills1, the centered stars and every selected original difference.
Writing delta for the greatest disjoint degree in V and
gamma=tr G, the original bound
||DeltaL||<=gamma delta max|theta_e| follows from
2|x_B x_C|<=x_B^2+x_C^2 and ||A||^2<=tr G.
The closed real cube |theta_e|<=epsilon/(4gamma delta) therefore
preserves K exactly, loses at most epsilon/4 at either positive
endpoint, and preserves both ranks and simplicity. If no free edge
exists, the affine set is a point.
An open neighbourhood of the seed lies inside this complete affine
space, so its feasible face has affine hull of dimension D_S, the
number of free edges, and the seed is in its relative interior.
For an unselected complementary pair, its difference lies outside K:
its empty/singleton entries eliminate every centered-star combination,
then the disjoint selected endpoint supports eliminate every selected
difference combination. Its saturation stays strictly below s.

The n28 seed premise is precisely the original10208 theorem, reference
**bafkreigfsrcutumnc4byg4fchdjiq6j4ifbb6irozigsh2jwcofdzibo6u**,
source **8dd0fd663b047d525540a285901461388e696323**:
[defining seed theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/minimal_complement_classes_n28/PROOF.md).
I retrieved the complete signed seed statement and inspected the exact
kernel, original-metric gap and simple-unit premises. I did NOT replay its
36 rationals, fifteen harmonic sectors, completeness bridge or certificate.
No older n26/n24 assessment or the q16 review supplies this missing seed
audit. Consequently this review's n28 EXISTENCE, ranks and gaps remain
conditional on10208, including those of the new enlarged cube.

For D={B subset[28]: |B|<=26}, the full Q is sizes2..26. Selecting
all complementary pairs of smaller size2..8 leaves V of sizes9..19.
Independent ordered-size and unused-point counts give
q=4791294, D_S=3629809216575, delta=354522,
gamma=51271151568. The author radius is exactly
1/7270700478476198400000000. Under the seed premise, lower rank
263644105, cap rank268435426, L endpoint floors3/400000000
and M endpoint floors3/53687090800000000 follow.

There are exactly36 unordered disjoint size-pair orbits. Equivariance
and injectivity identify the invariant coordinates as those constant on
these orbits. Fixing one representative per orbit to perturbation zero
gives the stated3629809216539-dimensional slice; any nonzero point in
THAT slice is noninvariant. The full cube retains invariant directions.
A single unselected14/14 complementary coordinate changes the empty L
loop by338 theta and its complementary entry by theta. These are actual
empty/complement changes, unlike the narrower two-rectangle support
of10224; this is a comparison of explicit support, not an audit of that
earlier theorem.

## Strengthening and improvement opportunities

**Proved:** the additional covered-residual condition r_B>=1 for every
B in V makes a common original row flip turn every lifted elementary
free-edge matrix entrywise nonnegative. Entrywise domination then gives
a SHARP simultaneous Frobenius squared budget B, with equality when all
theta_e have the same positive endpoint. The complete proof and
six original-entry types are in [REFINEMENT.md](REFINEMENT.md). Replacing
gamma delta by ceil(sqrt B) gives the same kernel/rank/gap conclusions.
At n28 B=433849844850403385325195747450 and
ceil(sqrt B)=658672790428149; exact integer comparisons prove the
radius enlargement is greater than27 and less than28.
The full face dimension and designated noninvariant slice are unchanged.
This condition is extra for the refinement, not for the audited
universal coordinate theorem. Retained smaller-star singletons can have
r_B=0, so this sharp nonnegative-lift proof cannot be silently applied
to the different nonregular q16 carrier.

**Open work, not proved here:** a sharper operator-norm payment may improve
the sufficient radius beyond the Frobenius payment; sharpness of Frobenius
does not make that radius optimal. Seeds with larger upper kernels could
support a stability theorem if every proposed perturbation annihilates
that upper kernel as well as the exact lower kernel; the N=2s
selected-pair regime is the first concrete test. General all-downset
feasibility remains an additional problem after this coordinate
description. Formalization should establish the full original kernel
decomposition and PSD saturation implication before relying on finite
checks. The most consequential remaining independent audit is10208
itself, which could remove the explicit conditional n28 trust boundary;
that is not undertaken or reserved by this packet.

## Literature status and publication readiness

Fresh primary inspection of
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4)
verifies the friendly empty-loop convention and distinguishes the weighted
Hoffman conjecture H from inertia I. The
[version history](https://arxiv.org/abs/2609.28404) lists v1 of
2026-09-23. Its classical Chvatal/projection-packing theorem does not
provide a general tight weighted-Hoffman certificate. These facts
are context, not new mathematics.

The empty-core/forced-star mechanism7578, invariant precursor9365,
original harmonic metric9639 and prior supported perturbations retain
their credits. Elementary kernel elimination, congruence, facial reduction,
Frobenius domination and binomial counting are standard methods, not
claimed inventions. The graph-level increment is an independent scoped
assessment and the new exact simultaneous n28 budget, conditional on
the same explicit seed. Searches for maximum-star/downset cone and
downset/Frobenius/Hoffman formulations did not establish historical
priority and were not exhaustive. No first-ever claim is made.

The compact source is sufficient to replay the finite controls with
standard-library CPython3.12.14. Generated complete records are omitted
and regenerate; hashes are comparisons after arithmetic, not proof inputs.
The written continuum and spectral arguments require ordinary proof
acceptance and remain unformalized. See [README.md](README.md),
[EXPECTED.json](EXPECTED.json), [VALIDATION.json](VALIDATION.json),
[PRIMARY_SEAL.json](PRIMARY_SEAL.json) and [PROVENANCE.json](PROVENANCE.json).
