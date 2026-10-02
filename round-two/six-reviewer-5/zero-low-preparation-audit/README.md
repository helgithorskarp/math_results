# Independent HIGH3 preparation audit

Actual reviewer: **six-reviewer-5**, independent mathematical reviewer.
Confirms committed LEMMA9661's complete181-function necessary cover for
its literal P27 / zero-prior-LOW branch. Proves that actual preparation
words before the first LOW singleton have at most six comparisons,
and that the full function determines their admissible word length.
All singleton/tail stages, other branches and the global endpoint stay open.

Read [REVIEW.md](REVIEW.md) and [REFINEMENTS.md](REFINEMENTS.md) for exact
hypotheses, ordinary reductions and trust boundaries. This is a full
original-domain audit, not a marker-profile approximation.

CPython3.12.14, standard library only. Set OMP_NUM_THREADS,
OPENBLAS_NUM_THREADS, MKL_NUM_THREADS, VECLIB_MAXIMUM_THREADS and
NUMEXPR_NUM_THREADS to1. Run sequentially from this directory:

```sh
python3 -B verify.py
python3 -B -O verify.py
```

Expected status: COMPLETE_ORIGINAL_CUBE_COVER_AND_ACTUAL_SIX_GATE_BOUND_VERIFIED.
Counts:338 original profiles /90 tight domains /9 activity images /
374 full functions /446 edges /193 exits /181 retained /actual bound6.
All745472 original cube assignments are also checked against independently
reconstructed oriented carrier words; all395264 cut assignments and all193
full wrong-rank witnesses are replayed.395 positive sorter controls,
eight evidence damages and the marker-conflation/orientation countercontrols
pass. Every edge has its exact inversion-potential decrease and grading.

Complete80790B EVIDENCE.json SHA256:
58fad9b96c9baf378c73d964dbd4429a48607b30e472c6a84c3cf068f809e899.
Full32-row functions are encoded as32-byte hex arrays; row equality is
checked completely. No large external corpus or solver is needed.

Optional network-enabled pinned native reproduction:

```sh
python3 -B reproduce_author.py --scratch /tmp/fresh-high3-preparation-replay
```

Use an empty fresh scratch directory. All eleven source files are pinned;
four native generate/verify children run strictly serially, each with the
same45-second guard, followed by the owned full comparison. All11968
function rows,446 edges,193 original cuts,374 shortest distances,
nine activity images and136 parent states are compared. Native ten damage
controls reject in both modes. Its certificate SHA256:
bdfdc23f34cffe622f623d00f4b005d57de1388c307a9662ab93b351c1d37257.

INDEPENDENCE.json records the six-file core/proof seal before native
materialization; the defining written proof/counts were visible throughout.
The first mistaken max7 expectation was corrected to kept6/whole7 before
native access. This is not a blinded or historical-priority claim.
VALIDATION.json records actual unchanged guards/costs and strict serial work.
Imported S11>=35,S12>=39, ordinary pruning/standardization/threshold/cut
bridges and code correspondence remain unformalized.9529's negative
corpus and the entire9616/9590 parent applications are not re-reviewed.
