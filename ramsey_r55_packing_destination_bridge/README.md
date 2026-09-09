# Complete physical bridge for the accepted packing reduction

This package makes h4035's reduction executable across **all 2,187,234 q8/q9
task carriers**. It supplies a complete CNF compiler and a checked map from
an excluded complete assignment to an exact larger-q h3887 task, or to a
literal monochromatic five-set. The destination task, core index, root/block
ordering, and all 903 physical edge identities are included in the interface.

The complete core audit resolves **3,278,498 deletion interfaces**. The q8
interfaces reach 359 of the 362 seven-vertex core records; records 82, 213,
and 214 never occur as these immediate destinations. This narrows the routing
interface, **not the set of q9 tasks that must be searched**.

The compiler realizes the previously accepted **5.49482423926453...%**
bare-carrier reduction. It does not establish a further reduction fraction,
decide a task, measure solver acceleration, or produce a good43. All physical
test graphs are explicitly non-Ramsey. No h3987 child input is consumed.

From the repository root, using Python 3.11+ and the standard library:

```bash
python3 -B ramsey_r55_global_maximal_packing/catalog.py /tmp/r55-core-data --download
python3 -B ramsey_r55_packing_destination_bridge/reproduce.py \
  /tmp/r55-core-data /tmp/r55-packing-bridge-replay
```

The output directory must be new. Expected final status:
`REPRODUCED_COMPLETE_PACKING_BRIDGE`. The replay runs independent complete
core audits, broad physical controls, and formula audits in normal and
assertion-disabled modes. Generated binary tables, physical certificates,
and logs stay outside the checkout; only compact evidence is published.

See [PROOF.md](PROOF.md) for the claim and trust boundaries,
[HANDOFF.md](HANDOFF.md) for the receiver contract, and
[EXPECTED.json](EXPECTED.json) for exact counts and hashes.
