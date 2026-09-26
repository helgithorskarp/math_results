# Two low planes at 71 points

Every 71-point line-free subset of \(\mathbb F_5^3\) has **two
nonparallel planes containing at most nine points each**. This gives a
complete cover of the remaining problem by **15 unordered pairs of five
normalized parallel profiles**. Every covered projection has an interior
\(4\times4\) deficit sum at most 11 and admits a three-hole affine height
normalization.

The [proof](THEOREM.md) combines the finite-field barycenter and quadratic
moment characters with exact plane/line incidence identities. A complete
planar census and 14 integer dual certificates establish the global
low-plane bound. The proof does not enumerate or solve the resulting
three-dimensional lifting problems.

The team's separate [upper-bound proof](../upper_bound71/README.md) gives
\(70\le r_5(\mathbb F_5^3)\le71\), with independent review pending.
Existence at 71 remains unresolved here. The theorem in this directory
does not depend on that upper-bound proof.

Run from this directory with Python 3.11 or later and a C++20 compiler:

```sh
python3 verify.py --out /tmp/low-pair71
cmp /tmp/low-pair71/summary.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected status: `LOW_PAIR71_VERIFIED`. The replay checks:

- All \(2^{25}\) labeled planar subsets, including the complete size-17
  exclusion, and all 91 permitted section spectra.
- All 85 centered ordered profiles, generated again using deficit
  compositions, and every symmetric \(3\times3\) matrix over \(\mathbb F_5\).
- All 14 cases of a 71-by-698 integer system, checking the dual inequality
  separately on every column.
- The five low-plane profile types, their 15 pair types, the interior
  deficit bounds, and incidence identities on 20 arbitrary 71-subsets.

The weakest certificate gives
\(a_7+a_8+a_9\ge117641713/100000000>1\).
The integer lower bounds in the seven moment classes are
\(2,3,2,2,3,2,2\); the zero form improves to four when the barycenter is
selected. In the zero-form case all low planes have size seven, contain
the barycenter, and their normal directions form an arc of size at most
six.

Python 3.11.2, Python 3.11.2 with `-O`, and Python 3.12.14 produced
identical summaries. GCC 12.2.0 was used. Ordinary complete replay takes
about seven seconds on the author machine. The complete AddressSanitizer
and UndefinedBehaviorSanitizer replay passed in about 22 seconds.
Peak child memory across these builds and checks was about 131 MiB.
A changed multiplier, a missing case, and a negative denominator were
each rejected.

To repeat the checking build:

```sh
python3 verify.py --sanitize --out /tmp/low-pair71-sanitize
cmp /tmp/low-pair71-sanitize/summary.json EXPECTED.json
```

The optional discovery script requires the packages in
[requirements-discovery.txt](requirements-discovery.txt):

```sh
python3 discover.py --out /tmp/low-pair71-rediscovered.json
python3 verify.py --out /tmp/low-pair71-rediscovery \
  --certificates /tmp/low-pair71-rediscovered.json
```

Discovery uses floating-point optimization, then exact rounding repair.
The theorem checker never imports NumPy, SciPy, or an optimizer. Different
valid rediscovered multipliers may have different bytes and rational
lower bounds; their integer conclusions and exact inequalities must
still pass the verifier.

The trust boundary is the written reduction, ordinary exhaustive C++
code, and ordinary exact Python code. No solver verdict, imported
classification dataset, proof-assistant formalization, or independent
peer review is claimed. Sources and prior-work attribution are in
[SOURCES.md](SOURCES.md).

Certificate SHA256:
`c1c05da8548ddb40f35db3d6cf86f9d353f468b2fd63412b18b27bc3d26833cb`.
