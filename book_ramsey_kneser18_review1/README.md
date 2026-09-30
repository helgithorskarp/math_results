# Independent Kneser eighteen-core review

Author: **six-reviewer-1**, role **independent mathematical reviewer**, 2026-09-30.

[REVIEW.md](REVIEW.md) independently confirms every induced eighteen-vertex Kneser-core host bound and proves a more precise cross-spine book obstruction. The unrestricted book-Ramsey gap remains open. The entire source fixture is attributed to six-books-3, source commit `dbc61bf5487fdfb09b727e9a8eea0e4c8e7ee5d9`; it is untrusted input, not imported author code.

Use GCC 12.2.0 or compatible C++17 and CPython 3.11.2+ standard library. One thread, no solver or dependencies:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
mkdir -p build
g++ -std=c++17 -O2 -Wall -Wextra -Wconversion -pedantic independent.cpp -o build/independent
python3 check.py build/independent --expected expected.json
```

The native calculation visits all 1,310,720 attachment masks, checks actual transport for all 1,330 deleted cores, checks every pair including repeated patterns with both colors, and directly rejects all 1,658 full twenty-two-vertex candidates. The Python layer independently checks cross-spine books, all 62 original witnesses and their complete orbit coverage, and six negative controls. No assertion-dependent acceptance logic is used. Full generated lists are captured in memory and summarized; do not commit them.

Checking build, with identical full-domain output:

```bash
g++ -std=c++17 -O1 -g -Wall -Wextra -Wconversion -pedantic -fsanitize=address,undefined -fno-omit-frame-pointer independent.cpp -o build/independent-san
python3 check.py build/independent-san --expected expected.json
python3 -O check.py build/independent --expected expected.json
```

Final release/native verification with optimized Python matched every expected byte: 3.427472 s / 40,692 KiB peak RSS. The complete AddressSanitizer/UndefinedBehaviorSanitizer build and Python witness layer also matched expected output with no sanitizer diagnostics: 10.000467 s / 464,056 KiB. All jobs were sequential and single-threaded within the existing 1 CPU / 2 GiB scope.

The source generator, independent author verifier, and author controls were separately replayed: 21.341103 s / 45,968 KiB; 4.981137 s / 55,260 KiB; 24.603726 s / 81,816 KiB. Complete domains and colored-pair lists matched entry by entry. Reconstructed source projection SHA256: `8cda3a6a61fb9d5ba534800ef25db4484d3051edfc63a5aa8e50f85a1de4b69d`.

`source_obstructions.json` is copied unchanged from the target's `obstructions.json`, SHA256 `1ea8e8b2442eee346caf5db798dd85dfb0e8f5f412f5b131c8ed6523b25be9d6`. `expected.json` contains only compact counts, hashes, and rejection labels; `SHA256SUMS` pins the published files. Relative links and source provenance are documented in the review. No mathematical completeness conclusion is drawn from a timeout or failed process.
