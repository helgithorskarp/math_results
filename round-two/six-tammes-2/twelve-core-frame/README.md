# Twelve-point twenty-contact frame

Actual author **six-tammes-2**, role **researcher**, 2026-10-02.

[PROOF.md](PROOF.md) gives a complete two-parameter reduction for twelve
distinct unit points with twenty specified contacts, on the closed cosine
interval `[14/25,593/1000]`. Only `epsilon=-1,eta=+1` can pack, and its
Gram discriminant satisfies `g>1/2`. Exactly 33 intercluster comparisons
remain. A thirteenth point and its two contacts are unnecessary.

This is a conditional core reduction. A fifteen-point code leaves three
arbitrary additional points. No optimizer occurrence, three-point capacity,
critical strip, new global bound or optimality is asserted. Independent
researcher review and formalization remain pending.

## Reproduction

Tested with **Python3.11.2**, standard library only. All mathematical
operations are exact rational functions or outward dyadic intervals; no
floating-point sign, random seed, CAS package or solver is needed.
Run from the repository root, sequentially, with one mathematical job and
native threads one. Each new replay output must not already exist.

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
G20_REPLAY_DIR=$(mktemp -d /tmp/g20-replay.XXXXXX)
python3 round-two/six-tammes-2/twelve-core-frame/replay.py --describe
python3 round-two/six-tammes-2/twelve-core-frame/replay.py --start 0 --output "$G20_REPLAY_DIR/range-0.json"
python3 round-two/six-tammes-2/twelve-core-frame/replay.py --start 2500 --output "$G20_REPLAY_DIR/range-2500.json"
python3 round-two/six-tammes-2/twelve-core-frame/replay.py --start 5000 --output "$G20_REPLAY_DIR/range-5000.json"
python3 round-two/six-tammes-2/twelve-core-frame/replay.py --start 7500 --output "$G20_REPLAY_DIR/range-7500.json"
python3 round-two/six-tammes-2/twelve-core-frame/replay.py --start 10000 --output "$G20_REPLAY_DIR/range-10000.json"
python3 round-two/six-tammes-2/twelve-core-frame/identities.py
python3 round-two/six-tammes-2/twelve-core-frame/controls.py
```

Execute all five ranges, with every requested literal actually checked.
One invocation, a saved cursor, a manifest or matching aggregate counts
does not reproduce the whole certificate. Each range checks at most 2500
literals, with 50 slogical/55 shard, depth22 and20000 nodes-per-tree guards.
A timeout, incomplete range or failed predicate proves no exclusion.

Expected structure:12091 leaves/24178prefix nodes, in four complete closed
partitions. The first three exclude the other orientations; the fourth
excludes `g<=1/2` on the surviving branch. The fixed
[PLAN.json](PLAN.json) is25451 bytes, SHA256
`cfbd89375154380d281174ad8f37ea42cf9ab7f8d284fc50965c31f8a3536506`.
[LITERALS.json](LITERALS.json) binds the42 typed surviving-point predicates.

The exact identity checker verifies63 rational identities, including twelve
unit identities, eighteen internal contacts, twelve noncontact products,
the circle chart coefficients and denominator bounds. The controls reject
20 damaged structures, accept changed JSON field order and harmless metadata,
and check nine arithmetic boundary cases, including square-root zero.
Both auxiliary programs also passed with Python `-O`, with identical
complete output and no assert-dependent guard.

[VALIDATION.json](VALIDATION.json) records all five actual ranges under the
same four-file source pins, plus actual auxiliary costs and complete control
results. The final2091-literal run took3.446634 seconds wall/18264 KiB RSS;
the largest auxiliary child RSS bound was30244 KiB. Existing1CPU/2GiB
scope and55 second guards were unchanged.

The complete ordinary geometry and feasible-subset/clipping/coverage
arguments are in [PROOF.md](PROOF.md). The programs and those arguments
are author checks. They are not independent researcher review or a formal
proof assistant result. See [DEPENDENCIES.md](DEPENDENCIES.md) and
[LITERATURE.md](LITERATURE.md) for credited prior work and exact scope.
Private repair forests, exploratory notes, operational checkpoints and
large transient data are not runtime inputs and are not published.
