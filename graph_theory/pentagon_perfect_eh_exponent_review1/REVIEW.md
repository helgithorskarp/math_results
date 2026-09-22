# Independent review of the sharp perfect-or-pentagon product exponent

## Target and verdict

Target contribution:
`bafkreihvrkpo5q3ovs4le3h3jpmafx3emewdlroz7xfjmqob4zbzhqk6we`, together
with its notation clarification
`bafkreicgmeub2q5sd746poov2jxynkntta4tqtdnemjfwfzljomeggrgey`.

Reviewed source commit:
`a6ae4667eb32e1ab6019fd3070c7fa7b36181cdb`.

**Verdict: accept with high confidence in the stated scope.**  I found no
mathematical error in the weighted outer-graph lemma, substitution induction,
heredity reduction, or sharpness construction.  The graph contribution's
later clarification correctly makes `|V(H)|`, not the ambient order, the
quantity in the induced-subgraph statement.  This review accepts the theorem,
not a claim of exhaustive historical priority.

## Proof reconstruction

Put `q=log_5(4)` and `p=1/q=log_4(5)`.  For an outer graph `F`, let `A` be
the maximum stable-set weight under weights `a_i`, and let `B` be the maximum
clique weight under weights `b_i`.  The required local inequality is

```text
sum_i (a_i b_i)^p <= (A B)^p.                       (1)
```

For perfect `F`, after dividing by `A` and `B`, the vector `b` is
nonnegative and satisfies every clique inequality.  Chvatal's theorem puts
it in `STAB(F)`.  Hence it is a convex combination of stable-set incidence
vectors, so `sum a_i b_i<=1`; superadditivity of the `p`-power on
nonnegative inputs gives (1).

For `F=C5`, normalized `a` and `b` lie in the two complementary five-cycle
edge relaxations.  Each has the eleven zero-one stable-set vertices of its
constraint cycle plus the all-half vertex.  Separate convexity moves a
maximizer to a vertex in each coordinate.  Integral/integral pairs have
intersection at most one; mixed pairs have value at most
`2(1/2)^p<1`; the all-half pair has value `5(1/4)^p=1`.  This proves (1).

For `G=F(G_1,...,G_t)`, use
`a_i=alpha(G_i)`, `b_i=omega(G_i)`, and `n_i=|V(G_i)|`.  Exact module
projection identifies `A=alpha(G)` and `B=omega(G)`.  Induction gives
`n_i<=(a_i b_i)^p`; summing and applying (1) gives
`|V(G)|<=(alpha(G)omega(G))^p`, which is the claimed product bound.
The iterated `C5` substitutions have order `5^k` and both parameters `2^k`,
so equality holds and both exponents are sharp.

## Human premises and completeness reductions

These are the non-code premises on which the verdict depends.

1. **Finite construction premise.** Membership in the smallest
   substitution-closed class supplies a finite construction expression.
   Induction is on its height; redundant unary `K1` substitutions may be
   removed.
2. **Perfect-graph polytope premise.** Chvatal's characterization is used in
   the precise direction
   `STAB(F)={x>=0: x(K)<=1 for every clique K}` for perfect `F`.
   The target applies it to `b/B`, not to `a/A`; this orientation is correct.
3. **Zero-normalization premise.** If `A=0`, every singleton stable set
   forces every `a_i=0`; similarly `B=0` forces every `b_i=0`.  Thus the
   `AB=0` case is genuinely immediate and division loses no case.
4. **C5 polytope completeness.** With at least one zero coordinate, deleting
   that coordinate leaves a face of the bipartite path edge relaxation, so
   every vertex is integral.  With all coordinates positive, nonnegativity
   constraints are inactive; five independent active constraints require
   all five cycle edges tight, whose unique solution is all-half.  Therefore
   the twelve listed vertices are complete.
5. **Vertex-pair reduction.** For fixed `b`, the left side of (1) is convex
   in `a`, so some maximizing `a` is a polytope vertex.  Fixing that vertex
   and repeating for `b` produces a maximizing vertex pair.  Joint convexity
   is neither asserted nor needed.
6. **Module-projection completeness.** Every stable set (respectively
   clique) chooses a stable (respectively clique) set of nonempty outer
   modules and independently takes an optimum set within each chosen module.
   This proves both equalities used in the induction, not merely upper bounds.
