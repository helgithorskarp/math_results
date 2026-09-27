# Finite distance intervals obstruct approximate strong factorizations

Complete author proof, 27 September 2026; independent review pending.
This supplement strengthens an existing obstruction to a proof mechanism.
It does not produce an adverse Gaussian hinge or enlarge a cap/flap family.

The distinction from the earlier [finite-interval reduction](PROOF.md) is
closure: an exact factorization obstruction need not, by itself, obstruct
approximation by factorizable maps. Here finiteness supplies that bridge.

## 1. The closed elementary relation

For N labelled points in R^d let D(P)=(|p_i-p_j|^2)_(i<j). Write

    I_d(P,Q) = {D(Z): D(Q)<=D(Z)<=D(P), Z in (R^d)^N}.

Distances are ordered coordinatewise. Complete labelled distance matrices
determine configurations up to ambient isometry, including degenerate ones.

Call P -> Q a **strong step with free frames** if there are orthonormal
bases a_1,...,a_d and b_1,...,b_d such that

    |b_r . (q_i-q_j)| <= |a_r . (p_i-p_j)|   for all i,j,r.       (1)

This deliberately allows independent input/output frames. It contains
coordinatewise strong contractions, arbitrary one-sided hyperplane folds,
and isometries. Summing squared inequalities shows that it is a contraction.
Changing either endpoint by an isometry preserves the relation.

On bounded sets of distance matrices this relation is closed. Indeed,
translate one label of each representative to zero. Bounded squared
distances bound all coordinates. Extract convergent subsequences of the
representatives and of their orthonormal frames, using compactness of O(d).
The limit preserves (1) and realizes the limiting distance matrices.
No bound on the number of factors is part of this assertion.

## 2. Finite-interval closure theorem

**Theorem.** Suppose I_d(P,Q) is finite. If pairs (P_n,Q_n), each admitting
a finite chain of strong steps with free frames, satisfy

    D(P_n) -> D(P),       D(Q_n) -> D(Q),

then P -> Q itself admits a finite chain of such steps. Its nonisometric
steps can be chosen from the finite interval and number at most |I_d|-1.

Equivalently, if no such chain exists, there is eta>0 such that **no** pair
of realized distance matrices within eta of the two endpoints can be joined
by a finite strong chain. The number of factors in an approximating chain
may tend to infinity, and both endpoints may vary.

**Proof.** Put S=I_d(P,Q), and draw a directed edge U -> V between its
distance matrices when (1) holds for representatives. Let R be the states
reachable from D(P). If D(Q) is reachable, delete repeated states from a
path; all remaining edges are contractions, giving the stated length bound.

Suppose instead that D(Q) is outside R. Every intermediate distance matrix
Z in an approximating chain satisfies

    D(Q_n) <= Z <= D(P_n).                                  (2)

Uniformly over **all stages of all sufficiently late chains**, the distance
from Z to S tends to zero. Otherwise take offending stages with distance
at least epsilon from S. Their distances are bounded by (2). Translating
one label to zero gives bounded representatives and a convergent subsequence.
Its limit is realizable and lies between D(Q) and D(P), hence in S, a
contradiction. This uses compactness of bounded realizable distances, not
compactness of an entire sequence of paths.

Choose disjoint small neighborhoods of the finitely many states of S. For
large n every stage lies in their union; the initial stage is near D(P),
and the terminal stage near D(Q). There is therefore an adjacent step
crossing from a neighborhood of R to a neighborhood of S minus R.
Along a subsequence the two neighboring states converge to fixed
U in R and V in S minus R. Closedness of (1) implies U -> V, contrary to
the definition of R. Thus approximation is impossible. QED.

The argument applies verbatim to any closed, isometry-invariant elementary
relation of contractions that contains isometries. Finiteness is essential
to this proof: a compact interval with infinitely many states need not
provide separated neighborhoods or a finite reachable-state cut.

**Indecomposable corollary.** If I_d(P,Q)={D(P),D(Q)} with distinct endpoints,
approximation by finite strong chains is possible if and only if P -> Q
is itself a strong step with free frames. In particular, a failed one-step
test on such a pair yields a neighborhood excluding all finite strong chains.

Adding arbitrarily many auxiliary labels cannot evade an obstruction on the
original N labels: restrict every step to those labels. The conclusion also
excludes limits of finite prefixes of a convergent infinite chain. It does
not concern operations that replace labelled sites by mixtures or use a
higher ambient dimension.

## 3. The preserved seven-site control

Use the existing control from the
[three-cap theorem, Section 6](../gaussian_disjoint_cap_reflections/PROOF.md).
It is reproduced here to expose every hypothesis of the new closure result,
not claimed as a new construction. Fix the four sites

    c0=(0,0,0), c1=(-1,-1,0), c2=(-1,0,1), c3=(0,-1,1).

