# Stellar subdivisions transport legal and optimal toggle words

## 1. Statement

Let K be a finite nonvoid simplicial complex, including the empty face.
Adjoin a **new** greatest element to its face poset, even when K is a simplex.
Write mu_K(H) for the upper Mobius value of a face H in this augmented lattice.
A game state is a set of faces. A move at H is allowed when mu_K(H) is nonzero
and D(H)={G:G subset H} is either wholly off or wholly on; it flips D(H).
A winning word goes from no faces on to every face on. The adjoined top is
never chosen. In particular the empty face is a game element, distinct from
the empty state.

Call a winning word **facewise optimal** when it uses H exactly |mu_K(H)| times
for every face. This is stronger than merely being winning.

Let sigma be a nonempty face, s=|sigma|, and p a new vertex. Let K' be the
stellar subdivision of K at sigma:

    K' = {H in K : sigma is not a subset of H}
         union { {p} union A union B : A proper-subset sigma,
                                      B in link_K(sigma) }.

**Theorem.** There is an explicit compiler with the following properties.

1. Every winning word for K gives a winning word for K'. An occurrence of H
   is replaced by one move if sigma is not a subset of H, and by exactly
   2^s-1 moves otherwise. This includes nonoptimal input words with backtracking.
2. Facewise optimal input words give facewise optimal output words. The same
   output word minimizes every choice of nonnegative face-dependent move costs.
