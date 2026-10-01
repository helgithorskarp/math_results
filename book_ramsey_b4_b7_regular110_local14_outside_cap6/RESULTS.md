# Exact results and reproduction record

Actual author **six-books-3**, role **researcher**, 2026-10-01.
All computations ran sequentially within the unchanged one-CPU,
2 GiB process scope, with numerical threads set to one. The proof
programs use exact standard-library Python integers and fractions;
the independent core audit uses C++17 integer arithmetic.

## Established scope

For a valid ten-regular red graph on 22 vertices and a root whose red
neighborhood has degrees **2^2,3^8**, the induced red graph on its eleven
blue neighbors has every degree in **{4,5,6}**. Its necessary degree
patterns are **6,6,4^9; 6,5,5,4^8; 5^4,4^7**. Existence of any pattern
is not proved. [PROOF.md](PROOF.md) supplies all incidence, relabeling,
counting and finite-coverage bridges and the credited corollaries for
fourteen-edge roots and 110-red-edge hosts. The conditional theorem
under the explicit local degrees needs neither older finite exclusion.
No complete local14, local15 or unrestricted Ramsey exclusion is claimed.

The size-eight branch is excluded analytically. In the size-seven-plus-
five branch, an additional double-low counting constraint is essential:
the uncut necessary system has a positive binary Gram realization of
rank five, recorded in [gram_control.json](gram_control.json). This
control is not a host coloring. Applying the proved constraint gives
the complete indefinite domain below.

## Complete finite coverage

The two low neighbor pairs have three fixed alignments. The eight-point
induced cubic-part graph has ten edges and the required degrees below.
The stabilizer acts on these fixed pair systems, not on an unknown host.

| Pair intersection | Cubic-part degrees | Fixed-degree graphs | Nonnegative full S0 | Stabilizer | Profiles |
|---|---|---:|---:|---:|---:|
| 2 | 1,1,3^6 | 1800 | 1260 | 1440 | 3 |
| 1 | 1,2,2,3^5 | 2765 | 2400 | 240 | 15 |
| 0 | 2^4,3^4 | 3871 | 3660 | 192 | 34 |
| Total | | 8436 | 7320 | | 52 |

The separate C++ audit visits **268435456** binary free-edge words,
namely 2^27, 2^26, 2^26. Its complete retained core sets equal those of
the prescribed-degree star census. The separate checker normalizes
all 7320 retained cores using groups reconstructed from generating
swaps. Complete comparison checks **732000** core entries against
literal adjacency and equality of the binary/star core sets.

Across all 52 profiles, seven-point miss-row candidates number 235
before the A--B necessary filters and 138 after: 99,34,5 contain zero,
one,two low points. Five-row candidates number 2658. Six-row candidates
number 1047 before the filters and 972 after; these six-row counts
are coverage data, not exclusions. Size-eight candidates number 23
before the filters and zero after, separately supported by the hand proof.

The complete selected-seven/five-pair and weighted-state census is:

| Quantity | Exact count |
|---|---:|
| Selected seven/five row pairs | 861 |
| Residual matrices | 184066 |
| Literal strictly negative integer forms checked | 184066 |
| Complete residual entries compared | 18406600 |
| Survivors | 0 |
| Distinct primitive ten-coordinate integer vectors | 259 |
| Profile references to these vectors | 268 |
| Largest absolute vector coordinate | 884 |

The whole-star generator and individual-edge checker agree on complete
selected-pair and weighted-state sets, not merely counts. Both use the
proved double-low cut when the seven-row misses neither low point.
The residual rank bound is necessary but unused: every enumerated
matrix already has a strictly negative form. The compact case records
in [expected.json](expected.json) are
`[seven_row_bitmask,five_row_bitmask,state_count,direct_cut]`.
There are zero directly impossible-cut selected cases; zero-state cases
are covered by complete weighted enumeration, not a solver status.

## Executed checks and resources

Commands are in [README.md](README.md). Times are observed local wall
seconds and are not performance guarantees. Child RSS is KiB. Where
the wrapper accumulated several sequential child measurements, the
recorded RSS is conservatively labeled as an upper bound.

| Completed job | Seconds | Peak child RSS / upper bound |
|---|---:|---:|
| C++ exhaustive binary core audit | 2.898353 | 11388 KiB |
| Initial public certificate generation | 13.027282 | 18812 KiB |
| Final full checker/generator comparison under Python -O | 27.692075 | <=26632 KiB |
| Checker with generator, census and forms imports blocked | 21.402253 | 20768 KiB |
| Final controls under Python -O | 1.375504 | <=26632 KiB |
| Fresh generation with both certificate files byte-identical | 12.586373 | <=26632 KiB |

The generator-free run checks all 184066 negative forms and all
732000 normalization entries using the completed binary audit. The
additional comparison run reconstructs the author domains and checks
all 18406600 residual entries. All jobs returned success and complete
coverage. No proof computation timed out, exceeded the scope, or
relied on floating arithmetic, an UNKNOWN result, or partial enumeration.

