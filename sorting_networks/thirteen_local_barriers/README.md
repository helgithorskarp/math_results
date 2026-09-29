# Local construction barriers for the thirteen-input incumbent

This source checks a compact obstruction certificate for two ways of trying to
shorten the published 45-comparator thirteen-input network. It does not exclude
arbitrary 44-comparator sorting networks and does not resolve their existence.

Actual author and executing agent: **six-sorting-1, researcher**, 2026-09-29.
The independent algorithms here were written and run by the same agent; this is
not an external review or a formal proof-assistant verification.

## Exact scope

`incumbent.txt` is the 45-comparator, ten-layer network labelled `N13L45D10` in
[Bert Dobbelaere's compilation](https://bertdobbelaere.github.io/sorting_networks.html#N13L45D10),
flattened in the order displayed within each layer. Its 45 gates are numbered
0 through 44. Comparator `(a,b)`, where `a<b`, places the smaller value on wire
`a`. The first line of the fixture is `13 45`.

The certificate `witnesses.txt` contains 174 distinct Boolean inputs. Its first
line is `13 174`. Each subsequent decimal integer `x` represents the input
whose wire `i` carries bit `i` of `x`, with wire 0 the least significant bit.
Every candidate in each of the following families fails at least one of these
174 inputs.

1. **Circuit repair:** delete any two of the 45 labelled gates, bypass their
   inputs and outputs along each wire, and insert one arbitrary standard
   comparator. Insert it at any cut of each of its two wire paths. Retain the
   original per-wire order of the other 43 gates and require the resulting
   circuit to be acyclic. Every topological schedule is covered, with no depth
   restriction. There are 990 deletion pairs and 4,458,189 labelled cut choices;
   2,290,014 choices are acyclic and 2,168,175 are cyclic. These are parameter
   counts, not numbers of distinct networks. Single-gate deletions are included
   by reinserting the second deleted gate in its former position.
2. **Contiguous block repair:** in the fixed flattened sequence, replace any
   of its 40 blocks of six consecutive gates by an arbitrary sequence of at
   most five standard comparators, leaving the prefix and suffix fixed. The
   checker covers all `40 * 78**5 = 115486974720` labelled strings of length
   five and separately excludes the empty replacement. Idempotence of the last
   comparator covers lengths one through four. Consequently no block of
   length at most six can be shortened by one: any such replacement extends
   to a replacement of a surrounding six-gate block.

In particular, a 44-comparator construction needs to leave both of these local
families. Preserving a 43-gate subcircuit of this incumbent with its original
wire order cannot succeed. These restrictions concern this specific network;
they are not normal forms for all sorting networks.

## Reproduce

Python 3.11.2 and GCC 12.2.0 were used. The checkers require only a C++20
compiler and its standard library; no SAT solver or third-party Python package
is used. All commands run one CPU job at a time.

From the repository root:

```bash
python3 sorting_networks/thirteen_local_barriers/verify.py \
  --work-dir scratch/thirteen-local-barriers --regenerate
```

The command first checks the fixture on all 8,192 Boolean inputs by direct
Boolean-list simulation, builds the two checkers sequentially, verifies both
barriers, and regenerates the 174-input certificate with an entry-by-entry
comparison. Expected principal output:

```text
incumbent: all 8192 Boolean inputs pass
certified=1 pairs=990 parameters=4458189 acyclic=2290014 cyclic=2168175 witnesses=174
complete=1 windows=40 strings=115486974720
complete=1 pairs=990 parameters=4458189 acyclic=2290014 cyclic=2168175 witnesses=174
regenerated certificate: byte-for-byte match
both local barriers verified; no global size lower bound claimed
```

Elapsed-time lines vary by host. Separate measured runs took about 0.5 seconds
for certificate generation, 2.7 seconds for the circuit checker, and 45 seconds
for the forty-window checker. Its two principal tables occupy about 8.5 MiB;
generated tables and binaries stay in the supplied scratch directory.

The exploratory window search can also be reproduced:

```bash
g++ -std=c++20 -O3 -Wall -Wextra -Wpedantic -Wconversion -Wshadow \
  sorting_networks/thirteen_local_barriers/search_windows.cpp \
  -o scratch/thirteen-local-barriers/search_windows
scratch/thirteen-local-barriers/search_windows \
  sorting_networks/thirteen_local_barriers/incumbent.txt \
  sorting_networks/thirteen_local_barriers/witnesses.txt \
  6 5 0 39 200000000
```

It completed 52,634,448 recursion nodes in about 84 seconds, with no added
witnesses and no restarts. A node limit is an operational stop and returns
`INCOMPLETE`, never a nonexistence claim.

## Why the checkers establish the stated scope

For circuit repair, the generator computes descendants of the two successor
gates at the insertion cuts. It rejects a placement if either predecessor lies
in this descendant set, exactly the condition for a new cycle. Otherwise it
schedules all retained gates outside the descendant set, the inserted gate,
then the descendant set, preserving the original order in each part.

`check_circuit.cpp` independently reconstructs the wire paths, input-port
connections and output ports. Recursive three-color visitation detects cycles;
each acyclic event computes its min and max output directly from its two parent
ports. It evaluates all 174 inputs in packed words and requires an adjacent
output inversion on at least one input for every acyclic placement. It uses
neither the generator's descendant criterion nor its scheduling algorithm.

For window repair, write a candidate as `P; R; S`. For each Boolean state `x`,
`check_windows.cpp` builds the bitset of all 6,084 ordered two-comparator
suffixes `(c,d)` for which `S(d(c(x)))` is sorted. It then enumerates all
474,552 ordered three-comparator prefixes `Q`. For each `Q`, the intersection
of those suffix bitsets over all `x = Q(P(h))`, with `h` in the certificate,
must be empty. An empty intersection rejects every two-comparator suffix at
once and hence every five-comparator string. The empty replacement is checked
directly. If a positive-length shorter replacement worked on the certificate,
repeating its last comparator would extend it to length five with the same
intermediate outputs, a contradiction.

`search_windows.cpp` supplies a distinct construction search. It uses exact
single-input distances to the fixed suffix's acceptance set, no-op deletion on
the current witness set, and commutation of disjoint comparators. It restarts
the window from the beginning whenever it adds a counterexample, so these
reductions always use one fixed witness set. The public window checker uses
none of these reductions and does not trust its search result.

Every arbitrary replacement that sorts all Boolean inputs would sort the
certificate inputs. Their failure therefore excludes the stated local family.
The zero-one principle promotes the incumbent's Boolean verification to sorting
over any totally ordered set. The local exclusions themselves need only the
necessary implication that a sorting network sorts every Boolean input.

## Validation and trust boundary

The circuit programs agreed on complete three-wire and four-wire known-optimal
fixtures (18 and 234 acyclic placements respectively). A redundant three-wire
network furnished a planted positive construction. The window checker verified
all three length-three windows of the four-wire optimal fixture against all 36
ordered two-comparator replacements each, and rejected
the same planted positive case as an insufficient obstruction certificate.
Address/undefined-behavior sanitizers passed the first 20 thirteen-wire deletion
pairs and the first six-gate window. Integer shifts stay within their unsigned
word widths, and counters fit in 64 bits at the supplied dimensions.

The mathematical trust boundary is the stated finite-family reduction, the
fixture and certificate parsing, ordinary C++ compilation and execution, and
the elementary comparator/bitset semantics. No unchecked solver result,
floating-point calculation, imported large proof corpus, or external numerical
data is required. No certificate minimality or global comparator lower bound
is asserted. This is a fixture-specific exact computational result; the cited
sources are not evidence of a priority claim for this local barrier.

SHA-256 values:

```text
incumbent.txt  f30f374c8f12472e7bbabdb23dfe980635b5640affbaf2b06c3bc2dbbbc22e5d
witnesses.txt  41335672c1ed9251ba687f9b9d44435b4de005cb0ef31429c20bacdb36fa3212
```

Primary context checked on 2026-09-29: the Dobbelaere compilation still reports
size bounds 44–45 for thirteen inputs; its live page and the
[SorterHunter repository copy](https://github.com/bertdobbelaere/SorterHunter/blob/master/sorting_networks.html)
were byte-identical. [Harder's paper](https://arxiv.org/abs/2012.04400) establishes
the optimal sizes for eleven and twelve inputs. This artifact adds a local
obstruction rather than a new global bound. The next construction frontier is
a repair affecting at least three incumbent gates and at least two added gates,
or a seven-gate-or-larger contiguous rewrite, or a different starting circuit.
