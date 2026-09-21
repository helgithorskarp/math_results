# Sharp order bounds and a tree classification for remote resolvers

All graphs below are finite, simple, undirected, and connected.  Fix a
vertex `p` of a graph `G`.  For a vertex `q != p`, let

\[
D_G(p,q)=\{u\in N_G(p):d_G(u,q)=d_G(p,q)-1\}
\]

be the full set of first directions of shortest `p`--`q` paths.  Put

\[
R_p=\{p\}\cup(V(G)\setminus N_G[p]),\qquad
F_p(p)=N_G(p),\qquad F_p(q)=D_G(p,q)\quad(q\in R_p\setminus\{p\}).
\]

Following the remote-signature criterion, call `p` a **remote resolver** when
`F_p` is injective on `R_p`.

## Theorem 1 (sharp degree--order bound)

If `p` is a remote resolver of degree `d`, then

\[
|V(G)|\le 2^d+d-1. \tag{1}
\]

Equality holds if and only if the map

\[
q\longmapsto D_G(p,q)
\]

is a bijection from `V(G) minus N_G[p]` onto the nonempty proper subsets of
`N_G(p)`.

The bound is sharp for every `d >= 1`.  For `d=1`, equality is attained by
`K_2`.  For `d>=2`, equality is attained by a bipartite graph `B_d` of
diameter four: take

* one root `p`;
* vertices `u_1,...,u_d`; and
* one vertex `x_S` for each nonempty proper subset `S` of `{1,...,d}`,

and add precisely the edges `p u_i` and `u_i x_S` with `i in S`.

### Proof

Every remote vertex `q` has at least one first direction, so `D_G(p,q)` is a
nonempty subset of `N_G(p)`.  It cannot be all of `N_G(p)`, because that would
give `F_p(q)=F_p(p)`.  Distinct remote vertices have distinct direction sets.
There are exactly `2^d-2` nonempty proper subsets of a `d`-set.  Since the
remaining vertices are `p` and its `d` neighbors,

\[
|V(G)|=1+d+|V(G)\setminus N_G[p]|
       \le 1+d+(2^d-2),
\]

which is (1).  Equality in this count is equivalent to using every available
signature exactly once, proving the stated equality criterion.

For `d=1`, `K_2` has no remote vertices and its one-element remote domain is
resolved.  Now let `d>=2` and consider `B_d`.  It is connected and bipartite,
the root has degree `d`, and every `x_S` is at distance two from `p`.  Its
neighbors among `u_1,...,u_d` are exactly those indexed by `S`; hence
`D_{B_d}(p,x_S)={u_i:i in S}`.  These sets are distinct, nonempty, and proper,
while `F_p(p)={u_1,...,u_d}`.  Thus `p` is a remote resolver and equality
holds.  Two vertices `x_{\{i\}}` and `x_{\{j\}}` with `i != j` are at distance
four, while every pair of vertices is at distance at most four, so `B_d` has
diameter four.  QED

## Theorem 2 (complete tree classification)

Let `T` be a tree of order at least two and let `p` have degree `d`.

* If `d=1`, then `p` is a remote resolver if and only if `T=K_2`.
* If `d>=2`, then `p` is a remote resolver if and only if `T` is obtained
  from the star `K_{1,d}`, centered at `p`, by subdividing an arbitrary subset
  of its edges exactly once.

Consequently a tree with a degree-`d` remote resolver has order at most

\[
2d+1\qquad(d\ge2), \tag{2}
\]

and equality holds exactly when every edge of the centered star is subdivided
once.  For `d>=2`, up to rooted isomorphism, the trees with a degree-`d`
remote resolver are the `d+1` spiders having `s` legs of length two and `d-s`
legs of length one, where `0<=s<=d`.

### Proof

In a tree the `p`--`q` path is unique.  Hence every remote vertex in the
component of `T-p` containing a neighbor `u` of `p` has the same signature
`{u}`.  Injectivity therefore permits at most one vertex beyond `u` in that
component.

If `d=1` and a remote vertex exists, its signature is the singleton `N_T(p)`,
which collides with `F_p(p)`.  Thus no remote vertex exists and connectedness
forces `T=K_2`; the converse is immediate.

Suppose `d>=2`.  The root signature has size at least two, so it cannot collide
with any singleton remote signature.  Pairwise injectivity of the remote
signatures is therefore equivalent to each component of `T-p` containing at
most one vertex besides its neighbor of `p`.  Such a component is either one
vertex or one edge.  Equivalently, every arm of the star centered at `p` has
length one or two.  This proves both directions of the classification.

There are `d` first-level vertices and at most one additional vertex on each
arm, giving (2).  Equality means that every arm has length two.  Permuting the
arms shows that the rooted isomorphism type is determined exactly by the
number `s` of subdivided arms.  QED

## Corollary 3 (sharp information capacity for one-probe blow-ups)

Let every quotient vertex `v` be replaced by an independent module `M_v` of
arbitrary size `m_v>=2`.  If the quotient has a remote resolver `p`, then its
independent substitution has full-feedback directional localization number
one.  In particular this applies to every classified tree above and to every
extremal graph `B_d`, whose quotient has `2^d+d-1` vertices.

### Proof

Probe a clone in `M_p`.  A target in an adjacent module returns its own clone
as a singleton.  A different clone in `M_p` returns the union of the modules
indexed by `N_G(p)`, and a target in a remote module `M_q` returns the union of
the modules indexed by `D_G(p,q)`.  Module disjointness and the remote-resolver
property therefore identify the robber's module (or locate the robber
immediately).  The assumption `m_v>=2` prevents a union response from being
an adjacent-target singleton.

After the robber moves, probe the clones of the identified independent module
one at a time.  A robber who leaves gives his own vertex as a singleton; on
the only continuing response, a scanned clone cannot be re-entered from
another clone of the same independent module.  The scan terminates after at
most the module size.  Thus one probe per round wins.  QED

Theorem 1 is an information-capacity statement: the empty direction set is
impossible for a remote target and the full set is reserved by the root, so
only `2^d-2` remote module labels are available.  The graphs `B_d` realize
every available label simultaneously, even under bipartiteness and diameter
four.  Theorem 2 shows that unique-path geometry collapses this exponential
capacity to the linear sharp bound `2d+1` and determines every equality case.
