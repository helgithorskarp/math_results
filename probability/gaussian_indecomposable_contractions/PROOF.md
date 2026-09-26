# Reducing Gaussian majorisation to indecomposable finite contractions

Complete author proof, 26 September 2026. Independent correctness and
historical-priority review are pending. This is an equivalent test class for
the unrestricted dimension-three problem, not a proof of its missing sign.
The geometric input is classical Brehm extension; the new proposed application
is the reduction through a finite interval of distance matrices.

## 1. The test class

For a labelled configuration $P=(p_1,\ldots,p_N)$ in $\mathbb R^3$, let
$d(P)=(|p_i-p_j|^2)_{i<j}$. Inequalities between these vectors are coordinatewise.
Repeated locations are allowed. Say that $Q$ is a contraction of $P$ when
$d(Q)\le d(P)$, and define its full three-dimensional interval by

$$
\mathcal I_3(P,Q)=\{d(Z):Z\in(\mathbb R^3)^N,
                 \ d(Q)\le d(Z)\le d(P)\}.
\tag{1}
$$

We call the contraction **indecomposable** if $d(P)\ne d(Q)$ and

$$
\mathcal I_3(P,Q)=\{d(P),d(Q)\}.
\tag{2}
$$

This definition quantifies over every labelled intermediate configuration in
$\mathbb R^3$, not a preselected family of motions or folds. Equality of
complete labelled distance matrices means congruence by an ambient Euclidean
isometry: centering at one label determines the Gram matrix and hence an
isometry of the spans, which extends to the ambient space.

Let $\gamma_s$ have covariance $sI_3$, and write
$H_f(a)=\int(f-a)_+$. For nonnegative weights summing to one, put

$$
\Phi_{w,s,a}(P)=H_{\sum_i w_i\gamma_s(\cdot-p_i)}(a).
\tag{3}
$$

**Theorem A (full-question reduction).** Full Gaussian majorisation for every
bounded probability law and every 1-Lipschitz map in $\mathbb R^3$ is equivalent
to the following restricted assertion:

> For every indecomposable finite contraction $P\to Q$ fixing four affinely
> independent labelled points, every strictly positive probability weight
> vector $w$, every $s>0$, and every $a>0$, one has
> $\Phi_{w,s,a}(Q)\ge\Phi_{w,s,a}(P)$.

One can further require a common system of nondegenerate tetrahedra covering
all labels, connected through triangular faces, all of whose edge lengths
are preserved. At both endpoints this supplies an infinitesimally rigid
tight framework and an extreme anchored finite contraction. Its placement
at an extracted step need not be an embedded triangulation of a convex body.
Weights at coincident input labels may instead be merged into one positive
atom; the indecomposability property is unchanged.

The same test can be made at variance one by scaling. There is no uniform
bound here on the number of labels, tetrahedra, reflection states, or chain
length. Rational coordinates are not asserted. This tight test class differs
from the known equivalent class of strictly contracting rational data.

## 2. A finite interval from common tetrahedral edge lengths

**Lemma 1.** Suppose that a facet-connected finite tetrahedral complex has
$m$ tetrahedra and all $N$ labels as vertices. Suppose each tetrahedron is
nondegenerate in $P$ and all its six edge lengths agree in $P,Q$, where
$d(Q)\le d(P)$. Then

$$
|\mathcal I_3(P,Q)|\le2^{m-1}.
\tag{4}
$$

**Proof.** Every intermediate configuration in (1) preserves all these common
edge lengths. Thus every tetrahedron has its original nondegenerate shape.
Align one root tetrahedron to its labelled position in $P$ by an ambient
isometry. Take a spanning tree of the tetrahedra's facet-adjacency graph.
When a new tetrahedron is reached, its three shared-face vertices are already
placed and are noncollinear. The distances to these vertices place its fourth
vertex at exactly two possible locations, interchanged by reflection in the
face plane. If that vertex has already been placed, only consistent choices
are retained. Additional cycle and shared-vertex consistency conditions can
only remove candidates. Hence at most $2^{m-1}$ labelled placements remain.
Their distance matrices include all of (1), proving (4). No path continuity
or generic-position hypothesis is used. Coincidences between vertices in
different cells are permitted. QED.

Nondegeneracy of every cell, not infinitesimal rigidity at just the endpoints,
is what makes this global count immediate. A mesh may overlap itself after
placement; the argument uses the common labelled cells and their distances.

