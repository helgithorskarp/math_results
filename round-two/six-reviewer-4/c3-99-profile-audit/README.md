# C3/99 Book Ramsey audit

Actual agent **six-reviewer-4**, independent mathematical reviewer.

[REVIEW.md](REVIEW.md) independently confirms LEMMA9596's two new
ordinary profile exclusions and proves a symmetry-free local obstruction.
The all99 conclusion explicitly imports earlier profile exclusions and
degree bounds; the secondary102 frontier additionally imports8971.
No102 or unrestricted22-vertex exclusion is claimed.

Python3.11+ standard library only. Tested3.12.14, native threads1,
serial mathematical children, fixed60s child deadlines:

```sh
python3 round-two/six-reviewer-4/c3-99-profile-audit/reproduce.py --out scratch/c3-99-review
python3 -O round-two/six-reviewer-4/c3-99-profile-audit/reproduce.py --out scratch/c3-99-review-O
```

The three full independent records must match RESULTS.json,
STRENGTHENING.json and CONTROLS.json byte for byte. To also repeat the
postseal author reproduction and full fixture comparison, obtain the
original11 files at the exact commit listed in AUTHOR_SOURCE.json in a
separate checkout, then use:

```sh
python3 round-two/six-reviewer-4/c3-99-profile-audit/reproduce.py --out scratch/c3-99-author --author-source /path/to/original/round-two/six-books-2/c3_edge99_exclusion
python3 -O round-two/six-reviewer-4/c3-99-profile-audit/reproduce.py --out scratch/c3-99-author-O --author-source /path/to/original/round-two/six-books-2/c3_edge99_exclusion
```

The driver checks every original source byte against its manifest before
execution and the full539-byte comparison record against COMPARISON.json.
Combined normal/O mathematics is3690 bytes, SHA256
`f677a391396e8fae0da53121fb641ef3262da0eac22df09140de3d54ac14cbd0`.
Without optional author input the same three independent records are
checked; the combined record omits the comparison component.

Core coverage:16384 ordered degree words,1128 sum matches,498 retained;
4096 labeledH words,174 relevant,1740 H/root checks and1044 parity rows.
Symmetry-free controls:165 labeled deficiency vectors and all8 low-class
graphs. Literal graph controls:14784 spines and2304 A-pair slacks. These
are original-label identity domains, not counts of valid22-vertex hosts.

Written ordinary reductions and code bridges are unformalized. Earlier
8012/9510/9554/8971 complete computations are not rerun. Existing owned
9490 is reused only for9453. The symmetry-free lemma uses no such premises.
See exact scope and hypotheses in REVIEW.md. Failure or deadline means
incomplete verification; guards are never raised. Generated domains and
receipts stay in scratch. Source contains no private ledger, key, corpus,
solver output or unrelated artifact.
