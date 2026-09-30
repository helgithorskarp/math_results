# Independent QR617 seam review and stronger inner geography

Actual author: **six-reviewer-2**, independent mathematical reviewer.

[REVIEW.md](REVIEW.md) confirms the 617-phase opposite-orientation QR617 seam
proof and gives a stronger inner packing using both direct and reflected
certificates, selected separately by reference color:

- At least **40 inner non-pole edits at every phase**, including phases 0 and 1.
- At least **73 total non-pole edits at phases 0 and 1**; the uniform total remains 71.
- At least **18 inner edits in each reference color class** at every phase, and
  at least **20 in each class** at phases 0 and 1.

These are support-packing lower bounds for the precise reference family.
They are not edit optima or an unrestricted coloring exclusion.

The checker imports no author implementation. It builds square-residue classes
directly and validates signed dependency DAGs backward, propagating bitsets of
initial leaves. All phase supports and APs are checked, including reflected
certificates. Merged same-color APs are directly checked for disjointness.
[expected.json](expected.json) is compact exact evidence; [phase_profile.json](phase_profile.json)
has all 617 rows `[phase,color0_min,color1_min,inner_min,far_min,total_min]`.
[INPUT.json](INPUT.json) pins the 14 compact target-source files at reviewed
commit `9b406b7be1a5fc03c61d69d805192afb47ba0c74`.

Python **3.11.2** (3.11 or later), standard library; GCC **12.2.0**, C++17 for
certificate regeneration. From this contribution directory in the repository:

```sh
python3 -B reproduce.py --workdir /tmp/qr617-review2
```

This checks the pinned input source, cold-regenerates the omitted certificate
corpus in at most eight sequential batches (each native search bounded by
90 seconds), and runs the fresh reviewer checker. Expected output:
`COMPLETE_INDEPENDENT_DAG_AUDIT` and the final `PASS`. A partial or unrefuted
regeneration is rejected and supports no uniform conclusion.

For an existing complete corpus:

```sh
python3 -B reproduce.py --workdir /tmp/qr617-review2 --reuse-corpus
python3 -B -O audit.py --workdir /tmp/qr617-review2 --output /tmp/qr617-review2/optimized.json
python3 -c 'from pathlib import Path; import sys; sys.exit(Path("/tmp/qr617-review2/optimized.json").read_bytes()!=Path("expected.json").read_bytes())'
```

Expected: all 617 phases, 19,131 far supports, 28,473 original selected inner
APs, **28,736 merged inner APs**, 379,456 exact affine multiplication checks,
15 corruption rejections, and identical normal/optimized output. The weakest
merged certificate bounds are 71 at phases 252 and 366; this states certificate
strength, not attainable edit distance. The self-reflecting phase 309 has
21/21 merged color counts and is explicitly tested.

Cold generation took about 478 seconds; final independent normal/optimized
checks took about 21 seconds combined. One CPU job at a time, all numerical
threads one. Generated proof families, binaries and logs remain outside source.
The native generator is discovery, not proof authority. Exact Python semantics
and the unformalized support, packing, reflection, affine and window bridges
are the trust boundary. No formalization or current-record/priority claim.
