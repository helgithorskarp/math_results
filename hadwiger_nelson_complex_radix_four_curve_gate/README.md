# Exact four-active-curve gate for the complex-radix frontier

HN2's collision theorem closes every noninjective member of the 243-point
complex-radix architecture.  This package strengthens the remaining injective
incidence condition by classifying exactly when four active event curves can
block all 256 additive F4 colour words.

The result is:

- only 91 residue-signature patterns can support an exactly-four-active
  obstruction: 81 without the radial circle and 10 with it;
- these signatures lift to 960,848 eligible curve quartets, before any claim
  of geometric concurrence or non-four-colourability;
- only 2,554 of the 132,130 D3 pair-system orbits can occur inside one of those
  quartets, with total Bezout allowance 156,176;
- the other 129,576 pair orbits force at least five active curves at any
  non-four-colourable parameter lying on that pair.

The compact [exact_four_interface.json](exact_four_interface.json) lists all 91
signature patterns and all 2,554 compatible pair representatives in the stable
curve IDs of HN2's source inventory.

## Reproduce

From this directory, with CPython 3.11 or later and no third-party package:

```sh
python3 -B verify.py --check-expected
python3 -B controls.py
python3 -B produce.py --out /tmp/hn_four_curve_certificate.json
python3 -B export_interface.py --out /tmp/hn_exact_four_interface.json
sha256sum /tmp/hn_four_curve_certificate.json certificate.json
sha256sum /tmp/hn_exact_four_interface.json exact_four_interface.json
```

The certificate hash is
`fdc7e4279131200deb150241ae576780340b0d284e0b1a6c46e0d9bdd639f645`.
The 30,225-byte explicit-interface hash is
`76c806cdb5458bbc45e730f7dcd9e3231d6ffc6f4dc99c2013e0f19966c562eb`.

The producer uses displacement residues.  The verifier instead constructs all
256 label colourings, derives every curve's failure mask directly from its
actual edge group, recovers the hyperplane partitions by disjointness, and
reconstructs D3 using exact rational substitutions in the event polynomials.

## Scope

This is a necessary-condition and exact-interface theorem.  It neither proves
that an eligible quartet is geometrically concurrent nor that any represented
graph is non-four-colourable.  It performs no physical chromatic search,
produces no candidate, and does not improve the 509-vertex record.
