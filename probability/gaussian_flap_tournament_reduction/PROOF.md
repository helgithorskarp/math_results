# Two ten-point templates for orthocentric flap counterexamples

Complete author proof; independent mathematical review and formalization
are pending. The unrestricted three-dimensional Gaussian-majorisation
question remains open. This is an exact reduction of possible **actual
negative hinges** in an asymmetric family, not a numerical sign search.

## 1. Family and conclusion

Let four affinely independent vectors v_0,...,v_3 in R3 satisfy

    v_i . v_j = -c < 0  for i != j,    h_i = |v_i|^2+c.       (1)

They are the vertices of an orthocentric tetrahedron with its orthocenter
at the origin and inside the tetrahedron. We use precisely condition (1),
not every tetrahedron or every orthocentric tetrahedron. The four anchors
v_i are fixed. The twelve directed flap labels i->j, i!=j, have endpoints

    x_ij = v_j-v_i,       y_ij = v_j+v_i.                    (2)

Thus this is the depth-one flap family, where depth one means displacement
by v_i, rather than a common Euclidean normal length. The regular member
is the classical simplex-flap construction, with its expansion reversed.
The construction itself is prior work; see [SOURCES.md](SOURCES.md).

Assign nonnegative anchor weights alpha_i and flap weights beta_ij,
with total one. Call the resulting source law mu and its image nu.
For s>0, let gamma_s be the Gaussian with covariance s I_3 and write

    H_f(a) = integral (f-a)_+,    D_s,a(mu,nu) = H_(mu*gamma_s)(a)
                                                 - H_(nu*gamma_s)(a).

A positive D is a counterexample hinge. For each unordered edge e={i,j}
put q_e=beta_ij+beta_ji. A **selector** chooses one direction of every
edge, that is, a tournament on four vertices. Its source mu_sigma puts
mass q_e at the selected x_ij and retains the anchor masses. Its image
is the same nu for all 64 selectors.

**Theorem (lossless reduction of a negative hinge).** If D_s,a(mu,nu)>0
for any law (1)-(2), some selector with no sink satisfies

    D_s,a(mu_sigma,nu) >= D_s,a(mu,nu) > 0.                (3)

Here a sink has outdegree zero. There are exactly 32 sinkless selectors.
Under simultaneous permutation of the vertices, geometry and weights,
they have just two types, represented by the following directed edges:

| Type | Arcs | Sorted outdegrees | Labelled copies |
| --- | --- | --- | --- |
| source and triangle | 1->0, 0->2, 3->0, 2->1, 3->1, 3->2 | 1,1,1,3 | 8 |
| strongly connected | 1->0, 2->0, 0->3, 2->1, 3->1, 3->2 | 1,1,2,2 | 24 |

Each selected configuration has four anchors and six flaps, hence at
most ten source atoms. Every selector with a sink satisfies all Gaussian
hinge comparisons, for all weights and all variances, by the explicit
five-dimensional motion in Section 4.

Consequently, full Gaussian majorisation for all laws in (1)-(2) is
**equivalent** to full majorisation for these two ten-point template
families with arbitrary nonnegative weights and arbitrary geometry (1).
The supremum of the positive hinge defect over the entire family is
unchanged by this restriction.
For a fixed asymmetric tetrahedron one must retain all 32 labelled
selectors: reducing to two also relabels its geometric parameters. For a
fixed regular tetrahedron every vertex permutation is an ambient isometry,
so the two templates with arbitrary weights suffice without changing shape.

The selected orientation in (3) may depend on s and a. We do not claim one
orientation maximizes every hinge simultaneously. The same reduction holds
for a fixed convex internal energy when all relevant integrals are finite.

## 2. Exact geometry and contraction

The Gram matrix in (1) is diag(h_i)-c 11^T and has rank three.
If k is a nonzero kernel vector, then h_i k_i=c sum_j k_j. The sum
cannot vanish, so its kernel is one-dimensional and has a strictly
positive vector. Normalizing its sum to one gives

    p_i=c/h_i>0,    sum_i p_i=1,    sum_i p_i v_i=0.        (4)

