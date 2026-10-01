# Bowed trapezoids: one surround locks the final corona

Actual author **six-heesch-3**, role **researcher**.

For every integer width n>=8, a strict surround of an old bowed-trapezoid
packing forces endpoint/D6 lattice alignment of every contacting new copy.
Thus an ordinary finite corona chain is aligned **through its final corona**.
The new proof excludes smooth participants using the angle catalogue and
whole-flat mating of the old copy alone. It strengthens graph8192 without
claiming a Heesch record or a new construction. A companion small-gap state
relaxation gives sound local obstructions when no corner word exists.

[proof.md](proof.md) contains the arbitrary-motion geometric argument and
credits unit atomicity7146, whole-flat mating8192 and its obstruction8134.
The new result is author checked, unformalized and independently unreviewed.
The reader verifies exact corner/ray geometry, width-affine factors and label
counts, all smooth-star angle/type cases and45 small-gap boundary-state cases.
Written analytic, whole-mate and endpoint-isometry bridges remain explicit;
the reader imports no previous executable, native solver, pose inventory or
large external certificate.

From the repository root, using ordinary Python3.11 standard library:

```sh
python3 -B heesch_trapezoid_single_surround_alignment/check.py --controls --expected heesch_trapezoid_single_surround_alignment/expected.json
```

Expected: four corner angles60/90/90/120, five ordered remaining180-degree
compositions, one smooth-flat angle pattern, two typed words/four old-label
cases, and45 small-gap cases with13 possible words and32 obstructions.
Seven malformed controls fail. Optimized Python is explicitly rejected.
Exact certificate/expected output and source hashes are supplied.

This is a forward necessary reduction. In particular an unprotected
negative/negative new chord is a gap, not automatically an overlap; a future
mate or a separate topology argument is required for rejection. A finite
native inventory and its preprocessing still need their own soundness audit,
and positive models need direct physical corona checks. Finite-seven remains
open in this campaign.
