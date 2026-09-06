# H560's entire left-selector relation depends only on vertex 310

For the fixed exact H560 graph, **eight optional vertices can be erased without
changing four-colourability anywhere in its induced vertex family**. The full
72-state interface depends on just one of its nine left-side selectors:
vertex 310. All 512 selector masks are classified, allowing arbitrary
recolouring of the mandatory large block.

Consequently the target search in this support reduces from 68 to **60 optional
vertices**. The retained 552-vertex support is five-chromatic by the new
equivalence and the accepted H560 theorem. There is no new graph on at most
508 vertices, no closure of the remaining family, and no right-block search in
this pass.

## Complete relation

Use the exact graph, mandatory set `M` of size 492, optional set `U` of size 68,
and field separator from the
[72-state parent theorem](../hadwiger_nelson_heule560_separator/README.md).
The large block `L` has 374 mandatory vertices and nine optional vertices

```text
W = [310,510,512,513,520,521,523,524,535].
```

Its 19 mandatory interface vertices are

```text
Q = [0,333,334,335,336,337,338,339,340,341,342,343,344,
     466,467,468,469,470,471].
```

For `A subseteq W`, let `P_A` be the words on `Q`, normalized by first colour
occurrence in increasing host order, that extend to proper four-colourings of
`G[(M intersect L) union A]`. The parent proves the complete sets
`P_empty = P72` and `P_W = P20`, of sizes 72 and 20, with `P20 subset P72`.

**Theorem.** For every one of the 512 subsets `A` of `W`,

```text
P_A = P72   if 310 is absent from A;
P_A = P20   if 310 is present in A.
```

The two cases each have 256 masks. Across all `72 * 512 = 36,864` state-mask
pairs, 23,552 are extendible and 13,312 are not. The canonical truth stream
lists the 72 states in increasing word order; each row is 512 ASCII bits in
integer mask order followed by a newline. Its SHA-256 is

```text
1458e9587a41c25a713cc821be1591a09b44b9b1bd443f5f13fcfa0accfa4ab9
```

This theorem concerns arbitrary proper interior colourings, not a fixed
colouring or a Kempe-switch neighbourhood.

## Compact positive and negative boundaries

The new [certificate](certificate.json) has 33,910 bytes, SHA-256

```text
e3c01e8694b4e27afe22ea633a2acbc77dae5d4268a8d0da59d7ce83f42c3a42
```

For each of the 52 words in `P72 minus P20`, it supplies:

* A proper colouring of `G[L minus {310}]`, with 382 vertices and 1,944 edges,
  realizing that boundary word. This is the maximal positive mask `510`.
* The minimal forbidden mask `1`, namely `{310}`. Its impossibility with that
  particular boundary word is certified below.

Bits 0 through 8 correspond to `W` in its displayed order. The 20 full-block
states inherit their positive witnesses from the parent certificate, so their
rows need no new witness. All colour strings use the parent's increasing
383-vertex order, with a dot precisely at an omitted vertex.

Thus every state in `P72` extends when all eight vertices other than 310 are
present. On the other side, only the 20 states extend when 310 alone is
present. Monotonicity now proves the displayed theorem for every mask:
`P_(W minus {310}) = P72` and `P_{310} = P20` squeeze all intermediate sets.

The definition-level verifier also checks all 36,864 cases explicitly using
set containment. Each belongs to exactly one of the positive downward sets
and negative upward sets. It verifies all 52 minimal forbidden masks and all
52 maximal good masks. The positive witnesses account for 101,088 new edge
inequalities plus 39,040 inherited ones, totalling **140,128**.

The negative statements are **boundary-pinned failures**. The 375-vertex
large graph containing vertex 310 is four-colourable, with 20 permitted
boundary words; rejecting the other 52 words does not make that graph
five-chromatic.

## One combined UNSAT certificate

Use four one-hot colour variables for every vertex of `L`, including absent
optional vertices, and nine selector variables. For an edge `uv` and colour
`c`, add the inequality clause guarded by the negative selectors of whichever
endpoints are optional. Hence the inequality is active exactly when both
endpoints are retained. An absent vertex can receive an arbitrary colour, so
the unconditional one-hot constraints impose no extra restriction on a
retained graph.

For each of the 52 forbidden pairs `(boundary word, minimal mask)`, introduce
a case variable `z`. Require at least one case variable. Each case implies
the 19 prescribed boundary colours and inclusion of its forbidden optional
mask. No exclusion of other optional vertices is necessary: the negative
claim covers every larger mask as well.

This combined formula is satisfiable if and only if at least one claimed
negative boundary case has a proper colouring. In one direction choose a true
case and restrict a model to its mandatory and required vertices. In the
other direction extend a hypothetical case colouring by giving absent
vertices arbitrary colours, select exactly its mask, and set only its case
variable true. Thus no at-most-one constraint on cases is needed.

The formula has **1,593 variables and 11,530 clauses**. It is UNSAT, with a
23,787-byte checked DRAT trace:

| Artifact | SHA-256 |
| --- | --- |
| Combined CNF | `267fcb54c8d31ea634c2b91b014a7b6c2bedd6b179ea4ec0be24c16b4e1cbae6` |
| Executed DRAT | `a05c3e10903903f567927d8626d408e254d27a7d35d08699c6ffbd7d1ae94db7` |

Kissat returned UNSAT. The first drat-trim check and a second check against
independently reconstructed CNF bytes both returned exit 0 with the exact
line `s VERIFIED`. [proof_manifest.json](proof_manifest.json) records all
dimensions, hashes and native binary identities. The raw CNF, proof and logs
remain local; fresh proof generation is fast and supported by the verifier.

