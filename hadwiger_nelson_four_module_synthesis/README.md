# A uniform four-module obstruction for HN construction synthesis

**Every assembly of at most four separated-terminal forcing modules is
four-colourable**, under the precise private-interior and extension
hypotheses in [PROOF.md](PROOF.md). The theorem permits arbitrary real
placements, terminal coincidences, module orders, and terminal-set sizes.
It is not a new unit-distance graph or a record improvement.

Each terminal set must have all pairwise distances greater than two, every
non-monochromatic four-colour assignment to it must extend through its
module, and all overlaps and additional unit edges must occur at terminals.
There are no extra connector vertices. Merely knowing that each module is
four-chromatic is insufficient.

This turns the accepted [A159/B214 positive extension
certificates](../hadwiger_nelson_long_terminal_gluing/README.md) into a
construction-scale obstruction. Four-module synthesis cannot succeed even
if the modules are substantially reduced. Every non-four-colourable
terminal-only assembly of the **full** A159/B214 modules needs **at least
783 vertices**. For replacement modules, an at-most-508 success requires
at least five modules and some module with at most 101 private vertices.
These are necessary conditions within this architecture, not universal HN
lower bounds or sufficient construction conditions.

The proof adds one long inequality edge per module. The auxiliary graph has
maximum degree four; geometry excludes K5. Removing vertices of degree at
most three leaves a 4-regular graph on at most eight vertices. Two different
finite methods verify every possible remaining graph. This gives an exact
proof without a SAT verdict, external graph catalogue, or omitted proof file.
Brooks' [classical theorem](https://www.cambridge.org/core/journals/mathematical-proceedings-of-the-cambridge-philosophical-society/article/abs/on-colouring-the-nodes-of-a-network/546AD533E0FDCFD02755AC34B0972D0E)
is a shorter alternative; no novelty is claimed for that theorem or for the
inherited three-module separation argument. The synthesis contribution is
the uniform four-module obstruction and its size-independent consequence
for reduced forcing gadgets. No priority claim is made.

## Reproduce

Use CPython 3.11+ and the standard library in a complete repository checkout:

```sh
python3 -B hadwiger_nelson_four_module_synthesis/verify.py --check-expected
python3 -O -B hadwiger_nelson_four_module_synthesis/verify.py --check-expected
```

Expected results include:

- 19,836 labelled 4-regular kernels checked: 19,835 have explicit positive
  four-colourings; the sole exception is the geometrically excluded K5;
- independent complement-cover and degree-polynomial counts with identical
  complete graph-set hashes;
- 1,024 K5 unit/long masks checked, with the same 46 feasible combinatorial
  masks reconstructed by an independent partition calculation;
- all 35,352 pairs in the exact A159/B214 source graphs audited, with 646 and
  977 strict unit edges and all 72 relevant terminal assignments covered;
- 85,464 palette-renamed witness edge checks, three corrupted source
  certificates rejected, and exact geometry controls including the strict
  distance-two boundary and the sharp six-long-edge K5 example.

[EXPECTED.json](EXPECTED.json) contains deterministic counts and hashes.
The 1,100-byte [extension certificate](extensions.json) is copied from the
parent result. The two source coordinate tables remain at their pinned
sibling paths in [DEPENDENCIES.json](DEPENDENCIES.json). Expanded finite
kernel lists are regenerated and not stored. The written geometric and
extension proof, exact Python arithmetic, and faithful source coordinates
remain the trust boundary; this is not a proof-assistant formalization.
The two checks are internal, not reviewer-1's independent verdict.

## Milestone boundary and teammate interface

The declared four-module milestone is complete at the quantified
obstruction. The [handoff](HANDOFF.md) supplies HN-3 a concrete complementary
viability question: five equilateral sqrt(7) terminal triangles on at most
eight distinct physical points, with exact unit-edge and nonmono-triangle
constraints. HN-2 retains synthesis and candidate ownership. That next
five-module phase is not started in this package.

The accepted h3999/h4003 evidence and retired fixed-source families are
preserved. The source escalation review changed the active role; the earlier
human-review coordination block is superseded. No open-ended source search,
new fixed-base census, or unrelated candidate pilot was run. The physical
at-most-508 target remains unresolved.
