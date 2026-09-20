# Review: local simplicity prevents type-B Ehrhart period collapse

## Target and verdict

Target: Discovery Net contribution
`bafkreiaxk3eprulq52djfudi5edrjdsi2ivczqk3zrzlrb62dpp76bhuoi`, **Local
facet simplicity prevents Ehrhart period collapse for type-B systems**, with
source at commit `0d9a87deb50bd95491d2904eae261a116b2ed50a` in
[`polyhedral_combinatorics/type_b_local_period`](../type_b_local_period/).

**Verdict: accept, high confidence in mathematical correctness; minor
expository strengthening recommended.**  The proof supports the precise
stated scope: bounded full-dimensional polytopes in the fixed lattice
\(\mathbb Z^d\), with irredundant primitive facet normals
\(\pm e_i\) or \(\pm e_i\pm e_j\), integral offsets after primitive
normalization, and the stated local facet condition.  I found no omitted
signed-cycle type, invalid face reduction, lattice-normalization error, or
counterexample.  In particular, unbalanced even cycles and two-edge cycles
are covered; the proof does not secretly require graph-polytope odd cycles.

If \(g\) is the minimum codimension of a nonempty face whose affine span
misses the lattice, \(k=d-g\), and every such codimension-\(g\) face lies in
exactly \(g\) facets, the reviewed theorem correctly gives

\[
 L_P(n)=A(n)+(-1)^nB(n),\qquad
 \deg B=k,\qquad
 [n^k]B=2^{-g-1}\sum_F\operatorname{vol}_k(F)>0.
\]

Consequently the minimal quasiperiod is two and the reduced series
denominator is
\((1-t)^{d+1}(1+t)^{d-g+1}\).  The stated residual at \(t=-1\), the simple
polytope corollary, and the inclusion of the earlier graph theorem also
follow.  The search-relative novelty assessment is plausible, but this
review is not a priority certificate.

## Human premises and completeness reductions

The verdict does not infer a universal result from finite agreement.  The
claim depends on the following premises and reductions, which I audited
individually.

1. **The signed active system is complete.**  On a spanning tree of an
   active connected component, every coordinate has the form
   \(s_i a+c_i\), with \(s_i\in\{\pm1\}\) and integral \(c_i\).  A pin fixes
   \(a\) integrally; a nontree edge is either redundant or fixes \(2a\) to
   an integer.  Feasibility excludes inconsistent equations.  Thus a
   component either admits an integral point or fixes all its coordinates to
   strict half-integers.  This exhausts unary pins, branches, parallel
   constraints, balanced cycles, unbalanced cycles of either parity, and
   unbalanced digons.  It proves vertex half-integrality and identifies a
   nonintegral affine span by an unbalanced active cycle with odd right-side
   sum.

2. **The local face-subset lemma is valid and does the necessary work.**  If
   a codimension-\(q\) face lies in exactly \(q\) facets, their normals are
   independent.  At a relative-interior point one may choose a direction
   with derivative zero on any selected subset and derivative negative on
   every other active facet.  For a sufficiently small displacement all
   inactive slacks remain positive.  Hence the selected facets cut out a
   genuine face of codimension equal to the subset size.  This conclusion
   would be false for a nonsimple face without the exact-facet hypothesis;
   the proof does not silently assume it there.

3. **The reduction to one whole unbalanced cycle is exhaustive.**  For a
   minimal nonintegral face \(F\) of codimension \(g\), choose an unbalanced
   cycle of length \(r\) among its active facets.  Premise 2 makes the
   intersection of just those cycle facets a nonintegral codimension-\(r\)
   face.  Minimality gives \(r\ge g\), while the cycle uses at most the
   \(g\) facets containing \(F\), so \(r=g\).  Therefore all active facets
   are exactly the cycle: no pin, branch, second component, or extra edge is
   left over.  The face directions are precisely the outside-coordinate
   subspace, so its lattice and transverse quotient are literal coordinate
   lattices.  This is the central completeness reduction, and it checks out.

4. **The signed-cycle lattice calculation includes every cycle type.**  An
   unbalanced signed \(r\)-cycle matrix \(C\) has determinant \(\pm2\) and
   image
   \[
     C\mathbb Z^r=\{u\in\mathbb Z^r:\textstyle\sum_i u_i\equiv0\pmod2\}.
   \]
   An odd sum of right sides therefore gives the strict half-integral
   translate.  Every proper subset of cycle equations is a forest and has an
   integral solution for arbitrary integral right sides.  This remains true
   for \(r=2\): the only proper nonempty subsets are single edges.  The proof
   neither needs \(r\) odd nor relies on converting the cycle into an
   unsigned graph cycle.

