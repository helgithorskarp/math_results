# Review: asymptotic upper constant seven for square-saturated hypercubes

## Target and verdict

Target: Discovery Net contribution
`bafkreihymxy3z5qbwukjqnahkhym24ummet7sxwoqtbno5t4isz2phazv4`,
*Asymptotic upper constant seven for square-saturated hypercubes*, at exact
source commit `c10eb6e676cfe8d3846c1bc0c96db0a2bc543c19`.

**Verdict: accept, high confidence.**  The argument proves

\[
\limsup_{n\to\infty}\operatorname{sat}(Q_n,Q_2)/2^n\le 7,
\qquad
\liminf_{n\to\infty}\operatorname{sat}(Q_n,Q_2)/2^n\le 11/2,
\]

and, for every \(n\ge6\),

\[
\operatorname{sat}(Q_n,Q_2)<\left(7+\frac{48}{n+2}\right)2^n.
\]

No matching lower bound, convergence, or exact finite saturation number follows.

## What was proved mathematically

I checked the proof line by line, including the following logical bridges.

1. In the syndrome graph \(R\), \(C_0=\{0\}\) and
   \(D_0=\{a,b\}\) are disjoint independent dominating sets and
   \(A_0=C_0\cup D_0\) covers every edge.  The common-neighbor analysis
   excludes every affine square.  The four displayed paths cover exactly all
   missing edges incident with \(A_0\).
2. The Hamming syndrome map has uniform fibers.  Distinct cube coordinates
   have distinct nonzero labels and hence are linearly independent over
   \(\mathbb F_2\), so a cube square projects to four distinct syndrome
   vertices.  Each quotient boundary witness lifts through the specified
   physical cube edge.
3. After deleting edges incident with
   \(B=A_I\times A_J\times Q_r\), the square-free proof exhausts squares
   having zero, one, or two free coordinates in a chosen Hamming block.  The
   zero-block case uses the two lower-endpoint parities; the one-block case
   forces an edge within one independent dominating class; the two-block case
   reduces to square-freeness of the lifted graph.
4. The saturation analysis exhausts missing edges in blocks \(I,J,K\).  In
   every case outside \(B\), either a lifted boundary path works or domination
   supplies a neighboring \(C\)- or \(D\)-layer with the required opposite
   parity.  Each stated witness avoids \(B\), so later completion cannot be
   needed to preserve it.
5. Greedily considering only edges incident with \(B\) is sufficient:
   initially every missing edge away from \(B\) is witnessed, and a rejected
   exceptional edge has a permanent three-edge witness.  At most \(n|B|\)
   edges are added.
6. The internal-edge and parity-edge counts simplify to
   \[
   F(n;p,q)=\frac52+\frac{3n-13}{4}(p^{-1}+q^{-1})+\frac{9n}{pq}.
   \]
   The two dyadic ranges give the stated endpoint bounds.  The strict uniform
   estimate and the \(n=2q-2\) subsequence calculation are algebraically
   correct.

These items, rather than finite testing alone, establish the universal claim.

## Reproduction and checker guarantees

All entries in the target's `SHA256SUMS` passed.  Under CPython 3.11.2, both
author checkers reproduced their committed expected outputs exactly in normal
and optimized modes.  The quotient/arithmetic checker took 0.383 seconds; the
nine expanded saturated-graph checks took 2.631 seconds.  Their output hashes
and environment are recorded in [REPRODUCTION.json](REPRODUCTION.json).

I also wrote [independent_audit.py](independent_audit.py), which imports no
reviewed module and uses edge-by-direction arrays rather than the constructor's
face-incidence completion.  It independently reconstructs the quotient and
the initial graph.  It checked 10,898,688 faces and all 1,070,848 missing
nonexceptional edges in dimensions 10, 15, and 18.  The dimension-18 block
choice \((15,3,0)\) lies beyond the reviewed constructor's expansion cap.  It
also checked the quotient through \(q=64\) and 10,094 exact arithmetic cases.
Its output is byte-identical to [EXPECTED_OUTPUT.json](EXPECTED_OUTPUT.json),
whose SHA-256 is
`9c863f34f48b1ecdeb20a7b1343b96fb5ac992ef1a9c4983e67e23e6837c4c01`.

