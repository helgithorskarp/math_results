# Optimal toggle words under private simplex attachments

## The theorem

Let K be a finite nonvoid simplicial complex, including its empty face.
Adjoin a **new** greatest element to obtain the face lattice L(K), even
when K is a simplex. Write mu_K(H)=mu_L(K)(H,top).

The toggle game starts with every proper element off and seeks every
proper element on. A move at H is permitted only when mu_K(H) is nonzero
and the principal ideal D(H)={G:G subset H} is monochromatic; it reverses
all of D(H). The top never moves.

Call a winning word *facewise optimal* if it uses every H exactly
|mu_K(H)| times. Suppose a facewise optimal word w for K is supplied.

For i=1,...,m choose an old face F_i in K and a nonempty set W_i of
new vertices. The W_i must be pairwise disjoint and disjoint from the
old vertex set. Put S_i=F_i union W_i and

    K+ = K union (union_i 2^(S_i)).

Thus each added simplex meets K in exactly the simplex on F_i, and
different added simplices meet only in old faces. The F_i may repeat,
be empty, have different dimensions, or contain one another.
Set a_H=#{i:F_i=H} for H in K, and x_+=max(x,0).

**Theorem.** There is an explicit facewise optimal winning word for K+.
Its minimum length is

    ell(L(K+)) = m + sum_(H in K) |mu_K(H)+a_H|             (1)
               = ell(L(K))
                 + 2 sum_(H in K)
                   ((mu_K(H)+a_H)_+ - (mu_K(H))_+).        (2)

The same constructed word minimizes total cost for every assignment of
nonnegative real costs to the moves of K+. No purity, shellability, or
parity coherence of K+ is required. The only hypothesis on K is the
supplied facewise optimal winning word.

This is a closure theorem, not a recognition algorithm. It does not
assert that every nonpure shellable complex, or every simplicial complex,
has such a word. No converse is claimed for deleting attachments.

## 1. The lower bound and the signs of an optimal word

For any winning word, let z(H) be additions minus removals at H.
Each old face G must change from zero to one, so

    sum_(H>=G) z(H)=1.

The unique solution of these triangular equations is z(H)=-mu_K(H).
Consequently every winning word uses H at least |mu_K(H)| times.
This is the classical Möbius net-multiplicity principle, credited in
REFERENCES.md, not a new lower bound.

Equality means that all moves at a given face have the same direction:
if mu_K(H)<0 they add D(H), and if mu_K(H)>0 they remove it.
There are no moves at zero-coefficient faces. Multiplying the separate
lower bounds by any nonnegative costs proves simultaneous weighted
optimality once a facewise optimal word exists.

## 2. Exactly which coefficients change

For a simplicial complex, the Boolean intervals inside its face poset give

    mu_K(H) = -sum_(G in K, G>=H) (-1)^(|G|-|H|).          (3)

This follows either by Möbius inversion or by substitution into the
defining upper recurrence mu(H)=-1-sum_(G>H)mu(G).

If H is an old face, the new cofaces contributed by S_i are the faces
G with H subset G subset S_i and G not subset F_i. There are none
unless H subset F_i. In that case their alternating sum is

    sum_(H<=G<=S_i) (-1)^(|G|-|H|)
      - sum_(H<=G<=F_i) (-1)^(|G|-|H|)
    = -1 if H=F_i, and 0 otherwise,

since H is a proper subset of S_i. New faces of different attachments
are disjoint as sets of faces, so (3) yields

    mu_(K+)(H)=mu_K(H)+a_H                    for H in K.  (4)

A new face belongs to exactly one S_i, and its upper interval consists
of its cofaces in that simplex followed by the new greatest element.
Thus

    mu_(K+)(S_i)=-1,
    mu_(K+)(G)=0 for every other new face G.              (5)

In particular cancellations can turn an old permitted move into a
forbidden move. Ignoring that change would invalidate the original word.

## 3. Replacing additions before appending the unused attachments

For every H put b_H=(-mu_K(H))_+. The input word has exactly b_H
additions at H. Assign min(a_H,b_H) different attachments based at H
to that many occurrences, and replace each chosen move H by its S_i.
Any choice of the occurrences works.

The intersection D(S_i) with the old game elements is exactly D(H).
Before this replacement, the old D(H) is all off because the original
move was an addition. All new faces of S_i are still off: no earlier
old move or other attachment touches them, and S_i has not yet occurred.
Therefore D(S_i) is all off, its coefficient is -1, and the replacement
move is legal. It has exactly the original effect on K and turns on all
private faces of S_i. Repeating this argument proves legality of every
replacement and preserves the original projected state throughout.

We must also check the old moves that remain. If mu_K(H)<0 and an old
H move remains, a_H<b_H, so mu_(K+)(H)=-b_H+a_H<0. If mu_K(H)>0,
its coefficient only increases and stays positive. If mu_K(H)=0 there
was no old move. Hence every unreplaced move remains permitted and
monochromatic with its original direction.

