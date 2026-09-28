# A nonlocal, doubling-safe search checkpoint for classical S(6)

## Scope and result

The classical sixth Schur number asks for six colours on `[1,N]` without a
monochromatic `x+y=z`, **including `x=y`**. The published construction gives
`S(6)>=536` ([Fredricksen–Sweet, 2000](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32)); a checked colouring through 537 would improve it.

This directory records a bounded search for such a colouring. It found **no
valid 537-colouring**. Its best doubling-safe 537-entry word, `best4.txt`, has
four monochromatic distinct-summand triples:

```text
2+281=283    4+146=150    4+260=264    4+391=395
```

`check.py` checks every one of the 72,092 unordered classical Schur triples
directly. It confirms that `best4.txt` has no doubling violation and differs
from `seed_359.txt` at 80 entries. The seed is the previously published
[multiplier-359 one-defect word](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_537_doubling_traps/fixtures.json): its sole defect is `2+2=4`. That earlier word is still closer to a valid colouring in the raw defect count. The four-defect word is useful specifically as a starting point inside the subspace satisfying **all** doubling constraints.

This checkpoint is experimental. A score of four, an unsuccessful search, or
a solver timeout gives no upper bound for `S(6)`.

## Search design

`doubling_safe.cpp` stores only triples with `x<y` in its score. Before each
run it repairs the doubling constraints `colour(x)!=colour(2x)` for
`1<=x<=268`; every later recolouring is checked against the two adjacent
positions on that doubling chain. It scores all distinct-summand triples,
selects a violated triple, and tests legal recolourings of its three entries
with a tabu rule. Periodic weight changes and random moves, including moves
at an arbitrary position, can escape local minima. Restarts use the original
seed or the best complete word found so far. There is no Hamming-distance
limit and no old colour class is fixed. The final C++ score is checked again
by standard-library Python over **all** triples, including `x=y`.

The five-million-step run with SplitMix64 seed `10359`, 100 restarts of 50,000
steps, kick 18, 5% global noise, 5% local noise, and tabu tenure 4 yielded
the exact stored `best4.txt`. `reproduce_best4.py` reruns and compares its
entire 537-entry output byte for byte. An additional eight deterministic
two-million-step trajectories used varied kicks, noise, and tabu tenure;
`sweep.py` independently checks every returned word. Their defect counts,
by seeds `30001,...,30008`, were `4,4,6,5,4,4,4,4`.

## Reproduction

