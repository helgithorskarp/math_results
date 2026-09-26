# The three extremal types containing a six-point plane

Every 70-point line-free subset of `F_5^3` that has **at least one**
six-point affine plane section is affinely equivalent to exactly one of
the three supplied constructions. They have respectively 5, 7, and 4
six-point planes, have coordinate sum zero, and are inclusion-maximal.
Every six-point section is a six-arc: no three of its points are collinear.

This strengthens the earlier [two-six-plane classification](../two_six_extremals70/README.md).
The new proof uses exhaustive section completion and bipartite matchings;
it does not use SAT exclusions or the earlier classification as premises.
All 104 normalized solutions have explicit checked affine maps from the
three seeds. No symmetry of an unknown point set is assumed.

As a separate conditional corollary, every plane in a hypothetical
71-point line-free set would contain at least eight points: deleting
a point from a seven-point section would produce one of the maximal
70-point sets above. The team's [complete author proof of the exact value
70](../decision71/README.md) is separate; this classification does not
independently verify its full exclusion. Independent review of this new
classification is pending.

## Reproduce

Requires Python 3.10 or later and a C++20 compiler named `g++`. The proof
replay uses only the Python and C++ standard libraries. From the repository root:

```sh
python3 -O affine_line_free_f5_3/one_six_extremals70/verify.py --out /tmp/one-six --jobs 2
python3 -O affine_line_free_f5_3/one_six_extremals70/validate.py --domain /tmp/one-six
```

Expected status: `ONE_SIX_EXTREMALS70_VERIFIED`, with 676,318,125
section pairs checked and exactly 104 normalized solutions. The independent
reference comparison reports `MATCHING_REFERENCE_AUDIT_PASSED` on 2,104
cases. All deterministic census counts are in [EXPECTED.json](EXPECTED.json).
The raw menus, intermediate pairs, and executables remain in the specified
output directory. They are not committed.

`--sanitize` enables AddressSanitizer and UndefinedBehaviorSanitizer for a
complete replay; it is slower. `--jobs 1` runs serially. For an optional
independent Boolean check of all 42,726 matching-size-18 cases in the two
validation section types, install `python-sat==1.9.dev15` and run:

```sh
python3 -O affine_line_free_f5_3/one_six_extremals70/validate.py --domain /tmp/one-six --solver-audit
```

This optional solver check is validation, not a premise of the theorem.
See [PROOF.md](PROOF.md), [VALIDATION.md](VALIDATION.md), and
[SOURCES.md](SOURCES.md) for coverage, attribution, and trust boundaries.
`derive_maps.py` can rediscover the affine certificates; the main verifier
only applies the certificates and checks their images.