For i=0,1,2 put

    v0=(1,1,1), v1=(1,-1,-1), v2=(-1,1,-1),
    x0=(1,-2,5), x1=(-2,-5,-1), x2=(-5,1,2),
    y_i=x_i-(8/3)v_i.

Let P=(c0,c1,c2,c3,x0,x1,x2) and Q=(c0,c1,c2,c3,y0,y1,y2).
Each moved site preserves distances to the three core sites in v_i.x=0;
they are noncollinear. The core determinant is -2. After aligning the core,
every intermediate site must be x_i or y_i, giving eight placements.
For the cyclic pairs (0,1),(1,2),(2,0), their squared distances are

| Reflection bits | 00 | 10 | 01 | 11 |
| --- | --- | --- | --- | --- |
| Squared distance | 54 | 34/3 | 130/3 | 134/9 |

Every nonconstant cyclic bit string has a 10. Its value 34/3 is below
the final 134/9, so it cannot occur between P and Q. Both endpoints satisfy
all 21 contraction inequalities. Thus the **complete** interval consists
of the two endpoints, rather than merely two states in a chosen model.

There is no strong step with free frames. The fixed core preserves all six
distances. Equality in the sum of squared coordinate inequalities forces
equality for each coordinate separately on all core pairs. The two scalar
labelled core configurations are related by a sign and translation. Because
c0=0 and the core spans R3, each output axis equals its input axis up to
sign. We may consequently use one common frame.

For a moved site whose scalar coordinate changes, equality of its distances
to all three tight anchors forces all three anchor coordinates to be the
same midpoint. That coordinate axis must be perpendicular to their plane,
hence parallel to v_i. Each nonzero displacement changes some coordinate.
All three v_i would therefore have to be axes of one orthonormal frame.
They are independent and have mutual dot products -1, which is impossible.

**Conclusion.** There is an open neighborhood of (D(P),D(Q)) containing no
pair joinable by a finite chain of strong contractions, even with changing
frames and auxiliary labels. The earlier exact-chain exclusion did not
state this approximation conclusion.

The example is nevertheless positive for every weighting, Gaussian variance,
and threshold, and for both arbitrary-radius ball-volume inequalities, by
the existing cap motion. Its normals lie in a hemisphere, witnessed by
(1,1,-1). The
[accepted hemisphere/four-cap theorem](../gaussian_cap_auxiliary_certificates/PROOF.md)
and its [review](../gaussian_cap_auxiliary_review2/REVIEW.md) supply the positive
side. That review did not review the strong-chain comparison; this supplement
supplies its own written argument and retains a pending-review status.

## 4. Consequence for the rational finite frontier

This obstruction is not confined to exact tight-edge inputs. Choose any
rational 0<lambda<1 sufficiently close to 1 and replace Q by lambda Q.
Every target pair is distinct, so every squared pair loss is now strictly
positive. The pair remains inside the excluded neighborhood. This is a
consequence about a perturbation of the same control, not a new cap theorem.

Choose an integer D clearing all coordinates of P and lambda Q. For all
sufficiently large k divisible by 7D, these exact endpoints, with uniform
weights 1/7, belong to the existing rational family R^c_k:

- 7<=A_k and both endpoint radii are at most 3k;
- L=256k^3 clears the coordinates, with the first labels at zero;
- the fixed positive squared-loss minimum eventually exceeds 1/(256k^4);
- W=4kA_k is divisible by 7.

These are precisely the constraints in
[the paired-cubature frontier, Section 5](../gaussian_prior_localization/CUBATURE_FRONTIER.md).
No padding or rerounding is necessary. Hence that finite frontier contains
strict rational inputs outside even the closure of finite strong chains.
This prevents discarding that portion by a claimed universal strong-fold
approximation theorem. It supplies **no negative Gaussian value**: the
chosen perturbation is positive by composing the cap map with a homothety.

The neighborhood proof gives no numerical eta, lambda, or first k. The
exact checker does not certify a particular perturbed rational-frontier
member. Nor can the strict-pair endpoint cutoff be applied to the original
tight control without this change of map. The middle-threshold sign on
general frontier inputs remains open.

## 5. Validation and limits

[strong_closure_control.py](strong_closure_control.py) checks the preserved
coordinates, core and face determinants, all eight placements, all 21 pair
bounds, the cyclic table, nonorthogonal normals, and the paired determinant
4096/27. It also checks the existing convex-hull cap separators and three
damaged inputs. It imports neither earlier checker nor expected output.

The compactness theorem, scalar-frame argument, and rational-frontier
existence argument are written mathematics. No program checks all frames,
all chains, a neighborhood radius, or a Gaussian integral. These finite
controls are author validation, not independent mathematical acceptance.
No universal failure of approximation by arbitrary contractions is claimed.

The primary-source comparison and the exact boundary of the novelty claim
are in [CAP_PRIOR_ART.md](CAP_PRIOR_ART.md). The accepted orthocentric
depth-one theorem and both former tournament templates remain closed at
their existing reviewed scope; nothing here reopens them.