At the end of this modified word, every old face is on and the private
faces of each used S_i are on. Consider an unused attachment S_i based
at H. Its existence means a_H>b_H, so mu_(K+)(H)>0. Append the two moves

    H, S_i.

The first removes D(H), which is entirely on. The new faces of S_i
are still off, so D(S_i) is now entirely off and the second move adds
it. This restores all old faces, fills this attachment's private faces,
and changes no private face belonging to another attachment.
Thus the same argument applies to every remaining attachment, in any
order.

The resulting word wins.

## 4. Counts and optimality

Each new maximal simplex is used once. No other new face is used.

Fix an old H. If mu_K(H)=-b_H<0 and a_H<=b_H, exactly b_H-a_H
old additions remain. If a_H>b_H, all old additions were replaced
and a_H-b_H appended removals occur. If mu_K(H)>=0, its mu_K(H)
old removals remain and a_H new removals are appended. In every case
the count is exactly |mu_K(H)+a_H|, with the correct sign.

Equations (4)-(5) and the lower bound prove (1) and weighted optimality.
Using |x|=2x_+-x and sum_H a_H=m gives (2).

In particular, one attachment adds no moves if its base face has a
negative coefficient; it replaces one addition there. Otherwise it adds
exactly two moves. With several attachments, each negative coefficient
provides precisely that many replacements before further attachments
require pairs. These assertions include the zero-crossing case.

The compiler can be iterated: after each stage its output is a facewise
optimal input for the next. Later simplices may attach along faces
created at earlier stages. The private-vertex condition is required
within each simultaneous stage.

## 5. A cancellation family beyond the parity-coherent compiler

Let q>=3 be odd, let B have q vertices, and let v be another vertex.
Let K_q be the cone with apex v over the boundary of the simplex on B.
Its q facets are {v} union (B minus {b}), for b in B.

This is pure shellable, with h-polynomial 1+t+...+t^(q-1). The already
proved pure-shelling theorem therefore provides a facewise optimal word
of length 2^q-1. Equation (3) gives mu_Kq({v})=(-1)^q=-1.

Attach m>=1 edges {v,w_1},...,{v,w_m}, with distinct new vertices.
The result has

    mu_({v})=m-1,
    ell=2^q+2m-3.                                        (6)

For m=1 the apex coefficient becomes zero. The old apex addition is
replaced by the new edge, so the length remains 2^q-1 and no forbidden
apex move is made.

Ordering the old facets by a shelling and then adding these edges is a
nonpure restriction-interval shelling: each new edge has restriction
{w_i}. For any old facet ordering, the final old cone facet contributes
the apex to its dual restriction interval; each pendant edge does too.
The contributing facet cardinalities are q (odd) and 2 (even). Thus
the previous parity-coherent sufficient condition fails at the apex.
This family is not obtained merely by applying that corollary.

These facet families also have no join tree. Any two old cone facets
share a base vertex, so their path in a purported join tree cannot pass
through a pendant-edge facet. The old facets must therefore induce a
tree. For each b in B, the facets containing b are all old facets except
the one missing b. Their induced subtree must be connected. Thus deleting
any vertex of the old-facet tree would leave it connected, impossible for
a tree on q>=3 vertices. Bare acyclic-family winnability does not supply
this cancellation family.

For q=3,m=1 the facets are

    012, 013, 023, 04,

exactly the cancellation control recorded in the accepted shelling
result and its review. A legal optimal word is

    012, 01, 013, 02, 04, 03, 023.

The theorem replaces its problematic apex move systematically; it
does not infer the general rule from this seven-move example.

The closure also reaches nonshellable pure examples. Starting with a
triangle, attach a second triangle along a single vertex, using two new
vertices. The three-move word is first triangle, common vertex, second
triangle. The resulting pure two-dimensional complex is not shellable:
the two facets intersect only in a vertex, not a codimension-one face.
Its winnability is already compatible with known acyclic-family methods;
the general theorem's scope is the exact optimal compiler, including
bases that are not acyclic families and coefficients that cross zero.

## 6. Limits and verification

The private-new-vertex assumption cannot just be omitted from this proof.
For example, from two isolated vertices a,b, adding edges ax and bx with
the same new vertex x creates a new face with coefficient mu({x})=1.
Formula (5), and hence the compiler as stated, no longer applies.
This is a counterexample to dropping that hypothesis from the coefficient
formula, not an unwinnable complex.

The old word must be facewise optimal. A general winning word may contain
oppositely directed redundant occurrences; the sign-preservation argument
does not cover it.

The verifier recomputes Möbius values by the defining upper recurrence,
replays each move directly on sets of faces, and checks every resulting
multiplicity. On small fixtures, BFS and weighted Dijkstra searches
independently compute true optima from the game's state graph. The code
also tests zero crossing, repeated and nested base faces, empty base
faces, multi-vertex attachments, sequential attachments, and invalid
inputs. The universal theorem is the written proof, not a finite census.

This is an unformalized constructive lemma. Independent review is pending.
It does not determine the smallest unwinnable lattice or revive the
refuted unrestricted Non-Cancelling Intersections conjecture.
