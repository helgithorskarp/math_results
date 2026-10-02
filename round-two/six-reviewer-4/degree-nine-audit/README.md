# Independent degree-nine cycle and leaf audit

Actual author **six-reviewer-4**, independent mathematical reviewer.
[REVIEW.md](REVIEW.md) contains the exact verdict, hypotheses, ordinary
slack-identity proof, maximum-degree hypothesis removals, 13-pattern necessary
near-equality classification, and two-pattern CaseI restriction.
The Ramsey interval remains22..23. Histograms and literal selected-spine
frames are not valid full-host constructions.

Use CPython3.12 (verified3.12.14), standard library only, from this directory.
Run serially under the existing oneCPU/2GiB scope and a 90-second external
guard; the measured jobs finish in less than2.428 seconds.

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1
python3 derive.py > /tmp/degree-nine-produced.json
python3 verify.py > /tmp/degree-nine-checked.json
cmp EXPECTED.json /tmp/degree-nine-produced.json
cmp EXPECTED.json /tmp/degree-nine-checked.json
python3 -O derive.py > /tmp/degree-nine-produced-O.json
python3 -O verify.py > /tmp/degree-nine-checked-O.json
cmp EXPECTED.json /tmp/degree-nine-produced-O.json
cmp EXPECTED.json /tmp/degree-nine-checked-O.json
python3 verify.py --self-test
python3 -O verify.py --self-test
python3 original_record.py ORIGINAL_EXPECTED.json > /tmp/degree-nine-original.json
python3 -O original_record.py ORIGINAL_EXPECTED.json > /tmp/degree-nine-original-O.json
cmp ORIGINAL_EXPECTED.json /tmp/degree-nine-original.json
cmp ORIGINAL_EXPECTED.json /tmp/degree-nine-original-O.json
python3 baseline21.py
python3 -O baseline21.py
sha256sum -c SHA256SUMS
```

Own self-tests print `{"damages_rejected": 10}`. The complete independent
stdout is8,718 bytes, SHA256
`a95b01bb89d6cf74ddb00de61b90d6d0bc205e53bf1fea5b3f3905b8ccc6a99d`.
The original record is3,152 bytes, SHA256
`63f30891258626922c5629f54d11f9ac75ce1b9e7ba95c65460357be308dc2cf`.
The checker prints complete coverage on stderr:27,062 residual-search calls,
102 literal selected colored spines,4,096 leaf-row trials/36 cores/12 cycles,
32,768 six-point graphs/2,880 rooted induced-cycle identity checks, and288
signed 22-point frames. It also checks a degree11,10,9,10 selected-spine
control to distinguish signed sum zero from individual corner degrees ten.

`derive.py` uses a two-variable integer margin parametrization after the
proved row-rank reduction. `verify.py` uses a separate search over all16
blue words with residual columns, pair capacities and row cost, then checks
literal third vertices. It imports no producer or researcher engine.
`original_record.py` reconstructs every original field with our own audit;
`ORIGINAL_EXPECTED.json` is a credited comparison fixture from six-books-1,
commit266d4715935381ce0aeb9386ad966364e0797f6d. It was introduced only after
our independent whole record was frozen. Native author programs were then
read and replayed separately, as recorded in provenance.

The1,056-byte `primary21.txt` is the unchanged public primary construction
from gwen-mckinley/ramsey-books-wheels. Its trailing search metadata is part of
the hashed raw file; the checker decodes only the leading JSON matrix and
normalizes its zeros to red and ones to blue. Baseline counts93/117 and3/6
are known results. No private ledger, signing material, bulky data, or solver
output is included. Python caches are ignored; all compact source and
fixtures remain tracked. All proof/code bridges remain unformalized.
