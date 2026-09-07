# Exact HN exclusions: consolidated scope and evidence

This package consolidates three reusable structural obstructions, six exact
construction or fixed-host closures, and three completed discovery pilots.
It includes a classical seven-point example that makes two important scope
limits executable. **No new candidate search, negative-family census, or
record improvement is claimed.**

Read [SYNTHESIS.md](SYNTHESIS.md) for precise hypotheses, consequences, proof
mechanisms, the scope example, and the remaining positive-signal gate.
[registry.json](registry.json) pins the mathematical source references,
principal proofs, published manifests, review documents and applicability
limits for all twelve entries. This is a selected consolidation of strong
results, not a complete bibliography or inventory of the campaign.

The strongest reusable statements are:

| Verified hypothesis | Consequence |
|---|---|
| Physical conjugation acts inertially at a finite place of an embedded number field | Every unit-distance graph in a similar subset is at most three-colourable; at residue characteristic two, at most two-colourable |
| The entire proposed edge graph is a finite abelian Cayley graph with an injective plane unit-distance drawing | It is a Cartesian product of cycles/segments on each component, and has chromatic number at most three |
| Points lie in two unit triangular lattices sharing a vertex | Their entire strict unit-distance graph is four-colourable, for every relative angle |

Each rule requires its stated hypotheses. Failure to trigger a rule is an
unresolved case, not evidence that five colours are necessary.

## What this consolidation checks

The source-identity audit checks 127 historical manifest entries and pins
144 distinct files in total, including five acceptance-review documents.
It does **not** rerun or independently review the historical theorems.
Their original proof and certificate obligations remain in the linked packages.
Review status is recorded as of the committed graph cutoff in the registry.

The new executable scope example is the classical Moser spindle. The same
seven points support a non-strict unit drawing of
`Cay(Z/7Z,{+1,-1})`, whose edge graph is three-chromatic. Its strict
completion has eleven unit edges and chromatic number four. Thus an upper
bound on a prescribed Cayley edge graph does not automatically bound all
unit contacts among its drawn points. The two unit diamonds also illustrate
why a colouring-pasting argument must account for cross-piece unit edges.

The checker evaluates all 21 distances by two exact arithmetic routes,
checks the spanning cycle and its colouring, and examines all
`3^7+4^7=18,571` colour words for the strict graph. It finds zero proper
three-colourings and 384 proper four-colourings. This is a checked scope
example, not a new construction or a claim of priority.

## Reproduce

From this repository, using CPython 3.11 or later and its standard library:

```sh
python3 hadwiger_nelson_exact_frontier_consolidation/audit.py
```

[EXPECTED.json](EXPECTED.json) gives the exact output. The audit reads
existing source files in the repository, verifies their pinned identities,
checks a few arithmetic consequences of published counts, and verifies the
scope example. It invokes no historical verifier, network request, SAT solver,
or floating-point predicate. Source bytes are pinned at repository snapshot
`a1aa6a2e28fd156abe98ce8236922527c6252fcc`; original mathematical source
commits are separately recorded. Changes to a pinned file fail the audit.

The seven-point example can also be checked without the historical packages:

```sh
python3 hadwiger_nelson_exact_frontier_consolidation/scope_guard.py
```

The campaign benchmark remains the supplied 509-vertex Parts graph. None of
the consolidated exclusions proves its global minimality. The three frozen
pilots contain 37 saved, labelled 508-vertex outputs with proper four-colourings;
they give no upper bound for unsampled point sets. The completed G79 trajectory
and all earlier pilot caps remain closed. No fourth growth pilot was started.
