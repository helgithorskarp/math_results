# All-eight handoff: the axial benchmark and extremal-map geometry

26 September 2026. This note records the human-authorized eight-lane
assignment and makes the existing geometric benchmark reusable. It adds
no positive subclass, improved constant or motion construction. The axial,
nonlinear-robustness and matrix proofs retain the scope and review status
in [REVIEW_GUIDE.md](REVIEW_GUIDE.md). Independent correctness and priority
review remain pending; the full bounded-law R3 question is open.

The geometric/internal-energy lane remains researcher 6. Researcher 4's
new extremal-map/deformation lane has a different primary task: reducing
arbitrary contractions to a sufficiently general extremal test class.
Both lanes use geometry, but a reduction of the unknown sign and a
construction proving that sign have different outputs.

The subsequent [hinge-margin theorem H](HINGE_MARGIN.md) adds a quantitative
interface on the existing motion class. It turns an R5 contracting motion
and an endpoint squared-distance defect D into a bound for the actual
hinge gap, with an explicit constant below a certified source peak. R4
retains construction and classification of new extremal maps; H consumes
a motion certificate. R2 receives exact benchmark inputs without needing
hinge quadrature, and R8 can compare its reference margins with H's actual
gap under this additional geometric hypothesis. No new subclass is added.
The same source's H2 completion replaces the source-peak cutoff with any
certified target peak, using a terminal pair-loss interval. It requires
the same motion certificate, and no R3 representation of the intermediate
configuration is assumed. The source and target bounds can be used together.

## 1. Ownership and reusable inputs

The lane numbers below are the current human assignment. Source links
identify reusable artifacts, not a claim about exclusive authorship of
every earlier input.

| Lane | Current responsibility | Interface with this benchmark |
| --- | --- | --- |
| 1 | Independent semigroup/PDE evolution; [heat-profile source](../gaussian_majorisation_heat_profiles/PROOF.md) | A and R provide all-variance positive geometric controls. Their positivity does not imply the proposed pointwise ordering of a PDE coefficient. An integrated comparison must retain its own signed forcing and boundary-data obligations. |
| 2 | Certified finite-atomic dependencies; [finite orthogonal averaging obstruction](../gaussian_majorisation_finite_orbit_obstruction/PROOF.md) | The exact labeled sites, weights, distance deficits and constants in this packet are reusable inputs. The universal proofs are not replaced by finite positive moments or a finite path grid. The averaging obstruction concerns a fixed finite pointwise rule for all weights, not the integrated hinge sign. |
| 3 | Measure-side localization and extremal reduction; [common-set transfer](../gaussian_prior_localization/PROOF.md), [uniform defect localization](../gaussian_prior_localization/DEFECT_LOCALIZATION.md) | On any compact subset of a certified domain, A/R prove the common-set theorem's all-law premise. The new localization bounds a strict witness by its defect size; it does not bound the subsequent rigid mesh or prove positivity of the resulting compact finite problem. |
| 4 | Extremal-map structure and admissible deformation; [rigid-mesh reduction](../gaussian_majorisation_extremal_maps/PROOF.md) | Use the distinctions in Sections 2--4 below. Extreme maps, rigid tight frameworks, compatible cell reflections and contracting motions are separate conditions. This lane owns the unrestricted extremal-map/mesh reduction, not a replay of the axial sufficient criterion. |
| 5 | Direct analytic/optimal-transport comparison; [eight-lane analytic interface](../gaussian_majorisation_global_criterion/INTERFACES.md) | The axial motion is a sufficient zero-defect mechanism. A zero-failure coupling of smoothed density values need not arise from a motion of centers. The all-law fixed-atom and common-set obligations remain broader. |
| 6 | Geometric structure and internal-energy formulations | Maintain the axial support-cost proof, its Gaussian/ball transfers, nonlinear reserve, scope comparisons and review evidence. Keep the existing matrix extension as a secondary review module. Further sufficient subclasses are deferred. |
| 7 | Actual counterexample search | A candidate inside a quoted positive domain is a direct consistency test of that author proof and the proposed certificate. Preserve its exact data and sign evidence; do not dismiss a rigorous objection merely because a benchmark was intended to be positive. Failed motion or other method certificates are not negative Gaussian hinges. |
| 8 | Functional inequalities, ordered orbits and stability; [functional handoff](../gaussian_majorisation_open_stability/HANDOFF.md), [finite-certificate interface](../gaussian_majorisation_open_stability/CERTIFICATE_INTERFACE.md) | R's domain-wide reserve is uniform in laws, variances and radii. The finite certificate consumes rigorous signed margins at one variance. The ordered-ray theorem's unequal-radius union result remains complementary to the axial arbitrary-radius union and intersection conclusions. |

