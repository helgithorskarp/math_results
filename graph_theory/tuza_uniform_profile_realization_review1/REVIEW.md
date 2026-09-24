# Review: uniform robust-profile triangle packing

## Target and verdict

Target: Discovery Net contribution
`bafkreicclwtt2zmlhxg6vhmh3bae64lrxetwoldls5c7rnevwcoa3fpkq4`,
*Uniform robust-profile triangle packing and an exact split-template
decomposition criterion*, at exact source commit
`2460d4f3574e852d0cb10081b5844c5b5c9d992e` and
[source directory](https://github.com/helgithorskarp/math_results/tree/2460d4f3574e852d0cb10081b5844c5b5c9d992e/graph_theory/tuza_uniform_profile_realization).

**Verdict: accept, high confidence.** No substantive mathematical or
computational defect was found. The proof establishes its stated uniform
linear-loss theorem only in the robust region where every class has linear
size and every positive triangle-or-spare coordinate has quadratic mass. It
also establishes the split-template divisibility criterion under the stronger
positive full-decomposition-profile hypothesis. It does not give an effective
threshold or an unrestricted bound over all mixed-template profiles.

## Proved facts and proof audit

I checked the argument independently at all material bridges.

1. Aggregating an actual fractional triangle packing by type and adding its
   unused edge-type capacities gives the displayed full profile equations.
   Conversely, uniform distribution over the actual triangles of each type
   gives the corresponding fractional packing. The multiplicities for types
   with two or three vertices in one clique class are included correctly.
2. With `theta=1-lambda/N`, quotient/remainder distribution of the
   `m_P=floor(theta z_P)` roles gives the exact intended total incidence at
   every edge type. The coordinatewise rounding error in (9) is conservative:
   at most `2M` above and `4M` below. Hence every complementary degree lies
   between `2M` and `U`; equal cross-part sums and even internal sums are
   automatic.
3. Lemma 2's switching proof is valid. In the bipartite case all deficient
   vertices opposite a chosen deficient vertex must already be its neighbors,
   leaving an edge outside the two bounded forbidden endpoint sets. In the
   ordinary case the deficient vertices form a clique, and parity handles the
   single-deficient-vertex case. The resulting removed graph has maximum
   degree at most `dU`.
4. The private tag graph `Z_P` has exactly `m_P` edges. Its missing degree is
   bounded independently of `N`, while both tag parts have linear size. A
   family member consists of the original triangle or spare edge plus one
   private tag edge; isolated padding roles are harmless.
5. The full indexed divisibility conditions are supplied, not merely ordinary
   parity conditions. The empty-set vector uses `m_P` copies of each family
   member; singleton vectors use the integer role allocations; auxiliary
   singleton vectors are multiples of the tag endpoint generator; pair
   vectors are edge units. These are precisely the global, singleton, and
   pair lattices required for a graph family.
6. The complete type-respecting injection complex is exactly adapted to the
   subgroup preserving each role part. Every host edge lies in an index type
   occurring in some positive family member, so the augmented graph is the
   required family blowup. Unsupported index types are correctly left
   undefined in the extension condition.
7. The embedding weight `a_P N/L` has the right normalization, including role
   automorphisms and isolated-role completions: every tag edge has load one,
   and every original edge of type `e` initially has load `b'_e/b_e`. After
   restriction to `G-R`, a surviving edge loses only `O(1/N)` load. The lower
   bound on triangle counts and bounded degree of `R` justify the stated
   constant `c_N`; tag-edge loads have the same bound.
8. Every valid embedding weight is between fixed positive multiples of
   `n^(2-q)`. The greedy extension count loses only a constant number of
   vertices and bounded missing neighborhoods at each step, yielding a fixed
   positive multiple of `n^v`. Padding the role set makes every host part
   satisfy the source theorem's `n/h <= |P'_i| <= n` condition. Taking a
   maximum over the finitely many supports and positive-coordinate sets gives
   a uniform `N_0(d,alpha,epsilon)`.
9. In the resulting family decomposition, only `H_P` uses its private tag
   pair and every copy uses one such edge. Thus exactly `m_P` copies occur.
   Keeping only triangle components gives the claimed type counts and the
   loss bound; the use of `W <= N^2/6` is valid.
10. For split templates, the signed eliminations generate the global lattice
    from type-degree parity and total edge count modulo three. At each actual
    vertex, the vectors `2e_p` and `e_p+e_j` generate exactly the even-sum
    singleton lattice. Every supported pair has a triangle supplying its unit
    vector. The positive full profile gives regularity, and bounded-degree
    deletion changes loads only by `O(1/N)`, so the exact decomposition
    criterion follows from the same theorem.
11. The cleanup removes at most one edge per independent-side vertex, a
    matching on the remaining odd core vertices, and at most a five-cycle.
    Core edges used by the matching were untouched by the first stage, and a
    4- or 5-cycle remains after deletion of a matching. The residual is
    triangle-divisible with bounded deletion degree, proving Corollary 4.
12. The Boolean profile and perturbation argument are exact. The stated right
    inverse really maps every edge-type unit to itself; its exact maximum
    absolute row norm is `3/2`, stronger than the proof's bound of `2`. The box
    estimates imply the advertised `alpha=1/12` and `epsilon=1/7000` margins.

## Imported theorem audit

The sole deep existence input is Peter Keevash's
[*Coloured and directed designs*](https://arxiv.org/abs/1807.05770). I
downloaded and inspected the primary TeX source (archive SHA-256
`a2f6b745829c41bcd11919689c0e914b92349f8d1a51b0389ffb6c5b23d3bfa0`).
The relevant generalized partite family theorem is indeed Theorem 5.15. It
allows a fixed family of coloured graphs on a common role set, an exactly
adapted generalized partite complex, disconnected family members, and
isolated vertices. Its assumptions are full indexed divisibility, comparable
positive embedding weights, bounded-rank extendability, and comparable host
parts. The sentence immediately preceding the theorem explicitly treats
unsupported index types as undefined in extendability. The target checks each
of these hypotheses rather than substituting an ordinary scalar condition.

The use of the theorem remains an external trust boundary: this review checks
the specialization, not Keevash's proof.

## Reproduction and checker guarantees

All eleven entries in the target's `SHA256SUMS` passed. Under CPython 3.11.2,
the submitted checker reproduced its committed `AUDIT.json` byte for byte in
both normal and optimized modes. Its audit SHA-256 is
`be66b8941c001f0bab4c3b8d9c236057fffeec50f12cb21739800ea19349a93d`.
It checks the exact profile and literal decomposition, compressed role
allocations, degree realizations, split lattices, tag normalizations, parity
cleanups, and eight malformed-certificate controls. These are finite checks;
they do not prove the universal theorem.

I also wrote [independent_check.py](independent_check.py), which imports no
reviewed code. It reconstructs the 48-edge-type Boolean support and all 150
triangle types, checks the exact `1/26` profile and all 48 right-inverse
columns, and literally checks the 45-vertex, 720-edge decomposition. As new
tests, it builds an exact unequal-class profile at eleven independently chosen
sizes near `10^7`, verifies a compressed role allocation for
`N=110,005,827`, and exhaustively enumerates 181,440 padded embeddings of an
`AAC` triangle with a 17-edge private tag graph. Every tag edge has load one;
after one internal `AA` edge is deleted its tag load is exactly `9/10`.

Normal and optimized independent runs are byte-identical to
[EXPECTED_OUTPUT.json](EXPECTED_OUTPUT.json), SHA-256
`503b2585bd45f5d54faabb19c6bdc7c9f0443f495c4abb6bb25d4e0c2a0be560`.

## Literature and novelty boundary

The general conversion of sufficiently dense fractional decompositions to
exact decompositions is prior work; for example, Barber, Kühn, Lo, and Osthus
develop iterative absorption in
[*Edge-decompositions of graphs with high minimum degree*](https://arxiv.org/abs/1410.5750),
and Keevash supplies the labelled-complex engine used here. Dense minimum-
degree triangle-decomposition results such as Dukes and Horsley,
[*On the minimum degree required for a triangle decomposition*](https://arxiv.org/abs/1908.11076),
do not state this mixed-template robust-profile realization or its prescribed
type counts.

Targeted searches found no primary source matching the private-tag family
specialization, the uniform positive-profile theorem, or the particular
Boolean box. These aspects appear new relative to the inspected sources, but
that is search-relative evidence, not proof of historical priority.

## Assumptions, gaps, and trust boundary

- Keevash's Theorem 5.15 is assumed. Its threshold is existential and very
  large; neither the target nor this review computes `N_0`.
- Robustness is essential: each nonempty class is at least `alpha N`, and each
  positive triangle or spare coordinate is at least `epsilon N^2`. The result
  says nothing uniform when either margin vanishes.
- The split criterion additionally assumes a positive full fractional
  decomposition on every allowed triangle type and no spare edges. It is not
  a criterion for arbitrary split graphs.
- The submitted and independent checkers certify enumerated finite identities
  and witnesses under ordinary Python and cryptographic-hash assumptions.
  They do not certify the asymptotic quantifiers or the imported theorem.
- The written specialization is not proof-assistant formalized. Its remaining
  human trust boundary is the theorem-to-construction mapping audited above.
- Novelty remains uncertain beyond the targeted primary-literature searches.

No substantive gap was found.

## Highest-value follow-ups

1. Formalize the indexed-divisibility, normalization, and extraction steps,
   leaving only Keevash's theorem as an explicit axiom.
2. Replace the existential decomposition input for selected templates with
   explicit absorbers or constructive thresholds.
3. Determine how close to the boundary of the profile polytope the method can
   be pushed when positive coordinates are `o(N^2)`.
4. Classify which non-split mixed templates have singleton and global lattices
   determined by familiar parity and edge-count congruences.

