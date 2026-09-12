# Complete monotone-chain Ramsey carrier reduction

Every ordered maximal-K4-packing task admits a disjoint, exactly indexed
partition into monotone chains of physical graphs. Each chain needs at
most one graph checked after locating its first blue-K5-free state; a
negative chain has at most two forbidden vertex-set witnesses and a
one- or two-line RUP proof under its chain constraints.

This reduces candidate obligations in **every original task** and in
**all 956 physical q8 cohorts**. The q8 factor is exactly
`15^88/A_88 = 20.184077869788...`, where

```
A_m = ([z^0]+[z^1]) (5+3z^2+3z^-2+z+z^-1+z^3+z^-3)^m.
```

The strict factors for q=7,8,9,10 are respectively >22, >20, >17, >11.
The reduction holds within each fixed core/block-to-block frame, with
no symmetry assumption. See [PROOF.md](PROOF.md) for the full theorem,
explicit partition, count, physical certificate bridge, and trust model.

**No original task or physical cohort is closed. No good43 or new Ramsey
bound is obtained. No runtime speedup is asserted.** A graph can change
within its original task during the reduction. These are not extra
implicates satisfied by every labeled original model. The result does
not compose multiplicatively with the earlier core-exchange normal form.

## Reproduce

Python 3.11+ standard library suffices for the core tests and receiver.
Run from the repository root:

```sh
python3 -B ramsey_r55_monotone_chain_carrier/reproduce.py --counts > /tmp/chain-counts.json
cmp /tmp/chain-counts.json ramsey_r55_monotone_chain_carrier/COUNTS.json
python3 -B ramsey_r55_monotone_chain_carrier/reproduce.py > /tmp/chain-controls.json
cmp /tmp/chain-controls.json ramsey_r55_monotone_chain_carrier/EXPECTED_CORE.json
```

For the optional original-task bridge controls, provide the four existing
McKay Ramsey(4,4) files `r44_3.g6`, `r44_7.g6`, `r44_11.g6`, `r44_15.g6`
in one directory. Their sources, exact hashes, and imported completeness
premise are in the pinned parent
[INPUTS.json](../ramsey_r55_global_maximal_packing/INPUTS.json).
No bulky input is duplicated here. For external RUP replay supply the
DRAT-trim executable at author source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.

```sh
python3 -B ramsey_r55_monotone_chain_carrier/reproduce.py \
  --catalog /path/to/catalog \
  --drat-trim /path/to/drat-trim > /tmp/chain-full-controls.json
cmp /tmp/chain-full-controls.json ramsey_r55_monotone_chain_carrier/EXPECTED_FULL.json
```

The external checker reports `s VERIFIED` for all three negative fixtures.
That pinned checker returns 1 for an input already containing an empty
clause, with `c trivial UNSAT`; the harness recognizes only that exact
case alongside its usual successful exit 0. It never accepts a status
without the checked physical witness and internal RUP validation.

The checks include 44,100 rectangle points, 78,556 states across complete
small star products, and **all 27,000 graphs** in the small physical
class consisting of a red root K4 and every three-vertex core. All 6,856
chain decisions agree with literal examination of every graph in that
class. A known good42 gives a positive physical control; the negative
fixtures exercise both endpoint cases, an interior cut, and residual
red-K4 maximality. Seven corrupted packets must be rejected. The full
run additionally tests 54 exact 903-bit graph round trips across all
18 original macro classes, plus 24 beginning/middle/endpoint physical
cohort decodes spanning all four bases and both guard sizes, and six
additional decodes of the exact active M8 positive-edge interval.

These controls validate the theorem's implementation, not a new Ramsey
subcase. There are zero target-solver calls and zero new task verdicts.

## Receiver

A canonical frame is JSON with `n,q,r,fixed_hex`. Bits follow the
lexicographic ordering of unordered physical pairs. Star bits in the
frame must be zero; all other bits are fixed. Production scope is n=43,
q=7..10, r=5..q, or one of the four physical q8 bases. Smaller dimensions
are accepted for the documented controls only.

```sh
python3 -B ramsey_r55_monotone_chain_carrier/receiver.py /path/to/frame.json 0 > /tmp/packet.json
python3 -B ramsey_r55_monotone_chain_carrier/check.py /tmp/packet.json --proof-prefix /tmp/chain
```

`chains.Product` provides exact chain integer rank/unrank and maps any
old star vector to its unique chain and position. The `mc1` packet
contains the frame, chain index, explicit hook path, cut, and literal
witness vertices. The checker rebuilds the entire chain independently.
It emits `/tmp/chain.cnf` and `/tmp/chain.drat` for a closed chain.

`bridge.OriginalTask(name, catalog_dir)` provides the exact old-task to
new-code interface. `address_old(graph)` returns a new chain code and
position; `decide(code)` returns the physical packet. The complete size
is `frame_count * chains_per_frame`. `bridge.physical_guard` validates
an actual M_r core guard on a packet's unchanged core, including cores
that are not catalog representatives. `bridge.PhysicalCohort(r, guard)`
provides an exact integer code over the **entire** physical guard cylinder
and needs no catalog data. Set `require_edge119=True` for the complete
active positive branch of M8. Both adapters expose `check(wrapper)` to
validate the task/base, guard, frame and chain identity before accepting
a packet. They do not read or operate any carrier queue.

A parent receiver must validate the **complete range** of frames and
chains before closing that parent. A chain proof cannot be imported as
an unguarded parent RUP lemma. [HANDOFF.md](HANDOFF.md) records this
boundary and the measured complete-carrier consequence.

## Provenance

[DEPENDENCIES.json](DEPENDENCIES.json) pins the relevant source files.
[CONTEXT.json](CONTEXT.json) records the fresh committed graph and source
review state. [COUNTS.json](COUNTS.json) contains exact full-size integers;
the decimal ratios are display only. Source and compact evidence are
covered by `SHA256SUMS`. No private ledger, key, raw catalog, queue state,
or large proof trace is included.

The partition method and RUP are classical; no priority claim is made.
The new application has author checks, with independently structured
count and physical-certificate implementations, but no external review
or proof-assistant formalization. Global good43 coverage retains the
parent catalog and Ramsey-number trust boundaries stated in the proof.
