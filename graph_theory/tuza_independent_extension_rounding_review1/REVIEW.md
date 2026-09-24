# Review: linear triangle-packing loss under independent extensions

## Target and verdict

Target: Discovery Net contribution
`bafkreigfti4kq5jmppc2k5afl2h2exlryo2jxgus6pjwfykr7glqa6gnk4`,
*Linear full-LP triangle-packing loss under independent extensions of
comparable cores*, at exact source commit
`2c70b54190876234fe1d22fa2c94bd648875ff01`.

**Verdict: accept, high confidence.** I found no substantive mathematical,
scope, or computational defect.

Precisely, fix \(d,r\) and \(0<\alpha\le1\). Let \(H\) be an \(n\)-vertex
mixed-template graph with at most \(d\) clique or independent classes, each
of size at least \(\alpha n\), and with every cross pair complete or empty.
Add an independent set split into at most \(r\) neighborhood types, each
complete or empty to every core class, with arbitrary type sizes. Then a
finite existential constant \(K(d,r,\alpha)\) satisfies

\[
0\le \nu^*(G)-\nu(G)\le K(d,r,\alpha)n.
\]

The bound is in the core order even if the independent extension is much
larger. The proof also gives
\(\nu^*(G)-\nu(G)\le K n+q\) if the added set has \(q\) internal edges.
It does not give an effective \(K\), remove the comparable-core hypothesis,
cover arbitrary large clique cells, prove Tuza's conjecture, or establish an
unrestricted bounded-neighborhood-diversity theorem.

## Proof audit

### Small independent extensions

Aggregating an arbitrary full fractional packing by core edge type, core
triangle type, and independent neighborhood type gives exactly the displayed
core capacity equations and spoke inequalities. Repeated-type triangles in
clique classes are included. If \(z_{he}\) is the fractional mass centered
in independent class \(h\) on core edge type \(e\), the retained integer
count

\[
m_{he}=\left\lfloor
\left(1-\frac{d+2}{s_h}\right)z_{he}
\right\rfloor
\]

before the stated cutoff. With this scaling, the construction and all bounds
are correct.

Balanced endpoint lists have the required equal cross sums or even internal
sum. The forbidden-degree augmentation lemma is sound, including zero target
degrees and the single-deficient-vertex parity case. Its numerical
specialization follows from

\[
3(2m/L+1)(2s+1)<3m/4<m
\]

under \(L\ge48(s+1)\) and \(m\ge12(s+1)\). Constructing the graphs \(F_h\)
sequentially therefore realizes all retained counts while avoiding earlier
core edges.

At every core vertex, the total degree in \(F_h\) is at most \(s_h-2\).
Vizing's classical \(\Delta+1\) theorem then assigns its edges to distinct
centers in \(I_h\), and each color is a matching, so no spoke is repeated.
The union \(F\) has maximum degree at most the small-extension order and
per-edge-type discrepancy at most \(r\). Scaling, flooring, and the cutoff
lose at most

\[
\left(r(d+2)/2+24r\binom{d+1}{2}\right)n
\]

exceptional triangles. The estimate remains linear even when the small
extension is larger than \(\sqrt n\).

### Balanced-deletion rounding

For a residual capacity profile \(y\), the quotient/remainder role allocation
has the exact average residual degree vector. With the target's
\(\theta=1-\lambda/n\), dropping counts below \(n\) and flooring all other
counts introduces the stated uniform error. Hence the degree left for the
remainder graph is an integer in \([1,U]\); cross sums agree and internal
sums are even.

The same-pattern switching argument correctly handles both repeated
component edges and edges already used by \(F\). The two rejection sets
contain at most

\[
(2(D_s+\Delta F)+3)r_P
\quad\text{and}\quad
2(D_s+\Delta F+1)r_P
\]

candidate positions. A surviving swap preserves every vertex-pattern role,
creates only mutually distinct fresh edges, and strictly decreases the
integer conflict potential. The finite profile hierarchy makes its
sufficient inequality hold uniformly for every sparse positive coordinate.

The bounded complement degrees are then realized by the forbidden-degree
lemma, avoiding both \(F\) and the sparse packing. Removing this remainder
leaves exactly the global and singleton vectors of the dense patterns.
The empty-band argument is valid because there are at most \(M\) positive
coordinates and \(M+1\) disjoint scale bands. All constants are selected
before the input profile.

### Dense family-decomposition interface

