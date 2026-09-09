# Four-cover event curves never concur in the complex-radix architecture

This package closes the exactly-four-active branch of

```text
A5(z) = T + zT + z^2T + z^3T + z^4T,
T = {0,1,(1+i sqrt(3))/2}.
```

HN3 h4135 found 960,768 quartets of noncircle event curves whose failure
hyperplanes can cover all 256 additive F4 colour words. HN2 h4151 subsequently
closed their exactly-four chromatic obligation, using F3 colourings for 934,632
quartets and planar K4 obstructions for 26,136. The present exact result is a
strict geometric strengthening: none of the 960,768 quartets has a common point
even over the complex affine parameter plane.

Thus all 960,768 quartets become forbidden simultaneous-incidence constraints
even inside a larger active set. This extends h4151's reusable K4 interface,
whose independently sufficient 2,376 triples cover only the 26,136 K4 cases.
The shared consequence remains that every injective non-four-colourable member
must activate at least five event curves.

The proof uses only CPython integer arithmetic.  At the prime 1,000,003 it
reconstructs exact projected resultants by evaluation and interpolation.  The
projection `t=x+2y` excludes 960,698 quartets and leaves 70 modular suspects;
`t=x+3y` leaves two, and `t=x+4y` excludes both.  Every projected resultant is
required to attain its sharp characteristic-zero degree bound, so a modular
gcd of one is a rigorous coprimality certificate over the rationals.

From the repository root:

```sh
python3 -B hadwiger_nelson_complex_radix_four_concurrence/verify.py --processes 8 --check-expected
python3 -O -B hadwiger_nelson_complex_radix_four_concurrence/verify.py --processes 8 --check-expected
python3 -B hadwiger_nelson_complex_radix_four_concurrence/controls.py
python3 -B hadwiger_nelson_complex_radix_four_concurrence/produce.py --out /tmp/four-concurrence.json --processes 8
```

The compact [certificate](certificate.json) is 2,838 bytes with SHA256
`9c2d6c362a4b8d206ac1aa8f141d9b093285f453c390ae7a75adba72d34ce3c6`.
The producer derives curve signatures from displacement residues.  The verifier
instead derives them from all actual edge-failure masks.  Its resultant engine
is separately checked against direct Sylvester determinants.

This is an exact geometric viability improvement, not a physical candidate or
a record improvement. It does not remove any pair-system orbit: a parameter
on one of the former 2,528 exactly-four-compatible systems might still activate
five or more curves. [FRONTIER_EFFECT.json](FRONTIER_EFFECT.json) gives the
precise higher-incidence interface and preserves that warning.
