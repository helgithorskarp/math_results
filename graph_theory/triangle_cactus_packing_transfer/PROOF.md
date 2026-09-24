# Linear packing loss for triangle-cactus families

Complete author proof; independent review of this transfer is pending.
The only deep input is the previously accepted balanced triangle-and-edge
profile theorem [B(t,1)](../tuza_bounded_type_linear_rounding/PROOF.md).
Its [independent acceptance](../tuza_bounded_type_linear_rounding_review1/REVIEW.md)
does not constitute a review of the argument here.

All graphs are finite and simple. Copies are **not induced**. Packings are
edge-disjoint; distinct packed copies may share vertices. A triangle cactus
here means a possibly disconnected graph whose nontrivial blocks are K2 or
K3. Thus bridges, arbitrarily branching trees of triangles, friendship
graphs, disconnected components, and isolated vertices are allowed. Every
pattern under discussion has at least one edge.

## 1. Statement and explicit transfer coefficient

Let F be a fixed nonempty finite family of triangle cacti, and let t>=1 be
a fixed integer. There is a finite K(t,F) such that every N-vertex graph G
with at most t mixed classes satisfies

    0 <= nu*_F(G) - nu_F(G) <= K(t,F) N.                  (1)

A mixed class is a clique or an independent set; each cross pair is complete
or empty. No lower bound on class sizes or their ratios is imposed. The
fractional optimum uses all copies of every pattern in F.

The stronger assertion rounds **every** feasible fractional packing, with
below-input counts separately for each vertex-class-typed pattern. Fix a
labeling of the vertices of each F in the family. A type A=(F,phi) specifies
the class phi(u) of each labeled vertex u of F. Choose one labeled
representation of each fractional copy and let x_A be the resulting mass.
We construct edge-disjoint copies with integer counts z_A such that

    0 <= z_A <= x_A,       sum_A (x_A-z_A) <= K(t,F) N.   (2)

No claim about balancing the *assembled* patterns at each vertex is made.

Write b(F) for the number of nontrivial blocks, put

    q = max_F |V(F)|,
    B = sum_F b(F) t^|V(F)|,

and let C=C(t,1), D=D(t,1) be the finite constants in the accepted balanced
profile theorem. One valid transfer coefficient is

    K(t,F) = C + B (2D + 80 + q).                       (3)

This expresses the new loss in terms of the existing constants; it does
not make C or D effective. In particular this is not a practical universal
algorithm. The order N cannot be replaced uniformly by o(N) for this whole
pattern class, since it contains K3 and complete graphs of even order N >= 4
have triangle packing loss at least N/6. Sharp constants for individual
F are not claimed. The empty pattern family is trivially handled separately.

More generally, the proof gives a **conditional clique-block transfer**.
For a fixed integer r>=2, suppose a host class has a balanced full-profile
theorem for K2,...,Kr with component loss CN and per-pattern vertex
discrepancy D. It then has the same
conclusion for every fixed family of block graphs with clique blocks of
order at most r, with

    K = C + B (2D + 20(r+1) + q).                       (4)

The arbitrary-class-size input used here is established only for r=3.
Equation (4) does not assert that input for r>=4.

## 2. What is imported from the accepted theorem

For each supported edge or triangle class-multiset P, let k_i(P) be its
number of vertices in class i, and a_eP its number of edges of class-pair
type e. Host capacities are n_i n_j across classes and binom(n_i,2) inside
a clique class. Given a nonnegative full profile

    sum_P a_eP Y_P = capacity_e,

with impossible types assigned zero, B(t,1) supplies edge-disjoint base
cliques, M_P of each type, with

    0 <= M_P <= Y_P,
    sum_P (Y_P-M_P) <= CN,
    |d_vP-k_i(P) M_P/n_i| <= D  for v in class i.        (5)

Here d_vP is the actual number of base P copies containing v. One edge
label per edge type is sufficient. Its mass will include both true edge
blocks and unused capacity. The *local* assertion in (5), not merely an
objective integrality gap, is needed below.

For the conditional statement (4), replace edge/triangle types here by all
clique types of orders 2,...,r and assume exactly (5) for those types. That
is an explicit hypothesis, not an additional conclusion imported from B(t,1).

The parent proof uses Keevash's generalized design theorem, sparse switches,
and an induction over class sizes. We import precisely (5), including its
existential constants; no new use or specialization of that design theorem
is hidden in this transfer.

## 3. A partition-constrained rounding lemma

There are finitely many items, each having a finite set of options. A
fractional choice gives nonnegative option weights summing to one per item.
Let soft constraints be 0/1 sums of options, and suppose each option occurs
in at most s soft constraints. There is a choice of exactly one option per
item for which **every** soft sum differs from its fractional value by at
most 2s.

