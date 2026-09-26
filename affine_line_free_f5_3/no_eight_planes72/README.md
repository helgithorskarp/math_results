# No eight-point planes at cardinality 72

Every 72-point subset of \(\mathbb F_5^3\) with no complete affine
line meets each affine plane in at least nine points. This is an exact
computer-assisted structural theorem. It leaves only BBB in the earlier
global case cover. Combined with Team A researcher 1's new
[weighted bound](../nine_plane_frame72/THEOREM.md), it forces at least
eleven nine-point planes. The current
numerical interval remains \(70\le r_5(\mathbb F_5^3)\le72\).

The [complete proof](THEOREM.md) reduces any remaining eight-point plane
to a mixed eight/nine-plane projection. Two different exact enumerations
agree on all 5,428 normalized projections. The earlier two-eight-plane
lemma excludes 144 of them. The other 5,284 form 1,252 affine classes;
every lifting formula has an UNSAT proof checked separately by DRAT-trim.

## Reproduce the new reduction and lifting proofs

Requires Python 3.10+, GCC with C++20 support, and
`python-sat==1.9.dev15`. Tested with Python 3.12.14 and GCC 12.2.0.
From this directory:

```sh
python3 -m pip install -r requirements.txt
python3 verify.py --out /tmp/no-eight-verify
```

Expected status: `NO_EIGHT_PLANE_REDUCTION_VERIFIED`. This checks both
enumerations entry by entry, the full affine partition, independent
geometry and group-action controls, the known 70-point positive control,
the planar upper bound 16, and all 1,252 proof-input hashes. It does
**not** regenerate the UNSAT proofs. Their checked production record is
in [certificates.jsonl](certificates.jsonl); [validation.json](validation.json)
records the run and controls.

Use the official [DRAT-trim](https://github.com/marijnheule/drat-trim)
checker, tested at source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. After building it:

```sh
python3 replay.py --out /tmp/no-eight-proofs --drat-trim /path/to/drat-trim
```

This regenerates and checks all 1,252 proofs. UNKNOWN, a changed input,
a failed checker or a SAT witness stops the run. A SAT witness is saved
and checked directly against all geometric constraints. The default
conflict budget is 500,000 per case; it is a stopping limit, never a
criterion for accepting an exclusion.

For two disjoint workers, use separate output directories with intervals
`--start 0 --stop 626` and `--start 626 --stop 1252`. Each case is
independent. A partial interval is explicitly reported as incomplete;
both complete intervals are needed for a full replay. Individual case
JSONs allow a failed or interrupted case interval to be rerun explicitly.

Raw CNFs, proof traces and checker logs are intentionally omitted from
Git. The manifest records their SHA256 hashes and proof sizes; the source
regenerates all of them. The original mixed proofs total 1,963,456,313
bytes. Their solver/checker times sum to 1,395.64 seconds across the
partitioned run, excluding formula generation; the largest case used
13,042 conflicts. Proof bytes may differ between solver builds;
each regenerated proof must pass the checker against the matching CNF.
The exact input hashes, rather than a particular solver's search path,
identify the finite claims being proved.

The pinned PySAT version's `get_proof()` can read an unflushed native
stream; its binary-to-text helper also failed during the preceding AA
computation. The runner flushes the native stream, preserves its binary
bytes, and asks DRAT-trim to parse and check them. It never substitutes a
solver verdict for a successful proof check.

## Dependencies and scope

The theorem uses the
[two-eight-plane exclusion](../two_eight_planes72/README.md) and the
[global low-plane theorem](../low_planes72/README.md). Those packages
contain their own written reductions, manifests and replay commands.
For a complete reproduction of the dependency chain, also run:

```sh
python3 ../two_eight_planes72/verify.py --out /tmp/two-eight-verify
python3 ../two_eight_planes72/replay.py --out /tmp/two-eight-proofs --drat-trim /path/to/drat-trim
python3 ../low_planes72/verify.py --out /tmp/global-low-planes-verify
```

The stronger nine-plane count additionally uses
[the weighted incidence certificate](../nine_plane_frame72/README.md).
The new verifier replays that certificate and its geometric controls.
That teammate result already supplied a complete BBB normal form without
excluding eight-point planes; this package proves that no such planes
can occur at all.

The local `model.py` is byte-identical to the already published AA
generator. The new mathematical work is the complete mixed catalogue,
its affine reduction, and all its checked lifting exclusions. No
assumption that every admissible quotient is realizable is made.

The proof still trusts ordinary compiled enumeration code, the written
mathematical reductions, the affine canonicalizer, the pinned cardinality
encoder and DRAT-trim. It is not a proof-assistant formalization and has
not received independent peer review.

The principal literature source is Elsholtz et al.,
[*Maximal line-free sets in* \(\mathbb F_p^n\)](https://arxiv.org/abs/2310.03382v2),
Periodica Mathematica Hungarica 90 (2025), 7–21,
[DOI](https://doi.org/10.1007/s10998-024-00617-x). This checkpoint continues
the repository's [upper bound 72](../upper_bound72.md). Targeted literature
and committed-graph checks found no duplicate of this structural result;
no priority claim is intended.
