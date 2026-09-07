# Complete nontrivial separator exclusion for good43 graphs

Every 43-vertex graph with no clique or independent set of order five has
**no separator of order at most 19 splitting off two parts of order at least
two**. At separator order 20, only the 10+13 side-size profile survives the
proof, and it forces minimum degree at most 20. Thus, in each color,

    kappa(G) >= min(delta(G),21),

with equality when delta(G)<=21. Singleton separator exceptions remain.
This improves the earlier unconditional connectivity-18 theorem and removes
the triangle-cap assumptions from the earlier nontrivial separator-18
classification. See [PROOF.md](PROOF.md) for the proof, prior work and exact
scope. No good43 graph or new Ramsey-number bound is claimed.

The new mechanism grows a clique of separator vertices onto a side with
independence number two. Ramsey bounds limit the sizes of the resulting
contact classes, which together must cover the separator. A separate
attachment-type count handles clique sides. The sole external computational
input is the classical R(4,5)<=25 theorem; no catalog or N5 classification
is needed for this argument.

## Reproduce

Python 3.11.2, standard library only. From this directory:

```sh
python3 reproduce.py > reproduced.json
python3 -O reproduce.py > /tmp/r55-separators-optimized.json
cmp expected.json reproduced.json
cmp expected.json /tmp/r55-separators-optimized.json
sha256sum -c SHA256SUMS
```

The scripts fail on missing/mismatched evidence. No solver is invoked. The
reported outputs are deterministic; resource measurements are recorded
separately in `VALIDATION.md`.

- `cases.py` produces the complete 21-row arithmetic certificate in
  `cases.json`. `check_cases.py` independently reconstructs the domain by
  compositions and tests all 49,054 integer attachment populations. All
  sixteen cases through order 19 are excluded. At order 20 only
  (side sizes 10,13; both independence numbers 2) remains, with delta<=20.
- `branches.py` defines two full F27 branches, fixes a 12-by-12 homogeneous
  cut, and streams their Ramsey clauses by compatible-clique enumeration.
  `check_branches.py` instead inspects all 3,850,392 physical monochromatic
  events across both branches and checks the full literal-stream digests.
  `branches.json` preserves all pins, partitions, clause statistics and
  cut clauses; no large CNF is stored.
- `controls.py` checks clique growth on all 33,867 labeled graphs of orders
  1 through 6, 6,144 anticomplete attachment graphs, and 37,376 clique-side
  attachment graphs. It also checks cut-clause signs and physical-to-frame
  variable transport and rejects malformed evidence.

The proof establishes the general theorem. Finite arithmetic checks and
small-graph controls support the reasoning but do not formally verify it.
The two implementations are internally separate algorithms, not independent
external research or peer review.

## Target-facing output

Both complete cut branches have **698 free physical pairs**; all 2^698
assignments in each are excluded. Their fully substituted Ramsey formulas
have 880,692 and 934,584 clauses respectively, each with no initial empty or
unit clause. This is a full branch decision beyond the normal form, without
a fixed-neighborhood subsystem, a symmetry assumption, or a solver cap.
It does not decide the rest of the 842-variable global F27 family.

For any disjoint vertex sets A,B of size at least two and combined size at
least 24, the proof gives a clause forbidding a constant-color A-B cut.
`nogood.py` emits this reusable consequence in the 903 physical variables
numbered by lexicographic pairs 01,02,...,0:42,12,...,41:42. Its input is JSON
with fields `a`, `b`, `cross_color`, where 0 is blue and 1 is red. For example:

```sh
python3 -c 'import json; print(json.dumps({"a":list(range(12)),"b":list(range(12,24)),"cross_color":0}))' > /tmp/r55-cut.json
python3 nogood.py /tmp/r55-cut.json
```

The output is one theorem-derived 144-literal clause. It is a valid
consequence of the full Ramsey constraints, not the whole formula or a
DRAT certificate. The two specific F27 cut clauses in `branches.json` use
the original **842-variable** frame numbering instead. The independent
checker verifies their transport to the physical numbering.

F27's separate universal-coverage argument retains its published N5=21
premise. Only the previously published frame definition is used to describe
the two branches here. The proof of their exclusion does not use that
coverage premise, earlier monolithic solver output, or the parked
neighborhood-gluing route. No claimed optimality or historical priority.