Here is a complete floating-variable proof. Freeze every variable equal to
0 or 1. Never change frozen variables. Keep every item equation as a hard
constraint. Drop a soft equation as soon as at most 2s of its variables are
still strictly between 0 and 1. Until then preserve its original sum.

If V variables are floating, every item containing one floating variable
contains at least two: its remaining sum is an integer, while one strictly
fractional entry cannot equal that integer. Consequently at most V/2 item
equations involve floating variables. Every retained soft equation contains
more than 2s floating variables; column sparsity implies that there are
strictly fewer than V/2 such equations. The total number of equations is
therefore less than V. A nonzero homogeneous null direction exists. Move
along it until a variable first reaches 0 or 1. All hard and retained soft
equations are preserved, and the number of floating variables decreases.

The process terminates. At removal, a soft sum still has its initial value;
only at most 2s unfrozen 0/1-coefficient variables can change afterward,
each by at most one. This proves the discrepancy bound. The proof also
handles real input weights. Rational data admit exact rational arithmetic.

This is a standard Beck-Fiala-style rounding argument for a partition
matroid. No novelty is claimed for the discrepancy lemma; a stronger
matroid version is in the primary literature cited in [SOURCES.md](SOURCES.md).

## 4. Labeling and orienting base cliques

This section is written for clique orders at most r; take r=3 for (1).
Every true block label ell=(A,b) has a target mass y_ell=x_A, a base clique
type P, and individually named vertex roles u in b. Include one disposable
slack label for each edge type. Define Y_P as the sum of the label masses
of that type. Apply the balanced full-profile input to obtain (5).

For a fixed P with Y_P>0, each base copy is an item. Its options choose a
label ell of type P and a class-respecting bijection from that abstract
block to the copy. Give each such option weight

    y_ell / (Y_P product_i k_i(P)!).

There are exactly product_i k_i(P)! bijections, regardless of the copy or
label. Thus item weights sum to one. A soft row counts all copies of label
ell; other rows count occurrences of a specified (ell,u) role at a specified
host vertex v. Every option meets one label row and |P| vertex-role rows,
so its column sparsity is at most r+1.

Set a=2(r+1). The fractional label count is

    mu_ell = M_P y_ell/Y_P <= y_ell.

For a role u of class i and v in that class, its fractional occurrence count
is (y_ell/Y_P)d_vP/k_i(P), which differs from mu_ell/n_i by at most D,
by (5). Round with Section 3. Every label count and vertex-role count changes
by at most a.

For every **true** label, remove copies until its count m_ell is at most
floor(y_ell). At most a copies are removed: before trimming the integer
count is at most mu_ell+a <= y_ell+a. Discard the slack copies outright.
If rho_v,ell,u is the retained actual role count, then

    0 <= m_ell <= y_ell,
    |m_ell-mu_ell| <= 2a,
    |rho_v,ell,u-m_ell/n_i| <= D+4a =: D1.              (6)

The last inequality uses an error at most D+2a relative to mu_ell/n_i,
then at most 2a/n_i in replacing mu_ell by m_ell. It holds even for n_i=1.
Zero-mass types have no copies and require no division by zero. The case
M_P=0 with Y_P>0 gives empty item sets and the same inequalities.

If L is the number of true block labels, the total block deficit is

    sum_true (y_ell-m_ell)
      <= sum_P (Y_P-M_P) + 2a L <= CN + 2a B.          (7)

Indeed, sum_all_labels(y_ell-mu_ell)=sum_P(Y_P-M_P), and all these summands
are nonnegative. Omitting slack labels can only decrease that sum. This
accounts for losses *before* gluing and does not multiply the original
CN loss by the number of blocks.

For r=3, a=8, D1=D+32, and (7) is CN+16B. All retained blocks, for all types
and labels together, are still edge-disjoint because they came from the
single base packing.

## 5. Assembly at an articulation vertex

Fix a typed pattern A with target x=x_A>0, and first consider a connected
component containing an edge. Its nontrivial blocks have a tree-like order:
start with one block, then add each new block along exactly one vertex of
the union already built. This follows from the block-cut incidence tree.
All other abstract vertices of a new block are new. Choose a previous
parent block containing the shared abstract vertex u.

At any stage keep partial copies that are injective on their abstract
vertices. They use distinct input instances of each block already added.
Let a_v be the number of current partial copies in which u maps to v, and
let b_v be the number of available instances of the new block with u at v.
All instances of the new label are still unused at this stage.

The raw parent role list dominates the current demand, so (6) gives

    a_v <= m_parent/n_i + D1 <= x/n_i+D1,
    b_v >= m_new/n_i-D1 = x/n_i-delta_new/n_i-D1,

where i=phi(u) and delta_new=x-m_new>=0. In particular

    sum_{v in class i} max(0,a_v-b_v)
       <= delta_new+2D1 n_i.                           (8)

