# Repeated-(1,2) class13: boundary-touch certificate

**six-sorting-1, researcher.** This is a compact, solver-free certificate
excluding the entire repeated-effective-(1,2) class of the exact B11 C22
problem: class code `349871875148001158693749134458897`, all 5,385
effective event orders, arbitrary allowable depth. It closes all five
tail instances of the published single-preparation reduction. Combining
the prior 417-class frontier with this exclusion leaves 416 necessary
classes. Global S13 remains 44–45 and B11 remains 22–23.

Combined with six-sorting-2's disjoint
[61-row ten-event class exclusion](../../sorting13_B11_image61_depth_free_exclusion/PROOF.md),
published during this pass, the frontier is **415** necessary classes:
89 ten-distinct, 297 eleven-distinct and 29 eleven-repeated. Its reported
clause audits, native DRAT check and Python RUP replay are an explicit
import for that cumulative count. This researcher's five obstructions
are independent of the peer solver proof.

The [proof](PROOF.md) uses one sorted marked control row per representative
prefix. Known S9=25 or S10=29 bounds how many physical tail comparisons
can touch the first one or two middle wires. Other literal input rows
force more comparisons to touch that boundary. The five cap/required
pairs are `2/3, 0/1, 1/2, 0/1, 0/1`.

The complete class-to-five-tails equivalence is an imported premise from
[the sibling single-preparation source](../thirteen_single_preparation_normal_form/PROOF.md),
graph8126, original source commit
`9e233924e79cc8a4b52001cda87cc8f56db3003c`. The two exact parent input
files are checked by their byte hashes; see [dependencies.json](dependencies.json).
The new proof also records the correction of the two row counts swapped
in that parent proof's displayed table: image16 has 51 rows, image18 has
54. The parent certificate already contained the correct row sets.

From a checkout of the source repository, with this directory and
`../thirteen_single_preparation_normal_form` present:

```sh
python3 -B generate.py
python3 -B verify.py
```

Python3.11+ standard library only; no solver or proof-trace download.
Assertions must remain enabled. Use `--parent /path/to/parent` to change
the sibling parent location. An alternate certificate may be given to
the checker with `--certificate path.json`.

The generator uses weighted profiles and Boolean integer masks. The
independent checker uses labelled support sets, scalar row lists, and
actual distinct negative marks against every free Boolean assignment.
It imports neither the generator nor a solver. Expected checker status
is `INDEPENDENT_CLASS13_BOUNDARY_EXCLUSION_VERIFIED`, with:

| Check | Completed cases |
|---|---:|
| Full13 prefix inputs over five cases | 40,960 |
| B11 prefix rows | 790 |
| Actual marked/free assignments | 4,096 |
| Local Boolean row/comparator cut checks | 36,864 |
| Mandatory internal comparator checks | 36 |
| B11 reconstruction inputs | 8,192 |
| Known full45 positive-control inputs | 8,192 |

The compact [certificate](certificate.json) has canonical SHA256
`0791a0bd8b4501a2912e9a85f0456c3f8ed236a30830780d6be4a59ea1ba6052`.
[source-manifest.json](source-manifest.json) records file hashes, versions,
measured checks and malformed-certificate rejection controls.

This is a written unformalized intermediate lemma with algorithmic checks
by the same researcher, rather than an external review or formalization.
The established S9/S10 bounds and the complete parent reduction are
explicit imports. The proof includes the zero-one, marked-pruning and
boundary-count bridges. It covers this necessary B11 effective class;
other B11 classes and other thirteen-input prefixes remain live.

Only compact source, fixtures and certificates belong here. Private SAT
instances, traces, ledgers, solver environments and checkpoints are excluded.
