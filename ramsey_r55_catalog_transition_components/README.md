# Transition components of the known Ramsey(5,5,42) catalog

## Result

Let the vertices of a *catalog transition graph* be the 656 known
Ramsey(5,5,42) graph orientations: the 328 stored representatives in McKay's
catalog and their complements.  Join two distinct isomorphism classes at
radius `r` when some labeling of one can be changed into the other by at most
`r` edge flips.  Exact transition maps through radius six give the following
component census.

```text
radius  class edges  component sizes
1       1,976        128,128,96,96,48,48,40,40,12,12,4,4
2       7,224        128,128,96,96,48,48,40,40,12,12,4,4
3      15,200        128,128,96,96,48,48,40,40,12,12,4,4
4      22,872        272,272,40,40,12,12,4,4
5      28,360        272,272,40,40,12,12,4,4
6      33,240        272,272,40,40,12,12,4,4
```

Thus the radius-six graph has exactly eight connected components, in four
complement-paired families.  Their `(base, complement)` orientation counts
are

```text
(270,2), (2,270), (40,0), (0,40),
(12,0),  (0,12),  (4,0),  (0,4).
```

The complete 656-row assignment is in `COMPONENTS_RADIUS6.tsv`.  In
particular, each of the 139,424 unordered pairs in different radius-six
components has edge-edit distance at least seven, where distance is minimized
over vertex relabelings.  This is a separation statement *within the known
catalog*, not a claim about an unknown Ramsey(5,5,42) graph.

The only component mergers through radius six first occur at radius four.
There are four bridge pairs, two up to complementation.  Each of the two base
pairs has 32 distinct class edges and 80 labeled base-source rows:

```text
B031 -> B186: flip 6,12; 1,27; 28,31; 16,35  (128-to-96 components)
B000 -> B123: flip 4,17; 3,25; 35,37; 20,38  (128-to-48 components)
```

The complement lifts give `C031 -> C186` and `C000 -> C123`.  These bridges
merge `128+96+48=272` in each orientation family.  Radii five and six add
5,488 and 4,880 previously absent class edges, respectively, but do not merge
any of the eight components.  At radius six the two 272-vertex components
have transition-graph diameter four; all six smaller components are cliques.

## Why the graph is exact

The sibling radius artifacts exhaust every Ramsey-preserving labeled flip set
of the stated exact size from each of the 328 stored representatives and map
every survivor to a stored or complement isomorphism class.  Complementing
each transition covers the other 328 source orientations.  Conversely, if
two known catalog orientations have edge-edit distance at most `r`, relabel a
minimum witness so its source is the stored representative (or complement it
first).  Its flip set must then occur in one of the exhaustive maps.  Hence
the cumulative class-edge set, and therefore its connected components, is
complete through radius `r` under the earlier artifacts' trust boundaries.

Self-transitions are discarded because the vertices here are isomorphism
classes.  Multiple labeled witnesses and witnesses first enumerated at a
larger exact radius can map to an already-present class edge; this is why map
row counts differ from newly added class-edge counts.

`analyze_components.py` pins every input map by SHA-256, checks its summary,
catalog indices, flip weights, and labeled-assignment uniqueness, adds the
complement lifts, and derives components independently with breadth-first
search and union-find.  It also verifies complement invariance, all component
sizes, all graph diameters, the radius-four bridge structure, and the
committed membership table.

## Reproduce

From this directory, using only Python 3.11 or later:

```sh
python3 analyze_components.py | tee /tmp/r55-components.out
cmp /tmp/r55-components.out EXPECTED_OUTPUT.txt
sha256sum -c SHA256SUMS
```

The derivation takes under a minute on the reference host and no third-party
package.  To recreate
the membership table at a temporary path:

```sh
python3 analyze_components.py --write-components /tmp/COMPONENTS_RADIUS6.tsv
cmp /tmp/COMPONENTS_RADIUS6.tsv COMPONENTS_RADIUS6.tsv
```

## Provenance, trust, and scope

The input catalog is McKay's ANU [Combinatorial Data
archive](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).  The page says
that the 328 stored records and their complements comprise 656 known graphs,
but that more 42-vertex graphs may exist.  McKay and Radziszowski describe the
catalog and neighborhood searches in [*Subgraph counting identities and
Ramsey numbers*](https://users.cecs.anu.edu.au/~bdm/papers/r55.pdf).  Targeted
primary-source searches through 2026-09-04 found no published edge-edit
component census of these catalog classes; that search-relative observation
is not a historical priority claim.

This artifact is a deterministic synthesis of previously published exact
maps; it does not repeat their SAT or nauty computations.  It inherits their
explicit solver, encoding, and canonical-labeling trust boundaries.  It does
not establish catalog completeness, construct a 43-vertex graph, or improve
the bound on `R(5,5)`.
