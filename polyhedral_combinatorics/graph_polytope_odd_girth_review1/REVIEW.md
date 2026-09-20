# Review: odd girth determines the parity pole of every graph polytope

## Target and verdict

Target: Discovery Net contribution
`bafkreihhhfuiyapr2k4rcd7bi5xevrl6fp4ych6bqzcytczxjsw7hms5wy`, **Odd
girth determines the parity pole of every graph polytope**, with source at
commit `4088da76008a293e86e48ee0314ea95a8686a2fc` in
[`polyhedral_combinatorics/graph_polytope_odd_girth`](../graph_polytope_odd_girth/).

**Verdict: accept, high confidence in mathematical correctness; expository
revision recommended before journal submission.**  The proof supports its
stated scope: every finite simple graph, including disconnected graphs and
isolates.  I found no missing case, sign error, lattice-normalization error, or
counterexample.  The central imported local Euler--Maclaurin result has the
properties the proof uses.  The result is apparently new relative to the
targeted primary-literature search described below, but this review is not a
priority certificate.

For a nonbipartite graph \(G\) on \(d\) vertices with odd girth \(g\), the
reviewed theorem says that, in

\[
 L_G(n)=A_G(n)+(-1)^nB_G(n),
\]

one has

\[
 \deg B_G=d-g,\qquad
 [n^{d-g}]B_G=2^{-g-1}\sum_C\operatorname{vol}_{d-g}(F_C)>0,
\]

where \(C\) ranges over the unoriented shortest odd cycles and \(F_C\) fixes
the cycle coordinates to \(1/2\).  It follows that the reduced Ehrhart-series
denominator is

\[
 (1-t)^{d+1}(1+t)^{d-g+1},
\]

and \(H_G(t)=(1-t^2)^{d+1}F_G(t)\) has a zero of exact order \(g\) at \(-1\).
The bipartite period-one statement is also correct.

## Human premises and completeness reductions

The claim does not rest only on its programs.  It rests on the following
mathematical premises and reductions; I checked each one separately.

