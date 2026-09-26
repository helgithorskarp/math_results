# Atomic rigidity and a simultaneous obstruction

All measures below are probability measures. A continuous contraction means
a continuous motion of labeled points during which every pair distance is
nonincreasing. Eigenvalues are listed in decreasing order; in dimension three
`lambda_2` is the middle eigenvalue. Convex order of random vectors must not
be confused with majorisation of their probability densities.

## 1. Common-output mixtures cannot improve an injective atomic map

This is researcher 8's prior Theorem B in
[the common-target packet](../gaussian_majorisation_common_target/PROOF.md).
We repeat the proof, allowing continuous mixtures and output isometries,
to state precisely the premise used below. Those routine extensions are
not the new contribution of this packet.

**Lemma 1 (prior atomic rigidity).** Let

\[
\mu=\sum_{i=1}^n w_i\delta_{x_i},\qquad
\nu=\sum_{i=1}^n w_i\delta_{y_i},\qquad w_i>0,
\]

where the points within each support are distinct. Suppose
`mu = integral mu_t d alpha(t)`, where `alpha` is a probability measure, and
each `mu_t` has a deterministic map to a law isometric to `nu`.
Then `mu_t = mu` for almost every `t`. After aligning each output with `nu`,
the map permutes the atoms and preserves their masses. If all the `w_i` are
distinct, its matching is exactly `x_i -> y_i`.

This statement needs no contraction assumption.

**Proof.** Nonnegativity and the mixture identity imply that `mu_t` is supported
on `X={x_1,...,x_n}` almost surely. Its deterministic image has `n` positive
atoms, so the map is a bijection. Its source mass vector `r_t` is therefore
a permutation of `w`. In particular, `||r_t||_2^2=||w||_2^2` and
`integral r_t d alpha=w`. Hence

\[
\int\|r_t-w\|_2^2\,d\alpha(t)
=\int\|r_t\|_2^2\,d\alpha(t)-\|w\|_2^2=0.
\]

Thus `r_t=w` almost surely. Distinct masses identify the matching. QED.

The statement also applies if the common output is specified by its Gaussian
convolution at one fixed positive variance: the Gaussian Fourier transform
never vanishes, so equality of those convolutions implies equality of the
center measures. It applies to finite or continuous mixtures, and permits
separate output isometries in the component comparisons.

**Consequence for proof methods.** Suppose a class of deterministic
contractions supplies the desired Gaussian comparison, and one tries to
enlarge it by expressing an input as a positive mixture whose components
all have one common output. On an injective finite atomic pair with distinct
masses, this cannot bypass failure of the original matching to belong to
that class. The result does not apply when the original map merges atoms;
the surplus source atoms then allow nontrivial splitting. It also says
nothing about comparison kernels that do not arise from deterministic maps,
different component outputs, or decompositions changing the Gaussian variance.

## 2. The anchored square-cone geometry

Set

\[
\begin{split}
a_1&=(1,0,1),&a_2&=(0,1,1),&a_3&=(-1,0,1),&a_4&=(0,-1,1),\\
b_1&=(1,1,1),&b_2&=(-1,1,1),&b_3&=(-1,-1,1),&b_4&=(1,-1,1).
\end{split}
\]

The ordered supports are `X=(0,A,-B)` and `Y=(0,A,B)`. All labels except
the `B` labels are fixed. Since `a_i dot b_j` is either 0 or 2, the cross
squared-distance loss is `4 a_i dot b_j`, either 0 or 8. All other losses
vanish. Among the 36 pairs there are eight losses of 8 and 28 of 0.
Consequently the map is 1-Lipschitz on its finite support. Kirszbraun's
extension theorem makes this a valid instance of the globally defined map
in Aishwarya--Li's conjecture; no particular extension is needed for these laws.

**Lemma 2 (prior geometric obstruction).** This labeled map has no continuous
contraction in `R^5`.

**Proof.** Translate the moving origin to zero. The `A` and `B` Gram matrices
are each constant throughout any contraction because all their endpoint
distances, including their distances from zero, agree. Thus there are linear
isometric embeddings `G_t,F_t:R^3 -> R^5` with anchor positions `G_t a_i`
and moving positions `F_t b_j`. Write `L_t=G_t^* F_t`.

