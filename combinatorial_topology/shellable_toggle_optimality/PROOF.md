# Shellings give universally optimal toggle words

## 1. Statement and conventions

Let K be a finite, nonvoid, pure simplicial complex, all of whose facets have
q vertices, where q>=1. The empty face belongs to K. Set

    L(K) = K together with a NEW greatest element hat1.

The order on K is inclusion. Even when K is a single simplex, its maximal
face and hat1 are different elements. This is a lattice: meet is intersection;
the join of faces is their union if that union is a face, and hat1 otherwise.

Write mu(H)=mu_L(H,hat1). Thus mu(hat1)=1 and

    mu(H) = -1 - sum_{G in K, H proper-subset G} mu(G).       (1)

The game starts with no elements on and seeks exactly K on. A move at a face
H is allowed if mu(H) is nonzero and its principal ideal

    D(H) = {G: G subset H}

is monochromatic. It toggles every element of D(H). The new hat1 is never
chosen or toggled. The empty face is an actual game element; it is not the
empty game state.

A shelling F_1,...,F_m is understood in its restriction-face form: for each
i the faces first appearing in F_i are exactly the interval

    [R_i,F_i] = {H: R_i subset H subset F_i}.                (2)

In particular R_1 is empty, and the intervals partition K. This is the usual
pure simplicial shelling convention, including zero-dimensional complexes.

**Theorem.** Given such a shelling, one can explicitly construct a winning
word which uses each face H exactly |mu(H)| times. Every occurrence of H
adds D(H) if mu(H)<0 and removes D(H) if mu(H)>0. Consequently:

1. The minimum number of moves is

       ell(L(K)) = sum_{H in K}|mu(H)|
                 = sum_{i=1}^m 2^{|R_i|} = h_K(2).        (3)

2. For ANY nonnegative real move costs c(H), the same word has minimum cost

       sum_{H in K} c(H)|mu(H)|.                          (4)

3. No augmented face lattice of a pure shellable complex is unwinnable.
   A supplied shelling is a compact certificate for this exclusion; no
   enumeration of the game's state graph is required.

Here the h-polynomial convention is

    h_K(t) = sum_{H in K} t^{|H|}(1-t)^{q-|H|}.

There is no assertion for arbitrary lattices, arbitrary nonshellable
complexes, or nonpure shellings. Nor is shellability asserted necessary.
The theorem does not determine the minimum order of an unwinnable lattice.

## 2. The unconditional cost lower bound

This part is the standard Möbius multiplicity principle, not a new invention;
see Amarilli--Monet--Suciu, Propositions 4.7 and 5.8. We give its short proof
to fix signs and make the optimization statement self-contained.

In any winning word on any finite lattice P, let a(v) and b(v) be the numbers
of moves at v that add and remove its ideal, and let z(v)=a(v)-b(v). Every
proper element x must finish on, so

    sum_{v>=x, v!=hat1} z(v) = 1.                         (5)

These equations are triangular in a reverse linear extension. Their unique
solution is z(v)=-mu(v,hat1), by the defining Möbius recurrence. Hence

    a(v)+b(v) >= |z(v)| = |mu(v,hat1)|.                  (6)

Multiplying (6) by any c(v)>=0 proves the lower bound (4). If a word attains
the unweighted bound, equality holds at every face separately; it therefore
also attains every nonnegative weighted bound. These observations alone do
not establish that a lower-bound-attaining legal word exists.

## 3. Shelling intervals prevent Möbius cancellation

For H in K, the Boolean intervals below every face give the alternative
formula

    mu(H) = - sum_{G in K, G>=H} (-1)^{|G|-|H|}.           (7)

For completeness, substitute the right side of (7) into (1). After swapping
sums, the inner sum over H subset G subset S equals (1-1)^{|S|-|H|}, so only
S=H survives, with value -1. Thus (7) follows by uniqueness in (1).

Split (7) over the disjoint shelling intervals [R_i,F_i]. There is no
contribution when H is not a subset of F_i. Otherwise the contributing
faces range from H union R_i to F_i. Their alternating sum is zero unless
H union R_i=F_i, and is (-1)^{q-|H|} in that case. Define

    b(H) = #{i: F_i\R_i subset H subset F_i}.

Then

    mu(H) = (-1)^{q-|H|+1} b(H).                          (8)

Purity makes the sign independent of i. In particular, every face in any
of the dual intervals [F_i\R_i,F_i] has nonzero Möbius value. Also,

    sum_H |mu(H)| = sum_H b(H) = sum_i 2^{|R_i|}.          (9)

Equation (8) is an elementary consequence of the classical shelling
partition. We do not claim the shelling partition or the h-polynomial
identity as new.

