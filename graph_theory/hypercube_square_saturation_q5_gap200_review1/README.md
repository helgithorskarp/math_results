# Independent review and correction: parity-free Q5 gap 200

## Verdict

**ACCEPT, high confidence, with one non-substantive documentation correction.**
The source package at commit `e96e53a93b3bb6749cd27fd73ee327c575782a29`
supports the local theorem

```text
Delta_K >= 200
```

for every nonempty square-free edge set in `Q_5`.  Conditional on the stated
active-square identities and the published exact value `ex(Q_5,C_4)=56`, its
global consequence

```text
sat(Q_d,Q_2) >= 4998 d 2^d / (2747d+7249),  d >= 5,
```

and the asymptotic constant `4998/2747` also check out.

This review simultaneously **withdraws the finite-completeness acceptance in
the preceding gap-166 review**.  The older proof and review incorrectly
asserted that `Delta_K` is even and therefore omitted the total-161 case.  The
gap-200 package removes that parity filter, explicitly checks all 504
total-161 placements, and proves a stronger bound.  Thus the old numerical
gap 166 survives as a corollary of the corrected theorem, not by its published
completeness argument.

## Human premises and completeness reductions

The high-confidence verdict depends on the following explicit premises.

1. The written `Q_3` slack identity `sigma=b+2q-t/2` is the intended local
   quantity and is nonnegative for a square-saturated restriction.
2. Every square-free `Q_4` has at most 24 edges, and the previously proved
   sharp facet inequality `delta_H=17S_H-3E_H>=0` is valid.
3. A `Q_5` counterexample with `Delta_K<200` can therefore contain only
   `Q_4` facets with `S_H<=15`: from `E_H<=24`,
   `delta_H<200` implies `17S_H<272`.
4. The two target searches really enumerate every square-free `Q_4` pattern
   under that cutoff, not merely compatible examples.  Code inspection found
   exhaustive facet-state branching in one implementation and exhaustive
   global-edge branching with admissible minimum-cost pruning in the other.
5. The 327,553 labeled patterns compress to all 147 positive boundary
   profiles below 200 with no parity assumption.  The profile recursion may
   stop before ten positive facets because the smallest positive deficit is
   28, so ten already total at least 280.
6. The edge-incidence, live-facet-capacity, and bad-boundary conditions are
   necessary.  In particular, a nonextendable boundary cannot face a
   zero-deficit facet, and fixing one distinguished facet is complete because
   its stabilizer action induces all of `Aut(Q_4)`.
7. Each proof-critical deficit catalog (`0,28,42,48,71,99,124`) is a single
   `Aut(Q_4)` orbit with the claimed size.  Exact shared-boundary agreement of
   ten facet restrictions is sufficient to define a global `Q_5` edge set;
   square-freeness is then inherited by its facets.
8. The zero-total case is separately excluded: `17k=4E_K` forces `k=4` or
   `8`, while the exact live-facet capacities `1` and `28` are below the
   required `17` and `34` edges.
9. The passage from the local theorem to all dimensions uses the published
   `ex(Q_5,C_4)=56`, the stated subcube-incidence counts, and the two displayed
   active-square identities.  The reviewer checked the rational substitution
   and cross-multiplication but did not reprove that external extremal theorem.

## Adversarial checks

Agreement between the target programs was treated as evidence only after the
case-space reductions above were audited.

- A self-contained calculation enumerated every `Q_5` edge subset of sizes
  zero through three directly from the `Q_3` slack definition.  All subsets
  of size at most two have even deficit.  Exactly 320 three-edge subsets have
  odd deficit 831; the first is the three-edge square path
  `{0-1,0-2,1-3}`, with `2S_K=51`.  This is a smallest counterexample to the
  old parity premise.
- The target production verifier reproduced its committed output in 117.3 s.
  Its separate global-edge checker reproduced its committed output in 492.5
  s.  Both obtained 327,553 cutoff patterns, 147 positive profile classes,
  and normalized graph-set hash
  `665c9726162be1c86740870eca4fdbaabadf380785a2ee92efd094e8deeefd7b`.
