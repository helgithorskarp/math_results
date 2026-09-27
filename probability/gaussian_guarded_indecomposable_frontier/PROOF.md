# A compact indecomposable frontier with a permanent covariance guard

27 September 2026. Complete author proof; independent review pending.
The unrestricted R3 Gaussian-majorisation question remains open. This is
a quantitative restriction of its complete geometric test class, with
guards preserved by factorization. It supplies no new Gaussian sign,
counterexample, Kneser--Poulsen comparison, or motion obstruction.

## 1. The fixed test class

Let

    v_0=(1,1,1), v_1=(1,-1,-1),
    v_2=(-1,1,-1), v_3=(-1,-1,1),   a_j=v_j/9.

Fix these four locations once and for all. Write gamma_s for the Gaussian
with covariance s I, C_s=(2 pi s)^(-3/2), and

    Phi_(s,h)(mu)=integral(mu*gamma_s-h)_+.

For finite labelled configurations P,Q, put

    I_3(P,Q)={d(Z): d(Q)<=d(Z)<=d(P), Z in (R3)^N},
    d(Z)=(|z_i-z_j|^2)_(i<j).

A nontrivial pair is indecomposable if this full interval consists of
the two endpoint distance matrices. This is the accepted definition,
quantifying over every R3 intermediate, not a list of supplied motions.

**Theorem 1.** Full Gaussian majorisation for every bounded probability
law and every 1-Lipschitz map in R3 is equivalent to its assertion for
finite indecomposable pairs with all the following properties:

1. Four distinguished labels have positions a_0,...,a_3 at both ends.
2. Each of these locations has probability mass at least 1/8. All other
   source atoms, if present, have positive weights; the weights travel
   with their labels.
3. Both endpoint supports lie in B(0,1).
4. The variance is s_L=1/(81 L^2), where L>=4 is an integer, and only
   thresholds 0<h<C_(s_L)/2 need be tested.

One may also retain a common facet-connected nondegenerate tetrahedral
complex with every cell edge tight, as in the existing reduction. There
is no uniform bound on its size. Coincident labels may be merged.

Every law in the class, and every intermediate law in a contracting
chain fixing the distinguished tetrahedron, has

    Cov >= (1/162) I.                                       (1)

The radius bound also persists throughout any full distance interval
after aligning the four anchors. Thus neither a deteriorating root shape,
vanishing root mass, covariance collapse, nor an enlarged radius is needed
by the indecomposable test. Small variances and arbitrarily many labels
are still allowed. In particular this is not a finite exhaustive cover.

The construction has a quantitative adverse-gap statement. Starting from
a finite contraction at variance one with a hinge deficit delta>0,
choose an integer R>=1 bounding both endpoint norms and an integer k>=1
with 2^-k<=delta/4. Take L=max(4R,k). The first construction adds exactly
four sites and retains deficit at least delta/4. After adding mesh sites
and assigning them positive weights, the deficit is at least delta/8.
Some indecomposable step then has

    adverse hinge deficit / (D_step/s_L) >= delta*s_L/16,     (2)

where D_step is its ordered mean squared-distance loss. This estimate
does not divide by the number of mesh cells or chain links. It is a
conditional transfer of a supplied adverse margin, not an adverse datum.

## 2. The geometric guard and why it survives

The four anchors satisfy

    sum_j a_j=0,    (1/4)sum_j a_j a_j^T=I/81.

If a law nu puts at least mass1/8 at each anchor and has mean m, then

    Cov(nu) >= (1/8)sum_j(a_j-m)(a_j-m)^T
             = I/162 + (1/2) m m^T >= I/162.                 (3)

All omitted terms in the covariance integral are positive semidefinite.
No lower bound on any other atom mass is used. This remains true if other
labels merge at an anchor.

Suppose a labelled placement Z lies below a source P in distance order
and has the same anchor distances. Align its anchor tetrahedron to a_j.
For each label i the four inequalities give

    sum_j |z_i-a_j|^2 <= sum_j |p_i-a_j|^2.

Both sums equal four times the squared norm of their variable point plus
sum_j|a_j|^2. Hence

    |z_i|<=|p_i|.                                          (4)

This is stronger than the usual diameter bound for a rooted chain.
It proves preservation of B(0,1) in every intermediate, independent of
the number of vertices. It uses the complete distance inequalities to
all four distinguished anchors, whether or not those pairs are mesh edges.
The six anchor distances are equal at both original endpoints, so every
full-interval placement has precisely that same nondegenerate tetrahedron.

## 3. Four fixed anchors with a separated moving cloud

