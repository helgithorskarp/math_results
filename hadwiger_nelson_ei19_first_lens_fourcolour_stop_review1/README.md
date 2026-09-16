# Independent review: EI19 first-lens four-colour stop

## Verdict

**Accept and strengthen at the fixed-realization, first-closure scope.** An
independent exact checker confirms that the isolated 19-point EI19 source has
35 unit edges and chromatic number four, that exactly 165 source pairs have
distance below two, and that the resulting 349 formal labels admit the
submitted collision-safe proper four-colouring.

The review adds two certified facts:

1. The actual collision quotient has between **247 and 349 physical points**.
   The lower bound is exact-certification information, not the target's
   tolerance-based 247-cluster diagnostic.
2. The 19-vertex EI19 source is **vertex-critical four-chromatic**. Direct
   exhaustive search rejects three colours for the full graph, while 19
   independently generated words three-colour every one-vertex deletion.

This is a rigorous stop for one fixed EI19 realization after one round of
two-unit-circle intersections. It is not a five-chromatic construction, an
exact physical census, a statement about later closure rounds or EI19's other
realizations, or a global Hadwiger--Nelson exclusion.

## Independent method

The checker pins twelve public target and dependency files but imports none of
their executable code. It independently:

- replays the 34-variable rational contraction certificate and all 171 source
  pair exclusions;
- uses exact `Fraction` interval endpoints and rounds only square roots, on a
  separately chosen `2^192` grid (the target instead uses integer dyadic
  intervals at `2^160` and rounds every operation);
- classifies all source pairs as 165 eligible and 6 ineligible, then encloses
  both lens points for each eligible pair;
- checks all 60,726 formal-label pairs: differently coloured rectangles are
  separated in a coordinate, while every same-colour squared-distance
  interval excludes one;
- checks all 388 rectangle-overlap pairs and their 247 connected components;
  and
- performs complete deterministic DSATUR searches on the EI19 source and its
  nineteen vertex deletions.

The independent rectangle stream has SHA-256

```text
f9fefacf17624b259fde2c3fde35c8de39b5463f2a64221867ae94e73cd16ec7
```

and the deletion-word stream has SHA-256

```text
cf9e424d927f0d3bd670c2e3a75c5928f161f82166922865eadd728484b13c94.
```

## Why 247 is a rigorous lower bound

Each formal label's exact point lies in its certified rectangle. If two labels
represent the same physical point, their rectangles intersect coordinatewise,
so those labels are adjacent in the rectangle-overlap graph and hence lie in
one connected component. Labels in different components therefore cannot
collide. The overlap graph has 247 components, with size histogram

```text
size 1: 227 components
size 3:   1 component
size 4:  10 components
size 7:   5 components
size 11:  4 components.
```

These component sizes account for all 349 labels. They do not prove that all
labels within a component coincide, so the review deliberately reports the
physical order as the interval `[247,349]`, not as 247.

## Geometric and chromatic scope

The contraction certificate gives a unique exact real root inside its
rational box. Its 35 listed source pairs are unit and all 136 unlisted source
pairs are non-unit. For every source pair at distance below two, the usual
two-circle formula produces two exact points at unit distance from both
endpoints; interval arithmetic encloses those exact points.

Different-colour rectangle separation makes the submitted colour well-defined
after physical collision. Same-colour unit-distance exclusion then makes it
proper for the complete physical unit-distance graph, including every
unanticipated unit contact. The EI19 source remains a four-chromatic subgraph,
so the closure's physical graph has chromatic number exactly four.

## Reproduction

From the repository root, with CPython 3.11 or later and only the standard
library:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B hadwiger_nelson_ei19_first_lens_fourcolour_stop_review1/independent_check.py --check-expected
PYTHONDONTWRITEBYTECODE=1 python3 -O -B hadwiger_nelson_ei19_first_lens_fourcolour_stop_review1/independent_check.py --check-expected
PYTHONDONTWRITEBYTECODE=1 python3 -B hadwiger_nelson_ei19_first_lens_fourcolour_stop_review1/controls.py
cd hadwiger_nelson_ei19_first_lens_fourcolour_stop_review1 && sha256sum -c SHA256SUMS
```

Normal and optimized reports must be byte-identical. The trust boundary is the
pinned public bytes, exact Python integer and rational arithmetic, the
mathematical square-root enclosure argument, direct finite search, SHA-256 and
ordinary hardware. No target executable, floating predicate, solver status,
private dataset or tolerance clustering is trusted.

## Record and graph context

Parts's [509-point, 2,442-edge construction](https://arxiv.org/abs/2010.12665)
remains the supported unrestricted five-chromatic plane unit-distance record.
Haugland's [2026 manuscript](https://arxiv.org/abs/2608.04542) explicitly does
not improve that order. This reviewed graph is four-chromatic and therefore is
not a record candidate.

Reviewed target:
[EI19 first-lens four-colour stop](../hadwiger_nelson_ei19_first_lens_fourcolour_stop/README.md),
mathematical commit `bada7569ddcfb515e608d6b043a0558416def00b`.

