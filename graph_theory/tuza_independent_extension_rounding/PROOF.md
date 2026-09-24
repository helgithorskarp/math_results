# Linear triangle-packing loss under independent extensions

Complete author proof, awaiting independent mathematical review. All graphs
are finite and simple. The imported dense decomposition theorem is Peter
Keevash's Theorem 5.15; its complete specialization is restated in
[DENSE_COMPLETION.md](DENSE_COMPLETION.md). Edge coloring uses classical
Vizing/Kempe methods, with a proof included below. No absolute priority claim
or new general design or coloring theorem is made.

A mixed-template graph partitions its vertices into clique or independent
classes, with each cross pair completely joined or empty. Write nu for the
maximum number of edge-disjoint triangles, nu* for the full fractional
triangle-packing optimum, and tau for the minimum size of an edge set meeting
every triangle. Classes need not be maximal twin classes.

**Theorem 1 (independent-extension closure).** Fix integers d>=1,r>=0 and
0<alpha<=1. There is a finite K=K(d,r,alpha) such that the following holds for
every n>=1. Let H have n vertices in at most d mixed classes, each of size
at least alpha*n. Add an independent set split into at most r classes I_h.
Each I_h has an arbitrary size s_h>=0 and is complete or empty to every core
class. There are no edges between any two vertices of the added set. Then

    0 <= nu*(G)-nu(G) <= K(d,r,alpha)*n.                 (1)

The bound is in the CORE order n, even when the independent extension is
arbitrarily larger. There is no lower bound on any s_h or on positive
fractional-profile coordinates. The proof rounds any feasible fractional
packing with the same linear-loss guarantee. The constant K and its initial
large-core threshold remain existential, because of the dense design input.
Finite small core orders are included by enlarging K, not by asserting that
the asymptotic construction already works at those orders.

The comparable-core condition remains. Section 6.1 permits linearly many
edges within the exceptional set as a direct corollary. This is not an unrestricted
O_d(N) result for every bounded-type graph and does not resolve Tuza's
conjecture. Even complete cores already require linear error order by the
standard parity obstruction.

The proof first treats a small independent extension, preserving bounded
per-type degree discrepancy in its core-edge union. It then uses a finite
hierarchy of independent-class sizes. A separate exact multiplicity cap
preserves nu, nu* and tau and explains why unbounded s_h cause no difficulty.
If H is edgeless, G has no triangles and the main conclusion is immediate.

## 1. Near-regular degree lists avoiding a forbidden graph

First, a useful general sufficient condition is this: degree lists with
maximum U and matching bipartite sums or even internal sum, asking for m
edges, can be realized avoiding any degree-D forbidden graph if

    m > 3U(D+U+1).                                    (2)

The lists may contain zero entries. The maximum-edge augmentation proof
below establishes this condition directly, without balancedness.

As a consequence, use s>=1 and a forbidden graph of maximum degree D<=s.
Target degree lists have
entries in [0,s], are balanced on each side (max-min<=1), have matching
bipartite sums or even internal sum, and ask for m edges. Each side has
length at least L>=48(s+1), and m>=12(s+1). Then an allowed simple graph
with exactly the specified degrees exists.

Let U be the largest target degree. Balance gives U<=2m/L+1 in both cases.
Consequently

  3U(D+U+1) <= 3(2m/L+1)(2s+1) < 3m/4 < m.       (A)

Choose an allowed graph J of maximum edge count under target degree bounds.
Bipartite: if a is deficient on the left, every deficient right vertex is
among its at most D+U existing/forbidden neighbors. Thus total missing
right degree <=U(D+U), so |J|>=m-U(D+U). For deficient a,b, at most
2U(D+U+1) edges cd obstruct replacing cd by ad,cb. Condition (2) supplies
an augmenting edge. Internally, deficient vertices form a clique in J union
the forbidden graph, so there are at most D+U+1. Hence
|J|>=m-U(D+U+1)/2 >2U(D+U+1). Two deficient vertices allow cd->ac,bd outside
their neighborhoods; a single deficient vertex has even deficiency at least
two and allows cd->ac,ad. All additions are allowed/new. Contradiction.
Zeros cause no difficulty because the proof uses total missing degree.

## 2. Classical Delta+1 edge coloring

