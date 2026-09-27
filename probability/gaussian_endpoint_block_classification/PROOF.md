# Endpoint-block classification and an eight-label Gaussian frontier

27 September 2026. Complete author proof, independent review pending.
The unrestricted dimension-three Gaussian-majorisation problem remains
open. This packet gives an actual all-variance sign certificate and an
exact classification of a finite type of factorization. It does not
assert necessity for Gaussian positivity or classify continuous motions.

The analytic inputs are the accepted R8 norm-preserving theorem and the
classical two-dimensional-displacement lift. No R5 exclusion result is a
premise. The new steps are the three-mover dichotomy, the exact ordering
classification, and its consequence for the rooted finite frontier.

## 1. Three moving points, with arbitrarily many fixed points

Let K be a bounded subset of R3 and T:K->R3 be 1-Lipschitz. Suppose T fixes
K outside at most three points. Then every probability law mu on K obeys

    integral (T#mu * gamma_s - h)_+ >= integral (mu * gamma_s - h)_+  (1)

for every variance s>0 and threshold h>=0. In particular the fixed part
may be diffuse. Every finite center selection in K obeys both individual-
radius Kneser--Poulsen inequalities: unions decrease and intersections
increase. The same holds after applying an independent rigid motion to
either endpoint configuration.

Here and below the independent endpoint motions in this last statement
preserve the conclusions; a supplied-coordinate certificate is not claimed
to be invariant under independently changing those frames.

For each moved point write

    v_i=q_i-p_i,    b_i=(|q_i|^2-|p_i|^2)/2.

There are two elementary positive cases, valid for any number of movers:

**Plane case.** If all v_i lie in a vector plane V, the classical leapfrog

    z_i(t)=((p_i+q_i)/2+cos(pi t)(p_i-q_i)/2,
                              sin(pi t)(p_i-q_i)/2)             (2)

lives in R3 x V, of dimension at most five. All unchanged points have zero
extra coordinates. Squared pair distances are

    (1+cos(pi t))/2 * |p_i-p_j|^2
       +(1-cos(pi t))/2 * |q_i-q_j|^2.

They decrease with t. Aishwarya--Li's continuous-contraction theorem and
two-coordinate Gaussian transfer give (1). Bezdek--Connelly Theorem1 and
Corollary3 give both arbitrary-radius ball inequalities. This case is
credited prior work, not a new motion construction.

**Anchor case.** If the linear equations

    v_i dot c = b_i                                             (3)

are consistent, then |p_i-c|=|q_i-c| for every mover. The equality holds
automatically for every fixed point. The accepted norm-preserving theorem
therefore gives (1) and both ball inequalities. The anchor c need not be
a support point, lie in the convex hull, or have bounded size uniformly
over the family. Each particular bounded input has a finite anchored
radius; the imported theorem holds at every positive variance.

With at most three movers either their displacement rank is at most two,
or there are exactly three independent displacement vectors. In the latter
case (3) is a nonsingular three-by-three system. These two cases exhaust
all inputs, including all rank degeneracies and coincident target points.
This proves the assertion. No norm bound on the inverse matrix or positive
weight floor is needed because the sign is exact, not perturbative.

For a finite list and a block B of its movers, call B **admissible for the
two primitives** when

    rank D_B <= 2,  or  rank[D_B | b_B] = rank D_B,               (4)

where D_B has the displacement row vectors. This is a precise name for
the two sufficient hypotheses above, not a characterization of all
positive contractions. Every block of at most three movers satisfies (4).

## 2. Exact ordering constraints from four endpoint distances

Now let P=(p_i), Q=(q_i), 1<=i<=N, be finite configurations with Q a
contraction of P. Let M={i:p_i!=q_i}. An **endpoint-switch chain** means
that each i in M changes once, from p_i to q_i, in an ordered sequence
of nonempty simultaneous batches. No other intermediate locations are
allowed, and every step must contract all pair distances. This is a
discrete factorization into genuine contractions, not a claim that its
jumps trace a continuous contraction in physical R3 or R5.

For i,j in M, put

    U_ij=|p_i-p_j|^2,   L_ij=|q_i-q_j|^2,
    A_ij=|q_i-p_j|^2,   A_ji=|p_i-q_j|^2.

Build a directed graph G on M by the rule

    j -> i  precisely when A_ij is outside [L_ij,U_ij].         (5)

Thus j->i prohibits i from switching strictly before j. If i changes
first, the squared distance of that pair visits exactly

    U_ij, A_ij, L_ij.

This sequence is nonincreasing exactly when A_ij is in the displayed
closed interval. If they change simultaneously, the only values are U_ij
and L_ij, already ordered. A pair containing a fixed label contributes
no extra ordering constraint: its only transition is directly between
its source and target distance. Consequently a batch assignment t_i is
an endpoint-switch chain if and only if

    t_j <= t_i for every edge j->i.                            (6)

This checks both excessive expansion and excessive early contraction.
Testing only the upper bound in (5) would give an incorrect classifier.

## 3. Complete component classification

Let C_1,...,C_l be the strongly connected components of G. Along any
directed path, (6) propagates. Vertices in the same component must
therefore have equal switch time. Conversely the condensation graph is
acyclic. Switch one entire component at each time, in any topological
order. Equation (6) holds, so every such chain contracts all pairs.

This proves two exact characterizations.

**Theorem A (small batches).** An endpoint-switch chain whose batches have
at most k moved labels exists if and only if every C_a has size at most k.
Equivalently, the smallest possible largest batch has size

    max_a |C_a|,                                               (7)

with value zero for the identity map. In particular, maximum component
size at most three proves (1) at every prior and variance and gives both
arbitrary-radius ball inequalities, by Section1 and finite transitivity.

**Theorem B (the full two-primitive classification).** A switch chain in
which every batch satisfies (4) exists if and only if every C_a satisfies
(4). When this holds, the same Gaussian and ball conclusions follow.

Sufficiency uses the component chain just constructed. For necessity,
failure of (4) means exactly

    rank D_B=3,  rank[D_B | b_B]=4.                             (8)

Both ranks persist when more rows are added. Thus a batch containing a
component that fails (4) also fails (4). Every component must be contained
in a single batch, proving necessity. This is completeness only for the
two specified primitives in endpoint-switch chains, not for arbitrary
norm-preserving factorizations with other intermediate locations or frames.

Collisions cause no gap. If two labels coincide at a stage of a contracting
chain, their distance is zero, so they coincide at every subsequent stage.
Each labelled transition therefore defines a single-valued 1-Lipschitz map
on the actual support. Push forward the current law at each stage; merging
atom masses preserves the argument. Ball radii stay attached to labels.

## 4. Adverse extraction without a loss in the normalized defect

Fix strictly positive weights w_i summing to one, a variance s>0 and a
threshold h. Write Phi(X)=integral(sum w_i gamma_s(.-x_i)-h)_+ and put

    D(P,Q)=sum_(i,j) w_i w_j (|p_i-p_j|^2-|q_i-q_j|^2).

Suppose Phi(Q)-Phi(P)=-delta<0. Along a topological component chain
X^0=P,...,X^l=Q let H_a=Phi(X^a)-Phi(X^(a-1)) and
D_a=D(X^(a-1),X^a). These quantities satisfy the exact telescoping laws

    sum H_a=-delta,    sum D_a=D(P,Q),    D_a>=0.                 (9)

If D_a=0, positivity of the weights and pairwise contraction force every
pair distance in that step to be equal. The two labelled placements are
congruent, so H_a=0. Each component passing (4) has H_a>=0 by the preceding
proof. Thus, among the failing components with D_a>0, there is an a with

    H_a/D_a <= -delta/D(P,Q).                                 (10)

Otherwise summing the strict reverse inequalities for all those components,
and the nonnegative H_a for the remaining ones, contradicts (9), since
their losses sum to at most D(P,Q). In particular D(P,Q)>0.

This extracts a contraction moving precisely one strongly connected,
rank-three, anchor-inconsistent block and having at least the original
normalized adverse value

    (Phi(source)-Phi(target))/(D/s).

No new label, weight, coordinate, variance, or threshold is introduced.
Each coordinate at either extracted endpoint is one of the original p_i
or q_i. Common bounding balls, rational coordinate/weight heights and
any initially fixed labels are therefore preserved. The property that
every distinct pair contracts strictly need not be preserved: fixed
labels in an extracted step have zero loss. This is an exact finite
frontier reduction, not a claim of a practical exhaustive cover.

Without normalization, if r components fail (4), the same telescoping
argument supplies one with H_a<=-delta/r. Every failing component has at
least four movers, hence r<=floor(|M|/4). No adverse input is supplied here.

## 5. A genuine restriction of the rooted indecomposable frontier

The accepted indecomposable reduction tests contractions fixing four
affinely independent labelled points, with a full three-dimensional
distance interval containing only the two endpoint matrices. Its Gaussian
sign remains open. Apply the preceding results in the frame fixing that
tetrahedron.

First, **every contraction in this frame with at most seven distinct
labels is positive**: at most three labels move. Equivalently, every
seven-point contraction preserving the six edges of a nondegenerate
tetrahedron is positive after aligning that tetrahedron. This does not assert the
unrestricted seven-atom theorem, whose endpoints need not share any fixed
tetrahedron. Any adverse witness in the accepted rooted indecomposable
test class has at least eight distinct labels and at least four movers.

Second, in a nontrivial rooted indecomposable pair the graph G on M is
strongly connected. Otherwise a first component in a topological order
gives a nonempty proper switched set and a contracting intermediate R.
It differs as a labelled placement from both P and Q and fixes the same
tetrahedron. Complete distances congruent to an endpoint would force R
to equal that endpoint: a Euclidean isometry fixing a nondegenerate
tetrahedron pointwise is the identity. This contradicts indecomposability.
Strong connectivity alone does not imply indecomposability.

Third, any adverse rooted pair must satisfy (8) on its movers. Rank at
most two is the plane case; consistent equations are the anchor case.
The four independent augmented rows in (8) give an exact nonzero
four-by-four minor. Equivalently there are four mover rows, a nonzero
linear dependence lambda among their displacement vectors, and

    sum lambda_i b_i != 0.                                   (11)

This is a certificate of the remaining algebraic case, not an adverse
Gaussian certificate. It need not constitute a minimal matroid circuit;
some coefficients of the dependence can be zero. For arbitrary inputs
a failed strongly connected component supplies such four rows.

For the rooted frame even separate endpoint anchors cannot avoid the
inconsistency: |p_i-a|=|q_i-b| at four fixed independent points forces
a=b by subtracting their four equations. No assertion about continuous
motion exclusion follows or is needed.

## 6. Unbounded positive examples requiring changing anchors

The classification is not limited to three movers in total. This explicit
asymmetric control has arbitrarily many components, each of size three.
Let alpha=3/4 and let the unit vectors be

    u_1=(1,2,2)/3,  u_2=(2,1,2)/3,  u_3=(6,2,3)/7.

Fix any bounded subset of the nonnegative coordinate orthant pointwise.
For k=0,...,m-1 set L_k=8^k and prescribe

    p_(k,i)=-L_k e_i,    q_(k,i)=alpha L_k u_i,  i=1,2,3.        (12)

All fixed-to-moving pairs contract: the displacement is coordinatewise
positive and (|q|^2-|p|^2)/2=-7L_k^2/32<0. We prove every other pair
contracts through the component order from larger to smaller L.

For two layers L>=8l, let z=u_i dot u_j>0 and a=(u_i)_j>0. The source,
outer-first mixed, and target squared distances are respectively

    U=L^2+l^2-2Ll*1_(i=j),
    A=alpha^2 L^2+l^2+2alpha Ll*a,
    D=alpha^2(L^2+l^2-2Ll*z).

The inequality A>=D is immediate. Also

    U-A >= (1-alpha^2)L^2-2(1+alpha)Ll >=0,

since L/l>=2/(1-alpha)=8. Thus the larger layer may switch first.
The opposite mixed distance is

    B=L^2+alpha^2 l^2+2alpha Ll*(u_j)_i.

As every coordinate of u_j is at least2/7,

    U-B <= (7/16)l^2-(3/7)Ll <0.

The smaller layer cannot switch strictly first. All cross-layer edges
therefore point from the larger layer to the smaller one, never back.

Within a layer the source pair distance is2L^2, whereas the target squared
distance is2alpha^2 L^2(1-u_i dot u_j)<2L^2. Each of the pairs
{1,2} and {1,3} has both mixed distances larger than2L^2, because the
relevant coordinates of u_i exceed7/24 and

    |alpha L u_i+L e_j|^2=L^2(1+alpha^2+2alpha (u_i)_j).

Their bidirectional edges connect all three vertices. There are no
cross-layer cycles, so the components are exactly the m triples.
Theorem A gives the all-prior/all-variance sign and both ball inequalities.

For one triple, the determinant of its displacement matrix at L=1 is
nonzero, and its unique anchor is

    c_0=(-161,-161,-175)/1688;   c_k=L_k c_0.                   (13)

With the four fixed points (2,2,2),(3,2,2),(2,3,2),(2,2,3), the full paired
affine rank is six already for one triple. When m>=2 the whole map has
neither a displacement plane nor a common norm anchor, since c_k differ.
The independent-anchor alternative also fails by the fixed tetrahedron
argument. Thus separate components matter for these two specific global
tests. No exclusion of any other known positive class or factorization
is claimed. The examples are controls for the classification, not a new
motion-obstruction family or a historical novelty claim.

Replacing L_k by8^-k for all k>=0 and adding the fixed point0 gives a
bounded countable example. Approximate a supported law by retaining
finitely many triples and moving the tail mass to0; the tail input and
output locations tend uniformly to0. The Gaussian densities converge
in L1 at each s>0, so the hinge comparisons pass to the limit. A diffuse
fixed part may be kept unchanged. This closure is optional and is not
needed by the finite certificate producer.

## 7. Exact implementation and boundaries

`certificate.py` validates rational finite input, builds (5), computes its
components, and tests (4) by matrices with at most four columns. It returns
a topological component chain, exact anchors or nonzero displacement-plane
normals, or `NOT_COVERED` with an inconsistent four-row minor. It uses a
quadratic number of geometric comparisons and polynomial rational algebra;
it never enumerates intermediate point configurations or Gaussian tests.

`check_certificate.py` imports no producer code. For a positive supplied
chain it reconstructs each stage, checks every pair distance directly,
and checks the supplied anchor or plane equation for every label. This
also verifies legitimate coarsenings of the component chain. It does not
need or trust a supplied precedence graph. The analytic transfer theorems
and universal component argument remain written proofs, not formal code.

`verify.py` independently compares the component count to all75 weak orders
for each of4096 directed graphs on four vertices. It also directly checks
all180 weak orders across the small geometric controls, verifies the
unbounded-family calibrations at m=1,...,4, exercises collisions, translation,
identity, changed frames and label order, and rejects10 damaged inputs or
certificates. This is a bounded exact validation, not a proof by exhaustive
enumeration of the class. No Gaussian integration or old motion checker is
run. A known positive four-point similarity deliberately returns
`NOT_COVERED`, preventing that status from being read as a counterexample.

The root/graph constraints exclude a concrete portion of the shared finite
frontier. They do not sign the remaining strongly connected, rank-three,
anchor-inconsistent blocks, bound their cardinality, or settle the headline
conjecture. Priority beyond the cited sources has not been established.
