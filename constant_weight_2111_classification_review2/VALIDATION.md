# Validation record

**six-reviewer-2, independent mathematical reviewer**, 2026-10-01.
All author executable code was read only. The reviewer's prior native source
is reused byte-for-byte, with [exact provenance](INPUT.json).

| Phase | Normal seconds | Optimized seconds | Normal / optimized parent peak RSS (KiB) |
| --- | ---: | ---: | --- |
| Complete cold carrier and native census | 16.001278 | 17.674605 | 64,852 / 65,972 |
| Complete packing quotient and incidence audit | 4.435456 | 3.947493 | 89,704 / 89,892 |
| Independent controls | 11.021811 | 1.718607 | not separately recorded |

The normal controls include ASan/UBSan compilation and execution; optimized
controls omit that duplicate native build. Census compiler/child peak RSS was
127,132 / 127,444 KiB. No sanitizer RSS estimate is inferred from that number.
All scopes retained one CPU / 2 GiB, one numerical-library thread and one
intensive local job at a time. Guards remained 200,000 states / ten seconds.

Both cold runs regenerate all twelve leaves, all 1,224 legal hub prefixes,
all 75 proof matrices, every complete native cover stream, the 210-way
second-point reconstruction and all 45,504 restored packings. Every packing
orbit is recomputed from actual stabilizer generators. The eight direct
incidence canonicalizations and exact group presentations are also rerun.
No proof cache or author executable source is used.

The complete regenerated census and classification JSON records agree
byte-for-byte. Their canonical stream hashes are:

```text
census       33c145fb4f270e4df95baa9a76f8cc65d449b6fcf69893cbaeb90f00b7f5780c
classification 55288c22191b72b3efbf37086852847f2b7b2a6c334d29cbf8dd84d1f666e28f
```

The compact full stable record, including all fiber summaries, eight literal
representatives, presentations, control outcomes and exact counting bridges,
is [expected.json](expected.json). Its SHA256 is:

```text
12a910c0217f3bc5dd043c3cda6fc1420c6459d9249d7b1c52a85d3af70f928b
```

The normal verifier explicitly used `--record` to establish this reviewer
baseline. The optimized verifier omitted `--record` and compared every byte.
Author runtime inputs and the reused native source are pinned and checked.
This publication copy is required to remain byte-identical to the checked
source; provenance checking is not represented as an additional cold proof run.

Complete results: 75 fibers; 69 empty fibers; six positive fibers; 45,504
restored first-hub packings; eight point-isomorphism classes; 66,421,555,200
fixed-profile labeled packings. Native total 3,086,538 states, maximum 191,601.
Packing walks visit 45,504 states and stabilizer closures 2,368. Independent
incidence trees visit 100 states, maximum 28 per representative, and produce
orders 18,6,6,18,2,6,2,6. Their abstract groups are
Dih(C3 x C3), S3, S3, Dih(C3 x C3), C2, S3, C2, C6.

Controls compare all 512 subset-defined targets with exact literal subset
truth, test 64 relabeling/conjugacy identities and use 900 incidence states
in total. Five corrupt fixtures and six malformed native/invalid-cap inputs
are rejected; two zero guards return INCOMPLETE visibly. A positive native
fixture exercises column index 839 and pair index 135. ASan and UBSan report
no diagnostics on that boundary fixture.

The ordinary homogeneous-incidence proof and prior independent dependencies
are detailed in [REVIEW.md](REVIEW.md). They establish the ten-unit-row result
and its exact boundary budget. Finite arithmetic checks are supplementary,
not substitutes for those written combinatorial bridges. No unrestricted
coding improvement, priority proof or formalization is asserted.
