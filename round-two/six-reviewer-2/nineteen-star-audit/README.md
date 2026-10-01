# Independent nineteen-star audit

Reviewer: **six-reviewer-2**, role **independent mathematical reviewer**.

[REVIEW.md](REVIEW.md) independently confirms committed lemma8537:
1,374 normalized nineteen-block packings, 46 marked and 44 unmarked
point-isomorphism classes when a replication-five uncovered pair exists.
The proof supplies every quantifier and the ordinary shortening transfer.
The reviewer also obtains full cyclic point groups (34 trivial, eight
C2, one C4, one C6) and the exact labeled count17!461/12. A literal
affine fixture checks the essential m>0 hypothesis and sharp h>=5.
No unrestricted coding bound or historical priority is claimed.

Requirements: GCC12.2+ with C++17; CPython3.11+ standard library.
From the repository root, place generated outputs outside the source:

```sh
g++ -std=c++17 -O2 -Wall -Wextra -Wconversion -Wshadow -pedantic \
  round-two/six-reviewer-2/nineteen-star-audit/ordered.cpp \
  -o /tmp/nineteen-ordered
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B -O round-two/six-reviewer-2/nineteen-star-audit/audit.py \
  --native /tmp/nineteen-ordered
python3 -B -O round-two/six-reviewer-2/nineteen-star-audit/controls.py \
  --native /tmp/nineteen-ordered \
  --result round-two/six-reviewer-2/nineteen-star-audit/EXPECTED.json
```

Expect COMPLETE,1374/46/44 and manifest SHA256
`83adc2817c988fa4450ede02c7da09b4da857e3f1850a0b0d0dee4cfd4a24bca`.
The fixed native guards are2,000,000 nodes/20seconds per graph; the
Python caller has a30-second native timeout. A failure gives no theorem.
The ordered searches visit543361/691196 nodes; the full independent
audit takes about three seconds and below25MiB child RSS. There is no
greedy coloring, maximal-clique pivot, symmetry pruning or author import.

Optional entrywise comparison, after regenerating the author's carrier:

```sh
python3 -B round-two/six-code-3/nineteen_star_classification/produce.py \
  --work /tmp/nineteen-author
python3 -B -O round-two/six-reviewer-2/nineteen-star-audit/audit.py \
  --native /tmp/nineteen-ordered \
  --author-manifest round-two/six-code-3/nineteen_star_classification/expected.json \
  --author-carriers /tmp/nineteen-author/producer-carriers.json
```

Both manifest and every actual carrier entry match. The author's data
are optional comparison evidence; independent reconstruction uses no
external corpus. [EXPECTED.json](EXPECTED.json) contains compact class
and full point-group data, checked automatically. Binaries and the
1,374-object comparison corpus are generated scratch, not published.

For the checking build replace `-O2` with
`-O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer`; the full
two-carrier audit passed with this build. Source/compiler/interpreter
and the unformalized completeness/decoding proofs are explicit trust
boundaries. [VALIDATION.json](VALIDATION.json) records executed checks.
