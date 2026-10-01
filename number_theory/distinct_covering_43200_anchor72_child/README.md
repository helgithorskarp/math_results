# One nineteen-class covering exclusion at ambient period43200

Actual author **six-covering-3**, role **researcher**.

The explicit nineteen-class parent in [proof.md](proof.md) has no distinct
covering completion with moduli>=8 dividing43200. Its minimum is exactly8;
actualLCM need only divide the ambient period. A complete missing72 split
has42 orbits, excluded by twenty stored integer weights. The related two
parents receive only the structural42-orbit reduction. Global bounds and
the whole-period covering question are unchanged.

From the repository root, Python>=3.10, standard library only:

```sh
python3 -B number_theory/distinct_covering_43200_anchor72_child/check.py --controls
python3 -B -O number_theory/distinct_covering_43200_anchor72_child/check.py --controls
```

Expected:42 representative children excluded,72 raw phases accounted for,
smallest stored physical gap72,1,160 resource instances,3,135,840 phase
buckets,76,800 union cases, and17 rejected controls across the two checkers.
[expected.json](expected.json) records exact event hashes. The20-second
loop cap fails on incomplete checking; `--phase a` proves only that child.

[input.json](input.json) is a19,419-byte fixture with203 literal Cartesian
boxes and1839 sparse coefficients for twenty weights. No solver or private
input is required. Written proof and author checks are complete; independent
review and formalization are pending. [SHA256SUMS](SHA256SUMS) records the
published source hashes.
