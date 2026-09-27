# A primitive obstruction to combining the new positive mechanisms

Complete author argument, 27 September 2026; independent review pending.
This is a counterexample to a **factorization proposal**, not to Gaussian
majorisation. The unrestricted Gaussian question remains open.

The new norm-preserving theorem signs a large class at every variance.
Could it, together with all contractions admitting a motion in R5, generate
every R3 contraction, at least by approximation? **No.** The existing
24-site proper-screw example is outside the closure of all finite such
compositions. This note supplies its complete two-state R3 distance
interval, an exact affine certificate excluding every choice of anchors,
and the resulting composition obstruction. The construction and its R5
barrier are credited to R4; the finite-interval compactness principle is
also prior R4 work. No new screw template or angle family is introduced.

## 1. Statement and precise scope

For a labelled configuration X in R3 write

    D(X)=(|x_i-x_j|^2)_(i<j).

Call a contracting step X -> Y admissible if it is of either type:

* N: there are a,b in R3 with |x_i-a|=|y_i-b| for every label;
* M: its prescribed matching admits a continuous contracting motion in R5,
  with the two endpoint configurations lying in copies of R3.

Independent endpoint isometries are permitted. Type N is the hypothesis
of R8's [all-variance theorem](../gaussian_norm_preserving_majorisation/PROOF.md).
Type M is the classical two-auxiliary-coordinate comparison class in
[Aishwarya--Li](https://arxiv.org/html/2609.07041v2), Section 1.2. Both
have full Gaussian comparison for every bounded law on their domain.

**Theorem.** Let P,Q be the rational 24-site pair in Section 2. Then:

1. Its full distance interval in R3 is exactly

       {D(Z): D(Q)<=D(Z)<=D(P), Z in (R3)^24}={D(P),D(Q)}.    (1)

2. No type N step joins P to Q, for any anchors. No type M step joins them.
3. There is an open neighborhood of (D(P),D(Q)) containing no pair that
   can be joined by a finite chain of type N or type M steps. The number
   of factors, their frames, and the number of auxiliary labels are not
   bounded. This also excludes endpoint limits of such finite chains.

The neighborhood is existential; no numerical radius is certified here.
In particular, for every sufficiently small rational e>0 the strictly
contracting pair P -> (1-e)Q is outside that compositional closure.
This is a statement about factorization, **not** an adverse Gaussian
sign for the perturbations or for P,Q.

For every positive pairwise distinct probability vector w on the 24 sites,
the exact pair of atomic laws (sum w_i delta_p_i, sum w_i delta_q_i) cannot
be connected by such a finite chain of deterministic contracting maps,
even when alternative intermediate supports and endpoint rematchings are
allowed. This law statement concerns exact endpoints; it does not claim
closure in an arbitrary topology on probability measures.

The unrestricted problem is not resolved, and no new ball-volume sign
follows. Operations on measures that do not arise from deterministic
contracting maps are not excluded.

## 2. The credited construction

Use J(u1,u2)=(-u2,u1), P0=I-J, epsilon=1/4, and

    U={0,e1,-e1,2e1,-2e1,e2,-e2,e1+e2},
    V=P0 U union {P0 u +/- epsilon e_j:
                              u in {0,e1}, j in {1,2}},
    a(v)=(v,(1+|v|^2)/2),      b(u)=(u,-|u|^2).

There are sixteen A sites and eight B sites. The source P consists of
A=(a(v)) and B=(b(u)). The target fixes A and sends

    b(u) -> (Ju,1-|u|^2).                                  (2)

Both groups span R3 affinely. Within each group all distances agree, and
the cross squared-distance loss is exactly

    |a(v)-b(u)|^2-|a(v)-T b(u)|^2=|v-P0 u|^2.              (3)

All 276 endpoint pairs therefore contract; 156 are tight and 120 strict,
with minimum positive loss 1/16. The paired affine rank is six. The eight
matched pairs v=P0 u are tight. These facts and the coordinates are
R4's [proper-screw construction](../gaussian_two_body_screw_obstruction/PROOF.md),
graph6472, not a construction claimed here.

## 3. The complete R3 interval has two states

Let Z be any placement in the interval (1). All within-A and within-B
distances are preserved. Align A pointwise with its source by an ambient
isometry. Four affinely independent anchors in each group imply that B
has the form

    b -> M b+t,                 M in O(3),
    c=M^T t,                    d=|t|^2.

Its cross loss is

    L(v,u)=2a(v).[(M-I)b(u)+t]-2c.b(u)-d.                  (4)

Thus 0<=L(v,u)<=|v-P0u|^2. In particular L(P0u,u)=0 on U.

The matched equation on u=x e1 is a polynomial of degree at most four.
Its fourth-degree coefficient is 2(1-M33). The fourth finite difference
at x=-2,-1,0,1,2 is 48(1-M33), hence M33=1. Orthogonality gives

    M=diag(N,1), N in O(2),       t=(v0,tau),
    c=(N^T v0,tau),              d=|v0|^2+tau^2.           (5)

The matched loss now becomes the quadratic polynomial

    2u^T P0^T(N-I)u+4tau|u|^2
       +2u^T(P0^T v0-N^T v0)+tau-d.                       (6)

The points 0,+/-e1,+/-e2,e1+e2 are unisolvent for total-degree-two
polynomials in two variables. Their zero values give

    d=tau,
    N^T v0=P0^T v0,
    sym[P0^T(N-I)]=-2tau I.                               (7)

Since N is orthogonal and P0 P0^T=2I, the middle equality implies
|v0|^2=2|v0|^2. Thus v0=0 and tau^2=tau, so tau=0 or 1.
Put k=1-2tau, which equals +1 or -1. The last equality says

    P0^T N=kI+zJ                                             (8)

for one real z. Taking Gram matrices in (8) gives
2I=(k^2+z^2)I, hence z=+1 or -1. Multiplication by P0/2 leaves exactly

    (tau,N)=(0,I), (0,-J), (1,J), (1,-I).                  (9)

This is exhaustive, including orientation-reversing possibilities: no
orientation assumption was made before solving (8).

Use the actual probe u=e1, v=P0e1+epsilon e1=(5/4,-1).
Its loss in (4), for the candidates (0,-J) and (1,-I), is respectively

    -2epsilon=-1/2,           epsilon^2-2epsilon=-7/16.    (10)

Both violate the lower bound zero. The two surviving placements are
exactly P and Q. This proves (1) over all real intermediate placements,
not just sampled motions, rational configurations, or a chosen template.

The checker reconstructs (4) as a formal linear expression in M,t,c,d.
It certifies the fourth difference and the quadratic identity (6), verifies
unisolvence, and checks all pairs of all four remaining placements.
The finiteness and exhaustiveness of (9) follow from the displayed proof.

## 4. A six-term anchor obstruction and its open form

Write a0=a(0), a+=a(P0e1), a-=a(-P0e1), and similarly b0,b+,b-.
Assign signed coefficients

    omega(a+)=omega(a-)=omega(b+)=omega(b-)=1,
    omega(a0)=omega(b0)=-2,
    omega=0 on the other labels.

Exact coordinate sums give

    sum omega_i=0,
    sum omega_i p_i=sum omega_i q_i=0,
    sum omega_i (|p_i|^2-|q_i|^2)=4.                       (11)

If anchor equality held, its squared version would say

    |p_i|^2-|q_i|^2
        =2p_i.a-2q_i.b-|a|^2+|b|^2.                      (12)

Multiplying by omega and summing contradicts (11). This rules out all
real anchors, including ones outside the supports or arbitrarily far away.

For the approximation claim we need more than failure at one pair.
Let C(P,Q) have rows (p_i,q_i,1), and append the norm-loss column to form
the 24-by-8 matrix A(P,Q). Exact elimination gives

    rank C(P,Q)=7,           rank A(P,Q)=8.                (13)

The checker emits eight row indices and the nonzero determinant of that
8-by-8 minor. If anchors exist, (12) forces every such determinant to
vanish. The chosen nonzero minor stays nonzero in a coordinate neighborhood.
Its absolute value is invariant under separate endpoint isometries:
orthogonal changes multiply the two coordinate blocks by orthogonal
matrices, and translations only add linear combinations of existing
columns to the norm-loss column. Thus a neighborhood of the pair of
distance matrices contains no type N step. Alternatively, bounded
representatives with a convergent subsequence give the same conclusion.
This avoids incorrectly assuming bounded anchors in an approximating
sequence.

## 5. The credited R5 barrier is also local

R4's Section 4 proves more than absence of one motion: no R5 placement
in this distance interval has a certain intrinsic height tau equal to 1/2.
Here is its precise premise and certificate, so the new closure statement
has an explicit trust boundary.

After fixing A in its R3 plane, (4) and the same tight equations give

    U(x,z)=(Nx,z,Kx),   t=(v0,tau,w),   N^TN+K^TK=I,
    d=tau,       U^Tt=(P0^T v0,tau),
    sym[P0^T(N-I)]=-2tau I.

Here K is 2-by-2 because the ambient space is R5. At tau=1/2 these imply

    N=alpha(I+J),       K^TK=k^2 I,       k^2=1-2alpha^2.

The four signed epsilon probes at u=0 give |(v0)_j|<=1/16, hence
|v0|^2<=1/128. Those at u=e1 give 3/8<=alpha<=5/8, so k^2>=7/32.
The equation for U^Tt gives

    K^T w=[(1-alpha)I+(1+alpha)J]v0.

Since k>0, also KK^T=k^2I. Together with d=1/2 this yields

    k^2/4=3|v0|^2,
    |v0|^2>=7/384>1/128,                                (14)

with rational gap 1/96. This is R4's proof, recalled and credited; the
checker audits its polynomial norm identity and rational bounds. The
original argument's independent-review status is recorded in SOURCES.md.

There is a useful distance-only expression for this height. For any
placement Z, in any Euclidean dimension, define

    r(B0)=1, r(A0)=-3/2, r(A+)=r(A-)=1/4,
    t(A0)=-1, t(A+)=t(A-)=1/2,
    tau(D(Z))=-(1/2) sum_(i,j) r_i t_j |z_i-z_j|^2.        (15)

Both coefficient sums vanish, so this is the scalar product of the two
corresponding affine differences. When A is fixed, it is exactly the
vertical coordinate of the moved b(0). Its endpoint values are 0 and 1.

Suppose type M steps had endpoint distances approaching D(P),D(Q).
On each continuous contracting R5 motion, (15) is continuous and takes
a value 1/2, once the endpoints are sufficiently close. At that stage
all distances lie between the two approximate endpoints. Normalize one
label to zero. Bounded pair distances give bounded coordinates in R5;
a subsequence converges to a realization in the exact interval with
tau=1/2. This contradicts (14). Hence a neighborhood of (D(P),D(Q))
contains no type M step either. No general closedness theorem for all
contracting motions is assumed.

## 6. Arbitrary finite compositions and approximation

This uses the finite-interval compactness argument already stated in
R4's [strong-chain closure theorem](../gaussian_indecomposable_contractions/STRONG_CLOSURE.md).
We give its two-state specialization with the local tests just proved.

Suppose finite chains of admissible steps have endpoint distance vectors
converging to D(P),D(Q). Every stage lies coordinatewise between its
chain endpoints. Uniformly over all stages, its distance from the set
{D(P),D(Q)} tends to zero. Otherwise an offending sequence of stages
has bounded representatives after translating one label to zero; a
subsequence converges to a third R3 state in (1), a contradiction.

Take disjoint small neighborhoods of the two states. Every sufficiently
late chain begins in the first and ends in the second, and every stage
lies in one of them. There is an adjacent step from the first to the
second. Along a subsequence these steps have endpoint distances converging
to D(P),D(Q). Infinitely many are of one of the two types N or M. Each
possibility contradicts its local exclusion in Sections 4 or 5.
This proves the neighborhood and closure assertion.

Auxiliary labels cannot help: restricting every step to the original
24 labels preserves either defining property. Independent frames were
already absorbed in the distance formulation. No bound on factor count,
step size, or anchor locations enters the proof.

All target sites are distinct. Consequently P -> (1-e)Q is strictly
contractive on every pair for 0<e<1 and converges to the obstructed pair
as e tends to zero. The neighborhood gives the stated rational existence
claim. It gives no specific allowable e and no Gaussian sign.

For the law-level exact statement, a deterministic map cannot increase
the number of support atoms. A chain beginning and ending with 24 distinct
positive atoms therefore has no collision at any stage. Its atoms carry
their original weights. Pairwise distinct weights force the prescribed
matching at the final law. Apply the labelled obstruction. For example,
weights (1,2,...,24)/300 in the checker's stated order are admissible.
The conclusion holds for the entire open set of distinct positive priors,
not only this calibration vector.

## 7. The remaining actual Gaussian obligation

Let f_(w,s)=sum w_i gamma_s(.-p_i) and g_(w,s)=sum w_i gamma_s(.-q_i).
The unresolved statement is precisely

    integral (g_(w,s)-h)_+ - integral (f_(w,s)-h)_+ >= 0
          for all positive w, s>0 and h>=0.                (16)

This note does not sign or refute (16). R1's independently accepted
spherical comparison proves it for each fixed w at every sufficiently
large variance. Earlier floating hinge searches did not give an adverse
candidate or a certified finite-variance region; those data are not
premises here. The finite-atomic low-noise regime remains closed to this
lane and is not reopened by this note.

The useful negative handoff is specific: closing the full question by
factoring arbitrary contractions into the new anchored class and the
classical R5 class is impossible, even by endpoint approximation and
unbounded finite factor counts. A positive proof of (16) would need a
comparison outside that compositional mechanism. Law-dependent couplings,
direct integrated identities, or other classes remain possible.

The exact code checks input geometry, formal finite differences,
unisolvence, four exhaustive algebraic candidates, the signed anchor
certificate, a nonzero minor, the height formula and R4's numerical-free
barrier identities. Compactness, rigidity, exhaustive real algebra and
the law argument are written proofs. No Gaussian quadrature, solver,
formal proof assistant, hidden data, or new numerical sign is used.