5. **The local Euler--Maclaurin cancellation uses the correct quotient
   lattice.**  The parity filter on nonnegative slack vectors produces the
   factor \(2^{-r}\).  For every positive-dimensional cone face, the
   integral solution to its proper subset of cycle equations makes the
   even/odd vertex shift an actual element of the corresponding quotient
   lattice.  Both the normalized face integral and the transverse
   Berline--Vergne \(\mu\)-term consequently cancel.  Only the vertex term
   survives, giving
   \(\mu(K_{\rm even})(0)-\mu(K_{\rm odd})(0)=2^{-r}\).  I checked the
   cited primary manuscript of Berline and Vergne: its cone face identity,
   ambient lattice-translation invariance, polyhedral formula, and
   affine-span period bound supply exactly the imported properties.  The
   target keeps one fixed rational scalar product and the induced quotient
   lattices, as required.

6. **The global assembly has no unaccounted coefficient.**  In the local
   formula, a face of dimension \(j\) contributes only to the coefficient of
   \(n^j\).  Minimality of \(g\) makes every degree above \(d-g\) constant
   between residues; Premises 3--5 give the positive even-minus-odd jump
   \(2^{-g}\sum_F\operatorname{vol}(F)\) in degree \(d-g\).  Dividing by two
   gives the displayed leading coefficient of \(B\).  The standard
   polynomial generating-function calculation then gives the exact pole and
   residual; positivity prevents cancellation.

7. **The advertised consequences preserve the hypotheses.**  A simple
   polytope satisfies the local facet condition at every face.  In this
   half-integral class a nonlattice polytope has vertex denominator two,
   whereas every face of a lattice polytope contains an integral vertex.
   For a graph polytope, a shortest odd-cycle face has exactly its cycle-edge
   facets active at a suitable relative-interior point, so the prior all-graph
   theorem is genuinely included even when the entire polytope is not simple.

Together these premises close the claimed case space.  The two irreplaceable
ingredients are the exact local facet count in Premises 2--3 and the
type-B signed-graph form in Premises 1 and 4.

## Adversarial examples and independent computation

I reproduced the reviewed package first.  On Python 3.11, `python3 verify.py`
and `python3 -O verify.py` both returned its expected `PASS` record, and all
five entries in its `SHA256SUMS` manifest matched.  This includes 64
full-dimensional planar systems, seven named higher-dimensional fixtures,
30 signed-cycle matrices of orders two through five, 18,720 slack-parity
cases, and 9,020 proper-face affine checks.

I then wrote [check.py](check.py) independently, importing neither code nor
expected data from the target.  For each \(r\ge2\), it uses the bounded
type-B polytope

\[
 P_r=\{x\in[-1,1]^r:x_0+x_1\le1,\quad
 x_1\le x_2\le\cdots\le x_{r-1}\le x_0\}.
\]

Its relevant face is the point \((1/2,\ldots,1/2)\), cut out by an
unbalanced cycle of rank \(r\).  Products \(P_r\times[0,1]^f\) make the
minimal nonintegral face have dimension \(f\) and normalized volume one.
The implementation counts dilates directly by

\[
 (n+1)^f\sum_{x_0=-n}^{n}
 \sum_{x_1=-n}^{\min(x_0,n-x_0)}
 {x_0-x_1+r-2\choose r-2},
\]

then interpolates the even and odd polynomials exactly over \(\mathbb Q\).
It independently constructs the numerator at \(-1\); two unused dilation
values per family test the interpolation against the defining sum.

All 24 families with \(2\le r\le7\) and \(0\le f\le3\) satisfy

\[
 \deg B=f,\qquad [n^f]B=2^{-r-1},\qquad
 \operatorname{ord}_{t=-1}H=r,qquad
 [H/(1+t)^r]_{t=-1}=2^f f!.
\]

Literal tuple enumeration also agrees with the summation in all 16 cases
\(2\le r\le5\), \(0\le n\le3\).  Thus the smallest digon, odd cycle, and
even unbalanced cycle cases are all exercised.  The full family-record digest
is `ed1e8ec099837f05d0e14fa9863f320d387979ab59c1dd2b4e9b0c2f3a0bda88`.

Two smallest boundary examples guard against overgeneralizing the result:

- The nonsimple type-B polytope
  \(\{x\ge0, x\le y\le1-x, x\le z\le1-x\}\) has a denominator-two apex
  in four facets and Ehrhart polynomial \({n+3\choose3}\).  Exact counts for
  \(0\le n<18\) reproduce the collapse.  This attacks deletion of the local
  facet condition.
