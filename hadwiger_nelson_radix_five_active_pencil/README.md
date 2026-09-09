# Exact five-active pencil frontier for A5(z)

This package exactly classifies the residue-cover geometry of a possible
counterexample with exactly five active noncircle curves in

```text
A5(z) = T + zT + z^2T + z^3T + z^4T,
T = {0,1,(1+i sqrt(3))/2}.
```

Five affine hyperplanes over F4 cover `F4^4` in exactly two ways: four
parallel sections plus an arbitrary fifth hyperplane, or the five-member
pencil through an affine codimension-two flat. HN3 h4165 excludes the first
form from simultaneous curve incidence. Of 5,712 abstract pencils, 5,382 use
only the 336 realized event signatures.

The realized pencils lift to 136,094,976 curve quintets. All 3,006 h4151 K4
sets lie inside one parallel class and therefore occur in no pencil. HN2
h4167's pair rules remove no pencil lift, while its triple rules remove
3,862,080, leaving 132,232,896 exact incidence survivors. Every one of the
5,382 pencils remains nonempty. These are necessary combinatorial survivors,
not asserted concurrent or physical five-chromatic graphs.

On the global h4117 quotient after the accepted circle closure and h4167 pair
filter, 2,740 of 131,356 pair representatives cannot belong to an exact-five
pencil and therefore require at least six active curves: 2,096 have parallel
signatures and 644 determine a pencil containing an unrealized signature.
The exact-five layer retains 128,616 representatives with conservative Bezout
allowance 7,585,472. This classification is D3-invariant. It does not delete
the 2,740 systems from the six-or-more-active frontier.

From the repository root, with standard-library CPython 3.11.2:

```sh
python3 -B hadwiger_nelson_radix_five_active_pencil/verify.py --check-expected
python3 -O -B hadwiger_nelson_radix_five_active_pencil/verify.py --check-expected
python3 -B hadwiger_nelson_radix_five_active_pencil/controls.py
python3 -B hadwiger_nelson_radix_five_active_pencil/produce.py \
  --out /tmp/hn-five-pencil-certificate.json \
  --export-interface /tmp/hn-five-pencil-interface.json
```

Output paths for the producer and export must not exist. The explicit
6,200,577-byte interface is regenerated rather than committed. It lists all
realized pencil signatures, all curve signatures, the three pair-orbit modes,
and a constraint-avoiding five-curve extension for every compatible pair.
See [HANDOFF.md](HANDOFF.md) for the HN2 boundary and [PROOF.md](PROOF.md) for
the exact classification.

Reviewer-1 independently accepted the h4167 incidence exclusions at h4169;
h4165 remains an explicit author-checked dependency. This is an exact frontier
stratification, not a physical candidate, a closure
of the six-active branch, or an improvement to the 509-vertex record.
