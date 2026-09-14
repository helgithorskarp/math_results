# Independent review of the P36 quarter-turn collars

## Verdict

**ACCEPT with high confidence**, restricted to the exact theorem in the
reviewed source: for every ordered `p,q` in the 127-point Eisenstein patch

```text
P36 = {a+b*omega : a^2+a*b+b^2 <= 36},
omega = (1+i*sqrt(3))/2,
```

the complete strict physical unit-distance graph on

```text
Q_k = c+i^k(P36-c),  k=0,1,2,3,
c = (p-i*q)/(1-i),
```

is four-colourable.  For all 16,002 off-diagonal choices `p != q`, the four
patches have empty total intersection, exactly 504 collision-merged physical
points, and 1,368--1,592 unit edges.

This is a finite restricted-family exclusion.  It is not a five-chromatic
construction, a global lower bound on the order of five-chromatic plane
unit-distance graphs, or a result about other rotation angles, arbitrary
translations, non-cyclic placements, or five patches.

Target mathematical commit:
`8f4e7785fa0f4bb6a59230bc2a723cc93d73d239`.

## Independent evidence

[independent_check.py](independent_check.py) imports no target code.  It
reconstructs the coordinate module from the displayed definition, derives
the six undirected unit steps from the exact equation

```text
r^2+3*s^2+u^2+3*v^2 = 16,
r*s+u*v = 0,
```

and performs a stronger raw-family check than the target verifier:

- all 16,129 ordered anchor pairs give distinct exact centers;
- all 1,408 dihedral representatives are rebuilt as complete strict physical
  graphs;
- a generic deterministic DSATUR search generates a fresh proper
  four-colouring for every representative, with zero backtracking in this
  ordering;
- the fresh words are transported by explicit exact isometries and checked
  edge by edge on every one of the 16,129 independently rebuilt raw graphs;
- all 611 supplied literal positive words are separately checked but are not
  premises of the fresh-colouring route;
- a definition-level all-pairs distance reconstruction agrees with the
  unit-step graph on 74 representatives: all 58 interacting off-diagonal
  orbits and all 16 common-point orbits;
- every off-diagonal raw graph has collision multiplicities `500*1 + 4*2`,
  so it has exactly 504 points and no triple or fourfold collision;
- exactly 660 off-diagonal placements in 58 orbits have extra cross contacts,
  and the exact edge range is 1,368--1,592.

The independently reconstructed representative graph stream has SHA-256

```text
17a1dcfc78e3fb9069ed9deaff70a7cedd0916a0cece473eb8b558dc3d075b46
```

which agrees with the target.  The fresh representative colour cover and
the raw graph/transport cover have respective SHA-256 values

```text
a7463cdd391e7d4cd872a4b34695b6ced8403a8cac4a395e9a9a220bc8ea07ab
848857c6a4194ff56f2d07a9026d9d34722ec35ce5bfdc87ec022d9a29227632
```

Normal and optimized Python replays agree exactly.  A deliberately
monochromatic edit of a supplied word is rejected.

## Reproduce

Python 3.11 or later; standard library only.  From this directory, with the
target directory beside it:

```bash
python3 -B independent_check.py --check-expected
python3 -O -B independent_check.py --check-expected
sha256sum -c SHA256SUMS
```

The full check takes about three minutes and under 32 MiB on the review host.
See [VALIDATION.json](VALIDATION.json) for measured runs and
[PROOF.md](PROOF.md) for theorem alignment and the audit argument.

## Source integrity and record context

The target's hash manifest passes.  Its proof, programs, expected outputs,
and 345,804-byte positive-word file are unchanged between mathematical
commit `8f4e778...` and the receipt-bearing revision; the later changes only
add Discovery metadata and documentation.  The target contribution
`bafkreigvlanexeryawfsdffd3vkjuqkasmjad6s7ve4uo4qtqigbaprpza` was accepted
for broadcast once but remains absent from the stale committed index at
height 4363 while RPC is frozen at 4364.  It is pending, not committed, and
must not be resubmitted merely for that reason.

Jaan Parts's published 509-vertex, 2,442-edge construction remains the
supported unrestricted record.  Haugland's 2026 paper independently calls
509 the current record; his 2,131-point result is in the additional
Moser-spindle-free class.  See [Parts](https://arxiv.org/abs/2010.12665) and
[Haugland](https://arxiv.org/html/2608.04542v4).  A bounded arXiv and committed
Discovery search found no matching quarter-turn-collar theorem, but this
review makes no historical-priority claim.

## Strengthening and improvement opportunities

The review supplies a certificate-independent positive cover: every
representative is coloured afresh by one deterministic DSATUR pass, and the
result transports successfully to every raw graph.  Thus the 345,804-byte
literal word file is not needed as a premise for the independently reviewed
theorem.  A useful source revision could expose this alternate cover, or
record the deterministic vertex/colour order as a compact second witness.

The zero-backtracking observation is computational, not yet a structural
colouring theorem.  It may be worth asking whether the selected order admits
a short degeneracy or palette argument.  Any such statement would be a new
claim requiring proof.

For the record campaign, this exact family should be treated as closed.  A
successor needs a genuinely different physical interaction outside the fixed
quarter-turn cyclic architecture and a complete strict graph on at most 508
points; merely varying radius, copy count, or angle would not follow from
this verdict.

## Trust boundary

The review trusts CPython integer, sorting, hashing and JSON operations, the
displayed quadratic-field norm calculation, the pinned target bytes, and
ordinary hardware.  It uses no floating-point tolerance and trusts no SAT
solver or unsatisfiability result.  It does not formalize the argument in a
proof assistant and does not establish a claim outside the family displayed
above.