We do **not** assume that surviving partial copies remain balanced.
Their domination by an original parent role list is sufficient.

A candidate new block rooted at v is incompatible with a partial copy only
if one of its other vertices already occurs in that partial copy. Every
other vertex w of the new clique is adjacent to v. Since all candidate
blocks are edge-disjoint, the edge vw shows that at most one candidate
rooted at v can contain any particular w. A partial copy therefore forbids
at most q-1, and certainly at most q, candidate blocks in the original list.

Greedily attach a compatible unused candidate to each request; discard a
request if none remains. With a requests and b candidates, each request
forbidding at most q candidates, this produces at least min(a,b)-q matches
(or zero if that lower bound is negative). To see this, a failed request
can occur only after at least b-q candidates have been used. If every
request succeeds the assertion is immediate. Thus at v the number of
discarded requests is at most max(0,a_v-b_v)+q. By (8), the stage loses at
most

    delta_new + (2D1+q)n_i <= delta_new+(2D1+q)N.        (9)

New embeddings are injective by construction. They use no edge twice,
even between distinct output copies or distinct types A, because all
input blocks were globally edge-disjoint. Copies discarded later need
not have their constituent blocks recycled.

For a component with b_j nontrivial blocks, its final count p_j consequently
satisfies 0<=p_j<=x and

    x-p_j <= sum_{b in component} delta_b
                    +(b_j-1)(2D1+q)N.                 (10)

For the first block the loss is exactly its deficit; every later block
is charged once by (9).

## 6. Disconnected components and isolated roles

The c connected components containing edges can be assembled separately.
Each candidate component copy has no isolated vertex. Because the candidate
copies are edge-disjoint, at most deg_G(w)<=N-1 of them contain a fixed host
vertex w: choose any incident edge within each such copy, obtaining distinct
host edges at w.

A partial union on at most q vertices therefore forbids at most q(N-1)
candidate copies of the next component. The same greedy argument joins two
lists of sizes p,p' into at least min(p,p')-q(N-1) vertex-disjoint pairs.
When both sizes are at most x, the new deficit is at most

    (x-p)+(x-p')+qN.

Joining c lists and using (10) yields a number z_A with

    0 <= z_A <= x_A,
    x_A-z_A <= sum_{b in A} delta_b
       + [(b(F)-c)(2D1+q)+(c-1)q]N
      <= sum_{b in A} delta_b+(b(F)-1)(2D1+q)N.         (11)

Extra edges between the component images do not matter: copies are not
induced. Add isolated vertices last. A positive input type was realized by
an injective original F copy, so class i has at least |phi^{-1}(i)| vertices.
Every current partial embedding uses only its prescribed nonisolated roles.
There are therefore enough unused vertices in each class for all its
isolated roles. Distinct output copies may reuse these vertices.

## 7. From a fractional F-packing to a full base profile

Each edge of a pattern belongs to exactly one nontrivial block. Replace
every fractional typed F copy of mass x_A by one block label of that mass
for each of its blocks. Summing edge loads gives exactly the original
fractional edge loads. Aggregate these masses by base clique type and add
the unused host edge capacity as a slack-edge label. This gives the full
profile required in Section 2; no capacity is counted twice. Positive typed
patterns satisfy class-size and adjacency feasibility, and so do all their
blocks. Nonedges of F impose no restrictions.

Apply Sections 4--6 to this one profile. There are at most B true block
labels. Summing (11) over all positive types A and then using (7), for N>=1,
gives

    sum_A(x_A-z_A)
      <= CN+2aB+B(2D1+q)N
      <= [C+B(2a+2D1+q)]N
       = [C+B(2D+20(r+1)+q)]N.

This proves the conditional transfer (4), and r=3 proves (2), (3), and (1).
For an empty host every pattern has an edge, hence every packing mass is
zero. Real weights cause no issue in the existence argument; all audited
computations use exact rational weights.

## 8. Verification boundary and what is new

The new mathematical bridge consists of assigning separate block labels
and roles, then assembling copies using parent-role domination and the
one-sided collision bound. Neither an objective-only triangle rounding
bound nor global block counts would suffice. No claim that a damaged partial
packing stays locally balanced is needed.

The source implements the floating-variable step and the collision-aware
assembly. Definition-level checks validate each option choice, discrepancy,
trim, role count, injective pattern embedding, and actual edge disjointness
on finite fixtures. Larger affine fixtures include all vertices in a single
class, so accidental collisions beyond the common articulation vertex really
occur. They are not restricted to the easy case of a different class for
every pattern vertex.

These checks do not implement the universal design theorem or prove (1) by
enumeration. The new universal argument is the written proof above, with
(5) as an explicit external dependency. Longer cycles, two-vertex gluing,
K4 blocks, growing t or growing F, formal verification, effective base
constants, and historical priority remain outside the unconditional claim.