- The reviewer checker imports neither target engine.  It regenerates the
  seven orbit catalogs from different representatives, recomputes their
  statistics and boundary signatures, derives all labeled placement counts
  from multiset multiplicities, and uses a generic exact-overlap gluer.  It
  excludes every one of the 2,430 placements across the thirteen residual
  totals, including 504 at total 161.
- The reviewer checker also verifies the live-facet capacity table and all
  rational global algebra, including the integer consequences 170 at `d=7`
  and 351 at `d=8`.

The reviewer checker is intentionally not advertised as a third complete
`Q_4` low-slack census.  Completeness of that census is supported by the two
audited target algorithms; the reviewer-owned program independently attacks
the proof-critical residual catalogs and closure.

## Caveat

The target README's exact-closure table lists the equality orbit with
`(E,b,e_0)=(17,0,0)`.  Direct recomputation from its representative gives
`(17,0,1)`: an equality pattern has one empty boundary.  The symbols `b,e_0`
were defined there only for positive-deficit patterns, and both target
programs special-case equality rather than use that table entry.  This is a
documentation inconsistency, not a theorem defect; the row should be labeled
"not applicable" or corrected to the representative's actual boundary data.

## Literature and scope

Primary context was refreshed on 2026-09-19.  Johnson--Pinto and
Morrison--Noel--Scott establish the surrounding hypercube-saturation problem
and its `Theta(2^d)` scale.  Dejter--Emamy-K--Guan supply the imported
five-cube extremal value, equivalently a 24-edge square hitting set and hence
`ex(Q_5,C_4)=80-24=56`.  Focused exact-phrase and constant searches found no
published `Delta_K>=200` theorem or `4998/2747` saturation constant.  That
supports the target's careful "apparently new relative to searched sources"
wording, not an unconditional historical-priority claim.

- [Johnson and Pinto, *Saturated Subgraphs of the Hypercube*](https://arxiv.org/abs/1406.1766)
- [Morrison, Noel, and Scott, *Saturation in the Hypercube and Bootstrap Percolation*](https://arxiv.org/abs/1408.5488)
- [Dejter, Emamy-K, and Guan, *On the fault tolerance in a 5-cube*](https://www.researchgate.net/publication/265697468_On_the_fault_tolerance_in_a_5-cube)

The review does not establish attainment of the local value 200, an exact
saturation number, or a formal proof independent of CPython semantics.

## Strengthening and improvement opportunities

1. Correct or mark inapplicable the equality row's `(b,e_0)` fields.
2. Export the complete 147-profile table and an independently checkable
   certificate tying every profile to the 327,553-pattern census.
3. Explain the shallow residual contradictions as short boundary lemmas;
   this could replace much of the final placement search with a readable
   proof.
4. Determine whether deficit 200 is attained.  If not, rerun the exact cutoff
   at the next justified threshold and report the true local minimum.
5. Formalize the finite reductions or provide proof certificates, and make
   the `ex(Q_5,C_4)=56` dependency locally reproducible.

## Reproduction

Python 3.11 or later and the standard library suffice.

```bash
cd graph_theory/hypercube_square_saturation_q5_gap200_review1
PYTHONDONTWRITEBYTECODE=1 python3 review_check.py > /tmp/q5-gap200-review.json
diff -u EXPECTED.json /tmp/q5-gap200-review.json
PYTHONDONTWRITEBYTECODE=1 python3 -O review_check.py > /tmp/q5-gap200-review-O.json
diff -u EXPECTED.json /tmp/q5-gap200-review-O.json
sha256sum -c SHA256SUMS
```

The reviewed target is
[`graph_theory/hypercube_square_saturation_q5_gap200`](https://github.com/helgithorskarp/math_results/tree/e96e53a93b3bb6749cd27fd73ee327c575782a29/graph_theory/hypercube_square_saturation_q5_gap200).
