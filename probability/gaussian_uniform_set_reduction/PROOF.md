# The full Gaussian question on equimeasurable lattice sets

Complete author proof; independent review pending. The unrestricted
dimension-three Gaussian-majorisation question remains open. This is an
exact reduction of its measure class, not a positive comparison theorem.
It gives a single discrete geometric test class in which the two initial
densities are equimeasurable and the map preserves volume on its support.

## 1. A countable geometric frontier

Let Q=[-1/2,1/2]^3. Choose a positive integer N and labelled integer centers
X_i,Y_i in Z^3, i=1,...,N, subject to the following conditions for i!=j:

    ||X_i-X_j||_infinity >= 2,
    ||Y_i-Y_j||_infinity >= 2,                              (1)

    |X_i-X_j|^2-|Y_i-Y_j|^2
       > 2 ||(X_i-X_j)-(Y_i-Y_j)||_1.                      (2)

Define the disjoint compact sets

    E = union_i (X_i+Q),       F = union_i (Y_i+Q),
    T(X_i+u)=Y_i+u,            u in Q.                     (3)

Their volumes are both N. Write mu_E=1_E/N and mu_F=1_F/N for the
probability densities, and gamma_s for the centered Gaussian with
covariance s I_3. For nonnegative integrable f put H_f(a)=integral(f-a)_+.

**Theorem 1 (uniform-set reduction).** The following assertions are equivalent:

