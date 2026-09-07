# R(5,5): physical completion of the full-support rank-four profile

No good 43-vertex graph exists in the following complete fixed-cut family.
Split the vertices as 20+23 and factor the red cross matrix over
`F_2` in rank four. On each side every one of the 15 nonzero labels occurs;
five row labels and eight column labels occur twice. All 443 edges within the
two sides are arbitrary.

The new computation excludes every non-affine choice of the eight doubled
column labels. It covers 19,279,260 pairs of doubled-label sets through 1,348
dual-`GL(4,2)` orbits. Every orbit formula has 443 physical variables and was
refuted by a DRAT proof checked with `drat-trim`. Together with the previously
accepted affine-hyperplane exclusion at Discovery Net h3757/h3761, this closes
the entire full-support multiplicity profile.

This profile has no zero labels and every label class has size at most two, so
it passes the all-pattern class caps accepted at h3775 and the stronger row cap
proved at h3783. The h3771 contact sieve can remove some cross matrices before
completion; the census here proves the stronger statement for the whole
profile and therefore excludes its entire intersection with the h3771 retained
interface.

This is a structured family exclusion. It does not construct a good43, prove
that every good43 has a rank-four cut, or improve the Ramsey lower bound.
Other support and multiplicity profiles in the retained rank-four family
remain open.

See [PROOF.md](PROOF.md) for the reduction and [VALIDATION.md](VALIDATION.md)
for evidence and trust boundaries. Compact verification is:

```sh
python3 -B reproduce.py
```

Expected status:

```text
VERIFIED_COMPACT_FULL_SUPPORT_RANK4_EXCLUSION
```

Full proof replay requires CaDiCaL 3.0.1 at commit
`c60730422e758ef1cebe7aeddf2dda31c996bf04` and `drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Run four independent commands
from this directory with an empty external output directory:

```sh
python3 -B proof_replay.py --solver /path/to/cadical --checker /path/to/drat-trim --exploration orbits_complete.json --manifest /tmp/r55-full-support/shard0.jsonl --summary /tmp/r55-full-support/summary0.json --shards 4 --shard-index 0
python3 -B proof_replay.py --solver /path/to/cadical --checker /path/to/drat-trim --exploration orbits_complete.json --manifest /tmp/r55-full-support/shard1.jsonl --summary /tmp/r55-full-support/summary1.json --shards 4 --shard-index 1
python3 -B proof_replay.py --solver /path/to/cadical --checker /path/to/drat-trim --exploration orbits_complete.json --manifest /tmp/r55-full-support/shard2.jsonl --summary /tmp/r55-full-support/summary2.json --shards 4 --shard-index 2
python3 -B proof_replay.py --solver /path/to/cadical --checker /path/to/drat-trim --exploration orbits_complete.json --manifest /tmp/r55-full-support/shard3.jsonl --summary /tmp/r55-full-support/summary3.json --shards 4 --shard-index 3
```

The public manifests give the expected formula and proof hashes. Generated
CNFs and proofs total about 8.61 GB and are deliberately omitted; the replay
regenerates and checks them one case at a time.
