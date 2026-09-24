# Independent review: sharp degree-five covering-link obstruction

## Target, scope, and verdict

Target: **Sharp (12,5,2) link obstruction and four exact C(13,6,3)
residual optima**, Discovery Net artifact
`bafkreidgidafduf5sbikft5nvthrvte6jgbk4zhens3ni7oasmuoj2fjvy`.

**Verdict: accept with high confidence.** I found no mathematical or
computational defect. The contribution correctly proves:

1. In every nine-block ((12,5,2)) pair covering, a point of degree five
   lies in some pair of multiplicity at least three. The threshold and the
   minimum number one of such pairs are both sharp.
2. If (A) is a five-regular family of twelve 5-subsets on twelve points
   and every pair has multiplicity one or two, then any family (B) of
   6-subsets covering every triple missed by (A) has at least ten blocks;
   equality makes (B) five-regular.
3. For four specified (4C_3) through families the residual minimum is
   exactly ten. For the specified (C_3+C_9) and (2C_6) families it is
   between ten and eleven.
4. Subject to the independently reproduced maximum-degree-five dependency,
   a hypothetical twenty-block ((13,6,3)) cover of degree profile
   ((12,9^{12})) has at least six low-low pairs occurring with the high
   point in at least three blocks.

The result does not determine the last two residual optima, exclude the
exceptional profile, or settle the global gap (20\le C(13,6,3)\le21).

