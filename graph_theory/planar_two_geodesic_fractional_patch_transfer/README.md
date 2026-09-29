# An exact fractional criterion for patch substitution

The [three-pair face-patch transfer](../planar_two_geodesic_face_patch_transfer/README.md)
uses a particular pairwise-disjointness pattern in a quotient. Here is an
**if and only if** criterion for any finite menu. It combines the team's
[mass-menu duality](../planar_two_geodesic_mass_menu_duality/README.md)
with an exact treatment of patches heavier than half the mass. A four-pair
octahedral example shows that the fractional criterion genuinely reaches
beyond a three-pair condition. These are structural positive results for
specified menus, not a resolution of
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

## Exact quotient criterion

Let `Q` be a finite connected graph with a partition `V(Q)=U disjoint Z`,
where `Z` is independent and `U` is nonempty. Think of `U` as the core and
each `z in Z` as an atom to be expanded into a patch. Let
`S_1,...,S_t`, `t>=1`, be subsets of `U`. For each `i`, let `R_i^*` be
the components of `Q-S_i` that meet `U`. An omitted component is necessarily
a singleton atom. For nonnegative quotient masses `mu`, put

    M = mu(V(Q)),       B = max_{z in Z} mu(z),

with `B=0` if `Z` is empty. The following are equivalent:

1. For every `mu`, some `S_i` leaves every component of `Q-S_i` with
   mass at most `max(M/2,B)`.
2. For every tuple `C_i in R_i^*`, there are nonnegative integers `a_i`
   with `A=sum_i a_i>0` such that

       2 sum_{i:v in C_i} a_i <= A           for every v in V(Q).     (D)

If some `R_i^*` is empty, condition 2 is vacuous and `S_i` always works.
Otherwise the integers can be chosen with support at most `|V(Q)|+1` and
`A <= b! 2^(b-1)`, where `b=min(t,|V(Q)|+1)`. A violating quotient mass,
when one exists, can be chosen positive and rational, hence integer after
scaling.

**Proof.** Fix a tuple of core-bearing components. The finite-menu
duality proof says that (D) fails exactly when some mass `mu` makes all
`C_i` strictly heavier than `M/2`. If no atom exceeds `M/2`, this mass
already makes all menu sets fail the proposed bound. If an atom `z`
exceeds `M/2`, then every `C_i` contains `z`: a set omitting `z` has mass
less than `M/2`. Because every `C_i` meets `U`, give `z` mass `1-epsilon`
and give each core vertex positive mass whose total is `epsilon`, where
`0<epsilon<1/2`; give the other atoms zero mass. Every `C_i` now has
mass strictly greater than `1-epsilon=max(M/2,B)`. Thus failure of (D)
always gives failure of condition 1. Conversely, if condition 1 fails,
choose for each `i` a residual component heavier than `max(M/2,B)`.
It cannot be a singleton atom, so it belongs to `R_i^*`. These components
are all heavier than half, contradicting (D) by the same duality theorem.
The integer bounds come directly from that theorem. Strict inequalities
can be preserved by rational perturbation and scaling. `QED`

The proof identifies a useful fact: the `B` exception does **not** weaken
the fractional test when every selected component contains a core vertex.
A heavy atom common to all such components can be kept heavy while a
small positive core mass pushes every component above that atom.

## Arbitrary patch expansion and heavy-patch repair

Replace each atom `z` by a finite nonempty connected patch `K_z`.
Retain the core graph. Every patch-to-core edge must project to a `z`-to-core
edge of `Q`, and there are no edges between distinct patches. All masses
are nonnegative. Assume the chosen `S_i` are unions of at most two paths
that remain shortest in the **whole expanded graph** `G`. If (D) holds for
every core-bearing tuple, at least one menu separator leaves every
component of `G-S_i` with mass at most

    max(M/2, max_z w(K_z)).                                      (1)

Indeed, collapse each patch mass onto its atom. Every expanded residual
component projects into one quotient residual component. Its mass is at
most that quotient component's mass. This remains true if a patch splits
after deleting core vertices. As a fixed-set combinatorial assertion, the
converse is exact across all expansions because singleton patches recover
`Q`. For a geodesic-menu assertion this converse applies when the
displayed core paths are already geodesic in `Q` with its chosen metric.