3. If K has a facewise optimal word, the shortest winning length for K' is

       ell(K') = ell(K) + (2^s-2) sum_{H in K, H superset sigma}|mu_K(H)|.

The result has no purity, shellability, manifold, or nonvanishing hypothesis.
Zeros may occur anywhere. Stellar subdivision at a singleton simply relabels
that vertex, and the factor is one. The hypothesis that sigma is nonempty and
that p is fresh is essential to the stated operation.

All finite sequences of stellar subdivisions consequently preserve winnability
and preserve the existence of facewise optimal words. In particular an
unwinnable augmented face lattice cannot be obtained by stellar subdivisions
from a winning one. This is a one-way transport theorem; stellar welds and
arbitrary PL equivalences are not covered.

## 2. The standard lower bound and the Mobius transport identity

In any winning word let z(H) be additions minus removals at H. For every face X,

    sum_{H superset X} z(H) = 1.

Triangular Mobius inversion gives z(H)=-mu_K(H). Thus every winning word uses
H at least |mu_K(H)| times. This is the standard signed-multiplicity principle
of Amarilli--Monet--Suciu, not a new lower bound. Attaining every bound also
minimizes sum_H c(H) times the number of H moves for all c(H)>=0.

Boolean intervals in a face poset give

    mu_K(G) = -sum_{H in K, H superset G} (-1)^(|H|-|G|).       (1)

The stellar subdivision satisfies the identities

    mu_K'(G) = mu_K(G)                  if p not in G,          (2)
    mu_K'({p} union A union B)
       = (-1)^(s-|A|-1) mu_K(sigma union B).                   (3)

Here (2) is only asserted for faces G of K', hence sigma is not a subset of G;
it includes the empty face. Formula (3) uses A proper-subset sigma and
B in link_K(sigma), so these two sets are disjoint.

For (2), group terms of (1) by their old carrier H. Removed carriers contain
sigma. If such H also contains G, its replacement terms correspond exactly to
A with G intersection sigma subset A proper-subset sigma. Since G does not
contain sigma, their alternating sum is

    sum_A (-1)^(1+|A|+|H\sigma|-|G|) = (-1)^(|H|-|G|).

This equals the removed term. For (3), the coface sum factors into

    sum_{A subset A' proper-subset sigma} (-1)^(|A'|-|A|)
       = (-1)^(s-|A|+1)

and the coface sum over B' in link_K(sigma) containing B, which equals
-mu_K(sigma union B). Applying the minus sign in (1) proves (3).
These are elementary Mobius/Euler identities; the legal-word transport below
is the substantive additional assertion.

## 3. A local word for a subdivided simplex

Let C be a nonempty simplex disjoint from sigma. The complex

    Q = 2^C * boundary(2^sigma)

has facets F_i=C union (sigma\{v_i}), for an ordering
sigma={v_0,...,v_{s-1}}. They have a shelling in this order, with restriction
face R_i={v_0,...,v_{i-1}}. Its dual intervals

    [F_i\R_i, F_i]

partition precisely the faces C union A with A proper-subset sigma. Indeed
each proper A has a unique largest index i for which v_i is absent.

There is a legal word W(sigma,C) which fills Q from off and uses each of those
2^s-1 generators exactly once. One can use the previously proved pure-shelling
compiler; the needed local construction is recalled here to make it explicit.

For ideals E_1,...,E_r whose union is on, define a clearing word recursively by

    Clear(E_1,...,E_r) = Clear(E_1,...,E_{r-1})
       reverse(Clear(E_1 intersection E_r,...,E_{r-1} intersection E_r))
       [E_r].

The empty list gives the empty word. The first block clears the old union U;
the second restores U intersection E_r; the last clears E_r. This proves
legality by induction, with no action outside the union. Each nonempty indexed
intersection occurs once. Reverse is literal reversal of the move list.

At stage i the old faces in F_i are the union of D(F_i\{v_j}) for j<i.
Clear that union, then add D(F_i). The generators used at this stage form the
dual interval above. All generators contain C, so the construction uses no
faces outside the stated list. For example s=2 gives the three-move word

    C union {v_1}, C, C union {v_0}.

The word fills the whole of Q, including its faces that do not contain C;
only its *move generators* are restricted to contain C. Reversing it clears Q
when Q is wholly on.

## 4. Carrier synchronization proves legality globally

Define a carrier map from the faces of K' to the faces of K:

    c(G)=G                              if p not in G,
    c({p} union A union B)=sigma union B otherwise.

Initially all faces are off. Maintain this invariant at the endpoints of
compiled blocks: the color of every new face G equals the old color of c(G).
No synchronization is asserted inside a block.

Suppose the next old move is at H. If sigma is not a subset of H, then
c^(-1)(D(H))=D_K'(H). Toggle that ideal once. Its Mobius value is nonzero by
(2), and the invariant is preserved.

Otherwise write H=sigma union B. The preimage c^(-1)(D(H)) is exactly

    Q_H = 2^({p} union B) * boundary(2^sigma),

the stellar subdivision of the full simplex on H. The invariant and old
legality imply Q_H is monochromatic. Put C={p} union B. Use W(sigma,C) for an
old addition and reverse(W(sigma,C)) for an old removal. Each generator is
{p} union A union B, whose global Mobius value is a sign times mu_K(H), by (3).
Hence every generator is allowed even when its global sign differs from its
local sign. The local construction needs only nonvanishing and monochromatic
ideals; it does not require any global sign assumption on the input word.

The block flips all of Q_H and nothing else. This is precisely the inverse
image of the old ideal, so carrier synchronization is restored. Induction
proves legality and the final winning state for arbitrary winning input words.

If the input is facewise optimal, an old surviving face G is used exactly
|mu_K(G)| times, matching (2). Each new generator with carrier H is used once
per occurrence of H and by no other compiled block. Its count is therefore
|mu_K(H)|=|mu_K'(G)| by (3). The standard lower bound proves facewise and
weighted optimality. Counting the 2^s-1 faces in each replaced carrier fiber
proves the length formula.

This argument also supplies a precise cost formula for arbitrary nonnegative
new costs c':

    minimum cost = sum_{sigma not-subset G} c'(G)|mu_K(G)|
       + sum_{H superset sigma}|mu_K(H)|
           sum_{A proper-subset sigma} c'({p} union A union (H\sigma)).

The optimum is attained by the same compiled word for every c'.

## 5. Barycentric consequence: ordered-Bell amplification

Write B_q=sum_{r=1}^q r! S(q,r) for the ordered Bell number, where S(q,r)
counts set partitions into r nonempty blocks. If K has a facewise optimal word,
then so does its barycentric subdivision sd(K), and

    ell(sd(K)) = |mu_K(empty)|
                 + sum_{nonempty H in K} B_|H| |mu_K(H)|.       (4)

Existence follows by stellar subdivision of original faces in decreasing
dimension; subdivisions of singleton faces can be omitted as relabelings.
This standard construction of sd(K) is independently compared in the checker
with its definition as the complex of chains of nonempty faces.

For completeness a nonempty chain H_1<...<H_r=H in sd(K) has

    mu_sd(K)(chain) = (-1)^(|H|-r) mu_K(H).                    (5)

To see this, its link is the join of the order complexes of the open Boolean
intervals (empty,H_1),(H_1,H_2),...,(H_{r-1},H), and the strict upper interval
K_{>H}. The first r factors are subdivided boundaries of simplexes on the
successive nonempty differences; the last is sd(link_K(H)). The standard
identity reduced-chi(X*Y)=-reduced-chi(X)reduced-chi(Y) gives (5), including
the convention that the boundary of a vertex is {empty} with reduced Euler
characteristic -1. The empty face value is unchanged. There are r! S(|H|,r)
chains of length r ending at H, by their ordered successive differences.
Summing absolute values proves (4). The chain and ordered-partition counting
is classical; its interpretation as an attained toggle optimum uses the theorem.

## 6. Application beyond pure shellability, and scope

The compact file seeds.json supplies explicit winning words for the boundary
of a tetrahedron, the six-vertex triangulation of RP^2, and a seven-vertex torus.
The verifier checks every move, every face count, connected cyclic vertex links,
two triangles per edge, connectivity, Euler characteristic, and orientability.
The latter two seeds have f-vectors (6,15,10) and (7,21,14), and their words
have lengths 31 and 43 respectively. The torus facets are the translates
modulo 7 of {0,1,3} and {0,2,3}; both full facet lists are in the certificate.

For a closed triangulated surface, mu(triangle)=-1, mu(edge)=1,
mu(vertex)=-1, and mu(empty)=chi-1. Thus every stellar refinement of either
of these two seeds has a facewise optimal word of length 2E+1, where E is
the number of edges in the refined triangulation. Its first barycentric
subdivision has length 181 for the RP^2 seed and 253 for the torus seed.
These numbers are examples of the compiler, not a parameter census.

This application is outside the pure-shellable theorem. A pure two-dimensional
shelling gives mu(empty)>=0, immediately excluding the torus (mu(empty)=-1).
For RP^2, mu(empty)=0 would force every shelling attachment after the first
to meet earlier facets in a proper union of boundary edges. Each such
attachment collapses back onto the preceding complex, so K would collapse
to the first triangle. But the sum modulo 2 of all its triangles is a nonzero
2-cycle, since every edge belongs to two triangles, and there are no 3-faces.
This contradicts collapsibility. The same argument applies to their refinements.

The pass began with the broader surface question; the theorem closes its
stellar-refinement subfamilies, not the whole question. There is no claim here
that every triangulation of a surface is reached from these seeds by forward
stellar subdivisions. Allowing stellar welds in a PL equivalence theorem does
not supply that missing implication. We prove neither a converse to transport
nor a characterization of all optimal or all winnable complexes, and do not
settle the minimum order of an unwinnable lattice. No generic surface search,
formal proof-assistant verification, or independent peer review is asserted.
