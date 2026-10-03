# Prime617 character flip rigidity

six-vdw-3, researcher. An AP7-free interval coloring with N>=3702 that differs anywhere outside the root from a single constant-phase affine quadratic-character baseline must differ in **at least 22 nonroot residue columns**. Thus a3704 extension needs at least 22 extra edited columns. See [the proof and exact scope](PROOF.md).

At3703 the family allowing at most 21 extra edits has exactly 252 actual colorings. This is a restricted-family classification around the historical seed, not a new lower bound for W(2,7). No22-edit completion has been found or excluded.

From the repository root, with **CPython3.11.2 and standard library only**:

```sh
python3 round-two/six-vdw-3/character617-flip-rigidity/reproduce.py --output /tmp/character617-fresh
```

Use a new empty output directory. The driver runs one mathematical child at a time, sets numerical thread variables to1, and retains a fixed20-second guard per child. A timeout leaves a partial execution receipt and proves no exclusion. The final `summary.json` must match [expected.json](expected.json) in its entirety. Final source hashes and sizes are pinned in [SOURCE_PINS.json](SOURCE_PINS.json).

[generate.py](generate.py) constructs Euler-character endpoint data, complete field AP controls, a normalized neighborhood-intersection family, and bounded literal lift/transport records. [check.py](check.py) imports none of that implementation: it uses square sets, Euclidean inverses, incremental field APs, literal integer position lists, and a bit-mask closed-family certificate check with full successor/reachability coverage. Normal and `-O` output files must be byte-identical. The driver also requires19 deliberately damaged records to be rejected in each mode.

The source and compact expected record are public. The regenerated867-state certificate, per-batch records, execution logs and virtual environments are not published; the driver reconstructs them locally. Algorithmic independence is by the same author, not external peer review. [Validation](VALIDATION.md) states the concrete completed run and trust boundary.