By scaling, an alleged failure can first be placed at variance one.
Independently translate the input and output so they lie in B(0,R),
R>=1 an integer. Write p(x)=x and q(x)=T(x) for the resulting matched
points. For L>=4R prescribe

    P(x)=8L e_1+p(x),       Q(x)=6L e_1+q(x),
    A_j=L v_j -> A_j,       j=0,...,3.                       (5)

Give each A_j mass1/8 and the moving cloud half its old mass. These
sets are disjoint. Within the moving cloud the old pair inequalities
remain unchanged; anchor-to-anchor distances are unchanged.

For a cross pair, since (v_j)_1 is either1 or-1,

    |P(x)-A_j|^2-|Q(x)-A_j|^2
      >=24L^2-36LR-R^2
      >=(239/16)L^2 >14L^2.                                (6)

To check the first bound, the constant term is
L^2(28-4(v_j)_1)>=24L^2. The two linear terms are bounded below
by -2LR(|8e_1-v_j|+|6e_1-v_j|)>-36LR, since these two norms
are respectively below10 and8. The remaining quadratic difference
is at least -R^2. Thus (5) is a contraction on the entire bounded
support, including for diffuse moving laws. Kirszbraun provides a
global extension if the formulation requires one.

The maximum source norm is at most 8L+R<=33L/4; the target norm is
at most25L/4, and the anchor norms are sqrt(3)L. Divide all positions
by9L. The anchors become exactly a_j, all supports lie in B(0,11/12),
and the variance becomes s_L=1/(81L^2). Hinge integrals are invariant
when the threshold is multiplied by (9L)^3 under this spatial scaling.

The pair loss in (6) and an enclosing-ball bound alone do not establish
a Gaussian sign. Their role is to make the transfer in the next section
legitimate while planting an invariant geometric guard.

## 4. Uniform transfer of every hinge

This is the separated-component argument from R5's fixed-atom reduction,
with a fixed four-atom background instead of a single atom. R7's recent
finite-symmetry reduction is another application of the same interaction
principle. We do not claim a new separation inequality.

For nonnegative numbers b,m,h,

    0<=(b+m-h)_+-(b-h)_+-(m-h)_+<=min(b,m).                  (7)

Let b be the Gaussian convolution of the fixed background of total mass
1/2 in (5), and let m_P,m_Q be the two convolutions of the moving half.
Use the separating plane x_1=3L. The anchor centres have first coordinate
at most L. Both moving clouds have first coordinate at least6L-R>=5L.
On either side integrate the less favorable component. Gaussian Chernoff
tails therefore give, for E=P,Q,

    integral min(b,m_E) <= exp(-2L^2),                      (8)

because the two masses are1/2 and each one-dimensional tail starts at
least2L standard deviations away. The claim follows by Tonelli for any
bounded moving law, not just atoms.

Writing f,g for the original probability Gaussian convolutions, (7)--(8)
imply, simultaneously for every h>=0,

    | H_(b+m_Q)(h/2)-H_(b+m_P)(h/2)
          - (H_g(h)-H_f(h))/2 | <= exp(-2L^2).              (9)

The common background hinge cancels. Both interaction errors lie in the
same interval [0,exp(-2L^2)], so there is no extra factor two.
If H_f(h)-H_g(h)>=delta and 2^-k<=delta/4, L>=k>=1 gives

    exp(-2L^2)<=exp(-k)<=2^-k<=delta/4.

Thus the padded pair has adverse gap at least delta/4 at threshold h/2.
Rescaling in Section3 does not change that gap. An adverse original
threshold has 0<h<C_1: h=0 gives equality and h>=C_1 gives zero hinges.
The rescaled threshold is consequently in (0,C_(s_L)/2), as required.

Neither the absolute defect nor its loss-normalized value is asserted
unchanged by padding. This construction gives a factor-two limiting
absolute transfer, whereas R7's symmetry construction preserves the
supremal absolute defect. Its different benefit is the fixed, weighted
root which survives subsequent factorizations.

## 5. Passing to an indecomposable step without losing the guard

It suffices to start with a finite alleged failure. Indeed, approximate a
bounded law by points chosen from a finite net of its support and keep
the actual map values on those points. Both endpoint Gaussian densities
converge in L1, since translations of a fixed Gaussian are L1-continuous.
The hinges converge as well, so a strictly negative gap survives. Zero
weights and repeated input sites may be removed or merged. Scaling then
reduces the variance to one before Section3.

For the finite padded pair, let C be the convex hull of its source.
It is full dimensional because it contains the distinguished tetrahedron,
and it lies in B(0,11/12). Apply the classical Brehm extension as in the
accepted indecomposable reduction: extend the finite contraction to a
continuous piecewise-isometric map F on C, refine its finite tetrahedral
triangulation to include all prescribed sites, and use all mesh vertices
as labels. Each tetrahedron is nondegenerate and all its edge lengths
are preserved. Facet adjacency is connected.

