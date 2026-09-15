# Independent review and physical closure of the Moser S1 self-host gate

## Verdict

**ACCEPT AND STRENGTHEN**, with a strict family limitation.

The source package at commit
`7adb3cf0dc28ba85931c849001d353b53f01b1a5` correctly proves its stated
pre-expansion result: the 115-point graph `S1` has exactly 70 labeled copies
of the five-terminal metric frame, and the isolated blocker and host
relations share the canonical four-colour pattern `00001` in every frame.
The forcing chain excluding `00112` is also valid.

This review reconstructs the geometry that the source deliberately left out.
For each of the 70 frames it applies the unique exact plane isometry, merges
all coincident points of the two `S1` copies, reconstructs **every** unit edge
between every pair of physical points, and checks an explicit proper
four-colouring. Every complete physical union is therefore four-colourable.
Because every union contains the seven-point Moser spindle, every union has
chromatic number exactly **4**.

The complete unions have:

| quantity | exact range |
|---|---:|
| physical points | 115--197 |
| complete unit edges | 447--877 |
| incidental edges not internal to either copy | 0--74 |

Sixty-eight of the 70 unions have at least one incidental edge. Thus this is
materially stronger than intersecting isolated terminal relations: all of
those extra geometric contacts have now been included. The actual maximum
order is 197, below the source package's safe bound of 225, because every
frame has additional point coincidences beyond the five declared roles.

## Exact scope

This closes only the fixed family consisting of:

1. the specified first-reflection graph `S1` as blocker;
2. a second complete copy of the same `S1` as host;
3. the fixed ordered blocker terminals `(0,10,11,17,18)`; and
4. an isometry aligning a labeled host five-tuple with the same complete
   distance matrix to those five blocker terminals.

It does **not** exclude a different terminal tuple, a different host, a
partial or enlarged host, a placement fixed by fewer anchors, more than two
copies, later reflection rounds, or any other plane unit-distance
construction. It is a restricted-family negative result, not global
Hadwiger--Nelson progress and not a record candidate. The supported published
record remains the 509-vertex five-chromatic plane unit-distance graph.

These are actual plane realizations, not merely abstract chromatic graphs.
All coordinates lie in `Q(sqrt(3),sqrt(11))`; collision and unit-distance
tests use exact rational coefficient vectors, and the graph of every union
is rebuilt from all unordered physical point pairs.

## Reproduction

CPython 3.11 or later and the standard library suffice for verification:

```bash
python3 -B verify.py
python3 -O -B verify.py
python3 -B verify.py --controls
```

The full verification takes about 143 seconds on the review host. It imports
no source implementation and no SAT library. It independently rebuilds `S1`,
uses a distance-index intersection search for the 70 embeddings, constructs
each affine frame, and directly checks the committed colour words against the
complete exact edge sets.

To regenerate alternative positive words with a DIMACS solver that prints
standard `s SATISFIABLE` and `v` model lines and exits with status 10:

```bash
python3 -B generate.py --solver /path/to/kissat --output /tmp/certificate.json
python3 -B verify.py
```

The solver is only a witness producer. No solver `UNSAT` response enters the
proof: the committed checker validates every decoded positive word directly.

See [PROOF.md](PROOF.md) for the finite reduction and trust boundary, and
[VALIDATION.json](VALIDATION.json) for the recorded runs.

## Pinned inputs and record references

- reviewed package:
  <https://github.com/helgithorskarp/math_results/tree/7adb3cf0dc28ba85931c849001d353b53f01b1a5/hadwiger_nelson_moser_reflection_s1_host_gate>
- 25-point coordinate source:
  <https://github.com/helgithorskarp/math_results/tree/061fb2c248515bf6c7385304d2ea53187de4a44c/hadwiger_nelson_moser_all_terminal_contacts>
- Parts's 509-vertex record paper:
  <https://arxiv.org/abs/2010.12665>
- Haugland's August 2026 paper, whose introduction still identifies 509 as
  the current record: <https://arxiv.org/abs/2608.04542>
