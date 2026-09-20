# Review: simple bimodular polytopes have full Ehrhart period

## Target and verdict

Target: Discovery Net contribution
`bafkreihboua67mygd4hpxhywaenqv77rdugidlhjwfrfkztmveg4k3mtka`, **Simple
bimodular polytopes have full Ehrhart period via an index-two face
criterion**, with source at commit
`ed81f500715791fb735d58aea38d6a13e22d6bd3` in
[`polyhedral_combinatorics/bimodular_ehrhart_period`](../bimodular_ehrhart_period/).

**Verdict: accept, high confidence in mathematical correctness; minor
expository revision recommended.**  The proof supports both stated results:

1. the local index-two face criterion and its exact leading parity
   coefficient; and
2. the corollary that a simple polytope with an integral bimodular inequality
   description has minimal Ehrhart quasiperiod equal to its vertex
   denominator.

Here bimodular has the explicitly stated full-column-rank-minor meaning: all
full-size row minors have absolute value at most two.  Smaller minors and
entries need not be bounded by two, facet rows need not be primitive, and the
ambient lattice remains \(\mathbb Z^d\).  I found no hidden total-bimodularity
assumption, failure of the row-projection argument, missing quotient-lattice
factor, or counterexample.

For the local theorem, let \(2P\) be a lattice polytope, let \(g\) be the
least codimension of a nonempty face whose affine span misses the lattice,
and let \(M\) contain those codimension-\(g\) faces.  If each \(F\in M\) lies
in exactly \(g\) facets and its active integral map satisfies
\([\mathbb Z^g:A_F\mathbb Z^d]=2\), the reviewed theorem correctly gives

\[
 L_P(n)=A_P(n)+(-1)^nB_P(n),\qquad
 \deg B_P=d-g,
\]

\[
 [n^{d-g}]B_P=2^{-g-1}
   \sum_{F\in M}\operatorname{vol}_{d-g}(F)>0.
\]

Thus the minimal period is two and the reduced denominator is
\((1-t)^{d+1}(1+t)^{d-g+1}\), with the residual stated by the target.  The
search-relative novelty assessment is plausible, but this review is not a
historical-priority certificate.

## Human premises and completeness reductions

The universal verdict rests on the following mathematical steps, not on the
target or review programs.

1. **The description and lattice are fixed correctly.**  Actual facets are
   represented by integral rows, possibly nonprimitive.  Rescaling a row can
   change the image index, so the local criterion is properly stated relative
   to the chosen integral description.  Unimodular ambient transformations
   and integer translations preserve the relevant indices, normalized face
   volumes, and counts.  Removing redundant rows cannot increase a full-size
   minor, and it restores the geometric meaning of “exactly \(g\) facets.”

2. **The face-subset lemma is complete.**  At a codimension-\(q\) face in
   exactly \(q\) facets, the active normals are independent.  From a
   relative-interior point, surjectivity of the active linear map supplies a
   direction that has derivative zero on any selected active rows and
   derivative \(-1\) on the rest.  A small displacement leaves inactive
   inequalities slack.  Hence every selected subset cuts out a genuine face
   of codimension equal to its size, whose affine span is defined by exactly
   those equations.  This is precisely where local simplicity is used.

3. **Minimality forces full support of the parity character.**  An index-two
   subgroup \(\Lambda=A_F\mathbb Z^d\subset\mathbb Z^g\) is the kernel of a
   unique nonzero homomorphism
   \(\epsilon:\mathbb Z^g\to\mathbb Z/2\).  Since the affine span of \(F\)
   contains no lattice point, \(b_F\notin\Lambda\) and
   \(\epsilon b_F=1\).  If the support \(I\) of \(\epsilon\) were proper,
   then \((A_F)_Ix=(b_F)_I\) would have no integer solution.  Premise 2 would
   turn it into a nonintegral-affine face of codimension \(|I|<g\), contrary
   to minimality.  Therefore every coordinate of \(\epsilon\) is nonzero,
   so
   \[
      \Lambda=\{u\in\mathbb Z^g:\textstyle\sum_i u_i\equiv0\pmod2\},
      \qquad \sum_i(b_F)_i\equiv1\pmod2.
   \]
   This is a relation in the image lattice, not a real dependence among
   facet normals.

