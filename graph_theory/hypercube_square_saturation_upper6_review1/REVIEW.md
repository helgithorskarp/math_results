# Review: shortened syndrome templates and upper constant six

## Target and verdict

Target: Discovery Net contribution
`bafkreib2coyqjuo45hvsv3heeftor2rwcrrcigflsodh42lmi43npznqt4`,
*Finite syndrome certificates give asymptotic upper constant six for square
saturation*, at exact source commit
`e30f5a692b7c727e738784ffe073d62c77a3fb51` and
[source directory](https://github.com/helgithorskarp/math_results/tree/main/graph_theory/hypercube_square_saturation_shortened_templates).

**Verdict: accept, high confidence.**  No substantive mathematical or
computational defect was found.  The construction proves, for every integer
\(n\ge14\),

\[
 \operatorname{sat}(Q_n,Q_2)
 <\left(6+\frac{49}{n+2}\right)2^n,
 \qquad
 \limsup_{n\to\infty}\frac{\operatorname{sat}(Q_n,Q_2)}{2^n}\le6.
\]

It neither determines an exact saturation number nor proves convergence.  It
does not improve the previously proved \(11/2\) subsequence upper bound.

## What was proved mathematically

I checked the complete proof rather than inferring the universal theorem from
the finite computations.  The important logical bridges are as follows.

1. The five certificate conditions are sufficient.  In the replicated
   quotient on \(U\times W\), all noncore edges join a center in the zero
   layer to a nonzero layer.  Hence any noncore affine square would have
   opposite centers \((a,0),(b,0)\) and noncenters
   \((x,z),(x+a+b,z)\), exactly the rectangle excluded by condition 4.
   Condition 5 supplies the displayed three-edge witness for every missing
   allowed noncore boundary edge; condition 2 handles the core.
2. The coordinate-label set
   \((T\times W)\setminus\{0\}\) consists of distinct nonzero vectors and
   spans \(U\times W\).  The syndrome map is therefore surjective with
   uniform fibers.  Two distinct labels are linearly independent over
   \(\mathbb F_2\), so a cube square projects to four distinct vertices of an
   affine square.  Conversely, a quotient boundary witness with directions
   \(e,d,e\), where \(e\ne d\), lifts through the prescribed physical edge.
3. The replicated block parameters are exact:
   \[
   \ell=|T|m-1,\qquad
   h=\frac{r_0+(m-1)r_1}{qm},\qquad
   \delta=\frac{|A|}{qm}.
   \]
   The supplied H, S, and F data meet every certificate condition and give the
   three parameter rows used later.
4. The two-block composition remains square-free for unequal certified
   blocks.  If a putative face meets both center products, it contains an
   isolated exceptional vertex.  Otherwise, zero, one, or two free
   coordinates in the centered block reduce respectively to the two lower
   parities, independence of a center class, or square-freeness of the block.
   The symmetric cases exhaust all faces.
5. The saturation argument exhausts missing edges in the first block, second
   block, and padding coordinates.  Boundary witnesses handle edges incident
   with one block center; otherwise domination supplies a center of the class
   selected by the lower parity.  Every witness avoids
   \(B=A_I\times A_J\times Q_r\).  Greedy consideration of the remaining
   edges incident with \(B\) preserves square-freeness; a rejected edge has a
   permanent witness.  At most \(n|B|\) edges are added.
6. Counting the starting union with multiplicity and ignoring deletions is a
   valid upper bound.  Each lower parity contains exactly
   \(d2^{d-2}\) edges in a complementary \(d\)-cube, since both complementary
   dimensions are at least two.  This yields
   \[
   h_I+h_J+
   \frac{(n-i)\delta_I+(n-j)\delta_J}{4}
   +n\delta_I\delta_J.
   \]
7. With \(x=n+2\) and the unique power of two \(m\) satisfying
   \(16m\le x<32m\), every row of the six-interval table has nonnegative
   padding.  Its leading endpoint values are
   \(47/8,191/32,95/16,189/32,6,6\), and its completion endpoint values are
   \(729/16,375/8,363/8,45,49,48\).  Both relevant expressions increase
   within each interval.  The exact finite-scale inequalities
   \(h<h_\infty\), \(n-\ell<x-L\), and \(n<x\) make the final inequality
   strict.

These arguments establish the universal theorem.  The finite checkers below
are corroboration, not substitutes for the replication and composition
proofs.

## Reproduction and checker guarantees

All entries in the target's `SHA256SUMS` passed.  Under CPython 3.11.2, all
three submitted programs reproduced their committed expected outputs exactly
in normal and optimized modes.  Their output SHA-256 values are:

- finite templates:
  `1890253af0b579b77227ba9bae2ee0f345b6c1ff62dbca2b1d772f8df7ac5054`;
- replicated quotient and arithmetic audit:
  `276d0d11c176e675cf06878a3da2c7966829b534b2663631f6ee5f3214e46916`;
- expanded cube reproduction:
  `d20ae7f446cd39e4d6db384caadf1ac047c96069fb9749f3d5c0c090ef66a861`.

The submitted checkers verify the three explicit certificates, quotient
scales 1, 2, 4, and 8, 4,083 consecutive dimensions, 732 large dyadic endpoint
cases, and 12 completed cubes through dimension 18.  The expanded cases check
1,242,793 selected and 1,656,375 missing edges.  Six deliberately malformed
certificate or graph controls are rejected.

I also wrote [independent_audit.py](independent_audit.py), which imports no
reviewed module.  It hardcodes the proof's displayed templates and first
requires exact equality with the published JSON.  Its affine-plane
enumeration is separate from the submitted cycle checker.  It rebuilds all
three quotients at the previously untested scale 32, including the 512-vertex
F quotient, and independently verifies the exact parameter rule for every
dimension from 14 through 100,000.

The independent cube test uses a full two-face table instead of the submitted
length-three-path verifier.  It selects the theorem's dimension-19 case with
blocks H(2), S(4), and one padding coordinate, beyond the target's expansion
cap.  It checks all 22,413,312 faces before and after greedy completion.  The
final graph has 1,935,771 selected edges, no square, and a three-edge witness
for every one of its 3,044,965 missing edges.  Normal and optimized outputs
are byte-identical to [EXPECTED_OUTPUT.json](EXPECTED_OUTPUT.json), whose
SHA-256 is
`9ff6d54a5011454913d72a8cc408e12bf7ea41d1dfc55888df84921212c7153e`.

OR-Tools is absent from the review environment, so the optional discovery
search was not rerun.  This is not an evidentiary gap: solver soundness and
optimality are not used, and the explicit F certificate is checked directly.

## Literature and novelty assessment

Johnson and Pinto's primary paper,
[*Saturated Subgraphs of the
Hypercube*](https://arxiv.org/abs/1406.1766), proves the uniform bound
\(10\cdot2^n\) and records \(6\cdot2^n\) only on dimensions
\(n=2(2^t-1)\).  Morrison, Noel, and Scott's primary paper,
[*Saturation in the Hypercube and Bootstrap
Percolation*](https://arxiv.org/abs/1408.5488), establishes the
\(\Theta(2^n)\) scale for fixed forbidden subcubes but not this constant.

The accepted predecessor established uniform asymptotic coefficient seven
and subsequence coefficient \(11/2\).  The present replication lemma and the
S/F shortened blocks close the dyadic gaps sufficiently to make coefficient
six uniform.  Targeted searches for the exact bound, shortened syndrome
templates, and finite-certificate formulation found no earlier primary
result.  The theorem therefore appears new within the inspected sources, but
this is search-relative evidence rather than a historical priority claim.
Subject to ordinary exposition and external peer review, it is
publication-ready as a certificate-assisted exact combinatorial theorem.

## Assumptions, gaps, and trust boundary

- The only mathematical premises beyond elementary hypercube and binary
  linear-algebra facts are the three explicit finite certificates; each is
  directly checked.  No external classification or solver theorem is used.
- The universal replication, syndrome lift, parity composition, greedy
  completion, and interval optimization are ordinary human-audited arguments,
  not proof-assistant formalizations.
- The checkers guarantee their enumerated finite claims under the Python
  runtime, operating system, hardware, input normalization, and ordinary
  SHA-256 assumptions.  Finite verification alone cannot establish the
  universal quantifiers.
- The published F template was solver-discovered, but neither the solver's
  correctness nor any optimality/UNSAT assertion enters the proof.
- Novelty remains uncertain outside the bounded literature search.

No substantive gap was found.

## Strengthening and improvement opportunities

1. **Search for a uniform coefficient below six (highest impact).**  Treat a
   certificate as a point with parameters \((|T|,r_1/q,|A|/q)\), enumerate or
   optimize additional core/row systems, and solve the induced dyadic interval
   covering problem exactly.  Any claimed improvement still needs explicit
   finite certificates and a complete endpoint proof.
2. **Certify optimality within bounded template classes.**  Produce SAT or
   exhaustive certificates showing whether smaller H/S/F-style points exist
   for fixed \(|U|,|A|,|T|\).  Independently checkable UNSAT proofs would
   distinguish an ansatz barrier from a merely unsuccessful search.
3. **Formalize the universal bridge.**  Encode the finite certificate
   predicate, replication lemma, syndrome lift, three square cases, saturation
   cases, and rational endpoint inequalities in Lean or Isabelle.  This would
   leave only the finite JSON-to-definition import as a computational trust
   boundary.
4. **Reduce the finite remainder.**  Replace the crude \(n|B|\) completion
   allowance with an explicit sparse square-free completion or a tighter
   incidence count.  This would improve the `49/(n+2)` term even without
   changing the asymptotic coefficient.
5. **Develop a multi-block composition.**  Three or more certified blocks may
   smooth the dyadic envelope further, but requires a new parity assignment
   and a complete classification of mixed-coordinate faces; simply iterating
   the present two-block proof is not justified.
