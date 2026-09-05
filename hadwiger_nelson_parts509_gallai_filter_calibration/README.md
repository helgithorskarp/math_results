# Gallai filtering retains all eighteen historical Parts residuals

**Exact finite calibration:** all eighteen specified, previously published
508-vertex residual supports pass the full low-degree Gallai condition.
Each is four-colourable, has selected-pool minimum degree at least four,
and meets all 17,250 distinct clauses in the common base colouring cover.
Their degree-four pool vertices induce forests with components of at most
three vertices. Consequently neither a full Gallai filter nor its
four-cycle/diamond subfilter removes any of these examples.

This is a limitation of that proposed filter on a fixed historical test
set. It does not prove the filter redundant on the entire family, close
the Parts pool, or establish a five-chromatic graph. These examples have
already received positive colourings and corresponding later cuts; they
are not claimed to survive the latest cover.

## Exact inputs and output

Use the committed strict unit graph on L union U, with L={0,...,373}
and the specified 303-element pool U=S union Q5. It has 677 distinct
points and 3400 exact unit edges, in Q(sqrt(3),sqrt(5),sqrt(11)) at common
denominator 288. For a selection X subset U, the low set is

    T(X) = {v in X : degree in H=L union X is exactly 4}.

Degrees include neighbours in both L and X. Fixed L vertices are not
members of T(X).

The eighteen supports, in report order, are:

- Index 0: `../hadwiger_nelson_parts509_pool_cover_residual30/certificate.json`.
- Indices 1 through 16: that package's `refinements.json`, in file order.
- Index 17: `../hadwiger_nelson_parts509_pool_cover_shrink01/postshrink_residual.json`.

Each row defines X=(S minus R) union A, of size 134. All eighteen X are
distinct and each includes points outside the closed H574 support.
The verifier rechecks their proper four-colourings on 43,125 selected-edge
incidences in total. It also rechecks all common base-clause intersections.
The base is precisely the union of the a=0,...,5, S-only, a=6 and a=7
families used in the residual30 package: 24,788 rows before equality
deduplication and 17,250 distinct clauses.

Across the eighteen low graphs there are 175 vertex occurrences and
17 edge occurrences. Their connected components are:

| Component | Occurrences |
|---|---:|
| Isolated vertex | 143 |
| Single edge | 13 |
| Path on three vertices | 2 |

Every block of such a forest is an edge or an isolated vertex, hence a
complete graph. These graphs satisfy the Gallai condition directly;
absence of small motifs alone is not used to infer it.

Separately, a complete census in the **whole 303-point pool graph** gives
2174 induced C4s and 798 induced diamonds (K4 minus one edge).
An opposite-pair enumerator and a canonical closed-walk enumerator agree
on the complete labelled sets. The sorted `kind:a,b,c,d` stream has SHA-256

```text
261608d60ae43d7bb282758521e4a5f8f65949aeac14d33cc460632d4682e297
```

This counts potential four-vertex blocks, not occurrences where all four
vertices have selected degree four. None lies entirely in T(X) for any
of the eighteen tested supports, as their full low graphs are forests.

## Reproduction

From the repository root, using Python 3.11 and the standard library:

```sh
python3 hadwiger_nelson_parts509_gallai_filter_calibration/verify.py
python3 hadwiger_nelson_parts509_gallai_filter_calibration/controls.py
```

The verifier ends with
`GALLAI FILTER REJECTS NONE OF THE 18 CERTIFIED HISTORICAL RESIDUALS`
and compares all reconstructed facts with `expected.json`. That file
contains every low vertex, edge and connected component, not just counts.
The control output is recorded in `controls_expected.json`.

Controls compare both motif enumerators with explicit graph isomorphism
to canonical C4 and diamond patterns on every labelled simple graph of
order four or five: 1088 graphs, 729 induced motif occurrences. Both
forest recognizers are compared with the separate criterion that every
nonempty induced subgraph has a vertex of degree at most one. The empty
forest is also checked. The two motif routes use different enumeration
and classification rules; geometry is shared, not independently rebuilt
by each of them.

Final validation took about 5.3 seconds with approximately 30 MiB peak
RSS. `final_validation.json` records the measurement and control results.
All geometry, witness and clause inputs are pinned in `manifest.json`.
No SAT solver, QBF configuration or proof trace was run in this pass.
No new colouring was generated, and no H574 deletion was audited.

## Method decision

The general reduction is classical: inclusion-minimal non-four-colourable
pool selections have degree at least four, and their degree-four pool
vertices induce a Gallai forest. [PROOF.md](PROOF.md) explains the
fixed-L application and exact finite checks. The source theorem is the
degree-choosability characterization, recalled by Cranston and Rabern in
[Beyond Degree Choosability](https://arxiv.org/abs/1511.00350).
No novelty is claimed for that theorem or its critical-graph consequence.

This was a bounded feasibility test before allocating a full guarded
encoding. Preliminary motif and forest probes preceded the frozen
verification plan; it was not a blind experiment. The observed rejection
rate is exactly 0/18 on this deliberately chosen historical test set,
not an estimate of a population rejection rate.

The result supplies no demonstrated gain for building a larger formula
from this guard alone. That implementation is not launched. A different
support or a mechanism sensitive to actual boundary colour constraints
would be a separate phase. The completed H574 closure, older pool cuts,
and paused QBF configurations retain their previous scope and status.
