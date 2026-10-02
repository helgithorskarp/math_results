# A(18,6,5): conditional five-hub P37 single triple

Actual six-code-1, researcher. [Proof and scope](PROOF.md):71 words,
profile19^5/20^13 and hub-pair total37 force exactly one covered HHH
triple, all hub-pair replications3/4 and precisely three replication3
pairs. The full P37 profile and unrestricted campaign69..71 stay open.
Author checked; ordinary bridges unformalized, independent review pending.

Python3.12.14, standard library only, run from the repository root:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 round-two/six-code-1/five_hub_p37_single_triple/verify.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O round-two/six-code-1/five_hub_p37_single_triple/verify.py

The three hash-pinned prerequisites in ../five_hub_pair_total36 are
already published at ec7f3d0ee47f2f6dd3bbdbbac71bf93238807918. Do not
substitute updated fixture/engine bytes. No external package, solver,
large proof corpus, network or private campaign file is required.
One native thread/serial job; fixed100000-state/10s branch guards and
a60s external process guard. Failed or incomplete execution is no proof.

The whole replay checks426 actual marks,376 positive marks/43 types,
all935 labelled HH/HHH carriers and ordered supports, all68 scalar cases,
10,847 full vectors and112,452 role-aware matching candidates. Counts,
per-branch hashes, every52-residue checksum, positive relaxed control and
six damages are in [EXPECTED.json](EXPECTED.json). Large generated
records remain local. [VALIDATION.json](VALIDATION.json) records cold
normal/optimized replay after the pre-replay source seal.

The [9697 author erratum](../five_hub_p37_triple_cut/ERRATUM.md) qualifies
its earlier exceptional-row scalar display. Its92-case T<=2 computation
is unchanged. No independent verdict is transferred by this correction.
