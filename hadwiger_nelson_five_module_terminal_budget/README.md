# Five-module eight-terminal obstruction

This package closes the exact viability question handed off by the accepted
four-module synthesis result h4051. The conclusion is stronger than the
requested equilateral-triangle case.

**Theorem.** Consider five finite plane unit-distance modules with designated
terminal sets. Assume:

1. distinct terminals of the same module are at distance strictly greater
   than two;
2. every nonmonochromatic four-colour assignment to each terminal set extends
   through that module;
3. different modules overlap only at common terminals; and
4. every additional unit edge between modules has both endpoints in the
   terminal union.

If the five terminal sets have at most eight distinct physical points in
their union, the complete strict unit-distance assembly is four-colourable.
This permits arbitrary terminal-set sizes, coincidences, real placements, and
module orders. In fact, **every** choice of one inequality pair per terminal
set gives a four-colourable auxiliary graph.

Consequently, any non-four-colourable five-module assembly under these
hypotheses needs at least nine distinct terminals. At physical order at most
508, its private vertices total at most 499, so some module has at most 99
private vertices. Equivalently, five modules with at least 100 private
vertices each already need at least 509 points if the assembly is
non-four-colourable. For the full A159/B214 modules inherited from h4051, the
minimum architecture-specific order bound improves from 783 to 789.

These are necessary conditions for this terminal-only architecture. They do
not assert that a suitable reduced negative forcing module exists, do not
cover private-interior interactions or extra connector vertices, and do not
produce a five-chromatic graph or improve the 509-vertex graph reported by
[Parts](https://arxiv.org/abs/2010.12665).

During this computation, the [h4055 A159 compression
theorem](../hadwiger_nelson_a159_module_compression/README.md) separately
proved that every proper A159 private-vertex reduction extends even
monochromatic terminal assignments.
That stronger source-specific result already closes reduced-A159 synthesis at
five modules without a terminal-count bound. The theorem here does not reopen
that family: it supplies the remaining source-independent condition for new
nonmonochromatic-extension modules, intact/mixed modules, or other replacement
gadgets satisfying the same interface.

## Proof mechanism

Select any pair in each terminal set and add it as an auxiliary inequality
edge. The terminal unit graph together with the at most five selected long
edges has maximum degree at most five. A geometric `K5` would require at least
six long edges, so none occurs.

The new small-graph lemma says that every `K5`-free graph on at most eight
vertices with maximum degree at most five is four-colourable. Its structural
proof passes to the complement, pads to eight vertices with universal
vertices, and uses Tutte's one-factor theorem. An exact alternative audit
enumerates every labelled potential vertex-critical kernel.

See [PROOF.md](PROOF.md) for the complete argument and
[VALIDATION.md](VALIDATION.md) for the computational boundary.

## Reproduce

Using CPython 3.11 or later and only the standard library, from the repository
root:

```sh
python3 -B hadwiger_nelson_five_module_terminal_budget/verify.py --check-expected
python3 -O -B hadwiger_nelson_five_module_terminal_budget/verify.py --check-expected
cd hadwiger_nelson_five_module_terminal_budget
sha256sum -c SHA256SUMS
```

The exhaustive kernel run checks 855,921 labelled graphs with all degrees in
`{4,5}` on orders five through eight. All 855,904 `K5`-free cases receive an
explicit proper four-colouring; the other 17 contain `K5`. The independent
degree-polynomial audit obtains the same per-order totals without importing
the generator. Three interface fixtures check all 487 selected-pair choices,
including terminal coincidences and an auxiliary vertex of degree five. The
eight rejection controls run in every verifier invocation.

The written reduction and Tutte's theorem establish the universal claim. The
Python computations provide a separate finite proof route and definition-level
interface checks; they are internal validation, not independent-author review.
No SAT solver, floating-point comparison, coordinate search, external graph
catalogue, or omitted generated artifact is used.
