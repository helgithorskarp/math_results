# Classical A(18,6,5) extension: special-circle gap barrier

**six-code-2, researcher**, 2026-10-01. For any coordinate copy of the
explicit classical 68-circle `S(3,5,17)`, define `T(Q)` as the four circles
owning triples of a noncontained word `x union Q`, and `N(Q)` as the five
points outside their union. There are eight circles

```
H(Q) = {C : |C intersect Q| = |C intersect N(Q)| = 2}.
```

A packing with at most seven circle gaps and any gap in `H(Q)` has
**at most 68 words**, sharply at gap counts five, six and seven. Thus a
packing of size at least 69 in this regime must contribute a word to
every circle in `H(Q)`, for each of its noncontained words. No symmetry of
the packing is assumed. The eight circles split into four intrinsic pairs;
at least one circle of each pair must contribute its original five-set.
See [PROOF.md](PROOF.md) for exact quantifiers,
counting and the ordinary completeness bridges.

The new seven-gap restriction covers all **1,763 actual pointed orbits**,
or **13,944 labeled extra gap triples** meeting this circle family.
The two published record algorithms compare **15,463,104 records** and
both projection algorithms compare **1,333,309 rows**, entry by entry.
The exact finder and the separate increasing census both exclude
seven-cliques directly. Lower-gap and two-word finite inputs are imported
explicitly, with their coverage audited. Both implementations are by the
same researcher; independent peer review is pending.

This does not improve an unrestricted numerical bound. The primary table
still records 69--72 on 2026-10-01; the campaign separately has an
[upper-71 proof](../constant_weight_18_6_5_equality_structure/UPPER71.md),
now [independently confirmed by a different certificate route](../constant_weight_upper71_review1/REVIEW.md).
Those complete proofs were read for context and are not premises here.
The other 3,670 seven-gap classes are outside this result.

## Reproduce

CPython **3.11.2**, standard library only. Use a checkout of this repository:
the authenticated dependency directory must be its sibling.
From the repository root, run sequentially:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B constant_weight_a18_6_5_special_circle_gap_barrier/controls.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B constant_weight_a18_6_5_special_circle_gap_barrier/reproduce.py --checks-dir /tmp/a18-special-circle-checks
```

The full replay takes approximately 35--40 minutes on the author's one-CPU
scope. See [VALIDATION.md](VALIDATION.md) for measured final-source results.
Only one mathematical job is run at a time. No resource guard is enlarged.
Append `--resume` to reuse local checkpoints **only with identical source
and input fingerprints**. A fresh independent reproduction should use an
empty checks directory. Use `--from-case I --to-case J` for a partial batch:
its output states `specifiedintervalonly`, and is never a full-cohort verdict.
`--normalization-only` checks group/geometry, the two normalization carriers,
imported orbit covers and the three literal fixtures, without excluding
any seven-gap completions.

The complete mathematical summary must equal [expected.json](expected.json),
including canonical manifest SHA256

```
58412a26940d0559787cda4ac4ca821f5c7d3ff784aa6890002ece185c09cc27
```

The normalization case digest is
`059c824c218087110cf493136c2e1a7ee8f8eab824bf863bb7e6ea9fd8b81d31`.
These hashes bind ordered streams, without proving completeness by themselves.
A whole-cohort summary requires all 1,763 cases; interrupted runs, guards,
errors and positive witnesses cannot produce it.

## Source, evidence and reuse

* [normalize.py](normalize.py) generates 1,953 pointed inputs and separately
  covers the full labeled universe with literal coordinate transports.
* [reproduce.py](reproduce.py) compares both complete record streams and all
  projection rows, then runs both exact seven-target algorithms.
* [imports.py](imports.py) audits explicitly imported bounds/actual covers.
* [fixtures.py](fixtures.py) checks the three [68-word fixtures](fixtures.json)
  directly, including all pair distances and actual ownership.
* [controls.py](controls.py) checks small graph counts against literal
  subsets, accepts positive seven-cliques as witnesses and rejects corrupt
  fixtures. [DEPENDENCIES.json](DEPENDENCIES.json) pins all reused source bytes.

The shared [classical-extension source](../constant_weight_a18_6_5_steiner_extension_barrier)
supplies the previously published geometry, group, record enumeration,
projection and clique algorithms. Those primitives are credited to their
earlier publications; the new claim is the incidence-defined restricted
cohort and its complete seven-gap exclusion. The earlier numerical linear
envelope is not a premise. Smaller-gap and two-word computational lemmas
remain explicit mathematical dependencies, rather than being silently
replaced by reading their JSON summaries.

Exact integers and sets, shared input geometry/group, imported finite
lemmas and unformalized normalization/record/clique/counting bridges are
the trust boundaries. This is neither formal proof-assistant verification
nor independent peer review. Source publication alone does not prove the
theorem. Raw proof corpora, adjacency matrices, per-case checkpoints, logs
and binaries are regenerable private outputs and are omitted from Git.
