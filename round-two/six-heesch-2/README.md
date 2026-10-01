# One-cell grafts of the seventeen-cell Heesch-four polyhex

Agent **six-heesch-2**, role **researcher**, fresh round two, 2026-10-01.
This package gives a reusable pair-centered upper-bound reduction and an exact
bounded classification of unmarked polyhexes. It is not a Heesch record.

Let `S` be the seventeen-cell polyhex in `seed.json`, recovered from page 278 of
[Kaplan's author PDF](https://cs.uwaterloo.ca/~csk/heesch/hex/17hex_3up.pdf).
Let `F` be all connected, hole-free eighteen-cell shapes obtained by adding one
cell to `S`, identified under all translations, rotations and reflections.

**Claim.** `F` has exactly 26 members. Allowing all Euclidean rigid motions:

| Classification | Members |
| --- | ---: |
| `H_c = H_h = 0` | 6 |
| `H_h = 1`, `H_c <= 1` | 10 |
| `H_h = 2`, `1 <= H_c <= 2` | 1 |
| Periodic plane tilers | 9 |

Thus every finite member has `H_h <= 2`. This complete one-cell-growth family
cannot supply a finite-five polyhex. The strict hole-free value for the two
case, and the strict values for the ten one cases, are not claimed.

`H_c` requires every cumulative corona prefix to be a disc. `H_h` permits holes
only in the final prefix. Each new copy touches the preceding corona, and the
old patch lies in the interior of the next. Upper tests deliberately permit
holes, so they remain sound relaxations. A local SAT-like positive test is
not a corona certificate or evidence of a plane tiling.

## Reduction and compact evidence

[proof.md](proof.md) proves the following finite-depth reduction. Start with
all disjoint contacts `E_0`. Retain a contact in `E_(r+1)` only if its two fixed
copies can be jointly surrounded using a disjoint packing whose contacts lie
in `E_r`. In an `H`-corona patch, any contacting pair with both levels at most
`H-r` lies in `E_r`. If no `E_r`-compatible root surround exists, `H_h <= r`.
This also directly rules out a plane tiling. A stable nonempty domain is
inconclusive.

The all-motion bridge uses polyhex angles 120/240 degrees and the matching of
whole unit edges and vertex sectors. This grid argument and basic halo exact
cover are prior methods, not claimed as new. The useful contribution here is
the pair-centered depth accounting and its fully checked application to this
distinct family; no absolute historical priority is asserted for local
consistency methods.

`cover.py` searches exact whole-footprint covers. `audit.py` checks every
negative decision through an acyclic rejection DAG, rebuilding coverage and
conflicts by a different cell-incidence implementation. It checks all excluded
first-surround contacts, all rejected interior pairs, and the final rejected
root tests. Positive covers receive direct checks. `check_geometry.py` also
rebuilds every contact inventory by matching opposing boundary edges, instead
of the generator's cell-to-halo translations.

`seed.json` contains 58 rigid placements proving the **known** seed has four
complete hole-free coronas, with new-copy counts `1,5,11,17,24`. The input PDF
was rounded display geometry. Its recovered cell sets and whole-copy placements
are checked exactly after recovery; reproduction needs no PDF or floating
point. The PDF SHA-256 is
`1c97496a4e7893a31c7a1a45b62d7101d6dc163068dcca3b6d12e759d2c9160f`.

`certificates.json` provides the first-surround witnesses, a complete two-corona
witness for canonical family index 18, and all periodic witnesses. The two
case has new-copy counts `1,7,14`; its first prefix is hole-free and its last
prefix has holes. Its upper proof shrinks contact domains
`558 -> 84 -> 7`; the last domain cannot surround the root. No negative claim
about all hole-free two-corona packings follows from this one lower witness.

The nine periodic certificates use one or two copies in an integer period
lattice. A checker compares every occupied-cell difference vector with that
lattice. Exactly one cell in each lattice class proves full coverage and no
overlap. It does not assume tiling from a large patch.

## Scope and prior art

[Kaplan, *Heesch Numbers of Unmarked Polyforms*](https://arxiv.org/abs/2105.09438),
Contributions to Discrete Mathematics 17(2), 150–171 (2022), gives the census
through seventeen-cell polyhexes and attributes the seed's Heesch number four.
The coordinate fixture and its lower witness here are a reproduction of prior
work. Adding one cell is complete because any connected single-cell enlargement
must add a halo cell. Twelve exact orientations and translation normalization
give every free representative.

An independent embedding test proves that none of these 26 shapes belongs to
the earlier
[sixteen-cell two-cell-growth family](../../heesch_polyhex_two_cell_growth/README.md)
or [articulation-growth family](../../heesch_polyhex_bridge_growth/README.md).
It checks all oriented embeddings of the sixteen-cell seed and its three
fifteen-cell articulation-deletion remainders.

The unrestricted-size finite-five *polyiamond* premise already has an attributed
realization of [Mann's known hexapillar family](https://faculty.washington.edu/cemann/Heesch.pdf):
[the published 215-cell source](../../heesch_polyiamond_hexapillar/README.md)
gives five hole-free coronas and an all-motion finite bound, and
[the 214-cell variant](../../heesch_polyiamond_local_deficit/README.md)
gives another finite-five example. These are relevant prior art. The meaningful
frontier retained here is finite-five for an unmarked **polyhex**, or a genuinely
stronger finite polyiamond construction. This package solves neither frontier.

## Reproduce

Use CPython 3.11.2 or compatible Python 3, with assertions enabled. Only the
standard library is required. From the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 round-two/six-heesch-2/verify.py
```

Expected final counts: `Hh0:6, Hh1:10, Hh2:1, periodic:9`, with
`all_upper_bounds_audited:true`. `expected.json` compares every canonical case,
every peeling row, the whole family hash, lower-prefix checks and audit totals.
Canonical family SHA-256:
`85d5318ee95b42d630b67fd45765a87fb65f8c95449426298d4456b30870394c`.

The checked run audited 5,473 negative calls, 757 positive calls and 31,284 failed
states across 506 finite cover instances. The checked runs took about 152 and
186 seconds and 46 MiB maximum resident memory in the stated environment,
on one CPU, without native
solvers. A 300,000-node guard raises an exception; an incomplete search cannot
produce a classification. Raw PDF data, exploratory scripts, failed-state DAGs,
logs, environments and private ledgers are not published.

The written geometric reduction, exact Python code and small auditor are the
trust boundary. The auditor shares integer isometry primitives with the search.
No proof-assistant formalization, independent peer-review verdict, priority
claim, universal eighteen-cell exclusion or finite-five construction is asserted.
The next constructive route needs simultaneous cell exchanges or other changes
that preserve deeper surrounds; single-cell grafts of this seed are exhausted.

The [exchange-family continuation](exchanges/README.md) treats all 4,990 free
one-delete-two-add shapes about the same seed. It extends the finite bound
to that family and supplies a star-type odd-cycle obstruction for an exact
Heesch-two example whose pair domains stabilize.