For every zero incidence `a_i dot b_j=0`, the corresponding cross distance
also agrees at the endpoints and must remain constant. Hence
`a_i dot L_t b_j=0`. The two independent zero incidences of each `b_j` force
`L_t b_j=lambda_j(t)b_j`. The first three `b_j` are independent, and

\[
b_1-b_2+b_3-b_4=0.
\]

Applying `L_t` to the circuit shows that all four scalars are equal.
Therefore `L_t=lambda(t) I`. It is continuous, starts at `-1`, and ends at `1`.
At a time when it is zero, `F_t(R^3)` is orthogonal to `G_t(R^3)`, which is
impossible in `R^5`. QED.

This is the square-cone obstruction in the earlier cone-reflection packet,
not a new claim about the minimal size of an arbitrary nonliftable map.
An endpoint or starting configuration moved by an isometry does not remove
the obstruction: any isometry between embedded copies of `R^3` can be joined
by a rigid motion in `R^5` (use a spare dimension to realize a reflection).

For orientation, nine is minimal **within central reflections of two
positively dual clusters with a labeled fixed origin**. With at most seven
other sites, one cluster has at most three vectors. If those vectors have
rank at most two, the paired linear span has dimension at most five and the
standard leapfrog path lies there. If they have rank three, their positive
cone is simplicial and the earlier cone-reflection theorem applies. One can
interchange the two clusters after an overall central reflection. This
restricted observation does not assert global minimality.

## 3. Every bijective contraction between these supports

**Lemma 3.** There are exactly 64 bijections `X -> Y` that are contractions.
Each fixes the origin, applies a square symmetry to the four `A` labels,
and independently applies a square symmetry to the four `B` labels.

**Proof.** The largest squared distance from the input origin is 3. The
largest squared distance from an output `A` point is 5 and from an output
`B` point is 8. Surjectivity forces the origin to map to the origin. An input
`A` point has squared norm 2, so cannot map to a `B` point of squared norm 3.
The two four-point groups are therefore preserved. Within either group,
a permutation preserves the sum of all squared distances. Nonexpansion of
each pair then forces preservation of every pair, so each permutation is one
of its eight square symmetries. Conversely all 64 choices are contractions:
output cross distances are at most 5, whereas input cross distances are at
least 5. QED.

Eight have paired rank 4, 32 have paired rank 5, and 24 have paired rank 6.
The first 40 admit the standard low-rank lifting proof. We do not assert
that rank 6 alone rules out other motions for the remaining maps.

## 4. Exact covariance separation

Assign the distinct weights

\[
w=(8,12,7,15,44,21,11,23,43)/184.                 \tag{1}
\]

Their centered covariance matrices are `C_X=M_X/33856` and
`C_Y=M_Y/33856`, with

\[
M_X=\begin{pmatrix}
21911&-1939&4308\\-1939&27407&-13124\\4308&-13124&31984
\end{pmatrix},\qquad
M_Y=\begin{pmatrix}
22271&77&216\\77&22375&-568\\216&-568&1408
\end{pmatrix}.                                             \tag{2}
\]

For `C_X-(16/25)I`, the exact unpivoted LDL diagonal is

\[
\left(\frac{6079}{846400},
-\frac{4015263}{13981700},
-\frac{1340459009}{2308776225}\right).
\]

For `C_Y-(13/20)I` it is

\[
\left(\frac{1323}{169280},\frac{127}{12420},
-\frac{1853737}{2862580}\right).
\]

Sylvester's law of inertia gives respectively one and two positive
eigenvalues. Consequently

\[
\lambda_2(C_X)<\frac{16}{25}<\frac{13}{20}<\lambda_2(C_Y).    \tag{3}
\]

**Theorem 4.** After any separate Euclidean isometries, these laws do not
admit a coupling `(U,V)` with `U` the input, `V` the output, and
`E[U|V]=V`. The same is true after adding independent isotropic Gaussian
noise of any common variance to both laws.