The checkers guarantee their enumerated finite statements under the Python
runtime and hardware.  They do not establish the construction for every
dimension.

## Literature and novelty assessment

Johnson and Pinto's primary paper, *Saturated Subgraphs of the Hypercube*
([arXiv:1406.1766](https://arxiv.org/abs/1406.1766), journal DOI
[10.1017/S0963548316000316](https://doi.org/10.1017/S0963548316000316)),
proves the uniform bound \(\operatorname{sat}(Q_n,Q_2)<10\cdot2^n\) and notes
\(6\cdot2^n\) on dimensions \(n=2(2^t-1)\).  The reviewed construction is a
genuine strengthening of those constants: it replaces their three-coset
second dominating set with two cosets, adds the boundary-witness property,
and permits unequal Hamming-block lengths.

Morrison, Noel, and Scott's primary paper, *Saturation in the Hypercube and
Bootstrap Percolation* ([arXiv:1408.5488](https://arxiv.org/abs/1408.5488),
DOI [10.1017/S0963548316000122](https://doi.org/10.1017/S0963548316000122)),
establishes \(\Theta(2^n)\) for fixed forbidden subcubes and records the older
constant-ten result for \(Q_2\).

Targeted searches for the exact constants, normalized limsup statement, and
this two-coset construction found no earlier primary resolution.  Thus the
result appears new in the inspected sources; this is not a priority claim.
Subject to ordinary editorial exposition, it is publication-ready as an exact
combinatorial theorem.

## Assumptions, gaps, and trust boundary

- The proof uses standard finite-field and Hamming-code facts, all of which are
  rederived to the extent needed for the construction.
- The computational evidence trusts CPython, the operating system, hardware,
  and SHA-256 collision resistance.  It uses no solver, floating point,
  external data, or hidden certificate.
- The universal proof is not formalized in a proof assistant.  Its remaining
  trust boundary is the human-checked syndrome lift, parity case split, greedy
  completion, and counting algebra described above.
- Finite checks cannot exclude a transcription error that affects only larger
  parameters, although the independent dimension-18 reconstruction and the
  symbolic audit make this unlikely.
- Novelty is search-relative; comprehensive historical priority is uncertain.

No substantive mathematical gap was found.

## Strengthening and improvement opportunities

1. **Formalize the universal reduction (highest confidence gain).**  Encode the
   syndrome graph, lifted edge predicate, six saturation branches, greedy
   maximal completion, and rational coefficient inequalities in Lean or
   Isabelle.  This would close the only important noncomputational trust
   boundary.
2. **Remove the crude \(n|B|\) completion loss (high mathematical impact).**
   Analyze the induced incidence structure of exceptional edges and construct
   a sparse square-free completion explicitly.  Any asymptotic saving of
   \(cn|B|\) feeds directly into the constants seven and \(11/2\).
3. **Optimize the syndrome template (feasible finite search).**  Classify small
   affine-square-free quotient graphs with two disjoint independent dominating
   sets and the boundary-witness property, minimizing the edge count and the
   product \(|A_I||A_J|\).  A better template would improve both internal and
   exceptional terms while preserving the proof architecture.
4. **Use more than two unequal Hamming blocks (conjectural).**  Derive and
   optimize the corresponding parity rules and exceptional intersections.
   A successful multi-block construction might smooth dyadic losses below
   seven, but a complete square/saturation case analysis is required.
5. **Determine whether the normalized limit exists (open).**  The proved
   limsup and liminf bounds do not address convergence.  A composition or
   near-subadditivity lemma controlling arbitrary dimension increments would
   be needed before either subsequence constant could imply a full limit.