Use a palette of Delta+1 colors and extend a proper partial coloring one
edge uv at a time. Let alpha be a missing color at u. Form a chain fan
v_0=v,...,v_t at center u. Rotating it means shifting the color of uv_i to
uv_(i-1) for i=1,...,t, leaving uv_t uncolored. Choose beta missing at v_t;
if missing at u,
rotate the fan and use beta. Otherwise let w be the unique beta-neighbor
of u. Append w if new. If w=v_j is already in the fan, j>=1, then beta
is missing at both v_(j-1) and v_t. Swap alpha/beta on the alternating
component containing u. It is a path because alpha was missing at u.
If this path does not end at v_(j-1), beta remains missing there, so rotate
the prefix through v_(j-1) and use beta. If it does end there, alpha becomes
missing there while beta remains missing at v_t; rotate the whole fan.
The changed edge uv_j now has color alpha, valid at its predecessor.
Every other fan color is outside {alpha,beta}, so its missing-color condition
survives. In each case one more edge is colored properly. Fan length is
bounded by Delta+1; no unbounded search. This is the classical Vizing
fan/Kempe argument, not a new coloring theorem.

## 3. Packing a small independent extension

Assume total s=sum s_h<=eta*n, where eta will be fixed sufficiently small.
All core classes have size >=alpha*n. A full profile z uses core-only
triangles, triangles h+edge-type e in the core, and spare edges.
Such a profile is obtained by aggregating any fractional packing by vertex
classes. If z_T is a core-triangle mass and z_he is an exceptional-triangle
mass, its relevant capacity equations and inequalities are

  sum_core T a_eT*z_T + sum_h z_he + z_e(spare) = b_e,
  sum_e k_i(e)*z_he <= s_h*n_i.

Here k_i(e) counts the endpoints of the core edge type e in class i, so
an internal edge has k_i(e)=2. Every coordinate is nonnegative. The full
triangle objective is the sum of the core and exceptional triangle masses.
All triangle types, including repeated core clique types, are included.
Let E=d(d+1)/2, c=d+2, cutoff kappa=12(s+1).
For s_h<=c put every m_he=0. Otherwise define

  t_he=floor((1-c/s_h) z_he),
  m_he=t_he if t_he>=kappa, else 0.                  (B)

For each h with s_h>c and each edge type e, distribute its endpoint degrees as evenly as possible in
each incident core class: floor(m_he/n_i) or ceiling for cross pairs,
floor(2m_he/n_i) or ceiling internally, with prefix extras. Each vertex's
total target degree for F_h is at most

  (1-c/s_h) sum_e k_i(e)z_he/n_i + d
  <=s_h-c+d=s_h-2.                                 (C)

The first inequality uses at most d incident edge-type coordinates; the
second is the original h--i spoke capacity. The maximum prescribed degree
of any single pair is <=s. Build F_h pair by pair while forbidding all
previous F_g. Previous maximum degree <=sum_g s_g<=s. If eta<=alpha/96
and n>=96/alpha then every part is at least 48(s+1); retained (B) meets
the other hypothesis of the near-regular lemma. It realizes all targets.
Different edge types have disjoint edge sets, and all F_h are disjoint.

An empty F_h needs no colors. Properly color every nonempty F_h with
Delta(F_h)+1<=s_h-1 colors. Assign colors to distinct
vertices x of I_h and replace each colored core edge uv by triangle xuv.
Each color is a matching, so every spoke is used at most once. Core edges
are disjoint across h. Every triangle is supported by the neighborhood of h.

Let F=union_h F_h. Then Delta(F)<=s, and at every vertex of type i, each
incident edge-type degree differs from its class average by at most r.
This is because each F_h list differs from its mean by less than one.

Let W_h=sum_e z_he. Every exceptional triangle uses two spokes, so
W_h<=s_h*n/2. Scaling (or discarding s_h<=c) loses at most c*n/2 for each h.
Rounding and cutoff discard less than kappa per edge type. Thus the total
loss of exceptional triangles is at most

  r*c*n/2 + 12*r*E*(s+1) <= (r*c/2+24*r*E)*n,      (D)

using s<=n and n>=1. This is linear even when s grows faster than sqrt(n).

## 4. Balanced-deletion core rounding

