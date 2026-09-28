# Three-colour trades cannot repair four explicit Schur assignments

**Family extension:** a [fixed-core criterion](CORE_FAMILY.md) now makes the
baseline splitting conclusion uniform over all valid 536-colourings fixing
225 specified positions. A checked Cartesian subfamily contains `2^53`
distinct valid colourings. Run `python3 -B check_core_family.py`.

**Stronger result:** every valid 537-colouring must split at least four
original colour classes of each of the four specified assignments. This
remains true after arbitrary colour relabelling and allows new entries
into otherwise intact classes. See [the splitting theorem and proof](SPLITTING.md)
and run `python3 -B check_splitting.py` for its separate certificate.

This directory proves 50 restricted exclusions relevant to the classical
sixth Schur number, with repeated summands included. It gives no new lower
or unrestricted upper bound for `S(6)`.

For the printed Fredricksen--Sweet 536-colouring, select any three colour
classes, add 537 to their union, and try to repartition that union into three
sum-free sets. **Every one of the 20 choices is impossible.** The other
three original classes remain fixed in this operation.

The same operation cannot repair any of three supplied 537-entry
near-colourings. Each has violations in exactly one old colour. All ten
three-colour palettes containing that colour are excluded for each input;
other palettes leave the old violation unchanged. A trade may change
arbitrarily many entries within its selected classes.

| Input | Original violations | Palettes excluded | Witness sizes |
| --- | --- | ---: | ---: |
| `baseline` | none on `[1,536]`; add 537 | 20 | 33–78 |
| `near537` | `12+12=24`, `12+24=36`, colour 4 | 10 | 14–31 |
| `team_near_190` | `22+22=44`, colour 1 | 10 | 21–79 |
| `team_near_359` | `2+2=4`, colour 2 | 10 | 25–83 |

There is also a necessary condition on **every** valid new colouring.
Connect old and new colour labels whenever an integer changes between
them. For the baseline, the connected component containing the new colour
of 537 must contain at least four labels. For each near-colouring, the
component containing its defective old colour must contain at least four
labels. [PROOF.md](PROOF.md) proves this implication and explains why it
does not count changed entries or changed old classes.

## Reproduce the exact result

CPython 3.11 or later; verification uses only the standard library.

```sh
cd schur_s6_three_colour_trades
python3 -B check.py
python3 -B test_checker.py
```

Expected checker output:

```text
PASS fixtures=4 palettes=50 nodes=791915 max_vertices=83
certificate_sha256=0a2af77d0ca4626641e77426d3a17bf7f7d056ecde5b3f117e3a422da7c900ea
```

The certificate is 11,748 bytes. Each row lists an induced additive
obstruction and an arbitrary root whose colour may be fixed by global
renaming. `check.py` independently checks every input's complete violation
list, palette coverage, witness containment, and non-three-colourability.
It exhausts a finite search using sound singleton propagation, including
two-vertex doubling constraints. It has no solver dependency or search
cutoff. `expected.json` records deterministic counts, not assumptions.
The complete check took about 18 seconds on one process in the author's
environment. Normal and optimized (`python3 -B -O check.py`) checks agree.

The four test groups include the known boundaries `S(1)=1`, `S(2)=4`,
`S(3)=13`; 1,024 comparisons with direct Cartesian-product enumeration;
60 additional deterministic three-colour controls using two different
fixed roots; doubling tests; and rejection of missing palettes, invalid
witness vertices and colourable claimed obstructions.

## Inputs and attribution

`fixtures.json` contains all four assignments as digit strings, plus
normalized-input SHA-256 hashes, expected violations and source links.
The finite results concern these exact strings; attribution is separate
from verification.

- `baseline` is the published [Fredricksen--Sweet construction (2000)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32),
  including the exceptional reflection pair 179/358. Its bytes match the
  [prefix-obstruction fixture](../schur_s6_prefix81_obstruction/baseline.txt),
  SHA-256 `2fdf85110de782426dd5deccfa7244f182441fda9870db64ba8e4eea7e3d600d`.
- `near537` comes from the [independent August 2026 attempt](https://github.com/umaia1234/agentic-conjectures/tree/main/problems/schur-6).
  The source file is `near_537_two_violations.col`, introduced in source
  commit `724761392945889c114aef4e802a5669379a4deb`.
  Its six rows are colour classes 1 through 6; our conversion assigns
  each listed integer its row number. The original file's SHA-256 is
  `ece0ce91784aca0199ffe24e36104c666c036a6c735181385fd2fabcc7627f25`.
  The candidate and its two-violation score are prior work, not our construction.
- The two team candidates are copied without relabelling from
  [Sol's doubling fixtures](../schur_s6_537_doubling_traps/fixtures.json),
  source commit `f666d69f54fd26212eacb860901f6453fddaac9a`.
  Their discovery and one-violation scores are credited to that contribution.

The [July 2026 shifted-template paper](https://arxiv.org/abs/2607.15034)
still uses the published bound `S(6)>=536`. Targeted literature and graph
searches on 2026-09-28 found no earlier statement of these exact palette
exclusions. This is a search-relative novelty assessment, not a priority
claim. The general trade reduction and elementary exchange-component
argument are included for clarity; no broad novelty is claimed for them.

## Discovery and remaining cases

Witness discovery used a separate guarded one-hot SAT encoding, CaDiCaL
1.9.5 through `python-sat==1.9.dev15`, and greedy vertex deletion with
deterministic shuffle seeds. `discover.py` provides this optional procedure:

```sh
python3 -m pip install python-sat==1.9.dev15
python3 discover.py near537 4 5 6 --seed 1 --budget 3000 \
  --output /tmp/schur-trade-candidate.json
```

This command proposes a witness; it does not certify it. Different deletion
orders or solver versions can give different witnesses. The published
finite theorem is reproduced directly by `check.py` without regenerating
the discovery search or trusting SAT UNSAT output. The displayed discovery
control produced the 14-vertex set `12*{1,...,14}`, independently checked
afterward.

The teammate fixture with multiplier 347 is **not covered** by this
publication. Its palette `{1,3,4}` was solver-UNSAT, but a direct independent
check of an 87-vertex witness did not finish within ten million search
nodes. The other checked cases do not establish the all-palette claim for
that fixture. Four-colour trades of the external `near537` candidate were
undecided at 200,000 SAT conflicts per palette. Neither unfinished check
is treated as an impossibility proof.

The result rules out repairs confined to three labels for the four listed
inputs. It leaves broader trades and unrestricted constructions open.
