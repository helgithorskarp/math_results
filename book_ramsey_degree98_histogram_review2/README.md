# Independent Book Ramsey histogram audit

Reviewer **six-reviewer-2**, independent mathematical reviewer. Confirms the entire 22-vertex red-degree histogram exclusion `(3,18,1)` in graph8317, including its graph8252 three-root prerequisite, with fresh exact computation. Original mathematical credit: six-books-1, researcher. [REVIEW.md](REVIEW.md) contains the complete scope, proof audit and strengthening.

Requires Python 3.11+, standard library only. Run from this directory, with all arithmetic/solver thread variables fixed to one:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B -O audit.py --work-dir /tmp/book98-review2 --expected expected.json
python3 -B -O controls.py --grams /tmp/book98-review2/positive_grams.json \
  --work-dir /tmp/book98-review2-controls --expected controls_expected.json
python3 -B -O baseline.py
```

The first command independently rebuilds all3370 marked cubic8 cores and searches18780 profiles, without the author's graph quotient or defect enumeration. It also rebuilds41 cubic10 profiles/1087 rooted completions, generates1023 exact negative congruence witnesses, verifies64 PSD copies/four types and32 binary Grams, then checks84 exceptional placements. All placements have an impossible A star under both the original7056-candidate filter and a larger52920-candidate filter allowing all four-neighbor stars.

The second command validates a positive incidence with repeated rows, exact arithmetic against5103 principal minors,400 independent adjugate entries, the64-word root census,33 signed host controls and complete permitted-star sets. The generated Grams are positive incidence controls, not host constructions. These runtime outputs remain outside the source directory.

The third checks the known21-vertex fixture's93 edges and3/6 page maxima. To reproduce the primary-source complement comparison, download the [primary construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt) to a temporary file and run:

```sh
python3 -B -O baseline.py --primary /tmp/R_B4_B7_construction_21vertices.txt
```

The source byte digest is pinned in [INPUT.json](INPUT.json); the primary file is never executed. This known construction is validation, not new research.

Files: `domains.py` complete finite carriers; `parent.py` marked row-multiset search; `exact.py` rational congruence/inversion; `zero.py` binary Gram and literal page filters; `incidence.py` own incidence canonization; `audit.py` orchestration; `controls.py` separately written arithmetic/codegree controls; `baseline.py` known fixture checker. Expected JSON records are output comparisons, not imported mathematical certificates. [VALIDATION.md](VALIDATION.md) records completed checks and exact versions.

No numerical eigenvalues, external graph catalogue, author negative vectors, solver, proof corpus or private ledger is required. Each search/canonization fiber has200000-state/10-second guards. Guard failures raise `INCOMPLETE` or reject an invalid setting; they do not prove nonexistence. Checks stay active under optimized Python. The proof remains ordinary unformalized mathematics plus exact reproducible computation; no global Ramsey endpoint is claimed.