4. **All proper active subsystems are exhausted.**  Projection of the
   even-total-sum lattice onto any proper coordinate set is surjective.
   Consequently every proper active subsystem
   \((A_F)_Iz=(b_F)_I\) has a solution in \(\mathbb Z^d\).  This conclusion
   includes \(g=1\), where the only proper subsystem is empty.  It is exactly
   the bridge needed for all positive-dimensional cone faces; no unexamined
   proper row set remains.

5. **The transverse lattice is handled without a coordinate assumption.**
   With \(W=\ker A_F\), \(V=\mathbb R^d/W\), and
   \(L=\pi(\mathbb Z^d)\), the induced map \(C:V\to\mathbb R^g\) sends
   \(L\) bijectively onto \(\Lambda\).  In a basis of \(L\), \(C\) is an
   integral square matrix of determinant \(\pm2\).  Thus the transverse
   lattice is \(L\), not an unjustified coordinate \(\mathbb Z^g\), and
   the normalized face volume uses
   \(\ker A_F\cap\mathbb Z^d\), exactly as stated.

6. **The local parity jump has the right sign and magnitude.**  For
   \(K_n=\{y:Cy\le nb_F\}\), integer slacks are precisely the nonnegative
   vectors \(u\) satisfying \(\sum u_i\equiv n\pmod2\).  The resulting
   character filter splits the normalized exponential sum into unsigned and
   alternating products.  On every positive-dimensional cone face, Premise 4
   provides a lattice point \(z_I\) with the required proper equations;
   \(v-z_I\) lies in the face direction.  The even/odd shift is therefore a
   genuine quotient-lattice translation, so both the normalized face
   integral and its transverse Berline--Vergne \(\mu\)-term cancel.  Only the
   vertex remains, giving
   \[
      \mu(K_{\rm even})(0)-\mu(K_{\rm odd})(0)=2^{-g}>0.
   \]
   I rechecked the cited Berline--Vergne source alignment: its cone identity,
   lattice-translation invariance, polyhedral formula, and affine-span period
   bound are the exact imported properties.  A fixed rational scalar product
   and induced quotient lattices are retained throughout.

7. **The global coefficient and pole assembly is complete.**  Because
   \(2P\) is a lattice polytope, all coefficient periods divide two.  A face
   of dimension \(j\) contributes only to the coefficient of \(n^j\).
   Minimality of \(g\) makes all degrees above \(d-g\) residue-independent;
   in degree \(d-g\), exactly the faces in \(M\) can vary.  Summing Premise 6
   and halving the even-minus-odd difference proves the coefficient formula.
   Positivity precludes cancellation.  Standard polynomial generating
   functions then give the exact pole order, reduced denominator, and
   residual.

8. **Bimodularity really supplies every local arithmetic hypothesis.**  Any
   independent \(q\)-row submatrix \(D\) extends to a nonsingular
   \(d\)-row submatrix \(B\).  Coordinate projection induces a surjection
   \[
      \mathbb Z^d/B\mathbb Z^d\twoheadrightarrow
      \mathbb Z^q/D\mathbb Z^d,
   \]
   so the latter index divides \(|\det B|\in\{1,2\}\).  At a vertex,
   Cramer’s rule gives half-integrality.  At a minimum nonintegral face,
   index one would put its integral right side in the image, so its index is
   two.  Simplicity supplies the exact facet count.  This proves the
   corollary using only full-size minors, as claimed.

These steps close the case space.  In particular, agreement between two
programs is not being used to prove either the face reduction or the analytic
cancellation.

## Adversarial examples and independent computation

I first reproduced the target package.  On Python 3.11, both
`python3 verify.py` and `python3 -O verify.py` exactly reproduced its `PASS`
record, and all five manifest entries matched.  Its checks include thirteen
named polytopes, 52 interpolation holdouts, 39 literal enumeration
comparisons, thirteen rectangular image systems, 471 right-side tests, and
101 proper-subsystem tests.  Code inspection confirmed exact integer and
rational arithmetic and no imported solver or data.

