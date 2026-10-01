# Independent Book22 Petersen audit

Actual agent **six-reviewer-2**, role **independent mathematical reviewer**.

REVIEW.md confirms six-books-3's lemma 8692 after auditing its complete
ordinary local-Petersen/Hall bridge. Earlier finite local-fourteen and
maximum-degree results and their independent audits remain explicit
dependencies. Hall's connected locally Petersen classification is imported,
not reproved. The global Ramsey interval remains 22–23.

The review also proves this independent conditional extension: if a valid
22-point graph has a degree-ten vertex with ten degree-ten red neighbors,
that neighborhood has no triangles or four-cycles and spans between
122-E and 15 edges, where E is the host's red edge count. In particular
E >= 107. A weighted four-cycle inequality treats signed neighbor deficits. At 109
edges a cycle with deficit sum one forces a unique eleven-row miss multiset
on its four columns; the other deficit-two branch is not classified.
This does not exclude all irregular graphs.

## Reproduce

From the repository root, with CPython 3.11.2 (standard library only):

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
    python3 -B round-two/six-reviewer-2/book-regular-audit/audit.py \
      --check round-two/six-reviewer-2/book-regular-audit/EXPECTED.json

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
    python3 -B -O round-two/six-reviewer-2/book-regular-audit/audit.py \
      --check round-two/six-reviewer-2/book-regular-audit/EXPECTED.json

Expected: PASS; 5,760 literal page identities, 20,736 weighted arithmetic
states, 60 Moore residual cycles and six rejected damaged inputs. The full
record also contains all 324 deficit-one pair histograms (one row multiset)
and an invalid red-only countercontrol exposing the necessary blue cap.
Output record SHA256:
7a5f5fdb5ab721ba9a4a6f8c5c2d2b8354fb0406d4d3d3b6a66adbe773592e95.
Omit --check to emit the complete deterministic record.

The code independently uses adjacency sets, four-coordinate row DP,
individual clique-spine budgets, residual cycle generation and generic
isomorphism backtracking. It imports no author code or third-party library.
The mathematical proofs are in REVIEW.md; finite controls are validation,
not an exhaustive search for 22-point hosts.

PRIMARY.g6 is the original 60-byte House of Graphs six-graph fixture.
PRIMARY21.txt is the original 1,056-byte published Ramsey construction
from the authors' companion repository. Its off-diagonal 0 entries are
red and 1 entries blue. PROVENANCE.json records original URLs, hashes
and the exact audited source commit. These are attributed prior-art inputs.

The independent normal/optimized runs and all six documented original
author commands passed sequentially under fixed 45-second guards.
VALIDATION.json records measurements and commands. No 22-point host enumeration,
large proof corpus, numerical solver or network access is needed for the
independent checker. Source publication does not formalize the proof.
