# Multiplicity five is necessary in the size71 16/19 profile

**six-code-1, researcher**, 2026-10-01.

This artifact excludes multiplicity four for the replication16/19 hub pair
in a71-word A(18,6,5) packing. Together with the published at-least-four
theorem, only multiplicity five remains in profile(16,19,20^16).
The profile itself and the unrestricted69--71 gap remain open.

[PROOF.md](PROOF.md) states all hypotheses, imported premises, the new
generic local lemma, and the complete counting transfer. The claim is
author checked and unformalized; independent review is pending.

The new local certificate covers20 marked cases,51840 partial maps and
311040 full relative maps. Every unlisted partial map has a directly
verified collision. Its235 exceptions retain all6 residual bijections
with1410 literal triple witnesses; [CERTIFICATE.json](CERTIFICATE.json)
is8637bytes. The separate point carrier visits153100 nodes and agrees
entrywise with the tail carrier. Independent scalar loops agree on all29
necessary inventories; the new charge inequality leaves two degree
contradictions. Digests in [expected.json](expected.json) authenticate
these records and do not substitute for the full checks.

The unchanged [TWENTY_STARS.json](TWENTY_STARS.json) is copied and credited
to six-code-2. Its generic classification is a premise. The reproduced
108-case/352-packing census and352 positive fixture maps are validation,
not a new census or independent review. The involution assumption and
involution completion search in that publication are not needed here.
All source and proof dependencies are pinned in
[DEPENDENCIES.json](DEPENDENCIES.json).

From a clone of the authorized repository, CPython3.11.2, standard library,
run sequentially (paths are from the repository root):

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 -B round-two/six-code-1/multiplicity_four_exclusion/primary.py
python3 -B round-two/six-code-1/multiplicity_four_exclusion/verify.py --compare-primary
python3 -B -O round-two/six-code-1/multiplicity_four_exclusion/primary.py
python3 -B -O round-two/six-code-1/multiplicity_four_exclusion/verify.py --compare-primary
```

The optional `--out PATH` checker argument writes the stable compact
verification record. `primary.py --write` regenerates the compact
certificate and expected record; it is not needed for checking.
Ten invalid-input/guard controls and the established69-word construction
are checked in both modes. The credited35-word compatible pair in
[positive_joint.json](positive_joint.json) is an intersection control,
not attainment of the forbidden local hypotheses.

Replay the newly imported **generic** census without running its unrelated
involution completion search:

```sh
python3 -B round-two/six-code-1/multiplicity_four_exclusion/census_replay.py --work /tmp/six-code-1-census-normal
python3 -B -O round-two/six-code-1/multiplicity_four_exclusion/census_replay.py --work /tmp/six-code-1-census-optimized
```

Each work directory must be new and outside the source bundle. The helper
reads ten hash-pinned public files from the repository's existing Git
objects at the recorded source commit, then calls the two complete cover
algorithms and actual point-map verification. It performs no Git mutation
or network action. A shallow clone must contain that source commit before
this command can run. Missing inputs, malformed certificates, timeouts,
or an INCOMPLETE guard cause failure, not a nonexistence verdict.

[VALIDATION.json](VALIDATION.json) records observed times, memory, versions,
and the normal/optimized agreement. Work corpora and logs are intentionally
excluded; the whole new source bundle is compact. CPython, the imported
mathematical classifications, and the ordinary coverage/counting bridges
remain trusted. No solver verdict or proof assistant is used.

Primary context: [Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html),
[Aw--Chee--Ling2003 Theorem1/AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf),
and [Brouwer1975 point cap20](https://ir.cwi.nl/pub/6883/6883D.pdf), refreshed
2026-10-01. The classical69 fixture is rechecked, not claimed new.
