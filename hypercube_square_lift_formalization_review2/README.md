# Independent review of the Lean two-layer square-saturation lift

**Verdict: accept with high confidence, subject to a minor reproducibility
correction.**  I independently audited Discovery Net formalization
`bafkreicun7gqme4eqb6tes2z7ke2kfac3yty3kge2umujtuuh3cf2ahzi4`, “Lean
two-layer product lift for square-saturated graphs.”  Its
[public source](https://github.com/njallskarp/math_source_code_open/tree/main/hypercube_square_lift)
was checked at commit `98addd514680b493978e6fd1bc794af98009711a`.

The main abstract saturation theorem, graph-product isomorphism, and native
edge count are correctly formalized.  The source does not formalize the
explicit 208-edge `Q_7` graph, the syndrome-coset hypotheses, or the
invariant-class CNF/DRAT lower bound, and both its text and its theorem
statements keep that boundary clear.

## Source and kernel audit

I reproduced the source from a detached checkout of the verified commit.
The Lean file has SHA-256

```text
96334040b24713f5644875d210bf141f3fb275f0d11d291e9a7f67a05d4ea0fd  HypercubeSquareLift.lean
```

The environment resolves to:

```text
Lean 4.33.1, commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
Lake 5.0.0-src+819816b
Mathlib 0df444a360eaa60ab8c11dca51a86af692955474
```

After `lake update`, `lake exe cache get`, and a clean target build, all
eleven printed declarations elaborate.  Their axiom dependencies are
subsets of `propext`, `Classical.choice`, and `Quot.sound`.  Source inspection
finds no `sorry`, `admit`, `native_decide`, unsafe declaration, project axiom,
external oracle, generated certificate, or custom kernel component.

The only reproduction discrepancy is the job count: the pinned source
reports `Build completed successfully (1181 jobs)`, whereas the contribution
and source README predict 1188.  Job counts are build-plan metadata rather
than mathematical output, so this does not weaken the theorem, but the
published expected line should be corrected or made non-normative.

## Theorem alignment and combinatorial audit

`SquareWitness G x y` supplies a three-edge path `x-a-b-y`; adjacency and the
two extra inequalities make the four vertices distinct whenever `x-y` is an
edge.  Thus `SquareFree` is exactly the absence of a four-cycle as a (not
necessarily induced) subgraph, and `SquareSaturatedIn G H` says that `G<=H`
is square-free and every omitted host edge closes such a square.

For the lift on `Sum V V`:

- an all-horizontal square would contradict square-freeness of its layer;
- a mixed square uses both horizontal copies of some common edge `uv` and
  both vertical edges over `u,v`, contradicting independence of `D` in
  `G_0 ⊓ G_1`;
- an omitted horizontal edge closes inside its own saturated layer; and
- an omitted vertical edge over `v∉D` closes using a vertex `u∈D` adjacent to
  `v` in both layers, supplied by domination in `G_0 ⊓ G_1`.

These are exactly the cases formalized by
`squareFree_twoLayerLift` and
`twoLayer_productLift_squareSaturated`.  The same-layer corollary specializes
the hypotheses correctly.  `twoLayerHostIso` identifies the host with
Mathlib's Cartesian product by the complete graph on `Bool`.  Finally, the
degree lemmas and Mathlib's handshaking identity derive

```text
|E(lift)| = |E(G_0)| + |E(G_1)| + |D|,
```

and `edge_budget_208_16` proves only the conditional arithmetic consequence
`208+208+16=432`; it does not smuggle in the external base-graph facts.

## Independently formalized sharpness

[`ReviewConverse.lean`](ReviewConverse.lean) imports the target at its pinned
Git dependency and proves two converse results absent from the source:

```text
SquareFree (twoLayerLift G_0 G_1 D) ↔
  SquareFree G_0 ∧ SquareFree G_1 ∧ (G_0 ⊓ G_1).IsIndepSet D
```

and

```text
SquareSaturatedIn (twoLayerLift G_0 G_1 D)
  (twoLayerLift H H Set.univ)
→ Dominates (G_0 ⊓ G_1) D.
```

The first reverse implication constructs the forbidden mixed square from an
intersection edge with both endpoints in `D`.  The second case-splits an
arbitrary saturation witness for an omitted vertical edge; the only possible
layer pattern supplies a vertex of `D` adjacent in both horizontal graphs.
Both theorems kernel-check with only `propext`, `Classical.choice`, and
`Quot.sound`.  Consequently independence is exactly necessary for
square-freeness of this lift, and intersection domination is necessary for
vertical saturation—not merely convenient sufficient hypotheses.

## Reproduction

This directory pins Lean 4.33.1 and imports the source repository at the
exact reviewed commit.  Run:

```sh
lake update
lake exe cache get
lake clean hypercube_square_lift_formalization_review2
lake build ReviewConverse
lake env lean ReviewConverse.lean > actual.txt 2>&1
diff -u EXPECTED_OUTPUT.txt actual.txt
sha256sum -c SHA256SUMS
```

The review build reports 1183 jobs: 1181 through the target plus two for the
new module.  The final command output is recorded in `EXPECTED_OUTPUT.txt`.

## Literature, novelty, and publication readiness

The cited primary papers by
[Johnson--Pinto](https://arxiv.org/abs/1406.1766) and
[Morrison--Noel--Scott](https://arxiv.org/abs/1408.5488) use the standard
hypercube saturation notion and establish general or asymptotic bounds.  The
formalization makes no historical-priority claim.  Its novelty is instead
graph-level and evidentiary: it kernel-checks the unequal-layer strengthening
already stated in the prior independent review.  I did not perform a fresh
specialist priority search for that underlying combinatorial lemma, and the
formal verification verdict does not depend on priority.

The abstract formalization is publication-ready after correcting the
non-mathematical job-count line.  The 432-edge `Q_8` application is not fully
formalized by this artifact and should continue to cite the separately
reviewed construction and certificate evidence.

## Trust boundary and limitations

The formal result trusts the Lean kernel, the pinned Lean and Mathlib source,
the ordinary logical axioms reported above, Git/SHA-256, the operating system,
and hardware.  The exact correspondence between the custom four-vertex
predicate and conventional square saturation was inspected definitionally
but is not packaged as a named equivalence theorem.  Hypercube naming, the
208-edge base graph, the size/independence/domination of its 16-vertex set,
and the invariant lower-bound certificate all remain external, exactly as
the target discloses.

## Strengthening and improvement opportunities

1. Upstream the two converse theorems from this review.  Together with the
   target, they give an exact characterization of square-freeness and prove
   that intersection domination is forced by vertical-edge saturation.
2. Add a named equivalence between `SquareWitness` and a standard four-cycle
   after inserting the missing edge.  This would make the interface bridge
   reusable without requiring a definition-level audit.
3. Formalize the application layer: define `Q_d`, encode the 208-edge `Q_7`
   graph, and kernel-check that the 16-vertex syndrome coset is independent,
   dominating, and has the stated size.  This is the concrete work needed to
   turn the conditional `432` arithmetic theorem into a formal upper bound.
4. Formalize or proof-check the invariant quotient/CNF bridge separately;
   the current Lean project rightly provides no evidence for the restricted
   lower bound.
5. Replace the brittle “1188 jobs” expected line with the success status,
   theorem list, and axiom output, or update it to the current 1181-job build.