**Lemma 2 (balanced-deletion rounding).** Fix an integer d>=1, 0<alpha<=1,
and A>=0. There exist eta>0,n0 and an explicit eventual linear coefficient.
Let H be any n-vertex mixed template with at most d classes, each of size
at least alpha*n, and let F be a subgraph of H. For n>=n0, H-F can realize truncated triangle
counts from EVERY real capacity profile y against b_e-f_e, provided
Delta(F)<=eta*n and each incident type-degree of F differs from its class
average by <=A. This is a capacity profile, not an assertion that uniform
distribution over surviving triangles is itself feasible.
An edgeless host is immediate, so assume there is a supported edge type.

For a supported edge type e, write b_ij=n_i*n_j and b_ii=binom(n_i,2).
A pattern P is an allowed triangle type or a spare single-edge type. Let
k_i(P) be its number of type-i vertices and a_eP its edge multiplicity.
The profile condition is y_P>=0 and sum_P a_eP*y_P=b_e-f_e, where f_e counts F edges.
For each pattern and class, assign floor(m_P*k_i(P)/n_i) roles to every
vertex, with one extra on the first remainder vertices. A type-i role has
incident edge-type vector l_iP, with k_i(P)-1 entries internally and k_j(P)
towards another type j. Put d_v=sum_P r_vP*l_iP. All repeated roles of one
type in a triangle or edge have the same vector. Internal incidences count
twice. Thus the average profile vector is precisely the average residual
degree p'_i,e used below.

Let M=binom(d+2,3)+binom(d+1,2), lambda=8(M+A)/alpha,
B=M(6/alpha+2), U=ceil(lambda+B+A). Define theta=1-lambda/n and
m_P=floor(theta y_P), dropping m_P<n. The per-coordinate loss beyond theta
is less than n. Average residual degree p'_i,e=(k_i(e)/n_i)(b_e-f_e) is at
least alpha*n/2 when eta<=alpha/4 and n>=4/alpha. Actual residual degree
differs from p' by at most A. Balanced local role allocation d_v therefore
obeys theta*p'-B <=d_v<=theta*p'+2M. Its complementary degrees are integers
in [1,U], since the lower bound is

  -A+lambda*alpha/2-2M =2M+3A >0.                 (E)

The sparse role-preserving lemma extends to avoidance of F. In copy t of
pattern P, assign its successive type-i roles to (t*k_i(P)+a) modulo n_i,
0<=a<k_i(P). This gives distinct vertices within each component for n_i>=3
and exactly the balanced role prescription, though different components may
repeat pairs or meet F. Use neighborhoods in F union the current component
graph. Let D_s be the maximum component degree counted with multiplicity,
and r_P the largest role count of P at any individual vertex. Replace D in
the candidate count by D_s+Delta(F).
Potential is repeated component-edge excess plus the number of component
edge occurrences lying in F. A swap creating edges absent from this union
strictly decreases that potential, preserving every vertex-pattern role.
The same criterion (4(D_s+Delta(F))+5)r_P<k_i(P)m_P suffices.

Here is its complete candidate count. Choose a component Q containing a
bad edge uv, and the role u of type i; let P be its pattern and A the one or
two other vertices. Among all k_i(P)*m_P type-i positions w in copies Q' of
the SAME P, reject w in {u} union A union the neighborhoods of A. This rules
out at most (2(D_s+Delta(F))+3)*r_P positions. Also reject a candidate if any
other vertex of Q' lies in {u} union N(u). At most D_s+Delta(F)+1 vertices
are forbidden by this second rule, each occurring at most r_P times and
beside at most two candidate positions; thus it rejects at most
2(D_s+Delta(F)+1)*r_P positions. Under the stated strict inequality some
candidate remains. Swapping u,w preserves both components' vertex
distinctness and every vertex-pattern role count. The new incident edges
are absent from F and the current component graph and are mutually distinct;
an equality across the two components would require w=u or u in A.
The bad occurrence disappears and the integer potential drops. Iteration
terminates in a packing disjoint from F. The role counts, and hence D_s and
r_P bounds, remain unchanged throughout.

Dense interface: for d,alpha,epsilon fixed there is delta>0 so the original
host minus degree-delta*n deletions decomposes into prescribed integer
pattern counts >=epsilon*n^2 when the global and singleton indexed lattices
hold. The full statement and proof are supplied in
[DENSE_COMPLETION.md](DENSE_COMPLETION.md). They restate Lemma 5 from the
preceding comparable-class package, with its private-edge family proof based
on Keevash's Theorem 5.15. This includes the indexed lattices, normalization,
part sizes, extension condition and order of all constant choices; no
independent acceptance of that previous package is presumed.

