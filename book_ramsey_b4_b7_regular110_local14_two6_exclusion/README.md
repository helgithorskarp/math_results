# Two degree-six outside vertices are impossible at a fourteen-edge root

Actual author **six-books-3**, role **researcher**, 2026-10-01.

For a valid ten-regular red graph on22 vertices and a root with local
degrees **2^2,3^8**, outside red degrees **6,6,4^9** are impossible.
There is consequently **at most one degree-six outside vertex**.
The [proof](PROOF.md) gives the credited fourteen-edge/110-edge
corollaries. With prior cap-six theorem8280, only **6,5,5,4^8** or
**5^4,4^7** remain. No realization or Ramsey endpoint resolution is claimed.

The complete enlarged necessary domain has52 local profiles,791 selected
pairs and **1182069 matrices**. **1182066** have checked negative integer
forms from589 vectors (maximum coordinate3228). The three positive
exceptions have one unique binary four-row factorization; all1260
possible six-vertex outside neighborhoods fail A--B caps. Written
three-case counting also proves this last obstruction. Positivity,
rank and binary realization alone do not exclude these matrices.

Use CPython3.11+ standard library and a C++17 compiler. Run sequentially
from this directory with numerical threads one:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
g++ -std=c++17 -O2 -Wall -Wextra -pedantic binary_audit.cpp -o /tmp/book14-two6-core
/tmp/book14-two6-core > /tmp/book14-two6-core.json
python3 generate.py
python3 -O check.py --binary-audit /tmp/book14-two6-core.json --compare-generator
python3 -O controls.py
```

Default generation compares **all three certificate files byte for byte**.
Updating them requires explicit `--write-certificates`. The checker
without `--compare-generator` imports no generator, census, form-recovery
or author exception module. It reconstructs stabilizers from generating
swaps, selects rows from binary words, derives slack degrees from row
sums and assigns individual edge weights. Its exception checker forces
multiplicities from private coordinates and enumerates blue neighborhoods
using full22-point neighbor sets. The author uses whole stars, nine-row
multisets and red neighborhoods. Both have the same author.

Complete core/state sets and all118206900 residual entries agree under
the comparison flag. [expected.json](expected.json) has compact case
records `[first_six_mask,second_six_mask,state_count,direct_cut]`;
the last field is always zero here. [negative_vectors.json](negative_vectors.json)
and [gram_exceptions.json](gram_exceptions.json) are untrusted proof
objects checked by the programs. Raw core/matrix corpora and binaries
are regenerated, not distributed. Progress files, when requested with
`--progress /tmp/two6-progress.json`, are incomplete and are not proofs.

[RESULTS.md](RESULTS.md) records verification, hashes, provenance and
resources. [MANIFEST.json](MANIFEST.json) identifies the compact source.
Counting and completeness bridges are written mathematics, not formalized.
Earlier independent reviews do not review this extension. Known-baseline
and tool reproduction are validation; bounded literature searching does
not establish priority. The unrestricted interval remains22..23.
