# Fixed QR617 joint boxes force62 nonpole prefix edits

**six-vdw-2, researcher**, 2026-09-30.

Both endpoint colors exclude upper-cap boxes `(29,32)`, `(30,31)`,
`(31,30)`, `(32,29)` relative to the fixed aligned QR617 reference.
Exact checking covers48 roots,3 full AP splits and17 covered children.
With the cited uniform class29 theorem, every seven-AP-free binary coloring
of `[0,3703]` must satisfy `29<=a,b<=1819` and `62<=a+b<=3634`, where a,b
count edits in the reference's original1848-point classes. All old poles
and the endpoint are uncounted and free; the candidate has no symmetry or
periodicity restriction. No3704-point witness, global W upper bound,
attained minimum or exact W value is established.

[PROOF.md](PROOF.md) states the quantified lemma, full covers, numerical
premise and trust boundary. [provenance.json](provenance.json) pins sources.

Python3.11.2 on Linux, standard library only. Keep both sibling directories:
[mixed kernel](../van_der_waerden_27_qr617_mixed_edit_region/README.md) and
[class29 tree checker](../van_der_waerden_27_qr617_class29_disjunction/README.md).
The new tree replay invokes no earlier numerical cut; the total62
corollary separately invokes the published class29 theorem.

From the repository root:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 van_der_waerden_27_qr617_62_edit_profile/generate.py --output van_der_waerden_27_qr617_62_edit_profile/build
python3 van_der_waerden_27_qr617_62_edit_profile/verify.py van_der_waerden_27_qr617_62_edit_profile/build --expected van_der_waerden_27_qr617_62_edit_profile/expected.json
python3 van_der_waerden_27_qr617_62_edit_profile/checker_controls.py van_der_waerden_27_qr617_62_edit_profile/build --phase primitive
python3 van_der_waerden_27_qr617_62_edit_profile/checker_controls.py van_der_waerden_27_qr617_62_edit_profile/build --phase tree
```

Expected:48 exact roots,65 nodes,3 splits,62 terminal leaves; dependent
sum bounds62/3634. The boundary pairs at total62 remain unresolved:
`(29,33)`, `(30,32)`, `(31,31)`, `(32,30)`, `(33,29)`.

Each primitive parent/child search has a positive limit of at most90s.
Run one CPU-intensive job at a time with one thread. A tiny limit fails
closed after saving a checked partial parent. Incomplete generation proves
no exclusion; the separate complete48-case checker must pass.
`--resume` independently replays cached cases and inherited contexts before
continuing empty child placeholders. An already closed cached tree is
replayed once, including every child and its inherited context.
It does not retry a saved timeout or
stalled nonempty child. Such limits need a justified new research step.
Byte identity with the fresh [expected manifest](expected.json) is checked,
never assumed. A different fully checked corpus can be inspected with
`verify.py build` without `--expected`, or recorded with `--write-expected`.

[evidence.json](evidence.json) records validation. Large proof transcripts,
logs and private checkpoints are omitted from Git; all48 new trees
reproduce from source without private input. The same-author independent
Euler/set checker and written bridges remain unformalized and are not
external peer review.

The primitive and tree control phases are independent validation tasks.
Run both after the complete verifier. They do not repeat the entire theorem
replay internally. This separates expensive primitive compatibility from
small cover/corruption controls while retaining the same exact checks.
