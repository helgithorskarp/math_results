# A degree-preserving switch barrier at 238 Cyclic(43) objective-12 states

This package exactly classifies alternating 2-switches at all 238 saved
objective-12 addition representatives in the certified primary Cyclic(43)
landscape. Every representative is a strict local minimum for this
degree-preserving four-edge move. Among 12,056,241 source-indexed switches,
none is neutral or descending, and every endpoint has at least 17
monochromatic copies of `K5`.

The exact minimum-neighbor histogram over the 238 sources is

```text
17:10, 18:5, 19:27, 20:84, 21:58, 22:54.
```

There are 502 switches attaining the source-specific minima. The package
also exhausts every second alternating 2-switch from all 502 endpoints.
Across 25,424,492 second switches, the only 502 descending moves are the
inverse moves back to the objective-12 sources; these are also the only 502
endpoints at objective 12. No second endpoint lies below 12.

Thus a candidate search which preserves these degree sequences cannot leave
one of the 238 states by a non-increasing 2-switch, and crossing by a cheapest
first switch gives no two-switch path to a better objective. This is a finite
local barrier theorem, not a construction of a Ramsey `(5,5;43)` graph, not a
global minimum theorem, and not a change to the known bounds on `R(5,5)`.

## Move and input

Number vertices by `Z/43Z` and color a seed edge red when its cyclic length is
in

```text
{1,2,7,10,12,13,14,16,18,20,21}.
```

The input states are the complete
`complete_additional_objective_12_rotation_representatives` array in
[`../ramsey_r55_cyclic43_q13_boundary_certificate/objective-twelve-component-fast.json`](../ramsey_r55_cyclic43_q13_boundary_certificate/objective-twelve-component-fast.json).
Its SHA-256 is
`4803b2e40dba06c0f82c3d23cbd5ae0a9127da0db24e5655971fff179fb68ec3`.
Every array entry is a list of lexicographic edge indices toggled from the
cyclic seed. The programs directly recount all 962,598 five-sets at every
source and find objective 12; completeness of the 238-state parent list is
inherited from the earlier certified computation.

For four distinct vertices, choose two of their three perfect matchings. If
the first matching's two edges have one color and the second matching's two
edges have the opposite color, toggling their four edges is an alternating
2-switch. Every vertex loses one red edge and gains one, so its red degree is
unchanged. The enumeration considers every four-set and every unordered pair
of perfect matchings, hence every such physical switch exactly once.

## Reproduction

Requirements are a C++20 compiler, Python 3.11 or later, and the sibling input
file above. From the repository root run

```bash
python3 -B ramsey_r55_cyclic43_q12_switch_barrier/reproduce.py \
  /tmp/r55-q12-switch-replay
```

The script builds four programs, regenerates both TSV certificates
byte-for-byte, runs two independent exhaustive checkers, and confirms that a
corrupted certificate is rejected. Expected headline output is stored in
[`EXPECTED_OUTPUT.txt`](EXPECTED_OUTPUT.txt). On the research host the four
enumerations together take about one minute.

`analyze_switches.cpp` uses a smallest-vertex bitset triangle count to update
the exact number of monochromatic five-sets after a flip. The independently
written `verify_switches.cpp` instead uses

```text
T(S) = (1/3) sum_{v in S} e(S intersect N(v)).
```

The two-level analyzer and verifier inherit their respective primary and
independent kernels. Both directly recount each objective-12 source before
enumeration and compare every per-source table entry, not only the totals.

## Scope

The theorem concerns exactly the 238 persisted addition representatives and
the stated alternating 2-switch neighborhood. It does not cover all
69,071,588 rotation orbits in the primary sublevel-12 component, arbitrary
edge moves, longer degree-preserving paths, disconnected low-objective
components, or any h3987/q10 survivor. The source-indexed switch totals are
not counts of distinct colorings after quotienting across different sources.

The result explains why a direct degree-preserving repair from these durable
Cyclic(43) boundary states fails and supplies a checked barrier for future
nonlocal construction mechanisms. No historical-priority claim is made.