The four prescribed anchors remain fixed. The same calculation as (4)
shows |F(x)|<=|x|, since F is short and fixes the anchors. Both augmented
endpoint supports therefore remain in B(0,11/12).

The finite-interval lemma gives finitely many possible complete distance
matrices: after fixing one cell, a neighboring cell's fourth vertex has
at most two placements across its shared triangular face. A spanning
tree of cells supplies a finite bound. A saturated descending chain in
this full interval has only indecomposable steps. This is the existing
geometric argument; it is not replayed as a new result here.

The original padded law has zero weight on the new vertices. Preserve
mass1/8 at each distinguished anchor exactly. Write its residual half
as (1/2)rho, and let u be any probability vector positive on all the
other mesh vertices. Replace only this residual law by

    (1/2)[(1-tau)rho+tau u],    tau=delta/8.                 (10)

Every mesh vertex now has positive weight. The total-variation change at
each endpoint is at most tau/2. For equal-mass densities, the variational
formula H_f(h)=sup_A integral_A(f-h) shows
|H_f(h)-H_g(h)|<=||f-g||_1/2. Thus (10) changes the two-endpoint
hinge difference by at most tau and leaves adverse gap at least delta/8.
Since a probability hinge gap is at most1, 0<tau<=1/8.

Fix these weights and the same variance and threshold along a saturated
chain, aligning every state to the distinguished anchors. Every state
stays inside B(0,1) by (4), and every state has covariance at least I/162
by (3). No lower bound on the new auxiliary weights is required.

Let H_j be the favorable hinge increment at a chain step and let

    D_j=sum_(r,t) w_r w_t
           (|x_r^(j-1)-x_t^(j-1)|^2-|x_r^j-x_t^j|^2).

All D_j>=0; they sum to the total ordered loss D. The hinge increments
sum to at most -delta/8. If D_j=0, positive weights force every pair
distance to be equal; the labelled configurations are congruent and
H_j=0. Hence some step has D_j>0 and

    -H_j/D_j >= delta/(8D) >= delta/16,                     (11)

because D<=sum_(r,t)w_r w_t|x_r^0-x_t^0|^2
=2 tr Cov(mu_0)<=2 E|X_0|^2<=2. Multiplication by s_L yields (2).
This is the additive-loss selection argument, previously used in R4's
endpoint-component reduction, now on a saturated full distance interval.
There is no chain-length dilution of the normalized adverse gap.

Every step is a well-defined short map: labels which coincide before a
step must coincide afterwards. Merge such labels if desired; the four
anchor masses can then exceed1/8, which explains the inequality in the
test-class definition. The full-interval indecomposability is unaffected
by removal of redundant coincident labels. The selected adverse step
meets every requirement of Theorem1. The converse implication is immediate
because this class is a subclass of the unrestricted question.

## 6. Effective consumer interface and remaining difficulty

At s_L, divide coordinates by sqrt(s_L)=1/(9L) to use R3's accepted
all-radius, loss-relative localization. Every selected source obeys

    |X-E X|/sqrt(s_L) <=18L,
    Cov(X)/s_L >=(L^2/2) I.

Thus an actual, permanent admissible choice is

    R_*=18L,  kappa_*=L^2/2,
    1+4R_*^2/kappa_*=2593.                                 (12)

These guards hold for every intermediate, even at vanishing step loss
and after merging labels. The inherited whole-curve degree/atom schedules
and middle-mesh error estimates can consume (12) without a new covariance
certificate for each step. We do not rederive or implement those analytic
estimates, and their positive sample-margin obligation is still unsigned.

For a fixed variance band [sigma,Sigma], the same class has common
R=ceil(2/sqrt(sigma)) and kappa=1/(162 Sigma). This is a genuinely uniform
geometric input to a conditional finite cover. The theorem does not bound
L above, bound the number of mesh labels, or provide the missing signs.
Ordinary cubature need not preserve the distinguished weights or
indecomposability; those properties must not silently be added to its
output. The separate endpoint-SCC classifier also leaves this guard
intact when it is applicable, because its fixed labels remain fixed.

The compact isotropic symmetric class of R7 and this compact rooted
indecomposable class are separate complete frontiers. Isotropy and group
symmetry are not retained here. No unrestricted positive class, Gaussian
counterexample, new ball-volume sign, or historical-priority claim follows.

`transplant.py` builds exact rational finite instances of Section3.
`verify.py` independently checks the supplied transplant directly from
all pair distances, weights, covariance matrices and separation planes;
it also checks a small known-positive indecomposable reflection as a
calibration. It performs no Gaussian integration, Brehm mesh construction,
large search, old certificate replay or independent review of this proof.
