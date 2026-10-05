# Boxed2143: exact tree dynamics and a failed uniform growth mechanism

Quinn (literature-researcher-3), 5 October 2026.
Different-researcher internal checker: Theo (literature-researcher-4).
The full bounded-exponential growth question remains **unsolved**.

This source contains three separately checked partial results:

* The maximum Cartesian tree is an exact state for legal new-maximum gaps
  and their shape updates. Weighted histories, rather than the number of
  shapes alone, give the avoidance counts.
* Incoming states are boundary-spine merges. A descending-priority merge
  word is admissible exactly when it has no consecutive LL after an R.
  This gives an exact reverse recurrence and an exact fixed-pair join DP.
* A specific proposed perfect-fiber join bound, which would imply the full
  negative growth answer, fails. Two explicit avoiding inputs of length31
  have exactly25635 valid rank partitions, below the proposed32768 bound.

The complete arbitrary-size arguments are
[TREE_STATE_LEMMA.md](author/TREE_STATE_LEMMA.md) and
[REVERSE_MERGE_AND_JOIN_BOUND.md](author/REVERSE_MERGE_AND_JOIN_BOUND.md).
The latter proves the conditional full-growth bridge, the exact counting
algorithm, and the all-size domain of the explicit test family. It records
an earlier invalid test family and its correction. The corrected finite
counterexample rejects that particular bound; it does not reject factorial
growth, establish an exponential bound, or reject all averaged/subclass bounds.

The exact target is to decide whether a constant C>0 bounds a_n<=C^n for
every n>=1, where a_n counts permutations with no i1<i2<i3<i4 satisfying
p[i2]<p[i1]<p[i4]<p[i3] and no unselected point strictly inside their rectangle,
or instead prove limsup a_n^(1/n)=infinity. No ordinary root limit is assumed.

The external primary context is Kitaev, Qiu and Xu,
[Coincidences and Growth of Boxed Mesh Patterns, arXiv2609.13764v1](https://arxiv.org/html/2609.13764v1),
Sections3 and7, especially Conjectures7.4/7.5. Its stated remaining orbit was
checked live on5 October2026. The original question appears in
[Avgustinovich, Kitaev and Valyuzhenich, Discrete Applied Mathematics161(2013),43–51](https://doi.org/10.1016/j.dam.2012.08.015).
Cartesian trees and their merges are standard structures. This publication
does not certify novelty or constitute external independent peer review.

Theo's full written checks and frozen independent outputs are
[tree review](review/QUINN_TREE_STATE_REVIEW.md),
[tree reproduction](review/quinn-tree-state-reproduction.json),
[reverse/join review](review/QUINN_REVERSE_JOIN_REVIEW.md), and
[reverse/join reproduction](review/quinn-reverse-join-reproduction.json).
The new acceptances were team messages467 and498. The reverse checker imports
no author executable: it uses direct value neighbors, postorder representatives,
monotone-stack trees, and bottom-up shuffle reconstruction. It matches every
complete state-weight stream through10, every1849 m7 pair count, ten literal
subset controls, and every complete level stream of the length31 certificate.
It does not claim to repeat all native candidates or sanitizer measurements.

From this directory, CPython3.11+ with the standard library suffices:

```sh
python3 -B review/check_quinn_tree_state.py --output /tmp/boxed2143-tree-replay.json
python3 -B review/check_quinn_reverse_join.py --output /tmp/boxed2143-reverse-join-replay.json
```

The first takes about11seconds/35MiB; the second about4minutes/525MiB on the
recorded single-process run. Output hashes/counts are reproducible; timing and
memory are environment dependent. Both verify the frozen author manifests
before and after replay. The portable scripts change only the default author
directory to ../author; exact original/public hashes are recorded in
[PUBLICATION_PROVENANCE.json](PUBLICATION_PROVENANCE.json).

For the direct literal C++ baseline (GCC12.2/C++20), outputs can remain outside
the frozen source:

```sh
g++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Wconversion -Wshadow author/balanced_join.cpp -o /tmp/boxed2143-balanced-join
/tmp/boxed2143-balanced-join author/balanced_fiber_h3.txt /tmp/boxed2143-native-replay.json
```

All6,345,768 m7 joins are tested by four-index choices and interior scans;
the retained table has minimum37 and sum790086. Exact integer arithmetic and
the prescribed input bounds exclude counter/mask overflow. Sanitizer controls
and compiler/input/output hashes are retained in author/. Python DP counters
are arbitrary precision. Its50k per-level state cap reports incomplete work,
never a truncated count; the certified length31 run stays below it.

The author/ directory is an unchanged38-file dependency snapshot, including
the earlier ten-file kernel packet. The kernel and its state obstruction were
already published at
[exact earlier source commit057746e13d1056047ddf0b7b59968e9a70f081ff](https://github.com/helgithorskarp/math_results/tree/057746e13d1056047ddf0b7b59968e9a70f081ff/boxed2143_insertion_obstructions_20261005).
Their presence here supports the new algorithms and does not add a new claim
to that earlier graph original. The historical cross-team comparison utility
needs its explicitly supplied peer paths; it is not a required portable replay.

Historical awaiting-review headers and original no-publication fields are
preserved verbatim; the written reviews and this README record the current
scope. No later workday3 construction/reciprocity hypothesis is in this packet.
Finite checks and the false sufficient bound do not satisfy the full target.
