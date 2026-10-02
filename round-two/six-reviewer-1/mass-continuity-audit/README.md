# Compression-mass continuity: independent review and stronger tube

Actual **six-reviewer-1**, **independent mathematical reviewer**, 2026-10-02.

[REVIEW.md](REVIEW.md) confirms the complete ordinary Lemma9440, including
all collisions and the sharp all-n square-root-mass constant. It proves
a larger global reflection-symmetry exclusion: every balanced norm-one
real octic profile with C>=24.531 has distance to the symmetric cone
strictly greater than75034077791/3572106488496000>1/48000. The exact
radius is81/53 times the original47/2-based radius. It also proves the
same sharp mass constant for arbitrary real originals in the
translation-quotient bottleneck metric, using centered energy.

These are auxiliary real compression/angular results. The global angular
maximum and complex first-power Tang--Zhang inequality remain open.
The proof is ordinary and unformalized; uniform C=16 and the complete
symmetric C<47/2 bound are explicitly credited prior premises.

The exact checker uses literal original-coordinate compression matrices,
whole polynomial spectral projectors and their differentiated quadratic
forms. It is distinct from the author's dual companion trace and
Euclid/Newton gradient checks. [core.py](core.py) reconstructs all13cases,
all projector entries/ranks, canonical labels, mass derivatives, second
moments, the free-variable sharp-family polynomial, translation and
symmetric projection controls, and every rational tube margin.
[expected.json](expected.json) is the entire typed record.

Python3.11+ standard library only; tested on CPython3.12.14. From the
repository root:

```bash
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-reviewer-1/mass-continuity-audit/check.py
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B -O round-two/six-reviewer-1/mass-continuity-audit/check.py
```

Expected statusPASS;13cases;11mathematical damage rejections;
whole canonical SHA256
91910329dc95b9eba8f3b955d8d1bcbcd80e053c07dc7adaef92b1c1b701d7de.
The checker rejects changed, missing, extra, reordered and wrongly typed
fixtures using --expected PATH, including under-O. --write refuses to
overwrite an existing fixture.

[independence.json](independence.json) records the complete independent
seal before the author executable/fixture was materialized, with exact
source hashes, normal/O timings and six external fixture damages.
The defining ordinary proof was visible before that seal.
[author-replay.json](author-replay.json) records later whole author
normal/O reproduction and eight independent scalar comparisons.

Finite exact checks corroborate the stated identities and concrete
controls. They do not replace the written all-n spectral/interlacing,
collision-limit, integration, sign-count or monotonicity arguments.
All jobs were serial/native1, internal45s/child50s guards and unchanged
1CPU2GiB; no solver, CAS, numerical eigenvalue search, large corpus or
resource escalation is required.
