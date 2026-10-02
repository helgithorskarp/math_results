# Author correction of the first closure example in9476

Actual author six-code-1, researcher, 2026-10-02 pass14.
Reviewer5's durable family message1978 identified this discrepancy.
The author's own sealed complete record confirms it. This is an author
prose correction; it does not claim an independent review verdict.

The original graph9476, bafkreiglk3wga73j4aqmxbrv5rnx2hxkibdomc6zwgthzuou6jnvozp2ym,
and original PROOF.md at source ec7f3d0ee47f2f6dd3bbdbbac71bf93238807918
gave the WRONG population in the first closure bullet, at
T1/X0/tau0/Q3/N5=0. That text described six ineligible units (five k0,
one k1/q3) and seven eligible nonunits, with D=I=29 and C empty.
It is actually vector ordinal0 of that branch, rejected earlier by
DISTINCT_RADIUS_TWO_CROSSINGS: C1+C2=0 < R+|B|=5+7.

The actual first ALL_COLORS_CLOSED_PARTITION vector, ordinal5 in the
branch's lexicographically sorted patterns, has:

- Five ineligible unit U0 rows: (e,k,q,eligible,c1,c2)=(0,0,0,false,5,0).
- One eligible unit: (0,1,0,true,4,0).
- Four eligible nonunits: (1,1,0,true,3,0).
- Three ineligible nonunits: (1,1,1,false,3,0).

Thus D=29,I=20,C1=9,C2=0, |A|=5,|C|=3,|B|=4 and R=5.
Every C color1 endpoint is consumed by units, there is no C color2
endpoint, and unit-B edges are forbidden. The actual nine-point U union C
side, containing k0 roots, is closed from four B points. Radius coverage
then excludes the population. The second closure example is unchanged.

The executable mathematical source, algorithms, literal carrier, all27 branches,
all136 vectors, ordered48/86/2 exclusions, and conditional P>=36 conclusion
are unchanged. Complete record SHA256 remains
77ebab7867e63eb1a88fad4bd8586559ff055fc598ac40782f69a30a9b3471dd.
The original graph body is immutable. This file and the subsequent
[exceptional-row/root-fan contribution](../exceptional_rows_root_fan/PROOF.md)
carry its explicit correction; the main-branch original proof now displays
the correct first illustration and links this note. No source seal or
EXPECTED value is silently replaced.

Reproduce the original complete record using the unchanged code:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 round-two/six-code-1/five_hub_pair_total36/verify.py --output /tmp/five-hub-original-record.json
```

In its `branches`, select T1/X0/tau0/Q3/N5=0 and zip `patterns` with
`certificates`. Indices0 and5 give the mistakenly described and actual
closure populations respectively. The author reconfirmed both with the
unchanged producer and separate colored-vertex oracle before publishing
this correction. Large regenerated records remain scratch.
