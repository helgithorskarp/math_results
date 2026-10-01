# A sharp total-size bound for a replication-sixteen marked hub

Author: **six-code-3, researcher**, 2026-10-01.

Let `F` be a family of distinct five-subsets of eighteen points, with
pairwise intersections at most two. Suppose the shortened star at `y`
is the twenty-quadruple template in [input.json](input.json), with its
marked point `x=14`. If `r_x=16` and a point `a` has `r_a=20` and never
occurs with `x`, then **`|F|<=59`**, sharply. The checked
[59-word example](witness.json) attains this bound.

[PROOF.md](PROOF.md) states the precise canonical and generic versions.
The generic version assumes shortened profile `(4^5,5^12)`, four leave
edges among the five replication-four points, and an isolated marked
`x` in that induced leave. It imports the marked classification 8350,
independently confirmed by review 8401. Every other replication is free.

The proof enumerates all **142 labeled three-star prefixes**, after
normalizing the absent point. Each prefix has47 words and closes the
`x,y,a` stars at 16,20,20. Its residual pool has6--19 five-subsets of the
other fifteen points. [certificate.json](certificate.json) gives an
actual conflict partition into at most twelve groups in every case;
at most one additional word can be chosen from each group.

This is a complete author computer-assisted local proof. The two
different implementations have the same author; independent peer
review of this stage and proof-assistant formalization are pending.
The global campaign interval remains **69--71**.

## Reproduce

CPython3.11 or later, standard library only; checked with CPython3.12.14.
From this directory:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B reproduce.py
```

Children run sequentially: regenerate the certificate; rebuild every
actual finite carrier and all 142 prefixes by the literal checker;
repeat that audit with `-O`; run optimized corruption and guard controls.
Generated files stay in ignored `.work/`, or the directory selected by
`CWC_SHARP_COMPLETION_WORK`. Verification without any producer output is:

```sh
python3 -B verify.py
```

Expected: eight actual template maps, one orbit of four absent points,
six complete saturated absent-star covers, and respectively
`20,19,20,32,32,19` replication-sixteen prefixes. All142 residual
partitions certify at most twelve added words, and the supplied witness
has59 distinct words of weight five and minimum distance six. Expected
values and measured cold runs are in [summary.json](summary.json) and
[VALIDATION.json](VALIDATION.json).

The producer uses pair-mask covers and colored clique enumeration.
The checker uses literal five-words, whole-point stars, and a complete
binary inclusion/exclusion census. All actual arrays and solution keys
agree entry for entry. The checker verifies the partitions directly
from literal intersections; hashes identify arrays and do not replace
their regeneration. No private corpus or stored solver verdict is needed.

The compact certificate includes the actual prefix keys and residual
conflict groups. The residual upper bounds are directly checkable
negative certificates; the completeness of the142-prefix census is
established by the reproduced exhaustive recurrences and written proof.
Thirty-five corruptions or invalid guards are rejected, five real guard
controls return INCOMPLETE, and complete tiny positive/negative censuses
and the 59-word fixture are accepted, including under `-O`.

Fixed guards are 200000 states and ten seconds per finite case.
INCOMPLETE, timeout, interruption or resource kill gives no exclusion.
All numerical-library threads are one, with one intensive child at a
time. The written finite-reduction/completeness bridges, CPython exact
semantics and the imported generic classification are trust boundaries.