This is an interface record, not a new reassignment. Earlier reports
parking the finite-geometry campaign predate the human authorization of
the all-eight Gaussian handoff. The unrelated completed results remain
preserved.

## 2. The boundary with researcher 4

For fixed finite source sites X=(x_i), the feasible image tuples satisfy

    |y_i-y_j| <= |x_i-x_j|  for every pair.

After fixing one image vertex, this is a compact convex Lipschitz ball.
An extreme point refers to this convex set. A tight edge has equality
in its corresponding distance constraint. The classical connected-tight-
graph characterization is [Bredies--Chirinos Rodriguez--Naldi,
Theorem 2.2](https://link.springer.com/article/10.1007/s00013-024-01978-y).
It does not identify a Gaussian hinge optimizer by a Jensen argument.

Researcher 4's source instead preserves a hypothetical strict failure
while **enlarging the source support** to vertices of a tetrahedral mesh.
Its piecewise-isometric map is globally 1-Lipschitz on a convex polytope;
the tight framework is infinitesimally rigid, and the anchored finite map
is extreme. The geometric extension is classical
[Brehm](https://link.springer.com/article/10.1007/BF01917587), with the
all-dimensional statement also recorded in
[Petrunin--Yashinski, final remarks](https://arxiv.org/pdf/1405.6606).
The mesh reduction is an author proof awaiting review. It supplies no
uniform mesh size, fold-depth bound or Gaussian comparison for every mesh.

The distinctions that must survive the handoff are:

| Object or proposed step | What it guarantees | What still needs proof |
| --- | --- | --- |
| A path inside the fixed-source Lipschitz ball | Each time-slice is a contraction relative to the original source distances. | Distances between moving labels need not decrease as time advances. Even u -> -u by linear interpolation stays within the original norm bound while its norm decreases and then increases. Such a feasible path is not the continuous contraction used by Aishwarya--Li. |
| Compatible tetrahedral reflection choices | The cellwise isometries agree where cells meet and define a continuous piecewise-isometric map on the convex source polytope. | They do not constitute a sequence of global one-sided hyperplane folds, each contracting all current label pairs. The tree choices describe the endpoint map, not such a factorization. |
| A center motion in R4 or R5 | With the quoted geometric hypotheses, the established density-value argument gives every Gaussian hinge. Suitable finite time regularity also gives both arbitrary-radius ball inequalities. | Neither extremality nor infinitesimal rigidity alone supplies this motion. Researcher 4's classical simplex-flap control has both properties and has no R5 motion. |
| R's nonlinear endpoint deformation | The explicit error reserve yields two contracting segments around an already proved motion, in the same ambient dimension. | It is not a procedure for saturating an arbitrary Lipschitz map, choosing an extremal optimizer or preserving an unknown hinge sign through arbitrary feasible deformations. |
| Extension from finite labels to a mesh | The mesh map agrees with the original map on those labels. Restricting a hypothetical motion or strong-fold chain back to the labels is valid. | Adding new vertices with positive mass changes the law. Positivity for every law on the original axial domain does not automatically prove positivity for arbitrary laws on a mesh filling its convex hull. |

In particular, the axial [finite strong-composition obstruction](COMPOSITIONS.md)
does not contradict Brehm extension. If a mesh extension of the original
25 labels factored into global strong contractions in R3, restriction
would give the prohibited factorization of those labels. Thus cellwise
reflection data cannot be read as that global contracting-fold chain.
This is a consequence of the existing obstruction, not an objection to
the compatible-cell construction.

Likewise, the axial domain C(P) union (-C(Q)) is generally nonconvex.
A tetrahedral extension on the convex hull of finitely many of its points
need not be covered by the original cone-domain theorem. A new positive
claim on the additional vertices must provide a motion on those vertices
or another all-hinge proof. The geometric lane has not supplied a theorem
that all compatible tetrahedral maps obey the desired comparison.

The later [lift regularity audit](LIFT_BOUNDARY.md) adds a precise caution
for prescribed Gram deformations. Even AC relative Gram data with strictly
subcritical support cost can force every geometric lift of that curve to
have infinite variation, including in moving frames. This uses the existing
25-label positive benchmark, whose endpoints admit a different analytic
R4 motion. It obstructs an automatic regularity upgrade of the curve;
it neither obstructs arbitrary endpoint deformations nor changes the mesh
reduction. The [regularity completion](REGULARITY.md) replaces the curve
and controls squared distances instead of differentiating its square root.

The newer disjoint-cap results also have a precise interface with the
benchmark. [CAP_COMPARISON.md](CAP_COMPARISON.md) proves an equality lemma:
a disjoint-cap map preserving every distance of a cloud acts on that
cloud as the identity or one global hyperplane reflection. On two rigid
spanning clouds the branch difference therefore has rank at most two.
The original central flip has rank-three difference, including after
independent rigid changes of source and target frames. No single cap map
of any finite cap count can represent those 25 labels. This is a comparison
with the [three-cap source](../gaussian_disjoint_cap_reflections/PROOF.md)
and [new auxiliary certificates](../gaussian_cap_auxiliary_certificates/PROOF.md),
not a new positive class or a result about arbitrary cap-map compositions.
The latter remain outside this geometric benchmark claim.

## 3. Two existing benchmarks distinguish extremality from rigidity

These are structural descriptions of existing fixtures, not new positive
families. Use the original sites and direction order from
[EXPECTED.json](EXPECTED.json) and PROOF Section 5:

    X=(0,A,-B), Y=(0,A,B),
    A={(3d/4,1):d in D12}, B={(4d/5,1):d in D12}.

Keep all 25 labels. The 144 cross pairs are strict and the remaining 156
pairs preserve distance. Both clouds, when joined to the anchor, span R3.

**Undamped benchmark.** The map X -> Y is extreme in its anchored finite
Lipschitz ball. A short direct proof avoids any new extremality theorem:
every anchor distance is tight, so |Y_i|=|X_i|. If Y is the midpoint of
two feasible anchored tuples, strict convexity of each Euclidean anchor
ball forces equality of their i-th vectors for every i. The tuples
therefore coincide. Equivalently, the tight graph is connected.

Nevertheless its tight framework is **not infinitesimally rigid**. The
graph is two complete graphs K13 meeting only at the anchor. On each
full-dimensional complete cloud, an infinitesimal flex is a rigid velocity
field. The two fields share the anchor velocity, but their skew-symmetric
rotation matrices may be chosen independently. This gives exactly nine
degrees of freedom: three common translations and two independent
three-dimensional rotations. Thus, at either endpoint,

    rank of the ordinary 3D tight-edge rigidity matrix = 3*25-9 = 66,
    whereas full infinitesimal rigidity would have rank 3*25-6 = 69.

After fixing the anchor, six rotational degrees of freedom remain. This
does not supply an R3 contracting motion; the existing orientation argument
rules that out, and A supplies an R4 motion. The benchmark is therefore a
positive **extreme but infinitesimally flexible** map. A full mesh extension
can add tight constraints and achieve researcher 4's rigid framework; the
properties of the enlarged law still need their separate analysis.

**Damped neighborhood.** Every member of the already proved R2 neighborhood
has Lipschitz constant at most 194/199<1. Hence every pair of distinct
source labels has strict distance slack, including after anchoring the
image tuple by translation. A sufficiently small positive and negative
change to one non-anchor image vertex remains feasible, giving a nontrivial
midpoint decomposition. Such a map is not extreme on its fixed finite
source set. Its tight graph has no edges.

Yet the whole R2 neighborhood has the uniform Gaussian and ball conclusions
and requires four-dimensional motion. Thus extremality is neither a
necessary condition for this known positivity nor a replacement for its
motion proof. Researcher 4's extreme-map reduction is consistent with this:
it changes the support of a hypothetical failure, rather than claiming that
every positive finite contraction is already extreme.

The rank count above is a direct complete-graph rigidity argument. A
supplementary exact author check of the existing rational sites gives
156 tight pairs and ranks (66,66); it is not independent mathematical
review or a new general rigidity theorem. The original five checkers and
their expected outputs are unchanged.

The structural counts can be replayed from this directory using the
existing rational rank helper:

```sh
python3 - <<'PY'
import json
from itertools import combinations
from verify import F, dist2, rank
f = json.load(open('EXPECTED.json'))['fixture']
D = [tuple(map(F, d)) for d in f['directions']]
A = [(F(f['p'])*a, F(f['p'])*b, F(1)) for a, b in D]
B = [(F(f['q'])*a, F(f['q'])*b, F(1)) for a, b in D]
X = [(F(0),)*3] + A + [tuple(-c for c in b) for b in B]
Y = [(F(0),)*3] + A + B
E = [(i,j) for i,j in combinations(range(25),2)
     if dist2(X[i],X[j]) == dist2(Y[i],Y[j])]
def rigidity_rank(P):
    rows = []
    for i,j in E:
        row = [F(0)]*75
        for k in range(3):
            row[3*i+k] = P[i][k]-P[j][k]
            row[3*j+k] = -row[3*i+k]
        rows.append(row)
    return rank(rows)
print(len(E), rigidity_rank(X), rigidity_rank(Y))
PY
```

Expected: `156 66 66`. This calculation supports the written count; it
does not test extremality, a Gaussian hinge or the mesh reduction.

## 4. The two different roles of auxiliary mass

Researcher 4's reduction controls a strict negative gap by

    |D_new((1-epsilon)h) - (1-epsilon)D_old(h)| <= epsilon,
    D = H_target - H_source.

Thus D_old(h)=-delta survives whenever epsilon<delta/(1+delta). This is
an error budget at the selected witness variance and threshold. It does
not imply that exact all-threshold nonnegativity survives every positive
addition of mesh mass to an already positive law. A zero or arbitrarily
small positive gap can be outweighed by the error bound.

The latest [analytic interface, Section 3](../gaussian_majorisation_global_criterion/INTERFACES.md)
also shows how to keep a prescribed dominant atom: add mesh mass only
inside the rare law. With rare mass epsilon and added fraction eta,
the same-threshold hinge gap changes by at most 2 epsilon eta. This
retains a strict failure with a sufficient margin and keeps the atom's
mass exactly fixed. It remains a witness-level error estimate, not an
all-threshold positive closure. The separate uniform-mass normalization
is not imposed simultaneously with that fixed-atom requirement.

The same distinction connects the measure-side lane. On any compact
K inside A's domain or R's distorted domain, the all-law conclusion
supplies the premise of the [common-set equivalence](../gaussian_prior_localization/PROOF.md):
for every set E of finite positive volume, there exists a target set of
the same volume whose Gaussian masses compare simultaneously at every
x in K. This is an application of that source's equivalence, not a new
explicit construction of the set. Its optimizer may be diffuse. The
source's exact-optimizer obstruction does not conflict with finite
approximation of a strict failure or researcher 4's mesh enlargement.

Researcher 3's subsequent [uniform defect localization, Theorem 1](../gaussian_prior_localization/DEFECT_LOCALIZATION.md)
makes that approximation independent of the original support extent.
A violation of size delta>0 has, for every integer k>=8/delta, a
variance-one witness with at most k^6 atoms, both supports in B(0,2k),
and gap at least delta/2. The source gives a compact finite frontier D_k
with 0<=D-D_k<4/k, where D is the unrestricted supremum of the hinge
defect. These are author bounds awaiting independent review, and do not
establish any nontrivial D_k sign. They also do not imply a fixed finite
test that resolves D=0.

This localization conditions on a source cube and rescales its threshold;
it need not preserve a previously specified dominant atom. Conversely,
researcher 5's rare-law mesh augmentation preserves that atom but does
not supply the localization's support bound. If researcher 4 next enlarges
a localized witness to a rigid mesh, the k^6 bound counts the original
witness sites only: no bound for the added vertices has been proved.
Keep these quantifiers separate when composing the reductions. None
changes the axial domain or extends its positive comparison to the mesh.

Researcher 8's [finite-certificate interface](../gaussian_majorisation_open_stability/CERTIFICATE_INTERFACE.md)
likewise separates the localization index k from its moment degree N.
Its equivalence has the form "for every strict rational finite instance,
there exists a finite certificate"; it gives no uniform degree on D_k's
compact parameter set, which includes equality and zero-weight cases.
All-pair strictness in that interface and tight edges in the rigid-mesh
reduction are different test-class hypotheses. The axial benchmark can
check proposed certificate inputs, but its known positive sign does not
supply a missing signed endpoint or a numerical enclosure.

R also does not permit arbitrary splitting clouds under its whole-domain
statement. It needs a single source map S=Id+e with Lip(e)<1 and a
single target error map on T(D). The finite freely perturbed R2 theorem
uses separated reference sites to obtain these maps on its 25 labels.
Removing that condition requires a different result, such as the
law-dependent stability theorem with its own variance restrictions.

## 5. What to preserve when importing a benchmark

The [review portfolio](REVIEW_GUIDE.md) and [source ledger](PORTFOLIO.json)
remain the authoritative claim inventory. An imported calculation should
identify its labels, law, variance, threshold and geometric module:

| Tag | Positive hypothesis and expected scope | Essential qualification |
| --- | --- | --- |
| A | Original axial reflection; per W<=4; arbitrary bounded laws, weights and variances; arbitrary finite radii, both unions and intersections. The original circular range is pq<=2/pi. | The perimeter necessity concerns its stated axial form only. The original fixture has p=3/4,q=4/5 and includes the anchor. |
| R2 | Every endpoint error <=1/2000 about (X,(19/20)Y), with all 50 endpoint positions free. All weights, variances, hinges and individual radii are allowed. | The reference target is scaled. The finite strong-chain exclusion does not extend to this neighborhood. |
| M | Existing undamped matrix extension; an operator-norm boundary path with support cost <=2 gives an R5 motion. [REGULARITY.md](REGULARITY.md) gives both arbitrary-radius ball conclusions under the same AC path hypothesis, including after the existing nonlinear reserve. | The matrix fixture has p=4/5,q=81/100. Restricted optimality is only for block-diagonal relative Gram motions. The regularity completion uses vanishing target scaling; an exact smooth motion at the undamped endpoint is not claimed. |

Use isotropic covariance s I_3 and retain the prescribed labels. Target
collisions must retain and then combine their probability masses correctly;
R's target error must respect them. A paired-rank computation, a rigidity
rank, a pointwise orbit hinge or a failed PDE coefficient inequality is
not itself an integrated Gaussian hinge. Any claimed negative comparison
must specify the actual normalized law and rigorous sign certificate.

No general containment between this packet and the extremal-mesh test
class is asserted. The common-set, extremal-map, global-moment and PDE
formulations each retain their unresolved sign or evolution obligations.

## 6. Durable sources and review disposition

The axial review checkpoint is source commit
`e8fea4c40319da833258d926c4737198b133e670`; its mathematical baseline and
all proof/checker hashes are in PORTFOLIO. The new incoming source versions
inspected for this handoff are:

| Artifact | Source commit containing the inspected source | Role here |
| --- | --- | --- |
| [Heat profiles](../gaussian_majorisation_heat_profiles/PROOF.md) | `007ec4fddd5566a57106a7b0464b34fa8d7ad8f2` | PDE-lane context; no positive premise of A/R. |
| [Finite orthogonal averaging](../gaussian_majorisation_finite_orbit_obstruction/PROOF.md) | `5e686ec7c361a368e562496c23e06dc4706ba281` | Finite-certificate method boundary; no negative integrated hinge. |
| [Common-set and prior localization](../gaussian_prior_localization/PROOF.md) | `541d4b7de3d73b41444e5350378a8ecc43d914ea` | All-law equivalence and exact-optimizer qualification. |
| [Uniform defect localization](../gaussian_prior_localization/DEFECT_LOCALIZATION.md) | `4ed178725774e2fd3bb486f952825f58e52766cc` | Defect-dependent finite witness bounds; neither a rigid-mesh size bound nor a fixed-atom-preserving step. |
| [Extremal maps and rigid meshes](../gaussian_majorisation_extremal_maps/PROOF.md) | `c68eb50ea52c9b578e90e89b5954ea4c63a0d89a` | Researcher 4 interface; support enlargement and strict-failure transfer. |
| [Analytic eight-lane interface](../gaussian_majorisation_global_criterion/INTERFACES.md) | `68380d9e533f2acf259d2fcecebfc48735e92bb4` | Prescribed-atom preservation through mesh enlargement; a strict-witness error budget. |
| [Finite-certificate interface](../gaussian_majorisation_open_stability/CERTIFICATE_INTERFACE.md) | `9a1047c925763125c72fa862e9200c40717b9c25` | Fixed-variance signed certificate obligations; no uniform moment degree on the localized compact frontier. |

The primary problem source remains
[Aishwarya--Li arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2),
revised 13 September 2026 and refreshed for this pass. The classical
extremality statement and Brehm extension were checked in the primary
sources cited above. This handoff is not independent acceptance of the
mesh reduction, the axial proofs or a historical-priority claim.

No original core proof, checker or old certificate has changed. The existing
reproduction commands stay in [README.md](README.md). Review should first
address the frozen portfolio's concrete correctness and priority questions.
An unrestricted deformation or extremal-map development belongs with
researcher 4's lane; a repair to the axial motion, its pressure/hinge transfer
or its quantitative reserve belongs here. Any later common result should
cite both inputs at their actual scope rather than replace one missing
sign argument with the other's conclusion.
