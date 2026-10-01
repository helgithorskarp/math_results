# Independent three-star audit: sixty-one words

Reviewer: **six-reviewer-2**, role **independent mathematical reviewer**.

[REVIEW.md](REVIEW.md) confirms committed lemma8627 and strengthens its
62-word bound to **61**, with exactly the original hypotheses. There
must be an uncovered triple of degree19 centers, all three pair
replications five, and at least one center with m=2. The vertex-disjointness
threshold improves from63 to62. Global coding bounds and the all-m=1
branch are unchanged by this proof; sharpness is not asserted.

The independent computation uses triple ownership, increasing tail
combinations and a native ordered clique traversal. It reconstructs
all11879 partitions,6582 y choices and226 complete42-word cores.
Every integer weight certificate is checked. [COLOR_CERT.json](COLOR_CERT.json)
then excludes20 residual words in the sole exceptional core with a
44-node complete branch tree, independently checked using literal sets.
[INPUT.json](INPUT.json) is the previously audited six-marked-class census
manifest; [EXPECTED.json](EXPECTED.json) pins the full deterministic output.

Requirements: CPython3.11+ standard library, GCC12.2+ and C++17. Run from
the repository root. Put binaries, downloaded proof data and generated
carriers in scratch, outside this source directory:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
g++ -std=c++17 -O2 -Wall -Wextra -Wconversion -Wshadow -pedantic \
  round-two/six-reviewer-2/three-star-audit/ordered.cpp -o /tmp/three-star-ordered
python3 - <<'PY'
import urllib.request
url = ('https://raw.githubusercontent.com/helgithorskarp/math_results/'
       'eabc8c23608b65585f6c376d02a2fc27e26440c8/'
       'round-two/six-code-3/three_nineteen_zero_triples/capacity.json')
urllib.request.urlretrieve(url, '/tmp/three-star-capacity.json')
PY
python3 -B -O round-two/six-reviewer-2/three-star-audit/audit.py \
  --native /tmp/three-star-ordered --certificate /tmp/three-star-capacity.json \
  --work /tmp/three-star-check
python3 -B -O round-two/six-reviewer-2/three-star-audit/controls.py \
  --native /tmp/three-star-ordered --certificate /tmp/three-star-capacity.json \
  --work /tmp/three-star-check
```

Expect COMPLETE,226 cores, original capacity bound62 and refinement61,
plus color check44 nodes/15 empty-domain leaves. The whole run takes
about30 seconds and below30MiB child RSS. Every generated carrier hash
matches the target record; the optional `--author-expected PATH` compares
all logical record fields explicitly. Author node counts differ because
the algorithms differ and are excluded from that comparison.

`--cases 0` (or any proper subset) resumes bounded selected cases, giving
COMPLETE_SELECTED_CASES. It cannot establish the uniform bound. Every
native request has fixed2million-node/20-second guards and a30-second
response timeout; each full marked case has a60-second guard. A guard
failure supplies no mathematical nonexistence.

For native checking, replace `-O2` with
`-O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer`. The entire
six-case audit passed this build in normal Python, as well as release
code under optimized Python. [VALIDATION.json](VALIDATION.json) and
[PROVENANCE.json](PROVENANCE.json) record exact executed runs and hashes.

`color_certificate.py` contains both an optional bitset tree generator
and its independent literal verifier. The proof requires only the small
published tree and checker; heuristic coloring was discovery only. The
200339-byte weight certificate is pinned by SHA256 and downloaded from
the original public source; it is untrusted until checked. No optimizer,
author executable, large generated corpus or formal kernel is required.
The ordinary reduction and computational trust boundaries are explicit
in REVIEW.md.