## 4. A legal word for clearing a union of ideals

Let E_1,...,E_r be sets, all of whose nonempty indexed intersections are
permitted toggle sets. If their union is initially all on, a word C(E_1,...,E_r)
turns that union off and affects nothing outside it. For r=0 the word is empty.
For r>=1 set

    C(E_1,...,E_r) =
      C(E_1,...,E_{r-1})
      reverse(C(E_1 intersect E_r,...,E_{r-1} intersect E_r))
      [E_r].                                             (10)

Proof by induction: the first word turns the old union U off. Its intersection
U intersect E_r is now off. The reversed inner word turns exactly that
intersection back on, while E_r\U has stayed on throughout. Thus E_r is
monochromatically on and may be turned off in the final move. The result is
that U union E_r is off. Outside this union nothing changes. Reversing a
legal toggle sequence gives a legal sequence from its final state.

Each nonempty indexed subset A of {1,...,r} contributes its intersection
exactly once in (10): subsets not containing r occur in the first block;
those containing r and another index in the second; and {r} at the end.
Thus the length is 2^r-1. Empty SET intersections cause no difficulty in this
abstract lemma; in the face-lattice application even D(empty) contains the
empty face and is not an empty set of game elements.

## 5. Constructing the optimum, facet by facet

Maintain the invariant that just the faces in the first i-1 facets are on.
Write R_i={r_1,...,r_s}. By (2), the old faces in F_i form exactly

    B_i = union_{j=1}^s D(F_i\{r_j}).                     (11)

For s=0 this is empty. Every nonempty indexed intersection of the ideals
in (11) is D(F_i\A) for a nonempty A subset R_i. By (8), its generating
face has nonzero mu, so it is an allowed move.

Use (10) to clear B_i, and then toggle D(F_i) on. All of D(F_i) is off
immediately before the last toggle: B_i was just cleared and the other faces
were new. This last move is allowed because mu(F_i)=-1. After it, all old
faces are restored and all new faces are on, establishing the invariant.

This stage uses every face in [F_i\R_i,F_i] once: all nonempty A come from
the clearing word, and A=empty from the last facet move. Over all stages,
each face H is used b(H)=|mu(H)| times. The final state is K, so the universal
lower bound (6) proves both optimality and the asserted sign of every move.
In particular, no separate assumption about intermediate signs is needed.

Finally, summing the h-polynomial over a shelling interval gives

    sum_{R_i<=H<=F_i} t^{|H|}(1-t)^{q-|H|} = t^{|R_i|}.

Thus h_K(t)=sum_i t^{|R_i|}, proving the last equality in (3).

## 6. Examples and exact limitations

- One q-vertex simplex: R_1=empty, h=1. Toggle its maximal face once. It is
  essential that the game top is the separately adjoined element.
- n isolated vertices: h=1+(n-1)t and ell=2n-1. The empty face is removed
  n-1 times; its Möbius value is n-1.
- Two triangles sharing an edge: h=1+t and ell=3. Add the first triangle,
  remove the common edge's ideal, add the second triangle.
- Cone over a four-cycle, shelling
  012, 023, 034, 041: restrictions empty, {3}, {4}, {1,4};
  h=1+2t+t^2 and ell=9. Its boundary vertices and boundary edges all have
  zero Möbius value, so this is not merely the known case with no zeroes.
  Its four facets have no join tree with the running-intersection property:
  each rim vertex forces an edge between its two incident facets, forcing
  a four-cycle in any such tree. At the empty face it also has four minimal
  covering zeroes, beyond the two-covering-zero condition proposed in
  Amarilli--Monet--Suciu Section 7. These distinctions concern those named
  sufficient conditions, not all conceivable prior consequences.

**Purity audit.** Consider the nonpure interval-shelling

    012, 013, 023, 04.

Every stage has a unique restriction face, but the common vertex {0} has
mu=0: its triangle contribution and its edge contribution cancel. The naive
word above attempts a forbidden move at {0}. This does not make the complex
unwinnable. A seven-move winning word is

    012, 01, 04, 02, 013, 03, 023,

which the independent replay and BFS check. The example explains exactly
why (8), and hence this particular shelling compiler, requires purity;
it does NOT prove that the theorem's conclusion fails for every nonpure
complex or that no stronger compiler could work.

No recognition algorithm for shellability is supplied. Given a shelling,
the emitted word has the exact optimal length h_K(2), at most 2^q times the
number of facets. This is an output-length statement, not a claim of a
polynomial-time algorithm for arbitrary succinctly represented complexes.
Finite computation corroborates the proof and implementation; it is not
the reason the all-size statement holds. Independent review and formal
proof-assistant checking have not yet been performed.
