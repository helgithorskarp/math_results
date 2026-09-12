# A sharper global edge window for Ramsey(5,5;43)

**Every 43-vertex graph with neither a clique nor an independent set of
order five has between 391 and 512 edges.**  This excludes the complete
unrestricted physical classes with exactly 390 or exactly 513 edges and
strictly sharpens the accepted `390..513` window.  No symmetry or structured
construction family is assumed.

The proof strengthens the accepted dense-neighborhood overlap lemma from
common degree deficit two to deficit three.  Of 6,669 coarse rooted-profile
pairs, 6,668 fail the two existing inequalities.  The unique survivor has
only six physical rooted occurrences; all 36 ordered gluings require deficit
at least four by exact `C`-to-`T` degree capacity.  A new weighted-incidence
argument then handles all eleven partitions of total degree excess six and
forces a forbidden five-clique.

See [PROOF.md](PROOF.md) for the complete reduction and trust boundaries.
`CERTIFICATE.json` records every finite count, exceptional occurrence,
physical-gluing requirement, and excess partition.

## Reproduce

Use CPython 3.11 or later and its standard library.  The sibling directory
`ramsey_r55_regular18_overlap_exclusion` is required; its two imported files
are hash-pinned in `DEPENDENCIES.json`.

From the repository root:

```sh
python3 -B ramsey_r55_global_edge_window_391_512/reproduce.py .
```

Expected final line:

```text
REPRODUCED_GLOBAL_GOOD43_EDGE_WINDOW_391_512
```

The replay regenerates the certificate with the set-based producer, checks
it byte-for-byte, invokes the independent bitset verifier normally and under
`python -O`, rejects two corrupt certificates, and checks every source hash.
Typical runtime is under one minute on one CPU core; no network access or
external solver is used.

The independent verifier's expected mathematical summary is:

```json
{"coarse_profile_pairs": 6669, "coarse_survivors": 1, "degree_excess_partitions": 11, "edge_window": [391, 512], "internal_exception_graphs_checked": 33951, "minimum_required_common_deficit": 4, "physical_occurrences": 6, "physical_ordered_gluings": 36, "status": "VERIFIED_GLOBAL_GOOD43_EDGE_WINDOW_391_512"}
```

## Scope

This is a universal necessary condition for a hypothetical good43 graph,
not an existence result and not an improvement of `43 <= R(5,5) <= 46`.
Historical priority is unclaimed.  The principal imported boundary is the
accepted completeness of the official order-24 `(4,5)` catalog and the
derived dense retained stream; exact references and hashes are in
`DEPENDENCIES.json`.

No pending Discovery Net transaction from an earlier campaign pass is
resubmitted by this package.
