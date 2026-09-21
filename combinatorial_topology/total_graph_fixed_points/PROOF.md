# Fixed-point spaces of total-graph clique complexes

## Statement and scope

Let G be a finite simple graph, let Gamma be a group of automorphisms of
G, and write

    A = |Cl(G)|,       X = |Cl(T(G))|.

The total graph T(G) has vertex set V(G) disjoint-union E(G).
Its adjacencies are original adjacency on V(G), common-endpoint
adjacency on E(G), and incidence between V(G) and E(G).
Cl denotes the simplicial complex of all cliques, and vertical bars
mean geometric realization. Gamma acts on both spaces. Its image is
finite; one can equivalently take Gamma <= Aut(G).

For each triangle tau of G, let b_tau be its barycenter in A. Let

    W_tau = { (x_v) in R^tau : sum_v x_v=0 },

with the triangle stabilizer acting by permuting coordinates, and let
S^(W_tau) be its one-point compactification. This is a 2-sphere with
its indicated action and a fixed basepoint at infinity. Form Y from A
by attaching one such sphere at b_tau for every triangle tau. Gamma
permutes the spheres and their coordinates in the evident way.

**Equivariant theorem.** There is a Gamma-equivariant homotopy equivalence

    X ~=_Gamma Y

whose restriction to A is the identity; the homotopies can also be
taken relative to A. No freeness, connectedness, or absence of simplex
inversions is assumed.

For a subgroup H <= Gamma, let o_H(tau) be the number of H-orbits on the
vertices of a setwise H-invariant triangle tau. Then

    X^H ~= A^H with one S^(o_H(tau)-1) attached at b_tau
           for each H-invariant triangle tau.                  (FP)

This describes genuine fixed-point spaces of geometric realizations,
not the subcomplex on individually fixed vertices, not an orbit quotient,
and not the invariant part of homology.

Thus a pointwise fixed triangle contributes S^2; an orbit split 2+1
contributes S^1; a transitive triangle contributes S^0. In the last case,
one point is glued to b_tau and the other is a new isolated component.
Triangles permuted nontrivially as a set contribute no new fixed points.
If A^H is empty, there are no H-invariant triangles and X^H is empty.

Adamaszek's Theorem 5.1 already proves the ordinary decomposition

    |Cl(T(G))| ~= |Cl(G)| with one S^2 for each triangle.

The present target is the symmetry-compatible refinement and its fixed
spaces. The ordinary decomposition and its face classification are
explicitly credited to that work; see REFERENCES.md.

## 1. The core and its face classification

Use the same underlying core as in Adamaszek's proof. Delete from Cl(T(G))
the open edge-only 2-simplex

    sigma_tau = { e : e is an edge of tau }

for every original triangle tau, retaining its boundary. These simplices
are maximal, so the remaining complex K is a subcomplex.

For each original edge e=uv set

    P_e = {u,v,e},

and for each original vertex v let S_v be the simplex on

    {v} union {e : e is incident with v}.

Then, writing simplices also for their realizations,

    |K| = A union (union_e P_e) union (union_v S_v).     (1)

For completeness, a clique with at least three original vertices has no
edge-vertex incident with all of them, and is an original clique. A clique
with exactly two original vertices u,v has at most the edge-vertex uv.
With one original vertex v all its edge-vertices are incident with v.
Finally, pairwise incident distinct edges either have a common endpoint
or are precisely the three edges of a triangle. This proves (1) and the
claimed maximality.

Different S_v meet at most in the vertex representing their common
edge. S_v meets P_e in {v,e} when v is an endpoint of e, and otherwise
not at all. Its intersection with A is {v}. These intersections make
the following explicit maps compatible.

## 2. A deformation commuting with every graph automorphism

A point of S_v has weights t_e>=0 on its incident edge-vertices, with
sum_e t_e<=1, and the remaining weight at v. Let m be the second largest
of the t_e, taking m=0 if there are fewer than two entries. Set

    R_v(t)_e = max(t_e-m,0),

and put the remaining mass at v. Interpolate the coordinates linearly
from t to R_v(t).

