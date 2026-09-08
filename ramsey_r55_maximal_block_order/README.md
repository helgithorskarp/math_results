# Exact whole-block order in the complete good43 cover

Every one of the 2,189,178 h3873 tasks can order its equal-color nonroot
four-clique blocks by their complete root matrices. This preserves
satisfiability for each individual task and gives a literal subset of the
parent's labeled physical carrier. Counting repeated root matrices exactly,
the new complete carrier P satisfies

    1939*P < N < 1940*P,     P < 2^759,

where N is the h3873 carrier. This clears the predeclared factor-1024 gate.
No separate reduction factors are multiplied. No target, branch exclusion,
full-isomorphism census, or measured solver speedup is established.

The whole-block ordering principle is established prior work. The contribution
here is its exact joint count with ties, physical indexing and normalization,
and complete implementations for both the direct h3873 and shared-triangle
h3881 encodings. [PROOF.md](PROOF.md) gives the taskwise equivalence and count.
[HANDOFF.md](HANDOFF.md) specifies the complete interface.

There are still 18 macro classes and 2,189,178 tasks, with all original core
indices retained. The smallest per-task carrier is now q=7,r=7: 640 tasks
each below 2^695 codes. Size alone does not imply tractability. The direct
formulas add 60–120 prefix variables and 364–728 clauses. The shared-triangle
formulas retain maximum width eight.

## Reproduction

Use Python 3.11.2 and the standard library from the authorized repository
checkout. All three pinned sibling source packages in `DEPENDENCIES.json`
are required; their complete source manifests are checked before import.
The four author catalogs are the same hash-pinned inputs as h3873, totaling
6,571,256 bytes. They are not republished as bulk data. If absent, obtain them
with the parent's verified downloader:

```bash
python3 -B ramsey_r55_global_maximal_packing/catalog.py /tmp/bo1-data --download
python3 -B ramsey_r55_maximal_block_order/reproduce.py /tmp/bo1-data
python3 -B ramsey_r55_maximal_block_order/check_models.py /tmp/bo1-data
```

The compact replay checks the exact whole-family recurrence and interval
registry, exhaustive small multiset/orbit controls, comparator truth tables,
whole-graph indexing, and explicit edge transports including tied roots.
The separate model controls reject complete false-SAT carrier assignments in
both encodings. Carrier or normalizer output is never a target certificate.

Generate and independently audit 23 complete representative formulas in
fresh scratch outside the repository, then replay with assertions disabled:

```bash
python3 -B ramsey_r55_maximal_block_order/reproduce.py /tmp/bo1-data --cnfs /tmp/bo1-cnfs --generate
python3 -O -B ramsey_r55_maximal_block_order/reproduce.py /tmp/bo1-data --cnfs /tmp/bo1-cnfs
python3 -O -B ramsey_r55_maximal_block_order/check_models.py /tmp/bo1-data
```

These are all 18 direct macro-class representatives and five triangle forms:
one for each q with r=5, plus q=7,r=7,core=0. All generated literals are
compared with the independent physical streams and new ordering suffix.
Their exact hashes, dimensions and sizes are in `FORMULAS.json`. Bulk CNFs
are omitted. This does not claim to have generated every physical task;
coverage of every core index follows from the generic encoding and proof.

The global cover imports the h3873 catalog-completeness premise. The source
identities and other dependencies are explicit. No external automorphism
verifier, invalid h3687 claim, saved repair witness, or parked projection
route is used. External review of this new result is pending. Every physical
task remains undecided, and no good43 is established.
