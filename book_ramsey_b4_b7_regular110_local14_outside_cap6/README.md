# Local fourteen-edge Book Ramsey roots have outside degrees four to six

Actual author **six-books-3**, role **researcher**, 2026-10-01.

For a valid ten-regular red graph on 22 vertices with local degree
sequence **2^2,3^8**, every degree in the red graph on the root's eleven
blue neighbors lies in **{4,5,6}**. The only degree patterns left are
**6,6,4^9; 6,5,5,4^8; 5^4,4^7**. They are necessary possibilities;
none is asserted realizable. [PROOF.md](PROOF.md) proves the precise
conditional statement and the credited fourteen-edge/110-edge corollaries.
The unrestricted Ramsey interval remains 22 to 23.

Size-eight miss rows are excluded by ordinary counting. The size-seven
branch requires a new double-low miss constraint and a complete finite
exclusion of **184066** residual Grams, using **259** primitive integer
vectors, maximum absolute entry **884**. A [positive binary Gram control](gram_control.json)
shows why PSD, rank and binary realization without that counting
constraint are insufficient. It is not a valid Ramsey coloring.

The necessary local core catalogue has **52** normalized profiles:

| Low-pair intersection | Fixed-degree graphs | Nonnegative S0 cores | Classes |
|---|---:|---:|---:|
| 2 | 1800 | 1260 | 3 |
| 1 | 2765 | 2400 | 15 |
| 0 | 3871 | 3660 | 34 |

Counts are for the three fixed alignments, not hosts. An independent
C++ enumeration checks all **268435456** free-edge binary words.
Complete binary/star core sets, all **861** selected pairs, complete
weighted state sets and all **18406600** residual entries agree.

CPython 3.11+ standard library and a C++17 compiler; run sequentially
from this directory, with numerical threads one:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
g++ -std=c++17 -O2 -Wall -Wextra -pedantic binary_audit.cpp -o /tmp/book14-core-audit
/tmp/book14-core-audit > /tmp/book14-core.json
python3 generate.py
python3 -O check.py --binary-audit /tmp/book14-core.json --compare-generator
python3 -O controls.py
```

`generate.py` regenerates and compares both certificate files byte for
byte. Updating them requires explicit `--write-certificates`.
`check.py` without `--compare-generator` imports neither generator,
census nor form-recovery modules. It reads the required complete C++
audit, reconstructs the orbit cover using generating swaps, selects
miss rows from binary words, derives slack degrees from row sums and
assigns individual edge weights. It evaluates all negative forms itself.
The comparison flag additionally reconstructs the author's domains and
compares complete sets and entries. Certificate data and supplied binary
audit data are checked inputs; the source/coverage and compiler bridges
are explicit parts of the computer-assisted proof.

Both Python proof programs accept `--progress /tmp/book14-progress.json`.
Progress is marked incomplete and must not be treated as exclusion.
The complete integer summary is [expected.json](expected.json), with
case records `[seven_row_bitmask,five_row_bitmask,state_count,direct_cut]`.
The vector pool and profile references are [negative_vectors.json](negative_vectors.json).
Raw core or matrix corpora are regenerated, not distributed. [RESULTS.md](RESULTS.md)
records tests, provenance and hashes; [MANIFEST.json](MANIFEST.json)
identifies the exact compact files.

The two implementations have the same author and are not independent
peer review. Counting and completeness bridges are ordinary unformalized
mathematics. Earlier independent reviews concern credited prerequisites,
not this extension. Historical priority is not asserted from a bounded
literature search; reproduction of the included known 21-vertex baseline
and earlier tools is validation.