1. For every bounded-support probability law mu on R3, every 1-Lipschitz
   map S, every s>0 and every a>=0,
   H_(mu*gamma_s)(a)<=H_((S#mu)*gamma_s)(a).
2. For every integer cube configuration (1)--(3), every positive integer q
   and every positive rational a,

       H_(mu_E*gamma_(q^2))(a)<=H_(mu_F*gamma_(q^2))(a).     (4)

Moreover, the supremum of the positive hinge defect is exactly the same
in these two classes. Thus any strict failure can be preserved, up to any
prescribed positive loss, using only this discrete set class.

The map in (3) is 1-Lipschitz on E, bijects E to F, preserves Lebesgue
measure there, and has derivative I on every component interior. Both
initial probability densities take just the values 0 and 1/N. In particular
they have identical concentration profiles min(v/N,1) before Gaussian
convolution, for every volume v>=0.
Between distinct components the contraction is strict at every point pair;
within each component it is an isometry.

The conclusion changes the law **and** the support map. It does not claim
that a minimizing law for a prescribed map is uniform, or that an arbitrary
fixed law can be replaced exactly. The sets are disconnected. No globally
volume-preserving extension, connected-domain statement, bound on N or on
the center coordinates, or finite exhaustive cutoff is asserted.

## 2. Why center contraction alone is insufficient

For two components write u=X_i-X_j, v=Y_i-Y_j. Points in them have
offsets r,t in Q, with h=r-t ranging over [-1,1]^3. Their squared-distance
loss is

    |u+h|^2-|v+h|^2
       = |u|^2-|v|^2+2(u-v).h.

Its minimum over all offsets is exactly

    |u|^2-|v|^2-2||u-v||_1.                               (5)

Consequently replacing > by >= in (2) is the necessary and sufficient
condition for the whole two cubes to contract. Equation (2) gives strict
contraction between components. It also proves the claimed global
1-Lipschitz bound on E, including component boundaries. Translation on
each disjoint cube proves T#mu_E=mu_F. Kirszbraun's theorem extends T to
a 1-Lipschitz map on R3 if the full-space formulation is required.

For example, scalar center differences u=3 and v=-2 contract, but their
unit intervals do not: the minimum squared-distance loss is 5-10=-5.
The same example along one coordinate is a failure for unit cubes in R3.
At center dilation 3 the loss becomes 45-30=15>0. Thus one must choose
the component scale after checking the slack; center inequalities cannot
simply be reused for sets of positive volume.

## 3. Strict uniform rational point laws retain every failure

We record the approximation step fully, so the set reduction does not
hide a change of weights, labels, or map assumptions. The elementary bound

    TV(gamma_s(. -x),gamma_s(. -y))
         <= |x-y|/sqrt(2 pi s)                             (6)

follows by integrating the directional Gaussian derivative. For equal-mass
densities f,g, both H and any fixed-volume concentration change by at most
TV(f,g). In particular a change of source and target adds their two errors,
uniformly over hinge thresholds.

By a common spatial rescaling we may first take s=1. Suppose a specified
hinge has positive source-minus-target gap d. Approximate the input law by
finitely many actual source points and retain their exact images. A finite
small-diameter partition of the bounded support does this; (6) makes the
total hinge error arbitrarily small. Merge identical source points and
discard zero weights. The finite source points are now distinct.

Expand these source centers by a factor 1+eta about any fixed origin,
leaving their images unchanged. For eta>0, every distinct pair then
contracts strictly. Taking eta small preserves the gap by (6). A generic
arbitrarily small perturbation of the target centers makes them distinct;
the finitely many strict pair inequalities persist. Approximate both
endpoint lists by rational coordinates, and their positive weights by
positive rational weights of total one. All strict inequalities and
distinctness persist. For a weight change from w to w', the combined hinge
error is at most sum_i |w_i-w'_i|, so this too can be arbitrarily small.

Write the resulting rational weights as n_i/N, with n_i positive integers.
For each i choose n_i distinct rational offset vectors d_(i,j), j=1,...,n_i,
and replace the weighted label by the uniformly weighted labels

    x_(i,j) = x_i + epsilon d_(i,j),
    y_(i,j) = y_i + (epsilon/2) d_(i,j).                   (7)

For sufficiently small positive rational epsilon, different old clusters
remain distinct at both endpoints and their finite strict inequalities
persist. Inside a cluster all distances decrease by the factor 1/2.
Thus all N source centers and all N target centers are distinct rational
points, and **every** pair contracts strictly. The uniform N-point laws
converge to the previous weighted laws as epsilon decreases; (6) controls
their hinge errors uniformly. These are genuine new contraction data,
not multiple labels at one source point with inconsistent images.

We have proved: any original positive gap can be retained to within any
prescribed positive loss by a uniformly weighted rational finite pair at
variance one, with strict contraction and injective endpoints. The earlier
[strict finite-witness source](../gaussian_majorisation_rank_abel/PROOF.md)
supplies a related reduction; the argument here spells out the equal-weight
splitting required for the set construction.

The hinge is continuous in its positive threshold, by dominated convergence.
Hence we can also choose a positive rational threshold b while retaining
the gap to any further prescribed positive loss. A strict positive gap
cannot occur at threshold zero.

## 4. Thicken after integer dilation

Fix one of the strict rational uniform pairs just constructed, denoted
x_i,y_i, at threshold b and variance one. For i!=j put

    d_ij=|x_i-x_j|^2-|y_i-y_j|^2 > 0,
    l_ij=||(x_i-x_j)-(y_i-y_j)||_1.

Choose a positive integer q which is a multiple of every coordinate
denominator, and increase it if necessary so that

    q d_ij > 2 l_ij                               for all i!=j,
    q ||x_i-x_j||_infinity >=2,
    q ||y_i-y_j||_infinity >=2                    for all i!=j. (8)

This is possible because the lists are finite, d_ij>0 and both lists
are distinct. Set X_i=q x_i and Y_i=q y_i. Their centers are integers,
and (8) is exactly (1)--(2) after scaling. It proves contraction of the
entire cubes, not merely of their centers.

Let alpha_X=N^(-1)sum_i delta_(X_i), and similarly alpha_Y. Gaussian
scaling gives the exact identity

    H_(alpha_X*gamma_(q^2))(b/q^3)
       -H_(alpha_Y*gamma_(q^2))(b/q^3)
       =H_(alpha_x*gamma_1)(b)-H_(alpha_y*gamma_1)(b).      (9)

Let U be uniform on Q, independent of a uniform label. Coupling X_i+U
to X_i moves a center by at most sqrt(3)/2. Equation (6) therefore bounds
the sum of the two hinge changes when thickening by

    | [H_(mu_E*gamma_(q^2))(a)-H_(mu_F*gamma_(q^2))(a)]
       -[H_(alpha_X*gamma_(q^2))(a)-H_(alpha_Y*gamma_(q^2))(a)] |
          <= sqrt(3)/(q sqrt(2 pi)) < 1/q,               (10)

uniformly in a. The last strict bound uses 2pi>3. Take a=b/q^3, still
positive rational. Increasing q through denominator multiples makes the
loss smaller than any desired amount, without spoiling (8).

Combining (9)--(10) proves the failure-preserving direction of Theorem 1.
The reverse direction follows because (3) is a genuine contraction and
mu_E is a bounded-support probability density. Applying the same argument
with arbitrary approximation tolerance to each original hinge value proves
equality of the two supremal positive defects. No optimizer attainment or
exchange of an infinite limit with a sign assertion is used.

## 5. What this changes about the remaining problem

The remaining full-question sign can be tested on integer data satisfying
the explicit arithmetic constraints (1)--(2), one integer q, and one rational
threshold. There are no independently chosen real weights, singular input
measures, local Jacobian losses on the support, or unequal initial density
profiles in this test class. All of these features can be removed from a
hypothetical failure. For instance a proof that heat flow preserves
majorisation for **all** volume-preserving support contractions of such
lattice sets would prove the full bounded-law conjecture.

The densities in this test are explicit. If Phi is the standard one-dimensional
Gaussian distribution function, then

    (mu_E*gamma_(q^2))(z)
      = (1/N) sum_i product_(k=1)^3
          [Phi((z_k-X_(i,k)+1/2)/q)
           -Phi((z_k-X_(i,k)-1/2)/q)],                    (11)

and replace X by Y for the target. Thus a validated integrated test has
only finite integer data and one fixed elementary kernel as inputs. A
sampled or unvalidated negative value is not a counterexample certificate.

This is not an inference that heat preserves general equimeasurability
order. The metric constraints on T still encode the difficult geometry.
The countable class has unbounded complexity, and a finite positive search
does not establish (4) universally. Conversely any rigorously negative
integrated hinge on one of these exact set instances would be a genuine
counterexample, by the verified whole-cube contraction.

The earlier [common-set minimax theorem](../gaussian_prior_localization/PROOF.md)
retains its diffuse optimizer obstruction for a **fixed** domain and map.
The present reduction changes both and only preserves a strict gap or a
supremum. The [uniform compact defect frontier](../gaussian_prior_localization/DEFECT_LOCALIZATION.md)
has different quantitative content: its atom/radius bound is not a bound
on the multiplicity N or dilation q introduced here. The
[shift-interaction obstruction](../gaussian_prior_localization/SHIFT_AVERAGING_BOUNDARY.md)
is also unchanged. This proof uses a globally coherent approximation; it
does not discard or cancel conditional interaction terms.

No new positive map class or Kneser--Poulsen consequence is proved. The
analytic approximation and equivalence are written proofs. The compact
[exact audit](verify.py) checks the integer geometry and its corner
criterion, including a rejected center-only shortcut; it does not evaluate
Gaussian hinge signs or search the unbounded class.
