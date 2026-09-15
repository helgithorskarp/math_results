# Independent review: Parts136 reverse receiver

## Verdict

**Accept with scope limitations.** At target commit
`119e7444ff958ce30e017dbff9fddfe45f5915f2`, the package
[`hadwiger_nelson_parts136_reverse_receiver`](../hadwiger_nelson_parts136_reverse_receiver/)
correctly certifies the complete unrestricted ordinary four-colour boundary
relation of the 136-point reverse Parts host. The relation has 41,025
canonical patterns, representing 984,516 fully labelled patterns. The
original 373-point removed module blocks every pattern.

This is a complete receiving specification with room for at most 372 new
physical points. It supplies no replacement, no five-chromatic graph below
509 vertices, and no new global bound.

## Independent physical reconstruction

`verify_review.py` imports no target module. It represents the coordinate
field as the nested tower `Q(sqrt(3))(sqrt(5))(sqrt(11))`, rather than either
of the target's flat radical multiplication routines, and checks all 129,286
unordered coordinate pairs exactly.

| object | points | internal unit edges |
|---|---:|---:|
| complete parent | 509 | 2,442 |
| retained host `H` | 136 | 564 |
| removed module `D` | 373 | 1,836 |

Exactly 42 edges cross the cut. Their host endpoints are the stated 19 pins
`[0,430,432,434,476,...,492]`, and those pins are independent in `H`. The
four complete edge streams agree entry-for-entry with fresh target output.
The target's parent five-word is proper on all 2,442 physical unit edges.

## Independent complete relation

The review uses two Boolean bits per colour, rather than the target's one-hot
encoding. Exhaustive truth tables check the four edge clauses and decoding.
Glucose 4 under PySAT 1.9.dev15 independently enumerated all host-colouring
orbits and terminated UNSAT after 376 seconds:

```text
canonical patterns       41,025
two boundary colours          7
three boundary colours    1,500
four boundary colours    39,518
fully labelled patterns 984,516
pattern stream SHA-256   f67f18e35fcd20c46c405c2b7458712091afd12f5fdeaee6443555735fb56649
```

Every independently produced 136-symbol word is checked against all 564 host
edges and its claimed boundary restriction. The independent and author
pattern sets agree exactly, while 40,287 of the 41,025 host words differ.

The labelled total correctly accounts for unused-colour stabilizers. Each
pattern using `k` colours has `24/(4-k)!` labelled images; multiplying every
canonical row by 24 would overcount the seven two-colour rows by 84.

## Structurally independent negative certificates

The independently generated completeness CNF has 272 variables and 248,408
clauses. It fixes vertex 0 to binary `00`, enforces every host edge, and blocks
all six origin-fixing images of every listed boundary pattern. A satisfying
assignment would decode to an omitted host pattern, and every omitted pattern
would satisfy it. CaDiCaL 1.9.5 returned UNSAT; `drat-trim` reported
`s VERIFIED` for the fresh trace.

The complete parent is separately encoded with 1,018 binary variables and
9,770 clauses. Its fresh DRAT trace also verifies. Together with the proper
five-word, this proves the physical parent is exactly five-chromatic.

| obligation | CNF SHA-256 | DRAT SHA-256 |
|---|---|---|
| host relation complete | `20c598da6dd0996515aad70d8012e89596c45d7517105191454dafccc58be402` | `3eb0e0a66b5d019e4b05f612b2f6381bc6726b67bfe5f76486b206d45539f0c7` |
| parent not four-colourable | `17277d4755cc4cc374061d9a6767af4db5febf1625066b357e65cdccaa60a40d` | `258c3b9d1715136f54d4b0a94a2cd267388c43cd117d63147943113f4fcc9803` |

The target's fresh one-hot generation also reproduced the complete witness
table, pattern stream and both CNFs byte-for-byte under the reviewer's newer
PySAT build. Both supplied author DRAT proofs replay successfully. Those
checks corroborate, but do not replace, the binary evidence.

