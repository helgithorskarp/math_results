# Pairwise nonisomorphism of the Parts-509 swap family

## Result

Let `G` be Jaan Parts's strict 509-vertex, 2,442-edge unit-distance graph.
The sibling contribution
`../hadwiger_nelson_parts509_swap_closure` certifies that exactly eleven
one-point swaps `G - u + q` are not four-colourable and that every other such
swap is four-colourable.  Number those exceptional graphs `S0,...,S10` in the
order of the `swaps` array in the sibling `swap_certificate.json`.

The exact, solver-free certificate in this directory proves

> **Theorem.** The twelve abstract graphs `G,S0,...,S10` are pairwise
> nonisomorphic.

Consequently the closed one-point-swap neighbourhood of the Parts graph
contains exactly twelve isomorphism classes of 5-chromatic strict unit-distance
graphs: the original class and eleven genuinely different swap classes.  By
the sibling certificates, every graph in this family has 509 vertices and is
5-vertex-critical.  This is a structural classification around the known
record, not a graph with fewer than 509 vertices and not a change to
`5 <= chi(R^2) <= 7`.

The eleven swaps have the following elementary parameters.

| graph | deleted `u` | degree of `q` | edges |
|---|---:|---:|---:|
| `S0` | 217 | 6 | 2,443 |
| `S1` | 220 | 6 | 2,443 |
| `S2` | 300 | 6 | 2,442 |
| `S3` | 301 | 6 | 2,442 |
| `S4` | 347 | 6 | 2,442 |
| `S5` | 350 | 6 | 2,442 |
| `S6` | 353 | 6 | 2,442 |
| `S7` | 356 | 6 | 2,442 |
| `S8` | 375 | 5 | 2,442 |
| `S9` | 413 | 7 | 2,443 |
| `S10` | 415 | 8 | 2,444 |

## Small invariant proof

For a finite graph `H` and a vertex `v`, define the degree profile

```text
p_H(v) = (deg_H(v), sorted multiset {deg_H(w) : w adjacent to v}).
```

An isomorphism preserves degrees and carries each neighbourhood bijectively to
the corresponding neighbourhood.  It therefore preserves both the degree
histogram and the multiset `{p_H(v) : v in V(H)}`.

The twelve graphs split into the following degree-histogram classes:

```text
{G}, {S0,S1}, {S2,S3}, {S4,S7}, {S5,S6}, {S8}, {S9}, {S10}.
```

Thus the degree histogram separates 62 of the 66 unordered pairs.  The four
remaining pairs are separated by the following explicit profile counts:

| pair | profile `(degree; neighbour degrees)` | left count | right count |
|---|---|---:|---:|
| `S0,S1` | `(5; 8,8,8,10,16)` | 2 | 1 |
| `S2,S3` | `(5; 7,8,8,10,17)` | 3 | 2 |
| `S4,S7` | `(5; 7,8,8,10,17)` | 4 | 3 |
| `S5,S6` | `(5; 7,8,8,10,17)` | 2 | 3 |

This proves all 66 nonisomorphism statements without a canonical-labeling or
isomorphism solver.  `classification_certificate.json` records every graph's
full degree histogram, a regression digest of its full profile multiset, and
an explicit separating witness for every pair.  Its SHA-256 is
`8ede08b5431b90810f4e4a08bfd1855b0d541fedc2a29dd898ace33f961e7b62`.
The digest is only a regression identifier; the checked invariant differences
are the proof.

## Reproduction

From the repository root, using only Python 3's standard library:

```bash
python3 hadwiger_nelson_parts509_swap_isomorphism/classify_swap_graphs.py \
  --expect hadwiger_nelson_parts509_swap_isomorphism/classification_certificate.json
```

Expected final JSON fields include:

```text
pairwise_comparisons: 66
degree_histogram_separations: 62
degree_profile_separations: 4
all_pairwise_separated: true
```

An independent optional check constructs the twelve graphs separately and
runs NetworkX's exact VF2 isomorphism test on all 66 pairs:

```bash
python3 -m venv /scratch/parts509-isomorphism-venv
/scratch/parts509-isomorphism-venv/bin/pip install -r \
  hadwiger_nelson_parts509_swap_isomorphism/requirements.txt
/scratch/parts509-isomorphism-venv/bin/python \
  hadwiger_nelson_parts509_swap_isomorphism/independent_networkx_check.py
```

Expected output:

```text
{"all_checks": true, "graphs": 12, "networkx_version": "3.5", "pairwise_nonisomorphic": 66}
```

## Inputs and trust boundary

The primary checker binds its inputs before constructing any graph:

```text
canonical base edge list
  5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c
swap_certificate.json
  a36a11bf3e63d3ec887b0f4507d51623773b968842a964a314e364713ac46ca3
```

The nonisomorphism proof trusts Python's integer, set, multiset, JSON, and
SHA-256 implementations and the short primary checker.  The optional NetworkX
run is an algorithmically different audit.  Geometry, completion-enumeration
completeness, 4-colourability of the other swaps, and non-4-colourability of
the eleven exceptions are not reproved here; they are the explicit trust
boundary supplied and checked by the sibling swap-closure artifact.  In
particular, this directory does not trust a SAT solver for its new claim.

## Context

- Jaan Parts, *Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane*, Geombinatorics 29(4) (2020), 137--166,
  <https://arxiv.org/abs/2010.12665>.
- Marijn J. H. Heule, *Computing Small Unit-Distance Graphs with Chromatic
  Number 5*, Geombinatorics 28(1) (2018), 32--50,
  <https://arxiv.org/abs/1805.12181>.

Targeted literature and committed-graph searches found no classification of
these eleven exceptional swaps.  This establishes graph-new structural
information relative to the searched sources, not historical priority.