There is a half-balance corollary under a local width condition. Suppose
`G` is connected; each patch boundary `N_G(K_z)` is a clique in the core;
and each torso `G[K_z union N_G(K_z)]` has treewidth at most three. Then
for **every** vertex mass, `G` has a half-balanced separator made of at
most two ambient shortest paths. If no patch is heavier than half, (1)
works. Otherwise the unique heavy patch has mass greater than `M/2`.
The [reviewed heavy-torso reduction](../planar_two_geodesic_prescribed_attachment_review1/REVIEW.md)
applies: its boundary clique occurs in one bag of a width-three torso
decomposition. Attach there one bag containing all vertices outside the
patch. A weighted centroid cannot be this outside bag, since its patch
branch carries more than half the mass. A local centroid bag has at most
four vertices and half-balances `G`. Cover its vertices by at most two
shortest paths in `G`, pairing vertices arbitrarily. Deleting more
vertices only shrinks residual components. Notice that this repair uses
ambient geodesics and does not require the fixed menu paths to enter a
heavy patch.

The quotient criterion is necessary and sufficient for the quantitative
fixed-menu bound (1) across all patch expansions; the width-three
condition is only a sufficient repair for half balance. No converse for
the half-balance corollary is claimed.

## A four-pair planar application

Let the six core vertices be the two-element subsets of `{0,1,2,3}`;
join intersecting subsets. This is the planar octahedron `L(K_4)`.
Attach to each core vertex `v` a pendant atom `z_v` adjacent only to `v`.
For each label `i`, let `C_i` consist of the three core vertices containing
`i` and their three attached atoms. Let `S_i` be the three core vertices
outside `C_i`. As in the [four-menu gap](../planar_two_geodesic_four_menu_gap/README.md),
two core edges cover `S_i`. Give every core edge unit length (or any
length in `[lambda,2lambda)` for one `lambda>0`), and give pendant
edges arbitrary positive lengths. Each selected core edge is then an
ambient geodesic. Deleting `S_i` leaves `C_i` and three
singleton atoms. Every core vertex and every atom belongs to exactly
two of `C_0,...,C_3`; thus `a_0=...=a_3=1` satisfies (D) at equality.
For every mass on the quotient, one of these four fixed pairs satisfies
(1).

All four pairs are needed for this **prescribed menu**: for any three
labels `i,j,k`, put unit mass on the three core vertices `{i,j}`, `{i,k}`,
and `{j,k}`. Each of the three corresponding `C` sets has mass two out
of total three, while all atom masses vanish. This also shows why the
three-pair transfer condition cannot certify this menu.

Now replace each `z_v` by an arbitrary connected planar patch attached
only at `v`, with the patch-plus-root torso of treewidth at most three.
The graph remains planar and all four core paths remain ambient
geodesics under the stated core metric, since an excursion into a
pendant patch must return to `v`. The theorem gives half balance for
every real vertex mass and every choice of positive **patch** edge
lengths, with **unbounded patch orders**. For an
explicit family, take a stacked planar triangulation of arbitrary size
for each patch and join one of its vertices to its root `v` by one edge.
Its torso has width at most three. The resulting connected planar graphs
have the octahedron as a subgraph, which has minimum degree four and
therefore treewidth at least four. This class is not covered merely
by the global treewidth-three theorem. Pendant attachment is an
articulation construction; no 2-connectivity or full triangulation claim
is made.

## Exact finite audit and scope

Run from the repository root with Python 3.11+ and the standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_fractional_patch_transfer/verify.py
```

The checker independently constructs the 12-vertex octahedral quotient,
certifies its planar embedding by the eight octahedral triangular faces
and pendant placement, enumerates all ambient unit-edge geodesics and
their unordered pairs, recomputes the four residual partitions, checks
the fractional incidence identity and three-pair witnesses, and tests
all `3^12` mass vectors with entries in `{0,1,2}`. These controls audit
the example; the all-real-mass quotient theorem and the expansion theorem
follow from the written proofs, not the bounded mass enumeration.

Expected output:

```text
quotient: vertices=12 edges=18 core_faces=8
all_geodesics=114 all_pairs=6555 prescribed_pairs=4
ternary_mass_vectors=531441 three_pair_witnesses=4 PASS
```

Primary background: Diot and Gavoille,
[*Path Separability of Graphs*](https://emilie-diot.eu/Article/DG10a),
for the width-three centroid argument. No priority claim for the exact
quotient formulation is made. The official Barbados problem list states
the unrestricted question; a listed workshop disproof talk has not been
identified with an exact theorem applicable to this formulation.
