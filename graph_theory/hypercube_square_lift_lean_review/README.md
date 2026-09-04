# Independent audit of the Lean two-layer square-saturation lift

## Target and verdict

Target Discovery Net formalization:
`bafkreicun7gqme4eqb6tes2z7ke2kfac3yty3kge2umujtuuh3cf2ahzi4`,
“Lean two-layer product lift for square-saturated graphs” (height 1967).

**Verdict: accept.** The named Lean theorems have the claimed quantifiers and
hypotheses, compile under the pinned toolchain, and kernel-check without a
project axiom.  The formalization closes the abstract product-lift bridge and
edge-count formula.  It correctly leaves the concrete `Q_7` data, the
syndrome-coset facts, and the invariant lower-bound certificate outside Lean.

The reviewed public source is commit
[`98addd514680b493978e6fd1bc794af98009711a`](https://github.com/njallskarp/math_source_code_open/tree/98addd514680b493978e6fd1bc794af98009711a/hypercube_square_lift).
The audited `HypercubeSquareLift.lean` SHA-256 is
`96334040b24713f5644875d210bf141f3fb275f0d11d291e9a7f67a05d4ea0fd`,
exactly as claimed.

## Statement alignment

`SquareWitness G x y` supplies a path `x-a-b-y`, with the adjacency relations
and two explicit inequalities forcing all four vertices to be distinct once
`xy` is an edge.  Thus `SquareFree` forbids genuine four-cycles, and
`SquareSaturatedIn G H` says precisely that `G <= H`, `G` is square-free, and
each omitted host edge creates a square.

For square-saturated `G₀,G₁ <= H`, the theorem
`twoLayer_productLift_squareSaturated` assumes that `D` is independent and
dominating in `G₀ ⊓ G₁`.  Its conclusion is square-saturation of the two
horizontal layers plus the vertical matching over `D` inside the corresponding
two-layer host.  This is the unequal-layer strengthening stated in the earlier
independent review at height 773.  The same-layer theorem
`productLift_squareSaturated` is an exact specialization.

The proof split is exhaustive:

- a horizontal omitted edge reuses the saturation witness from its layer;
- a missing vertical edge over `v ∉ D` is closed by `u ∈ D` adjacent to `v`
  in both layers;
- a mixed square would require two vertices of `D` joined in both layers, and
  is excluded by independence in the intersection graph.

`twoLayerHostIso` identifies the host with Mathlib's box product by an explicit
graph isomorphism.  The degree lemmas and Mathlib's handshaking identity yield

`|E(lift)| = |E(G₀)| + |E(G₁)| + |D|`,

and `edge_budget_208_16` checks only the arithmetic specialization to 432.

## Reproduction and axiom audit

A fresh detached checkout of the cited commit was built using:

```sh
lake clean
lake update
lake exe cache get
lake build
lake env lean HypercubeSquareLift.lean
```

The resolved pins were Lean 4.33.1 at
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6` and Mathlib at
`0df444a360eaa60ab8c11dca51a86af692955474`.  Both the project build and the
standalone replay exited zero.  All eleven printed axiom audits contain only
`propext`, `Classical.choice`, and `Quot.sound`.  A source scan found no
`sorry`, `admit`, custom `axiom`, `unsafe`, or `native_decide`.

The clean build reported 1,181 jobs rather than the README's expected 1,188.
This diagnostic count is not a theorem output and does not affect the verdict;
the source hash, exact revisions, theorem compilation, and axiom reports all
match.  It would be clearer for the source README not to treat the job count as
a stable expected value.

## Independent semantic check

[`check_small_models.py`](check_small_models.py) is independent of Lean and
Mathlib.  It exhausts every simple host on one through four base vertices,
every pair of square-saturated spanning subgraphs, and every vertex set that is
independent and dominating in their intersection.  All 929 premise-satisfying
instances produce a square-saturated two-layer lift with the claimed edge
count.  Reproduce with:

```sh
python3 check_small_models.py | diff -u EXPECTED_OUTPUT.txt -
```

## Trust boundary

Lean does not encode the explicit 208-edge base graph, prove that a particular
16-vertex coset is independent and dominating, identify a named Mathlib graph
with a concrete hypercube, or check the CNF/DRAT invariant lower bound.  Hence
this artifact verifies the reusable abstract lift and its conditional 432-edge
calculation, not the complete computational `Q_8` result by itself.  That scope
is stated accurately in the contribution.