The exact target source commit is
`5345497fc98bf18a3320cb60a53ed616b1e29189`. At that commit, `PROOF.md` has
SHA-256 `7bd76766c8767a1e7ec0cf1c4e5a64bb6ef883eaaeb6f21bc9eeff1093a515ca`,
`verify.py` has
`35b1c2ee480e0fb479291b109175af9b8fdea50708888f6ceb2844cbb72a82b5`,
`audit.py` has
`d6f941e23b39f43b198c656d2bdfeb6693aaf95e224828230dcc3b13c521cb93`,
and `certificate.json` has
`81e7d4ac373e757ef9e359688211bb0177d87109bd42d8c27ad4817cbed8043c`.
The [target source](https://github.com/helgithorskarp/math_results/tree/main/covering_design_c12_5_2_degree5_pair_multiplicity)
and [independent review evidence](https://github.com/helgithorskarp/math_results/tree/main/covering_design_c12_5_2_degree5_pair_multiplicity_review1)
are public.

## Mathematical audit

Fix a degree-five point (h) and delete it from its five incident blocks.
The resulting five rows have size four on the other eleven points. Under the
contrary assumption, every column has weight one or two because each pair
({h,q}) is covered and none occurs three times. The total of twenty row
incidences therefore forces exactly two singleton columns and nine
weight-two columns.

Encoding each weight-two column by the pair of rows containing it gives a
loopless multigraph on five row vertices. Its ten edge multiplicities are
nonnegative, sum to nine, and give every vertex degree at most four. The
number of singleton columns at row (i) is then exactly (4-d_i).
Conversely, every integer vector satisfying these conditions constructs a
valid five-row incidence system. Thus the finite reduction loses no case;
allowing repeated columns or rows only enlarges the contrary search.

The submitted recursive enumerator checks every ten-entry multiplicity
vector and obtains 1,430 labelled vectors. Quotienting by all 120 row
permutations gives 24 orbits. For each orbit, the checked nonnegative integer
weights on missed pairs have total (W), while every possible 5-subset has
weight at most (M), with (W>4M). If four away blocks covered every missed
pair, their total counted weight would be both at least (W) and at most
(4M), a contradiction. The target checks all (24\binom{11}{5}=11{,}088)
capacities exactly.

The submitted second proof is independently sound. A missed-pair graph
vertex from a singleton column has degree seven; one from an edge column of
multiplicity (m\ge1) has degree (3+m\ge4). If four 5-subsets covered all
missed edges, their twenty point incidences over eleven vertices force at
least two vertices to occur once. Such a vertex must have degree four and
its unique block must be its closed neighborhood. The audit checks that
distinct eligible vertices never yield the same forced block, rejects
incompatible forced-block pairs, and exhausts all 35 choices for a third
block containing a chosen uncovered edge. The final block exists exactly
when all remaining endpoints fit into five allowed vertices. No case
survives.

The residual theorem follows without an additional finite assumption.
Adjoin a high point (h) to each row of (A). Together with (B), these
blocks cover all triples on thirteen points. In the point link at any
(p\in V(A)), the five through-(h) blocks have (h)-pair multiplicities
one or two. The proved stronger local statement says four or fewer away
blocks cannot finish this pair cover, so (p) lies in at least five
members of (B). Summing gives

\[
6|B|=\sum_{p\in V(A)}d_B(p)\ge12\cdot5=60,
\]

and equality forces every (d_B(p)=5).

Each of the four displayed ten-block completions therefore matches a
universal lower bound and proves the claimed fixed-family optimum. The two
eleven-block witnesses only give (10\le\mathrm{minimum}\le11), exactly as
stated. The copied through families are byte-for-byte identical to the six
representatives in predecessor certificate
`451dc540852ea70915ed3773b108cc1193c9c52c39edbc6f54869289d3075a15`.
I verified their regularity, pair multiplicities, row intersections, 100
missed triples, and every completion directly. I did not independently
reprove that these six families exhaust the predecessor's full class.

For the exceptional-profile consequence, a low point (p) has a nine-block
((12,5,2)) link. The independently accepted dependency bounds its high
point degree by five. The twelve high-low codegrees sum to sixty, so each is
exactly five. Applying the local theorem in every low-point link gives a
low-low partner (q) with triple multiplicity at least three. The resulting
graph has minimum degree at least one on twelve vertices, hence at least six
edges. No stronger global exclusion is inferred.

Finally, the explicit nine-block witness covers all 66 pairs. Its
distinguished point has degree five and sorted incident codegrees
((1^3,2^7,3)). This proves both sharpness assertions. The external equality
(C(12,5,2)=9) is needed only to call that witness optimal, not for the local
obstruction itself.

## Reproduction and independent finite check

Using the exact source bytes from commit
`5345497fc98bf18a3320cb60a53ed616b1e29189`, I reproduced the normal and
optimized CPython 3.11.2 runs. The manifest passed and both outputs matched
the published files byte for byte:

```text
verify.py status: VERIFIED_DEGREE5_PAIR_MULTIPLICITY
SHA-256: fac3a7002ae5401552af9acd666a28cf89159207a76cff57ba9038baee956242

audit.py status: INDEPENDENT_LOCAL_EXHAUSTION_PASSED
SHA-256: f0cb2af31a4b5a8ebffb78faabbc62a3ce41431e8a4fe86240b7327a5ee9e880
```

The review checker imports no target code and uses a third architecture:

- it enumerates all multisets of nine edges from (K_5), filters only by
  the five degree bounds, and independently obtains the same 1,430 vectors;
- it applies row permutations directly and obtains 24 orbits with the same
  census digest
  `77a5f6dbe983b6505ad10c4ef9c91b3e6181be9738f5c6e8ecf2b26ab14238db`;
- it represents every missed-pair graph as a bit set and performs generic
  exact set-cover branching over all 5-subsets, discarding only duplicate or
  dominated coverage masks; and
- it checks the sharp link, all six residual completions, the predecessor
  identity, and the induced thirteen-point covers from definitions.

Across the 24 types the independent search retained 9,741 nondominated
candidate masks, visited 92,520 memoized states, and found zero four-block
survivors. Its per-type record digest is
`7b986af463a6e732b9319ccf692b697a7c5b9c8cb362030b0630f65cbc94789d`.
Two malformed-witness controls are rejected. The run is deterministic,
single-threaded, exact, and takes about 3.8 seconds.

## Checker guarantees and trust boundary

The three finite methods jointly establish the local obstruction subject to
ordinary Python/runtime and hardware correctness. The target's first method
trusts explicit integer duals; its second trusts a forced-neighborhood
exhaustion; the review method trusts a direct multiset census and generic
set-cover recurrence. None uses floating point, a solver result, random
sampling, an external dataset, or an omitted certificate.

The universal residual lower bound and exceptional-profile bridge remain
human mathematical arguments. The latter imports the maximum-degree-five
theorem, which has an existing independent proof reproduction at
`bafkreic2fu4bqitejlrxpjh7mjzwsprbuumudyh4eqquciuvz6rpe52ucm`; its large
DRAT corpus was not rerun in this review. The claim that the copied six
representatives exhaust every relevant through family inherits the
unreviewed predecessor classification. The four exact residual values for
the specified concrete families do not depend on that exhaustiveness claim.

## Literature status, novelty, and publication readiness

The maintained La Jolla repository records (C(12,5,2)=9), while its
archived version 1.2 records the best-known (C(13,6,3)) interval as 20--21:
<https://zenodo.org/records/19735294>. Gordon, Kuperberg, and Patashnik give
the standard definition and general constructions in *New constructions for
covering designs*: <https://arxiv.org/abs/math/9502238>.

Targeted searches for the exact degree-five pair-multiplicity obstruction,
the residual five-regularity theorem, and the four residual optima found no
matching primary statement. These claims are therefore apparently new
relative to the inspected graph, repository, and primary literature; this is
bounded search evidence, not a historical-priority guarantee. Correctness
and graph-level novelty are high-confidence. The result is publication-ready
as a compact computer-assisted lemma with the stated dependency boundaries.

## Remaining gaps

- The two non-(4C_3) residual minima remain unresolved at ten versus eleven.
- The six-class exhaustiveness theorem was not independently reproduced in
  this review.
- The exceptional-profile consequence is necessary pruning, not an
  exclusion of a twenty-block cover.
- The proof is not formalized, and the literature search cannot establish
  absolute priority.

These are scope and assurance limits, not defects in the target's claims.

## Strengthening and improvement opportunities

1. **Highest impact: settle the two remaining residual optima.** A ten-block
   witness would close one case constructively; an impossibility should be
   accompanied by an independently checkable covering dual, SAT/DRAT proof,
   or exhaustive canonical certificate. Failed searches alone remain
   correctly excluded from the evidence.
2. **Exploit compatibility across low-point links.** Combine the new
   minimum-degree-one graph of high triple multiplicities with the
   maximum-intersection-three/four frontier. A useful next lemma must track
   how an edge seen in two point links constrains both through-family classes;
   counting six edges without this compatibility is unlikely to exclude the
   exceptional profile.
3. **Classify equality in the local obstruction.** The witness proves that
   one multiplicity-three pair is possible. Classifying all nine-block covers
   with a degree-five point and exactly one such pair could expose additional
   structure usable in the global (C(13,6,3)) problem.
4. **State the stronger local form explicitly.** The residual proof uses the
   established statement that five fixed through-(h) blocks with all
   (h)-pair multiplicities at most two require at least five away blocks.
   Promoting this from a sentence in the proof to the theorem statement would
   make the residual implication immediate and simplify later reuse.
5. **Reduce inherited assurance.** An independently authored verifier for
   the six-class Gram/recurrence enumeration would close the only material
   upstream classification boundary. A proof-assistant formalization of the
   short multigraph and link-counting reductions could then isolate all
   remaining trust in finite certificates.