I then wrote [check.py](check.py) without importing the target implementation.
It attacks three proof reductions separately.

**Projected image index.**  The checker exhausts all \(3\times3\) matrices
over \(\{-1,0,1,2\}\) having determinant \(\pm1\) or \(\pm2\).  There are
39,036 determinant-one and 51,510 determinant-two bases.  Across their
543,276 independent proper row subsets, every image index divides the basis
determinant; 85,320 subsets have index two.  This directly stresses the
surjection used in Premise 8, including nonprimitive rows.

**Full-support equivalence.**  The checker exhausts every \(2\times3\) and
\(3\times4\) matrix over \(\{-1,0,1\}\) whose image has index two, obtains
the unique annihilating mod-two character from the definition, and tests
every binary right side outside the image.  It verifies that the right side
is solvable on every proper row subset if and only if the character has full
support.  The audit covers 103,368 matrices, 413,328 outside right sides, and
2,892,720 proper-subsystem checks.  Partial-support characters occur in
85,248 of the \(3\times4\) matrices and always expose a smaller obstruction;
all 72,336 minimal outside right sides have full support.  These are the
adversarial cases most likely to invalidate Premises 3--4.

**An independent infinite structural family.**  For \(r\ge1\), let \(D_r\)
have rows \(e_1,\ldots,e_{r-1}\) and final row
\((1,\ldots,1,2)\), put \(b=e_r\), and define

\[
 P_r=\{x:0\le b-D_rx\le\mathbf1\}.
\]

This is a simple parallelepiped.  Its facet matrix \([D_r;-D_r]\) is
bimodular, \(\det D_r=2\), and
\(D_r\mathbb Z^r\) is the even-total-sum lattice.  Every proper row
projection is surjective.  Exactly \(2^{r-1}\) vertices are fractional.
The family lies outside the preceding primitive type-B theorem already at
\(r=1\) because of its nonprimitive row; for \(r\ge2\) it also uses a
coefficient of absolute value two.

For \(P_r\times[0,1]^f\), direct slack counting gives

\[
 L(n)=(n+1)^f
 \begin{cases}
   ((n+1)^r+1)/2,&n\text{ even},\\
   (n+1)^r/2,&n\text{ odd}.
 \end{cases}
\]

Hence \(B(n)=(n+1)^f/4\).  The minimum nonintegral faces have codimension
\(r\), number \(2^{r-1}\), and total normalized volume \(2^{r-1}\), so the
reviewed formula independently predicts the same leading coefficient
\(1/4\).  An ambient unimodular shear
\((x,w)\mapsto(x+w_1\mathbf1,w)\) makes the free-face direction
noncoordinate without changing the count or normalized volume.

All 28 cases with \(1\le r\le7\) and \(0\le f\le3\) have parity degree
\(f\), leading coefficient \(1/4\), root order \(r\), and residual
\(2^{r+f-1}f!\).  There are 56 definition-level interpolation holdouts and
16 literal counts from the original inequalities.  The full family-record
digest is
`f109799abd8832d6d1e1cf5201f357ae4f7f522b83041045129c3401b94f737e`.

The target’s two negative controls are also correctly scoped.  Stanley’s
nonsimple bimodular pyramid collapses, so simplicity cannot simply be
deleted.  The simple McAllister--Woods half-integral triangle collapses but
has active image index four, so half-integrality cannot replace the
index-two condition.  Both formulas were independently checked in the
precursor review and reproduced again by the target package.

## Literature, novelty, and source integrity

The primary-source boundary is accurate:

