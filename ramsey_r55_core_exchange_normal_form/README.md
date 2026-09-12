# Core-edge exchange normal form for good43

Every 43-vertex graph with no clique or independent set of size five has a
maximal monochromatic K4 packing satisfying a new local exchange inequality.
A lexicographic potential proves termination in at most 675 improvements.
The implementation supplies exact destinations across all q7–q10 strata.

Intersecting the resulting restrictions with the reviewed maximal-residual
carrier gives an upper certificate **0.30507766938747466... times** its previous
upper certificate. All 2,189,178 original tasks are included; 2,188,482 task
bounds improve, including every q8 task. An explicit schema also proves actual
nonredundancy on 547,361 all-red task carriers. **No task is newly decided and
no Ramsey bound changes.** These are new-family constraints, not learned
clauses for an old fixed task.

Read [PROOF.md](PROOF.md) for the theorem, counting proof and trust boundaries,
and [HANDOFF.md](HANDOFF.md) for receiver semantics.

From the repository root, with Python 3.11+ and g++ supporting C++20:

```sh
python3 -B ramsey_r55_core_exchange_normal_form/reproduce.py /tmp/r55-core-exchange-replay
```

The output directory must not exist. The script downloads four byte-pinned
McKay catalogs (about 6.6 MB expanded), regenerates the imported residual
count files in fresh scratch, and checks the new evidence. No solver is used.
With already preserved inputs:

```sh
python3 -B ramsey_r55_core_exchange_normal_form/reproduce.py /tmp/r55-core-exchange-replay \
  --catalog /path/to/catalog \
  --residual-counts /path/to/residual_counts
```

The residual directory contains `3.tsv`, `7.tsv`, `11.tsv`, `15.tsv`; their
reviewed hashes are enforced. Catalog completeness and old count theorems
remain imported even when their numerical files are regenerated. The new
824 degree keys and 1,648 two-row counts have a separate inclusion–exclusion
checker. `EXPECTED.json` holds exact class and global rational bounds.

For physical controls and the standalone receiver check:

```sh
python3 -B ramsey_r55_core_exchange_normal_form/interface_controls.py /path/to/catalog /tmp/interfaces.json
```

The mathematical frontier remains `43 <= R(5,5) <= 46`, as in
[Angeltveit–McKay](https://arxiv.org/abs/2409.15709).
The catalog inputs are from [McKay's Ramsey data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
Targeted literature and committed-graph searches found no prior instance of
this exact normal form; no historical priority for packing exchange is claimed.
This package has same-author checks and no external review yet.