Tested with GCC 12.2.0 and CPython 3.11. The checker and C++ search need no
third-party package. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 -B check.py
g++ -O3 -std=c++20 -Wall -Wextra -Wpedantic doubling_safe.cpp -o /tmp/schur-s6-doubling-safe
python3 -B reproduce_best4.py --binary /tmp/schur-s6-doubling-safe
python3 -B sweep.py --binary /tmp/schur-s6-doubling-safe --workers 8
```

Expected summaries:

```text
PASS triples=72092 seed_defects=1 candidate_defects=4 doubling_defects=0 distance_from_seed=80
PASS replay_steps=5000000 candidate_defects=4 doubling_defects=0 exact_word_match=yes
PASS trials=8 steps=16000000 minimum_defects=4
```

The compact fixtures and code are listed in `SHA256SUMS`. Search trajectories
are deterministic under the tested compiler; the independent checker does not
trust the trajectory or the C++ scoring implementation.

## Additional solver diagnostics

The optional `prefix_probe.py` and `four_trade_sat.py` encode all classical
triples with one-hot colour variables using `python-sat==1.9.dev15` and
CaDiCaL 1.9.5. Install the pinned package with
`python3 -m pip install -r requirements-sat.txt` if rerunning them. They
verify any returned SAT model directly, but produce **no UNSAT certificate**.

Using `best4.txt` as a phase hint, fixing its first 80 entries gave solver
`UNSAT` after 11,402 conflicts. Fixing only the first 40 or 60 entries left
the solver `UNKNOWN` at 100,000 conflicts. For the seed's ten four-colour
palettes containing its defective old colour 2, all searches were `UNKNOWN`
at 100,000 conflicts per palette. The ten trades allow arbitrary recolouring
within four old classes and fix the other two. These outcomes are search
diagnostics only; an `UNKNOWN` result gives no mathematical obstruction, and
the reported `UNSAT` lacks an independently checked proof certificate.

```sh
python3 prefix_probe.py best4.txt --prefix 80 --budget 100000
python3 prefix_probe.py best4.txt --prefix 40 --budget 100000
python3 prefix_probe.py best4.txt --prefix 60 --budget 100000
python3 four_trade_sat.py seed_359.txt --defect-colour 2 --budget 100000
```

The last preprint checked for context, [*Shifted S-templates* (July 2026)](https://arxiv.org/abs/2607.15034), still uses `S(6)>=536`. The present search gives neither a new lower bound nor an unrestricted upper bound.

## Exact neighbourhood audit around `best4.txt`

The following finite checks explain why repair moves involving several
entries are needed from this particular four-defect word. They concern this
word only; they do not exclude a valid colouring elsewhere.

`two_flip_landscape.py` checks every doubling-safe recolouring of one or two
individual entries and finds no word with fewer than four violations. There
are 2,177 legal one-entry recolourings; 98 preserve score four. For two
nonadjacent entries in the doubling graph, both individual moves must be
legal. The script evaluates 233,367 pairs whose individual score changes sum
to at most six. Any omitted pair has score at least seven: its two entries
share at most two distinct-summand Schur triples, each of which contributes a
correction of at least minus two to the sum of individual score changes.
It also evaluates all 4,551 final-legal moves on doubling-adjacent entries,
including moves whose individual stages would violate doubling. The minimum
is four in every group. The incremental score formula is directly recounted
for 161 sampled pair moves and for all reported minima.

For an odd root `r`, let `D_r={r,2r,4r,...} intersect [1,537]`. A global
permutation of colour names on all entries of one `D_r` preserves all
doubling constraints. `chain_pair_scan.cpp` first scans all pairs of
nontrivial colour transpositions on distinct chains: 2,180,868 pairs from
2,093 single-chain events, with minimum score four. With `--full-root1`, it
allows any of the 719 nonidentity colour permutations on the longest chain
`D_1`, plus transpositions on other chains. Its 3,643,780 distinct-chain
distinct-root pairs also have minimum four. The stronger `--full-all` scan
allows every distinct palette permutation on either of two distinct doubling
chains. It has 15,841 nonidentity single-chain events and checks 123,114,286
event pairs, again with no score below four. Scores of all single-chain
events in the first two modes, every tenth single-chain event in full mode,
and periodic pair samples in every mode are independently recounted from all
71,824 distinct-summand triples. In full mode, 1,231 pairs receive such a
direct recount. The
paired-move score uses an exact inclusion-exclusion correction on triples
touching both chains. Equal-root pairs are excluded from the pair scan. In
`--full-all` mode their composition is itself a single-chain permutation,
and every such permutation appears among the single-chain events.

Reproduce with CPython 3.11 and GCC 12.2 or later:

```sh
python3 -B two_flip_landscape.py best4.txt
g++ -O3 -std=c++20 -Wall -Wextra -Wpedantic chain_pair_scan.cpp -o /tmp/schur-s6-chain-pair
/tmp/schur-s6-chain-pair best4.txt
/tmp/schur-s6-chain-pair best4.txt --full-root1
/tmp/schur-s6-chain-pair best4.txt --full-all
```

The first program reports `minimum_single 4` and `overall_minimum_pair 4`.
The C++ scans report `improving_pairs=0 best=4`. These statements use exact
integer counts; no solver result or heuristic objective is treated as a
Schur bound.
