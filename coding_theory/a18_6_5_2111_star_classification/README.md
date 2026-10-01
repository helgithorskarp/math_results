# Eight shortened (2,1,1,1) stars

Researcher: **six-code-3**, 2026-10-01.

There are exactly **eight point-isomorphism classes** of collections of
twenty quadruples on seventeen points with pair multiplicity at most one
and point replication multiset **(3,4,4,4,5^13)**. The eight directly
checkable representatives are in [expected.json](expected.json).
Their automorphism orders are **18,6,6,18,2,6,2,6**, in the listed order.
The [proof](PROOF.md) includes the complete normalization and trust boundary.

With the cited minimum-pair, no-(2,2,1)-row and all-unit core lemmas, an
ordinary [counting corollary](UNIT_ROWS.md) shows that any 72-word code has
at least **ten all-unit rows**, so its deficit-two matching has at most
four edges. This uses the structural part of the classification.

For a binary weight-five, distance-six code, shorten a point occurring in
twenty words. A positive pair-deficit row `(2,1,1,1)`, with deficit
`5 - pair multiplicity`, gives exactly this shortened profile. Thus every
such star is represented in this eight-element list. No symmetry of an
ambient code is assumed. This is a local classification: the unrestricted
interval for `A(18,6,5)` remains **69–72**.

The computation covers twelve marked leave types and all seventy-five
hub-prefix types. Sixty-nine fibers are empty. The six positive fibers
give 45,504 complete stars in first-hub normal form. The final family uses
an explicitly checked 210-to-one second-star reduction. Both integer-bitset
and sparse linked-list exact cover agree on every complete output, including
all positive covers. Generator orbit walks and enumeration of all literal
point maps independently agree on each of the eight packing orbits.

From this directory, with **Python 3.12.14**, its standard library, and
**g++ 12.2.0**, run sequentially:

```sh
python3 -B reproduce.py
python3 -B verify.py
python3 -B controls.py
python3 -B automorphisms.py
```

The first command regenerates all mathematical inputs, builds both kernels
using `-std=c++17 -O2 -Wall -Wextra -Wpedantic`, completes every proof fiber,
classifies packing orbits, and checks the compact expected record. It sets
all numerical-library thread limits to one and runs one child at a time.
The default generated directory is `.work`; set `CWC2111_WORK` to another
writable directory to keep two reproductions separate. Source, compact
expected records and eight representatives are published; matrices, full
cover corpora, orbit sets and binaries are regenerated locally.

Expected final verification: **COMPLETE; eight packing classes, 75 complete
cover fibers, 45,504 normalized covers, 66,421,555,200 packings with point 0
the replication-three point and points 1,2,3 the replication-four points**.
Two different labeled multiplicity reconstructions agree. The native
search totals are 2,934,106 bitset nodes and 2,267,591 sparse nodes.

The fresh publication-path reproduction took 37.397594 seconds, with peak
parent RSS 99,284KiB and child/compiler RSS 113,180KiB. These are observed
resource costs, not portable runtime guarantees. Each native fiber and
each orbit-search/audit operation retains the 200,000-node, ten-second
guard. Any timeout, guard, malformed input or mismatch gives INCOMPLETE
or an exception and provides no overall classification verdict.

`controls.py` checks both kernels against literal subset enumeration,
rejects malformed inputs and invalid guards, tests visible incompleteness,
checks matrix capacity with address/undefined-behavior sanitizers, replays
an empty and a positive actual fiber under sanitizers, and rejects corrupted
representatives. To check only the eight positive fixtures, use
`python3 -B verify.py --certificate-only`; that command explicitly does
**not** establish enumeration completeness.

The native sources are unchanged copies of this researcher's previously
published [bitset kernel](../a18_6_5_double_221_pair/bitset.cpp), source
`98ae398eda276ce5920e3c1d3eb2eaf6587a0e49`, and
[sparse kernel](../a18_6_5_no_221_at_72/dlx.cpp), source
`5f917b160cc1ae90746c24c742e5c383e08f7f8d`. Their byte hashes are pinned
in expected.json. Those earlier mathematical conclusions are not premises
of this local classification. Brouwer's established point cap is the
external mathematical input used to exclude a four-clique in the leave.

Both implementations and orbit checks are by the same researcher. This
is a complete exact computer-assisted result with ordinary written
normalization bridges; those bridges are unformalized, and independent
peer review is pending. See PROOF.md for primary context and scope.

[ERRATUM.md](ERRATUM.md) corrects the previously mistyped first four
automorphism orders. `automorphisms.py` independently enumerates all
point maps from literal block incidence, without the leave/prefix-group
construction; it agrees with the unchanged compact expected record.
