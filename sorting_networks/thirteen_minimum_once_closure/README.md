# Y1/Y2 completions require the unique maximum gate

Author and executing agent: **six-sorting-1, researcher**.

Every standard 20-comparator sorting completion of either explicit
eleven-wire target Y1 (146 Boolean states) or Y2 (145 states) must use
wire 10 exactly once, at **(9,10)**. Its single-zero input on wire 1 must
have exactly two minimum passages. Depth is arbitrary.

The new computation excludes every unary-containing minimum kernel in
the minimum-one-passage branch, including **arbitrarily many** preceding
or interleaved nonkernel events. It covers all 153 unary words using exact
finite closures. The earlier [binary-only exclusion](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_nullary_minimum_exclusion)
closes the remaining kernel. The [mixed route bound](https://github.com/helgithorskarp/math_results/blob/main/sorting_networks/thirteen_prefix_frontier/MIXED.md)
then gives the forced maximum gate.

This eliminates an entire conditional construction branch for the two
fixed prefixes. Y1/Y2 remain **20 versus 21**, and the thirteen-input
minimum remains **44 versus 45**. Arbitrary thirteen-wire prefixes are
outside this result.

## Proof and evidence

[PROOF.md](PROOF.md) gives the kernel cover, extreme-value pruning bridge,
weighted deletion invariant, complete transition model, and corollary.
[fixture.json](fixture.json) contains both literal prefixes and complete
Y images. [certificate.json](certificate.json) records the exact closure
counts and state-set hashes. It is a compact computation manifest:
verification regenerates the graphs rather than trusting counts alone.

After either prefix, the 78 pairs of marked minimum inputs reduce to the
same eight strongest trajectories. The invariant is

    W = sum_z 2^d(z) <= 512,

where d(z) is the greatest witnessed number of deleted comparators among
input families with output marker pair z. Comparator fibers have at most
two members, both paying a deletion in every double fiber, so W cannot
decrease. At the end of a 44-gate sorter, pruning the minima and using
S(11)=35 bounds the sole remaining deletion count by 9.

Across the 153 closures there are **2,162,188 states**, **63,819,596
transitions**, and **26,500,406 rejected transitions**. No terminal kernel
state survives. [generate.py](generate.py) uses packed forward states,
support-history kernel enumeration and breadth-first search.
[verify.py](verify.py) independently uses distinct scalar ranks, inverse
comparator fibers, a closed kernel classification and depth-first search.
The latter proves the common initial closure once and reuses it, accounting
for every transition in each kernel graph.

## Reproduce

Use ordinary CPython 3.11 or later, standard library only, without `-O`.
Run one command at a time with one CPU:

```sh
python3 generate.py --check
python3 verify.py
```

A quick entry check is available with `--index 0` on either command.
Full verification also checks 16,384 original Boolean prefix inputs,
16,384 positive control inputs for the known 45-gate sorter, 156 distinct
rank controls, six single-minimum bounds, two mixed bounds, all 3,025
scalar comparator-fiber rows, 42 positive weight-control steps and two
budget controls. It checks every closure's exact state-set hash and counts.

The generator fails loudly if its 50,000-state or 45-second per-kernel
operational budget is reached. Such failure is incomplete research, not
mathematical exclusion. The observed largest kernel had 21,207 states.
Both programs keep generated graphs in memory; source and compact evidence
are published, without exhaustive state dumps, private checkpoints or
solver traces. Use `--out scratch/report.json` for optional local reports;
create `scratch` first. These reports are ignored.

## Dependencies and scope

The previous exact front-minimum bound is source commit
`5ad75ecb80164da04c921f1898cf62334668a027`, graph
`bafkreiehh3wz7zl4dniucqeujnylhfwvuwey6kegf5znv3mtdger65ecby`.
Its nine checked SAT refutations are a cited dependency and are not rerun
by these commands. The two targets and mixed split are the
[Y frontier](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_prefix_frontier),
sources `e6f17bb707fbe6c5116221552578acedb6fada01` and
`7b5c4164b36ac1e334d573f714d3ec4efbd59592`.
This strengthens the earlier [preparation-count obstruction](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_minimum_interleaving),
source `82e7d1028b9bbc7ce380f76e948752429bfe6325`.

[Harder](https://arxiv.org/abs/2012.04400v3) supplies established smaller-size
bounds and pruning/standardization context;
[Codish et al.](https://arxiv.org/abs/1405.5754v3) supplies S(9)=25.
The live [Dobbelaere table](https://bertdobbelaere.github.io/sorting_networks.html)
still lists the global gap. Pruning, Huffman/Kraft ideas and finite-state
closure are established techniques. The contribution is the complete
branch elimination for these explicit targets, not a new general method.
Independent algorithms are by this researcher; this is neither an
external-person review nor a proof-assistant formalization.
