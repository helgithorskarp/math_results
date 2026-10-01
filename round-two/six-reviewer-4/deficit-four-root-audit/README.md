# Independent deficit-four full-root audit

Actual reviewer: six-reviewer-4, independent mathematical reviewer.

Confirmed the finite 108-edge exclusion of a full-degree root with an edge-deleted Petersen neighborhood (LEMMA 8828), with no minimum-degree assumption. The raw 135-matrix census is explicitly imported from the sufficient independent REVIEW 8808. This checker independently verifies transfer to deficits 0 through 4, reconstructs actual physical star domains and proves completion impossibility by at most two synchronous path-consistency rounds, without branching. See REVIEW.md for the full verdict, ordinary bridges, credit and trust boundary.

Run from this directory with CPython 3.11 and the standard library:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B check.py
python3 -B -O check.py
```

Both print `PASS` after regenerating every own exact case/header and control record and comparing the complete expected JSON. `--emit` prints those regenerated compact records; no network, solver or native package is required. The normal and optimized results agree. No Python assert supplies a correctness gate.

Expected: 135 hash-identified incidence matrices, zero-word counts 92/78/42/11/1, 41 uniquely tagged nonempty-domain cases (12/18/3/8 by the four surviving deficit patterns). There are 94 empty individual domains, 15 empty initial binary relations, 22 first-round path failures and 4 second-round path failures. All eight degree-seven cases are included; the single degree-six incidence is rejected physically. Path consistency removes 222,560 unordered star pairs. All 4,096 three-variable binary networks, 1,024 six-point graphs and the credited known 21-point positive completion pass their relevant controls.

CENSUS.json is a 6,078-byte credited finite input. Its mathematical completeness is inherited from REVIEW 8808's independent column-partition proof, not from digest agreement. The checker proves that the new deficit-three/four word sets add no word to the old reviewed 97-word universe and checks every census entry. Its canonical compact matrix digest is `95b5e500fb3c9f05257b7083ecfa3da25974031ac5ae8cfa94cb91aba98b75ce`. The source, prior reviewer and exact pinned hashes are recorded in PROVENANCE.json. The own expected record freezes summaries only; large relation/deletion traces are not published and are recomputed.

Optional original-output comparison: in a checkout containing the original source pinned at 73541f65acb727908733d83b07481f65be96afb4, run the producer and solver sequentially, keeping generated output outside the source directory:

```sh
python3 -B round-two/six-books-3/near108-local14/generate.py --output-dir /tmp/books108-original
python3 -B round-two/six-books-3/near108-local14/solve.py --output-dir /tmp/books108-original
python3 -B round-two/six-reviewer-4/deficit-four-root-audit/compare.py /tmp/books108-original --controls
python3 -B -O round-two/six-reviewer-4/deficit-four-root-audit/compare.py /tmp/books108-original --controls
```

The comparison validates every original incidence, unique tag and exact physical domain and rejects eight altered inputs. The original generator/solver is never imported by the independent checker. All ten original native replay commands passed separately, including complete multicover/literal proof algorithms and native damage controls.

The finite proof imports reviewed 8808's raw census and ordinary classification. General nonregular root refinement also uses its reviewed 109 branch. Arbitrary-valid use imports only 8012's maximum-degree-ten theorem. No global 108-edge exclusion, historical-priority claim, new global degree-floor novelty, formal-proof result or Ramsey endpoint follows. Ordinary arguments remain unformalized. Fixed process/round guards raise incomplete-result errors rather than mathematical verdicts; all actual runs completed under existing limits.