**Proof.** Such a coupling would give
`Cov U - Cov V = E[(U-V)(U-V)^T] >= 0`. The min-max principle implies
coordinatewise ordering of the decreasing covariance eigenvalues.
Translations do not affect covariance and rotations do not affect its
eigenvalues. This contradicts (3). Common isotropic noise adds the same
scalar to each eigenvalue and leaves the contradiction intact. QED.

This rules out the martingale sufficient criterion for eventual Gaussian
comparison in the team's endpoint theorem. It does not refute that theorem
or imply failure of its spherical inequality.

## 5. An open set of weights and a quantitative splitting obstruction

**Theorem 5.** For every probability vector `p` with
`||p-w||_1 <= 1/4000`, the pair on these same ordered supports has distinct
positive masses and satisfies both Theorem 4 and the following obstruction:
it cannot be obtained by a common-output positive mixture of deterministic
maps having continuous contracting motions in `R^5`.

**Proof.** All support vectors have squared norm at most 3. For any two
probability vectors at L1 distance `delta`, their covariance matrices on
either support differ in operator norm by at most `9 delta`: the raw second
moment contributes at most `3 delta`, and the difference of the mean outer
products at most `6 delta`. The eigenvalue min-max principle and (3) give

\[
\lambda_2(C_Y(p))-\lambda_2(C_X(p))
>\frac1{100}-18\delta\ \geq\ \frac{11}{2000}>0.
\]

The smallest original mass is `7/184`, and the smallest gap between two
distinct original masses is `1/184`. Positivity and distinctness persist
since `delta <= 1/4000`. Lemma 1 therefore forces every common-output
component to use the original labeled matching, which Lemma 2 excludes
from the five-dimensional motion class. QED.

The obstruction is unchanged by a common scaling or by separate endpoint
isometries; its covariance margin scales by the square of the scale.

**Theorem 6 (approximate outputs on the same support).** At the central
weight vector (1), the following relaxation also fails. One cannot write
`mu_w` as a positive mixture of input laws on `X`, each carried by a
five-dimensionally continuously contracting deterministic map to a law on
`Y` with positive mass vector `q_t` satisfying

\[
\|q_t-w\|_1<1/851
\]

almost surely. Separate output isometries are allowed before aligning
their supports and mass vectors with `Y`.

**Proof.** Each component map is a bijection, so Lemma 3 applies. If `P` is
its source mass permutation, `r=Pq`. The identity matching is unavailable
by Lemma 2. For every other contraction permutation,

\[
w\cdot(w-Pw)=\tfrac12\|w-Pw\|_2^2\ \geq\ \frac4{184^2}
=\frac1{8464}.                                           \tag{4}
\]

Indeed the origin is fixed and the two groups are separately permuted;
the smallest mass difference in the `A` group is `3/184`, and in the `B`
group `2/184`. Any nontrivial permutation moves at least two entries.
Equality in (4) is attained by the square reflection interchanging the
`B` masses 21 and 23 and fixing the other labels; it has paired rank 5.

For a zero-sum vector `e`, `w dot Pe` is at most
`(max w-min w)||e||_1/2`. Since `max w-min w=37/184`,

\[
w\cdot r\leq \|w\|_2^2-\frac1{8464}
                +\frac{37}{368}\|q-w\|_1<\|w\|_2^2.
\]

Here `(1/8464)/(37/368)=1/851`. Averaging contradicts
`integral r_t d alpha=w`. The positive pointwise deficit has positive
integral, so a uniform strict margin below `1/851` is not required. QED.

This is a certified separating bound, not a claim that `1/851` is the
optimal distance to that class. It concerns perturbing weights on the
same supports, not arbitrary perturbations of the centers.

## 6. What remains

The published common-output construction for collapsed tetrahedral
rays uses twelve source rays and six output rays, so Lemma 1 does not
obstruct that construction. It explains precisely why that mechanism
cannot be transferred unchanged to generic injective finite pairs.

The nine-point law is a rational, robust test for methods beyond both
deterministic low-dimensional motions and center-law convex order. Its
Gaussian hinge inequality has not been decided here. No new
Kneser--Poulsen volume inequality or Gaussian counterexample is claimed.
The original full-dimensional problem is the sole research target; this
packet supplies an exact obstruction to two routes toward it.