The controls verify 1260 roots in 252 varied ten-regular graphs after
1522 degree-preserving switches; they compare **65398 red and 73202
blue literal A--B identities**. The implied row constraints are checked
in 32499 red-cap and 69650 blue-cap cases. These control graphs need
not satisfy both book restrictions and are not candidate constructions.
All **784** abstract ordered low-pair systems and **35280** eight-point
rows confirm the structural size-eight argument. All **44100** ordered
pairs of four-subsets of ten points check the inclusion-exclusion count
behind the new double-low cut. **Eight forged certificates** are rejected
under optimized Python. The positive control is reconstructed in all
100 entries from nine binary four-point rows, its rank five is checked
with exact fractions, and all 259 published vectors have nonnegative
forms on that Gram. The control fails the new cut.

## Exact comparison pins

| Object | SHA256 |
|---|---|
| Complete selected-pair stream | 4df693ef68797955f733a59310cde29980ddd2bcd6013ff3b60ac301e5577c01 |
| Complete weighted-state/residual-matrix stream | 4555c12a0fd56a37ff11fa52bda4074b5a92f45e327d5932519999b7103bd720 |
| negative_vectors.json bytes | 02da635fa32351130a950821b05f17a7763b09322930bb059f5bf776e74587dc |
| expected.json bytes | 8462e31d487115397ec02b22c7da524c118354d84b3daa730a043ba8701c5b83 |
| Retained labeled F masks, intersection 2 | fabb8ca35f2f168e17b51a7ffd982594b1f0f590e5352bd90dce410ecf4babba |
| Retained labeled F masks, intersection 1 | db5ca670ef5be68653aaf9ce679c16d9f21bae25380e00de0caefd2da9098cbf |
| Retained labeled F masks, intersection 0 | 362bc584a750b832e33432c2547ea1175a28fab4006210f4033bcba2cdd5f0ef |

Hashes are reproducibility pins, not substitutes for complete enumeration
or checked negative forms. Raw binary/core and residual-matrix corpora
are regenerated from the compact source and are not published.

## Provenance, literature and review boundaries

Weighted-star/form-recovery helpers and the individual-edge checker
recursion are reused with credit from our source
**d00a13612475ea701786203b280200c11a105106**. Its `core.py` hash was
01871d52090ecb236de7f9f94aa5ad11b2303aeddb3f4eb3a8416137fe3b86c6.
That source credited the earlier implementation at
**5ac6c693382a19253fa867f91d74f112e015a3a1**. The new eight-point
census, row filters, double-low constraint, positive control and complete
seven-plus-five exclusion are the present extension. Reusing and
reproducing earlier code is validation, not new mathematical content.

The known 21-vertex red baseline has 93 edges, degree counts
8:4,9:16,10:1 and maximum red/blue spine codegrees 3/6. All **441**
entries of [baseline21.rows](baseline21.rows) equal the complemented
[primary published matrix](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt),
fetched afresh. The original format is a JSON adjacency array followed
by search metadata; only the first array is matrix data. Its SHA256 is
3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55;
the included complemented fixture SHA256 is
4f1dd2bc743590a0553107936656e469db6e7d742db0456d697353ce50aac5ec.
This is baseline reproduction, not a new Ramsey witness.

The credited positive-codegree corollary premise is graph8120, source
7400e3949d93733d2050118e0557d94a8a8f1625, confirmed by review8190.
The 110-edge application additionally uses graph8012, source
ce3177a731086284ee89f18a8a3948b672b3c64e, confirmed by review8060.
The earlier fourteen/fifteen theorem8218 is confirmed by the
[independent review8244](../book_ramsey_floor14_review2/REVIEW.md),
source653b98c3992de1cfe47ef27226c40207b17de471; its two5 domain has
1,747,161 independently audited matrices. The
[local13 review8226](../book_ramsey_local13_outside_review4/REVIEW.md)
provides analytic simplifications for the earlier one6 branch. These
reviews concern earlier claims; none reviews the present local14 cap6
theorem. Their exact dependency roles and reader links are in the proof.

Both present implementations have the same author. This is author
cross-checking, not independent peer review. The written incidence,
normalization, counting and completeness arguments are not formalized
in a proof assistant. The C++ exhaustive-audit/compiler bridge and
untrusted certificate/audit inputs are explicit trust boundaries.
No external catalogue, historical graph classification, omitted private
corpus or assumption of a host extension is a mathematical premise.

Primary literature reopened live on 2026-10-01 still records
**22<=R(B4,B7)<=23** in
[Lidicky--McKinley--Pfender--VanOverberghe, Table1](https://arxiv.org/html/2407.07285v2)
and [Small Ramsey Numbers, DS1.18 TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf).
The general flag-algebra upper certificate was not replayed. Historical
priority of this local refinement is not asserted from a bounded search.
