# H7/F617 phase-ten adjacent-run density

Author: **six-vdw-2, researcher**. This is a conditional exact lemma in the
two-color, seven-term van der Waerden construction family.

For an admissible H7-invariant coloring of F617*, write
`y_i=c(3^i)` and `f_i=y_i XOR y_(i+44)`. If a phase value occurs exactly ten
times, each run of that value of length at least two has a third occurrence
within positions two through six from the run start. Equivalently, the selected
phase pattern `0 1 1 0 0 0 0 0` is forbidden at every cyclic position.
Both phase values are covered separately. [PROOF.md](PROOF.md) states the
quantifiers, normalization, six excluded cases and dependencies.

The prior selected-adjacency lemma ensures that such a run exists. This result
does not exclude phase weights 10 or 34, strengthen the nonconstant phase band,
or supply a 3704-point coloring. The remaining adjacent heads are unresolved.

The files regenerate six DIMACS models with the actual field constraints and
an exact-seven prefix counter. The independently written literal-residue
auditor reconstructs every clause and every gate. The inherited strict RUP
kernel checks all positive propagation hints through an empty clause in normal
and optimized Python. Neither native SAT answers nor DRAT conversion are trusted
as a mathematical certificate.

Use a complete repository checkout: fifteen required helper/premise files in
sibling directories are byte-pinned by [SOURCE_PINS.json](SOURCE_PINS.json).
Use Python 3.11.2, `python-sat==1.8.dev24`, `six==1.17.0` and CaDiCaL195.
Compile `drat-trim` from the source URL/hash in that manifest, retaining the
source as `drat-trim.c` beside its executable. Put the converter, environment and
all generated outputs in a scratch directory outside tracked source.

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python round-two/six-vdw-2/order7-phase-ten-adjacent-density/reproduce.py \
  --work /tmp/vdw-adjacent-density-work --converter /tmp/vdw-tools/drat-trim
python round-two/six-vdw-2/order7-phase-ten-adjacent-density/guards.py \
  --checked-work /tmp/vdw-adjacent-density-work --work /tmp/vdw-adjacent-density-guards
```

Expected final status: `EXACT_H7_PHASE10_ADJACENT_RUN_DENSITY_LEMMA`, six cases,
125492 strict additions and 2094091 checked hints **per Python mode**. The
canonical CNF/proof hashes are in [EXPECTED.csv](EXPECTED.csv). A different
valid regenerated proof may establish the same claim without reproducing the
proof bytes. Optional `--certificate-cache DIR` uses `DIR/head/STEM.lrat` as an
untrusted candidate and still regenerates/audits the model and strictly checks
the proof twice. `--resume` replays already checked positives without repeating
an identical bounded failure.

Native proposals request 50000 conflicts with a 30-second external limit;
conversion uses 25 internal/30 external seconds, strict replay 30 seconds per
mode and definitions 55 seconds per stage. Stop at an incomplete stage. A private
follow-up model returned UNKNOWN and is deliberately absent from this positive
reproduction fixture; its status and digest are retained in
[VERIFICATION.json](VERIFICATION.json). Do not repeat it as an identical search.

Only compact source, hashes and summaries are published. Generated models,
native proof streams, LRAT files, caches and logs remain scratch artifacts.
[VALIDATION.md](VALIDATION.md) records the separate algorithm checks and trust
boundaries. This is an author-checked, unformalized claim; no external independent
review is asserted.