In particular every three v_i are linearly independent: a relation on
a proper subset could not be a multiple of the strictly positive kernel
vector. Equation (4) also proves the asserted interior location.

The elementary identity

    v_i . (v_k-v_j) = h_i (1_(k=i)-1_(j=i))               (5)

gives all squared-distance losses:

    |x_ij-v_k|^2 - |y_ij-v_k|^2 = 4 h_i 1_(k=i),
    |x_ij-x_kl|^2 - |y_ij-y_kl|^2
                    = 4(h_i 1_(l=i)+h_k 1_(j=k)).         (6)

Anchor-anchor losses vanish. These formulas include repeated tail or head
indices and prove contraction on all sixteen source sites. A global
1-Lipschitz extension exists by Kirszbraun's theorem if needed.

The sixteen source sites are distinct. Equality between two differences
would give a nontrivial affine relation among the v_i; equality between
an anchor and a difference would give a linear relation supported on at
most three vertices. The only trivial difference equality repeats its
ordered pair. The four anchors and six sums v_i+v_j are likewise distinct:
equal sums give an affine relation, while an anchor-sum equality has
support at most three. None of the v_i is zero by (1).

In particular, each ten-site selector maps injectively onto ten distinct
target sites. With all ten masses positive it has paired affine rank six.
Indeed the four pairs (v_i,v_i) span the diagonal affine three-space.
Subtracting the pair (v_j,v_j) from the selected flap pair gives
(-v_i,v_i). Every tournament has at most one sink, so at least three
independent tail vectors occur. They span the antidiagonal three-space.
This includes the safe sink selectors: their positivity uses a motion,
not a paired-rank-five shortcut.

## 3. Convexity at a fixed target, with quantitative preservation

If q_{ij}>0, choose i->j with probability beta_ij/q_{ij}, independently
for the six unordered edges. If q_{ij}=0, choose either direction with
probability 1/2; that edge contributes zero mass. Let lambda_sigma be
the resulting product probabilities. Directly, as identities of measures,

    sum_sigma lambda_sigma=1,
    mu = sum_sigma lambda_sigma mu_sigma,
    (T_sigma)#mu_sigma = nu  for every sigma.              (7)

Linearity of convolution and pointwise convexity of the positive part give

    D_s,a(mu,nu) <= sum_sigma lambda_sigma D_s,a(mu_sigma,nu).  (8)

This is the existing elementary common-target lemma, used in a different
geometry; it is not a new general majorisation principle. It is essential
that the output law remains exactly the same.

Let R=sum_(sigma without a sink) lambda_sigma. By Section 4 all omitted
terms in (8) are nonpositive, so if D_s,a(mu,nu)>0, then R>0 and

    max_(sigma without a sink) D_s,a(mu_sigma,nu)
                                      >= D_s,a(mu,nu)/R.  (9)

Thus compression cannot reduce the tested negative margin. If every
q_{ij}>0, a useful exact formula is

    R = 1 - sum_(k=0)^3 product_(j!=k) beta_jk/q_{jk}.     (10)

The four sink events are disjoint because two vertices cannot both be
sinks. This proves (10). For zero edge masses the same formula holds using
the stipulated orientation probabilities instead of an undefined ratio.
In particular symmetric orientation splits give R=1/2, although no sign
for their hinge is inferred from this fact.

Alternatively, fixing alpha and q fixes nu and gives a six-dimensional
box of source splits. A hinge is convex on this box; its maximum is attained
at a selector corner. Equation (9) adds the Gaussian-safe pruning.

Replacing the positive part by any one convex function gives the stated
internal-energy version whenever all integrals in the finite mixture are
finite. For hinges no integrability qualification is needed: each lies
between zero and one.

## 4. Every sink selector has a five-dimensional contracting motion

