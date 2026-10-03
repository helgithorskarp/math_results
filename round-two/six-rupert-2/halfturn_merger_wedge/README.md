# J74 finite companion-merger wedge

six-rupert-2, actual role researcher. The ordinary conditional lemma is in
[PROOF.md](PROOF.md). Global J74 is **OPEN**. The result is author checked,
unformalized and independently **UNREVIEWED**.

For original $r=(q_x-\epsilon,1,-t-\eta)$, the entire CLOSED wedge
$0\le\eta\le\epsilon\le1/905077199000$ and the physical relative
Cayley-radius $1/1000$ source gate around SET$\{G,GH,J_rG,J_rGH\}$,
every original physical translation and scale at least one are retained:
fit iff $\eta=0$, source in that SET, original translation zero and scale
one. This includes the source-branch merger. It proves no arbitrary-source
entry into the gate or strict passage.

Run from a checkout of the authorized repository. CPython3.11.2 and its
standard library are sufficient; no installed solver or numerical package
is used. All numerical/solver/BLAS/OpenMP threads must be one.

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 round-two/six-rupert-2/halfturn_merger_wedge/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -O round-two/six-rupert-2/halfturn_merger_wedge/check.py
python3 round-two/six-rupert-2/halfturn_merger_wedge/controls.py
python3 -O round-two/six-rupert-2/halfturn_merger_wedge/controls.py
```

The full expected mathematical-record SHA256 is
`14d60fc373911db0f63feaeccbc25e66825bbe4110d5fa56114a8787e4defb8f`;
ten false mathematical fixtures reject, full control-record SHA256
`841887c862d7ab1e06d8ee8971f4239eb395b55f70974ac49e9e4146eb8c880e`.
Checks are explicit and survive optimized Python.

`check.py --output PATH --transcript PRIVATE_PATH` can emit the complete
mathematical record and every original support gap. Such transient records
belong in scratch and are not publication inputs. The compact expected
record keeps every polynomial coefficient, exact constants, direct
comparison records and ordered per-support gap hashes. Whole fresh
normal/O/EMPTY relocated replay evidence is in [VALIDATION.json](VALIDATION.json).
Replays compare full entries, not only counts or hashes.

The only runtime prerequisites outside this directory are original
`../model.py` and code-only `../q5.py`, verified by full SHA256 BEFORE
import. For an isolated replay, copy this directory plus those two files
with the same relative layout into an otherwise empty directory. There
is no serialized geometry cache, old source tree, solver output or old
contact inventory input. See [DEPENDENCIES.json](DEPENDENCIES.json).
The old ordinary9961 theorem supplies boundary fixed-G sufficiency ONLY;
its full prior certificate is not newly replayed here.

The conservative finite receiving width is not an optimal or global
coverage bound. The unformalized geometric bridges in the ordinary proof,
the correctness of the compact ordered-field code, original model identity
and the explicitly named boundary dependency are the trust boundary.
Source publication and author replay are not independent review.
