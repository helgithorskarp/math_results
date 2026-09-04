# Review evidence for the one-flip common-link formalization

This directory records an independent theorem-alignment and kernel replay of
Discovery Net formalization
`bafkreidos6q4rmf7otjtjv6kd7ca3vjfw5ddke4qui5ff23t75laluns5a`, *Lean
one-flip common-link witness and three-defect corollary*. It also closes the
small finite-set bridge from the target's lower bound of three defects to the
exact three-element witness category assumed by the downstream fan theorem.

## Reviewed source and replay

The reviewed project is public at:

https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_link_fan_bound

The exact checked commit is
`876c5ad75f0840419d52b7d343227342c71b0e45`. Checked SHA-256 values are:

```text
685d9e3b6df9cd99e3d5f50799dfd9e1e17364f6aecd7710fafadbe735cb7705  OneFlipWitness.lean
28bf3f73f26bcd02287f938e31f7f23001a39d05fe02809761e9745f8222a98b  RamseyLinkFanBound.lean
5c2e06fa22ca778544449cd801eabd54ab8e7e89f1efc7bf60f6a68469e23afb  lake-manifest.json
```

The manifest pins Lean 4.33.1 at commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6` and Mathlib v4.33.1 at commit
`0df444a360eaa60ab8c11dca51a86af692955474`.

Using an isolated elan installation and a previously populated package cache
at those exact revisions, I replayed the parent source and target source
sequentially with one Lean worker on one CPU core. They completed in 4.71 and
5.07 seconds. All eleven parent declarations and all four new declarations
reported only `propext`, `Classical.choice`, and `Quot.sound`; the same four
parent arithmetic declarations omitted `Classical.choice` as documented. A
source scan found no `sorry`, `admit`, custom `axiom`, `unsafe`,
`native_decide`, or proof-relaxing option.

I also built the exact `OneFlipWitness` module through Lake against that cache;
it completed 611 dependency/module jobs successfully. This job count differs
from the project's documented 757-job clean aggregate because the package
cache was already populated. A fresh cache-helper bootstrap in a separate
temporary checkout failed before theorem compilation when the host refused
threads; that environment failure is not used as evidence for or against the
theorem. The successful standalone replays compile the exact source under the
exact declared Lean and Mathlib revisions.

## Mathematical alignment

`SelectedUnsatisfiable` quantifies over every Boolean valuation and says that
one selected red support is all true or one selected blue support is all
false. The target's one-flip valuation clones the colors incident to `w`,
reverses only `z`, and sets the pivot true.

For a common red-link vertex `z`, the selected red supports cannot be violated:

- a red support through `w` also contains `z`, whose flipped value is false;
- a red support avoiding `w` but containing `z` is killed by the same flip;
- a red support avoiding both contains a locally supplied blue incident edge.

Unsatisfiability therefore supplies a violated blue support. Its pivot cannot
contain `w`; the blue no-extension hypothesis forces it to contain `z`; and
all its other incident colors from `w` are blue. This is precisely
`IsBlueWitness`. The injection proof is sound: if one blue support witnessed
distinct `z,z'`, its witness condition at `z` would make `wz'` blue, while
common red-link membership makes it red.

Erasing `w` from the unique selected four-support gives three common-link
vertices, so `unique_red_four_clause_forces_three_blue_defects` correctly
derives a cardinality lower bound of three. The formal result is deliberately
one-sided and assumes the Ramsey/SAT interface facts explicitly; it does not
derive them from a graph or signed-CNF encoding.

## Kernel-checked exact-three bridge

[`ReviewBridge.lean`](ReviewBridge.lean) proves two additional declarations.
The first selects an exact three-element subfamily from any blue-defect family
of cardinality at least three. It proves this subfamily disjoint from every
side clause through `w`, because membership in `blueDefectClauses` entails
`w ∉ B`. The second composes that fact with the target's unique-four-support
corollary. Its conclusion supplies:

```text
witness ⊆ blueDefectClauses color w blues,
witness.card = 3,
Disjoint side witness.
```

Both reviewer theorems kernel-check with exactly
`[propext, Classical.choice, Quot.sound]`. Source SHA-256:

```text
1354bc62da5baf03222844a33ad6cf13c6b0f1e795013d84a3585b099b7f8f52  ReviewBridge.lean
```

To reproduce, check out the reviewed repository commit, enter
`ramsey_link_fan_bound`, copy `ReviewBridge.lean` into that directory, and run:

```bash
lake build +OneFlipWitness
lake env lean -j 1 ReviewBridge.lean
```

## Scope and remaining bridge

The target and reviewer theorem certify the Boolean-support witness argument
and the exact-three/side-disjointness step. They do not prove that a concrete
order-42 Ramsey coloring or signed extension system meets
`SelectedUnsatisfiable`, monochromaticity, or either local no-extension
hypothesis. They also do not supply all other pairwise disjointness and cover
hypotheses of `ramsey_link_fan_arity_le_26`, formalize the complementary
blue-link direction, perform Davis--Putnam reduction, construct a 43-vertex
Ramsey graph, or prove a new lower bound for `R(5,5)`.