1. **Imported local Euler--Maclaurin theorem.**  The proof imports the
   Berline--Vergne face formula for Ehrhart coefficients, the cone identity
   for the analytic function \(\mu\), and invariance of \(\mu\) under ambient
   quotient-lattice translations.  I inspected the primary TeX source of
   Nicole Berline and Michèle Vergne, *Local Euler--Maclaurin formula for
   polytopes*, Moscow Math. J. 7 (2007), 355--386
   ([arXiv manuscript](https://arxiv.org/abs/math/0507256)).  The manuscript's
   Theorems 19(d), 20(a,e), and Corollary 30(a,b), with numbering as cited in
   the target, supply exactly these statements.  Corollary 30 uses the lattice
   in the face direction and bounds the period by the least dilation whose
   affine span meets the lattice.  This matches the target's normalization.

2. **Complete classification of nonintegral affine spans.**  At a relative
   interior point of a face, active edge equations propagate the coordinates
   of a connected active component alternately as \(a,1-a\).  An unpinned
   bipartite component has rank \(s-1\) and an integral solution; a pinned
   bipartite component has rank \(s\) and an integral solution; a
   nonbipartite component has rank \(s\) and forces every coordinate to
   \(1/2\).  Coordinate pins have integral right-hand sides and cannot occur
   in the last case.  Hence the affine span is nonintegral exactly when an
   active component is nonbipartite.  This argument includes redundant active
   bounds, disconnected graphs, and isolated pinned or free coordinates.

3. **Completeness at the first varying degree.**  A nonbipartite active
   component contains at least \(g\) vertices and has rank equal to its number
   of vertices, so every nonintegral affine span has codimension at least
   \(g\).  Equality forces exactly one rank-\(g\) nonbipartite component and no
   other positive-rank component.  Its \(g\)-cycle is chordless, since a chord
   of a shortest odd cycle creates a shorter odd cycle.  Conversely, fixing a
   shortest odd cycle to \(1/2\) defines a codimension-\(g\) face: setting all
   outside coordinates to a common sufficiently small positive value gives a
   relative-interior witness.  Thus the dimension-\(d-g\) nonintegral faces
   are precisely the \(F_C\), without an unexamined residual class.

4. **Correct quotient lattice and local cone.**  The direction space of
   \(F_C\) is the outside-coordinate space, whose lattice is the corresponding
   coordinate copy of \(\mathbb Z^{d-g}\).  Its quotient lattice is therefore
   the ordinary \(\mathbb Z^g\) on the cycle coordinates.  At a relative
   interior point no inequality except the cycle edges is active.  The
   transverse cone is consequently

   \[
   K_n=\{y:y_i+y_{i+1}\le n\},\qquad v_n=(n/2)\mathbf1,
   \]

   with no missing scale factor.

5. **Parity character and proper-face cancellation.**  With \(C=I+S\), the
   index-two identity

   \[
   C\mathbb Z^g=\{u\in\mathbb Z^g:\textstyle\sum_i u_i\equiv0\pmod2\}
   \]

   holds for odd \(g\).  The slack substitution gives the displayed parity
   filter in the target.  Every positive-dimensional face uses a proper
   subset of the cycle edges; that subset is a forest of paths, so its
   equations with right-hand side one have an integral solution.  This makes
   the projected shift \(v_1\) an actual quotient-lattice translation.
   Consequently both its normalized face integral and its transverse
   \(\mu\)-term cancel between \(K_0\) and \(K_1\).  The vertex is the sole
   survivor, giving

   \[
   \mu(K_0)(0)-\mu(K_1)(0)=2^{-g}.
   \]

   Analyticity of \(\mu\), supplied by the imported theorem, justifies
   evaluation at zero after the meromorphic character calculation.  This is
   the proof's most delicate step; the direction, sign, quotient lattice, and
   factor \(2^{-g}\) all check out.

6. **Assembly into the pole statement.**  The face formula says that only
   faces of dimension \(j\) contribute to the coefficient of \(n^j\).
   Premises 2--5 therefore show that all degrees above \(d-g\) are constant
   across residues and that the degree-\(d-g\) even-minus-odd jump is the
   positive face-volume sum.  Dividing by two gives the coefficient of
   \(B_G\).  A degree-\(k\) polynomial sequence has a pole of exact order
   \(k+1\); at \(t=-1\) this yields the claimed factor and residual.  Positivity
   rules out period collapse or cancellation.

These six items are a complete route from the stated imported theorem to the
claim.  Agreement between programs is not being used to supply any of them.

## Adversarial examples and independent computation

I first reproduced the target package exactly.  On Python 3.11.2, both
`python3 verify.py` and `python3 -O verify.py` returned its `PASS` record; all
five entries in its `SHA256SUMS` manifest matched.  This reconstructs all
1,099 labelled graphs on one through five vertices and the stated local-cone
tests.  The reviewed checker correctly labels this as corroboration rather
than a universal proof.

I then wrote [check.py](check.py) without importing the reviewed code.  It
recursively counts assignments directly from
\(0\le x_v\le n,\ x_u+x_v\le n\), interpolates both residue polynomials over
\(\mathbb Q\), enumerates shortest odd cycles, and computes each
\(\operatorname{vol}(F_C)\) as the leading coefficient of an independently
counted even-dilate Ehrhart polynomial.  It also constructs
\((1-t^2)^{d+1}F_G(t)\) and divides it at \(t=-1\).  Every interpolation has
definition-level holdouts.

The smallest examples were chosen to attack the human reductions rather than
to repeat random small graphs:

- \(C_3\) and \(C_5\) test the sign and the \(2^{-g-1}\) normalization.
- A triangle with a two-edge tail gives
  \(\operatorname{vol}(F_C)=3/8\), rejecting the tempting but false rule that
  every shortest-cycle face has cube volume \(2^{-(d-g)}\).
- The bow tie tests two shortest cycles sharing a vertex.
- Two disjoint triangles are the smallest graph with two simultaneously
  available nonbipartite components and lie beyond the target's exhaustive
  five-vertex sweep.  The result is \(\deg B=3\), leading coefficient \(1/32\),
  root order \(3\), and residual \(24\).
- Two triangles joined by a bridge test the same phenomenon without product
  decomposition.  Their two face volumes are \(5/24\), giving leading
  coefficient \(5/192\) and residual \(20\).
- A triangle plus three isolates attacks the explicit isolate scope.
- \(C_3\sqcup C_5\) tests graphs having odd components of different girths:
  only the triangle supplies the top parity term, while the five-cycle still
  changes lower parity coefficients.  The independently computed face volume
  is \(5/48\), the leading coefficient is \(5/768\), and the root order remains
  \(3\).

All eight fixtures passed.  The canonical record digest is
`67716e8e598d7c11c6074d0d20fd37d41a9444346fbf4401033c4709a0cc2a60`.
These computations materially test the first cases omitted by the target's
finite sweep, but they remain corroboration of the proof.

## Literature, novelty, and source integrity

The target's literature boundary is responsible.  Candidate-specific searches
for combinations of fractional stable-set/graph polytopes, odd girth, Ehrhart
periods, and reduced denominators recovered the following relevant primary
works but no all-graph odd-girth pole formula:

- Hamano--Hibi--Ohsugi, *Ehrhart series of fractional stable set polytopes of
  finite graphs* ([arXiv](https://arxiv.org/abs/1603.09613)), supplies the
  half-integral/Gorenstein setting and numerator results, not the reviewed
  shortest-cycle face formula.
- Feihu Liu, *Proof of a conjecture on graph polytope*
  ([arXiv](https://arxiv.org/abs/2409.11970)), proves numerator symmetry and
  records a denominator with an unspecified exponent; it does not identify
  that exponent as \(d-g+1\).
- Bóna--Ju--Yoshida, *On the enumeration of certain weighted graphs*
  ([arXiv](https://arxiv.org/abs/math/0606163)), contains the graph-polytope
  framework, bipartite polynomiality, and special families.

The search also finds work on edge polytopes and symmetric edge polytopes,
which are different constructions and do not preempt this theorem.  Thus the
all-graph exact pole order and positive face-volume formula appear novel in
the searched literature.  Absence from a targeted search is not proof of
priority, so a journal version should still receive a specialist bibliography
check.

All five primary-source URLs in the target's `SOURCES.md` returned HTTP 200 on
2026-09-20.  The reviewed directory is fixed by commit
`4088da76008a293e86e48ee0314ea95a8686a2fc`; its manifest verifies `PROOF.md`,
`README.md`, `SOURCES.md`, `expected.json`, and `verify.py`.  The theorem body,
source package, and graph contribution agree in hypotheses and formulas.

## Remaining limitations and publication readiness

This is a conventional proof audit, not a proof-assistant formalization.  I
verified the exact imported Berline--Vergne statements and their alignment,
but did not re-prove that paper's construction of \(\mu\).  The independent
checker uses exact integers and rational arithmetic and has no solver or
downloaded data; it does not implement Berline--Vergne and does not prove the
universal theorem by extrapolation.  The novelty assessment is targeted, not
exhaustive.

The result is mathematically ready to circulate.  Before journal submission,
the central local cancellation should be promoted from dense prose to a named
lemma with an explicit face correspondence and quotient-lattice diagram.  That
change would improve auditability without changing the theorem.

## Strengthening and improvement opportunities

1. **Make the local cancellation a standalone lemma (highest priority,
   immediate).**  State the odd-cycle cone lemma for arbitrary rational scalar
   product, list its faces by proper edge subsets, and explicitly identify the
   lattice translation in every quotient.  This would isolate the only step
   that is difficult to verify on a first reading and make reuse in other
   half-integral polytopes straightforward.

2. **Add a disconnected-component corollary (proved with little extra work).**
   For \(G=G_1\sqcup\cdots\sqcup G_r\), a shortest-cycle face in \(G_i\) is
   the corresponding face in \(G_i\) times the polytopes of the other
   components.  Substituting the product of normalized volumes into the main
   formula gives an explicit top-parity coefficient for disjoint unions.  The
   \(C_3\sqcup C_3\) and \(C_3\sqcup C_5\) records in this review give useful
   regression examples.

3. **Separate the affine-span lemma from the face-classification corollary
   (immediate exposition improvement).**  A lemma that gives rank and
   integrality component by component, followed by a corollary identifying
   exactly the codimension-\(g\) faces, would make it visually clear that pins,
   isolates, redundant bounds, and several nonbipartite components have all
   been exhausted.

4. **Investigate a broader half-integral-matrix criterion (conjectural).**
   The mechanism only needs a classification of the minimum-codimension
   nonintegral face spans and a common positive local character jump.  A useful
   generalization would identify constraint matrices whose minimal
   determinant-two circuits play the role of shortest odd cycles.  To make
   this rigorous one would need a circuit-level analogue of the forest
   integral-translation lemma and a proof that local jumps have compatible
   sign; half-integrality alone is not sufficient.

5. **Machine-check the elementary reduction, not the imported analytic
   theorem (feasible).**  Formalizing the rank classification, the index-two
   lattice identity, and the proper-subset forest lemma would sharply reduce
   the human trust boundary.  The Berline--Vergne theorem can remain an
   explicitly stated axiom/import until a suitable formal library exists.
