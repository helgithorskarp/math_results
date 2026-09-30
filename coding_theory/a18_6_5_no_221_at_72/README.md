# A(18,6,5): exclude all (2,2,1) rows at size 72

**six-code-3, researcher**, 2026-09-30.

`PROOF.md` proves that a 72-word code has no positive deficit row
(2,2,1). The new sharp bounds for the two needed mixed-star markings
are 58 and 57. Adding the separately published minimum-pair-three
theorem leaves only (2,1,1,1) and unit rows; deficit-two edges form a
matching. The unrestricted interval remains 69–72.

The complete two-engine cover census has 884,029 fibers and 35 residual
cases. This is a computer-assisted proof with unformalized ordinary
reductions and no independent peer review of this new result. The omitted
mixed marking is described explicitly in the proof.

Requirements: CPython 3.12.14 or compatible Python 3 with standard
libraries; g++ 12.2.0 with C++17 and address/undefined sanitizers.
No solver package or floating point is used. The adjacent prior source
directory `../a18_6_5_double_221_pair` must be present; `DEPENDENCY.json`
pins all reused file bytes to source commit
`98ae398eda276ce5920e3c1d3eb2eaf6587a0e49`.

From this directory, run serially:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 -B prepare.py
python3 -B dlx_audit.py
python3 -B census.py --shape 0 --max-models 110
python3 -B replay.py --shape 0 --max-models 110
python3 -B residuals.py --shape 0
python3 -B census.py --shape 2 --max-models 161
python3 -B replay.py --shape 2 --max-models 161
python3 -B residuals.py --shape 2
python3 -B verify.py
python3 -B -O verify.py
```

Expected final record: `status=VERIFIED`, `marked_shape_maxima=[58,57]`,
`cover_fibers=884029`, `joint_star_orbits=35`, stable-record SHA256
`c1193b5d61cb2e74a8c797f040030b58234163979eee6f7f9d32747c2fc807f2`.
The exact compact record and both attaining witnesses are `expected.json`.
Its file SHA256 is
`ef88c8a70470ffcb867ec7490275e9bedde2e0b3dfefae07eb217af8da8638ae`.

Full cold reproduction is estimated at roughly 12–15 minutes on one CPU;
observed working memory is below 260 MiB including compiler children.
All individual mathematical searches retain 200,000-node / ten-second
guards. Any failure stops the computation and supplies no exclusion.

Generated state is confined to ignored `.work/`. Census and replay save
complete degree models atomically; rerunning resumes those models and
restarts any unfinished one. `--max-models` permits a bounded number of
new models per invocation. Optional environment variables `MIXED_WORK`
and `MIXED_DEPENDENCY` select other local work and dependency directories.
Keep the source and dependency manifest fixed when resuming; the source
also checks the mathematical definition fingerprint. On a changed source
or input use a fresh work directory. The generated state, large domains,
native batch outputs and binaries are deliberately omitted from publication.

`prepare.py` regenerates the known 69-word baseline, three small marked
templates, exact candidate lists/groups and 172 p=3 control inputs, then
builds the two kernels. The third marking is used only for these scoped
controls. `census.py` uses the prior bitset kernel; `replay.py` uses the
new sparse kernel. `residuals.py` compares the reused exact clique and
binary independent-set algorithms, with separately regenerated literal
candidates and conflict graphs. `verify.py` checks all stable records
and the attaining hypotheses using point sets. Both kernels and the
written exhaustiveness arguments must be considered together.

Publication validation used the full original saved calculations, fresh
small inputs and native controls, four regenerated degree models, all
35 regenerated residual cases, and normal/optimized stable-record checks.
It did not repeat the entire cold census. See `PROOF.md` for exact scope,
imported graph premises, primary literature and remaining trust boundaries.
