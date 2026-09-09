# All 238 supplied Cyclic(43) defect-support repair families are impossible

This package certifies a broad structured obstruction around the persisted
Cyclic(43) objective-twelve states.  For each of the 238 supplied source
representatives, free **every** edge belonging to one of its twelve current
monochromatic `K5`s and fix every other physical edge.  Every one of these 238
Boolean subcubes is UNSAT by unit propagation.

The free supports have 60 to 97 edges.  Thus each result excludes all
`2^60` through `2^97` simultaneous recolourings in its declared subcube.  The
sum over the 238 indexed families is
`432902959030480243214044364800`; this is an indexed total, not a claim that
the subcubes are disjoint.

This generalizes the earlier source-51 exclusion to every supplied source.
It is not a good43 construction, does not establish `R(5,5) >= 44`, and does
not classify cyclic states outside the inherited 238-state list.

## Reproduction

From the repository root, run into a fresh directory:

```bash
python3 -B \
  ramsey_r55_cyclic43_q12_all_defect_support_exclusion/reproduce.py \
  /tmp/r55-q12-all-defect-support-replay
```

Expected status:

```text
REPRODUCED_ALL_238_DEFECT_SUPPORT_FAMILIES_UP_UNSAT
```

The replay does all of the following:

1. pins the inherited source file by SHA-256;
2. compiles the generator as strict C++20 in release and
   address/undefined-sanitized modes;
3. regenerates [CENSUS.tsv](CENSUS.tsv) and the 18,077-row compact
   [PROOF.tsv](PROOF.tsv) byte for byte in both modes;
4. verifies all 238 sources in normal and optimized Python with a separately
   implemented clique-recursion census; and
5. rejects three deliberate corruptions of the census and proof.

No SAT solver result is trusted.  The proof traces contain only physical
five-vertex witnesses: 56 to 90 unit assignments followed by one falsified
Ramsey clause, so the cores have 57 to 91 clauses.

## Exact scope

For source graph `G_i`, let `D_i` be its twelve monochromatic five-sets and
let `S_i` be the union of their edge sets.  The excluded family consists of
all red-blue colourings agreeing with `G_i` outside `S_i`; edges in `S_i` are
arbitrary and need not preserve degree, symmetry, or the original defects.

The 238-source completeness is conditional on the pinned persisted list,
exactly as in the upstream boundary certificate.  This package does not
regenerate the upstream 1,041,887-orbit frontier, cover disconnected cyclic
basins, exclude supersets of `S_i`, or decide any of the 161 UNKNOWN h3987
q10 tasks.  A good43 reachable from one of these sources must change at least
one edge outside its original defect support.

See [PROOF.md](PROOF.md) for the finite reduction and [HANDOFF.md](HANDOFF.md)
for the construction consequence.
