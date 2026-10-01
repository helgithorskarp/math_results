# Sharp-67 independent audit

Actual reviewer: **six-reviewer-5**, independent mathematical reviewer.
The [review](REVIEW.md) confirms the exact uncovered19/20/20, pair5/5/4 restricted
maximum, crediting the already independently reviewed nineteen-star classification.
It independently regenerates all46 joint cases, checks77 residual capacities and
sharpness, and proves the complete equality quotient:107 normalized codes,
60 unmarked point-isomorphism classes, all asymmetric. Historical priority and
the unrestricted endpoint remain outside this verdict.

Python3.11.2, GCC12.2.0/C++17, OpenSSL3.0.22 and its development headers were used.
No author module/executable, third-party Python package, solver or proof assistant
is required. The four small author inputs are vendored with explicit original
paths/commits/hashes in [INPUTS.json](INPUTS.json). The complete reviewed classification
is a mathematical premise; the full1374-object earlier census is not redone.

Run from this directory, with build products and case outputs outside Git:

```bash
g++ -std=c++17 -O2 -Wall -Wextra -Wpedantic -Wconversion -Wshadow \
  joint.cpp -lcrypto -o /tmp/reviewer5-sharp67-joint
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 check.py --work /tmp/reviewer5-sharp67 \
  --executable /tmp/reviewer5-sharp67-joint
python3 point_maps.py /tmp/reviewer5-sharp67/exact.json /tmp/reviewer5-quotient.json
python3 -O controls.py /tmp/reviewer5-sharp67/exact.json /tmp/reviewer5-quotient.json \
  --executable /tmp/reviewer5-sharp67-joint --work /tmp/reviewer5-controls \
  --output /tmp/reviewer5-controls.json
```

The exact outputs equal [EXPECTED.json](EXPECTED.json) and
[POINT_QUOTIENT.json](POINT_QUOTIENT.json). Mathematical output omits execution
measurements so these hashes are deterministic:

- Full exact inventory: `82c76a8eb6a82476cfd8b53938eecfeb1b9292abe4b613ace2e2715a08880790`.
- Point quotient: `19dd5acdee88a1cda81b2c7333167154d9d802c3304cd055c0d62fad38c5c232`.

The exact inventory contains1,540,398 tail choices summarized by46 complete
transcript hashes,18,062 complete first-center stars,77 cores, capacities17..22,
and all107 literal equality codes. The quotient contains all60 representatives'
full point groups and107 actual merging maps. Each code is an unordered word family;
the quotient forgets distinguished centers. The exact labeled-family count is
`60*18! = 384142422343680000` under the equality hypotheses.

The native engine's 346,519,480 visited nodes are distributed across1,558,460
bounded private-star queries. Per-query guards remain2,000,000 nodes/20seconds,
whole-case guard60seconds, subprocess65seconds. Point-isomorphism guards are
2,000,000nodes/20seconds per call and60seconds total. Failure, timeout, partial
output or a missing case cannot certify absence. All stages run sequentially,
one thread, under the existing1CPU/2GiB process scope.

An optional `check.py --reuse-census` mode reruns the residual/positive/negative
and equality stages after checking every local case against all complete published
transcript and joint hashes. It **assumes those local native case records came from
a completed own cold run**. It is an ancillary convenience, not a portable negative
certificate or another cold census. Final normal cold validation was229.396seconds;
optimized-Python ancillary replay reused the completed local native records.
Normal and optimized exact output agree. Repeating `point_maps.py` under `-O`
reruns its complete quotient and gives byte-identical mathematical output.

For the recorded bounded sanitizer check:

```bash
g++ -std=c++17 -O1 -g -fno-omit-frame-pointer -fsanitize=address,undefined \
  -Wall -Wextra -Wpedantic -Wconversion -Wshadow joint.cpp -lcrypto \
  -o /tmp/reviewer5-sharp67-san
ASAN_OPTIONS=detect_leaks=1 UBSAN_OPTIONS=halt_on_error=1 \
  /tmp/reviewer5-sharp67-san --controls
ASAN_OPTIONS=detect_leaks=1 UBSAN_OPTIONS=halt_on_error=1 \
  /tmp/reviewer5-sharp67-san 10 /tmp/reviewer5-sharp67/input-10.txt
```

This covers all5126 small-graph/bit-boundary comparisons,15400 twelve-point
four-tail partitions and the **complete positive case10**, all its23 joint cores.
The entire sanitized case's candidate/solution and joint output matches release,
including all negative queries. It is not a full46-case sanitized replay.
Literal checks reject nine damaged certificates/witnesses and eleven malformed
native calls; arbitrary full point relabelings of all60 classes are recovered.
[VALIDATION.json](VALIDATION.json) states exact measurements and trust boundaries.

The full private tail/query transcripts are never written by this checker: their
canonical strings are incrementally hashed, avoiding the original454MiB corpus.
Compact case records, input words, binaries, timing data and temporary controls
remain in the chosen work path. Only compact source/evidence is published.
