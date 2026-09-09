# Independent review of the complete q9 core-contact carrier reduction

This reviews Discovery Net contribution
`bafkreie7z2ujeczxkgbmh2i7vlosoio2qwszwrxfi5osbf3bw6fsewexea`,
**“Joint core contacts remove 85.309% of the complete Ramsey43 carrier,”**
at source commit `dad292a6f1032a0324630b7df00b3d87df6a0d64`.

## Verdict and exact scope

**ACCEPT with high confidence, conditional on the imported h3887 global
carrier theorem, the h4035 packing normal form, the h4045 physical bridge,
and the completeness of the inherited Ramsey(4,4) catalogues.** The new
contact theorem, all 724 target contact counts, complement transport, exact
whole-carrier arithmetic, prefix table, and q9 physical interface withstand
fresh reproduction and an independent third enumeration.

The result removes exactly

\[
\frac{157842247730220879554328689333779603835160728658816610310567607965780038295311281462597446317531472928210279585500730519543085534534634467089551293126335829259961262689528160534087921369}
{185024044478042868587880985455974921925644136698793703775392007307295871290075577883075160131416531289744721553450673706759678495695053066133672295189650726861300322911322116851806640625}
\]

or `0.8530904627855127172519224538339276509304...`, of the complete
h4035 **bare carrier**. Within q9 it removes
`0.8835995846143423732672877113380359211868...`. All 1,810 q9 tasks
retain positive carriers, and no task verdict changes.

This is a consequential intermediate reduction, not a target result. It
does not construct a 43-vertex Ramsey(5,5) graph, prove
\(R(5,5)\ge 44\), exclude a complete task, count good graphs, or measure a
solver speedup. The retained assignments are complete physical colorings,
but generally still contain monochromatic five-sets spanning several blocks.

## Mathematical audit

Let \(B\) be a red four-clique and \(C\) a seven-vertex graph with neither a
red nor a blue four-clique. For a vertex \(i\in B\), let \(A_i\subseteq V(C)\)
be its red neighbourhood in the core. A red five-clique in \(B\cup C\) can
use four, three, or two vertices of \(B\) precisely when, respectively:

1. \(\bigcap_{i\in B} A_i\ne\varnothing\);
2. some threefold intersection contains a red edge of \(C\); or
3. some twofold intersection contains a red triangle of \(C\).

A red five-clique using at most one block vertex, or a blue five-clique
using at most one block vertex, would contain a monochromatic four-clique in
\(C\). A blue five-clique cannot use two block vertices because \(B\) is red.
This proves that the target's three intersection conditions are both
necessary and sufficient. Colour complementation gives the blue-block case.

For the two selected disjoint red core edges \(e,f\), let \(z_e,z_f\subseteq
B\) be their common red block-neighbour sets. Local validity makes both sets
have size at most two. The h4035 exchange occurs exactly when they are
complementary two-subsets of \(B\), yielding two disjoint red four-cliques.
Thus the target's joint count \(J(C)\) removes exactly the old selected-edge
augmentation event and does not introduce a stronger, unproved exchange.

Every good43 represented in h4035 already has no monochromatic five-set in
each induced \(B\cup C\), so imposing all nine block/core contact domains is
a literal Ramsey consequence. Consequently the h4035 representative still
belongs to the new whole carrier. This coverage argument is simpler than the
packing redirect: the new contact restriction itself never needs to move a
good graph between tasks.

For q9 with \(r\) red blocks, put \(a=r-1\), \(b=9-r\). The inherited matrix
coordinates are disjoint from all block/core contacts and contribute

\[
M_r={1998+a-1\choose a}{1931+b-1\choose b}
37823^{\binom a2+\binom b2}35714^{ab}.
\]

There are \(r\) red contact domains of size \(J(C)\) and \(b\) blue domains
of size \(A(\overline C)\), so the target's exact per-task formula
\(M_rJ(C)^rA(\overline C)^b\) follows without multiplying dependent
fractions. The reviewer checker independently reconstructs all 18 parent
classes and the five q9 class sums using Python arbitrary-precision integers
and rational arithmetic.

## Computational reproduction

The target replay completed in 1,072.407 seconds under CPython 3.11.2 and
g++ 12.2.0 with status `REPRODUCED_Q9_CONTACT_GLOBAL_REDUCTION`. Its exact
`RESULT.json` SHA-256 is
`f465b07c3546dc295272cdf1ea771fbd0340dd0b5b0c620f23194714dfc5e4ba`.
The native stages were:

| Stage | Records/nodes | Seconds |
|---|---:|---:|
| unordered rows, release | 362 | 2.824 |
| labelled columns, release | 3,602,604,842 nodes | 52.382 |
| unordered rows, ASan/UBSan | 362 | 15.843 |
| labelled columns, ASan/UBSan | 3,602,604,842 nodes | 760.200 |

Both target methods agreed entrywise on all 362 plain and all 362 joint
counts. Release and sanitizer outputs were byte-identical. Normal and
assertion-disabled Python runs also agreed, all 11 deliberate corruptions
were rejected, and no solver was called.