Finite profile hierarchy: epsilon_0=1. Given epsilon_j, use dense completion
at epsilon_j/2 with tolerance delta_j. Let

  tau_j=min(alpha/128,alpha/[64(U+1)],delta_j/4),
  0<epsilon_(j+1)<min(epsilon_j/2,alpha*tau_j/(16M)).

Do this for j=0,...,M. Finally fix eta<=min(alpha/4,min_j tau_j/2).
These constants are fixed before F and y. An empty interval among the M+1
bands splits dense y>=epsilon_j*n^2 from sparse y<epsilon_(j+1)*n^2.
The cyclic sparse list has multiplicity degree
D_s<=6M*epsilon_(j+1)*n/alpha+2M<tau_j*n/2 for large n. Every retained sparse
count is at least n, so r_P<=3m_P/(alpha*n)+1<=4m_P/(alpha*n). Thus Delta(F)+D_s
<=tau_j*n and the avoidance switch applies. Let S be the sparse union.

Complement degree lists from (E) have matching/even sums. The general
criterion (2) builds R disjoint from F union S. Indeed positive target
entries give at least n_i/2 edges per internal pair and at least the smaller
class size per cross pair; for large n these exceed 3U(D+U+1), where
D<=tau_j*n. Equivalently, the stronger sufficient side-length bound
n_i>=alpha*n>8(U+1)(tau_j*n+U+1) holds. Delta(R)<=dU.
The remaining global counts are precisely the dense m_P, and each local
vector is sum_dense r_vP l_iP because S preserved every sparse role count.
Total deletion degree <=tau_j*n+dU<=delta_j*n eventually. Dense completion
applies. Supported types cannot be all sparse: b_e-f_e>=alpha^2*n^2/8,
whereas all sparse contributions sum to <3M epsilon_(j+1)n^2.
Take a finite maximum over this hierarchy and the finitely many template
supports to obtain a uniform n0. The resulting edge-disjoint components
have exactly the prescribed retained m_P counts. Retain their triangle
components. Since W=sum_triangle y_T<=n^2/6, shrinking loses at most
lambda*n/6 and dropping/rounding at most M*n, so the loss is
(lambda/6+M)*n. For A=0 and F empty this gives the same truncated counts and
coefficient as the preceding comparable-class profile theorem.

In the independent-extension application use A=r and core profile

  y_T=z_T for core-only triangles,
  y_e(spare)=z_e(spare)+sum_h(z_he-m_he).

Then sum_P a_eP*y_P=b_e-f_e for every e, and all coordinates are nonnegative.
Its triangle objective
is exactly the original core-only mass. The bounded type-discrepancy proved
in section 3 supplies the hypothesis. Combining with (D) proves the small
independent-extension theorem, with eventual coefficient
lambda/6+M+r*(d+2)/2+24*r*E. The constant eta is also reduced to alpha/96 and
at most one. All thresholds depend only on d,r,alpha, not on the profile or
individual exceptional sizes.

## 5. A universal multiplicity cap

For ANY n-vertex core H and independent twin classes, replace every
s_h by min(s_h,n). This preserves nu, nu*, and the triangle-cover number tau.

For an ordinary packing, the core edges used by triangles centered in I_h
form a simple graph F_h. Recolor it with at most Delta(F_h)+1<=n colors,
assigning them to the retained n vertices when truncation is necessary.
Core edges and all other triangle classes stay fixed. Monotonicity gives
equality of optima.

For a fractional packing and each class actually capped, symmetrize over I_h.
Let t^h_uv be its total
weight using core edge uv and center in I_h. For each core vertex u,
sum_v t^h_uv<=deg_H(u)<=n-1 by core-edge capacities. Distribute t^h_uv
uniformly among the n retained vertices. Each spoke load is <=(n-1)/n,
and each core-edge load is unchanged. Thus the objective is preserved.
For triangle covers, let B be an optimal cover in the capped graph and J
its residual core graph after removing the selected core edges. For each
capped independent class h, the chosen spokes at each of its n copies form
a vertex cover of J[N_h]. If its minimum vertex-cover size is k, these spokes
cost at least n*k. All edges of J[N_h] number at most (n-1)*k, since a minimum
vertex cover meets them all. Add these core edges to B and remove all h
spokes, never increasing the size. Repeat for all capped classes. The
resulting cover extends to arbitrarily many copies because every such
triangle is now hit in the core. Monotonicity proves tau equality.

