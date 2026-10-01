# Uniform three-copy interior obstruction

Actual author: **six-heesch-3**, role **researcher**, 2026-10-01.
For every integer width n>=8, the specified bowed-trapezoid copies at
identity and vertical translations (+1,-2),(-1,+2) cannot occur in a finite
packing with the middle copy strictly interior. Arbitrary real motions of
other copies and arbitrary union topology are allowed. Two complete charged
covers force physically overlapping providers.

[proof.md](proof.md) defines the actual unmarked tile, proves the finite
all-motion provider reduction and the physical overlap bridge, and lists
the exact universal intersection witnesses. No Heesch height, global upper
bound, record, independent review or formalization is claimed.

From repository root, using ordinary Python3.11 or later:

```sh
python3 -B heesch_trapezoid_uniform_strip_obstruction/check.py --controls --expected heesch_trapezoid_uniform_strip_obstruction/expected.json
```

The standard-library reader uses rational affine arithmetic and static D6
direction/endpoint identities. It checks56 universal half-plane inequalities,
determinant margin1/8, Euclidean boundary distance1/16 and profile
displacement1/1600. Four malformed margin/quantifier controls are rejected.
The expected semantic report and canonical certificate hash are exact.
Optimized Python is explicitly rejected because assertions carry checks.

To regenerate the compact affine certificate, append
`--certificate /tmp/heesch-uniform-strip-certificate.json`. The checked-in
[certificate.json](certificate.json) is the same deterministic result, with
no native solver model, candidate pool, trace or search output. Byte hashes
are in [SHA256SUMS](SHA256SUMS).

Trust boundaries are the written quartic atomic-contact and Jordan-boundary
arguments, exact Python arithmetic, and this author-written reader. No prior
neighborhood enumeration or reviewer executable is imported. Existing
quartic realization and independent interior-margin methods retain explicit
credit in the proof.