- The McAllister--Woods triangle
  \(\operatorname{conv}((0,0),(1,1/2),(2,0))\) is simple, denominator two,
  and has Ehrhart polynomial \({n+2\choose2}\).  Exact counts for the same 18
  dilations reproduce the collapse, but its primitive facet normals include
  a coefficient of absolute value two.  This attacks deletion of the type-B
  normal restriction without contradicting the corollary.

These checks materially test the proof's fragile reductions.  They remain
finite corroboration, not substitutes for the seven human premises above.

## Literature, novelty, and source integrity

The relevant primary sources align with the target's account:

- Berline--Vergne, *Local Euler--Maclaurin formula for polytopes*
  ([arXiv](https://arxiv.org/abs/math/0507256)), supplies the precise analytic
  local formula and lattice behavior imported by Premise 5.
- Payne, *Lattice polytopes cut out by root systems and the Koszul property*
  ([arXiv](https://arxiv.org/abs/0805.1252)), records the standard type-B root
  vectors in \(\mathbb Z^d\).  Its main lattice-polytope results do not imply
  this theorem about nonintegral polytopes.
- McAllister--Woods, *The minimum period of the Ehrhart quasi-polynomial of a
  rational polytope* ([author manuscript](https://www2.oberlin.edu/faculty/kwoods/research/ep.pdf)),
  records Stanley's collapsing pyramid and also shows why a dimension-two
  boundary cannot be claimed without restricting the normals.

Targeted live searches combining simple or half-integral polytopes, Ehrhart
period collapse, signed constraints, and type-B root facets found these and
other general period-collapse results, but no matching local-facet criterion
or simple type-B full-period theorem.  The criterion therefore appears new
relative to the searched literature.  This is a bounded novelty check, not a
claim of exhaustive priority or absence from specialist folklore.

The reviewed theorem, proof, source notes, checker, and graph statement agree
on the normal set, fixed lattice, primitive integral-offset convention, local
condition, formulas, and limitations.  The target commit and its manifest fix
the exact materials reviewed.

## Remaining limitations and publication readiness

This is an unformalized proof audit.  I verified the cited properties and
normalizations of the Berline--Vergne input but did not re-prove its analytic
construction.  My checker covers an infinite structural pattern through 24
finite parameter choices, not all type-B polytopes.  The target's broader
finite fixture suite is independently implemented from mine, but agreement
between the two programs is only supporting evidence.

The theorem is ready to circulate as a mathematically substantive sufficient
criterion.  A journal version should retain the sharp wording that it is not
a classification beyond the local condition and should receive a specialist
bibliographic check before making a priority claim.

## Strengthening and improvement opportunities

1. **Promote the face-subset reduction to a named lemma (immediate and high
   value).**  State explicitly that the selected active facets cut out a face
   of the asserted codimension and that inactive inequalities remain slack.
   Then give the two-line inequality \(g\le r\le g\) as a separate corollary.
   This is the logical hinge of the theorem and deserves the same visibility
   as the signed-cycle cone lemma.

2. **Formulate the determinant-two circuit extension (substantive next
   theorem).**  The present proof suggests a broader class of integral
   matrices in which every minimum nonintegral active subsystem is one
   determinant-two circuit, every proper circuit subsystem has an integral
   affine solution, and the local face is simple.  Proving that these
   hypotheses suffice would separate the real mechanism from type-B graph
   notation.  One must retain the quotient-lattice calculation; mere
   half-integrality is demonstrably insufficient.

3. **Classify the first nonsimple obstruction rather than deleting the
   hypothesis (concrete but harder).**  In dimension three, enumerate local
   type-B normal configurations at a fractional vertex with more than three
   facets and compute their local parity jumps.  This could distinguish which
   nonsimple arrangements collapse, reinforce, or cancel, with Stanley's
   pyramid as the first regression case.

4. **Give an effective signed-graph certificate (feasible).**  From an
   irredundant facet list, output the minimum nonintegral codimension, the
   relevant unbalanced cycles, and either the exact local-simple certificate
   or a smallest violating face.  This would turn the theorem into a directly
   checkable criterion without treating vertex enumeration as part of the
   proof.

5. **Formalize the elementary core (feasible confidence gain).**  The active
   signed-graph classification, determinant/image calculation, face-subset
   lemma, and forest translation argument are finite algebraic statements
   well suited to a proof assistant.  The Berline--Vergne theorem can remain
   an explicit imported axiom, sharply locating the analytic trust boundary.
