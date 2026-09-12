# Complete two-blue-block compatibility: no additional original exclusions

Every order-11 R(4,4) core in the pinned 546,356-record author catalog, except
record 516166, extends to a 19-vertex graph with two prescribed disjoint blue
K4 blocks, no red K4, and no blue K5. All 104 cross edges are unrestricted.
The exception is the same Wagner-graph/independent-triple join excluded by the
[one-blue-block package](../ramsey_r55_q8_blue_block_obstruction/README.md).

This complete scaling test adds **zero original carrier exclusions**.
The two-block condition is necessary for all 1,092,712 original q8,r5 and
q8,r6 tasks. Its only two negative IDs were already source-certified in pass 33.
Every one of the 1,092,710 retained IDs has a literally checked necessary
fragment. These fragments do not assert that any original full43 task is SAT.

The carrier remains at 521 source-certified exclusions, of which 518 are
inherited accepted exclusions, and 2,188,657 source-certified UNKNOWN IDs.
No q8 physical cohort closes and no Ramsey bound changes. The earned short
scaling pass fails its original-reduction gate. A high-level carrier-consumption
approach change is due; this result does not justify a block-count ladder.

## Evidence

`classify.py` uses one complete 19-vertex formula with the eleven-vertex core
supplied through exact assumptions. It saves 546,355 literal 104-bit edge
words and one negative sentinel. The independent C++ checker decodes each
core and every physical edge and checks red K4 and blue K5 by neighborhood
intersection. It shares neither the Python SAT encoder nor its graph parser.

For the exceptional record, `verify.py` maps every clause of the already
published 15-vertex obstruction into the complete 19-vertex formula. It renames
and checks the actual 2,002-addition LRAT trace against that full input. An
unexpected additional negative core cannot be admitted without a new proof.
The original-ID difference is checked against the prior exact source ledger.

All 546,356 records were decided. Generation took 978.45 seconds in the recorded
run. Every positive graph and the negative proof passed receiving verification.
The new decoder also passed ASan/UBSan checks on 1,024 valid graphs before
rejecting the deliberately incomplete scope; malformed padding, a false graph,
a truncated word and an unlisted negative sentinel were rejected.

## Reproduction

Python 3.11, `python-sat==1.9.dev15` (CaDiCaL300), and C++17/g++ are sufficient.
The catalog is the exact uncompressed `r44_11.g6` from
[McKay's primary Ramsey graph data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html),
SHA-256 `39e10a1bb2d6b36d556e646e12f0181b2bc3bd45b334ad7f495b8900d7680433`.
Global completeness up to isomorphism is imported from that catalog.

```bash
python3 ramsey_r55_two_blue_block_scaling/reproduce.py \
  /absolute/cache/r44_11.g6 /absolute/new-output
```

The default 1,800-second generation envelope is checked between complete solver
calls. Exceeding it raises an error; partial outputs never become a complete
classification. The complete receiving check can also be run separately:

```bash
python3 ramsey_r55_two_blue_block_scaling/verify.py \
  /absolute/cache/r44_11.g6 /absolute/classification /absolute/new-verification
```

The 7,648,984-byte witness stream, generated CNFs/proofs, binaries and logs stay
outside Git. The published source regenerates them and pins the compact prior
proof package in `DEPENDENCIES.json`. `EXPECTED.json` records the complete
receiving result and hashes. No new solver UNSAT assertion is trusted without
a checked trace, and no outside novelty or priority claim is made.