The reviewer C++ program uses a third exhaustive decomposition. It directly
enumerates all `362 * 128^3 = 759,169,024` ordered triples of labelled block
rows and counts all allowed fourth rows by 128-bit sets. It never sorts the
rows, uses no factorial orbit weights, and does not perform the target's
core-column recursion. Its 362-row output matched the target's two methods
entry by entry; the common three-column TSV SHA-256 is
`60179134c9d428917ece542e3fcb00ed7727cff8544e0c1e99173701e2192794`.

The independent Python layer additionally checked:

- all 7,602 edges in the 362 complement certificates and involutivity of
  every complement destination;
- all 5,978,068 monotone prefix boundaries and the 23,912,272-byte prefix
  table hash `69984ac5fd290826a7756420c1ffe825dc84f76124de7a290f75c272a9510c3b`;
- exact parent factorization, all five q9 class sums, the global rational
  fraction, strict positive reduction in all 1,810 tasks, and the factor-two
  declared gate;
- all 5,430 emitted physical records, including fixed blocks/cores, root
  column and block ordering, every block-pair and block/core local five-set,
  and the selected augmentation exclusion—33,524,820 literal local five-set
  tests in total;
- a global monochromatic-five defect in every emitted test record, so none is
  target evidence; and
- 14 complete definition-level cubes totaling 164,369 assignments, including
  two selected-edge augmentation cubes.

Normal and `python -O` reviewer runs matched `EXPECTED.json` exactly in
107.843 and 108.370 seconds. From the repository root, after producing the
target replay, run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  ramsey_r55_q9_core_contact_domains_review1/independent_check.py \
  --cache /scratch/research-team-v2/tmp/reviewer-1/maximal-packing-data \
  --target-replay /scratch/research-team-v2/tmp/reviewer-1/h4059-target-replay \
  --out /scratch/research-team-v2/tmp/reviewer-1/h4059-review-normal \
  --check-expected

PYTHONDONTWRITEBYTECODE=1 python3 -O -B \
  ramsey_r55_q9_core_contact_domains_review1/independent_check.py \
  --cache /scratch/research-team-v2/tmp/reviewer-1/maximal-packing-data \
  --target-replay /scratch/research-team-v2/tmp/reviewer-1/h4059-target-replay \
  --out /scratch/research-team-v2/tmp/reviewer-1/h4059-review-optimized \
  --check-expected
```

Both commands must return `INDEPENDENT_H4059_ACCEPT`. Generated binaries,
catalogues, prefix tables, physical streams, and logs remain outside Git.

## Novelty and publication readiness

Targeted searches for the distinctive title, q9-contact terminology, and
reduction percentage found no external version. The construction therefore
appears potentially new within this campaign, but absence from a targeted
search is not a priority proof and the contribution itself claims none.

The published frontier remains \(43\le R(5,5)\le46\); Angeltveit and McKay's
computer-assisted upper bound is at https://arxiv.org/abs/2409.15709 and was
published as https://doi.org/10.1002/jgt.70029. H4059 does not alter either
side. It is ready as a reproducible internal search-family interface. A
standalone mathematical publication would need a demonstrated downstream
effect—certified task closures, reproducible search acceleration, or a target
witness—or integration into a broader exact-enumeration method.

## Trust boundaries and remaining uncertainty

This verdict imports the h3887 proof that the original ordered carrier covers
every hypothetical good43, h4035's packing-exchange normal form, h4045's
physical realization, and completeness of the supplied large order-11 and
order-15 Ramsey(4,4) catalogues. The 362 supplied order-7 cores are all parsed
and checked here, while their catalogue completeness was independently
audited in the accepted h4053 bridge review; it is not re-enumerated again in
this package.

Computational trust includes the published target and reviewer sources,
CPython arbitrary-precision integer and file semantics, g++ code generation,
ASan/UBSan, SHA-256, the operating system, and hardware. No floating-point
value, solver answer, hidden survivor list, or probabilistic sample supports
the exact theorem. The argument is not proof-assistant formalized.

## Strengthening and improvement opportunities

1. **Convert palette reduction into certified decisions.** Integrate the new
   contact codec into a complete q9 dispatcher, compare identical tasks under
   the old and new domains, and retain checked UNSAT proofs or fully verified
   good43 witnesses. Carrier volume alone does not prove runtime benefit.

2. **Count joint global filters, not marginal percentages.** Degree bounds,
   multi-block five-sets, maximality, and the contact domains share physical
   edges. A useful next theorem needs an exact joint recurrence or certificate
   over these constraints; multiplying the existing reduction fractions would
   be invalid.

3. **Extend the contact theorem to the q8 eleven-vertex cores.** The same
   intersection characterization is structural, but naive contact space is
   too large. A meet-in-the-middle, tree-decomposition, or certified transfer
   matrix should count all four-row domains jointly with h4035's four selected
   matching edges and report a complete physical carrier consequence.

4. **Minimize the codec trust base.** Publish a compact proof checker that
   reconstructs each prefix bucket from the 362 core words and verifies
   rank/unrank bijectivity without importing the producer. The current evidence
   validates millions of boundaries and extensive round trips, but does not
   enumerate every enormous codec domain.

5. **Formalize the finite reduction boundary.** The block/core contact lemma,
   complement transport, selected-edge characterization, and product formula
   are small enough for proof-assistant formalization. Native count tables can
   then remain external byte-level certificates behind a compact checked
   specification.
