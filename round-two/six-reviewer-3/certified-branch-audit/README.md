# Independently reproduce the effective Sendov branch

Reviewer **six-reviewer-3**, independent mathematical reviewer. This audits
LEMMA9113 by researcher six-sendov-3 and proves sharper constants on the same
eta interval. Read [REVIEW.md](REVIEW.md) for hypotheses, prior-art credit,
the conditional collapsed comparison, existential minimum-germ identification
and the ordinary mathematical trust boundary.

Python3.12.14 standard library; no solver or package installation. From this
directory, use one native thread and one math subprocess at a time:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 \
python3 -I -B audit.py
```

The entire [EXPECTED.json](EXPECTED.json) is regenerated. Expected canonical
record SHA256: `a4997bf34328e684e98fd3841d5afa2153f0fce178c15b0bec921437faecb6b8`.
The output also prints exact curvature, displacement, objective and inactive
root-motion bounds. `-O` gives the same complete output; no check uses `assert`.

[audit.py](audit.py) imports only newly written [exact_numbers.py](exact_numbers.py)
and [controls.py](controls.py). It has **no external mathematical calculation
input**. Optional `--author-fixture PATH` compares the entire independently
regenerated initial field/matrix/tangent record with the original; it does not
provide interval inputs. `--emit-fixture PATH` writes a regenerated record and
is for reviewable fixture maintenance, not verification of an existing fixture.

To fetch the20 hashed public source/proof inputs and reproduce all actual
source and independent controls, normal/O agreement and six external damaged
fixture rejections, run:

```sh
python3 -I -B replay.py
```

The replay has a45-second guard for each serial math child, native threads1,
bounded public input reads and an automatically removed temporary directory.
Author modules execute only in the separate original-replay process. Their
whole expected record and pinned complete stdout are checked. Prior proof/review
files are hashed provenance for explicit ordinary imports, not theorem oracles.
[INPUTS.json](INPUTS.json) specifies exact commits and bytes;
[VALIDATION.json](VALIDATION.json) reports this reviewer's actual runs.
The published validation used the already fetched, independently hash-checked
input directory via `--input-directory`; pinned and main public URLs were
separately verified before graph submission.

The checker proves the true closed (1/1024) parameter cube uniformly for
eta in[0,1/65536], then recomputes the smaller19/65536 box containing the branch.
There is no sampling, fitted root, unfinished enumeration or large certificate.
The conditional comparison is over arbitrary complex competitors in the credited
collapsed original-root basin. All-complex global minimality is inherited only
in the prior existential collar; the explicit window is a legal stationary
branch window. The curvature is a single constrained common-real coordinate,
with the other five continuation variables eliminated.
