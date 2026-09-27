# Complete Gaussian sign on a deep-flap rational cell

At variance one, every contraction in an explicit 96-coordinate box around
a damped depth-two simplex-flap configuration satisfies every Gaussian hinge
inequality. The anchored slice has 90 coordinates and its denominator-2048
lattice belongs to the existing rational frontier R^c_2. All sixteen masses
are 1/16; source and target coordinates each vary independently by 1/2048.
The target remains extended, and the reference has paired rank six.

The certificate proves an adverse hinge bound below -1/128 throughout
[1/512,9/32]. Its low endpoint is covered by **signed superlevel volumes**:
504 adjoining logarithmic threshold windows use 194,280 integer-verified
radial endpoints, followed by an analytic bound to threshold zero. A
source-peak bound covers the high endpoint. There is no sampled-threshold
or floating-point-sign premise.

- [Theorem, complete reduction, and scope](PROOF.md)
- [Exact cell input](CELL.json)
- [Full replay](verify.py), [radial checker](radial.py), and [middle checker](middle.py)
- [Expected record](EXPECTED.json) and [dependencies](SOURCES.md)

From this directory, standard-library Python 3.11 or later:

```sh
python3 -B verify.py
python3 -B -O verify.py
sha256sum -c SHA256SUMS
```

Expected status: `GAP_FREE_DEEP_FLAP_CELL_PASS`. Runtime is about two minutes
on one CPU. Floating-point bisection proposes rational radial brackets;
outward integer exponential arithmetic checks every bracket before use.
The 13,997,521-point reference lattice is reconstructed from 597,861 orbits.
No large witness list is omitted: the compact generator and verifier replay
all radii, grid values, and threshold knots. `--progress` prints bounded
progress; `--emit` still performs every mathematical check before emitting
an expected record.

**Author proof; independent review pending.** The earlier near-point cell
has its own [independent acceptance](../gaussian_frontier_middle_cell_review2/REVIEW.md).
That review does not cover this new radial-volume argument. The accepted
depth-one flap class remains closed; no all-depth classification is made.
This fixed-variance result supplies neither unrestricted majorisation nor
a new Kneser--Poulsen consequence.