The bound n cannot uniformly be reduced to n-1 for ordinary packing: for
odd complete cores of order n>=3, n independent centers can use every core edge, whereas
n-1 centers provide at most (n-1)*floor(n/2)<binom(n,2) matching edges. A
packing of binom(n,2) triangles would have to use exactly one core edge in
every triangle, so clique-only triangles cannot repair that obstruction.

This cap is an elementary application of classical coloring and covering,
not a novelty claim about complete split graphs.

## 6. Finite hierarchy for arbitrary independent-class sizes

After the cap, s_h<=n, and total graph order <=(r+1)n. For r=0 the core
theorem applies. For r>=1 set epsilon_0=1. At stage j=0,...,r let
alpha_j=min(alpha,epsilon_j)/(r+1), and obtain eta_j,K_j,n0_j from the
small-extension theorem with core-class bound d+r, independent-class bound r,
and proportion alpha_j. Choose

  0<epsilon_(j+1)<min(epsilon_j/2,eta_j/(2r)).

At most r positive ratios s_h/n occupy the r+1 half-open intervals, so one
is empty. Move all classes with s_h>=epsilon_j*n into the core H'. Its order
n' lies between n and (r+1)n, and all its at most d+r classes have size at
least alpha_j*n'. The remaining independent vertices total
s<r epsilon_(j+1)n<=eta_j*n/2<=eta_j*n'. Their neighborhoods remain unions
of core classes, with no adjacency to the moved independent classes.
Apply the small-extension theorem. Loss <=K_j*n'<=(r+1)max_j K_j*n.
All thresholds are fixed before the supplied class sizes. Enlarge the
constant for the finitely many n below the maximum threshold: every triangle
uses at least one core edge, so nu*(G)<=|E(H)|<=n(n-1)/2 regardless of the
extension sizes. Arbitrarily large original independent multiplicities do
not change either optimum by section 5.

This proves Theorem 1 with existential K(d,r,alpha). It covers small
independent classes at all scales, including multiple incomparable growing
scales. It is not a complete bounded-neighborhood-diversity result.

## 6.1. A sparse graph on the exceptional vertices

**Corollary 3.** Keep the comparable core H of order n and at most r
neighborhood types into its classes, but allow an arbitrary graph on the
added set X. Put q=|E(G[X])|. With the same constant as Theorem 1,

    nu*(G)-nu(G) <= K(d,r,alpha)*n + q.                  (3)

In particular, the loss is linear in n whenever q<=beta*n for a fixed beta.
The vertices of X need not be twins in the full graph; only their
neighborhoods into H have at most r types. This includes arbitrary induced
graphs on at most C*sqrt(n) exceptional vertices, for fixed C, since then
q<=C^2*n/2.

To prove this, delete the q internal X edges, obtaining G_0 to which
Theorem 1 applies. From any fractional packing of G discard triangles using
one of those edges. Their total weight is at most q, by summing the unit
fractional capacities of the deleted edges; repeated counting only increases
that upper bound. Thus nu*(G)<=nu*(G_0)+q, while nu(G)>=nu(G_0).
The displayed inequality follows. This is a direct edge-deletion corollary,
not another design-existence input or a finite-test inference.

When the exceptional induced graph has superlinear edge count, (3) does
not give linear loss. In particular, growing clique cells larger than the
square-root scale remain a substantive excluded boundary.

## 7. Exact evidence and limits

The source builds balanced forbidden-degree realizations, proper edge
colorings, literal exceptional triangles and sparse components avoiding
their core edges. A separately formulated checker verifies every edge,
color, triangle, local type degree and replayed sparse swap. It also checks
compressed core-role identities, exact finite class-hierarchy arithmetic,
multiplicity-cap witnesses, direct minimum triangle covers on small expanded
graphs, and damaged certificates. The hierarchy checks use illustrative
rational tolerances, not computed Keevash constants.

These are author checks of finite constructions and identities, not
independent mathematical review. They do not implement the dense-family
existence theorem, formalize this proof, or compute eta, n0 or K. The
unformalized verification of the imported theorem's hypotheses remains an
explicit trust boundary. Source attribution and graph dependencies are
recorded in [SOURCES.md](SOURCES.md).
