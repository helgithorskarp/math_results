# Dean k=5 v1.0.1: bridge counterexample to the literal end-block-arm statement

This note audits the preprint *Cycles of length divisible by five in graphs
of minimum degree five*, version 1.0.1 (Zenodo DOI
<https://doi.org/10.5281/zenodo.22182448>). It identifies a local statement
defect, not a counterexample to the main theorem.

## The defect

Lemma 7.2, “Literal end-block arm” (`lem:type-i-endblock-arm`, source lines
2714–2744), allows a *nontrivial end-block*. The paper's definition explicitly
counts a bridge with its two ends as a block (source lines 176–180). The lemma
is therefore false as written.

Let (Y) be the path (u-z-t), let (B=Y[\{u,z\}]), and add an ambient
vertex (p\notin V(Y)) with the edge (pu). Then:

- (Y) is connected but not 2-connected;
- (B=uz) is a nontrivial bridge end-block with cutvertex (z) and open
  interior (I=\{u\});
- the rooted graph has roots (u,z), so there are no nonroots and the degree
  premise in part (a) holds vacuously;
- after the required deletion of (uz), the graph (B-uz) has no
  (u\)-(z) path at all, rather than three good paths.

Run the dependency-free check with:

```bash
python3 verify_counterexample.py
```

Expected final line:

```text
PASS: part (a) has 0 rooted paths although its premise is vacuous
```

## Scope and repair

The proof paragraph itself says that bridge end-blocks are excluded in every
application. I checked all explicit later citations of the lemma. The relevant
open endpoint has component degree at least 2 in the first call, at least 4 in
the next two calls, and at least 3 (or 4) in the final cash-out call. A bridge
end-block's open endpoint has component degree 1, so none of these applications
uses the counterexample case.

The local statement is repaired by replacing “nontrivial end-block” with
“non-bridge end-block” (equivalently here, a 2-connected end-block). Under the
section's standing triangle-free hypothesis and the stated degree premises,
the published rooted-path argument then applies. Thus this defect is
nonfatal on the presently audited dependency chain; it should not be read as
an independent validation of the rest of the proof.
