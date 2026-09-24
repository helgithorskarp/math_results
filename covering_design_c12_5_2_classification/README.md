# The 107 optimal (12,5,2) coverings

**Exact classification.** Up to permutation of the twelve points, there are
exactly **107** nine-block `(12,5,2)` coverings. Their degree profiles are:

| Point degrees | Isomorphism classes |
|---|---:|
| `(4^9,3^3)` | 53 |
| `(5,4^7,3^4)` | 46 |
| `(5^2,4^5,3^5)` | 6 |
| `(5^3,4^3,3^6)` | 2 |

There are **13,531,795,200** such coverings on a fixed labelled twelve-point
set, with the nine blocks unordered. Marking a point of degree 3, 4, or 5
gives respectively **306, 592, or 56** isomorphism classes.

[CATALOGUE.json](CATALOGUE.json) contains all representatives, their
automorphism orders, and their point orbits. Each representative has both
12 point signatures (bit positions are the nine blocks) and nine block masks
(bit positions are the twelve points). Indexing starts at zero.

The proof uses the previously established
[maximum point degree five theorem](../covering_design_c12_5_2_link_degree_bound/).
The new enumeration is exact integer computation. An independent search
compares complete labelled answer sets, and NetworkX independently checks
the reduced types, nonisomorphism, automorphism orders, and point orbits.

## Reproduce

The primary proof needs Python 3.11 or later and no packages:

```bash
python3 verify.py > actual.json
diff -u EXPECTED.json actual.json
sha256sum -c SHA256SUMS
```

The independent checks were run with Python 3.12.14 and NetworkX 3.7:

```bash
python3.12 -m venv /tmp/c12-cover-audit
/tmp/c12-cover-audit/bin/pip install -r requirements-audit.txt
/tmp/c12-cover-audit/bin/python audit.py > actual_audit.json
diff -u AUDIT_EXPECTED.json actual_audit.json
/tmp/c12-cover-audit/bin/python marked_five.py > actual_marked.json
diff -u MARKED_EXPECTED.json actual_marked.json
/tmp/c12-cover-audit/bin/python validate.py
```

The primary run takes about ten seconds; the independent checks take a few
minutes in total. See [VALIDATION.json](VALIDATION.json) for measured costs.
Successful statuses are `VERIFIED_107_OPTIMAL_C12_5_2_CLASSES`,
`INDEPENDENT_107_CLASS_AUDIT_PASSED`, and
`INDEPENDENT_MARKED_DEGREE5_CENSUS_PASSED`.

The canonical catalogue digest, distinct from its pretty-printed file hash,
is `0625eb0738454c54f50869b9dbe2421301d6721787cd005d22b29d4fe2264d7e`.

## Application and scope

Every degree-nine point of a twenty-block `(13,6,3)` covering has one of
these 107 links. For the remaining global degree profile `(11,10,9^11)`,
some degree-nine point shares five blocks with the degree-eleven point.
Thus only **56 pointed link classes** need be considered at that pair;
see [PROOF.md](PROOF.md) for the counting argument.

This catalogue enables complete compatibility tests between several point
links. It does not exclude either remaining global degree profile and does
not decide whether `C(13,6,3)` is 20 or 21.

The maximum-degree-five prerequisite is an imported computer-assisted result
with independent review; its upstream SAT certificates are not replayed
here. The independent algorithms in this directory are internal checks,
not external peer review or proof-assistant formalization. The precise
reduction and trust boundaries are in [PROOF.md](PROOF.md), and the bounded
literature and graph context is in [SOURCES.md](SOURCES.md).