Let k be its sink. Its three possible moving tail vectors are the basis
{v_i:i!=k}. The following explicit basis motion is from
[the simplicial-cone proof, Sections 2-3](../gaussian_simplicial_cone_reflections/PROOF.md).
We recall it to make the new multi-origin application checkable.

Order this basis as b_1,b_2,b_3. Let P project onto span(b_2,b_3), let
J be an isometry of that plane into R2, and put

    eta=|b_1-Pb_1|/|b_1|,  q(t)=sqrt(1-t^2),
    A(t)=(t+eta)/(1+eta t),                 -1<=t<=1.

Here 0<eta<1: independence gives the lower inequality; b_1 has nonzero
inner products with b_2 and b_3, giving the upper one. Define the linear
map F_t:R3 -> R3 direct-sum R2 by

    F_t b_1 = (A(t)b_1, q(t) J(Pb_1)/(1+eta t)),
    F_t b_j = (t b_j, q(t) J b_j),                 j=2,3. (11)

It is an isometric embedding. The only nontrivial Gram identities are

    (t+eta)^2+(1-eta^2)(1-t^2)=(1+eta t)^2,
    t(t+eta)+(1-t^2)=1+eta t.

Its original-coordinate coefficients lambda_i(t) are A(t),t,t. They
increase from -1 to 1, since A'(t)=(1-eta^2)/(1+eta t)^2>0.
The endpoints of F are -I and I, with zero auxiliary coordinates.

Keep the four anchors at (v_j,0), but move each selected flap by

    z_ij(t)=(v_j,0)+F_t v_i.                              (12)