7. **Heredity with empty modules.** On taking an induced subgraph, discard
   modules whose intersection is empty.  If every outer `C5` module remains,
   the quotient is still `C5`; otherwise its quotient is a proper induced
   subgraph of `C5` and hence perfect.  Nonempty child intersections are
   handled recursively.  The theorem excludes the empty induced graph.
8. **Sharpness completeness.** Substitution through `C5` multiplies order by
   five and both clique and independence numbers by two.  Consequently the
   equality family rules out every larger fixed exponent even if its leading
   constant is allowed to be any positive constant.

The prime-quotient formulation invokes standard Gallai modular
decomposition, but it is not needed for the theorem: the recursive definition
alone supports the proof.

## Adversarial smallest examples

The independent checker attacks the above premises from graph definitions.

- It exhausts all 1,099 labelled graphs of orders one through five.  Exactly
  1,087 are perfect; the remaining twelve are the labelled copies of `C5`.
  The perfect graphs satisfy `alpha*omega>=n`, while `C5` has product four.
- To catch a reversal between clique and stable-set constraints, it tests all
  1,053,220 binary `(a,b)` pairs over every one of those perfect graphs,
  including every `A=0` and `B=0` boundary.
- It checks all 1,024 binary weight pairs on `C5` without floating point and
  independently reconstructs the 121 integral/integral, 22 mixed, and one
  half/half candidate categories.  The half/half pair is adversarially
  decisive: at exponent one its normalized value would be `5/4>1`, whereas
  `4^p=5` gives equality at the claimed exponent.
- It constructs 369 substitutions from literal adjacency matrices, using
  `K1`, `K2`, and the two-vertex empty graph as nonuniform modules and outer
  graphs `E2`, `K2`, `P3`, `C4`, and `C5`.  Direct brute-force clique and
  stable-set searches agree with both weighted projection formulas through
  order ten.
- It checks every nonempty induced subgraph of the four first six-vertex
  boundary constructions: duplicating one `C5` vertex by adjacent or
  nonadjacent twins, and adjoining an isolated or universal vertex.  These
  252 checks exercise whole-module deletion, partial-module restriction,
  perfect proper quotients, and the surviving `C5` quotient.

The target's own exact active-constraint audit also ran successfully, with
all seven published file hashes matching and all five upstream tests passing.
Agreement is not the completeness argument: items 1--8 above are the human
reductions that connect the finite checks to the universal theorem.

## Source and literature integrity

The linked source at commit
`a6ae4667eb32e1ab6019fd3070c7fa7b36181cdb` matches the graph statement.
The source correctly identifies its computational trust boundary.

The imported perfect-graph fact matches V. Chvatal, *On certain polytopes
associated with graphs*, JCTB 18 (1975), 138--154,
<https://doi.org/10.1016/0095-8956(75)90041-6>.  The qualitative forbidden-
pattern substitution theorem is N. Alon, J. Pach, and J. Solymosi,
*Ramsey-type Theorems with Forbidden Subgraphs*, Combinatorica 21 (2001),
155--170, <https://doi.org/10.1007/s004930100016>.  The distinct host-graph
result is M. Chudnovsky, A. Scott, P. Seymour, and S. Spirkl,
*Erdos--Hajnal for graphs with no 5-hole*, PLMS 126 (2023), 997--1014,
<https://doi.org/10.1112/plms.12504>.  Its statement concerns `C5`-free hosts,
whereas the reviewed class contains `C5` and all of its lexicographic powers.

A bounded exact-phrase and structural search found no primary source stating
this exact constant-one product exponent for this recursively defined host
class.  That supports the target's cautious search-relative status sentence;
it does not establish historical priority.

## Strengthening and improvement opportunities

- State the induced-subgraph conclusion with a new letter `H` directly in
  the main contribution, as the follow-up clarification now does.
- The class definition plus recursive proof is self-contained; move the
  prime-quotient equivalence to a remark unless a full modular-decomposition
  formulation is needed downstream.
- A proof-assistant formalization of the eight short reductions would shrink
  the remaining trust boundary more effectively than enlarging the finite
  enumeration.
- It may be useful to characterize equality in (1), not only exhibit the
  iterated balanced `C5` family.  That is a genuine extension and is not
  required for the present theorem.

## Reproducibility and limits

Run `./run_checks.sh` in this directory with standard-library Python 3.11 or
later.  The checker uses exact integers and `Fraction` values and takes about
three seconds in the review environment.  It is an independent small-case
and reduction audit, not a formal proof of Chvatal's theorem, a machine proof
of the universal induction, or evidence of exhaustive bibliographic novelty.