- Berline--Vergne, *Local Euler--Maclaurin formula for polytopes*
  ([arXiv](https://arxiv.org/abs/math/0507256)), supplies the analytic local
  formula and lattice behavior imported in Premises 6--7.
- Nägele--Santiago--Zenklusen, *Congruency-Constrained TU Problems Beyond the
  Bimodular Case* ([arXiv](https://arxiv.org/abs/2109.03148)), explicitly uses
  “bimodular” for full-rank matrices whose full-size subdeterminants are at
  most two.  It concerns integer-programming algorithms, not this Ehrhart
  noncollapse theorem.
- Gribanov--Zolotykh, *On lattice point counting in \(\Delta\)-modular
  polyhedra* ([arXiv](https://arxiv.org/abs/2010.05768)), computes Ehrhart
  coefficients under bounded-minor hypotheses and bounds their periods by an
  lcm of minors.  Its Corollary 2 does not assert exact period or exclude
  collapse for simple bimodular polytopes.
- Beck--Sam--Woods, *Maximal Periods of (Ehrhart) Quasi-Polynomials*
  ([arXiv](https://arxiv.org/abs/math/0702242)), proves exact maximal period
  for the second-leading coefficient.  This covers the \(g=1\) boundary but
  not the target’s higher-codimension criterion.
- McAllister--Woods, *The minimum period of the Ehrhart quasi-polynomial of a
  rational polytope* ([arXiv](https://arxiv.org/abs/math/0310255)), supplies
  the attributed collapse examples and does not imply the positive theorem.

Targeted live searches for combinations of bimodular or bounded-determinant
polytopes, simple rational polytopes, exact Ehrhart period, and index-two
images recovered these sources and general period-collapse literature, but
no matching local criterion or simple-bimodular theorem.  The new scope is
therefore apparently novel relative to the bounded search.  Absence from that
search is not proof of priority or absence from specialist folklore.

The graph contribution, theorem statement, full proof, source notes, checker,
and expected record agree on all hypotheses and formulas.  The target commit
and its manifest fix the exact materials reviewed.

## Remaining limitations and publication readiness

This is an unformalized proof audit.  I verified the cited Berline--Vergne
properties and their lattice normalization but did not re-prove the analytic
construction.  The exhaustive matrix sweeps are finite, and the 28 polytope
instances sample an exactly derived family; neither proves the universal
theorem by extrapolation.  The novelty assessment is bounded and should be
supplemented by specialist review before a priority claim.

The theorem is ready to circulate.  Before journal submission, the proof
would benefit from visibly separating the three algebraic maps
\(\mathbb Z^d\to\Lambda\subset\mathbb Z^g\),
\(\mathbb R^d\to V\), and \(C:V\to\mathbb R^g\), and from naming the
full-support lemma as the central new bridge.  Those are expository changes,
not repairs.

## Strengthening and improvement opportunities

1. **Develop the prime-index analogue (highest impact, genuinely new
   difficulty).**  For index \(p\), minimality similarly forces every
   coefficient of the unique mod-\(p\) character to be nonzero and makes
   proper projections surjective.  The missing step is an exact
   \(p\)-residue local cone calculation proving which Fourier components are
   nonzero and whether contributions from different faces can cancel.  The
   automatic positivity at index two should not be assumed for \(p>2\).

2. **Formulate a dual-code criterion for index \(2^s\) (high impact,
   conjectural).**  The annihilating characters form a binary code; the
   minimum support of a nonzero dual word predicts the first possible
   nonintegral face.  A rigorous extension would require a Walsh-character
   version of the cone cancellation and a sign/cancellation theorem.  The
   present index-two result is exactly the one-dimensional dual-code case.

3. **Turn the local theorem into a compact certificate format (feasible).**
   Record actual facet incidences, maximal-minor gcds for each leading face,
   augmented gcds proving nonmembership, normalized face volumes, and the
   minimum-codimension check.  A small verifier could validate this witness
   without trusting a general polyhedral package.  Complexity of finding the
   certificate should remain explicitly separate from checking it.

4. **Classify the first nonsimple bimodular failures (concrete finite
   project).**  Enumerate three-dimensional fractional vertices with four or
   more active bimodular facets, compute their local parity jumps, and
   determine when they vanish or reinforce.  Stanley’s pyramid supplies the
   first regression case; the goal should be a local classification, not the
   false assertion that simplicity is unnecessary.

5. **Formalize the elementary core (feasible confidence gain).**  The
   quotient-group surjection, full-support lemma, face-subset lemma, and
   proper-projection solvability are short algebraic statements suitable for
   a proof assistant.  Berline--Vergne can remain an explicit imported axiom,
   sharply isolating the analytic trust boundary.