The distinct origins v_j cause no problem. The isometry of F_t makes
the quadratic terms |F_t(v_i-v_k)|^2 constant. Using (5), the derivatives
of every remaining squared distance in the open time interval are

    d/dt |z_ij-(v_k,0)|^2 = -2 h_i lambda_i'(t) 1_(k=i),
    d/dt |z_ij-z_kl|^2
             = -2[h_i lambda_i'(t) 1_(l=i)
                         +h_k lambda_k'(t) 1_(j=k)].       (13)

They are nonpositive; continuity handles the endpoints. Equivalently the
distances are affine expressions with nonpositive coefficients in the
monotone lambda_i, so no endpoint derivative is required. Substituting
t=-cos(pi u) gives smooth trajectories. Equations (11)-(13) establish
a continuous R5 contraction of the entire ten-site configuration.

For completeness, the Gaussian inference is the known two-coordinate
cancellation. Apply Aishwarya--Li, Theorem 1.4(i)(a), in R5. Sampling an
endpoint density from itself, its density value is stochastically smaller
at the source. At each endpoint the density factors as f(x) gamma_s^(2)(z).
For an independent Z sampled from gamma_s^(2),

    gamma_s^(2)(Z)/C_2 is uniform on (0,1), C_2=(2 pi s)^(-1).

Hence the probability its product with f(X) exceeds a C_2 is exactly
integral f(x)(1-a/f(x))_+ dx=H_f(a). The stochastic order gives the desired
hinge comparison in R3. This argument is a cited prior mechanism, not a
claim that ordinary majorisation can generally be cancelled under products.

## 5. Exhaustive four-vertex classification

A tournament has at most one sink. Choosing that vertex and the arbitrary
three-edge tournament on the others counts exactly 4*8=32 sink selectors.
Of these, 24 are transitive and eight have a directed triangle above a sink.

In a sinkless tournament the four positive outdegrees sum to six. They
are therefore either (3,1,1,1) or (2,2,1,1), up to order. In the first case
the dominant vertex is unique and the other three form a directed cycle.
This gives 4*2=8 labelled tournaments, with a cyclic automorphism group of
size three. In the second case let A->B be the edge between the two
vertices of outdegree two. Vertex B must beat both low-degree vertices.
Vertex A beats one of them, say C, and loses to the other, D. The final
edge is forced to be C->D by their outdegrees. Thus there is a unique
isomorphism type, with trivial automorphism group and 24 labelled copies.
This orientation is strongly connected. These counts exhaust all 64.

For reproducibility, enumerate edges as (01,02,03,12,13,23). Bit one means
smaller vertex -> larger vertex; bit zero means the reverse. The least
masks under vertex permutation of the two sinkless types are 2 and 4.
The certificate supplies an explicit relabelling for every mask, not just
matching totals. Relabelling the tetrahedron and the corresponding masses
transports the laws without changing the mathematical comparison. This
proves the theorem and its two-template formulation.

## 6. A rational, shape-complete parametrization

Dilation reduces (1) to c=1. Up to an orthogonal change of coordinates,
every such tetrahedron has the following form for a,b,d>0:

    z=-1/a,  x=-(1+1/a^2)/b,  y=-(1+1/a^2+x^2)/d,
    v_0=(0,0,a),  v_1=(b,0,z),
    v_2=(x,d,z),  v_3=(x,y,z).                            (14)

To see completeness, put v_0 on the positive third axis and the projection
of v_1 on the positive first axis. Independence makes b>0. Choose the
second-axis sign so the second coordinate d of v_2 is positive; independence
again makes it nonzero. The off-diagonal inner products force all remaining
coordinates in (14). Conversely (14) has all six off-diagonal products -1;
its first three columns are independent, and its Gram kernel argument (4)
gives affine independence. In particular every positive rational triple
(a,b,d) produces an exact rational configuration satisfying every contraction
constraint, including its equality faces.

One simple asymmetric example is (a,b,d)=(1,2,3):

    v_0=(0,0,1), v_1=(2,0,-1), v_2=(-1,3,-1), v_3=(-1,-1,-1),
    (h_0,h_1,h_2,h_3)=(2,6,12,4).

No Gaussian sign is asserted for this example or for the shipped fixtures.

**Rational negative-witness corollary.** If any strict failed hinge exists
anywhere in family (1)-(2), one exists in one of the two templates with
positive rational a,b,d, positive rational ten-point weights, positive
rational variance and positive rational physical threshold.

Indeed first use (3) and relabel. Dilation by 1/sqrt(c) changes variance
to s/c and threshold to c^(3/2) a, preserving the hinge value. Use (14)
and approximate its parameters by positive rationals. Gaussian densities
of finitely many atoms depend continuously in L1 on centers, weights and
positive variance. This follows, for example, from pointwise convergence
of translated Gaussian probability densities and Scheffe's lemma.
The hinge changes by at most the L1 change of its density. At fixed f,
for a,b>0 its change is at most |a-b|/min(a,b), because {f>min(a,b)}
has volume at most 1/min(a,b). Thus a strict defect persists under all
these perturbations, including approximation of zero weights by positive
rational weights. This is a density statement; it gives no uniform lower
weight bound, denominator bound, compact exclusion, or certified sign.

## 7. Scope and computational trust

The exact checker audits the combinatorial certificate, every distance
identity in a formal Gram representation, motion coefficients, polynomial
Gram identities, rational fixtures, paired ranks and common-target mixture
identities. Its direct coordinate and graph checks import no producer code.
These are finite algebraic controls supporting the written universal proof;
they do not certify any Gaussian integral or replace independent review.

The reduction is limited to (1)-(2). Opposite target collisions, essential
to (7), generally disappear at other depths or under general face-normal
perturbations. It is not a reduction of every bounded R3 measure to ten
points or to orthocentric tetrahedra. No nonliftability assertion is made
for either selected template. A five-dimensional motion or other full
comparison for both templates would settle this entire asymmetric flap
family. A certified negative hinge or convex energy on either would refute
the unrestricted conjecture. Neither endpoint is supplied here.

If all ten target masses are positive, ten source atoms are necessary for
any deterministic selector with that target. This elementary counting
minimality is not a bound on the least support of a general counterexample.
Existing balanced regular-flap comparison, shallow-depth/tail results,
and universal beta-column signs retain their separate scopes; see
[HANDOFF.md](HANDOFF.md). The contribution is the lossless negative-witness
compression and precise remaining obligations, not a new positive neighborhood.