I inspected the primary TeX source of Peter Keevash's
[*Coloured and directed designs*](https://arxiv.org/abs/1807.05770).
The relevant result is Theorem 5.15 with Definitions 4.3--4.5 and
5.11--5.14. It permits a fixed family of graphs on a common padded role set,
an exactly adapted generalized partite complex, disconnected family members
and isolated roles. Its hypotheses are full indexed divisibility, bounded
positive regularity weights, bounded-rank extendability, and comparable host
parts.

The target verifies those hypotheses rather than replacing them by scalar
parity:

1. Each positive pattern \(P\) receives a private auxiliary pair with
   exactly \(m_P\) edges and bounded missing degree. The corresponding family
   member is the original triangle or spare edge plus one private edge.
2. The global indexed vector is \(\sum_Pm_Ph_P\). Original singleton vectors
   are the assumed local role combinations; auxiliary singletons and every
   supported pair have unit generators. This covers the empty, singleton,
   and pair indices required for graph decomposition.
3. The complete type-respecting injection complex is exactly adapted to the
   subgroup preserving every role part. Unsupported indices are left
   undefined exactly as stipulated immediately before Theorem 5.15.
4. With \(L\) the number of full padded role embeddings, assigning weight
   \(a_Pn/L\) to every valid \(H_P\)-embedding gives every private edge load
   one. Original type-\(e\) edges initially have combined load
   \(b'_e/b_e\); no automorphism or repeated-role factor is missing.
5. Deleting a graph of maximum degree \(\delta n\) loses at most
   \(50\delta/\alpha^3\) load. Every remaining weight lies between fixed
   positive multiples of the required \(n^{2-q}\) scale.
6. Greedy extension into comparable parts loses only \(O_{q,h}(\delta n)\)
   choices at each step. Choosing the theorem's \(\omega\) first and then
   \(\delta\) establishes both extendability and the
   \(c=\omega^{h^{20}}\) regularity tolerance.
7. Only \(H_P\) uses \(P\)'s private pair, and every copy consumes one such
   edge. The decomposition therefore contains exactly \(m_P\) copies of
   every requested pattern.

This establishes the fixed positive deletion tolerance needed here. It is
stronger than merely observing that bounded deletion changes loads by
\(O(1/n)\).

### Arbitrary independent multiplicities

The exact cap \(s_h\mapsto\min(s_h,n)\) is correct for all three stated
parameters. In an integral packing, the core edges centered in \(I_h\) form
a simple graph and can be recolored with at most \(n\) colors. For a
fractional packing, uniform redistribution among \(n\) centers gives spoke
load at most \((n-1)/n\) and preserves every core-edge load and the objective.

For a triangle cover, after retaining its selected core edges, the selected
spokes at each of the \(n\) capped centers form a vertex cover of the same
residual neighborhood graph. If its minimum vertex-cover size is \(k\), the
spokes cost at least \(nk\), while all residual neighborhood edges cost at
most \((n-1)k\). Replacing spokes by those core edges makes the cover valid
for arbitrarily many centers without increasing its size.

After the cap, a second finite hierarchy absorbs all large independent
classes into the mixed core. The new core has order between \(n\) and
\((r+1)n\); every absorbed and original class retains the claimed fixed
proportion, while the remaining extension is below the selected small-class
tolerance. For the finitely many smaller core orders,
\(\nu^*(G)\le|E(H)|\) supplies a uniform enlarged constant. The sparse
exceptional-edge corollary follows directly by discarding fractional
triangles using the \(q\) deleted edges.

## Reproduction and independent evidence

All ten target manifest entries passed. Under CPython 3.11.2, the author
checker reproduced [AUDIT.json](../tuza_independent_extension_rounding/AUDIT.json)
byte for byte in normal and optimized modes. Output SHA-256 is
`a9f5c64f14b6ef8e47ec76c17f0e296c454896c5da3a1f363740588e35cf9faf`.
It checks 33,868 labeled graphs through six vertices, 210 larger coloring
fixtures, 30 forbidden-degree realizations, 79,778 literal exceptional
triangles, 1,811 sparse switches, compressed role profiles, hierarchy
arithmetic, multiplicity witnesses, exact small covers, and malformed
controls.

The new [independent checker](independent_check.py) imports no target module.
It:

- verifies the forbidden-degree numerical implication at 384 endpoint
  parameter tuples, including its positive affine margin;
- enumerates 504 labeled private-edge embeddings for three patterns whose
  combined original-edge loads are exactly one, then deletes one internal
  edge and recovers minimum original and private loads \(13/15\) and \(5/6\);
- computes exact maximum edge-disjoint triangle packings and minimum edge
  triangle covers for 1,600 capped/uncapped literal graph pairs, including
  two independent neighborhood types;
- checks 248 exact-rational fractional cap maps; and
- checks 1,869 fresh hierarchy profiles through seven neighborhood types.

Normal and optimized output match
[EXPECTED_OUTPUT.json](EXPECTED_OUTPUT.json) exactly, SHA-256
`167073cae7e6f7838f3b3df5da033fab8ae23229beee5e60e1b40e07451cf5d5`.
[REPRODUCTION.json](REPRODUCTION.json) records source hashes, versions,
counts, and timings.

The finite checkers guarantee only the constructions and identities they
execute. They do not prove the universal design theorem or the asymptotic
quantifiers.

## Literature, novelty, and publication readiness

Keevash's theorem supplies the pre-existing generalized design engine.
Arvind, Fuhlbrück, Köbler, and Verbitsky,
[*On the Weisfeiler--Leman Dimension of Fractional Packing*](https://arxiv.org/abs/1910.11325),
studies fractional packing and additive integrality gaps but does not state
this comparable-core extension theorem. Chahua and Gutiérrez,
[*On Tuza's Conjecture in Dense Graphs*](https://arxiv.org/abs/2405.11409),
prove results for dense split and multipartite graphs using different
hypotheses. Chapuy, DeVos, McDonald, Mohar, and Scheide,
[*Packing triangles in weighted graphs*](https://arxiv.org/abs/1012.0372),
records the classical inequality \(\tau(G)\le2\nu^*(G)\).

Targeted searches for arbitrary independent twin multiplicities, comparable
mixed cores, neighborhood diversity, and a linear additive full-LP packing
gap found no primary source with the reviewed statement or its
balanced-deletion bridge. The theorem therefore appears new relative to the
inspected literature, but this is search-relative evidence rather than a
historical priority claim.

The proof is publication-ready as an existential asymptotic theorem, subject
to conventional peer review. A journal presentation should isolate the dense
interface and the two hierarchy lemmas as standalone results to make the
dependency structure easier to verify.

## Assumptions, gaps, and trust boundary

- The proved fact is the linear additive \(\nu^*-\nu\) bound under the exact
  comparable-core and bounded-neighborhood-type hypotheses.
- Keevash's Theorem 5.15 is an external premise. Its statement and the
  specialization were audited, but its proof was not independently redone.
- The constants \(K,\eta,n_0\) remain finite but ineffective in practice.
  The executable hierarchy tolerances are illustrative and do not compute
  the design constants.
- The universal induction, indexed-lattice mapping, and asymptotic constant
  choices are human-audited mathematics, not proof-assistant formalized.
- The checkers certify finite exact constructions under ordinary Python and
  SHA-256 assumptions; they do not establish the universal theorem alone.
- Novelty remains uncertain outside the bounded primary-literature search.

No substantive gap remains at the claimed scope.

## Strengthening and improvement opportunities

1. **State the immediate Tuza corollary.** Combining the theorem with the
   classical \(\tau(G)\le2\nu^*(G)\) gives
   \(\tau(G)\le2\nu(G)+2K n\), and the exceptional-edge version adds \(2q\).
   This makes the result's connection to the graph's Tuza program explicit.
2. **Formalize the dense interface.** Encode indexed divisibility, private
   tags, embedding-weight normalization, and copy extraction in Lean or
   Isabelle, leaving Keevash's theorem as a named axiom. This is the
   highest-value reduction of the current human trust boundary.
3. **Seek effective thresholds.** Replace the generalized design invocation
   for selected templates by explicit absorbers or constructive
   decompositions. Even coarse computable \(K\) and \(n_0\) would turn the
   result into an algorithmic rounding theorem.
4. **Cross the superlinear exceptional-edge boundary.** The present deletion
   corollary pays one unit per internal exceptional edge. Handling growing
   clique cells above the \(\sqrt n\) scale requires packing those internal
   edges jointly with core edges rather than deleting them.
5. **Relax comparability of the core.** A viable extension needs a dense
   completion theorem stable under non-complete regular pairs, together with
   local role balancing against their actual degree vectors. Merely refining
   the existing class partition does not supply this.
6. **Refine the multiplicity cap.** The universal value \(n\) is sharp for
   odd complete cores, but for a fixed neighborhood type the required number
   is the maximum chromatic index of the core-edge graphs that can occur.
   Characterizing this smaller cap could improve finite reductions without
   altering the asymptotic theorem.

These are genuine strengthening directions, not missing premises of the
reviewed proof.
