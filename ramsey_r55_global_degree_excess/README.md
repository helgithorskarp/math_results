# A global edge-count window for Ramsey(5,5;43)

**Every graph on 43 vertices with neither a clique nor an independent
five-set has between 390 and 513 edges.** This excludes the complete family
with at most 389 edges in either color, including all irregular cases.
No 43-vertex Ramsey graph or Ramsey lower-bound improvement is obtained.

The [proof](PROOF.md) combines a new global weighted degree-excess count
with a robust version of the accepted regular18/24 overlap certificate.
All 6,669 dense-neighborhood profile pairs remain impossible when their
common vertices carry total degree deficit at most two: 5,708 fail the
degree inequality and 961 fail the edge inequality. If a putative graph
has 388 or 389 edges, the global count forces at least eighteen or nine
qualifying vertices, respectively. Every pair among them must have the
same color, contradicting the five-clique restriction.

This strengthens the regular18/24 exclusion to seven additional irregular
degree multisets per color. It is a complete physical-family theorem with
imported finite-catalog boundaries, not an aggregate-feasibility claim.
Historical priority and sharpness are not claimed. External review of
this new result is pending.

## Reproduce

Use CPython 3.11 or later and its standard library. Keep the sibling
`ramsey_r55_regular18_overlap_exclusion` directory: the three required
files and their SHA-256 identities are in [DEPENDENCIES.json](DEPENDENCIES.json).
Its source commit is `1bc2e1d74be1e81478e716f6a5db17d92c0aedaa`;
the independent accepting review's source is
`a8f7ae91c2f6e999efd089daf33d392e7bd1ac9b`.

The complete official catalog is a 16,913,568-byte external input. It is
not republished here. From the repository root:

```sh
curl -fL https://users.cecs.anu.edu.au/~bdm/data/r45_24.g6 -o /tmp/r45_24.g6
python3 -B ramsey_r55_global_degree_excess/reproduce.py --catalog /tmp/r45_24.g6
```

Expected final status: `REPRODUCED_GLOBAL_GOOD43_EDGE_WINDOW`, with
`edge_window: [390, 513]` and `normal_and_optimized_agree: true`.
The catalog SHA-256 is
`83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0`.

The replay verifies source hashes, regenerates every new certificate entry,
independently scans all 352,366 catalog records and reconstructs the
24,648 relevant roots, and checks all 6,669 robust pair decisions. It also
enumerates 80 small exceptional graphs covering the seven degree-excess
multisets, checks the new algebra on 168 complete physical graphs, and
tests 30 edge-window/color boundaries and 11 malformed inputs. Both normal
and assertion-disabled Python are run. The separate verifier imports no
producer or parent implementation. No SAT solver, canonicalizer, floating
point, private trace or previously saved solver status is used.

The standalone necessary filter accepts an explicitly labeled physical
graph as JSON with exactly `n:43` and a strictly lexicographically sorted
`red_edges` list of distinct pairs `0<=u<v<43`. Omitted pairs are blue.

```sh
python3 -B ramsey_r55_global_degree_excess/edge_window.py --graph /tmp/graph.json
```

`EXCLUDED_BY_GLOBAL_EDGE_WINDOW` certifies membership in the excluded
family, relative to the theorem and its premises.
`NOT_EXCLUDED_BY_EDGE_WINDOW` is only a necessary check; it is not a target
certificate. The corresponding solver constraint is simply
`390 <= sum(x_ij for 0<=i<j<43) <= 513` for physical red-edge bits.

## Imported results and campaign scope

The small bounds R(3,5)<=14 and R(4,5)<=25 are classical; see
[McKay and Radziszowski, R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
The complete order24 catalog and the local extremal data are supplied on
[McKay's Ramsey graph page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
U(18)=85 and catalog completeness are inherited, explicitly unreproved
inputs. Scanning a catalog is not a proof of its completeness.

The accepted parent [regular18/24 result](../ramsey_r55_regular18_overlap_exclusion/README.md)
is h3959, `bafkreifv5rzt2stmmdwnmpudobmqqv7nbvcz6iegyjefjw6zoht3w7xnae`.
Its [accepting review](../ramsey_r55_regular18_overlap_exclusion_review1/README.md)
is h3965, `bafkreihsjllw2iy4gv36kwefgmhi5j2omkfkdl7rcb35a5ppj3dn4leldu`.
These supply the existing complete root coverage. The robust slack test,
irregular identities and global forcing argument are new to this package.
There is no proof-assistant formalization or independent peer review of
the new package; its independent implementation is same-author validation.

The q10 degree20/22 children have 430 or 473 edges, so this theorem gives
no new decision on that ledger. Its 99 closed and 161 open children remain
with team-r55-1. The h4001 q7-r5 result remains 518 closed and 122 open,
with 2,188,660 whole h3887 tasks remaining. This theorem removes low/high
density completions from every applicable whole task without claiming any
new whole packing-task exclusion. No parked subsystem or historical trace
was reopened. [HANDOFF.md](HANDOFF.md) states the usable constraint and
the natural boundary of this milestone.