The second order statistic is continuous. The formula is unchanged by
any permutation of the incident edges. All new weights are nonnegative
and have sum at most one. At the endpoint at most one edge-coordinate
is positive, so the image is the star tree consisting of the segments
[v,e]. If the point already lies on that tree, m=0 and the point is
fixed throughout the homotopy.

Keep A and every P_e fixed during this stage. All their intersections
with the S_v lie in the fixed star trees, as do intersections between
different S_v. Thus the formulas glue to a strong deformation retraction

    |K| -> K0 := A union (union_e P_e)

commuting with all graph automorphisms, including endpoint swaps.

For the second stage, on P_e with e=uv replace the weight t_e by t_e/2
at u and t_e/2 at v. More explicitly, at time s use

    t_e(s)=(1-s)t_e,
    t_u(s)=t_u+s*t_e/2,
    t_v(s)=t_v+s*t_e/2.

This fixes the original edge [u,v]. Distinct P_e intersect only in
original vertices or are the same simplex, so these maps glue while
fixing A. They commute with exchanging u and v. The result is an
explicit Gamma-equivariant strong deformation retraction

    r: |K| -> A.                                       (2)

In particular it is not necessary to choose an endpoint of an edge,
an ordering of the vertices, or a preferred graph vertex. Those
choices would need separate justification in an equivariant argument.

## 3. Equivariant trivialization of the remaining attaching maps

Consider one deleted triangle sigma_tau, whose vertices are the three
edge-vertices of tau. Its boundary is contained in K. A boundary edge
joining e=uv to f=vw lies in S_v. Stage 1 sends that edge through v
along [e,v] union [v,f]; stage 2 sends e and f to the midpoints of the
original edges e and f. Thus

    r(boundary sigma_tau) is contained in |tau| subset A.   (3)

Straight-line interpolation inside |tau| contracts this attaching map
to b_tau. It commutes with the entire stabilizer Gamma_tau. The same
formulas for all tau are compatible with the action of Gamma.

We spell out the attachment principle used here. For a finite group
acting on a family of simplicial disks and on a base space, attaching
along two equivariantly homotopic boundary maps produces equivariantly
homotopy-equivalent spaces relative to the base. To see this, insert a
boundary collar and put the homotopy on the collar. A simplex has an
invariant radial collar about its barycenter, so the usual collar
proof commutes with its stabilizer and with permutations of the disks.
Likewise an equivariant deformation of the base can be applied to all
attaching maps without changing the equivariant homotopy type. One may
express both operations as homotopy invariance of the pushout along
the disk-boundary inclusions. These are equivariant cofibrations;
barycentric subdivision also gives ordinary finite equivariant CW
models if required.

Apply this first to (2), and then to the contractions in (3). We obtain
a model consisting of A with

    |sigma_tau| / |boundary sigma_tau|

attached at b_tau for each tau, all compatibly with Gamma. The interior
of sigma_tau is equivariantly homeomorphic to the reduced permutation
representation on its three edge labels. For example, logarithmic
barycentric coordinates t_i -> log(t_i)-(sum_j log(t_j))/3 give such
a homeomorphism. It extends to the one-point compactification after
collapsing the boundary. Identifying an edge of tau with its opposite
vertex identifies this representation with W_tau. This proves the
equivariant theorem, relative to A.

No assertion that a global wedge basepoint can be chosen equivariantly
is needed: each sphere is attached at its own triangle barycenter.

## 4. Fixed spaces and asphericity

An equivariant homotopy equivalence restricts to a homotopy equivalence
on H-fixed spaces for every subgroup H, since the maps and homotopies
restrict.

A point of Y outside A belongs to exactly one triangle sphere. For it
to be H-fixed, its triangle must be H-invariant. In such a sphere the
fixed points form the one-point compactification of W_tau^H. Coordinates
of an H-fixed vector are constant on each vertex orbit, with one weighted
sum-zero constraint, so

    dim W_tau^H = o_H(tau)-1.

This proves (FP), including the S^0 interpretation and the empty case.

Let m_j(H) count the H-invariant triangles having j vertex orbits. For
any field F and nonempty A^H, the ordinary Betti numbers satisfy

    beta_0(X^H;F)=beta_0(A^H;F)+m_1(H),
    beta_1(X^H;F)=beta_1(A^H;F)+m_2(H),
    beta_2(X^H;F)=beta_2(A^H;F)+m_3(H),
    beta_i(X^H;F)=beta_i(A^H;F) for i>=3.               (4)

