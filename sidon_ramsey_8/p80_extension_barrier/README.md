# A five-class obstruction to extending the published P80 partition

**Exact computer-assisted lemma.** Let `P` be the partition of `[80]` in
[partition80.txt](partition80.txt), reproduced from Table I (the row `I=8`) of
Xiu, Fan and Liang, *On Disjoint Golomb Rulers*,
[arXiv:1405.4535v1](https://arxiv.org/pdf/1405.4535), page 6.
For each `e` in `{0,1}`, no partition of `[81]` into eight integer Sidon sets
contains three classes of `P+e`.

Thus an extension of either embedding must replace at least six original
classes. The assertion allows arbitrary sizes for the replacement classes.
Reflection about 41 gives the same obstruction for the reflected seed.
It concerns this specified published partition and these embeddings; it does
not exclude other partitions of `[81]` or improve the numerical bounds
`81 <= SR(8) <= 85`.

Here a Sidon set has distinct unordered pair sums, including repeated
summands. Equivalently its positive differences are distinct. All arithmetic
is in the integers, not modulo an interval length. Input coordinates and the
seed file are one-based.

## Complete finite reduction

For each shift, choose three seed classes to retain. These `C(8,3)=56`
choices exhaust the possibility of retaining at least three. The complement
`R` in `[81]` has 51 points and must be partitioned into five Sidon classes.
The program exhaustively enumerates 12-element Sidon subsets of each `R`
and finds none. Larger Sidon sets would contain a 12-element subset, so all
five remaining classes have size at most 11.

There must be an 11-element class, since five sets of size at most 10 cover
at most 50 points. We exhaust two possibilities:

1. Exactly one class has size 11. Choose it from the complete catalog on `R`.
   The remaining 40 points must be covered by four 10-element Sidon sets.
   Generate their complete catalog and decide exact cover.
2. At least two classes have size 11. Choose an unordered disjoint pair from
   the complete catalog on `R`. The remaining 29 points must have one of
   the profiles `(10,10,9)`, `(11,10,8)`, `(11,9,9)`, `(11,11,7)`.
   Enumerate the required large subsets and check the final complement
   directly from its pair sums. This also includes cases with three or four
   11-element classes. In these particular runs, no 11-element set occurs
   in any of the 29-point complements.

Every completion in both cases fails. There is no assumption of balance,
reflection symmetry, maximality of a class, or uniqueness of the P80 seed.
Neither the earlier P84 profile lemma nor a solver verdict is a premise.

| Complete count | Seed shift 0 | Seed shift 1 |
|---|---:|---:|
| 51-point domains | 56 | 56 |
| 12-element subset occurrences | 0 | 0 |
| 11-element subset occurrences on the domains | 1,094 | 1,024 |
| Disjoint 11-element pairs | 128 | 126 |
| 10-element subsets on 40-point complements | 3,153,154 | 2,895,923 |
| 10-element subsets on 29-point complements | 1,503 | 1,915 |
| 11-element subsets on 29-point complements | 0 | 0 |
| Successful completions | 0 | 0 |

These are occurrences over the specified domains and branches, not counts
of globally distinct subsets. There is no deduplication across domains.

## Algorithms and independent-method checks

[verify.cpp](verify.cpp) supplies two complete enumeration methods:

- Method 0 builds increasing sets while maintaining all used positive
  differences and bit masks of feasible next elements. Its elementary
  diameter bound uses the distinct differences among remaining elements.
  Exact cover branches on a remaining point of least incidence.
- Method 1 fixes the least and greatest elements, then inserts interior
  elements while maintaining distinct unordered pair sums, including
  doubles. Its gap bound uses the sum of distinct positive consecutive
  gaps. Exact cover branches on the least remaining point.

Both methods sort every generated catalog. Each writes a canonical binary
trace, which is checked against its SHA-256 hash and compared **entry by
entry** with the other method's trace. The trace records each domain, target
size and complete sorted answer, including empty catalogs. Format: a
16-byte mask, 8-byte target size, 8-byte count, then that many 16-byte masks;
all words use little-endian byte order, with points represented internally
by bits 0 through 80.

| Shift | Trace bytes | SHA-256 |
|---|---:|---|
| 0 | 50,538,800 | `e11d54cebfdd52018aa7b25c2895ce4cd99bea33bde2d1934f200a1ea814ed86` |
| 1 | 46,426,208 | `ff3492f41e9f577bee35bc149ec816677f392d4e0252c54e11cde29b14bb05ad` |

The implementations share the written case reduction, orchestration and
some residual-cover logic. They are internal checks using distinct
algorithms, not external peer review or proof-assistant verification.
The trust boundary is the finite reduction, source, compiler and runtime.
All calculations are exact; masks use GCC's unsigned 128-bit extension.
No floating-point weights, external catalog, SAT trace or optimization
library is used by this certificate.

Six positive controls include a 51-point five-class packing, a 40-point
four-class packing and four 29-point packings. The Python driver checks
returned partitions directly from unordered pair sums and exact coverage.
A positive domain can admit multiple size profiles; the recorded witness
sizes are not a uniqueness assertion.

## Reproduction

Requires Python 3.11 or later, GCC with C++20 and unsigned 128-bit support,
and a POSIX environment. No third-party Python package is required.

```sh
python3 reproduce.py --work /tmp/p80-extension --jobs 4 --independent
```

The work directory must be outside this repository. The driver compiles the
source with strict warnings, runs both shifts and both methods, checks all
counts and trace hashes, compares traces bytewise, verifies the positive
controls, and writes `verification.json`. Omitting `--independent` runs only
method 0. A failed check or interrupted process is not a completed proof.
Generated traces, executables and logs remain in the work directory.
The fresh four-process delivery run completed in 379.339 seconds with
GCC 12.2.0 and Python 3.11.2. All twelve sanitizer controls passed
(AddressSanitizer and UndefinedBehaviorSanitizer, both methods).
See [validation.json](validation.json) for the delivered run and
[expected.json](expected.json) for the exact acceptance values.

This obstruction records the limit of a natural block-replacement search
from the published lower-bound witness. A global construction search, a
new seed, or replacements involving at least six seed classes remain
possible. The campaign's unrestricted SR(8) problem remains open.