## Why the module blocks and what a replacement must do

Every parent edge is internal to `H`, internal to `D`, or one of the 42
recorded `B`--`D` edges. If a colouring of `D union B` agreed on `B` with a
host colouring, they would glue to a four-colouring of the parent, contradicting
the checked parent certificate. Thus the original module blocks all 41,025
host patterns.

For a future replacement, let `X` be its distinct points outside `H` after
collision merging. The sub-509 allowance is `|X|<=372`; a replacement that
lists the 19 shared pins has at most 391 vertices including them. If it shares
only those pins with `H` and every new--host contact occurs there, empty
intersection of the two complete boundary relations is necessary and
sufficient for non-four-colourability of the exact union.

Any extra coincidence or unit contact with `H` outside those pins invalidates
the 19-pin reduction: enlarge the actual interface or check the complete
physical graph. A candidate must also have at most 508 merged points, include
every unit edge, provide a proper five-word, and retain independently
checkable non-four evidence. The benchmark module has 373 new points and is
one point over budget; the review supplies no smaller blocker.

## Reproduction

Use CPython 3.11 and PySAT 1.9.dev15. Keep all generated tables, CNFs, traces
and logs outside Git:

```bash
python3 -m venv /tmp/parts136-review-venv
/tmp/parts136-review-venv/bin/pip install -r requirements.txt

/tmp/parts136-review-venv/bin/python -B enumerate_binary.py \
  --out /tmp/parts136-review-enum --solver glucose4 --seconds 900

/tmp/parts136-review-venv/bin/python -B verify_review.py \
  --relation /tmp/parts136-review-enum/host_relation.tsv \
  --out /tmp/parts136-review-cnf

/tmp/parts136-review-venv/bin/python -B controls.py \
  --source ../hadwiger_nelson_parts136_reverse_receiver \
  --relation /tmp/parts136-review-enum/host_relation.tsv

/tmp/parts136-review-venv/bin/python -B certify_binary.py \
  --cnf-dir /tmp/parts136-review-cnf \
  --out /tmp/parts136-review-proofs \
  --cadical /path/to/cadical --drat-trim /path/to/drat-trim --seconds 900
```

The 6.44 MB relation, 39.3 MB completeness CNF, 75.1 MB completeness
proof, and 27.8 MB parent proof are omitted. `EXPECTED.json` freezes the
theorem-bearing checker result; `VALIDATION.json` freezes run and proof
metadata; `SHA256SUMS` covers the compact package.

## Record, Discovery and trust boundary

Parts's paper reports the 509-point, 2,442-edge construction, and Haugland's
2026 spindle-free paper still identifies 509 as the unrestricted size record.
This receiver is an actual plane cut but not itself a non-four-colourable
replacement or record candidate.

A final bounded team refresh also inspected the later Moser S1 self-host gate
and the author's direct archive-module intake. The former has a common
four-colour terminal pattern in all 70 selected frames; the latter finds no
existing blocker inside the 372-point allowance. These are restricted intake
stops, not objections to or premises of the receiver theorem.

The target's Discovery contribution
`bafkreiezmeip5lbeqvxsbvhkdh7fjl6sj5c76et3jqg5aezm2niay5rnsu` received
CheckTx code zero but remains pending/unindexed. The committed index was stale
at height 4,363 while RPC remained frozen at 4,364. A review submission must
therefore relate only to the committed Hadwiger--Nelson problem until both
artifacts commit.

The proof trusts the pinned coordinate source, CPython arbitrary-precision
integers, the small tower/encoding/checker implementations, PySAT and Glucose
only for positive enumeration, `drat-trim` for the negative certificates,
SHA-256 for identity comparisons, and ordinary hardware. CaDiCaL generates
the retained DRAT traces but its UNSAT exit alone is not trusted. This is
independent computer-assisted evidence, not proof-assistant formalization or
a novelty-priority claim.
