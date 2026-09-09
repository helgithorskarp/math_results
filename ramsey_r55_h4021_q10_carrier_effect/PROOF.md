# Exact fixed-prefix effect

## Imported objects

h3987 partitions two q10 middle-degree branches into 260 physical child
prefixes.  Its checked ledger has 99 `CERTIFIED_UNSAT` records and 161
`UNKNOWN` records: 67 in `d20-22` and 94 in `d22-20`.  In every unknown
prefix the already fixed physical pairs are:

- 60 red pairs internal to ten labelled four-blocks on vertices 0 through 39;
- the three blue pairs of the core triangle on vertices 40, 41, 42;
- twelve root-block/core contact bits from one of 65 canonical 4 by 3 words;
- one branch pivot pair; and
- in 29 residual `d22-20` children, the additional forced red pair numbered
  148.

The first four items are distinct, so 132 tasks fix 76 edges and the 29
forced-residual tasks fix 77.

h4021's checked interface describes a forbidden partial coloring on 19
vertices.  It has 147 fixed pairs.  Its distinguished root is joined to all
other 18 template vertices in the selected color.  After substituting a
receiver's partial physical map, status `CONFLICT` means every cut literal is
fixed false, equivalently every one of the 147 prescribed template pairs is
already fixed to its template color.

## Star certificate

For any ordered h4021 embedding and either selected color, a `CONFLICT`
therefore requires the physical image of the root to have at least 18 incident
pairs already fixed in that color.  This is a necessary condition independent
of the placement of the five modules.

`analyze.py` reconstructs the exact h3987 ledger using h3987's generator and
then evaluates both fixed-color degrees at all 43 vertices in every one of the
161 unknown prefixes.  The independent checker instead brute-forces all 144
row/column actions on every 12-bit core word, rebuilds the 65 representatives,
rebuilds all 260 child records, and performs its own degree count.  Both find:

```text
maximum fixed red degree  = 6
maximum fixed blue degree = 6
eligible task/root/color triples with degree >= 18 = 0 of 13,846
```

Every ordered 19-position interface embedding belongs to exactly one of those
task/root/color triples.  Hence the number of direct conflict embeddings is
zero among

```text
161 * 2 * P(43,19)
  = 31,354,282,889,700,248,043,107,942,400,000
```

task-labelled embedding attempts.  `EXPECTED.json` reports the per-task-free
interface space `2*P(43,19)` as
194,747,098,693,790,360,516,198,400,000 and separately records all 161 tasks.
The consequence is zero newly closed tasks and 161 still unknown.

## Interface and controls

The producer imports the pinned h4021 `interface.py`, instantiates both colors,
and checks the 147-literal output and the 18 root polarities.  `controls.py`
uses the actual receiver on both colors and obtains each documented status:

- all 147 template pairs fixed as prescribed gives `CONFLICT`;
- leaving one root pair free gives a one-literal `CLAUSE`;
- fixing that root pair oppositely gives `TAUTOLOGY`.

It also makes two receiver calls on every one of the 161 q10 prefixes using an
identity-position embedding and observes no conflict.  These 322 calls test
the transport path; the universal conclusion comes from the independently
checked root-star implication, not from sampling.

The replay checks pinned SHA256 identities, compares two exact computations,
runs both under normal Python and `python -O`, and confirms rejection of six
deliberately altered result files.

## Claim boundary

This proves only zero **direct fixed-prefix** h4021 closures.  When template
pairs are free, the receiver can emit a nonempty valid clause.  We neither
enumerate all such clauses nor measure their possible CDCL effect.  A template
may occur in a completion of a q10 prefix.  No SAT task is decided, no partial
DRAT stream is promoted, no coloring is constructed, and no Ramsey lower bound
changes.
