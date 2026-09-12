# Final bidomination trial: the local-link route does not close good43

Campaign pass 39 **fails the final structural-feasibility gate**. The complete class of 43-vertex graphs with no clique or independent set of size five and domination number four in both colors remains unresolved. No original task or complete physical family is closed. The structural slot should be reassigned within R(5,5); this checkpoint does not authorize another pass in the trial.

The [previous pass](../ramsey_r55_bidomination_checkpoint) preserves the exact complete-class formula and its UNKNOWN run. That run was not restarted. This pass tested a structural way to avoid that unresolved computation: force a loss in local edge capacity from the common-neighbor requirements, then strengthen the argument with individual attachment incidences.

Both proposed shortcuts fail. All 453 published edge-extremal `(4,5)` graphs at orders 18 through 24 pass the pair-common-neighbor test. Seven bundled literal witnesses already suffice to show that none of the seven local edge ceilings decreases. Moreover, a general closed-neighborhood construction supplies individually valid attachment supports satisfying the root intersection conditions with arbitrary repetition. Their simultaneous physical realization is not certified. The missing mixed clique constraints are essential.

These are negative method diagnostics, not a new Ramsey bound or a feasibility theorem about good43. No Discovery Net mathematical claim is submitted for this pass.

## Exact evidence

With CPython 3.11.2 and its standard library:

```bash
python3 -B verify.py
```

This checks seven literal graphs, their lack of `K4` and `I5`, all pair common-neighbor conditions, every closed-neighborhood attachment support, and the 147 corresponding one-attachment physical graphs. It needs no external catalog. It also compares the output to `EXPECTED.json` and checks the public file manifest.

To repeat the optional entire top-edge census using McKay's external data:

```bash
python3 -B verify.py --catalog-tar /path/to/r45extreme.tar.gz --catalog24 /path/to/r45_24.g6
```

Both data files remain external. The second command verifies their expected hashes, extracts the six relevant tar members in memory, selects the two order-24 graphs with 132 edges, and checks all 453 records. It is not a census of all `(4,5)` graphs at orders 18 through 23. Completeness and optimality of those extremal catalogs are imported from the primary sources, not proved by this program.

See [METHOD.md](METHOD.md) for the precise failed implications, attachment lemma, residual obligation, and comparison with the other current campaign approaches. `WITNESSES.json` records exact graph6 strings and provenance; `CENSUS.json` records the optional census. These are same-author checks, not independent review.

## Primary sources and inherited state

- Angeltveit and McKay, [R(5,5) <= 46](https://arxiv.org/abs/2409.15709), especially Sections 1, 3 and the appendix, supplies the published frontier and extremal-neighborhood background.
- McKay's [Ramsey data page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html) supplies the extremal `(4,5)` data. Its order-42 collection is expressly incomplete and is not an endpoint premise.
- The repository was inspected at start through source commit `5320ed73129e0114fca9bdc2e57c43204e2d9fa1`, then through `f8e41ceed56853101677eb11afd1987699fe2611` at the boundary. R2's maximum-codegree cover has no new closure; R3's new source claims the edge window 392--511. R4's new order-45 cut inequalities retain a rational feasible relaxation point. None is a premise of this diagnostic, and no independent review of those packages is claimed here.
- The committed Discovery Net graph remained at height 4363 at pass start. All old pending transactions and prior source archives are preserved without resubmission.

The full principal report issued at 22:41:26 UTC was read at the boundary. It preserves the live final pass and explicitly recommends ending this structural assignment if the final complete-class gate is missed. That is the outcome recorded here.

The Ramsey range remains the published `43 <= R(5,5) <= 46`. Source publication is evidence preservation, not proof of the unresolved endpoint.