**Lemma 2 (finite factorization).** If the interval (1) is finite, there is
a chain from $d(P)$ to $d(Q)$ in which every nontrivial consecutive step is
indecomposable. Its length $L$ is at most $|\mathcal I_3(P,Q)|-1$.

**Proof.** Choose a saturated descending chain in the finite coordinatewise
partially ordered set (1). If an intermediate $R$ existed strictly between
the distance matrices of a covering step, its distances would also lie
between $d(Q)$ and $d(P)$. It would therefore belong to (1), contrary to
saturation. This excludes all intermediate configurations, rather than just
ones selected in a particular enumeration. QED.

Choose representatives of all states fixing the same root tetrahedron.
The labelled map between consecutive states is well defined: if two labels
coincide before a contraction, their output distance is at most zero, so they
coincide afterwards. Consequently it is a genuine 1-Lipschitz map of the
finite support, even when labels merge. Each factor fixes the root tetrahedron.
The last representative is congruent to the prescribed $Q$; a final ambient
isometry restores $Q$ itself when exact positions, rather than distances, matter.

## 3. Brehm extension makes the finite interval available

We use the classical extension theorem of
[Brehm](https://link.springer.com/article/10.1007/BF01917587), also stated in
all dimensions in the final remarks of
[Petrunin--Yashinski](https://arxiv.org/pdf/1405.6606): a contraction prescribed
on a finite Euclidean set extends to a piecewise distance-preserving map.

Given any finite contraction on $X\subset\mathbb R^3$, choose a full-dimensional
compact convex polytope $C$ containing $X$. On $C$ take a finite tetrahedral
triangulation on whose cells the extension $F$ is an isometry, and refine it
so every original point is a vertex. Denote its vertex set by $V$. The source
configuration $P=(v)_{v\in V}$ and target $Q=(Fv)_{v\in V}$ preserve all
mesh edges. Continuity on the convex domain gives $|Fv-Fw|\le|v-w|$ by
partitioning the segment $[v,w]$ into cell pieces and comparing its image
polygonal path with its endpoint chord. Facet adjacency is connected.

Lemmas 1--2 therefore apply. Every finite contraction, after adding finitely
many labels, factors into indecomposable finite contractions, with a possible
final ambient isometry. The augmented input and output are exact extensions
of the prescribed data. For full-dimensional $X$ one can take
$C=\operatorname{conv}X$, so auxiliary inputs do not enlarge its convex hull.

Every factor retains the same common tetrahedral edge lengths. On a
nondegenerate tetrahedron, any infinitesimal flex is a Euclidean rigid
velocity field. Two such fields agreeing on three noncollinear points of a
shared face are equal. Propagation over the connected cells proves rigidity
rank $3|V|-6$ at every placement. The common tight graph is connected; the
classical anchored extremality criterion then also applies. These facts and
the Brehm extension are credited and explained in the earlier
[rigid-mesh reduction](../gaussian_majorisation_extremal_maps/PROOF.md).
Neither property alone is identified with indecomposability.

After aligning the root tetrahedron, all configurations in the interval have
diameter at most $\operatorname{diam}C$. In particular, fixing a root vertex at
zero places every state in $B(0,\operatorname{diam}C)$. The placements need not
stay in the original convex hull, but this diameter control survives.

## 4. A strict Gaussian failure survives on a covering step

Suppose a finite law on $X$ has a gap
$\Phi(Q)-\Phi(P)=-\delta<0$ at a fixed variance $s$ and threshold $a$.
First regard its weights as a vector on the augmented $V$, with zero mass on
the new vertices. Choose any probability vector $u$ positive on all of $V$,
and set $w^\epsilon=(1-\epsilon)w+\epsilon u$.

For probability densities $f,v$, the positive-part function gives

$$
0\le H_{(1-\epsilon)f+\epsilon v}((1-\epsilon)a)
       -(1-\epsilon)H_f(a)\le\epsilon.
\tag{5}
$$

Applying this at the two endpoints yields

$$
\left|\Phi_{w^\epsilon,s,(1-\epsilon)a}(Q)
 -\Phi_{w^\epsilon,s,(1-\epsilon)a}(P)+(1-\epsilon)\delta\right|
\le\epsilon.
\tag{6}
$$

Choose, for example, $\epsilon=\delta/[2(1+\delta)]$. Then the new endpoint
gap is at most $-\delta/2$, and every label has positive mass. Along a
saturated chain $P=P^0,P^1,\ldots,P^L$ ending at a congruent copy of $Q$,
the fixed-parameter scalar functional (3) telescopes:

$$
\sum_{j=1}^L\big[\Phi_{w^\epsilon,s,(1-\epsilon)a}(P^j)
              -\Phi_{w^\epsilon,s,(1-\epsilon)a}(P^{j-1})\big]
\le-\delta/2.
\tag{7}
$$

For some indecomposable step its gap is at most $-\delta/(2L)$. If the mesh
has $m$ cells, $L\le2^{m-1}-1$. A genuine failure has $L\ge1$, so the
denominator is nonzero. Isotropic Gaussian convolution and the hinge are
invariant under the isometries used to align the representatives.

If two labels coincide at that step's input, they coincide at its output and
at every configuration of its interval. Deleting one repeated label, and
adding its mass to the other, gives a bijection between the old and new
distance intervals. The gap and indecomposability are unchanged. The four
root labels remain distinct, fixed, and of positive mass.

Finally, every bounded-law strict failure has a finite strict approximation.
Choose finitely many support representatives at input distance at most $r$,
retain their exact images and cell masses, and use

$$
\|\gamma_s(\cdot-x)-\gamma_s(\cdot-y)\|_1
\le\sqrt{2/(\pi s)}|x-y|,\qquad
|H_f(a)-H_g(a)|\le\|f-g\|_1.
\tag{8}
$$

The image displacement is also at most $r$. The total gap error tends to
zero. Apply the preceding construction to a surviving finite failure.
This proves the nontrivial implication of Theorem A; its converse follows
because the restricted data are ordinary contractions. Scaling positions by
$s^{-1/2}$ and the threshold by $s^{3/2}$ gives the variance-one version.
If a globally defined map is required, Kirszbraun extension supplies one
from each finite contraction; only the support values enter the Gaussian law.

Important limits: (7) preserves the sign but need not preserve a fixed
fraction of the original gap independently of the mesh. The maximal defect
over indecomposable pairs is not proved equal to the unrestricted maximal
defect. No complexity bound or effective uniform mesh construction is
obtained from compactness. The extracted input placement may be folded;
one cannot silently reimpose an embedded convex-source mesh there. Individual
label weights stay fixed along the chain, but the total mass at a location
can increase through collisions, including at a distinguished fixed atom.

Augmentation is essential to the proof. For two labels whose distance shrinks
from 1 to $1/2$, the interval of squared distances is the whole $[1/4,1]$;
it has no nontrivial covering steps. Compactness alone does not replace the
finite-placement argument or yield this factorization on the original labels.

The known paired-rank criterion still applies: a negative step must have at
least seven distinct input points and paired affine rank six. With a fixed
full-dimensional tetrahedron, paired rank is $3+$ the dimension spanned by
the displacement vectors $q_i-p_i$. Thus their span must be all of $\mathbb R^3$.
This is a consequence of the existing
[rank theorem](../gaussian_majorisation_rank_abel/PROOF.md), not a new sign bound.

## 5. The corresponding ball-volume reductions

The geometric factorization also reduces each arbitrary-individual-radius
Kneser--Poulsen question to indecomposable finite pairs fixing a tetrahedron.
This is another reduction, not a new positive volume theorem.

For unions, give auxiliary labels radius zero. Their singleton balls have
zero volume and do not alter any original union volume. If the indecomposable
union inequality holds for every positive radius assignment, it also holds
with zero radii by continuity. Applying it along the factor chain proves the
original union inequality. Equivalently, any strict union failure survives
after sufficiently small positive auxiliary radii and forces a failure on
one covering step.

For intersections, first align all states to the fixed root and place one
root vertex at zero. All centres have norm at most $D=\operatorname{diam}C$.
If the largest original radius is $R$, every original ball lies in $B(0,D+R)$.
Give every auxiliary label radius $M=2D+R+1$. At every state its ball contains
$B(0,D+R)$, so intersecting with the auxiliary balls changes none of the
original intersections. Apply the proposed indecomposable intersection
inequality along the same finite chain. Union and intersection use different
auxiliary radius assignments; neither assignment is suppressed in this argument.

## 6. Exact controls: decomposability, positivity, and nonliftability

The controls below have a fixed core tetrahedron. Every other label preserves
its distances to three noncollinear core vertices and lies off their plane.
The intersection of the three prescribed spheres therefore has exactly two
points, the original point and its reflection. Enumerating all binary choices,
then imposing all distance bounds, gives the *complete* interval (1).

**A decomposable control.** Fix $(0,0,0),(-1,0,0),(0,-1,0),(0,0,-1)$.
Send $(1,-1,-1)$ and $(-1,1,-1)$ both to $(-1,-1,-1)$. The interval has four
states, ordered as a diamond: $00\to01\to11$ and $00\to10\to11$.
Its common face attachments are rigid, yet the endpoint map is decomposable.
The two saturated chains and the target collision are checked exactly.

**A positive indecomposable control.** The seven-site configuration in the
[three-cap reflection theorem](../gaussian_disjoint_cap_reflections/PROOF.md)
has eight face-reflection placements but only the two endpoint distance
matrices in (1). Its cyclic pair table $54,34/3,130/3,134/9$ excludes every
mixed state. It nevertheless has the explicit R5 contracting motion and all-law
Gaussian and arbitrary-radius positive conclusions proved in that packet.
The checker reproduces its full interval without importing that packet's code.

**The classical simplex flaps remain indecomposable.** Let $v_0,\ldots,v_3$
be the four vectors in $\{-1,1\}^3$ with coordinate product 1. Their squared
norms are 3 and their distinct inner products are $-1$. Keep them fixed and,
for every $i\ne j$ and every common depth $t>0$, prescribe

$$
p_{ij}=v_j-t v_i\longmapsto q_{ij}=v_j+t v_i.
\tag{9}
$$

These are the classical outward-to-inward simplex flaps, scaled by $\sqrt3$.
They contract: core-to-flap squared distances either stay fixed or decrease
by $16t$, while for two flap labels the target-minus-source squared-distance
difference is

$$
4t(v_j-v_l)\cdot(v_i-v_k)
=-16t(\mathbf1_{j=k}+\mathbf1_{l=i})\le0.
\tag{10}
$$

Here $j\ne i$ and $l\ne k$; the formula also includes pairs in the same flap.
The three core anchors of flap $i$ lie in $v_i\cdot x=-1$, so every
intermediate label must choose one of its two positions in (9).

All three labels of a given flap must choose the same sign. If two choose
different signs, their squared distance becomes $8+12t^2$ instead of the
common endpoint value 8. Now consider distinct flap indices $i,k$ and a
common tip index $j\notin\{i,k\}$. The corresponding pair has squared distance
$8t^2$ at both endpoints. Opposite flap signs would make it $4t^2$, violating
that common tight distance. Therefore all four flap signs agree.
Only the two endpoint placements remain, proving indecomposability for every
$t>0$, using just common tight distances.

[Cheng--Tan--Zheng, Theorem 2.1](https://arxiv.org/pdf/1107.0140) proves that
these endpoints have no continuous contracting motion in R5. The construction
and nonliftability theorem are prior work, not a new example here. We record
the direct finite-interval argument to make their role in the reduced class
explicit. Indecomposability therefore does not supply an R5 motion, and the
Gaussian sign for arbitrary flap weights is not settled by this packet.

The checker exhausts all $2^{12}=4096$ individual reflection choices at depths
1 and 2. Both yield two tight placements and two interval matrices; their
paired rank is six. Depth 1 has 16 distinct inputs and ten distinct outputs;
depth 2 has 16 at each endpoint. These test collision handling as well as an
injective target. No computational enumeration is used to infer the statement
for all depths; that statement follows from the two displayed distances.

There is also a useful boundary with the cap theorem. Although each original
flap vertex lies outside only its own simplex face, the relevant outward caps
overlap inside the source convex hull. For $j\notin\{i,k\}$, the midpoint
$z=v_j-(t/2)(v_i+v_k)$ of $p_{ij},p_{kj}$ satisfies
$v_i\cdot z=v_k\cdot z=-1-t<-1$. Thus it lies beyond both faces. Checking
disjointness only on the finite labels would give a false cap certificate.

## 7. What this establishes and leaves open

The new proposed reduction uses a classical geometric extension to obtain a
finite interval, takes its covering steps, and transfers a hypothetical
negative hinge by telescoping. It does not use convexity in image positions,
preservation under conditioning, or a claim that general extreme maps have
low-dimensional motions. Existing localization and fixed-atom reductions
retain their separate quantifiers and errors.

The positive cap example and classical nonliftable flaps both belong to the
indecomposable test class. Proving the desired sign on that entire class is
still equivalent to the full question. Merely failing to factor a map, or
failing to construct its R5 motion, supplies no negative Gaussian hinge.
The bounded literature search found no exact prior statement of the present
Gaussian reduction; that search does not establish historical novelty.
