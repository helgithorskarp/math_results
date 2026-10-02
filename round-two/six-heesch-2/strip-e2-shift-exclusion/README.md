# Uniform shifted-contact E2 obstruction for unmarked polyhex strips

Actual author **six-heesch-2**, role **researcher**. For every integer k>=6,
the registered contact `(I;6,4-k)` is absent from E2. See [the exact claim,
ordinary argument, complete supplier tables and scope](proof.md).
Author checked; unformalized and independently unreviewed. The finite-five
Heesch target remains unmet.

From a checkout retaining the listed sibling dependency files, run:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 round-two/six-heesch-2/strip-e2-shift-exclusion/verify.py
```

Python 3.12.14, standard library only, was used. Four serial child jobs
generate and check the certificates in normal and `-O` modes. Each has a
43-second/100000-operation guard, a 45-second signal and a 47-second outer
timeout. Source-width32, atlas128 and tree64 guards are unchanged. Guarded
or incomplete work is inconclusive. Generated certificates stay ignored;
the six compact literal inputs reconstruct every proof artifact.

`expected.json` pins ten published dependency files, both predecessor E1
input tables, the six new literal cases and the deterministic generator
and reader hashes. It records 12/13 complete point suppliers, a 19-pose
union atlas, 6/4 eligible suppliers, 24 physical cross-clashes and a
two-node main DAG. The four finite E1 collars have six total DAG nodes;
the two cap trees have eight nodes. Every reader rejects all seventeen
damaged-certificate controls. The readers are algorithmically separate
for endpoint reduction and material geometry but share kernels and are
by the same author; this is not independent review.

Dependency source commits are recorded in `expected.json`. The imported
9321 geometry is unconditional; its unproved 32-pose E2 inclusion and any
global Heesch bound are unused. The old numerical T5 value is unused.
`supplier_trees.py` reuses the generic complete-tree checker published in
9542. Runtime outputs, private search corpora and operational checkpoints
are excluded from this contribution.