## Family equivalence and the 552-vertex corollary

Put

```text
D = [510,512,513,520,521,523,524,535],
G552 = G minus D.
```

The complete relation proves, for every `T subseteq U`,

```text
G[M union T] is four-colourable
    if and only if G[M union (T minus D)] is four-colourable.
```

Indeed deletion of `D` leaves both the right block and the presence of 310
unchanged, so the left relation is unchanged. The parent's gluing equivalence
then gives the assertion. Restoring vertices may recolour the large block;
this is not a claim that every fixed full-graph colouring extends unchanged.

For any induced vertex subset missing some vertex of `M`, the accepted
[mandatory-boundary theorem](../hadwiger_nelson_heule632_minimize/README.md)
already supplies four-colourability. Its erasure is also four-colourable by
restriction. Hence the erasure equivalence extends to **every induced vertex
subset of G**. We do not claim an analogous fixed-edge-set result for arbitrary
edge-deleted subgraphs.

The exact induced support `G552` has **552 vertices and 2,726 unit edges**.
If it were four-colourable, the erasure equivalence would colour G,
contradicting the accepted H560 lower bound. The inherited five-colouring is
checked on all 2,726 retained edges. Thus `chi(G552)=5` without a separate
candidate SAT query. The lower-bound corollary uses both the new equivalence
and the accepted parent theorem; it is not a claim of a fresh stand-alone
G552 UNSAT trace or of criticality.

The entire family has 256 equivalent choices of the erased vertices for
every choice of the remaining 60 optional vertices. Within this fixed support,
the existence of a five-chromatic graph on at most 508 vertices is therefore equivalent to a
non-four-colourable `G552[M union T]` with `|T| <= 16`. By monotonicity this can
be padded to `|T|=16`, giving

```text
C(60,16) = 149,608,375,854,525
```

canonical supports, instead of `C(68,16) = 1,469,568,786,235,308`. This is an
equivalent candidate domain, not an assertion that these supports remain
uncoloured by every other certificate. No new census of their colourability
was performed.

Writing `R_B` for the right-block relation on its 59 optional vertices, the
remaining target has two exact cases:

| Presence of 310 | Right optional budget | Necessary and sufficient failure condition | Exact-size canonical supports |
| --- | ---: | --- | ---: |
| Absent | at most 16 | `R_B intersect P72` is empty | `C(59,16) = 109,712,808,959,985` |
| Present | at most 15 | `R_B intersect P20` is empty | `C(59,15) = 39,895,566,894,540` |

## Reproduce and verification boundary

From the repository root, with Python 3.11 or later and a fresh output path:

```sh
python3 -B hadwiger_nelson_heule560_left_relation/verify.py \
  --prove --out /tmp/hn560-left-check \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim
```

This requires no PySAT or original search archive. It reconstructs the exact
geometry and combined CNF, verifies all positive witnesses and all state-mask
pairs, generates a fresh negative proof and checks it. The expected field
`new_negative_proof_verified` is true; compare substantive fields with
[expected.json](expected.json). An existing proof archive can instead be used
with `--archive /path/to/archive`. `--positives-only` leaves the new negative
claims unverified and is not a complete theorem reproduction.

The completeness of the parent's 72-state interface and the accepted H560
mandatory/lower-bound theorem are explicit imported premises. Their proof
regeneration commands remain in their linked packages. They are not silently
rerun here. The present checker independently reconstructs all 199,396 host
norm tests using sparse-radicand arithmetic, verifies the stated field split,
and checks every supplied new and inherited positive witness it uses.

To repeat the frozen monotone search, use python-sat 1.8.dev24 with Glucose 4.1:

```sh
python3 -B hadwiger_nelson_heule560_left_relation/build.py \
  --out /tmp/hn560-left-search \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim
```

[plan.json](plan.json) was frozen before any new native query. The search
selects an unclassified mask, propagates positive and negative containments,
and minimizes each failure by single-vertex removal. It makes no assumption
that the answer will depend on only one vertex. Every provisional negative
is discharged by the combined proof. The search used 520 oracle calls and
completed search plus proof in about 1.14 seconds, excluding input geometry;
the proof step took about 0.34 seconds. Limits were 20,000 calls, 300 search
seconds, and 200,000 conflicts/10 seconds per query. There was exactly one
fresh Kissat proof query, bounded by two million conflicts and 120 seconds.

The producer uses ordered XOR field multiplication and bitmask propagation.
The verifier imports no producer executable; it uses sparse-radicand norms,
direct set containment for all 36,864 cases, and its own CNF builder. Seven
mutated certificates are rejected. An optimized-Python structural audit
agrees with the normal report. [run_summary.json](run_summary.json) and
[validation.json](validation.json) give the precise execution and audit scope.

The trust boundary is pinned input data, exact Python arithmetic, independence
of the radical basis, the two imported parent theorems, the written monotonicity
and gluing arguments, and the DRAT checker. This is author-run algorithmic
verification, not external peer review or proof-assistant formalization.

## Campaign checkpoint

The complete left-selector phase is finished. No right-block computation,
new support search, separate G552 deletion sweep, or record claim has begun.
The next bounded milestone should assess an exact right-block selector
relation under the now-complete 20/72-state interface. It must preserve
unrestricted right-interior recolouring and produce a family-level decision
or a clearly delimited feasibility result. It should not revert to fixed
colouring templates or timed-out QBF configurations.

The teammate's [whole shared-midpoint closure](../hadwiger_nelson_shared_midpoint/README.md)
was inspected as durable coordination context and remains a separate geometric
direction. No background process or unfinished certificate remains.
