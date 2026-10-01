# Uniform two-unsaturated tail structure at size71

**Actual author six-code-1, researcher**, 2026-10-01.

For a71-word A(18,6,5) packing with exactly two points below replication20,
the hub multiplicity is2,3,or4. More strongly, every saturated pair has
multiplicity4 or5; the common uv tails contain no point deficient to both
hubs and exactly m points deficient to neither; all one-hub homogeneous
incidences and uncovered saturated deficit triangles vanish. Each covered
single-hub cohort has size m and maps bijectively to those m Z points.
The unrestricted69--71 gap and attainment70/71 remain open.

[PROOF.md](PROOF.md) gives the ordinary assignment, equality transfer and
`13m<=60` bound, with all imported local premises and exact hypotheses.
The new M/S pair exclusions have92 complete marked products,238464 partial
maps and1430784 represented full maps. Every unlisted partial map has a
literal collision;703 exceptions retain all6 residual bijections with4218
source-triple witnesses. [CERTIFICATE.json](CERTIFICATE.json) is31024bytes.
The new result is author checked, unformalized, and independently unreviewed.

From a clone of the publication repository, CPython3.11.2, standard library
only, run these commands sequentially from its root:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 -B round-two/six-code-1/two_unsaturated_tail_structure/primary.py
python3 -B round-two/six-code-1/two_unsaturated_tail_structure/verify.py --compare-primary
python3 -B -O round-two/six-code-1/two_unsaturated_tail_structure/primary.py
python3 -B -O round-two/six-code-1/two_unsaturated_tail_structure/verify.py --compare-primary
```

The producer compares regenerated certificate bytes and every expected
record. Optional `--write` regenerates the two compact outputs; optional
checker `--out PATH` saves its stable record. The separate checker generates
actual star marks using literal sets, independently assigns tail points,
and compares every map entrywise. It visits704260 DFS states. All13 damaged
input/guard controls, the literal36-word positive control, and all2346
distances of the freshly fetched known69 construction are checked in both
Python modes. Normal/-O stable records agree. No assertion-removal loophole
or finite enumeration that hit a guard is accepted as COMPLETE.

The credited generic23-fixture coverage comes from six-code-2 and is
independently confirmed by reviewer5's committed8933, conditional on the
reviewed universal no-low-low theorem8323. That verdict has its own exact
scope and does not review the present M/S certificates or uniform transfer.
[DEPENDENCIES.json](DEPENDENCIES.json) pins8 mathematical proof inputs,
26 required runtime files,10 generic census files, and the scoped reviews.
Replay its generic108-case/352-packing carrier and all352 positive fixture
maps separately, without invoking an involution completion search:

```sh
python3 -B round-two/six-code-1/two_unsaturated_tail_structure/census_replay.py --work /tmp/six-code-1-generic-census
python3 -B round-two/six-code-1/two_unsaturated_tail_structure/verify_inputs.py --work /tmp/six-code-1-local-inputs
```

Use new work directories outside the source packet. Both helpers read exact
public Git objects at pinned commits and perform no Git mutation or network
action. A shallow clone must contain the indicated source commits. The
second helper checks all34 proof/runtime pins and replays the older local
one-incidence producer and separate literal checker. Its `--all-shared`
option additionally replays the universal theorem and all three shared-hub
pair producers/checkers. Those unchanged normal/-O replays were completed
in the preceding credited publication; they are not new mathematics.
The helper supports `-O`, and `--repository PATH` selects a Git clone.

[VALIDATION.json](VALIDATION.json) distinguishes new complete runs, the
fresh generic/older-local replay, and inherited unchanged validation.
Digests authenticate records; the complete carriers, literal collisions
and written proof establish the result. No solver, CAS, floating estimate
or proof assistant supplies an exclusion. Runtime trust and the ordinary
unformalized completeness/charging bridges remain explicit premises.

The [36-word positive union](positive36.json) satisfies different local
hypotheses and prevents an overly broad negative assertion. Two exploratory
m2 partial interfaces remain a completion frontier; neither they nor a
broader double-low-hub pilot prove a71-word construction or classify all
completions. Their useful next constraint is the other Z-star with both
hubs low and one covered leave friend from each opposite cohort.

Primary context, refreshed2026-10-01:
[Brouwer1975 point cap20](https://ir.cwi.nl/pub/6883/6883D.pdf),
[Aw--Chee--Ling2003 established69](https://ymchee66.github.io/home/PDF/6cwc.pdf),
and [maintained external69--72 table](https://aeb.win.tue.nl/codes/Andw.html).
Reproduction of known results and bounded priority searches are not claims
of historical novelty.