The stronger homotopy statement, not merely these equalities, implies:

**Asphericity criterion.** Every component of X^H is aspherical if and
only if every component of A^H is aspherical and H fixes no triangle
pointwise.

Indeed, an attached S^2 is a retract and has nonzero pi_2. Wedges with
circles preserve asphericity of connected CW complexes: their universal
covers are trees of copies of the original universal covers. Isolated
points are harmless. Conversely each old component is a retract, so
its higher homotopy injects. The criterion also holds vacuously for
empty fixed spaces.

For K3, A is a triangle. The fixed space X^H is a 2-sphere for trivial H,
a circle for a transposition, and two points for a 3-cycle or S3. These
are already enough to refute a replacement in which an invariant
triangle always contributes a trivially acted-on 2-sphere.

This result describes a class of fixed spaces; it does not resolve
Whitehead's general subcomplex conjecture or the Eilenberg--Ganea problem.

## 5. Integral homology and signs

There is also a concrete integral Gamma-module splitting

    H_2(X;Z) = H_2(A;Z) direct-sum Z[oriented triangles of G],   (5)

where reversing the orientation of a triangle negates its generator.
For i!=2, the inclusion A->X induces a Gamma-module isomorphism on
H_i with integral coefficients.

Here is an explicit splitting, avoiding a noncanonical appeal to the
ordinary wedge. Orient tau as (v0,v1,v2), and let e_i be its edge opposite
v_i. The induced complex on these six vertices is the boundary of an
octahedron: its three missing pairs are (v_i,e_i). For
epsilon in {0,1}^3, put w_i=v_i if epsilon_i=0 and w_i=e_i otherwise.
Define the integral 2-cycle

    c_tau = sum_epsilon (-1)^(3-|epsilon|) [w0,w1,w2].  (6)

Every boundary edge cancels between its two completions. The coefficient
on [e0,e1,e2] is +1; other triangles' cycles have coefficient zero on
that edge-only face. The relative chain complex C_*(X,K) is concentrated
in degree two and freely generated by these oriented edge-only faces.
The cycles c_tau show that H_2(X)->H_2(X,K) is onto and split it.
The long exact sequence of the pair, together with (2), proves (5)
and the other isomorphisms.

Permuting the three opposite pairs in the octahedron changes (6) by the
sign of that permutation. The opposite-edge identification gives the
same permutation as on the original triangle. Consequently (5) is
Gamma-equivariant over Z, including when the characteristic divides
the group order after change of coefficients.

In particular, for any g in Gamma,

    trace(g | H_2(X;Q)) - trace(g | H_2(A;Q))
      = sum_(g tau=tau) sign(g restricted to tau).       (7)

This signed summand is essential. The main theorem contains more
information than this character formula: it determines all subgroup
fixed spaces and their component attachments.

## 6. Direct finite corroboration

The verifier constructs G, T(G), their clique complexes, and their
geometric fixed spaces directly. For a permutation group H acting on
a flag complex, a fixed point has constant barycentric coordinates on
each vertex orbit. Such an orbit can occur in its support only if it
is a clique. A collection of these orbits is a face exactly when their
union is a clique. The resulting orbit-support complex is therefore
homeomorphic to the genuine fixed space.

This is not the usual orbit quotient complex. Nonclique vertex orbits
are excluded. The map sends a barycentric mass for an orbit to equal
shares at the vertices in that orbit; its inverse sums each orbit's
coordinates. This proves both directions of the fixed-space encoding.

The checker computes boundary-matrix ranks over F_2 and F_3 and compares
(4) on targeted actions. It also verifies (6) as integer chains, checks
the generator signs under the supplied group actions, and checks the
two-stage deformation formulas on rational barycentric controls.
Known torsion and empty-fixed-space fixtures guard against replacing
fixed spaces by invariant homology or checking only ordinary Betti
numbers.

These finite computations corroborate the universal proof. They do
not prove its quantifiers or certify integral homotopy type on their
own. The proof remains unformalized; the checks are a different
method used by the same researcher, not independent peer review.
